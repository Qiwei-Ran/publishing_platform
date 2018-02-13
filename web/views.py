#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from web.models import PpProjectDetail, PpProject
from web import services, version_operation
from perms.auth_handle import check_auth
from svn import handle
from web.forms import ProjectForm
from utils import pages, push_core
from log.decorator import record
from django.urls import reverse_lazy

import os
import logging

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from perms.decorator import auth_check

projectDetailServices = services.ProjectDetailServices()
projectServices = services.ProjectServices()
logger = logging.getLogger('publishing_platform.web.view')


@method_decorator(login_required(), name='dispatch')
class ProjectIndexView(ListView):
    template_name = 'index.html'
    data = {'success': '', 'fail': '', 'wait': ''}

    def get_queryset(self):
        success = PpProjectDetail.objects.filter(deploy_success=0).count()
        fail = PpProjectDetail.objects.filter(deploy_success=1).count()
        wait = PpProjectDetail.objects.filter(deploy_success=2).count()
        self.data['success'] = success
        self.data['fail'] = fail
        self.data['wait'] = wait

    def get_context_data(self, **kwargs):
        context = super(ProjectIndexView, self).get_context_data(**kwargs)
        context['data'] = self.data
        return context


'''
# the first index page
@login_required
def show_index(request):
    status = check_auth(request, "select_project")
    if not status:
        logger.error('%s: Do not have enough  power access project index.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    res = {'success': '', 'fail': '', 'wait': ''}
    try:
        deploy_success = projectDetailServices.list_projects_bydeploy(0).count()
        deploy_fail = projectDetailServices.list_projects_bydeploy(1).count()
        deploy_wait = projectDetailServices.list_projects_bydeploy(2).count()
        res['success'] = deploy_success
        res['fail'] = deploy_fail
        res['wait'] = deploy_wait
    except Exception as e:
        logger.error('%s: Index page Get data from database error: %s ', request.user.first_name, e)
    else:
        return render(request, 'index.html', res)
'''


class ProjectsListView(ListView):
    template_name = 'web/list1_projects.html'
    context_object_name = 'data'

    def get_queryset(self):
        self.queryset = PpProjectDetail.objects.filter(is_del=0)
        return self.queryset


class ProjectListView(ListView):
    template_name = 'web/list_projects.html'
    version_data = {}

    def get_queryset(self):
        self.queryset = PpProjectDetail.objects.filter(is_del=0)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        for item in self.queryset:
            project_versions = PpProject.objects.filter(item.project_name)
            version_list = []
            for i in project_versions:
                version_list.append(i.version)
            self.version_data['version_state'] = project_versions[0].state
            self.version_data['version_create_time'] = project_versions[0].create_time
            self.version_data['version_list'] = version_list
            self.version_data['project_name'] = item.project_name

        context['data'] = self.queryset

        results = []

        project_count = self.queryset.count()

        for project in self.queryset:
            version_list = []

            name = project.project_name

            result = {'id': '', 'version': '', 'state': '', 'name': '', 'create_time': ''}

            project_version = PpProject.objects.filter(project_name=name)

            if project_version:
                version_state = project_version[0].state
                version_create_time = project_version[0].create_time
            else:
                version_state = ''
                version_create_time = ''

            for i in project_version:
                version_list.append(i.version)

            result['id'] = project.id
            result['name'] = name
            result['version'] = version_list
            result['state'] = version_state
            result['create_time'] = version_create_time
            results.append(result)
        result_list, paginator, objects, page_range, current_page, show_first, show_end = pages.listing(results,
                                                                                                        self.request, 2)
        return results

        return None


