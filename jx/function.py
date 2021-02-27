# coding=utf-8

import json
import os
from jx.models import *
from jx.util import *
from jx.views import check_login, sys_error
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.forms.models import model_to_dict
from django.db.utils import *
from django.conf import settings
import pandas as pd


rule_tables = ['khpc', 'jxkhgz', 'khgzdz', 'khjgmx', 'khjghz', 'bcykh',
               'kh_khpc', 'kh_jxkhgz', 'kh_khgzdz', 'kh_khjgmx', 'kh_khjghz', 'kh_bcykh']


def get_field_name(s):
    """
        Refer to below get_static_data to get [col1,col2,...] used by FE Jinja2
    """
    try:
        return s[s.find(':')+1:].split(',')
    except:
        logger.error(sys_info())
    return []


def get_static_data(payroll, s, where=''):
    """
        Transfer select data from DB to FE by Jinja2 templates->function method
        s: "table_name:col1,col2,..."
        where: additional where condition to get dynamic data
        TODO: more where condition, e.x.: 'DWH IN %(departments)s'
    """
    try:
        sql = "SELECT " + s[s.find(':')+1:] + " FROM " + s[:s.find(':')]
        if where != '':
            condition = ""
            if where.find('DWH IN %(departments)s') != -1:
                from jx.module import VIEW_JZGJCSJXX
                ds = VIEW_JZGJCSJXX.get_managed_departments(payroll)
                condition = " WHERE " + where % {'departments': str(ds).replace('[', '(').replace(']', ')')}

            sql += condition

        cursor = connection.cursor()
        logger.info(sql)
        cursor.execute(sql)
        sql_result = dictfetchall(cursor)

        return sql_result

    except:
        logger.error(sys_info())

    return []


def get_column_info(class_name, field):
    try:
        model = __import__('jx.module', fromlist=(["module"]))
    except ImportError:
        model = __import__('module')

    if class_name in rule_tables:
        try:
            model = __import__('jx.rule', fromlist=(["rule"]))
        except ImportError:
            model = __import__('rule')

    model_class = getattr(model, class_name.upper())
    columns = model_class.get_title_columns()

    try:
        for column_ in columns:
            if column_['field'] == str(field):
                return column_
    except:
        logger.error(sys_info())

    return {}


def calculate_kpi(departments, year, start, end, _payroll, db):
    from jx.rule import KH_JXKHGZ, KH_KHJGMX, KH_KHGZDZ, KH_BCYKH

    # 获得参与部门的已启用规则
    active_gzh = []
    gzdz_query = db.query(KH_KHGZDZ)
    gzdz_query = gzdz_query.filter(KH_KHGZDZ.DWH.in_(departments), KH_KHGZDZ.KHNF == year, KH_KHGZDZ.GZQY == '已启用')
    gzdz_data = gzdz_query.all()
    if not gzdz_data:
        import datetime  # for year.strftime
        logger.error('no active rules for ' + str(_payroll) + '@' + year.strftime("%Y"))
        return
    for gzdz in gzdz_data:
        active_gzh.append(gzdz.GZH)

    # 获得参与部门的不参与考核教职工
    bcykh = []
    bcykh_query = db.query(KH_BCYKH)
    bcykh_query = bcykh_query.filter(KH_BCYKH.DWH.in_(departments), KH_BCYKH.KHNF == year, KH_BCYKH.CYZT == '不参与')
    bcykh_data = bcykh_query.all()
    for data in bcykh_data:
        bcykh.append(data.JZGH)

    # 获得参与部门的所有运算规则
    rules_query = db.query(KH_JXKHGZ)
    rules_query = rules_query.filter(KH_JXKHGZ.DWH.in_(departments), KH_JXKHGZ.GZH.in_(active_gzh))
    rules = rules_query.all()

    # 对获得的每个规则进行运算
    for rule in rules:
        try:
            # 根据规则定义的参与考核的类名获得参与考核对象
            # TODO: All modules SHOULD have JZGH(payroll), stamp
            class_to_check = rule.get_input_class()  # get class to check
            data_query = db.query(class_to_check)  # query out by class defined in rule
            data_query = data_query.filter(class_to_check.DWH.in_(departments))
            data_query = data_query.filter(class_to_check.JZGH.notin_(bcykh))  # filter out not included JZGH
            data_query = data_query.filter(class_to_check.stamp.between(start, end))  # filter stamp out of start-end
            data_query = data_query.order_by(-class_to_check.id)  # order which is useless in rule calculation
            data = data_query.all()  # get dataset
            if len(data) == 0:
                continue

            for x in data:  # for each data
                logger.debug(x.__dict__)
                try:
                    if not rule.match(x):  # match rule condition
                        continue

                    logger.debug(rule.calculate(x))
                    logger.debug(rule.get_output_template() % x.__dict__ % rule.__dict__)

                    # Save
                    obj = KH_KHJGMX(
                        JZGH=x.JZGH,
                        DWH=rule.DWH,
                        GZH=rule.GZH,
                        KHNF=year,
                        KHJD=rule.calculate(x),
                        KHMX=rule.get_output_template() % x.__dict__ % rule.__dict__
                    )
                    db.add(obj)
                except:
                    logger.error(sys_info())
                    pass

                db.commit()
        except:
            logger.error(sys_info())
            pass
    return


