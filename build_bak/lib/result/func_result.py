# -*- coding:utf-8 -*-
# Author : 'zhangjiawen'
# Data : 2019/11/18 0018 12:40

from code import FuncRetCode
from utils.operation_utils import add


class FuncResult:

    def __init__(self, fun_ret_code: FuncRetCode, data=None, desc=None, msg: dict=None):
        code_item = fun_ret_code
        if desc is not None:
            code_item.desc = desc
        self.code = code_item
        self.data = data
        self.msg = msg

    def set_data(self, data):
        self.data = data

    def set_msg(self, msg: dict):
        self.msg = msg

    def add_msg(self, key, msg):
        if self.msg.get(key):
            self.msg[key] = add(self.msg[key], msg)
        else:
            self.msg[key] = msg

    def get_code(self):
        return self.code.value

    def get_code_val(self):
        return self.get_code().code

    def get_code_desc(self):
        return self.get_code().desc

    @property
    def is_success(self):
        return self.get_code_val() == FuncRetCode.SUCCESS.value.code

    @property
    def no_handle(self):
        return self.get_code_val() == FuncRetCode.NO_HANDLE.value.code

    @property
    def no_data(self):
        return self.get_code_val() == FuncRetCode.NO_DATA.value.code

    def __repr__(self):
        return '<FuncResult[%r, %r]>' % (self.code, type(self.data))
