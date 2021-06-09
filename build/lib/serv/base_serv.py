# -*- coding:utf-8 -*-

# Name: base_serv
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2020-07-07 17:14

from sqlalchemy import func, and_, or_


func_switch = {
    'max': func.max,
    'min': func.min,
    'count': func.count
}

condition = {
    '=': lambda x, *y: x == y[0],
    '!=': lambda x, *y: x != y[0],
    '>': lambda x, *y: x > y[0],
    '>=': lambda x, *y: x >= y[0],
    '<': lambda x, *y: x < y[0],
    '<=': lambda x, *y: x <= y[0],
    '>,<': lambda x, *y: and_(x > y[0], x < y[1]),
    '>=,<': lambda x, *y: and_(x > y[0], x < y[1]),
    '>,<=': lambda x, *y: and_(x > y[0], x < y[1]),
    '>=,<=': lambda x, *y: and_(x > y[0], x < y[1]),
    'between': lambda x, *y: and_(x >= y[0], x <= y[1]),
    '<>': lambda x, *y: or_(x > y[0], x < y[1]),
    '<,>=': lambda x, *y: or_(x > y[0], x < y[1]),
    '<=,>': lambda x, *y: or_(x > y[0], x < y[1]),
    '<=,>=': lambda x, *y: or_(x > y[0], x < y[1]),
}


class BaseServ:
    table = None

    def query_data(self, func_cols=None, filters=None, group_by=None, having_condition=None):
        """

        :param func_cols: ((func, col_name),)
        :param filters: 查询条件
        :param group_by:
        :param having_condition: （oper, val）having 条件
        :return:
        """
        fields, nums_condition, = [], None
        if group_by:
            fields = group_by
            for func_col in func_cols:
                fields.append(func_switch[func_col[0]](getattr(self.table, func_col[1], 1)))
                if having_condition and func_col[0] == having_condition[0] and func_col[1] == having_condition[1]:
                    nums_condition = condition[having_condition[2]](
                        func_switch[func_col[0]](getattr(self.table, func_col[1], 1)), *having_condition[3:])
        query = self.table.query(fields)
        if filters:
            query = query.filter(filters)
        if group_by:
            query = query.group_by(*group_by)
        if nums_condition:
            query = query.having(having_condition)

        return query.all()
