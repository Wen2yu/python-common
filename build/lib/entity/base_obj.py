# -*- coding:utf-8 -*-
# Author : 'zhangjiawen'
# Data : 2019/11/18 0018 12:40

from common.utils.date_utils import convert_val_to_datetime
from common.utils.json_utils import dumps


class BaseObj(object):

    datetime_cols = []

    def __init__(self, **kwargs):
        if kwargs:
            for key in kwargs.keys():
                if hasattr(self, key):
                    setattr(self, key,
                            convert_val_to_datetime(
                                kwargs.get(key), fmt=kwargs.get('fmt')) if key in self.datetime_cols else kwargs.get(key))

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
