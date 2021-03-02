# coding=utf-8

import time
import hashlib


class AuthUtil:

    def __init__(self):
        pass

    @staticmethod
    def get_auth_url(ak_str, sk_str):
        timestamp = (str(round(time.time() * 1000)))
        need_signature_str = sk_str + timestamp + ak_str
        return "access_key=" + ak_str + "&timestamp=" + timestamp + "&signature=" + AuthUtil.get_sign_str(
            need_signature_str)

    @staticmethod
    def get_sign_str(need_sign_str):
        m = hashlib.md5()
        m.update(need_sign_str.encode("utf8"))
        return m.hexdigest()