def summarize_kpi(departments, year, db):
    from jx.rule import KH_KHJGMX, KH_KHJGHZ

    data_query = db.query(KH_KHJGMX)
    data_query = data_query.filter(KH_KHJGMX.DWH.in_(departments), KH_KHJGMX.KHNF == year)
    data_set = data_query.all()

    set_query_all = db.query(KH_KHJGHZ)
    for data in data_set:
        def save(DWH, KHNF, JZGH, GZH, cur=False):

            set_to_query = set_query_all.filter(
                KH_KHJGHZ.DWH == DWH, KH_KHJGHZ.KHNF == KHNF,
                KH_KHJGHZ.JZGH == JZGH, KH_KHJGHZ.GZH == GZH
            )
            set_to = set_to_query.all()
            obj = None
            if not set_to:
                obj = KH_KHJGHZ(DWH=DWH, KHNF=KHNF, JZGH=JZGH, GZH=GZH, KHJDHJ=0.0)
                db.add(obj)
            else:
                obj = set_to[0]

            obj.KHJDHJ += data.KHJD
            obj.save()
            db.commit()

            if cur:  # 按上级部门汇总绩点
                logger.info(obj.LSDWH)
                if obj.LSDWH and trim(str(obj.LSDWH)) != '' and obj.LSDWH != 'None':
                    obj = save(obj.LSDWH, KHNF, JZGH, GZH, cur)
            return obj

        save(data.DWH, data.KHNF, data.JZGH, '', False)  # 汇总教职工个人绩点
        save(data.DWH, data.KHNF, '', data.GZH, True)  # 按规则汇总部门绩点
        save(data.DWH, data.KHNF, '', '', True)  # 按部门汇总绩点

        db.commit()
    return


def role_inline_edit(req):
    try:
        if req.method != 'POST':
            return JsonResponse({'success': False, 'msg': '消息类型错误！'})

        usercode = req.COOKIES.get('payroll')
        if usercode is None:
            return JsonResponse({'success': False, 'msg': '请重新登录！'})

        user = SysUser.objects.get(payroll__exact=usercode)
        if user.role_id not in (1, 2):
            return JsonResponse({'success': False, 'msg': '登录用户没有权限！'})

        payroll_number = req.POST.get('payroll', '')
        if payroll_number == '':
            return JsonResponse({'success': False, 'msg': '参数错误！'})

        payroll_user = SysUser.objects.get(payroll__exact=payroll_number)
        payroll_user.role_id = int(req.POST.get('role_id', '4'))
        payroll_user.save()
        return JsonResponse({'success': True, 'msg': '修改成功！'})

    except SysUser.DoesNotExist:
        return JsonResponse({'success': False, 'msg': '用户不存在，请重新登录！'})

    except:
        return JsonResponse({'success': False, 'msg': '系统异常，请联系管理员！'})


def getpower(req):
    role_name = req.GET.get("role_name", "")
    cursor = connection.cursor()
    sql = """
        SELECT a.id, a.menu_name, a.menu_classify, b.permission
        FROM jx_menu a 
        LEFT JOIN jx_role_menu b ON b.menu_id = a.id
        LEFT JOIN jx_role c ON c.id = b.role_id
        WHERE c.role_name=
    """ + "'" + role_name + "'"

    cursor.execute(sql)
    sql_result = dictfetchall(cursor)
    for a in sql_result:
        c = []
        b = a['permission'].split(',')
        for num in range(0, 6):
            if b[num] == 'y':
                c.append(str(int(num) + 1))

        str1 = ','.join(c)
        a['permission'] = str1

    return HttpResponse(json.dumps(sql_result))


