# coding=utf-8

# from django.urls import path
# from django.contrib import admin

from django.conf import settings
from django.conf.urls import url
from . import views, function
import cas.views


urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^error/$', views.error, name='error'),

    url(r'^role_manage/$', views.role_manage, name='role_manage'),
    url(r'^role_assign/$', views.role_assign, name='role_assign'),
    url(r'^role_inline_edit', function.role_inline_edit, name='role_inline_edit'),
    url(r'^getpower', function.getpower, name='getpower'),
    url(r'^get_other_power', function.get_other_power, name='get_other_power'),
    url(r'^add_power', function.add_power, name='add_power'),
    url(r'^del_power', function.del_power, name='del_power'),
    url(r'^edit_permission', function.edit_permission, name='edit_permission'),
    url(r'^del_role', function.del_role, name='del_role'),

    url(r'^jx_upload_file', function.jx_upload_file, name='jx_upload_file'),  # duplicate
    url(r'^staffinfo', function.staffinfo, name='staffinfo'),  # duplicate
    url(r'^get_department', function.get_department, name='get_department'),
    url(r'^get_allhrdpmt', function.get_allhrdpmt, name='get_allhrdpmt'),
    url(r'^get_title', function.get_title, name='get_title'),
    url(r'^get_data', function.get_data, name='get_data'),
    url(r'^delete_data', function.delete_data, name='delete_data'),
    url(r'^edit', function.edit, name='edit'),
    url(r'^run_kpi', function.run_kpi, name='run_kpi'),

    url(r'^base/*/', views.base, name='base'),  # 基本数据信息


    # 绩效考核管理
    url(r'^jxkhgz/$', views.jxkhgz, name='jxkhgz'),
    url(r'^khjgmx/$', views.khjgmx, name='khjgmx'),

]

if settings.CAS:
    urlpatterns.append(url(r'^$', cas.views.login, {"next_page": "index"}, name='cas-login'))
    urlpatterns.append(url(r'^logout/', cas.views.logout, {"next_page": "/jx/"}, name='cas-logout'))
else:
    urlpatterns.append(url(r'^$', views.login, name='login'))
    urlpatterns.append(url(r'^logout/', views.logout, name='logout'))
