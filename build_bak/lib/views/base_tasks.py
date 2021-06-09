#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" __module_name__ """

__author__ = 'zhangjiawen'

from utils import first
from utils.func_utils import FUNC_MAP


def get_tasks(app_name, level=0):
    return sorted(filter(
        lambda l: l[0] in [app_name, ''] and l[1] == str(level) if level > 0 else True,
        map(lambda k: k.split('.'), FUNC_MAP.keys())), key=lambda x: (x[0], x[1]), reverse=True)


def get_task_by_name(name: str, app_name=None, level=0):
    key = name if name.count('.') == 2 else '.'.join(first(get_tasks(app_name, level), lambda x: x[2] == name))
    return FUNC_MAP[key]
