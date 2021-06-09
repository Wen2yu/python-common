# -*- coding:utf-8 -*-
# Author : 'zhangjiawen'
# Data : 2019/11/18 0018 12:40

import sys
import traceback
from enum import Enum

from code import FuncRetCode
from result import FuncResult
from functools import wraps
from .json_utils import dumps
from .date_utils import now

FUNC_MAP = {}


class OrderType(Enum):
    DEFAULT = 0
    ORDER = 1
    PARALLEL = 2
    OTHER = 3


func_run_switch = {
    OrderType.DEFAULT: lambda funcs: func_stream(funcs),
    OrderType.ORDER: lambda funcs: func_stream(funcs),
    OrderType.PARALLEL: lambda funcs: func_parallel(funcs)
}


def regist_func(name=None, app='', level=1, default_params=None, replace=False):
    """
    regist func for later use
    :param name:
    :param app:
    :param level:
    :param default_params:
    :param replace:
    :return:
    """

    def decorate(f):
        key = '.'.join([app, str(level), name if name else f.__name__])
        if not FUNC_MAP.get(key) or replace:
            FUNC_MAP[key] = (f, default_params)
        else:
            regist_func(name, app, level+1, default_params, replace)
        return f
    return decorate


def run_task(app, log_model=None):
    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            func_params = dumps(kwargs)
            app.logger.info('task[%s] begin, params=%s' % (func.__name__, func_params))
            log_prop = {
                'app': getattr(app, 'name', str(app)),
                'task_name': func.__name__,
                'super_task': kwargs.get('super_task'),
                'create': now(),
                'params': func_params,
            }
            result = func(*args, **kwargs)
            if result:
                log_prop['result_code'] = result.get_code_val()
                log_prop['result_desc'] = result.get_code_desc()
            if log_model and 'save' in dir(log_model):
                log_model(**log_prop).save()
            app.logger.info('task[%s] end, params=%s' % (func.__name__, func_params))
            return result

        return inner
    return wrapper


def func_stream(run_funcs, app=None):
    """
    按顺序依次执行方法列表，如果方法返回值为成功则继续执行下一个方法，否则返回当前方法的结果且不再执行剩下的任务
    :param run_funcs: [(func,  # must
                        params: dict,  # not must, param map
                        data_param_name  # not must, the param key which need the last fun'data returned
                    ),]
    :param app: 调用该方法的app
    :return:
    """
    result = FuncResult(FuncRetCode.NO_HANDLE)
    data = None
    try:
        for run_func in run_funcs:
            func = run_func[0]
            params = None if len(run_func) < 2 else run_func[1]
            if len(run_func) > 2:
                params[run_func[2]] = data
            if params:
                if type(params) == dict:
                    result = func(**params)
                elif type(params) in [list, tuple]:
                    result = func(*params)
                else:
                    result = func(params)
            else:
                result = func()
            if not result:
                if app:
                    app.logger.warning('WARN: the function %s with params {%s} no data returned ' % (
                        func.__name__, params))
                continue
            if result.is_success:
                data = result.data if result.data else data
            elif result.no_handle:
                data = result.data if result.data else []
                if app:
                    app.logger('WARN: the function %s with params {%s} no handle ' % (func.__name__, params))
            elif result.no_data:
                data = []
                if app:
                    app.logger('WARN: the function %s with params {%s} no data returned ' % (
                        func.__name__, params))
            else:
                break
    except Exception as e:
        if app:
            app.logger.error('there has occured errors from %s which caused by %s' % (app.name, e))
        traceback.print_exc(file=sys.stdout)
    return result


def func_parallel(run_funcs):
    """
    并发执行方法列表中的所有方法
    :param run_funcs:
    :return:
    """
    pass


def pre_dependency(func, *args, order_type=OrderType.ORDER):
    """
    run some functions the func depended before run the func
    :param func:
    :param args:
    :param order_type:
    :return:
    """
    run_funcs = []
    for arg in args:
        key, params, data_param_name = arg
        func = FUNC_MAP.get(key)
        run_funcs.append((key, params, data_param_name))
    func_run_switch[order_type](run_funcs)
    return func
