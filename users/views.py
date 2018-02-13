#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import json
import logging

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
# Create your views here.
from django.views.generic import ListView
from django.views.generic import UpdateView, CreateView
# class based view
from django.views.generic.edit import FormView

from log.decorator import record
from perms.auth_handle import auth_dict_class
from users.forms import UserCreateForm, DepartmentFrom, LoginForm, UserEditForm
from users.models import (CustomUser, DepartmentMode)
from utils.generate_uuid import web_uuid

logger = logging.getLogger('publishing_platform.web.view')
from django.views.generic import View
from django.shortcuts import get_object_or_404
from perms.decorator import auth_check

"""
用户管理
"""


# 用户列表
@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserListView(ListView):
    template_name = 'users/user_list.html'
    context_object_name = 'uf'
    queryset = CustomUser.objects.filter(is_active=True, is_staff=True)


'''
@login_required()
def user_list(request):
    u"""
    查看用户列表
    :param request:
    :return: HTML Page
    """
    status = check_auth(request, "add_department")
    if not status:
        logger.error('%s: Do not have enough  power access user list.', request.user.first_name)
        return render(request, 'default/error_auth.html', locals())

    uf = CustomUser.objects.all().filter(is_active=True, is_staff=True)
    # return render_to_response('users/user_list.html', result)
    return render(request, 'users/user_list.html', locals())
'''


