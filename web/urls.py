#!/usr/bin/env python3

from django.conf.urls import include, url
from web import views

urlpatterns = [
    url(r'^show_index/$', views.ProjectIndexView.as_view(), name='index'),
    url(r'^list/$', views.list_projects, name='project-list'),

    url(r'^list1', views.ProjectsListView.as_view()),

    url(r'^add/$', views.project_add),
    url(r'^detail/(\d+)/$', views.ProjectDetailView.as_view()),
    # url(r'^test/(\d+)/$', views.ProjectDetailView.as_view()),
    # url(r'^1/$', 'views.show_api'),
    url(r'^check_project_ajax/$', views.check_project),
    url(r'^delete_batch/$', views.project_delete_batch),
    url(r'^delete/(?P<id>\d+)/$', views.project_delete),
    url(r'^search_project_ajax/$', views.project_search),
    url(r'^select_version_ajax/$', views.project_change_version),
    # publish functions about test  and product env
    url(r'^test_push/$', views.project_test_push),
]