# list the project page
@login_required()
def list_projects(request):
    status = check_auth(request, "select_project")
    if not status:
        logger.error('%s: Do not have enough  power access project list.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    results = []

    # list all the projects
    try:
        project_list = projectDetailServices.list_all_projects()  # 包含多个查询结果queryset对象的列表queryset
        project_count = projectDetailServices.list_all_projects().count()
        count = {'count': project_count}
        for item in project_list:  # 迭代出单个的queryset
            version_list = []
            res = {'id': '', 'version': '', 'state': '', 'name': '', 'create_time': ''}

            project_name = item.project_name  # 取出该queryset的单个值
            # list the version queryset
            project_version = projectServices.list_all_versions(project_name)  # 根据之前的结果进行查询，结果是多个对象的queryset
            # state和create_time取最小的版本做为默认显示
            if project_version:
                version_state = project_version[0].state
                version_create_time = project_version[0].create_time
            else:
                version_state = ''
                version_create_time = ''
            for i in project_version:
                version_list.append(i.version)  # 取值放入列表
            res['id'] = item.id
            res['name'] = item.project_name
            res['version'] = version_list
            res['state'] = version_state
            res['create_time'] = version_create_time
            results.append(res)
    except Exception as e:
        logger.error('%s: Project_list page Get data from database error: %s ', request.user.first_name, e)
    else:
        result_list, paginator, objects, page_range, current_page, show_first, show_end = pages.listing(results,
                                                                                                        request, 2)
        return render_to_response('web/list_projects.html', locals())


# project detail
@method_decorator(auth_check('update_project'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class ProjectDetailView(ListView):
    template_name = 'web/project_detail.html'
    context_object_name = 'results'

    def get_queryset(self):
        self.queryset = get_object_or_404(PpProjectDetail, id=self.args[0])
        return self.queryset


'''
@login_required()
def list_detail(request, project_id):
    status = check_auth(request, "update_project")
    if not status:
        logger.error('%s: Do not have enough  power access project detail.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    try:
        detail = projectDetailServices.list_project_detail_by_id(id=project_id)
        return render_to_response('web/project_detail.html', {'results': detail}
                                  )
    except Exception as e:
        logger.error('%s: Project detail page Get data from database error: %s ', request.user.first_name, e)
        raise e
'''


@record()
@login_required()
def project_add(request):
    status = check_auth(request, "add_project")
    if not status:
        logger.error('%s: Do not have enough  power add project.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    if request.method == 'POST':
        init = request.GET.get("init", False)
        uf = ProjectForm(request.POST)
        uf.project_name = request.POST['project_name']
        project_version = request.POST['project_version']
        war_path = request.POST['war_path']

        ss = uf.is_valid()
        m = uf.errors
        state = 0
        if uf.is_valid():
            project_name = uf.cleaned_data['project_name']
            if PpProjectDetail.objects.filter(project_name=uf.project_name) and PpProject.objects.filter(
                    version=project_version, project_name=project_name):
                emg = u'添加失败，该项目 %s 已存在！' % project_name
                return render_to_response('web/project_add.html', locals())
            try:
                if not PpProjectDetail.objects.filter(project_name=uf.project_name):
                    uf.save()
                if not PpProject.objects.filter(
                        version=project_version, project_name=project_name):
                    projectServices.save_project(project_name, war_path, project_version, state)
            except Exception as e:
                logger.error('%s: Save project to database error: %s.', request.user.username, e)
                raise e
            logger.info('%s: Add the project %s success', request.user.username, project_name)
            if not init:
                return HttpResponseRedirect('/project/list/')
            else:
                return HttpResponseRedirect('/project/list/')
        else:
            return render_to_response('web/project_add.html', locals())
    else:
        uf = ProjectForm()

        return render_to_response('web/project_add.html', locals())


# the def is the project_add page's ajax swap
# no inspection SpellCheckingInspection
@login_required()
def check_project(request):
    status = check_auth(request, "add_project")
    if not status:
        logger.error('%s: Do not have enough  power to check_out project', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    data = request.POST
    dict1 = {'project_version': '', 'project_name': '', 'status': '', 'war_path': ''}
    # reckon the md5 of the project
    svn_addr = data['svn_address']
    svn_addr_str = svn_addr.encode("utf-8").strip()
    if svn_addr_str.strip().endswith('/'):
        project_name = svn_addr_str[0:-1].split('/')[-1]
    else:
        project_name = svn_addr_str.split('/')[-1]
    check_path = '/projects/%s' % project_name

    # check out the new repository
    try:
        svn_info = handle.SvnInfo(svn_addr, check_path, 'test1', 123456)
        svn_info.setlocale()
        svn_dir = os.path.exists(svn_info.out_path + '/.svn')
        if not svn_dir:
            os.system('mkdir %s -p' % svn_info.out_path)
            svn_info.checkout_file()
        # get project name,version and return ajax
        check_result = version_operation.VersionOperation()
        version, war_path = check_result.first_get_version(check_path)
        dict1['status'] = 0
        dict1['project_name'] = project_name
        dict1['project_version'] = version
        dict1['war_path'] = war_path
    except Exception as e:
        logger.error('%s: Can not check the project to new repo: %s', request.user.first_name, e)
    else:
        return JsonResponse(dict1)


'''
class ProjectDeleteBatchView(View):
    def post(self, request):
        ids = str(request.POST.get('ids'))
        for id in ids.split(','):
            project_name = PpProjectDetail.objects.get(id=id).project_name
            project_name_str = project_name.encode("utf-8")

            PpProjectDetail.objects.get(id=id).update(is_del=1)
            PpProject.objects.filter(project_name=project_name_str).update(is_del=1)
        return HttpResponseRedirect('/project/list/')
'''


@record()
@login_required()
def project_delete_batch(request):
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: Do not have enough  power to delete project batch.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    ids = str(request.POST.get('ids'))
    for id in ids.split(','):
        project_name = projectDetailServices.list_project_detail_by_id(id).project_name
        project_name_str = project_name.encode("utf-8")
        try:
            projectDetailServices.delete_logic_by_id(id)
            projectServices.delete_logic_by_name(project_name_str)
            logger.warn('%s: delete project %s success', request.user.first_name, project_name)
        except Exception as e:
            logger.error('%s: Cant delete project batch:%s', request.user.first_name, e)
    return HttpResponseRedirect('/project/list/')


class ProjectDeleteView(UpdateView):
    model = PpProjectDetail

    def get_object(self, queryset=None):
        self.queryset = PpProjectDetail.objects.get(id=self.kwargs['id'])

    def get(self, request, *args):
        project_name = self.queryset.project_name
        PpProjectDetail.is_del = 1
        PpProject.objects.filter(project_name=project_name).update(is_del=1)
        logger.error('%s: Delete project %s', request.user.first_name, project_name)
        return HttpResponseRedirect('/project/list/')


@record()
@login_required()
def project_delete(request, project_id):
    status = check_auth(request, "del_project")
    if not status:
        logger.error('%s: can not run delete project', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        project_name = projectDetailServices.list_project_detail_by_id(project_id).project_name
        project_name_str = project_name.encode("utf-8")
        projectDetailServices.delete_logic_by_id(project_id)
        projectServices.delete_logic_by_name(project_name_str)
        logger.error('%s: Delete project %s', request.user.first_name, project_name)
    except Exception as e:
        logger.error('%s: Delete error: %s ', request.user.first_name, e)
    return HttpResponseRedirect('/project/list/')


@record()
@login_required()
def project_search(request):
    """
    条件搜索项目
    :param request:
    :return: result of condition
    """
    status = check_auth(request, "select_project")
    if not status:
        return render_to_response('default/error_auth.html', locals())

    results = []
    status = request.GET.get('change_status', '')
    keyword = request.GET.get('keyword', '')
    s_url_split = request.get_full_path().split('&')
    s_url_split.pop()
    s_url = '&'.join(s_url_split)

    if status:
        status = int(status)
    else:
        status = ""
    if keyword:
        project_list = projectDetailServices.list_project_by_keyword(keyword)
    else:
        project_list = projectDetailServices.list_all_projects()
    project_count = project_list.count()
    count = {'count': project_count}
    for item in project_list:  # 迭代出单个的queryset
        version_list = []
        res = {'id': '', 'version': '', 'state': '', 'name': '', 'create_time': ''}

        project_name = item.project_name  # 取出该queryset的单个值
        # list the version queryset
        try:
            project_version = projectServices.list_all_versions(project_name)  # 根据之前的结果进行查询，结果是多个对象的queryset
            # state和create_time取最小的版本做为默认显示
            if project_version:
                version_state = project_version[0].state
                version_create_time = project_version[0].create_time
            else:
                version_state = ''
                version_create_time = ''
            for i in project_version:
                version_list.append(i.version)  # 取值放入列表
            res['id'] = item.id
            res['name'] = item.project_name
            res['version'] = version_list
            res['state'] = version_state
            res['create_time'] = version_create_time
            search = 1
            results.append(res)
            result_list, paginator, objects, page_range, current_page, show_first, show_end = pages.listing(results,
                                                                                                            request, 2)
        except Exception as e:
            logger.log('%s: Can not get version in search: %s', request.user.first_name, e)
    if 'page' in request.get_full_path():
        return render_to_response('web/list_projects.html', locals())
    else:  # restful framework api test
        return render_to_response('web/project_list_search.html', locals())


@login_required()
def project_change_version(request):
    status = check_auth(request, "select_project")
    if not status:
        return render_to_response('default/error_auth.html', locals())

    dicts = {'project_name': '', 'project_version': '', 'state': '', 'create_time': ''}
    try:
        select_version = request.GET.get('select_version')
        project_name = select_version.split('-')[0]
        project_version = select_version.split('-')[1]
    except Exception as e:
        logger.error('%s: Get version string is error.', request.user.first_name)
        raise e
    results = projectServices.list_project_by_version(project_name, project_version)
    state = results.state
    create_time = results.create_time

    dicts['project_name'] = project_name
    dicts['project_version'] = project_version
    dicts['state'] = state
    dicts['create_time'] = create_time

    return JsonResponse(dicts)
    # return dicts
    # return render_to_response('web/select_version.html', locals(), context_instance=RequestContext(request))


@record()
def project_test_push(request):
    """
    the function will implement publish the war package to the test env.
    :param request:
    :param id: the project id
    :return: the status code, 0 is ok , 1 is fail.
    """
    '''
    status = check_auth(request, "select_project")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))
    '''

    if request.method == 'POST':
        select_version = request.POST.get('select_version')
        project_name = select_version.split('-')[0]
        project_version = select_version.split('-')[1]
        try:
            version_data = PpProject.objects.get(version=project_version, project_name=project_name)
            project_data = PpProjectDetail.objects.get(project_name=project_name)
            war_path = version_data.war_path
            target_address = project_data.test_address
            remote_location = '/root/'
            result = push_core.push_war(war_path, target_address, remote_location)
            update = PpProject.objects.filter(version=project_version, project_name=project_name).update(state=1)
            logger.info('%s: Push the %s version %s Success', request.user.first_name, project_name, project_version)
        except Exception as e:
            raise e
        else:
            return HttpResponse('ok')


'''
@api_view(['GET', 'POST'])
def show_api(request):
    if request.method == 'GET':
        project_list = projectDetailServices.list_projects_bydeploy(0)
        serializer = PpProjectDetailSerializer(project_list, many=True)
        return Response(serializer.data)
'''
'''
        name = 'ok' + m['svn_address']
        version = '1.1.1'
'''
