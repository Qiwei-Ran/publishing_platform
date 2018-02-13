#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

admin.autodiscover()

schema_view = get_schema_view(title='User API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='project/show_index')),
    # project manager
    url(r'^project/', include('web.urls')),
    # config manager
    url(r'^config/', include('config.urls')),
    # auth manager
    url(r'^users/', include('users.urls.views_urls')),
    url(r'^perms/', include('perms.urls.views_urls')),
    # log record
    url(r'^log/', include('log.urls')),

    # rest_framework test
    # url(r'^api-auth/', include('web.urls', namespace='web')),

    # api urls
    url(r'^api/users/', include('users.urls.api_urls', namespace='api-users')),
    url(r'^api/perms/', include('perms.urls.api_urls', namespace='api-perms')),
    url(r'^api-docs/', schema_view, name='docs'),

]
