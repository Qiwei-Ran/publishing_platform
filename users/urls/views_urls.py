#!/usr/bin/env python3

__author__ = 'QiweiRan'

from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^user_list/$', views.UserListView.as_view(), name='user-list'),
    url(r'^user_edit/(?P<pk>\d+)/$', views.UserEditView.as_view()),
    url(r'^user_add/$', views.NewUserView.as_view()),
    url(r'^status/(?P<id>\d+)/$', views.UserStatusView.as_view()),
    url(r'^user_static/$', views.UserDisabledView.as_view()),
    url(r'^user_delete/(\d+)/$', views.UserDeleteView.as_view()),
    # url(r'^detail/$', 'user_detail'),
    url(r'^old/$', views.UserDimissionView.as_view()),
    # url(r'^login/$', views.user_login),
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.LoginOutView.as_view()),
    url(r'^reset_password/$', views.reset_password),
    # department manager
    url(r'^department_list/$', views.DepartmentListView.as_view(), name='department-list'),
    url(r'^department_add', views.DepartmentAddView.as_view()),
    url(r'^department_edit/(?P<pk>\d+)/$', views.DepartmentEditView.as_view()),
]