def get_other_power(req):
    role_name = req.GET.get("role_name", "")
    role = Role.objects.filter(role_name=role_name)

    if not role:
        return JsonResponse([], safe=False)

    cursor = connection.cursor()
    sql = '''
        SELECT a.menu_id
        FROM jx_role_menu a 
        LEFT JOIN jx_role b ON b.id = a.role_id
        WHERE b.role_name =
    ''' + "'" + role_name + "'"
    cursor.execute(sql)

    id_list = []
    for a in dictfetchall(cursor):
        id_list.append(a['menu_id'])

    res = []
    for query in Menu.objects.exclude(id__in=id_list):
        res.append(model_to_dict(query))

    return HttpResponse(json.dumps(res))


def add_power(req):
    role_name = req.GET.get("role", "")
    menus = req.GET.get("menu", "").split('_')

    try:
        role = Role.objects.get(role_name=role_name)
        if not role:
            HttpResponse('菜单或角色不存在')

        cursor = connection.cursor()
        for menu_id in menus:
            cursor.execute(
                """
                    INSERT INTO jx_role_menu (role_id, menu_id, permission)
                    VALUES (%(role_id)s, %(menu_id)s, '%(permission)s')
                """ % {
                    'role_id': role.id,
                    'menu_id': menu_id,
                    'permission': "n,n,n,n,n,n",
                }
            )
        return HttpResponse('添加成功')

    except:
        return HttpResponse('数据库错误')


def del_power(req):
    try:
        role = Role.objects.get(role_name=req.GET.get("role", ""))
        menu = Menu.objects.get(menu_name=req.GET.get("menu", ""))
        role.menu.remove(menu)
        return HttpResponse('删除成功')
    except:
        return HttpResponse('数据库错误')


