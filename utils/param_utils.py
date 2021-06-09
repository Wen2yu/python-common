# -*- coding:utf-8 -*-

# Name: param_utils
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2020-01-03 10:13

import time

from .date_utils import cur_day_begin, add_days
from .log_utils import log


def gen_task_params(app, **kwargs):
    today = cur_day_begin()
    yesterday = add_days(today, -1)
    old_params = kwargs if kwargs else None
    if not (kwargs.get('begin') and kwargs.get('end')):
        kwargs.update({'begin': yesterday, 'end': today})
    if not kwargs.get('ts'):
        kwargs['ts'] = int(time.time())
    log(app, 'old_params: %s, new_params: %s' % (old_params, kwargs))
    return kwargs


def handle_receive_args(args):
    kw = {}
    for (k, v) in args.items():
        kw[k] = v
    return kw
