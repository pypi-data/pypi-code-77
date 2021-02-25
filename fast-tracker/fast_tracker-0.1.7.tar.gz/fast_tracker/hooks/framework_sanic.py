# -*- coding: utf-8 -*-

import sys

from fast_tracker.api.web_transaction import web_transaction
from fast_tracker.api.transaction import current_transaction
from fast_tracker.api.function_trace import function_trace
from fast_tracker.api.time_trace import record_exception
from fast_tracker.common.object_wrapper import (wrap_function_wrapper,
                                                function_wrapper)
from fast_tracker.common.object_names import callable_name
from fast_tracker.core.config import ignore_status_code


def _bind_add(uri, methods, handler, *args, **kwargs):
    return uri, methods, handler, args, kwargs


@function_wrapper
def _nr_wrapper_handler_(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    name = callable_name(wrapped)
    view_class = getattr(wrapped, 'view_class', None)
    if view_class:
        try:
            method = args[0].method.lower()
            name = callable_name(view_class) + '.' + method
        except:
            pass
    transaction.set_transaction_name(name, priority=3)
    import sanic
    transaction.add_framework_info(name='Sanic', version=sanic.__version__)
    return function_trace(name=name)(wrapped)(*args, **kwargs)


@function_wrapper
def _nr_sanic_router_add(wrapped, instance, args, kwargs):
    uri, methods, handler, args, kwargs = _bind_add(*args, **kwargs)

    callable_name(handler)
    if hasattr(wrapped, 'view_class'):
        callable_name(wrapped.view_class)
    wrapped_handler = _nr_wrapper_handler_(handler)

    return wrapped(uri, methods, wrapped_handler, *args, **kwargs)


@function_wrapper
def _nr_sanic_router_get(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception:
        transaction = current_transaction()
        if transaction:
            name = callable_name(wrapped)
            transaction.set_transaction_name(name, priority=2)
        raise


@function_wrapper
def _nr_wrapper_error_handler_(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if not transaction:
        return wrapped(*args, **kwargs)

    name = callable_name(wrapped)
    transaction.set_transaction_name(name, priority=1)
    try:
        response = function_trace(name=name)(wrapped)(*args, **kwargs)
    except:
        record_exception()
        raise

    return response


def _bind_error_add(exception, handler, *args, **kwargs):
    return exception, handler


@function_wrapper
def _nr_sanic_error_handlers(wrapped, instance, args, kwargs):
    exception, handler = _bind_error_add(*args, **kwargs)

    callable_name(handler)
    wrapped_handler = _nr_wrapper_error_handler_(handler)

    return wrapped(exception, wrapped_handler)


@function_wrapper
def error_response(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    exc_info = sys.exc_info()
    try:
        response = wrapped(*args, **kwargs)
    except:
        record_exception(*exc_info)

        record_exception()
        raise
    else:
        if hasattr(response, 'status'):
            if not ignore_status_code(response.status):
                record_exception(*exc_info)
        else:
            record_exception(*exc_info)
    finally:
        exc_info = None

    return response


def _sanic_app_init(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)

    error_handler = getattr(instance, 'error_handler')
    if hasattr(error_handler, 'response'):
        instance.error_handler.response = error_response(
            error_handler.response)
    if hasattr(error_handler, 'add'):
        error_handler.add = _nr_sanic_error_handlers(
            error_handler.add)

    router = getattr(instance, 'router')
    if hasattr(router, 'add'):
        router.add = _nr_sanic_router_add(router.add)
    if hasattr(router, 'get'):
        callable_name(router.get)
        router.get = _nr_sanic_router_get(router.get)

    return result


def _nr_sanic_response_parse_headers(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    cat_headers = transaction.process_response(str(instance.status),
                                               instance.headers.items())

    for header_name, header_value in cat_headers:
        if header_name not in instance.headers:
            instance.headers[header_name] = header_value

    return wrapped(*args, **kwargs)


def _nr_wrapper_middleware_(attach_to):
    is_request_middleware = attach_to == 'request'

    @function_wrapper
    def _wrapper(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        name = callable_name(wrapped)
        if is_request_middleware:
            transaction.set_transaction_name(name, priority=2)
        response = function_trace(name=name)(wrapped)(*args, **kwargs)

        return response

    return _wrapper


def _bind_middleware(middleware, attach_to='request', *args, **kwargs):
    return middleware, attach_to


def _nr_sanic_register_middleware_(wrapped, instance, args, kwargs):
    middleware, attach_to = _bind_middleware(*args, **kwargs)

    callable_name(middleware)
    wrapped_middleware = _nr_wrapper_middleware_(attach_to)(middleware)
    wrapped(wrapped_middleware, attach_to)
    return middleware


def _bind_request(request, *args, **kwargs):
    return request


def _nr_sanic_transaction_wrapper_(wrapped, instance, args, kwargs):
    request = _bind_request(*args, **kwargs)
    if request.headers.get('upgrade', '').lower() == 'websocket':
        return wrapped(*args, **kwargs)

    return web_transaction(
        request_method=request.method,
        request_path=request.path,
        query_string=request.query_string,
        headers=request.headers)(wrapped)(*args, **kwargs)


def instrument_sanic_app(module):
    wrap_function_wrapper(module, 'Sanic.handle_request',
                          _nr_sanic_transaction_wrapper_)
    wrap_function_wrapper(module, 'Sanic.__init__',
                          _sanic_app_init)
    wrap_function_wrapper(module, 'Sanic.register_middleware',
                          _nr_sanic_register_middleware_)


def instrument_sanic_response(module):
    wrap_function_wrapper(module, 'BaseHTTPResponse._parse_headers',
                          _nr_sanic_response_parse_headers)
