# -*- coding:utf-8 -*-

# Name: base_log
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2020-01-13 14:29

from .base_model import BaseModel


class BaseLog(BaseModel):
    """
    日志类基类
    """

    def save(self):
        pass
