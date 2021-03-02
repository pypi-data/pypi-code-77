# coding=utf-8

import time
import hashlib
import uuid


class AuthUtil:

    def __init__(self):
        pass

    @staticmethod
    def get_auth_url(ak_str, sk_str, params_dict):
        if not params_dict:
            params_dict = {}
        if 'sign_version' not in params_dict.keys():
            params_dict['sign_version'] = '2.0'
        if 'sign_nonce' not in params_dict.keys():
            params_dict['sign_nonce'] = str(uuid.uuid4()).replace('-', '')
        if 'sign_type' not in params_dict.keys():
            params_dict['sign_type'] = 'MD5'
        timestamp = (str(round(time.time() * 1000)))
        if 'timestamp' not in params_dict.keys():
            params_dict['timestamp'] = timestamp
        params_dict['access_key'] = ak_str
        sorted_params = AuthUtil.sort_params_str(params_dict)
        signature = AuthUtil.get_signature(ak_str, sk_str, sorted_params, str(round(time.time() * 1000)))
        url = AuthUtil.get_url_params(params_dict)
        return url + '&signature=' + signature

    @staticmethod
    def get_url_params(params_dict):
        if not params_dict:
            return ''
        url_params = ''
        for key, value in params_dict.items():
            url_params += key + '=' + value + '&'
        if url_params.endswith('&'):
            url_params = url_params[0:-1]
        return url_params

    @staticmethod
    def sort_params_str(params_dict):
        keys = sorted(params_dict.keys())
        sorted_params_str = ''
        for key in keys:
            sorted_params_str += key + '=' + params_dict[key] + '#'
        return sorted_params_str

    @staticmethod
    def get_signature(ak_str, sk_str, param_str, timestamp):
        if not ak_str or not sk_str or not param_str:
            raise Exception('参数缺失')
        need_sign_str = sk_str + '$' + timestamp + '$' + ak_str + '$' + param_str
        m = hashlib.md5()
        m.update(need_sign_str.encode("utf8"))
        return m.hexdigest()