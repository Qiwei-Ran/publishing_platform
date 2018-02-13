from django.conf.urls import url
from log import views

urlpatterns = [
    url(r'^record_list/$', views.RecordListView.as_view(), name='record-list'),
    url(r'record_clear/$', views.RecordClearView.as_view()),
]
