#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.shortcuts import render_to_response, HttpResponseRedirect
from config.models import HostInfo
from perms.auth_handle import check_auth
from config.forms import HostInfoForm, EditHostInfoForm
from utils.generate_uuid import web_uuid
import logging
from log.decorator import record

# Create your views here.

from django.views.generic import DeleteView, UpdateView, CreateView

logger = logging.getLogger('publishing_platform.web.view')


# 主机可用列表

def host_list(request):
    '''
    perm_code = check_auth(request, 'administrator')
    if not perm_code:
        render_to_response('default/error_auth.html', locals(), context_insance=RequestContext(request))
    '''
    data = HostInfo.objects.filter(is_del=0)
    return render_to_response("config/host_list.html", locals())


@record()
def host_add(request):
    """
    add the host info
    :param request:
    :return:
    """
    '''
    perm_code = check_auth(request, 'administrator')
    if not perm_code:
        render_to_response('default/error_auth.html', locals(), context_insance=RequestContext(request))
    '''
    if request.method == 'POST':
        try:
            uf = HostInfoForm(request.POST)
            if uf.is_valid():
                data = uf.save(commit=False)
                # data.uuid = web_uuid()
                data.uuid = web_uuid().replace('-', '')
                data.save()
                logger.info('create new host ok')
                return HttpResponseRedirect('/config/host_list/')
        except Exception as e:
            logger.error('can not create new host:', e)
            raise e
    else:
        uf = HostInfoForm()
        return render_to_response('config/host_add.html', locals())


@record()
def host_del(request, uuid):
    """
    删除主机
    :param request:
    :param uuid:
    :return:
    """
    '''
        perm_code = check_auth(request, 'administrator')
        if not perm_code:
            render_to_response('default/error_auth.html', locals(), context_insance=RequestContext(request))
    '''
    try:
        data = HostInfo.objects.get(uuid=uuid)
        data.delete()
        logger.info('success delete host %s', data.host_name)
    except Exception as e:
        raise e
    return HttpResponseRedirect('/config/host_list')


@record()
def host_edit(request, uuid):
    """
    this is a edit function of host_info
    :param request: Post
    :param uuid:
    :return: save result
    """
    '''
            perm_code = check_auth(request, 'administrator')
            if not perm_code:
                render_to_response('default/error_auth.html', locals(), context_insance=RequestContext(request))
        '''

    data = HostInfo.objects.get(uuid=uuid)

    if request.method == 'POST':
        try:
            uf = EditHostInfoForm(request.POST, instance=data)
            if uf.is_valid():
                uf.save()
                logger.info('success edit host %s') % data.host_name
                return HttpResponseRedirect('/config/host_list/')
        except Exception as e:
            raise e
    else:
        uf = EditHostInfoForm(instance=data)
        return render_to_response('config/host_edit.html', locals())
