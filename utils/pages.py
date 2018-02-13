#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'QiweiRan'

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def page_list_return(total, current=1):
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total
    return range(min_page, max_page)


def listing(result_list, request, per_page):
    result_list = result_list
    paginator = Paginator(result_list, per_page)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1
    page_range = page_list_return(len(paginator.page_range)+1, current_page)
    try:
        objects = paginator.page(current_page)
    except (EmptyPage, PageNotAnInteger):
        objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0
    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    return result_list, paginator, objects, page_range, current_page, show_first, show_end
