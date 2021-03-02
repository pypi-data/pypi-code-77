# -*- coding: utf-8 -*-
import json
from base64 import b64decode
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .settings import *


class FoolishAuthentication(TokenAuthentication):
    """
    只是简单的认可请求头中携带的用户信息，然后创建一个不保存的零时用户。
    此APP只能用于带有认证功能的API网关背后，用于简化系统内部的用户认证。
    """

    keyword = 'Foolish'

    def authenticate_credentials(self, key):
        user_model = get_user_model()

        if FOOLISH_AUTH_USER_SAVED:
            try:
                user = user_model.object.get(username=key)
            except ObjectDoesNotExist:
                if FOOLISH_AUTH_CREATE_USER:
                    user = user_model.object.create(username=key)
                else:
                    raise AuthenticationFailed(_('User inactive or deleted.'))
        else:
            user = user_model(username=key)

        return user, key


class FoolishPayloadAuthentication(TokenAuthentication):
    keyword = 'FoolishPayload'

    @staticmethod
    def set_user_attr(user, payload: dict):
        for k, v in payload.items():
            if hasattr(user, k):
                setattr(user, k, v)

    def authenticate_credentials(self, key):
        user_model = get_user_model()

        mod = len(key) % 4
        if mod != 0:
            key += '=' * (4 - mod)

        payload = json.loads(b64decode(key))
        username = payload.get('username')

        if FOOLISH_AUTH_USER_SAVED:
            try:
                user = user_model.objects.get(username=username)
            except ObjectDoesNotExist:
                if FOOLISH_AUTH_CREATE_USER:
                    user = user_model.objects.create(username=username)
                    self.set_user_attr(user, payload)
                    user.save()
                else:
                    raise AuthenticationFailed(_('User inactive or deleted.'))
        else:
            user = user_model(username)
            self.set_user_attr(user, payload)

        return user, key
