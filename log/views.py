#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
from django.shortcuts import render
from models import OperaRecord
from django.shortcuts import render_to_response
from perms.auth_handle import check_auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import logging
from django.utils.decorators import method_decorator
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from perms.decorator import auth_check
from utils.paginator import Paginator

logger = logging.getLogger('publishing_platform.web.view')


class RecordListView(ListView):
    template_name = 'log/record_list.html'
    context_object_name = 'data'
    queryset = OperaRecord.objects.all()
    paginate_by = 2
    paginator_class = Paginator


'''
def check_record(request):
    status = check_auth(request, 'check_log')
    if not status:
        logger.error('%s: No permission access check record', request.user.first_name)
        return render_to_response('default/error_auth.html', locals())
    data = OperaRecord.objects.all()
    return render_to_response('log/record_list.html', locals())
'''


# 清空操作记录
@method_decorator(auth_check('clear_record'), name='dispatch')
@method_decorator(login_required(), name='dispatch')
class RecordClearView(View):
    def get(self, request):
        OperaRecord.objects.all().delete()
        logger.error('%s: No permission access check record', request.user.first_name)
        return HttpResponseRedirect('/log/record_list/')


'''
def record_clear(request):
    status = check_auth(request, 'clear_record')
    if not status:
        logger.error('%s: No permission access check record', request.user.first_name)

    return HttpResponseRedirect('/log/record_list/')
'''
