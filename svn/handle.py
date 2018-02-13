#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

import pysvn
import locale


class SvnInfo(object):
    def __init__(self, svn_url, check_path, user, user_password):
        self.svn_url = svn_url
        self.out_path = check_path
        self.password = user
        self.username = user_password
        self.client = pysvn.Client()

    def setlocale(self):
        language_code, encoding = locale.getdefaultlocale()
        if language_code is None:
            language_code = 'en_GB'
        if encoding is None:
            encoding = 'UTF-8'
        if encoding.lower() == 'utf':
            encoding = 'UTF-8'
        locale.setlocale(locale.LC_ALL, '%s.%s' % (language_code, encoding))

    def get_login(realm):
        retcode = True
        username = realm.username
        password = realm.password
        save = False
        return retcode, username, password, save

    def checkout_file(self):
        self.client.callback_get_login = self.get_login
        self.client.checkout(self.svn_url, self.out_path)

    def update_file(self):
        self.client.callback_get_login = self.get_login
        self.client.update(self.out_path)
