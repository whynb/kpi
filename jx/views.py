# coding=utf-8

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.db import connection
from urllib import parse
from jx.util import *
from jx.form import *
from jx.models import *
from jx.exception import *
from jx.password import AES3


time_out = settings.COOKIE_TIME_OUT


def get_menu(payroll):

    def find(ms, mm):
        i = 0
        for s in ms:
            if s['name'] == mm['menu_classify']:
                return i
            i += 1
        return -1

    user = SysUser.objects.get(payroll=payroll)
    menu_list = Role.objects.get(id=user.role_id).menu.all().order_by('menu_icon').values()
    menus = []

    for m in menu_list:
        f = find(menus, m)
        if f != -1:
            menus[f]['items'].append({
                    'name': m['menu_name'],
                    'url': m['menu_addr'],
                })
        else:
            menus.append({
                'name': m['menu_classify'],
                'url': None,
                "items": [{
                    'name': m['menu_name'],
                    'url': m['menu_addr'],
                    }]
                }
            )

    return menus


def get_module_static_method(class_name, method, module_name='module', view_prefix='view'):
    try:
        try:
            module = __import__('jx.'+module_name, fromlist=([module_name]))
        except ImportError:
            module = __import__(module_name)

        v_class = getattr(module, (view_prefix + '_' + class_name).upper())
        return getattr(v_class, method)()

    except:
        logger.error(sys_info())

    return []


def get_menu_name(req):
    path = req.get_full_path().split('/')
    menu_addr = str('/' + path[1] + '/' + path[2] + '/')
    if path[2] == 'base':
        menu_addr += path[3] + '/'
    menu = Menu.objects.get(menu_addr=menu_addr)
    return menu.menu_name


def get_with_users(req):
    payroll = req.COOKIES.get('payroll')
    user = SysUser.objects.get(payroll__exact=payroll)
    menu = req.get_full_path().split('/')[3]
    if menu in ['zzjgjbsjxx', '']:
        return False
    return True if user.role_id in (1, 2) else False


def get_role_menu_permission__(req):
    user = SysUser.objects.get(payroll=req.COOKIES.get('payroll'))
    path = req.get_full_path().split('/')
    menu_addr = str('/' + path[1] + '/' + path[2] + '/')
    if path[2] == 'base':
        menu_addr += path[3] + '/'
    menu = Menu.objects.get(menu_addr=menu_addr)

    cursor = connection.cursor()
    sql = '''
        SELECT b.permission
        FROM jx_role_menu b 
        WHERE b.role_id = %(role_id)s AND b.menu_id = %(menu_id)s
    ''' % {
        'role_id': user.role_id,
        'menu_id': menu.id,
    }

    cursor.execute(sql)
    _dict = dictfetchall(cursor)

    # INFO 2021-03-09 14:30:26,491 views.py views get_role_menu_permission 105: [{'permission': 'y,y,y,y,y,y'}]
    logger.info(_dict)
    for a in _dict:
        c = []
        b = a['permission'].split(',')
        for num in range(0, 6):
            c.append(True if b[num] == 'y' else False)

        return c

    return []


def get_role_menu_permission(req):
    user = SysUser.objects.get(payroll=req.COOKIES.get('payroll'))
    path = req.get_full_path().split('/')
    menu_addr = str('/' + path[1] + '/' + path[2] + '/')
    if path[2] == 'base':
        menu_addr += path[3] + '/'
    menu = Menu.objects.get(menu_addr=menu_addr)

    from jx.sqlalchemy_env import db, text
    sql = '''
        SELECT b.permission
        FROM jx_role_menu b 
        WHERE b.role_id = :role_id AND b.menu_id = :menu_id
    '''

    _dict = db.execute(text(sql), {'role_id': user.role_id, 'menu_id': menu.id,}).fetchall()
    db.commit()  # db.rollback() while execute->except to keep out db deadlock
    logger.info(_dict)
    for a in _dict:
        c = []
        b = a[0].split(',')
        for num in range(0, 6):
            c.append(True if b[num] == 'y' else False)

        return c
    return []


def can_login(req):
    """
    :param req: http request
    :return: True - can login, False - can not
    """

    payroll = req.COOKIES.get('payroll', '')
    if payroll and len(payroll):
        users = SysUser.objects.filter(payroll__exact=payroll)
        
        # TODO: password authentication or cas verification
        return True if users else False

    return False


def check_login(fn):
    """
    Decorator to check if user can login by payroll
    :param fn: request
    :return:
    """
    def log(_req):
        """
        TODO: log each request such as who, when, what...
        :param _req:
        :return:
        """

        return _req

    def wrapper(req, *args, **kwargs):
        try:
            from jx.function import __check_user_auth
            __check_user_auth(log(req))
        except UserAuthException:
            logger.error(sys_info())
            return JsonResponse({'success': False, 'msg': '登录用户没有授权该项操作'})

        try:
            return fn(req, *args, **kwargs) if can_login(req) else HttpResponseRedirect('/jx/')
        except:
            logger.error(sys_info())
            return HttpResponseRedirect('/jx/error/')
    return wrapper


# decorator to catch general exception
def sys_error(fn):
    def wrapper(req, *args, **kwargs):
        try:
            # TODO: verify SQL injection. sqlalchemy->text() DOESN'T work due to compose SQL
            v = eval(str(req.POST.dict()))
            for k, val in v.items():
                if len(k.split(' ')) > 1 or len(val.split(' ')) > 1:
                    return JsonResponse({'success': False, 'tag': '参数错误：所有参数不能含有空格'})

            v = eval(str(req.GET.dict()))
            for k, val in v.items():
                if len(k.split(' ')) > 1 or len(val.split(' ')) > 1:
                    return JsonResponse({'success': False, 'tag': '参数错误：所有参数不能含有空格'})

            return fn(req, *args, **kwargs)
        except:
            logger.error(sys_info())
            return JsonResponse({
                'success': False,
                'data': [],
                'rows': [],
                'message': u'系统异常，请重试',
                'msg': u'系统异常，请重试',
                'tag': u'系统异常，请重试'
            })
    return wrapper


