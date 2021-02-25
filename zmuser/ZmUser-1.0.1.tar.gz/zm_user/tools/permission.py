from functools import wraps

from flask import g

from zm_user.tools.jsonify import jsonify_fail


def permission_check_login():
    """
    判断是不是超级管理员
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.user is None:
                return jsonify_fail(code=-10000, msg="请先登录")
            return func(*args, **kwargs)

        return inner

    return wrapper


def permission_check_root():
    """
    判断是不是超级管理员
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.user is None:
                return jsonify_fail(code=-10000, msg="请先登录")
            if not g.user.is_root():
                return jsonify_fail(msg="无操作权限")
            return func(*args, **kwargs)

        return inner

    return wrapper

