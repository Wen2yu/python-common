# -*- coding:utf-8 -*-
# Author : 'zhangjiawen'
# Data : 2019/11/18 0018 12:40

from datetime import datetime, timedelta, date
import calendar
import time


MONTHS = 12
HOURS = 23
MINUTES = 59
SECONDS = 59

DATE_FMT = '%Y-%m-%d'
DATE_FMT0 = '%y-%m-%d'
DATE_FMT_HMS = '%Y-%m-%d %H:%M:%S'
DATE_FMT_IMS = '%Y-%m-%d %I:%M:%S'
DATE_FMT0_HMS = '%y-%m-%d %H:%M:%S'
DATE_FMT0_IMS = '%y-%m-%d %I:%M:%S'
DATE_FMT_Ymd = '%Y%m%d'
DATE_FMT_ymd = '%y%m%d'
DATE_FMT_Ymd_HMS = '%Y%m%d %H:%M:%S'
DATE_FMT_Ymd_IMS = '%Y%m%d %I:%M:%S'
DATE_FMT_ymd_HMS = '%y%m%d %H:%M:%S'
DATE_FMT_ymd_IMS = '%y%m%d %I:%M:%S'
DAY_BEGIN = '00:00:00'
DAY_BEGIN12 = '00:00:00 am'
DAY_END = '23:59:59'
DAY_END12 = '23:59:59'

ZERO_DATETIME = datetime(1970, 1, 1)
DATE_20190101 = datetime(2019, 1, 1)
DATE_20210201 = datetime(2021, 2, 2)

date_str_switch = {
    DATE_FMT: lambda year, month, day: '%s-%s-%s' % (year, month, day),
    DATE_FMT_Ymd: lambda year, month, day: '%s%s%s' % (year, month, day)
}


def from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)


def now():
    return datetime.now()


def now_timestamp():
    return now().timestamp()

def now_str(fmt=DATE_FMT_HMS):
    return time.strftime(fmt)


def cur_day_str(fmt=DATE_FMT):
    return time.strftime(fmt)


def day_begin(day):
    return datetime(day.year, day.month, day.day)


def day_end(day):
    return datetime(day.year, day.month, day.day, hour=23, minute=59, second=59)


def cur_day_begin_str():
    return '%s %s' % (cur_day_str(), DAY_BEGIN)


def cur_day_end_str():
    return '%s %s' % (cur_day_str(), DAY_END)


def day_str(day: datetime, fmt=DATE_FMT, hms=False):
    return '%s%s' % (date_str_switch[fmt](day.year, day.month, day.day),
                     ' %s' % DAY_END if hms else '')


def cur_day_begin():
    n = now()
    return n - timedelta(hours=n.hour, minutes=n.minute, seconds=n.second, microseconds=n.microsecond)


def cur_day_end():
    return cur_day_begin() + timedelta(hours=HOURS, minutes=MINUTES, seconds=SECONDS)


def yesterday_begin():
    n = now()
    return n - timedelta(days=1, hours=n.hour, minutes=n.minute, seconds=n.second, microseconds=n.microsecond)


def yesterday_str(fmt=DATE_FMT):
    return day_str(yesterday_begin(), fmt=fmt)


def yesterday_end():
    return cur_day_begin() + timedelta(hours=HOURS, minutes=MINUTES, seconds=SECONDS)


def add_days(day, days):
    return day + timedelta(days)


def add_months(day, months, p_day=0):
    month = (day.month + months) % MONTHS
    year = day.year + (day.month + months - 1) // MONTHS
    month = month if month else MONTHS
    return datetime(year, month,
                    p_day if p_day else min(day.day,  calendar.monthrange(year, month)[1]))


def month_first(day, days=1):
    return datetime(day.year, day.month, days)


def month_first_str(day, fmt=DATE_FMT, hms=False):
    return '%s%s' % (date_str_switch[fmt](day.year, day.month, 1),
                     ' %s' % DAY_BEGIN if hms else '')


def month_last_str(day, fmt=DATE_FMT, hms=False):
    return '%s%s' % (date_str_switch[fmt](day.year, day.month, month_days(day)[1]),
                     ' %s' % DAY_END if hms else '')


def month_last(day):
    return month_first(day) + timedelta(month_days(day)[1] - 1, hours=23, minutes=59, seconds=59)


def month_days(day):
    return calendar.monthrange(day.year, day.month)[1]


def str_to_date(st, fmt=DATE_FMT):
    return datetime.strptime(st, fmt)


def is_number(val):
    if type(val) in [int, float]:
        return True
    if type(val) == str:
        try:
            float(val)
            return True
        except ValueError:
            return False
    return False


def convert_val_to_datetime(val, fmt=DATE_FMT_HMS):
    if not fmt:
        fmt = DATE_FMT_HMS
    if type(val) == datetime:
        return val
    elif type(val) == int or is_number(val):
        return datetime.fromtimestamp(val) if val >= 86400 else datetime(1970, 1, 1)
    elif type(val) == date:
        return datetime(val.year, val.month, val.day)
    elif type(val) == str:
        return datetime.strptime(val, fmt)
    else:
        return None
