# -*- coding:utf-8 -*-

# Name: BaseEnumItem
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2019/12/12 9:23


class BaseEnumItem(object):
    def __init__(self, code, desc):
        self._code = code
        self._desc = desc

    @property
    def code(self):
        return self._code

    @property
    def desc(self):
        return self._desc

    def __repr__(self):
        return self._code, self._desc

    def __str__(self):
        return self._desc
