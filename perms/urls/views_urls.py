#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'QiweiRan'

from django.conf.urls import url
from perms import views

urlpatterns = [
    # 导航栏
    url(r'^roles_list/$', views.RoleListView.as_view(), name='role-list'),
    url(r'^roles_add/$', views.RoleAddView.as_view()),
    # url(r'^test/$', views.RoleAdd.as_view()),
    # 操作
    url(r'^group_auth/(?P<uuid>[^/]+)/$', views.AuthAddView.as_view()),  # 权限查看与修改
    url(r'^group_user/(?P<uuid>[^/]+)/$', views.GroupUserAddView.as_view()),  # 成员管理
    url(r'^role_edit/(?P<pk>[^/]+)/$', views.RoleEditView.as_view()),
    url(r'^role_delete/(?P<pk>[^/]+)/$', views.RoleDeleteView.as_view()),
    url(r'^role_status/(?P<uuid>[^/]+)/$', views.RoleStatusView.as_view())
]
