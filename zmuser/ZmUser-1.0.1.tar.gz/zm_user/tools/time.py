import datetime
import time


def datetime_to_str(dt, fmt='%Y-%m-%d %H:%M'):
    if dt:
        return dt.strftime(fmt)
    else:
        return ''


def datetime_to_int(dt, fmt='%Y-%m-%d %H:%M'):
    return time.strptime(dt.strftime(fmt), fmt)


def str_to_datetime(str, fmt='%Y-%m-%d %H:%M'):
    return datetime.datetime.strptime(str, fmt)


def time_have_unit(count: int, unit: str):
    # 时间带单位的处理,返回秒
    if unit == "周":
        return count * 7 * 24 * 60 * 60
    return count * 24 * 60 * 60


def int_to_day(i):
    # 秒数转成天数
    return int(i / 60 / 60 / 24)
    pass


def int_to_datetime(i):
    # 秒数转时间
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i))
    print(dt)
    return dt


def int_to_str(i):
    # 秒数转时间后再转换成字符串
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i))
    return datetime_to_str(dt, fmt='%Y-%m-%d %H:%M')
