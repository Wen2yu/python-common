# -*- coding:utf-8 -*-

# Name: json_encoder
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2019-12-31 17:01


from datetime import datetime, date
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


