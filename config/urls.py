from django.conf.urls import url
from config import views

urlpatterns = [
    # Host Manager
    url(r'^host_list/$', views.host_list),
    url(r'^host_add/$', views.host_add),
    url(r'^host_edit/(?P<uuid>\w+)/$', views.host_edit),
    url(r'^host_del/(?P<uuid>\w+)/$', views.host_del),
]
