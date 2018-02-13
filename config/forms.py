#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.forms import ModelForm
from config.models import HostInfo


class HostInfoForm(ModelForm):
    """
    this is the HostInfo form
    """

    class Meta:
        model = HostInfo
        fields = ["ip", "host_name", "belong_projects", "user", "ssh_key", "memo"]


class EditHostInfoForm(ModelForm):
    """
    this is the HostInfo form
    """

    class Meta:
        model = HostInfo
        fields = ["host_name", "belong_projects", "user", "ssh_key", "memo"]
