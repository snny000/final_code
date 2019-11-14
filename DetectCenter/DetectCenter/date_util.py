# -*- coding: utf-8 -*-
import threading
import time, datetime

timeLock = threading.RLock()


def get_current_time():
    """
    获取指定格式的当前时间.
    时间格式：yyyy-MM-dd HH:mm:ss
    """
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with timeLock:
        return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')


'''
功能：
	获得相应格式的当前时间的字符串
参数：
	time_format：时间格式
返回值：
	strtime：当前时间的字符串
'''
def get_current_date_string(time_format="%Y-%m-%d %H:%M:%S"):
    strtime = time.strftime(time_format, time.localtime(time.time()))
    return strtime


def get_last_days(num):
    """
    获得最近num天（包括当前日期）的日期字符串列表.
    """
    str_now = time.strftime('%Y-%m-%d', time.localtime())
    now_date = datetime.datetime.strptime(str_now, '%Y-%m-%d')
    date_list = []
    for day in range(num - 1, -1, -1):
        date = now_date - datetime.timedelta(days=day)
        date_list.append(date.strftime("%Y-%m-%d"))
    return date_list


# print get_last_days(3)