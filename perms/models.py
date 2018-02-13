#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from django.db import models
from users.models import CustomUser
from django.core.urlresolvers import reverse


# Create your models here.


# 权限组表
class AuthGroup(models.Model):
    """
    权限组
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group_name = models.CharField(max_length=100, verbose_name=u'角色名称', unique=True)
    group_user = models.ManyToManyField(CustomUser, blank=True, verbose_name=u'所属用户')
    enable = models.BooleanField(default=True, verbose_name=u'是否启用')
    explanation = models.TextField(verbose_name=u'角色描述')
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.group_name

    def get_absolute_url(self):
        return reverse('role-list', self)

    class Meta:
        verbose_name = u"角色管理"
        verbose_name_plural = verbose_name


# 具体权限表，与用户相关
class UserAuthWeb(models.Model):
    """
    web app权限，1表示有权限，0表示没有权限，所有数据全部外键关联user表，当用户删除时相应权限也随之删除
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    u"""
    项目管理
    """
    select_project = models.BooleanField(default=False, verbose_name=u"查看项目")
    add_project = models.BooleanField(default=False, verbose_name=u"新增项目")
    del_project = models.BooleanField(default=False, verbose_name=u"删除项目")
    update_project = models.BooleanField(default=False, verbose_name=u"修改项目")
    u"""
    发布管理
    """
    test_deploy = models.BooleanField(default=False, verbose_name=u"测试发布")
    test_complete = models.BooleanField(default=False, verbose_name=u"测试完成")
    online_deploy = models.BooleanField(default=False, verbose_name=u"线上发布")
    u"""
    用户管理
    """
    add_user = models.BooleanField(default=False, verbose_name=u'添加用户')
    edit_user = models.BooleanField(default=False, verbose_name=u'修改用户')
    edit_pass = models.BooleanField(default=False, verbose_name=u"修改密码")
    delete_user = models.BooleanField(default=False, verbose_name=u"删除用户")
    add_department = models.BooleanField(default=False, verbose_name=u"部门管理")
    u"""
    日志
    """
    log_look = models.BooleanField(default=False, verbose_name=u"日志记录")
    group_name = models.ForeignKey(AuthGroup, verbose_name=u'所属角色', help_text=u"添加角色组权限")

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u"权限管理"
        verbose_name_plural = verbose_name


# sudo权限的，貌似不相关
class AuthSudo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group_name = models.CharField(max_length=64, verbose_name=u"组名", help_text=u"sudo组")
    shell = models.TextField(verbose_name=u'命令')
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.group_name

    class Meta:
        managed = True
        db_table = 'AuthSudo'
        verbose_name = u"sudo授权"
        verbose_name_plural = verbose_name
