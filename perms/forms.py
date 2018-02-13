#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from models import AuthGroup, UserAuthWeb


class RoleFrom(forms.ModelForm):
    """
    增加权限组的表单
    """
    enable = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((True, '启用'), (False, '禁用')),
        required=True, initial=True,
        widget=forms.RadioSelect,
        label=u"是否启用"
    )

    class Meta:
        model = AuthGroup
        fields = ["group_name", "explanation", "enable"]


class AuthAddForm(forms.ModelForm):
    """
    forms of add_auth
    添加权限的表单
    """

    class Meta:
        model = UserAuthWeb
        fields = ["select_project", "add_project", "del_project", "update_project", "test_deploy", "test_complete",
                  "online_deploy", "add_user", "edit_user", "edit_pass", "delete_user", "add_department", "log_look",
                  "group_name"]


class AuthUserAddForm(forms.ModelForm):
    """
    添加权限组用户
    """

    class Meta:
        model = AuthGroup
        fields = ["group_user"]
