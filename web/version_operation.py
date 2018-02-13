#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import os
import re
from web import services
from utils import list_project
import logging

projectDetailServices = services.ProjectDetailServices()
projectServices = services.ProjectServices()
listProject = list_project.ListProjects()
logger = logging.getLogger('publishing_platform.web.view')


class VersionOperation(object):
    # update all projects version
    @staticmethod
    def update_version():
        projects = listProject.list_all_projects()
        # iteration the list of all projects
        for project in projects:
            try:
                path_list = project.split('/')
                war_path = path_list
                # search the version and name
                package_name = path_list[-1]
                p = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}')
                p_result = p.search(package_name)
                project_version = p_result.group()
                project_name = path_list[-2]
            except Exception as e:
                raise e
            else:
                project_exist = projectDetailServices.lis_project_detail_by_name(project_name)
                version_exist = projectServices.list_project_by_version(project_name=project_name,
                                                                        project_version=project_version)
                if project_exist:
                    if not version_exist:
                        state = 0
                        projectServices.save_project(project_name, war_path, project_version, state)
                        logger.info('System: update %s version %s success', project_name, project_version)

    @staticmethod
    def first_get_version(check_path):
        command = "ls %s" % check_path
        try:
            dirs_string = os.popen(command)
        except Exception as e:
            logger.error('System: Version file do not exist: %s', e)
            raise e
        else:
            dirs_string1 = dirs_string.read()
            dirs_list = dirs_string1.split('\n')
            dirs_list.pop()

            for i in dirs_list:
                p = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}')
                p_result = p.search(i)
                project_version = p_result.group()
                war_path = check_path + '/' + i

                return project_version, war_path
