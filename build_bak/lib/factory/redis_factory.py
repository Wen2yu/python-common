# -*- coding:utf-8 -*-

# Name: redis_factory
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2020-01-20 11:10

import redis


def get_redis(**kwargs):
    return redis.StrictRedis(connection_pool=redis.ConnectionPool(**kwargs))
