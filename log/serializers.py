#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework import serializers
from models import OperaRecord


class OperaRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperaRecord
        fields = ('id', 'user', 'request_method', 'request_url', 'create_time')
