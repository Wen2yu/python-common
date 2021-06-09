#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" __module_name__ """

__author__ = 'zhangjiawen'


def set_attrs(o, **kwargs):
    for k, v in kwargs.items():
        if hasattr(o, k):
            setattr(o, k, v)
