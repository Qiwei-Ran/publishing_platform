#!/usr/bin/env python
# -*-coding: utf-8-*-

from django.db import models

status_id = [(1, u"在线"), (0, u"离线")]


# Create your models here.
class HostInfo(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    ip = models.GenericIPAddressField(verbose_name=u'IP地址')
    host_name = models.CharField(max_length=255, verbose_name=u'主机名')
    belong_projects = models.CharField(max_length=255, verbose_name=u'所属项目')
    user = models.CharField(max_length=255, verbose_name=u'登录用户')
    ssh_key = models.TextField(verbose_name=u'登录key', null=False, blank=False)
    status = models.IntegerField(verbose_name=u'状态', choices=status_id, default=0)
    memo = models.TextField(verbose_name=u"备注", blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    is_del = models.BooleanField(verbose_name=u"是否删除", default=0)

    class Meta:
        verbose_name = u"主机信息"
        verbose_name_plural = verbose_name
        app_label = 'config'
