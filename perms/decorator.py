from perms.auth_handle import check_auth
from django.shortcuts import render
import logging
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth.decorators import login_required, user_passes_test

logger = logging.getLogger('publishing_platform.web.view')


def auth_check(auth):
    @wraps(auth, assigned=available_attrs(auth))
    def deco(func):
        @wraps(func, assigned=available_attrs(func))
        def _deco(request, *args, **kwargs):
            status = check_auth(request, auth)
            if status:
                return func(request, *args, **kwargs)
            else:
                logger.error('%s: No permission to list the role', request.user.first_name)
                return render(request, 'default/error_auth.html', locals())
        return _deco
    return deco


'''
def auth_check(auth, login_url=None):
    @wraps(auth, assigned=available_attrs(auth))
    def check_perms(request, user):
        status = check_auth(request, user, auth)
        if status:
            return True
        else:
            logger.error('%s: No permission to list the role', request.user.first_name)
            # return render(request, 'default/error_auth.html', locals())
    return user_passes_test(check_perms, login_url=login_url)
'''

'''
    @wraps(auth, assigned=available_attrs(auth))
    def check(auth):
        auth = auth_check_deco(auth)
        return auth
'''
