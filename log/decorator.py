#!/usr/bin/env python
# -*- coding:utf-8 -*-

from models import OperaRecord
from django.core import serializers
import json
import re


def record():
    """The decorator will record the post operate to db"""

    def deco(func):
        def _deco(request, *args, **kwargs):
            if request.method == "POST":
                username = request.user.first_name
                request_method = request.method
                request_url = request.path
                json_data = json.dumps(request.POST)
                # noinspection SpellCheckingInspection
                request_data = re.sub(r'"csrfmiddlewaretoken"[^,]+,', '', json_data)
                data = OperaRecord(user=username, request_method=request_method, request_url=request_url,
                                   request_date=request_data)
                data.save()
                return func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)

        return _deco

    return deco