def edit_permission(req):
    role_name = ''
    if req.method == 'POST':
        menu_id = req.POST.get('menu_id')
        role_name = req.POST.get('role_name')
        permission = req.POST.get('permission')

        b = ['n', 'n', 'n', 'n', 'n', 'n']
        if permission == '':
            permission = 'n,n,n,n,n,n'

        else:
            a = permission.split(',')
            for c in a:
                b[int(c) - 1] = 'y'
            permission = ','.join(b)

        role = Role.objects.get(role_name=role_name)
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE jx_role_menu SET permission = '%(permission)s' 
                WHERE role_id = %(role_id)s AND menu_id = %(menu_id)s
            """ % {
                'role_id': role.id,
                'menu_id': menu_id,
                'permission': permission,
            }
        )

    return HttpResponse(json.dumps(role_name))


def del_role(req):
    role_name = req.GET.get("role", "")
    role = Role.objects.filter(role_name=role_name)
    if not role:
        return HttpResponse('角色不存在')

    try:
        cursor = connection.cursor()
        sql = "UPDATE jx_sysuser SET role_id = NULL WHERE role_id=" + str(role[0].id)
        cursor.execute(sql)
        role[0].delete()
        return HttpResponse('删除成功')

    except:
        return HttpResponse('数据库错误')


def get_department(req):
    logger.info(req.COOKIES.get('payroll'))
    return JsonResponse({}, safe=False)

    cur_college = req.GET.get("cur_college", '')
    try:

        cursor = connection.cursor()
        sql = """select * from app_curr_department WHERE 1"""
        if cur_college != '' and cur_college != '-1':
            sql = sql + """ AND college_id="""+str(cur_college)
        cursor.execute(sql)
        dbresult = dictfetchall(cursor)
        return JsonResponse(dbresult, safe=False)
    except:
        return '数据库错误'


def get_dwh(req):
    # TODO: get DWH while compose upload files
    logger.info(req.COOKIES.get('payroll'))
    return '.'


def save_file(req):
    def get_file_prefix(pth):
        names = [name[:4] for name in os.listdir(pth) if os.path.isfile(os.path.join(pth, name)) and name[:4].isdigit()]
        if names:
            s = str(int(max(names)) + 1)
            return '0' * (4-len(s)) + s + '-'
        else:
            return '0000-'

    function = trim(req.POST.get('Function'))
    f = req.FILES.get("FileName", None)  # 获取上传的文件，如果没有文件，则默认为None

    d = settings.UPLOAD_DIR + '/jx/' + get_dwh(req) + '/' + function + '/' + today().replace('-', '/')
    if not os.path.exists(d):
        os.makedirs(d)

    ff = os.path.join(d, get_file_prefix(d) + f.name)
    df = open(ff, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in f.chunks():  # 分块写入文件
        df.write(chunk)
    df.close()
    return function, ff


def get_objects_between(name, start, end):
    from django.apps import apps
    model = apps.get_model('jx', name)
    m1 = model.objects.filter(
        start__gte=start,
        start__lte=end
    )
    m2 = model.objects.filter(
        end__gte=start,
        end__lte=end
    )
    m3 = model.objects.filter(
        start__lte=start,
        end__gte=end
    )
    return m1 | m2 | m3


def get_module_class(function):
    class_prefix = 'view'
    try:
        module = __import__('jx.module', fromlist=(["module"]))
    except ImportError:
        module = __import__('module')

    if function in rule_tables:
        class_prefix = 'kh'
        try:
            module = __import__('jx.rule', fromlist=(["rule"]))
        except ImportError:
            module = __import__('rule')

    module_class = getattr(module, (class_prefix + '_' + function).upper())
    return module_class


def get_model_dr_class(low_class_name):
    try:
        model_dr = __import__('jx.model_dr', fromlist=(["model_dr"]))
    except ImportError:
        model_dr = __import__('model_dr')

    if low_class_name[:2] == 'kh':
        try:
            model_dr = __import__('jx.rule', fromlist=(["rule"]))
        except ImportError:
            model_dr = __import__('rule')

    model_dr_class = getattr(model_dr, low_class_name.upper())
    return model_dr_class


def __get_column_definition(columns, column):
    for k_, v_ in columns.items():
        if len(v_) < 1:
            return []
        if v_[0] == column:
            return v_
    return []


def __format_value(vv, fm, enum_values=None):
    """
    TODO: format vv per key[k][1] if defined
    :param vv:
    :param fm:
    :return:
    """
    if enum_values is None:
        enum_values = []

    if fm == 'Enum':
        from typing import Iterable
        return '' if not isinstance(enum_values, Iterable) else (vv if vv in enum_values else enum_values[0])

    elif fm == "DateTime":
        v = str(vv).replace('-', '').replace(' ', '').replace(':', '')
        y, m, d = '1970', '01', '01'
        hh, mm, ss = '00', '00', '00'
        try:
            if len(v) >= 4:
                y = str(int(v[:4]))
            if len(v) >= 6:
                m = str(int(v[4:6]))
                m = ('0' + m) if len(m) == 1 else m
            if len(v) >= 8:
                d = str(int(v[6:8]))
                d = ('0' + d) if len(d) == 1 else d
            if len(v) >= 10:
                hh = str(int(v[8:10]))
                hh = ('0' + hh) if len(hh) == 1 else hh
            if len(v) >= 12:
                mm = str(int(v[10:12]))
                mm = ('0' + mm) if len(mm) == 1 else mm
            if len(v) >= 14:
                ss = str(int(v[12:14]))
                ss = ('0' + ss) if len(ss) == 1 else ss
        except:
            sys_info()
        return y + '-' + m + '-' + d + ' ' + hh + ':' + mm + ':' + ss

    return vv


def __row_replace_key(__row, __key, uniq=None):
    if uniq is None:
        uniq = []

    res = {}
    cc_str, vv_str, uu_str = '', '', ''
    for kk, vv in __row.items():
        k = trim(str(kk))
        v = trim(str(vv))
        if k in __key:
            if len(__key[k]) > 2:
                v = __format_value(v, __key[k][1], __key[k][2])
            elif len(__key[k]) > 1:
                v = __format_value(v, __key[k][1])
            res[__key[k][0]] = v
            cc_str += str(__key[k][0]) + ', '
            vv_str += "'" + str(v).replace("'", "char(39)") + "', "
            if str(__key[k][0]) not in uniq:
                uu_str += str(__key[k][0]) + "='" + str(v).replace("'", "char(39)") + "', "
        else:
            # res[k] = v  # ignore useless fields
            pass

    return res, cc_str[:-2], vv_str[:-2], uu_str[:-2]


@check_login
@sys_error
def jx_upload_file(req):
    # TODO: summarize notes and errors in line <br> and tip, such as adds, updates, columns ignored, cell error
    # TODO: verify if unique columns existence
    from jx.sqlalchemy_env import cursor, conn

    try:
        function, file_name = save_file(req)
        module_class = get_module_class(function)
        upload_tables = module_class.get_upload_tables()

        df = pd.read_excel(file_name, na_values='')  # 这个会直接默认读取到这个Excel的第一个表单
        df = df.where(df.notnull(), '')

        for upload_table in upload_tables:
            model_dr_class = get_model_dr_class(upload_table)
            table = model_dr_class.__tablename__
            columns = model_dr_class.get_column_label()
            unique = model_dr_class.get_unique_condition()

            sql_where = " WHERE 1=1 "
            for u in unique:
                sql_where += " AND " + u + "='%(" + u + ")s'"

            sql_count = "SELECT COUNT(*) AS count FROM %(table)s" % {'table': table} + sql_where

            for record in df.to_dict('records'):
                rec, c_str, v_str, u_str = __row_replace_key(record, columns, unique)
                cursor.execute(sql_count % rec)
                result = cursor.fetchall()
                if result[0][0]:  # update
                    sql = "UPDATE %(table)s SET " % {'table': table} + u_str + sql_where % rec
                else:  # insert
                    sql = """ 
                        INSERT INTO %(table)s (%(columns)s) VALUES (%(values)s) 
                    """ % {'table': table, 'columns': c_str, 'values': v_str, }

                logger.info(sql)
                cursor.execute(sql)
                conn.commit()  # NOTE: 必须commit; 否则独占数据库链接；可以考虑使用django connection自动commit

        return JsonResponse({'success': True, 'msg': '文件处理成功，请检验数据!'})

    except:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '文件处理失败，请修正后重试！'})


def get_user_information(payroll):
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM view_jzgjcsjxx WHERE JZGH='%(payroll)s' """ % {'payroll': payroll})
    select_out = dictfetchall(cursor)
    return select_out[0] if select_out else []


