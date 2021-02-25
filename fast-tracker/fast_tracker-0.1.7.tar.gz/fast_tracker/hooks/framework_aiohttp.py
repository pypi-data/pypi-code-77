# -*- coding: utf-8 -*-

import itertools
import asyncio
import inspect

from fast_tracker.api.external_trace import ExternalTrace
from fast_tracker.api.function_trace import function_trace
from fast_tracker.api.transaction import current_transaction, ignore_transaction
from fast_tracker.api.web_transaction import web_transaction
from fast_tracker.common.async_wrapper import is_coroutine_function, async_wrapper
from fast_tracker.common.object_names import callable_name
from fast_tracker.common.object_wrapper import (wrap_function_wrapper,
                                                function_wrapper, ObjectProxy)
from fast_tracker.common.span_enum import SpanType, SpanLayerAtrr
from fast_tracker.core.config import ignore_status_code

SUPPORTED_METHODS = ('connect', 'head', 'get', 'delete', 'options', 'patch',
                     'post', 'put', 'trace')


def aiohttp_version_info():
    import aiohttp
    return tuple(int(_) for _ in aiohttp.__version__.split('.')[:2])


def headers_preserve_casing():
    try:
        from multidict import CIMultiDict
    except:
        return True

    d = CIMultiDict()
    d.update({'X-fast_tracker-ID': 'value'})
    return 'X-fast_tracker-ID' in dict(d.items())


def should_ignore(exc, value, tb):
    from aiohttp import web

    if isinstance(value, web.HTTPException):
        status_code = value.status_code
        return ignore_status_code(status_code)


def _nr_process_response_proxy(response, transaction):
    nr_headers = transaction.process_response(response.status,
                                              response.headers)

    response._headers = HeaderProxy(response.headers, nr_headers)


def _nr_process_response(response, transaction):
    nr_headers = transaction.process_response(response.status,
                                              response.headers)

    response._headers.update(nr_headers)


