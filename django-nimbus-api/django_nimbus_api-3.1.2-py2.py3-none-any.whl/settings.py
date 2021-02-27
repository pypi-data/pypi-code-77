# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""
Package Description
"""
import os
import sys
import logging
import json
from functools import wraps
from django.conf import settings


DEFAULTS = {
    'API_ALLOW_EMPTY': True,

    # 公钥私钥
    'API_PRIVATE_KEY': "",
    'API_SECRECT_KEY': "",

    # 错误捕捉
    'API_CATCH_EXCEPTION_ENABLED': True,
    'API_CATCH_EXCEPTION_HANDLER': None,

    # 分页参数
    'PAGE_QUERY_PARAM': 'page',
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,

    # 分页返回参数
    'API_PAGE_NAME_TOTAL_DATA': "total",
    'API_PAGE_NAME_TOTAL_PAGE': "pageCount",
    'API_PAGE_NAME_PAGE': "currentPage",
    'API_PAGE_NAME_PAGE_SIZE': "pageSize",
    'API_PAGE_NAME_DATA': "records",
}


class APISettings(object):
    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'API_CONFIG', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


api_settings = APISettings(DEFAULTS)
