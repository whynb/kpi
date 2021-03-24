# coding=utf-8
# TODO: data status should be done by work flow

"""
NOTE: SQL injection
REFER: https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/

错误用法：
sql = "select id, name from user_table where id=%s and name=%s" % (id, name)
cur.execute(sql)

正确用法：
execute() 函数本身有接受sql语句参数位的，可以通过python自身的函数处理sql注入问题。
1.Django: cur.execute('select id, name from user_table where id=%s and name =%s', [id, name])
2.SQLAlchemy: db.execute(text("select * from log where username=:usr"), {"usr": "jetz"})
3.SQLAlchemy: db.execute("select * from log where username=:1 ", ["jetz"])
"""


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
from jx.exception import *
from pymysql.err import Error
from jx.password import pc


rule_tables = ['khpc', 'jxkhgz', 'khgzdz', 'khjgmx', 'khjghz', 'bcykh',
               'kh_khpc', 'kh_jxkhgz', 'kh_khgzdz', 'kh_khjgmx', 'kh_khjghz', 'kh_bcykh']


def get_field_name(s):
    # NOTE: Refer to below get_static_data to get [col1,col2,...] used by FE Jinja2
    try:
        res = []
        arr = s[s.find(':') + 1:].split(',')
        for a in arr:
            if a.find('AS') != -1:
                res.append(trim(a[a.find('AS')+2:]))
            elif a.find('as') != -1:
                res.append(trim(a[a.find('as')+2:]))
            else:
                res.append(a)
        res.append(trim(s[:s.find(':')]))
        return res
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
        cursor.execute(sql)  # NOTE: NO SQL injection
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
            class_to_check = rule.get_input_class()  # get class to check
            if class_to_check == 'VIEW_':  # NOTE: no KHSJDX for 增减业绩点 or no class defined in module.py
                continue

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

                    obj = KH_KHJGMX(
                        JZGH=x.JZGH,
                        DWH=rule.DWH,
                        GZH=rule.GZH,
                        KHNF=year,
                        KHJD=rule.calculate(x),
                        KHMX=rule.get_output_template() % {**x.__dict__, **rule.__dict__}
                    )
                    db.add(obj)
                except:
                    logger.error(sys_info())
                    pass

                try:
                    db.commit()
                except:
                    db.rollback()
                    logger.error(sys_info())

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
            # db.commit()

            if cur:  # 按上级部门汇总绩点
                logger.info(obj.LSDWH)
                if obj.LSDWH and trim(str(obj.LSDWH)) != '' and obj.LSDWH != 'None':
                    obj = save(obj.LSDWH, KHNF, JZGH, GZH, cur)
            return obj

        save(data.DWH, data.KHNF, data.JZGH, '', False)  # 汇总教职工个人绩点
        save(data.DWH, data.KHNF, '', data.GZH, True)  # 按规则汇总部门绩点
        save(data.DWH, data.KHNF, '', '', True)  # 按部门汇总绩点

        try:
            db.commit()
        except:
            db.rollback()
            logger.error(sys_info())
    return


@check_login
@sys_error
def role_inline_edit(req):
    try:
        if req.method != 'POST':
            return JsonResponse({'success': False, 'msg': '消息类型错误！'})

        payroll = req.COOKIES.get('payroll')
        user = SysUser.objects.get(payroll__exact=payroll)
        if user.role_id not in (1, 2):
            return JsonResponse({'success': False, 'msg': '登录用户没有权限！'})

        payroll_number = req.POST.get('payroll', '')
        if payroll_number == '':
            return JsonResponse({'success': False, 'msg': '参数错误, 用户不存在！'})

        payroll_user = SysUser.objects.get(payroll__exact=payroll_number)
        role_id = int(req.POST.get('role_id', '4'))
        if role_id == 1:  # 禁止FE修改成为超级管理员
            return JsonResponse({'success': False, 'msg': '参数错误, 请联系管理员！'})
        
        payroll_user.role_id = role_id
        payroll_user.save()
        return JsonResponse({'success': True, 'msg': '修改成功！'})

    except SysUser.DoesNotExist:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '用户不存在，请重新登录！'})

    except:
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '系统异常，请联系管理员！'})


def __get_power(role_name):
    cursor = connection.cursor()
    sql = """
        SELECT a.id, a.menu_name, a.menu_classify, b.permission, a.menu_addr
        FROM jx_menu a 
        LEFT JOIN jx_role_menu b ON b.menu_id = a.id
        LEFT JOIN jx_role c ON c.id = b.role_id
        WHERE c.role_name=%s
    """

    cursor.execute(sql, [role_name])
    sql_result = dictfetchall(cursor)
    for a in sql_result:
        c = []
        b = a['permission'].split(',')
        for num in range(0, 6):
            if b[num] == 'y':
                c.append(str(int(num) + 1))

        str1 = ','.join(c)
        a['permission'] = str1
    return sql_result