@function_wrapper
def _nr_aiohttp_view_wrapper_(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if not transaction:
        return wrapped(*args, **kwargs)

    name = callable_name(wrapped)
    transaction.set_transaction_name(name, priority=1)

    return function_trace(name=name)(wrapped)(*args, **kwargs)


@function_wrapper
def _nr_aiohttp_initial_class_transaction_name_(
        wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if not transaction:
        return wrapped(*args, **kwargs)

    name = callable_name(instance)
    transaction.set_transaction_name(name, priority=1)
    return wrapped(*args, **kwargs)


def _nr_aiohttp_wrap_view_(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)
    from aiohttp.web import View
    if inspect.isclass(instance._handler):
        try:
            init = getattr(instance._handler, '__init__')
        except AttributeError:
            def init(*args, **kwargs):
                pass

        if not hasattr(init, '__wrapped__'):
            instance._handler.__init__ = \
                _nr_aiohttp_initial_class_transaction_name_(init)

        if issubclass(instance._handler, View):
            for method in SUPPORTED_METHODS:
                handler = getattr(instance._handler, method, None)

                if handler and not hasattr(handler, '__wrapped__'):
                    setattr(instance._handler, method,
                            _nr_aiohttp_view_wrapper_(handler))
    else:
        instance._handler = _nr_aiohttp_view_wrapper_(instance._handler)
    return result


def _nr_aiohttp_wrap_wsgi_response_(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)

    class ResponseProxy:
        def __getattr__(self, name):
            if instance.response is self:
                raise AttributeError("%r object has no attribute %r" % (
                    type(instance).__name__, 'response'))
            return getattr(instance.response, name)

    instance.response = ResponseProxy()

    return result


def _nr_aiohttp_response_prepare_(wrapped, instance, args, kwargs):
    def _bind_params(request):
        return request

    request = _bind_params(*args, **kwargs)

    nr_headers = getattr(request, '_nr_headers', None)
    if nr_headers:
        nr_headers.update(instance.headers)
        instance._headers = nr_headers

    return wrapped(*args, **kwargs)


@function_wrapper
def _nr_aiohttp_wrap_middleware_(wrapped, instance, args, kwargs):
    @asyncio.coroutine
    def _inner():
        result = yield from wrapped(*args, **kwargs)
        return function_trace()(result)

    return _inner()


def _nr_aiohttp_wrap_application_init_(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)

    if hasattr(instance, '_middlewares'):
        for index, middleware in enumerate(instance._middlewares):
            if getattr(middleware, '__middleware_version__', None) == 1:
                traced_middleware = function_trace()(middleware)
            else:
                traced_middleware = _nr_aiohttp_wrap_middleware_(middleware)
            instance._middlewares[index] = traced_middleware

    return result


def _nr_aiohttp_wrap_system_route_(wrapped, instance, args, kwargs):
    ignore_transaction()
    return wrapped(*args, **kwargs)


class HeaderProxy(ObjectProxy):
    def __init__(self, wrapped, nr_headers):
        super(HeaderProxy, self).__init__(wrapped)
        self._nr_headers = nr_headers

    def items(self):
        nr_headers = dict(self._nr_headers)
        for key, _ in self._nr_headers:
            if key in self:
                nr_headers.pop(key)

        return itertools.chain(
            self.__wrapped__.items(), nr_headers.items())


def _nr_aiohttp_add_cat_headers_(wrapped, instance, args, kwargs):
    transaction = current_transaction()
    if transaction is None:
        return wrapped(*args, **kwargs)

    try:
        cat_headers = ExternalTrace.generate_request_headers(transaction)
    except:
        return wrapped(*args, **kwargs)

    tmp = instance.headers
    instance.headers = HeaderProxy(tmp, cat_headers)

    if is_coroutine_function(wrapped):
        @asyncio.coroutine
        def new_coro():
            try:
                result = yield from wrapped(*args, **kwargs)
                return result
            finally:
                instance.headers = tmp

        return new_coro()
    else:
        try:
            return wrapped(*args, **kwargs)
        finally:
            instance.headers = tmp


def _nr_aiohttp_add_cat_headers_simple_(wrapped, instance, args, kwargs):
    transaction = current_transaction()
    if transaction is None:
        return wrapped(*args, **kwargs)

    try:
        cat_headers = ExternalTrace.generate_request_headers(transaction)
    except:
        return wrapped(*args, **kwargs)

    for k, _ in cat_headers:
        if k in instance.headers:
            return wrapped(*args, **kwargs)

    instance.headers.update(cat_headers)
    return wrapped(*args, **kwargs)


def _bind_request(method, url, *args, **kwargs):
    return method, url


def _nr_aiohttp_request_wrapper_(wrapped, instance, args, kwargs):
    transaction = current_transaction()
    if transaction is None:
        return wrapped(*args, **kwargs)

    method, url = _bind_request(*args, **kwargs)
    trace = ExternalTrace('aiohttp', url, method, span_type=SpanType.Exit.value, span_layer=SpanLayerAtrr.HTTP.value)

    @asyncio.coroutine
    def _coro():
        try:
            response = yield from wrapped(*args, **kwargs)

            try:
                trace.process_response_headers(response.headers.items())
            except:
                pass

            return response
        except Exception as e:
            try:
                trace.process_response_headers(e.headers.items())
            except:
                pass

            raise

    return async_wrapper(wrapped)(_coro, trace)()


def instrument_aiohttp_client(module):
    wrap_function_wrapper(module, 'ClientSession._request',
                          _nr_aiohttp_request_wrapper_)


def instrument_aiohttp_client_reqrep(module):
    version_info = aiohttp_version_info()

    if version_info >= (2, 0):
        if headers_preserve_casing():
            cat_wrapper = _nr_aiohttp_add_cat_headers_simple_
        else:
            cat_wrapper = _nr_aiohttp_add_cat_headers_

        wrap_function_wrapper(module, 'ClientRequest.send', cat_wrapper)


def instrument_aiohttp_protocol(module):
    wrap_function_wrapper(module, 'Request.send_headers',
                          _nr_aiohttp_add_cat_headers_)


def instrument_aiohttp_web_urldispatcher(module):
    if aiohttp_version_info() < (3, 5):
        system_route_handler = 'SystemRoute._handler'
    else:
        system_route_handler = 'SystemRoute._handle'

    wrap_function_wrapper(module, 'ResourceRoute.__init__',
                          _nr_aiohttp_wrap_view_)
    wrap_function_wrapper(module, system_route_handler,
                          _nr_aiohttp_wrap_system_route_)


def _bind_handle(request, *args, **kwargs):
    return request


def _nr_request_wrapper(wrapped, instance, args, kwargs):
    request = _bind_handle(*args, **kwargs)

    # Ignore websockets
    if request.headers.get('upgrade', '').lower() == 'websocket':
        return wrapped(*args, **kwargs)

    coro = wrapped(*args, **kwargs)

    if hasattr(coro, '__await__'):
        coro = coro.__await__()

    @asyncio.coroutine
    def _coro(*_args, **_kwargs):
        transaction = current_transaction()
        if transaction is None:
            response = yield from coro
            return response

        # Patch in should_ignore to all record_exception calls
        transaction._ignore_errors = should_ignore

        import aiohttp
        transaction.add_framework_info(
            name='aiohttp', version=aiohttp.__version__)

        import aiohttp.web as _web

        try:
            response = yield from coro
        except _web.HTTPException as e:
            _nr_process_response(e, transaction)
            raise
        except Exception:
            nr_headers = transaction.process_response(500, ())
            request._nr_headers = dict(nr_headers)
            raise

        _nr_process_response(response, transaction)
        return response

    _coro = web_transaction(
        request_method=request.method,
        request_path=request.path,
        query_string=request.query_string,
        headers=request.raw_headers)(_coro)

    return _coro(*args, **kwargs)


def instrument_aiohttp_web(module):
    global _nr_process_response
    if not headers_preserve_casing():
        _nr_process_response = _nr_process_response_proxy

    wrap_function_wrapper(module, 'Application._handle',
                          _nr_request_wrapper)
    wrap_function_wrapper(module, 'Application.__init__',
                          _nr_aiohttp_wrap_application_init_)


def instrument_aiohttp_wsgi(module):
    wrap_function_wrapper(module, 'WsgiResponse.__init__',
                          _nr_aiohttp_wrap_wsgi_response_)


def instrument_aiohttp_web_response(module):
    wrap_function_wrapper(module, 'Response.prepare',
                          _nr_aiohttp_response_prepare_)
