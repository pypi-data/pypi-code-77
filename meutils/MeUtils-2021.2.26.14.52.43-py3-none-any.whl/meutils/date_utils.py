#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : date_utils
# @Time         : 2020/11/12 11:41 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.common import *

"""
pd.to_datetime(time.time(), unit='s')
>>> f'{now:%Y-%m-%d %H:%M:%S}'

"""


def date_difference(format='%Y-%m-%d %H:%M:%S', start_time=datetime.datetime.now(), **kwargs) -> str:
    """
    start_time: datetime.datetime.today()
    days: float = ...,
    seconds: float = ...,
    microseconds: float = ...,
    milliseconds: float = ...,
    minutes: float = ...,
    hours: float = ...,
    weeks
    """
    if isinstance(start_time, str):
        start_time = datetime.datetime.strptime(start_time, format)
    date = start_time - datetime.timedelta(**kwargs)
    return date.strftime(format)



if __name__ == '__main__':
    print(date_difference(days=1))
    print(datetime.datetime.strptime('20210222', '%Y%m%d'))
    print(type(datetime.datetime.strptime('20210222', '%Y%m%d')))
