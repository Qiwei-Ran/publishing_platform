#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework_bulk import BulkModelViewSet
from rest_framework import viewsets, response, generics
from rest_framework.views import APIView
from perms.models import AuthGroup
from perms.serializers import AuthGroupSerializer, RoleUpdateUserGroupSerializer
from users.permissions import IsSuperUser
from users.models import CustomUser


class AuthGroupViewSet(viewsets.ModelViewSet):
    """This is Model include"""
    queryset = AuthGroup.objects.all()
    serializer_class = AuthGroupSerializer
    permission_classes = (IsSuperUser,)


class RoleUpdateUserGroupApi(generics.RetrieveUpdateAPIView):
    """Update Roles belong users"""
    queryset = AuthGroup.objects.all()
    serializer_class = RoleUpdateUserGroupSerializer
    permission_classes = (IsSuperUser,)
