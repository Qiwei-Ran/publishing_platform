from django.conf.urls import url
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter
from users.api import DepartmentModeViewSet
from users import api

app_name = 'users'

router = BulkRouter()
router.register(r'v1/departments', api.DepartmentModeViewSet, 'department')
router.register(r'v1/users', api.UserViewSet, 'users')

'''
department_list = DepartmentModeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
'''

urlpatterns = [
    # url(r'^v1/department_list/$', department_list, name='department-list'),
    url(r'^v1/token/$', api.UserToken.as_view()),
    url(r'v1/profile', api.UserProfile.as_view()),
    url(r'^v1/departments/(?P<pk>\d+)/edit/$', api.DepartmentModeUpdateApi.as_view(), name='department-department')
]

urlpatterns += router.urls
