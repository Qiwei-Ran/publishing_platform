#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'


def enum(**enums):
    return type('Enum', (), enums)


Status = enum(one=0, two=1, three=2, four=3)
