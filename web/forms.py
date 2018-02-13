#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from models import PpProjectDetail, PpProject


class ProjectForm(forms.ModelForm):
    class Meta:
        model = PpProjectDetail
        fields = ['svn_address', 'project_name', 'relation_person', 'test_address', 'deploy_address', 'description']
