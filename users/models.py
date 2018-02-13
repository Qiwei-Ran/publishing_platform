#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import validators
from django.core.mail import send_mail
import uuid
from rest_framework.authtoken.models import Token
from collections import OrderedDict

# Create your models here.

# 做数据库的枚举，choise用
auth_id = [(u"普通用户", u"普通用户"), (u"管理员", u"管理员")]
auth_gid = [(1001, u"运维部"), (1002, u"网络部"), (1003, u"研发部"), (1004, u"测试部")]


# 部门组
class DepartmentGroup(models.Model):
    department_groups_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'组名')
    description = models.TextField(verbose_name=u'介绍', blank=True, null=True)

    # 当调用department_groups_name的时候会返回它的Unicode表现形式
    def __unicode__(self):
        return self.department_groups_name

    class Meta:
        verbose_name = u"部门组"
        verbose_name_plural = verbose_name


# 部门表
class DepartmentMode(models.Model):
    department_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'部门名称')
    description = models.TextField(verbose_name=u'介绍', blank=True, null=True)
    desc_gid = models.IntegerField(verbose_name=u'部门组', choices=auth_gid, blank=True, null=True)

    # created_by = models.OneToOneField('users.CustomUser',on_delete=models.CASCADE)

    def __unicode__(self):
        return self.department_name

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = verbose_name


# 用户管理类，不生成表
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


# 用户表
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.Email and password are required.
    Other fields are optional.用户的session_keys是定时更新的，到了过期时间，就会更新session_key，
    然后将该session_key存入session表
    """

    email = models.EmailField(_(u'邮箱'), max_length=254, unique=True)
    username = models.CharField(_(u'用户名'), max_length=30, unique=True)
    first_name = models.CharField(_(u'名字'), max_length=30, blank=False)
    last_name = models.CharField(_(u'last_name'), max_length=30, blank=False)
    department = models.ForeignKey(DepartmentMode, blank=True, null=True, verbose_name=u'部门', related_name="users")

    mobile = models.CharField(_(u'手机'), max_length=30, blank=False,
                              validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                    _('Enter a valid mobile number.'),
                                                                    'invalid')])
    session_key = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'session_key')
    user_key = models.TextField(blank=True, null=True, verbose_name=u'用户登录key')
    menu_status = models.BooleanField(default=False, verbose_name=u'用户菜单状态')
    user_active = models.BooleanField(verbose_name=u'设置密码状态', default=0)
    uuid = models.CharField(max_length=64, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'name': self.first_name,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'mobile': self.mobile,
            'department': self.department,
            'is_staff': self.is_staff,
        })


    @property
    def is_valid(self):
        if self.is_active and self.is_staff:
            return True
        return False

    def __unicode__(self):
        return self.first_name

    __str__ = __unicode__


class PrivateToken(Token):
    """Inherit from auth token, otherwise migration is boring"""

    class Meta:
        verbose_name = _('Private Token')


class AccessKey(models.Model):
    id = models.UUIDField(verbose_name='AccessKeyID', primary_key=True,
                          default=uuid.uuid4, editable=False)
    secret = models.UUIDField(verbose_name='AccessKeySecret',
                              default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.CASCADE,
                             related_name='access_key')

    def get_id(self):
        return str(self.id)

    def get_secret(self):
        return str(self.secret)

    def __unicode__(self):
        return str(self.id)

    __str__ = __unicode__
