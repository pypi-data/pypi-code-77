import logging
import sys
import time
from functools import wraps

from flask import session

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def auth_required(func, identity_key: str):
    """检查是否登录

    :param func:
    :param identity_key: 登录信息在session中的标识
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if identity_key in session:
            return func(*args, **kwargs)
        else:
            return 'You are NOT logged in!'

    return wrapper


def log_time(func):
    """记录处理时间

    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        # logger.debug('run %s use: %s ms', func.__name__, int(round(time.perf_counter() - start, 3) * 1000))
        logger.debug('run %s use: %s s', func.__name__, time.perf_counter() - start)
        return ret

    return wrapper
