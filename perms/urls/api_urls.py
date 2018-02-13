from django.conf.urls import url
from perms import api
from rest_framework_bulk.routes import BulkRouter

app_name = 'perms'

router = BulkRouter()
router.register(r'v1/roles', api.AuthGroupViewSet, 'roles')

urlpatterns = [
    url(r'^v1/roles/(?P<pk>[^/]+)/user_manager/$', api.RoleUpdateUserGroupApi.as_view()),
]

urlpatterns += router.urls
