#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" __calendar_utils__ """

__author__ = 'zhangjiawen'

from datetime import datetime
from calendar import monthcalendar


def month_work_days(day: datetime, weekends=(5, 6), holidays: list = None, workdays: list = None):
    year, month = day.year, day.month
    work_days, rest_days = [], []
    week_day_lists = monthcalendar(year, month)
    for week_days in week_day_lists:
        weekend_days = []
        for wd in weekends:
            weekend_days.append(week_days[wd])
        for d in week_days:
            if d == 0:
                continue
            if holidays and d in holidays or (
                    d in weekend_days and (not workdays or workdays and d not in workdays)):
                rest_days.append(d)
            else:
                work_days.append(d)
    return work_days, rest_days


def month_nrd_work_day(day: datetime, nrd: int, weekends=(5, 6),
                       holidays: list = None, workdays: list = None, is_full=False) -> datetime:
    year, month = day.year, day.month
    if is_full:
        return datetime(year, month, workdays[nrd]) if workdays and len(workdays) >= nrd else None
    else:
        week_day_lists = monthcalendar(year, month)
        index, has_found, found_day = 0, False, 0
        for week_days in week_day_lists:
            weekend_days = []
            for wd in weekends:
                weekend_days.append(week_days[wd])
            for d in week_days:
                if d == 0:
                    continue
                if holidays and d in holidays or (
                        d in weekend_days and (not workdays or workdays and d not in workdays)):
                    continue
                index += 1
                if index == nrd:
                    has_found, found_day = True, d
                    break
            if has_found:
                break
        return datetime(year, month, found_day) if found_day else None
