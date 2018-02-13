#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: auth_handle.py
#         Desc: 2015-15/3/31:上午11:56
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
from django.contrib.sessions.backends.db import SessionStore

from perms.models import UserAuthWeb, AuthGroup


# 权限检查
def check_auth(request, data):
    try:
        if request.user.is_superuser or request.session["fun_auth"].get(data, False):
            return True
        else:
            return False
    except KeyError:
        return False


# 更新session到数据库
def auth_session_class(uuid):
    u"""
    1.更新session数据表, 更新session权限到数据库session表会立即生效
    2.用户的session_keys是定时更新的，到了过期时间，还是跟cookie也有关系的，就会更新用户的session_key字段，然后将该session_key存入session表
    最好定时清除session数据库的session过期数据，因为没有任何作用了
    :param uuid:
    :return:
    """

    data_id = AuthGroup.objects.get(uuid=uuid)
    all_user = data_id.group_user.all()
    for i in all_user:
        # 根据已有的用户session_key更新session权限到session表
        s = SessionStore(session_key=i.session_key)  # 此处不会新建session，只有存在的session才进行更新session表，login才会新建session

        s["fun_auth"] = auth_dict_class(i)  # 得到的是权限字典
        s.save()  # 更新session数据表
    return True


def auth_dict_class(user):
    """
    更新权限后，保存到字典，返回给session类使用
    刷新页面权限即生效，重新从数据库获取权限信息
    return:
    """
    auth_group_data = {}
    auth_tuple = UserAuthWeb._meta.get_fields()
    auth_list = [f.name for f in auth_tuple]
    auth_list.remove("group_name")
    auth_list.remove("uuid")

    # 判断获取用户的权限
    user_name = user
    if user_name:
        group_auth = user_name.authgroup_set.all().filter(enable=True)
        # 权限
        for auth_uuid in group_auth:
            uuid = str(auth_uuid.uuid)
            data = AuthGroup.objects.get(uuid=uuid)
            try:
                auth_info = UserAuthWeb.objects.get(group_name=data)

                for i in auth_list:
                    try:
                        s = getattr(auth_info, i)
                        if s:
                            auth_group_data[i] = s
                    except AttributeError:
                        pass
            except UserAuthWeb.DoesNotExist:
                pass
        return auth_group_data
    else:
        return auth_group_data
