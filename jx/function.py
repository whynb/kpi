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


def calculate_kpi(_payroll):
    from jx.module import VIEW_JZGJCSJXX
    departments = VIEW_JZGJCSJXX.get_managed_departments(str(_payroll))

    from jx.sqlalchemy_env import db
    from jx.rule import KH_JXKHGZ, KH_KHJGMX
    # TODO: additional query options
    rules_query = db.query(KH_JXKHGZ)
    rules_query = rules_query.filter(KH_JXKHGZ.DWH.in_(departments))
    rules = rules_query.all()

    for rule in rules:
        try:
            class_to_check = rule.get_input_class()  # get class to check
            data_query = db.query(class_to_check)  # query out by class defined in rule
            data_query = data_query.filter(class_to_check.DWH.in_(departments))

            # TODO: additional query options, such as timestamp
            # filter by additional condition input from FE such as KPI batch id/period
            # data_query = data_query.filter(class_to_check.timestamp.between(start, end))

            data_query = data_query.order_by(-class_to_check.id)  # order which is useless in rule calculation
            data = data_query.all()  # get dataset
            if len(data) == 0:
                continue

            for x in data:  # for each data
                logger.debug(x.__dict__)  # TODO: logger
                try:
                    if not rule.match(x):  # match rule condition
                        continue

                    logger.debug(rule.calculate(x))  # TODO: print/output/save rule calculation
                    logger.debug(rule.get_output_template() % x.__dict__ % rule.__dict__)

                    # Save
                    obj = KH_KHJGMX(
                        JZGH=x.JZGH,
                        DWH=rule.DWH,
                        GZH=rule.GZH,
                        KHJD=rule.calculate(x),
                        KHMX=rule.get_output_template() % x.__dict__ % rule.__dict__
                    )
                    db.add(obj)
                    db.commit()
                except:
                    logger.error(sys_info())
                    pass
        except:
            logger.error(sys_info())
            pass


def summarize_kpi(_payroll):
    # TODO: how to summarize ??? while calculate->save
    pass
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
    # TODO: get DWH
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


@check_login
@sys_error
def jx_upload_file(req):
    from jx.sqlalchemy_env import cursor, conn

    def __format_value(v, fm):
        """
        TODO: format v per key[k][1] if defined
        :param v:
        :param fm:
        :return:
        """
        if fm == "DateTime":
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

        return v

    def __row_replace_key(__row, __key, uniq=None):
        if uniq is None:
            uniq = []

        res = {}
        cc_str, vv_str, uu_str = '', '', ''
        for kk, vv in __row.items():
            k = trim(str(kk))
            v = trim(str(vv))
            if k in __key:
                if len(__key[k]) > 1:
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

    try:
        function, file_name = save_file(req)

        df = pd.read_excel(file_name, na_values='')  # 这个会直接默认读取到这个Excel的第一个表单
        df = df.where(df.notnull(), '')

        table_prefix = "dr"

        try:
            model_dr = __import__('jx.model_dr', fromlist=(["model_dr"]))
        except ImportError:
            model_dr = __import__('model_dr')

        if function in ['jxkhgz']:
            table_prefix = 'kh'
            try:
                model_dr = __import__('jx.rule', fromlist=(["rule"]))
            except ImportError:
                model_dr = __import__('rule')

        model_dr_class = getattr(model_dr, (table_prefix + '_' + function).upper())
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
    method_in = ('True', 'False')

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

        v['table_prefix'] = 'dr'
        if v['menu'] in ['jxkhgz']:
            v['table_prefix'] = 'kh'

        v['set_to'] = set_to
        sql_update = "UPDATE %(table_prefix)s_%(menu)s SET %(field)s='%(set_to)s' WHERE id=%(id)s" % v

        cursor = connection.cursor()
        logger.info(sql_update)
        cursor.execute(sql_update)

        return JsonResponse({'success': True, 'msg': '成功更新为：' + set_to})

    except Error:  # django.db.utils.Error
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '更新失败：数据库错误'})


@check_login
@sys_error
def get_title(req):
    v = eval(str(req.GET.dict()))
    # code  # DWH if type=='d', JZGH if type=='u'
    # type  # d - department, u - user
    # start|end  # start/end date from FE
    module_name = 'module'
    view_prefix = 'view'
    if v['menu'] in ['jxkhgz', 'khjgmx']:
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
    if v['menu'] in []:
        module_name = 'rule'
        view_prefix = 'kh'

    v['table'] = (view_prefix + "_" + v['menu']).upper().lower()  # change to lower due to un-support upper SQL on Linux
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
            sql_where += " AND DWH='%(department)s'"
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
@sys_error
def delete_data(req):
    payroll = str(req.COOKIES.get('payroll'))
    # TODO: check delete auth ???

    v = eval(str(req.POST.dict()))
    v['table'] = "dr_" + v['menu']
    v['id_in'] = v['id'].replace('[', '(').replace(']', ')')

    sql_delete = """ DELETE FROM %(table)s WHERE id IN %(id_in)s """ % v
    # TODO: add more WHERE conditions to keep system safe
    # 1. zzjgjbsjxx can't delete parent and current
    # 2. jzgjcsjxx can't delete self and admin
    # 3. other conditions ???

    cursor = connection.cursor()
    logger.info(sql_delete)
    cursor.execute(sql_delete)

    return JsonResponse({'success': True, 'msg': '删除数据成功'})


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
    logger.info(req.COOKIES.get('payroll'))
    try:
        # TODO: clear first

        calculate_kpi(req.COOKIES.get('payroll'))
        summarize_kpi(req.COOKIES.get('payroll'))
        return JsonResponse({'success': True, 'msg': '绩效考核运行成功，请核查数据！'})

    except:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '绩效考核运行失败：数据库错误'})
