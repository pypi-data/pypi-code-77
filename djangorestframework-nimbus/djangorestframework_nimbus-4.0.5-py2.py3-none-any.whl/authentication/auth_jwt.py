# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication as JWTAuthentication
from ..err_code import ErrCode, APIError


class JSONWebTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if not jwt_value:
            # raise AuthenticationFailed('Authorization 字段是必须的')
            raise APIError(ErrCode.ERR_AUTH_NOLOGIN, status_code=401)
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            # raise AuthenticationFailed('签名过期')
            raise APIError(ErrCode.ERR_AUTH_NOLOGIN, status_code=401)
        except jwt.DecodeError:
            # raise AuthenticationFailed('解码失败')
            raise APIError(ErrCode.ERR_AUTH_NOLOGIN, status_code=401)
        except jwt.InvalidTokenError:
            # raise AuthenticationFailed('非法用户')
            raise APIError(ErrCode.ERR_AUTH_NOLOGIN, status_code=401)
        user = self.authenticate_credentials(payload)
        return user, jwt_value

