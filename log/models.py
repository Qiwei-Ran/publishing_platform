#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from django.utils.timezone import now


# Create your models here.

class OperaRecord(models.Model):
    user = models.CharField(max_length=255, verbose_name=u'用户')
    request_method = models.CharField(max_length=255, verbose_name=u'请求方法')
    request_url = models.CharField(max_length=255, verbose_name=u'请求URL')
    request_date = models.CharField(max_length=255, verbose_name=u'请求数据')
    create_time = models.DateTimeField(max_length=255, verbose_name=u'时间', default=now)

    class Meta:
        verbose_name = u'操作记录'
        verbose_name_plural = verbose_name
