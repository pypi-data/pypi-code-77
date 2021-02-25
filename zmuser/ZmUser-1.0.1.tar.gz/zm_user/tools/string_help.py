import re


def is_phone(phone):
    """
    该函数判断一个字符串是否为手机号
    :param phone: 手机号
    :return:
    """
    tel = str(phone)
    ret = re.match(r"^1\d{10}$", tel)
    if ret:
        return True
    else:
        return False


def is_email(email):
    """
    该函数判断一个字符串是否为邮箱
    :param email: 邮箱
    :return:
    """
    email = str(email)
    ret = re.match(r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$", email)
    if ret:
        return True
    else:
        return False


def is_none_str(s):
    """
    判断s是否为空
    :param s:
    :return:
    """
    if isinstance(s, str):
        s = s.strip()
    if isinstance(s, int):
        return False
    if isinstance(s, float):
        return False
    if not s:
        return True
    if len(s) > 0:
        return False
    if not s or len(str(s.strip())) < 1:
        return True
    return False


def str_to_int(s, default=0):
    if isinstance(s, int):
        return s
    try:
        return int(s)
    except Exception as e:
        return default


def str_to_bool(s, default=True):
    if isinstance(s, str):
        if str in ["false", "False"]:
            return False
        if str in ["true", "True"]:
            return False
    try:
        return bool(s)
    except Exception as e:
        return default
