#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import os
import sys
import daemon
from apscheduler.scheduler import Scheduler
from handle import SvnInfo

# 将当前文件所在的目录加入系统变量
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'publishing_platform.settings'
django.setup()
from web.version_operation import VersionOperation
from utils import list_project
import logging

listProject = list_project.ListProjects()
scheduler = Scheduler(daemonic=False)
logger = logging.getLogger('publishing_platform.web.view')


# 定时更新svn的文件内容
@scheduler.interval_schedule(seconds=5)
def svn_update_auto():
    # 定时 checkout or update 数据库已记录的所有svn地址
    projects = listProject.list_all_projects()
    # iteration the list of all projects
    try:
        for project in projects:
            path_list = project.split('/')
            project_name = path_list[-2]
            svn_address = 'svn://2.2.2.102/tags/%s' % project_name
            out_address = '/projects/%s' % project_name
            svn_info = SvnInfo(svn_address, out_address, 'test1', 123456)
            svn_info.setlocale()
            if os.path.exists(svn_info.out_path + '/.svn'):
                svn_info.update_file()
                logger.info('Update new soft package %s') % project_name
            else:
                svn_info.checkout_file()
                logger.info('Create new project package %s') % project_name
    except Exception as e:
        logger.info('Create or update project error:', e)
        raise e


# 定时更新所有已建立项目的版本到数据库（会被pynotify替代？）
@scheduler.interval_schedule(seconds=6)
def auto_update_version():
    version_update = VersionOperation()
    version_update.update_version()


if __name__ == '__main__':
    with daemon.DaemonContext():
        scheduler.start()
