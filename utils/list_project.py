#!/usr/bin/env python
# -*- coding: utf-8 --*--
import os
import re


class ListProjects(object):
    @staticmethod
    def list_all_projects():
        p = re.compile('.*?\.war')
        f = os.walk(r'/projects/')
        result = []
        try:
            for root, dirs, files in f:
                for m in files:
                    if p.search(m):
                        result.append(os.path.join(root, m))
        except NameError:
            return None
        return result
