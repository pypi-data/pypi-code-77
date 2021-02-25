# -*- coding: utf-8 -*-

import sys

from fast_tracker.api.wsgi_application import WSGIApplicationWrapper
from fast_tracker.common.object_wrapper import wrap_out_function
from fast_tracker.common.coroutine import (is_coroutine_function,
                                           is_asyncio_coroutine)


def is_coroutine(fn):
    return is_coroutine_function(fn) or is_asyncio_coroutine(fn)


def _nr_wrapper_Application_wsgi_(application):

    try:
        if 'tornado.web' in sys.modules:
            import tornado.web
            if isinstance(application, tornado.web.Application):
                return application
    except ImportError:
        pass

    if is_coroutine(application):
        return application
    elif (hasattr(application, '__call__') and
          is_coroutine(application.__call__)):
        return application
    else:
        return WSGIApplicationWrapper(application)


def instrument_gunicorn_app_base(module):
    wrap_out_function(module, 'Application.wsgi',
                      _nr_wrapper_Application_wsgi_)