def error(req):
    return HttpResponseRedirect('/jx/') if req.method == 'POST' else render(req, 'error.html')

pc = AES3('boomboomboomboom')
def login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            payroll = form.cleaned_data['payroll']
            # password = '111111'
            k = pc.encrypt(form.cleaned_data['password'])
            users = SysUser.objects.filter(payroll__exact=payroll, password__exact=k)

            if users:
                from jx.function import get_user_information
                user = get_user_information(payroll)

                response = HttpResponseRedirect('/jx/index/')
                response.cookies.clear()
                response.set_cookie('payroll', payroll, time_out)
                response.set_cookie('DWH', user['DWH'] if user else '', time_out)
                response.set_cookie('rollname', parse.quote(users[0].role.role_name), time_out)
                return response
            else:
                response = HttpResponseRedirect('/jx/error/')
                response.cookies.clear()
                return response
    else:
        form = LoginForm()

    res = render(req, 'login.html', {'form': form})
    res.cookies.clear()
    return res


@check_login
def logout(req):
    res = HttpResponseRedirect('/jx/')
    res.cookies.clear()
    return res


@check_login
def index(req):
    if req.method == 'POST':
        return HttpResponseRedirect('/jx/')

    user = str(req.user)
    if settings.CAS:
        users = SysUser.objects.filter(payroll__exact=req.user)
        if not users:
            SysUser(payroll=user, role_id=4, usertype_id=4).save()
    else:
        user = req.COOKIES.get('payroll')

    response = render(
        req,
        'index.html',
        {
            'tips': '开始',
            'menus': get_menu(user),
        }
    )
    response.set_cookie('payroll', user)
    return response


@check_login
def role_manage(req):
    if req.method == 'POST':
        roleform = RoleForm(req.POST)
        if roleform.is_valid():
            role_name = roleform.cleaned_data['role_name']
            is_exist = Role.objects.filter(role_name=role_name).exists()
            if not is_exist:
                r = Role(role_name=role_name)
                r.save()
            else:
                messages.add_message(req, messages.INFO, '该角色已存在')
    else:
        roleform = RoleForm()

    payroll = req.COOKIES.get('payroll')
    user = SysUser.objects.get(payroll__exact=payroll)
    roles = Role.objects.all()
    if user.role_id != 1:
        from django.db.models import Q
        roles = roles.filter(~Q(id=1))
        
    return render(
        req,
        'role_manage.html',
        {
            'menus': get_menu(payroll),
            'roles': roles,
            'roleform': roleform,
            'tips': get_menu_name(req),
        }
    )


@check_login
def role_assign(req):
    usercode = req.COOKIES.get('payroll')
    user = SysUser.objects.get(payroll__exact=usercode)

    def get_roles():
        res = []
        roles = Role.objects.all()
        for role in roles[1:]:
            res.append([str(role.id), str(role.role_name)])
        return res

    logger.info(get_roles())

    return render(
        req,
        'role_assign.html',
        {
            'tips': get_menu_name(req),
            'menus': get_menu(req.COOKIES.get('payroll')),
            'editable': True if user.role_id in (1, 2) else False,
            'roles': get_roles()
        }
    )


@check_login
def base(req):
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[3]
    return render(
        req,
        'base.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns'),
            'title_columns': get_module_static_method(menu, 'get_title_columns'),
            'search_columns': get_module_static_method(menu, 'get_search_columns'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
        },
    )


@check_login
def jxkhgz(req):
    from jx.function import get_static_data, get_field_name
    from jx.module import generate_class_view

    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'jxkhgz.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
            'class_view': generate_class_view('module', False),
        }
    )


@check_login
def khjgmx(req):
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'khjgmx.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
        }
    )


@check_login
def khpc(req):
    # BUG: 系统bug:考核批次页面，点击超级管理员后，再点击东北大学，考核批次数据不再显示，需要刷新页面; 其他页面也有此类问题
    # 在某种特定情况重现，但是没有保存log，与SQLAlchemy的事务处理有关；检查 insert/update execute/commit match
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'base.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
        }
    )


@check_login
def khgzdz(req):
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'base.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
        }
    )


@check_login
def khjghz(req):
    # TODO: add showing radio condition: '单位'（default），'教职工'，'考核名称'
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'khjghz.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
            'sum_footer': True,
        }
    )


@check_login
def bcykh(req):
    from jx.function import get_static_data, get_field_name
    payroll = req.COOKIES.get('payroll')
    menu = req.get_full_path().split('/')[2]
    return render(
        req,
        'base.html',
        {
            'payroll': payroll,
            'tips': get_menu_name(req),
            'menu': menu,
            'menus': get_menu(payroll),
            'editable': get_role_menu_permission(req),
            'with_users': get_with_users(req),
            'hide_columns': get_module_static_method(menu, 'get_hide_columns', module_name='rule', view_prefix='kh'),
            'title_columns': get_module_static_method(menu, 'get_title_columns', module_name='rule', view_prefix='kh'),
            'search_columns': get_module_static_method(menu, 'get_search_columns', module_name='rule', view_prefix='kh'),
            'static_func': get_static_data,
            'static_fields': get_field_name,
        }
    )

