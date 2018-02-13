#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
# from __future__ import unicode_literals

from django.db import models


class PpOperateRecord(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.CharField(max_length=255, blank=True)
    operation = models.CharField(max_length=255, blank=True)
    project = models.CharField(max_length=255, blank=True)
    crate_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pp_operate_record'
        app_label = 'web'


class PpProject(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    state = models.IntegerField(default=0)
    war_path = models.CharField(max_length=255, unique=False)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField(blank=True, null=True)
    is_del = models.CharField(max_length=255, default=0)

    class Meta:
        db_table = 'pp_project'
        app_label = 'web'


class PpProjectDetail(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?

    project_name = models.CharField(max_length=255, verbose_name=u'项目名')
    svn_address = models.CharField(max_length=255, verbose_name=u'SVN地址')
    relation_person = models.CharField(max_length=255, verbose_name=u'关联人')
    test_address = models.CharField(max_length=255, verbose_name=u'测试发布地址')
    deploy_address = models.CharField(max_length=255, verbose_name=u'线上发布地址')
    description = models.CharField(max_length=255, blank=True, verbose_name=u'备注')
    deploy_success = models.IntegerField(default=0, verbose_name=u'部署成功与否')
    create_time = models.DateTimeField(null=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(blank=True, null=True, verbose_name=u'更新时间')
    is_del = models.CharField(max_length=255, null=True, default=0, verbose_name=u'是否删除')

    class Meta:
        db_table = 'pp_project_detail'
        app_label = 'web'


class PpState(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.IntegerField()

    class Meta:
        db_table = 'pp_state'
        app_label = 'web'
