#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import models
from django.core import serializers


class ProjectDetailServices(object):
    # select all projects
    @staticmethod
    def list_all_projects():
        result = models.PpProjectDetail.objects.filter(is_del=0)
        return result

    @staticmethod
    def list_projects_bydeploy(deploy_status):
        result = models.PpProjectDetail.objects.filter(deploy_success=deploy_status)
        return result

    def list_deploy_projects_bydate(self, time):
        result = models.PpProjectDetail.objects.filter(create_time=time)
        result = serializers.serialize("json", result)
        return result

    def list_project_detail_by_id(self, id):
        result = models.PpProjectDetail.objects.get(id=id)
        return result

    def lis_project_detail_by_name(self, name):
        result = models.PpProjectDetail.objects.get(project_name=name)
        return result

    def list_project_by_keyword(self, keyword):
        result = models.PpProjectDetail.objects.filter(project_name__contains=keyword, is_del=0)
        return result

    def delete_logic_by_id(self, id):
        p = models.PpProjectDetail.objects.get(id=id)
        p.is_del = 1
        p.save()


class ProjectServices(object):
    @staticmethod
    def list_all_versions(project_name):
        result = models.PpProject.objects.filter(project_name=project_name)
        return result

    def list_projects_detail(self):
        result = models.PpProject.objects.all()
        return result

    def save_project(self, project_name, war_path, project_version, state):
        models.PpProject.objects.create(
            project_name=project_name,
            version=project_version,
            war_path=war_path,
            state=state,
        )

    def list_project_by_version(self, project_name, project_version):
        result = models.PpProject.objects.get(project_name=project_name, version=project_version)
        return result

    def delete_logic_by_name(self, name):
        models.PpProject.objects.filter(project_name=name).update(is_del=1)