def get_top_departments():
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM dr_zzjgjbsjxx WHERE LSDWH='' OR LSDWH IS NULL """)
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


def get_sub_departments(parent):
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM view_zzjgjbsjxx WHERE LSDWH='%(parent)s' ORDER BY DWH """ % {'parent': parent})
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


def get_department_users(dept):
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM view_jzgjcsjxx WHERE DWH='%(dept)s' ORDER BY JZGH """ % {'dept': dept})
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


@check_login
@sys_error
def get_allhrdpmt(req):
    method = req.GET.get('method')
    # method_in = ('True', 'False')  # NOTE: control if add users
    method_in = ('True')

    payroll = req.COOKIES.get('payroll')
    user = get_user_information(payroll)
    departments = []
    if user:
        departments = get_sub_departments(str(user['DWH']))

    # 超级管理员
    login_user = SysUser.objects.get(payroll=payroll)
    if login_user.role_id == 1:
        departments = get_top_departments()

    data = []

    def insert_department(d, t):
        t.append({
            'type': 'd',
            'text': str(d['DWH']) + "-" + str(d['DWMC']),
            'code': str(d['DWH']),
            'href': str(d['id']),
            'tags': [str(d['DWH'])],
            'nodes': []
        })

    def insert_user(u, t):
        t.append({
            'type': 'u',
            'text': str(u['JZGH']) + "-" + str(u['XM']),
            'code': str(u['JZGH']),
            'href': str(u['id']),
            'tags': [str(u['JZGH'])]
        })

    def search_department(dt, t):
        for d in dt:
            # this department
            insert_department(d, t)

            # children departments
            if str(d['DWH']) != str(d['LSDWH']):
                ds = get_sub_departments(d['DWH'])
                if ds:
                    search_department(ds, t[len(t)-1]["nodes"])

            # children users
            if method in method_in:
                for uu in get_department_users(d['DWH']):
                    insert_user(uu, t[len(t)-1]["nodes"])

            # clear empty
            if not len(t[len(t)-1]["nodes"]):
                t[len(t) - 1].pop("nodes")

    search_department(departments, data)

    # append first level users
    if method in method_in:
        for du in get_department_users(str(user['DWH'])):
            # continue
            insert_user(du, data)

    # response as bootstrap-treeview
    return JsonResponse({'success': True, 'tag': u'刷新成功', 'data': data})


@check_login
def edit(req):
    """
    :param req: id=30&DWJC=00000C&field=DWJC&menu=zzjgjbsjxx
    :return:
    """
    try:
        v = eval(str(req.POST.dict()))
        set_to = trim(str(v[v['field']]))
        if set_to.find('null') != -1:
            return JsonResponse({'success': False, 'msg': '更新失败：值中含有 null'})

        v['class_name'] = 'view_' + v['menu']
        if v['menu'] in rule_tables:
            v['class_name'] = 'kh_' + v['menu']

        column = get_column_info(v['class_name'], v['field'])
        model_dr_class = get_model_dr_class(column['table'])
        unique = model_dr_class.get_unique_condition()

        where = '1=1'
        for u in unique:
            if u not in v:
                return JsonResponse({'success': False, 'msg': '更新失败：数据唯一性条件不满足'})
            where += ' AND ' + u + "='%(" + u + ")s'"
        if where == '1=1':
            return JsonResponse({'success': False, 'msg': '更新失败：数据更新条件未定义'})

        # NOTE: update by id
        if unique == [v['field']] and column['table'] == v['class_name']:
            where = "id='%(id)s'"

        v['set_to'] = set_to
        v['where'] = where % v
        v['table'] = column['table']
        sql_update = "UPDATE %(table)s SET %(field)s='%(set_to)s' WHERE %(where)s" % v

        cursor = connection.cursor()
        logger.info(sql_update)
        cursor.execute(sql_update)

        return JsonResponse({'success': True, 'msg': '成功更新为：' + set_to})

    except Error:  # django.db.utils.Error
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '更新失败：数据库错误'})


@check_login
def get_col_def(req):
    payroll = str(req.COOKIES.get('payroll'))
    v = eval(str(req.GET.dict()))
    print(v)
    return JsonResponse(get_static_data(payroll, v['value'], v['where']), safe=False)


@check_login
@sys_error
def get_title(req):
    v = eval(str(req.GET.dict()))
    # code  # DWH if type=='d', JZGH if type=='u'
    # type  # d - department, u - user
    # start|end  # start/end date from FE
    module_name = 'module'
    view_prefix = 'view'
    if v['menu'] in rule_tables:
        module_name = 'rule'
        view_prefix = 'kh'

    from jx.views import get_module_static_method
    return JsonResponse(get_module_static_method(v['menu'], 'get_title_columns', module_name, view_prefix), safe=False)


@check_login
@sys_error
def get_data(req):
    payroll = str(req.COOKIES.get('payroll'))

    v = eval(str(req.GET.dict()))

    module_name = 'module'
    view_prefix = 'view'
    if v['menu'] in rule_tables:
        module_name = 'rule'
        view_prefix = 'kh'

    # v['table'] = (view_prefix + "_" + v['menu']).upper().lower()
    v['table'] = ("view_" + v['menu']).upper().lower()  # change to lower due to un-support upper SQL on Linux
    v['start'] += "-01 00:00:00"
    v['end'] = month_end(v['end'])
    if 'sort' not in v or v['sort'] in ('', None):
        v['sort'] = 'id'
        v['order'] = 'DESC'

    # code  # DWH if type=='d', JZGH if type=='u'
    # type  # d - department, u - user
    # TODO: use department and payroll to get data
    if 'type' in v:
        if v['type'] == 'd':
            v['department'] = v['code']
            v['payroll'] = payroll
        if v['type'] == 'u':
            user = get_user_information(v['code'])
            v['department'] = str(user['DWH'])
            v['payroll'] = v['code']
    else:
        v['type'] = 'u'
        v['payroll'] = payroll

    l_user = SysUser.objects.get(payroll=payroll)
    v['role'] = l_user.role_id

    sql_count = """ SELECT COUNT(*) AS count FROM %(table)s """ % v
    sql_content = """ SELECT * FROM %(table)s """ % v

    sql_where = " WHERE 1=1 "
    if v['type'] == 'u':
        sql_where += " AND JZGH='%(payroll)s'"
    elif v['type'] == 'd':
        if v['menu'] == 'zzjgjbsjxx':  # 组织机构基本数据信息
            sql_where += " AND (DWH='%(department)s' OR LSDWH='%(department)s')"
        else:
            sql_where += " AND DWH='%(department)s'"  # TODO: DWH IN ('', '') -> VIEW_ZZJGJBSJXX.get_managed_departments
    else:
        sql_where += " AND 1=0"
    sql_where %= v

    sql_search = ""
    if 'search' in v and v['search'] not in ('', None):
        from jx.views import get_module_static_method
        search_columns = get_module_static_method(v['menu'], 'get_search_columns', module_name, view_prefix)
        if search_columns:
            sql_search = " AND (1=0 "
            for col in search_columns:
                sql_search += " OR %(col)s LIKE \'%%%(search)s%%\' " % {'col': col, 'search': v['search']}
            sql_search += ")"

    sql_olo = ' ORDER BY %(sort)s %(order)s LIMIT %(limit)s OFFSET %(offset)s' % v

    cursor = connection.cursor()
    logger.info(sql_count + sql_where + sql_search)
    cursor.execute(sql_count + sql_where + sql_search)
    count = dictfetchall(cursor)[0]["count"]

    logger.info(sql_content + sql_where + sql_search + sql_olo)
    cursor.execute(sql_content + sql_where + sql_search + sql_olo)
    select_out = dictfetchall(cursor)

    return JsonResponse({'total': count, 'rows': select_out})


@check_login
def delete_data(req):
    payroll = str(req.COOKIES.get('payroll'))
    # TODO: check delete auth ???

    v = eval(str(req.POST.dict()))
    data = json.loads(v['data'])
    function = v['menu']
    count = v['count']

    module_class = get_module_class(function)
    upload_tables = module_class.get_delete_tables()

    from jx.sqlalchemy_env import cursor, conn
    for d_table in upload_tables:
        model_dr_class = get_model_dr_class(d_table)
        unique = model_dr_class.get_unique_condition()

        where = '1=1'
        for u in unique:
            where += ' AND ' + u + "='%(" + u + ")s'"
        if where == '1=1':
            continue

        for c in range(0, int(count)):

            sql_delete = """ DELETE FROM %(table)s WHERE %(where)s """ % {'table': d_table, 'where': where % data[c]}

            # TODO: add more WHERE conditions to keep system safe
            # 1. zzjgjbsjxx can't delete parent and current
            # 2. jzgjcsjxx can't delete self and admin
            # 3. other conditions ???

            # cursor = connection.cursor()  # change to SQLAlchemy cursor to keep delete transaction
            logger.info(sql_delete)
            cursor.execute(sql_delete)

    conn.commit()
    return JsonResponse({'success': True, 'msg': '删除数据成功'})


def __format_create_value(v, columns):
    val = {}

    for k_, v_ in v.items():
        _v = v_
        col_def = __get_column_definition(columns, k_)
        if len(col_def) > 1:
            if col_def[1] == 'DateTime':
                _v = __format_value(v_, 'DateTime')
            if col_def[1] == 'Enum' and _v == '':
                _v = __format_value(_v, 'Enum', col_def[2])

        if k_ not in ('id', 'stamp', 'note'):
            val[k_] = _v

    # NOTE: 增减业绩点
    if 'create_data_item' in v:
        if v['create_data_item'] == 'khjgmx':
            val['note'] = v['note']
            val['GZH'] = 'ZZZ'
            val['stamp'] = now()

    return val


@check_login
def create_data(req):
    payroll = str(req.COOKIES.get('payroll'))
    # TODO: create auth verification
    # TODO: additional check and default value set

    def __translate_column_to_chinese(columns, col):
        for k, v in columns.items():
            if v[0] == col:
                return k
        return ''

    def __transform_key_to_chinese(vv, columns):
        res = {}
        for k, v in vv.items():
            nk = __translate_column_to_chinese(columns, k)
            res[nk] = v
        return res

    _v = eval(str(req.POST.dict()))
    function = _v['create_data_item']

    module_class = get_module_class(function)
    upload_tables = module_class.get_delete_tables()

    from jx.sqlalchemy_env import cursor, conn
    for d_table in upload_tables:
        model_dr_class = get_model_dr_class(d_table)
        columns = model_dr_class.get_column_label()
        unique = model_dr_class.get_unique_condition()

        tv = __format_create_value(_v, columns)

        where = '1=1'
        for u in unique:
            if u in tv and not len(trim(tv[u])):
                return JsonResponse({'success': False, 'msg': '创建失败：' + str(u) + '为空'})  # TODO: to Chinese readable
            where += ' AND ' + u + "='%(" + u + ")s'"
        if where == '1=1':
            continue

        sql_count = """ SELECT COUNT(*) AS count FROM %(table)s WHERE %(where)s 
        """ % {'table': d_table, 'where': where % tv}
        logger.info(sql_count)
        cursor.execute(sql_count)
        count = cursor.fetchall()
        if count[0][0] > 0:
            return JsonResponse({'success': False, 'msg': '创建失败：数据主键重复'})

        c_key = __transform_key_to_chinese(tv, columns)
        rec, c_str, v_str, u_str = __row_replace_key(c_key, columns, unique)

        sql_insert = """ INSERT INTO %(table)s (%(columns)s) VALUES (%(values)s) 
        """ % {'table': d_table, 'columns': c_str, 'values': v_str, }

        logger.info(sql_insert)
        from pymysql.err import DataError
        try:
            cursor.execute(sql_insert)
            cursor.fetchall()
            pass
        except DataError as e:
            logger.error(sys_info())
            return JsonResponse({'success': False, 'msg': '创建失败: ' + str(e)})  # TODO: translate exception

    conn.commit()
    return JsonResponse({'success': True, 'msg': '新建数据成功'})


@check_login
@sys_error
def staffinfo(req):
    payroll = str(req.COOKIES.get('payroll'))
    user = SysUser.objects.get(payroll=payroll)

    v = eval(str(req.GET.dict()))
    if 'sort' not in v or v['sort'] in ('', None):
        v['sort'] = 'id'
        v['order'] = 'DESC'

    l_user = SysUser.objects.get(payroll=payroll)
    v['role'] = l_user.role_id

    sql_count = """ SELECT COUNT(*) AS count FROM view_sysuser """
    sql_content = """ SELECT * FROM view_sysuser """

    sql_where = " WHERE 1=1 "
    if user.role_id == 1:
        pass
    elif user.role_id == 2:
        user_info = get_user_information(payroll)
        sql_where += " AND DWH='%(department)s'" % {'department': str(user_info['DWH'])}
    else:
        sql_where += ' AND 1=0'

    sql_search = ""
    if 'search' in v and v['search'] not in ('', None):
        search_columns = ['payroll', 'XM', 'DWMC']
        if search_columns:
            sql_search = " AND (1=0 "
            for col in search_columns:
                sql_search += " OR %(col)s LIKE \'%%%(search)s%%\' " % {'col': col, 'search': v['search']}
            sql_search += ")"

    sql_olo = ' ORDER BY %(sort)s %(order)s LIMIT %(limit)s OFFSET %(offset)s' % v

    cursor = connection.cursor()
    logger.info(sql_count + sql_where + sql_search)
    cursor.execute(sql_count + sql_where + sql_search)
    count = dictfetchall(cursor)[0]["count"]

    logger.info(sql_content + sql_where + sql_search + sql_olo)
    cursor.execute(sql_content + sql_where + sql_search + sql_olo)
    select_out = dictfetchall(cursor)

    return JsonResponse({'total': count, 'rows': select_out})


@check_login
@sys_error
def run_kpi(req):
    try:
        from jx.rule import KH_KHJGMX, KH_KHJGHZ, KH_KHPC
        from jx.sqlalchemy_env import db
        from jx.module import VIEW_JZGJCSJXX

        payroll = req.COOKIES.get('payroll')
        departments = VIEW_JZGJCSJXX.get_managed_departments(str(payroll))

        # get latest active year
        query = db.query(KH_KHPC)
        query = query.filter(KH_KHPC.DWH.in_(departments), KH_KHPC.JHZT == '已激活')
        query = query.order_by(-KH_KHPC.KHNF)
        query_out = query.all()
        if not query_out:
            return JsonResponse({'success': False, 'msg': '未找到已激活考核年份！'})
        year = query_out[0].KHNF
        FBZT = query_out[0].FBZT
        start = query_out[0].RQQD
        end = query_out[0].RQZD

        # clear first
        query = db.query(KH_KHJGMX)
        query = query.filter(KH_KHJGMX.DWH.in_(departments), KH_KHJGMX.KHNF == year)
        query_out = query.all()
        for out in query_out:
            db.delete(out)
            continue
        query = db.query(KH_KHJGHZ)
        query = query.filter(KH_KHJGHZ.DWH.in_(departments), KH_KHJGHZ.KHNF == year)
        query_out = query.all()
        for out in query_out:
            db.delete(out)
            continue
        db.commit()

        calculate_kpi(departments, year, start, end, req.COOKIES.get('payroll'), db)

        if FBZT == '已发布':
            summarize_kpi(departments, year, db)

        return JsonResponse({'success': True, 'msg': '绩效考核运行成功，请核查数据！'})

    except:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '绩效考核运行失败：数据库错误'})


@check_login
def custermize_kpi(req):
    # TODO: 不考核教职工可在教职工页面采用相同方法
    try:
        payroll = str(req.COOKIES.get('payroll'))

        v = eval(str(req.POST.dict()))
        data = json.loads(v['data'])
        year = __format_value(v['year'], "DateTime")
        user = get_user_information(payroll)

        from jx.sqlalchemy_env import db
        from jx.rule import KH_KHGZDZ

        for index in data:
            query = db.query(KH_KHGZDZ)
            query = query.filter(KH_KHGZDZ.DWH == user['DWH'], KH_KHGZDZ.KHNF == year, KH_KHGZDZ.GZH == index)
            query_out = query.all()
            for out in query_out:
                db.delete(out)
            db.commit()

            obj = KH_KHGZDZ(user['DWH'], year, index).save()
            db.add(obj)
        db.commit()

        return JsonResponse({'success': True, 'msg': '绩效考核定制成功，请核查数据！'})

    except:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '绩效考核定制失败：数据库错误'})
