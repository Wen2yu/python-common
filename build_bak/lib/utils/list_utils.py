# -*- coding:utf-8 -*-
# Author : 'zhangjiawen'
# Data : 2019/11/18 0018 12:40


def first(items, condition=None, def_val=None):
    if len(items) > 0:
        if condition:
            for i in items:
                if condition(i):
                    return i
        else:
            return items[0]
    return def_val