@check_login
@sys_error
def getpower(req):
    return HttpResponse(json.dumps(__get_power(req.GET.get("role_name", ""))))


@check_login
@sys_error
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
        WHERE b.role_name=%s
    '''
    cursor.execute(sql, [role_name])

    id_list = []
    for a in dictfetchall(cursor):
        id_list.append(a['menu_id'])

    res = []
    for query in Menu.objects.exclude(id__in=id_list):
        res.append(model_to_dict(query))

    return HttpResponse(json.dumps(res))


@check_login
@sys_error
def add_power(req):
    from jx.sqlalchemy_env import db, text
    role_name = req.GET.get("role", "")
    menus = req.GET.get("menu", "").split('_')

    try:
        role = Role.objects.get(role_name=role_name)
        for menu_id in menus:
            if str(role.id) != '1':  # not admin
                if str(menu_id) == '1':
                    continue

            db.execute(
                text("INSERT INTO jx_role_menu (role_id, menu_id, permission) VALUES (:role_id, :menu_id, :p)"),
                {'role_id': role.id, 'menu_id': menu_id, 'p': "n,n,n,n,n,n"}
            )
            db.commit()
        return HttpResponse('添加成功')

    except Role.DoesNotExist:
        logger.error(sys_info())
        return HttpResponse('菜单或角色不存在')

    except:
        db.rollback()
        logger.error(sys_info())
        return HttpResponse('数据库错误')


@check_login
@sys_error
def del_power(req):
    try:
        role = Role.objects.get(role_name=req.GET.get("role", ""))
        menu = Menu.objects.get(menu_name=req.GET.get("menu", ""))
        role.menu.remove(menu)
        return HttpResponse('删除成功')
    except:
        return HttpResponse('数据库错误')


@check_login
@sys_error
def edit_permission(req):
    if req.method != 'POST':
        return HttpResponse(json.dumps(''))

    from jx.sqlalchemy_env import db, text
    role_name = ''

    try:
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
        try:
            db.execute(
                text("UPDATE jx_role_menu SET permission=:permission WHERE role_id=:role_id AND menu_id=:menu_id"),
                {'role_id': role.id, 'menu_id': menu_id, 'permission': permission}
            )
            db.commit()
        except:
            logger.error(sys_info())
            db.rollback()

    except Exception:
        logger.error(sys_info())

    return HttpResponse(json.dumps(role_name))


@check_login
@sys_error
def del_role(req):
    from jx.sqlalchemy_env import db, text
    role_name = req.GET.get("role", "")
    role = Role.objects.filter(role_name=role_name)
    if not role:
        return HttpResponse('角色不存在')

    if str(role[0].id) in ['1', '2', '3', '4']:
        return HttpResponse('禁止删除该角色')

    try:
        # cursor = connection.cursor()
        sql = "UPDATE jx_sysuser SET role_id = NULL WHERE role_id=:role_id"
        db.execute(text(sql), {'role_id': str(role[0].id)})
        db.commit()
        role[0].delete()
        return HttpResponse('删除成功')

    except:
        db.rollback()
        return HttpResponse('数据库错误')


def get_dwh(req):
    try:
        return str(get_user_information(str(req.COOKIES.get('payroll')))['DWH'])
    except:
        logger.error(sys_info())
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
    if not f:
        raise FileSaveException('上传文件名为空')

    try:
        d = settings.UPLOAD_DIR + '/jx/' + get_dwh(req) + '/' + function + '/' + today().replace('-', '/')
        if not os.path.exists(d):
            os.makedirs(d)

        ff = os.path.join(d, get_file_prefix(d) + f.name)
        df = open(ff, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in f.chunks():  # 分块写入文件
            df.write(chunk)
        df.close()
        return function, ff
    except:
        raise FileSaveException('保存文件失败: ' + f.name)


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
    :param vv:
    :param fm: 'Enum'｜"DateTime"
    :enum_values: value set for Enum type data
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
    cc_str, vv_str, uu_str, not_processed = '', '', '', []
    for kk, vv in __row.items():
        k = trim(str(kk))
        v = trim(str(vv))
        if k in __key:
            if len(__key[k]) > 2:
                v = __format_value(v, __key[k][1], __key[k][2])
            elif len(__key[k]) > 1:
                v = __format_value(v, __key[k][1])

            rk = str(__key[k][0])
            res[rk] = v
            cc_str += rk + ', '
            vv_str += ":" + rk + ", "
            if rk not in uniq:
                uu_str += rk + "=:" + rk + ", "
        else:
            # res[k] = v  # ignore useless fields
            not_processed.append(k)
            pass

    return res, cc_str[:-2], vv_str[:-2], uu_str[:-2], not_processed


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


def __check_user_auth(req):
    method = req.method
    menu = req.POST.get('menu', '') if method == 'POST' else req.GET.get('menu', '')

    _auth = 0
    req_menus = req.get_full_path().split('/')
    req_menu = req_menus[2] if req_menus[2] not in ['base'] else req_menus[3]
    if req_menu in ['create_data', ]:
        _auth = 1
    elif req_menu in ['delete_data', ]:
        _auth = 2
    elif req_menu in ['edit', 'role_inline_edit']:
        _auth = 3
    elif req_menu in ['get_data', ]:
        _auth = 4
    elif req_menu in ['jx_upload_file', ]:
        menu = trim(req.POST.get('Function'))
        _auth = 5
    elif req_menu in ['___download', ]:  # NOTE: coding while support BE download
        _auth = 6
    else:
        _auth = 0

    payroll = req.COOKIES.get('payroll')
    user = SysUser.objects.get(payroll__exact=payroll)
    pws = __get_power(user.role.role_name)
    for pw in pws:
        _pws = pw['menu_addr'].split('/')
        _pw = _pws[len(_pws)-2]

        if menu != _pw:
            continue

        if _auth in eval('[' + pw['permission'] + ']'):
            return

    if _auth == 0:
        return

    raise UserAuthException("No Auth: %s to %s @%s" % (payroll, req_menu, menu, ))


@check_login
@sys_error
def jx_upload_file(req):
    from jx.sqlalchemy_env import db, text

    msg, status, status_count, update_or_insert, update_lines, insert_lines, false_lines = '', False, 0, '', 0, 0, 0
    try:
        function, file_name = save_file(req)
        module_class = get_module_class(function)
        upload_tables = module_class.get_upload_tables()

        df = pd.read_excel(file_name, na_values='')  # 这个会直接默认读取到这个Excel的第一个表单
        df = df.where(df.notnull(), '')

        if len(df.to_dict('records')) == 0:
            return JsonResponse({'success': False, 'msg': '上传文件为空，请重新选择！'})

        line = 1
        for upload_table in upload_tables:
            model_dr_class = get_model_dr_class(upload_table)
            table = model_dr_class.__tablename__
            msg_tablename = model_dr_class.__tablename__CH__ if hasattr(model_dr_class, '__tablename__CH__') \
                else model_dr_class.__tablename__
            columns = model_dr_class.get_column_label()
            uniques = model_dr_class.get_unique_condition()
            if len(uniques) == 0:
                msg += msg_tablename + ': 数据唯一性条件未定义，未处理！<br>'
                continue

            if len(uniques[0]) and isinstance(uniques[0], str):
                uniques = [uniques, ]
            unique = uniques[len(uniques)-1]

            all_unique = []
            for unique in uniques:
                all_unique += unique
            all_unique = list(set(all_unique))

            for record in df.to_dict('records'):
                line += 1
                rec, c_str, v_str, u_str, not_processed = __row_replace_key(record, columns, unique)

                if line == 2 and not_processed:
                    msg += msg_tablename + ': 列 ' + str(not_processed) + ' 未处理<br>'

                if 'DWH' in all_unique:
                    from jx.module import VIEW_JZGJCSJXX
                    managed_departments = VIEW_JZGJCSJXX.get_managed_departments(req.COOKIES.get('payroll'))
                    if rec['DWH'] not in managed_departments:
                        msg += '行' + str(line) + ': 未处理，单位错误<br>'
                        false_lines += 1
                        continue

                zero_count, one_count, sql_where = 0, 0, ''
                for unique in uniques:
                    counts = __get_data_counters(table, unique, rec)
                    if counts['count'] == 0:
                        zero_count += 1
                    elif counts['count'] == 1:
                        one_count += 1
                    else:
                        pass
                    sql_where = ' WHERE ' + counts['where']

                if one_count == len(uniques):  # update
                    sql = "UPDATE " + table + " SET " + u_str + sql_where
                    update_or_insert = 'U'
                elif zero_count == len(uniques):  # insert
                    sql = "INSERT INTO " + table + " (" + c_str + ") VALUES (" + v_str + ")"
                    update_or_insert = 'I'
                else:
                    msg += '行' + str(line) + ': 未处理，请检查' + str(all_unique) + '<br>'
                    false_lines += 1
                    continue

                logger.info(sql)
                try:
                    db.execute(text(sql), rec)
                    db.commit()  # NOTE: 必须commit; 否则独占数据库链接；可以考虑使用django connection自动commit
                    if update_or_insert == 'U':
                        update_lines += 1
                    elif update_or_insert == 'I':
                        insert_lines += 1
                    else:
                        logger.error('update_or_insert->' + str(update_or_insert))
                except:
                    db.rollback()
                    logger.error(sys_info())
                    false_lines += 1
                    msg += '行' + str(line) + ': 数据处理异常，请修正后重试<br>'

            msg += msg_tablename + ': 更新%(u)s行, 插入%(i)s行, 失败%(f)s行<br>' % {
                'u': update_lines, 'i': insert_lines, 'f': false_lines,
            }

            if (line - 1) == (update_lines + insert_lines):
                status_count += 1
            line, update_lines, insert_lines, false_lines = 1, 0, 0, 0

        if status_count == len(upload_tables):
            status = True
            msg = '文件处理成功, 请检验数据！<br>' + msg
        else:
            msg = '文件处理失败, 请检验数据！<br>' + msg

        return JsonResponse({'success': status, 'msg': msg})

    except FileSaveException as e:
        logger.error(e)
        return JsonResponse({'success': False, 'msg': str(e)})

    except:
        logger.error(sys_info())
        msg = '文件处理异常, 请检验数据！<br>' + msg
        return JsonResponse({'success': status, 'msg': msg})


def get_user_information(payroll):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_jzgjcsjxx WHERE JZGH=%s", [payroll])
    select_out = dictfetchall(cursor)
    return select_out[0] if select_out else {}


def get_sysuser_information(payroll):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_sysuser WHERE payroll=%s", [payroll])
    select_out = dictfetchall(cursor)
    return select_out[0] if select_out else {}


def get_top_departments():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dr_zzjgjbsjxx WHERE LSDWH='' OR LSDWH IS NULL")
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


def get_sub_departments(parent):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_zzjgjbsjxx WHERE LSDWH=%s ORDER BY DWH", [parent])
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


def get_department_users(dept):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_jzgjcsjxx WHERE DWH=%s ORDER BY JZGH", [dept])
    select_out = dictfetchall(cursor)
    return select_out if select_out else []


@check_login
@sys_error
def get_allhrdpmt(req):
    method = req.GET.get('method')
    # method_in = ('True', 'False')  # NOTE: control if add users
    method_in = ('True', )

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
                uus = get_department_users(d['DWH'])
                for uu in get_department_users(d['DWH']):
                    if uu['JZGH'] not in ['admin', ]:
                        insert_user(uu, t[len(t)-1]["nodes"])

            # clear empty
            if not len(t[len(t)-1]["nodes"]):
                t[len(t) - 1].pop("nodes")

    search_department(departments, data)

    # append first level users
    if method in method_in and user:
        for du in get_department_users(str(user['DWH'])):
            if du['JZGH'] not in ['admin', ]:
                insert_user(du, data)

    # response as bootstrap-treeview
    return JsonResponse({'success': True, 'tag': u'刷新成功', 'data': data})


def __get_data_counters(table_name, unique=None, value_set=None):
    if unique is None or value_set is None or len(unique) == 0 or len(value_set) == 0:
        return {'count': -1, 'message': '主键或数据集未定义'}

    msg_unique = ''
    for u in unique:
        if u in value_set and not len(trim(value_set[u])):
            msg_unique += ' ' + u
    if msg_unique != '':
        return {'count': -1, 'message': '主键数据未定义' + msg_unique}

    where = '1=1'
    for u in unique:
        where += ' AND ' + u + "=:" + u
    sql_count = "SELECT COUNT(*) AS count FROM " + table_name + " WHERE " + where

    from jx.sqlalchemy_env import db, text
    count = db.execute(text(sql_count), value_set).fetchall()
    return {'count': count[0][0], 'message': '获得数据数量 ' + str(count[0][0]), 'where': where}


@check_login
def edit(req):
    """
    :param req: id=30&DWJC=00000C&field=DWJC&menu=zzjgjbsjxx
    :return:

        def get_title_columns() -> List[dict]:
        return [
            {'table': 'dr_jzgjcsjxx', 'field': 'DWH', 'title': '单位号', 'editable': 'False', 'type': 'text', 'create': 'F', },
            {'table': 'dr_zzjgjbsjxx', 'field': 'DWMC', 'title': '单位名称', 'editable': 'T', 'type': 'table', 'value': 'dr_zzjgjbsjxx:DWH,DWMC', 'where': 'DWH IN %(departments)s', 'create': 'True', },

    """
    from jx.sqlalchemy_env import db, text

    payroll = str(req.COOKIES.get('payroll'))
    try:
        v = eval(str(req.POST.dict()))
        set_to = trim(str(v[v['field']]))
        if set_to.find('null') != -1:
            return JsonResponse({'success': False, 'msg': '更新失败：值中含有 null'})
        v['set_to'] = set_to

        v['class_name'] = 'view_' + v['menu']
        if v['menu'] in rule_tables:
            v['class_name'] = 'kh_' + v['menu']

        column = get_column_info(v['class_name'], v['field'])
        if column['type'] == 'table':
            fields = get_field_name(column['value'])
            data_set = get_static_data(payroll, column['value'], column['where'])
            for data in data_set:
                if str(data[fields[1]]) == str(set_to):
                    v['set_to'] = str(data[fields[0]])
                    v['field'] = fields[0]
            column = get_column_info(v['class_name'], fields[0])

        if len(column) == 0:
            return JsonResponse({'success': False, 'msg': '更新失败：未找到所编辑字段'})

        model_dr_class = get_model_dr_class(column['table'])
        uniques = model_dr_class.get_unique_condition()
        v['table'] = column['table']

        if len(uniques) == 0:
            if column['table'] != v['class_name']:
                return JsonResponse({'success': False, 'msg': '更新失败：数据唯一性条件未定义'})
            v['where'] = "id=:id"
        else:
            if len(uniques[0]) and isinstance(uniques[0], str):
                uniques = [uniques, ]

            for unique in uniques:
                counts = __get_data_counters(column['table'], unique, v)

                update_unique = True if v['field'] in unique else False
                if update_unique:
                    if counts['count'] != 0 or column['table'] != v['class_name']:
                        return JsonResponse({'success': False, 'msg': '更新失败：数据唯一性条件未定义!'})
                    v['where'] = "id=:id"
                else:
                    if counts['count'] != 1:
                        return JsonResponse({'success': False, 'msg': counts['message']})
                    v['where'] = counts['where']

        sql_update = "UPDATE " + column['table'] + " SET " + v['field'] + "=:set_to WHERE " + v['where']
        logger.info(sql_update)
        db.execute(text(sql_update), v)
        db.commit()
        return JsonResponse({'success': True, 'msg': '成功更新为：' + set_to})

    except Error:
        db.rollback()
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '更新失败：数据库错误'})

    except:
        db.rollback()
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '更新失败：数据库错误!!!'})


@check_login
@sys_error
def get_title(req):
    v = eval(str(req.GET.dict()))
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
    cursor = connection.cursor()
    payroll = str(req.COOKIES.get('payroll'))
    v = eval(str(req.GET.dict()))

    module_name = 'module'
    view_prefix = 'view'
    if v['menu'] in rule_tables:
        module_name = 'rule'
        view_prefix = 'kh'

    v['table'] = ("view_" + v['menu']).upper().lower()
    sql_table_count = """SELECT COUNT(information_schema.VIEWS.TABLE_SCHEMA) AS count
        FROM information_schema.VIEWS WHERE TABLE_SCHEMA='kpi' AND TABLE_NAME=%s"""
    logger.info(sql_table_count)
    cursor.execute(sql_table_count, [v['table']])
    count = dictfetchall(cursor)[0]["count"]
    if int(count) == 0:
        logger.info(v['table'] + '->' + str(count))
        return JsonResponse({'total': 0, 'rows': []})

    v['start'] += "-01 00:00:00"
    v['end'] = month_end(v['end'])
    if 'sort' not in v or v['sort'] in ('', None):
        v['sort'] = 'id'
        v['order'] = 'DESC'
    if v['order'].lower() not in ('asc', 'desc'):
        v['order'] = 'DESC'

    # code  # DWH if type=='d', JZGH if type=='u'
    # type  # d - department, u - user
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

    sql_count = "SELECT COUNT(*) AS count FROM " + v['table']
    sql_content = "SELECT * FROM " + v['table']
    sql_query_set = []

    # NOTE: add stamp as filter condition
    sql_where = " WHERE 1=1 "
    if v['menu'] not in ('zzjgjbsjxx', 'jzgjcsjxx', ):
        sql_where += """
            AND DATE_FORMAT(stamp, '%%Y-%%m-%%d')>=%s
            AND DATE_FORMAT(stamp, '%%Y-%%m-%%d')<=%s    
        """
        sql_query_set.append(v['start'][:10])
        sql_query_set.append(v['end'][:10])

    if v['menu'] == 'khjghz':
        items = eval(str(v['item']))
        if isinstance(items, str):
            sql_where += " AND 1=0 "
        else:
            if '1' in v['item']:
                sql_where += " AND XM IS NULL AND KHMC IS NULL"
            if '2' in v['item']:
                sql_where += " AND XM IS NOT NULL AND KHMC IS NULL"
            if '3' in v['item']:
                sql_where += " AND XM IS NULL AND KHMC IS NOT NULL"

    if v['type'] == 'u':
        sql_where += " AND JZGH=%s"
        sql_query_set.append(v['payroll'])
    elif v['type'] == 'd':
        if v['menu'] == 'zzjgjbsjxx':  # 组织机构基本数据信息
            sql_where += " AND (DWH='%(department)s' OR LSDWH='%(department)s')" % v
        else:
            from jx.module import VIEW_ZZJGJBSJXX
            __dpts = VIEW_ZZJGJBSJXX.get_managed_departments(v['department'])
            sql_where += " AND DWH IN " + str(__dpts).replace('[', '(').replace(']', ')')
    else:
        sql_where += " AND 1=0"

    # NOTE: filter out admin
    if sql_where.find('JZGH') != -1 or v['menu'] in ('jzgjcsjxx', ):
        sql_where += ' AND JZGH NOT IN ("admin", "")'

    sql_search = ""
    if 'search' in v and v['search'] not in ('', None):
        from jx.views import get_module_static_method
        search_columns = get_module_static_method(v['menu'], 'get_search_columns', module_name, view_prefix)
        if search_columns:
            sql_search = " AND (1=0 "
            for col in search_columns:
                sql_search += " OR " + col + " LIKE %s"
                sql_query_set.append('%' + trim(str(v['search'])) + '%')
        sql_search += ")"

    logger.info(sql_count + sql_where + sql_search)
    cursor.execute(sql_count + sql_where + sql_search, sql_query_set)
    count = dictfetchall(cursor)[0]["count"]

    sql_olo = ' ORDER BY %s %s LIMIT ' + str(int(v['limit'])) + ' OFFSET ' + str(int(v['offset']))
    sql_query_set.append(v['sort'])
    sql_query_set.append(v['order'])

    logger.info(sql_content + sql_where + sql_search + sql_olo)
    cursor.execute(sql_content + sql_where + sql_search + sql_olo, sql_query_set)
    select_out = dictfetchall(cursor)

    return JsonResponse({'total': count, 'rows': select_out})


@check_login
@sys_error
def get_json(req):
    v = eval(str(req.GET.dict()))
    try:
        from jx.views import get_module_static_method
        arr = v['path'].split('|')
        content, title_columns = {}, get_module_static_method(arr[0], 'get_title_columns')
        for tc in title_columns:
            if tc['field'] == arr[1]:
                for act in tc['action']:
                    if act['type'] == arr[2]:
                        content = act['content']

        # {'type': 'table', 'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH=:this', 'to': 'JZGH:JZGH,XM'}}]}
        # {'type': 'table', 'value': 'view_jzgjcsjxx:JZGH,XM', 'where': 'DWH IN :this', 'to': 'JZGH:JZGH,XM'}}]}
        if content:
            t_f = content['value'].split(":")
            sql = "SELECT " + t_f[1] + " FROM " + t_f[0]
            if trim(content['where']) != "":
                if content['where'].find('DWH IN :this') != -1:
                    from jx.module import VIEW_ZZJGJBSJXX
                    ds = VIEW_ZZJGJBSJXX.get_managed_departments(trim(v['this']))
                    sql += " WHERE " + content['where'].replace(':this', str(ds).replace('[', '(').replace(']', ')'))
                else:
                    sql += " WHERE " + content['where']

            if sql.find('JZGH') != -1 or trim(t_f[0]) in ['dr_jzgjcsjxx', 'view_jzgjcsjxx', ]:
                sql += ' AND JZGH NOT IN ("admin")'

            from jx.sqlalchemy_env import db, text
            try:
                logger.info(sql)
                pro = db.execute(text(sql), v)
                db.commit()
                return JsonResponse(fetchall_sqlalchemy_in_dict(pro), safe=False)
            except:
                db.rollback()
                logger.error(sys_info())
    except:
        logger.error(sys_info())

    return JsonResponse([], safe=False)


@check_login
@sys_error
def get_class_view(req):
    return JsonResponse([], safe=False)

    from jx.module import generate_class_view
    return JsonResponse(generate_class_view('module', False), safe=False)


@check_login
@sys_error
def change_password(req):
    msg = ''
    try:
        from jx.sqlalchemy_env import db, text

        npwd = pc.encrypt(req.POST.get('newpwd'))
        sql_change = "UPDATE jx_sysuser" + " SET password=:pwd, time_pwd=NOW() WHERE payroll=:payroll"
        logger.info(sql_change)
        try:
            db.execute(text(sql_change), {'pwd': npwd, 'payroll': req.COOKIES.get('payroll')})
            db.commit()
            msg += ': 修改密码成功<br>'
            return JsonResponse({'success': True, 'msg': msg})
        except:
            db.rollback()
            msg += ': 数据库错误<br>'
            logger.error(sys_info())
            return JsonResponse({'success': False, 'msg': msg})
    except:
        msg += ': 系统异常<br>'
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': msg})


@check_login
def delete_data(req):
    payroll = str(req.COOKIES.get('payroll'))
    v = eval(str(req.POST.dict()))
    data = json.loads(v['data'])
    function = v['menu']
    count = v['count']

    module_class = get_module_class(function)
    delete_tables = module_class.get_delete_tables()

    msg = ''
    from jx.sqlalchemy_env import db, text
    for d_table in delete_tables:
        model_dr_class = get_model_dr_class(d_table)
        uniques = model_dr_class.get_unique_condition()
        msg_tablename = model_dr_class.__tablename__CH__ if hasattr(model_dr_class, '__tablename__CH__') \
            else model_dr_class.__tablename__

        if len(uniques) == 0:
            return JsonResponse({'success': False, 'msg': '删除失败：数据唯一性条件未定义'})

        if len(uniques[0]) and isinstance(uniques[0], str):
            uniques = [uniques, ]
        unique = uniques[len(uniques)-1]

        where = '1=1'
        for u in unique:
            where += ' AND ' + u + "=:" + u
        if where == '1=1':
            msg += msg_tablename + ': 删除失败, 未定义数据唯一性条件<br>'
            continue

        if function == 'zzjgjbsjxx':  # can't delete parent and current
            from jx.module import VIEW_ZZJGJBSJXX
            user = get_user_information(payroll)
            __dpts = VIEW_ZZJGJBSJXX.get_managed_departments(str(user['DWH'])).remove(str(user['DWH']))
            where += " AND DWH IN " + str(__dpts).replace('[', '(').replace(']', ')')

        if function == 'jzgjcsjxx':  # can't delete self and admin
            where += " AND JZGH NOT IN ('admin', '" + payroll + "')"

        # TODO: add more WHERE conditions to keep system safe
        for c in range(0, int(count)):
            sql_delete = "DELETE FROM " + d_table + " WHERE " + where
            try:
                logger.info(sql_delete)
                db.execute(text(sql_delete), data[c])
                db.commit()
                msg += msg_tablename + ': 删除数据成功<br>'
            except Error as e:
                db.rollback()
                logger.error(sys_info())
                msg += msg_tablename + ': 删除失败, ' + str(e) + '<br>'
    try:
        db.commit()
    except Error:
        logger.error(sys_info())
        db.rollback()

    return JsonResponse({'success': True, 'msg': msg})


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

    # NOTE: 考核结果明细有 note and stamp
    if 'create_data_item' in v:
        if v['create_data_item'] == 'khjgmx':
            val['note'] = v['note']
            val['stamp'] = now()

    return val


@check_login
def create_data(req):
    from jx.sqlalchemy_env import db, text

    _v = eval(str(req.POST.dict()))
    function = _v['create_data_item']

    module_class = get_module_class(function)
    create_tables = module_class.get_create_tables()

    msg, status = '', False
    for d_table in create_tables:
        model_dr_class = get_model_dr_class(d_table)
        columns = model_dr_class.get_column_label()
        uniques = model_dr_class.get_unique_condition()
        msg_tablename = model_dr_class.__tablename__CH__ if hasattr(model_dr_class, '__tablename__CH__') \
            else model_dr_class.__tablename__

        if len(uniques) == 0:
            msg += msg_tablename + ': 创建失败, 数据主键未定义!<br>'
            continue

        tv = __format_create_value(_v, columns)

        if len(uniques[0]) and isinstance(uniques[0], str):
            uniques = [uniques, ]

        msg_unique = ''
        for unique in uniques:
            counts = __get_data_counters(d_table, unique, tv)
            if counts['count'] != 0:
                msg_unique += msg_tablename + ': 创建失败, 数据主键重复('
                for u in unique:
                    msg_unique += __translate_column_to_chinese(columns, u) + '->' + str(tv[u]) + ', '
                msg_unique = msg_unique[:-2]
                msg_unique += ')<br>'

        if msg_unique != '':
            msg += msg_unique
            continue

        unique = uniques[len(uniques)-1]
        c_key = __transform_key_to_chinese(tv, columns)
        rec, c_str, v_str, u_str, not_processed = __row_replace_key(c_key, columns, unique)

        sql_insert = "INSERT INTO " + d_table + "(" + c_str + ") VALUES (" + v_str + ")"

        logger.info(sql_insert)
        try:
            db.execute(text(sql_insert), rec)
            msg += msg_tablename + ': 新建数据成功<br>'
            status = True
        except Error as e:
            logger.error(sys_info())
            msg += msg_tablename + ': 创建失败, ' + str(e) + '<br>'
            status = False

    try:
        db.commit() if status else db.rollback()
    except Error as e:
        logger.error(sys_info())
        msg += '数据提交错误, ' + str(e) + '<br>'
        status = False

    return JsonResponse({'success': status, 'msg': msg})


@check_login
@sys_error
def staffinfo(req):
    payroll = str(req.COOKIES.get('payroll'))
    user = SysUser.objects.get(payroll=payroll)

    v = eval(str(req.GET.dict()))
    if 'sort' not in v or v['sort'] in ('', None):
        v['sort'] = 'id'
        v['order'] = 'DESC'

    if v['order'].lower() not in ('asc', 'desc'):
        v['order'] = 'DESC'

    l_user = SysUser.objects.get(payroll=payroll)
    v['role'] = l_user.role_id

    sql_count = """ SELECT COUNT(*) AS count FROM view_sysuser """
    sql_content = """ SELECT * FROM view_sysuser """

    sql_query_set = []
    sql_where = " WHERE role_id!=1 AND usertype_id!=1" if payroll != 'admin' else " WHERE 1=1"
    if user.role_id == 1:
        pass
    elif user.role_id in (2, 3):
        from jx.module import VIEW_JZGJCSJXX 
        ds = VIEW_JZGJCSJXX.get_managed_departments(payroll)
        sql_where += (" AND DWH IN " + trim(str(ds)).replace('[', '(').replace(']', ')')) if ds else " AND DWH=%s"
    else:
        sql_where += ' AND 1=0'

    if 'payroll' in v:
        sql_where += ' AND payroll=%s'
        sql_query_set.append(trim(str(v['payroll'])))

    sql_search = ""
    if 'search' in v and v['search'] not in ('', None):
        search_columns = ['payroll', 'XM', 'DWMC']
        if search_columns:
            sql_search = " AND (1=0 "
            for col in search_columns:
                sql_search += " OR " + col + " LIKE %s"
                sql_query_set.append('%' + trim(str(v['search'])) + '%')
            sql_search += ")"

    cursor = connection.cursor()
    logger.info(sql_count + sql_where + sql_search)
    cursor.execute(sql_count + sql_where + sql_search, sql_query_set)
    count = dictfetchall(cursor)[0]["count"]

    sql_olo = ' ORDER BY %s %s LIMIT ' + str(int(v['limit'])) + ' OFFSET ' + str(int(v['offset']))
    sql_query_set.append(v['sort'])
    sql_query_set.append(v['order'])

    logger.info(sql_content + sql_where + sql_search + sql_olo)
    cursor.execute(sql_content + sql_where + sql_search + sql_olo, sql_query_set)
    select_out = dictfetchall(cursor)

    for s in select_out:
        s['password'] = ''

    return JsonResponse({'total': count, 'rows': select_out})


@check_login
@sys_error
def run_kpi(req):
    from jx.rule import KH_KHJGMX, KH_KHJGHZ, KH_KHPC
    from jx.module import VIEW_JZGJCSJXX
    from jx.sqlalchemy_env import db

    try:
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
        query = query.filter(KH_KHJGMX.DWH.in_(departments), KH_KHJGMX.KHNF == year, KH_KHJGMX.GZH.notlike('ZJ%'))
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

    except Error:
        db.rollback()
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '绩效考核运行失败：数据库错误'})


@check_login
def custermize_kpi(req):
    from jx.rule import KH_KHGZDZ
    from jx.sqlalchemy_env import db

    try:
        payroll = str(req.COOKIES.get('payroll'))

        v = eval(str(req.POST.dict()))
        data = json.loads(v['data'])
        year = __format_value(v['year'], "DateTime")
        user = get_user_information(payroll)

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

    except Error:
        db.rollback()  # NOTE: OR open SQLAlchemy autocommit
        logger.error(sys_info())
        return JsonResponse({'success': False, 'msg': '绩效考核定制失败：数据库错误'})