# 修改账户
@method_decorator(auth_check('edit_user'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserEditView(UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'users/user_edit.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        logger.info('%s: save user info change to database', self.request.user.first_name)
        return super(UserEditView, self).form_valid(form)


'''
@record()
@login_required()
def user_edit(request, id):
    """
    修改账户
    :param request:
    :return:
    """
    status = check_auth(request, "edit_user")
    if not status:
        logger.error('%s: Do not have enough  power to edit user info.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    # 使用表单
    try:
        data = CustomUser.objects.get(id=id)
    except ObjectDoesNotExist as e:
        logger.error('%s: Can not get user info for edit.', request.user.first_name)
        raise e
    else:
        data_time = time.strftime('%Y-%m-%d %H:%M:$S', time.localtime(time.time()))
        if request.method == 'POST':
            uf = UserEditForm(request.POST, instance=data)
            if uf.is_valid():
                uf.save()
                logger.info('%s: save user info change to database', request.user.first_name)
                return HttpResponseRedirect("/users/user_list/")
        else:
            uf = UserEditForm(instance=data)
            return render(request, 'users/user_edit.html', locals())
        '''

'''
# 禁用/恢复用户
@record()
@login_required()
def status_change(request, id):
    """
    用户状态控制
    :param request:
    :param id:
    :return:
    """
    status = check_auth(request, 'edit_user')
    if not status:
        logger.error('%s: Do not have enough  power to edit user status.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        user = CustomUser.objects.get(pk=id)
    except ObjectDoesNotExist as e:
        logger.error('%s: user manager - can not get user by id.', request.user.first_name)
        raise e
    else:
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        logger.info('%s: Change user status complete.', request.user.first_name)
        return render_to_response('users/user_list.html', locals())
    '''


# 查看禁用账户
@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserDisabledView(ListView):
    template_name = 'users/user_list.html'
    context_object_name = 'uf'
    queryset = CustomUser.objects.filter(is_active=True, is_staff=False)


'''
@login_required()
def user_static(request):
    """
    查看禁用的账户
    :param request:
    :return:
    """
    check_perms = check_auth(request, 'add_department')
    if not check_perms:
        # noinspection SpellCheckingInspection
        logger.error('%s: Do not have enough  power to show dimission user.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        uf = CustomUser.objects.all().filter(is_staff=False, is_active=True)
    except Exception as e:
        logger.error('%s: Get dimisson person data error.', request.user.first_name)
        raise e
    return render_to_response('users/user_list.html', locals())
'''


# 注册/新建用户
@method_decorator(auth_check('add_user'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class NewUserView(CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        form.instance.is_staff = 1
        form.instance.session_key = ""
        form.instance.uuid = web_uuid()
        form.instance.is_active = 1
        return super(NewUserView, self).form_valid(form)


'''
@record()
@login_required()
def register(request):
    """
    添加用户
    :param request:
    :return:
    """
    status = check_auth(request, "add_user")
    if not status:
        logger.error('%s: Do not have enough  power to  create user.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    content = {}
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        try:
            if form.is_valid():
                form.is_staff = 1
                new_user = form.save(commit=False)
                new_user.is_staff = 1
                new_user.session_key = ""
                new_user.uuid = web_uuid()
                new_user.save()
                logger.info('%s: create user complete.', request.user.first_name)
                if EMAIL_PUSH:
                    token = str(hashlib.sha1(
                        new_user.username + new_user.uuid + time.strftime('%Y-%m-%d',
                                                                          time.localtime(time.time()))).hexdigest())
                    url = u'http://%s/accounts/newpasswd/?uuid=%s&token=%s' % (request.get_host(), new_user.uuid, token)
                    mail_title = u'发布平台初始密码'
                    mail_msg = u"""
                    Hi,%s:
                            请点击以下链接初始化账户密码,此链接当天有效:
                                %s
                            有任何问题，请随时和运维组联系。
                        """ % (new_user.first_name, url)
                    send_mail(mail_title, mail_msg, u'发布平台<devops@funshion.net>', [new_user.email], fail_silently=False)
                return HttpResponseRedirect('/users/user_list/')
            else:
                data = UserCreateForm()
                return render_to_response('users/reg.html', locals())
        except Exception as e:
            logger.error('%s: Create user fail.', request.user.first_name)
            raise e
    else:
        data = UserCreateForm()
        return render_to_response('users/reg.html', locals())
    '''


# 被禁用的用户
# noinspection SpellCheckingInspection
@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserDimissionView(ListView):
    template_name = 'users/user_list.html'
    context_object_name = 'uf'
    queryset = CustomUser.objects.filter(is_active=False, is_staff=False)


'''
@login_required()
def user_old(request):
    u"""
    离职用户
    """
    status = check_auth(request, "add_department")
    if not status:
        logger.error('%s: Do not have enough power to look unusable user.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        uf = CustomUser.objects.all().filter(is_active=False, is_staff=False)
    except Exception as e:
        logger.error('%s: Select unusable user error', request.user.first_name)
        raise e
    else:
        return render_to_response('users/user_list.html', locals())
    '''


# 删除用户
@method_decorator(auth_check('delete_user'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserDeleteView(ListView):
    def get(self, *args):
        user = CustomUser.objects.get(id=self.args[0])
        user.is_staff = False
        user.is_active = False
        user.save()
        return HttpResponseRedirect('/users/user_list/')


'''
@record()
@login_required()
def user_delete(request, id):
    u"""
    删除用户,离职用户
    """
    status = check_auth(request, "delete_user")
    if not status:
        logger.error('%s: Do not have enough  power to delete user.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        user = CustomUser.objects.get(pk=id)
        user.is_staff = False
        user.is_active = False
        user.save()
    except Exception as e:
        logger.error('%s: delete user has error: %s', request.user.first_name, e)
    else:
        logger.info('%s: delete user %s complete', request.user.first_name, user.first_name)
    return render_to_response('users/user_list.html', locals())
'''


# 禁用启用账户
@method_decorator(auth_check('delete_user'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class UserStatusView(View):
    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        logger.info('%s: Change user status ok', request.user.first_name)
        return render(request, 'users/user_list.html', locals())


'''
@record()
@login_required()
def user_status(request, id):
    u"""
    禁用启用用户
    """
    status = check_auth(request, "delete_user")
    if not status:
        logger.error('%s: No permission to forbidden user', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    try:
        user = CustomUser.objects.get(pk=id)
    except Exception as e:
        logger.error('%s: Can not get data from user table.', request.user.first_name)
        raise e
    else:
        if user.is_staff:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        logger.info('%s: Change user status ok', request.user.first_name)
        return render_to_response('users/user_list.html', locals())
'''

"""
部门管理
"""


# department manager

# 部门列表
@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class DepartmentListView(ListView):
    template_name = 'users/department_list.html'
    context_object_name = 'content'

    def get_queryset(self):
        self.queryset = DepartmentMode.objects.all()
        content = {}
        for i in self.queryset:
            users_list = []
            dep_all = i.users.all().values("first_name")
            for t in dep_all:
                users_list.append(t.get("first_name"))
            content[i.department_name] = {"user_list": users_list, "department_id": i.id}
        return content


'''
@login_required()
def list_department(request):
    u"""
    部门列表
    :param request:
    :return:
    """
    status = check_auth(request, "add_department")
    if not status:
        logger.error('%s: No permission to show department.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    uf = DepartmentMode.objects.all()
    content = {}
    for i in uf:
        users_list = []
        dep_all = i.users.all().values("first_name")
        for t in dep_all:
            users_list.append(t.get("first_name"))
        content[i.department_name] = {"user_list": users_list, "department_id": i.id}
    return render_to_response('users/department_list.html', locals())
'''


@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class DepartmentAddView(CreateView):
    model = DepartmentMode
    form_class = DepartmentFrom
    template_name = 'users/add_department.html'
    success_url = reverse_lazy('department-list')

    def form_valid(self, form):
        logger.info('%s: Add department success.', self.request.user.first_name)
        return super(DepartmentAddView, self).form_valid(form)


'''
# 部门新增
@record()
@login_required()
def department_add(request):
    """
    添加部门
    :param request:
    :return:
    """
    status = check_auth(request, "add_department")
    if not status:
        logger.error('%s: No permission to add department.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    # 验证post方法
    if request.method == 'POST':
        try:
            a = request.POST.get
            uf = DepartmentFrom(request.POST)
            if uf.is_valid():
                uf.save()
            # return render_to_response('user/department_add.html', locals(), context_instance=RequestContext(request))
            logger.info('%s: Add department success.', request.user.first_name)
            return HttpResponseRedirect("/users/department_list/")
        except Exception as e:
            logger.error('%s: %s', request.user.first_name, e)
            raise e
    else:
        uf = DepartmentFrom()
    return render_to_response('users/add_department.html', locals())
'''


@method_decorator(auth_check('add_department'), name='dispatch')
@method_decorator(record(), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class DepartmentEditView(UpdateView):
    model = DepartmentMode
    form_class = DepartmentFrom
    template_name = 'users/edit_department.html'
    success_url = reverse_lazy('department-list')

    def form_valid(self, form):
        logger.info('%s: Edit department success.', self.request.user.first_name)
        return super(DepartmentEditView, self).form_valid(form)


'''
# 部门修改
@record()
@login_required()
def department_edit(request, id):
    u"""
    修改部门
    :param request:
    :param id:
    :return:
    """
    status = check_auth(request, "add_department")
    if not status:
        logger.error('%s: No permission to edit department.', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())

    data = DepartmentMode.objects.get(id=id)
    if request.method == 'POST':
        try:
            uf = DepartmentFrom(request.POST, instance=data)
            u"验证数据有效性"
            if uf.is_valid():
                uf.save()
            logger.info('%s: Edit department success.', request.user.first_name)
            return HttpResponseRedirect("/users/department_list/")
        except Exception as e:
            raise e
    uf = DepartmentFrom(instance=data)
    return render_to_response('users/edit_department.html', locals())
'''

"""
登录/登出操作
"""


class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_field_name = 'next'

    def form_valid(self, form):
        form_data = form.cleaned_data
        username = form_data['username']
        password = form_data['password']

        try:
            data = CustomUser.objects.get(username=username)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            raise e
            # return render(self.request, 'users/login.html', locals())
        check_data = check_password(password, data.password)
        if check_data:
            login(self.request, data)
            auth_data = auth_dict_class(self.request.user)
            self.request.session["fun_auth"] = auth_data  # 给session添加信息
            user_data = CustomUser.objects.get(email=self.request.user.email)
            user_data.session_key = self.request.session.session_key  # 登录保存新建的session_key到用户表
            user_data.save()
            self.request.session.set_expiry(28800)
            logger.info('%s: login success.', username)
            return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, 'index'))


'''
# 用户登录
def user_login(request):
    """
    用户登录验证
    :param request:
    :return:
    """
    form = LoginForm(request.POST)
    if form.is_valid():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            data = CustomUser.objects.get(username=username)
            check_data = check_password(password, data.password)
            if check_data:
                data.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, data)  # 登录后新建session_key，并保存session到session表
                # 获取权限,并存入session。此处是新建或利旧session数据表记录，跟cookie（存session_key）有关，cookie过期就会新建，不然就会继续用于数据库的读取
                auth_data = auth_class(request.user)
                request.session["fun_auth"] = auth_data  # 给session添加信息

                user_data = CustomUser.objects.get(email=request.user)
                user_data.session_key = request.session.session_key  # 登录保存新建的session_key到用户表
                user_data.save()
                request.session.set_expiry(28800)
                logger.info('%s: login success.', username)
                # return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(request.GET['next'])
        except:
            return render(request, 'users/login.html', locals(), )
    return render(request, 'users/login.html', locals())
'''


@method_decorator(login_required(), name='dispatch')
class LoginOutView(View):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect("/users/login/?next=/project/show_index/")


'''
# 登出用户
@login_required()
def user_logout(request):
    u"""
        退出登录
        """
    # auth.logout(request)
    request.session.flush()
    return HttpResponseRedirect("/users/login/?next=/project/show_index/")
'''


# 找回密码
def reset_password(request):
    return None


# 菜单状态调整
def menu_class(request):
    user = request.user.username
    try:
        menu = CustomUser.objects.get(username=user)
        if menu.menu_status:
            menu.menu_status = False
            menu.save()
        else:
            menu.menu_status = True
            menu.save()

        content = {"status": 200, "message": "update is ok"}
    except:
        content = {"status": 403, "message": "what ary you doing"}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


# 测试
def user_auth_node(request):
    u"""
    查看用户
    :param request:
    :return:
    """

    return None
