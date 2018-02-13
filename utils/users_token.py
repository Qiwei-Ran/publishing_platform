#! /usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf import settings
import base64
from django.core.cache import cache
import uuid


def generate_token(request, user):
    expiration = 3600
    remote_addr = request.META.get("X_HTTP_REAL_IP") or \
                  request.META.get('REMOTE_ADDR', '')
    if not isinstance(remote_addr, bytes):
        remote_addr = remote_addr.encode("utf-8")
    remote_addr = base64.b16encode(remote_addr)
    token = cache.get('%s_%s' % (user.id, remote_addr))
    if not token:
        token = uuid.uuid4().hex
        print ('Set cache: %s' % token)
        cache.set(token, user.id, expiration)
        cache.set('%s_%s' % (user.id, remote_addr), token, expiration)
    return token


def refresh_token(token, user, expiration=settings.CONFIG.TOKEN_EXPIRATION or 3600):
    cache.set(token, user.id, expiration)


