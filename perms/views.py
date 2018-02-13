#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import json
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
# Create your views here.
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.utils.decorators import method_decorator
from log.decorator import record
from perms.auth_handle import auth_session_class
from perms.forms import RoleFrom, AuthAddForm, AuthUserAddForm
from perms.models import AuthGroup, UserAuthWeb
from users.models import CustomUser
from perms.decorator import auth_check

logger = logging.getLogger('publishing_platform.web.view')


# 权限首页
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RoleListView(ListView):
    template_name = 'perms/index.html'
    group_user_count = {}

    def get_queryset(self):
        self.queryset = AuthGroup.objects.order_by("-date_time")

        for i in self.queryset:
            try:
                data_id = AuthGroup.objects.get(uuid=i.uuid)
            except ObjectDoesNotExist as e:
                logger.error('%s: Get role data by id error.', self.request.user.first_name)
                raise e
            self.group_user_count[i.uuid] = data_id.group_user.count()

    def get_context_data(self, **kwargs):
        context = super(RoleListView, self).get_context_data(**kwargs)
        context['group_user_count'] = self.group_user_count
        context['data'] = self.queryset
        return context


'''
@login_required()
def roles_list(request):
    u"""
    权限组首页
    param request:
    return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to list the role', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    data = AuthGroup.objects.all().order_by("-date_time")
    group_user_count = {}

    for i in data:
        try:
            data_id = AuthGroup.objects.get(uuid=i.uuid)
            group_user_count[i.uuid] = data_id.group_user.all().count()
        except Exception as e:
            logger.error('%s: Get role data by id error.', request.user.first_name)
            raise e
    return render_to_response('perms/index.html', locals())
'''


@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RoleAddView(CreateView):
    model = AuthGroup
    form_class = RoleFrom
    template_name = 'perms/role_add.html'
    success_url = reverse_lazy('role-list')

    def form_valid(self, form):
        logger.info('%s: success add roles', self.request.user.first_name)
        return super(RoleAddView, self).form_valid(form)

    def form_invalid(self, form):
        return self.form_class


'''
# 角色添加
@record()
@login_required()
def roles_add(request):
    u"""
    角色添加
    :param request:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to add role.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    data = RoleFrom()
    if request.method == 'POST':
        try:
            uf = RoleFrom(request.POST)
            if uf.is_valid():
                uf.save()
                logger.info('%s: success add roles', request.user.first_name)
                return HttpResponseRedirect('/perms/roles_list/')
        except Exception as e:
            logger.error('%s: role add error: %s', request.user.first_name, e)
            raise e
        return render_to_response('perms/role_add.html', locals())
    else:
        return render_to_response('perms/role_add.html', locals())
    '''


# 添加/更改权限
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class AuthAddView(View):
    form = AuthAddForm
    context_object_name = 'data'

    def get(self, request, **kwargs):
        form = self.form
        uuid = str(self.kwargs['uuid'])
        try:
            group_uuid = AuthGroup.objects.get(uuid=uuid)
            group_data = UserAuthWeb.objects.get(group_name=uuid)
            data = AuthAddForm(instance=group_data)
        except:
            data = AuthAddForm()
        return render(request, 'perms/add_auth.html', locals())

    def post(self, request, uuid):
        uuid = str(uuid)
        try:
            group_data = UserAuthWeb.objects.get(group_name=uuid)
            uf = AuthAddForm(request.POST, instance=group_data)  # 已有该条记录就更新，instance会填充已有记录的UUID
        except:
            uf = AuthAddForm(request.POST)  # 没有该条数据的uuid，就新建保存

        if uf.is_valid():
            uf.save()  # 保存权限信息到数据库
            logger.info('%s: update %s role perms success.', request.user.first_name, group_data.group_name)
            auth_session_class(uuid)  # 刷新该用户组中用户session的权限到数据库
            return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4))


'''
    self.object = UserAuthWeb.objects.get(group_name=self.kwargs['uuid'])
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    context = self.get_context_data(object=self.object, form=form)
    return self.render_to_response(context)
'''

'''    
     model = UserAuthWeb
     form_class = AuthAdd
     template_name = 'perms/add_auth.html'
 '''

'''
    def get_object(self, queryset=None):
        self.queryset = UserAuthWeb.objects.filter(group_name=self.kwargs['uuid'])
        return self.queryset
'''
'''
    def form_valid(self, form):
        form.save()
        # group_uuid = AuthGroup.objects.get(uuid=uuid)
        auth_session_class(self.kwargs['uuid'])
        logger.info('%s: update %s role perms success.', self.request.user.first_name, form.data.group_name)
        return super(AuthAddView, self).form_valid(form)
'''

'''
@record()
@login_required()
def add_auth(request, uuid):
    """
    添加权限
    :param request:
    :param uuid:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to add auth.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    uuid = str(uuid)
    group_uuid = AuthGroup.objects.get(uuid=uuid)

    try:
        group_data = UserAuthWeb.objects.get(group_name=uuid)  # 以此判断是否已有权限数据
        data = AuthAdd(instance=group_data)
    except:
        data = AuthAdd()

    if request.method == 'POST':
        try:
            uf = AuthAdd(request.POST, instance=group_data)  # 已有该条记录就更新，instance会填充已有记录的UUID
        except:
            uf = AuthAdd(request.POST)  # 没有该条数据的uuid，就新建保存

        if uf.is_valid():
            uf.save()  # 保存权限信息到数据库
            logger.info('%s: update %s role perms success.', request.user.first_name, group_data.group_name)
            auth_session_class(uuid)  # 刷新该用户组中用户session的权限到数据库
    return render_to_response('perms/add_auth.html', locals())
'''


