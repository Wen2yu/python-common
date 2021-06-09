# -*- coding:utf-8 -*-

# Name: json_utils
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2019-12-31 16:50

import json
from code.json_encoder import DateEncoder


def dumps(item):
    return json.dumps(item, cls=DateEncoder)


def loads(json_str, **kwargs):
    return json.loads(json_str, encoding='utf8', **kwargs)