# 删除角色
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RoleDeleteView(DeleteView):
    model = AuthGroup
    success_url = reverse_lazy('role-list')


'''
@record()
@login_required()
def delete_role(request, uuid):
    """
    删除权限，权限组
    :param request:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to delete role.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        uuid = str(uuid)
        group_uuid = AuthGroup.objects.get(uuid=uuid)
        group_uuid.group_user.clear()
        group_uuid.delete()
        logger.info('%s: Delete role %s success.', request.user.first_name)
    except Exception as e:
        logger.error('%s: Delete role failed.', request.user.first_name)
        raise e
    return HttpResponseRedirect('/perms/roles_list/')
'''


# 成员管理
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class GroupUserAddView(View):
    form = AuthAddForm

    def get(self, request, uuid):
        form = self.form
        uuid = str(uuid)
        data_id = AuthGroup.objects.get(uuid=uuid)

        data = AuthUserAddForm(instance=data_id)
        user_all = CustomUser.objects.all()

        all_user = data_id.group_user.all()
        user_list = [x.first_name for x in all_user]
        return render(request, 'perms/group_user.html', locals())

    def post(self, request, uuid):
        uuid = str(uuid)
        data_id = AuthGroup.objects.get(uuid=uuid)

        uf = AuthUserAddForm(request.POST, instance=data_id)  # 只用该角色组的group_user数据做表单
        if uf.is_valid():
            uf.save()
            logger.info('%s: update user from role %s permission success.', request.user.first_name,
                        data_id.group_name)
            auth_session_class(uuid)
            return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4))


'''
@record()
@login_required()
def add_group_user(request, uuid):
    """
    添加权限组用户,成员管理功能
    :param request:
    :param uuid:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to add group_user', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    uuid = str(uuid)
    data_id = AuthGroup.objects.get(uuid=uuid)

    if request.method == 'POST':
        try:
            uf = AuthUserAddForm(request.POST, instance=data_id)  # 只用该角色组的group_user数据做表单
            if uf.is_valid():
                uf.save()
                logger.info('%s: update user from role %s permission success.', request.user.first_name,
                            data_id.group_name)
                auth_session_class(uuid)
        except Exception as e:
            raise e
    data = AuthUserAddForm(instance=data_id)
    user_all = CustomUser.objects.all()

    all_user = data_id.group_user.all()
    user_list = [x.first_name for x in all_user]

    return render_to_response('perms/group_user.html', locals())
'''


# 修改角色
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RoleEditView(UpdateView):
    model = AuthGroup
    template_name = 'perms/edit_role.html'
    form_class = RoleFrom

    def form_valid(self, form):
        if self.request.is_ajax():
            form.save()
            auth_session_class(self.kwargs['pk'])
            logger.info('%s: Success change the role %s', self.request.user.first_name, form.data.get('group_name'))
            return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4))
        return super(RoleEditView, self).form_valid(form)


'''
@record()
@login_required()
def edit_role(request, uuid):
    """
    修改role角色
    :param request:
    :param uuid:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No perms to edit role', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    uuid = str(uuid)
    group_uuid = AuthGroup.objects.get(uuid=uuid)

    if request.method == 'POST':
        try:
            uf = RoleFrom(request.POST, instance=group_uuid)
            if uf.is_valid():
                uf.save()
                auth_session_class(uuid)
                logger.info('%s: Success change the role %s', request.user.first_name, group_uuid.group_name)
                return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4, ))
        except Exception as e:
            logger.error('%s: Edit role %s failed:', request.user.first_name, e)
            raise e
    else:
        data = RoleFrom(instance=group_uuid)
    return render_to_response('perms/edit_role.html', locals())
'''


# 角色状态更改
@method_decorator(auth_check('administrator'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RoleStatusView(View):
    def get(self, request, uuid):
        uuid = str(uuid)
        group_uuid = AuthGroup.objects.get(uuid=uuid)
        if group_uuid.enable:
            group_uuid.enable = False
            group_uuid.save()
            auth_session_class(uuid)
        else:
            group_uuid.enable = True
            group_uuid.save()
            auth_session_class(uuid)
        logger.info('%s: Change user status ok', request.user.first_name)
        return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4, ))


'''
@record()
@login_required()
def role_status(request, uuid):
    """
    角色状态转换
    :param request:
    :return:
    """
    status = check_auth(request, "administrator")
    if not status:
        logger.error('%s: No permission to change status of role', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    try:
        uuid = str(uuid)
        group_uuid = AuthGroup.objects.get(uuid=uuid)
    except ValueError as e:
        logger.error(e)
        raise e
    if group_uuid.enable:
        group_uuid.enable = False
        group_uuid.save()
        auth_session_class(uuid)
    else:
        group_uuid.enable = True
        group_uuid.save()
        auth_session_class(uuid)
    return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4, ))
'''

'''
# 发布权限？
def auth_swan(request):
    u"""
    权限首页
    :param request:
    :return:
    """
    return None
'''
