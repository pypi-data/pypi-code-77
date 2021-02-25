# -*- coding: utf-8 -*-


import functools

from fast_tracker.packages import six

from fast_tracker.api.external_trace import ExternalTrace
from fast_tracker.api.transaction import current_transaction
from fast_tracker.common.object_wrapper import ObjectWrapper
from fast_tracker.common.span_enum import SpanLayerAtrr, SpanType


def httplib_endheaders_wrapper(wrapped, instance, args, kwargs,
                               scheme, library):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    def _connect_unbound(instance, *args, **kwargs):
        return instance

    if instance is None:
        instance = _connect_unbound(*args, **kwargs)

    connection = instance

    if hasattr(connection, '_nr_library_info'):
        library, scheme = connection._nr_library_info

    url = '%s://%s:%s' % (scheme, connection.host, connection.port)
    try:
        skip_headers = getattr(connection, '_nr_skip_headers', False)

        with ExternalTrace(library=library, url=url, span_type=SpanType.Exit.value, 
                           span_layer=SpanLayerAtrr.HTTP.value) as tracer:
            if not skip_headers and hasattr(tracer, 'generate_request_headers'):
                outgoing_headers = tracer.generate_request_headers(transaction)
                for header_name, header_value in outgoing_headers:
                    connection.putheader(header_name, header_value)

            connection._nr_external_tracer = tracer

            return wrapped(*args, **kwargs)

    finally:
        try:
            del connection._nr_skip_headers
        except AttributeError:
            pass


def httplib_getresponse_wrapper(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    connection = instance
    tracer = getattr(connection, '_nr_external_tracer', None)

    if not tracer:
        return wrapped(*args, **kwargs)

    response = wrapped(*args, **kwargs)

    del connection._nr_external_tracer

    if hasattr(tracer, 'process_response_headers'):
        tracer.process_response_headers(response.getheaders())
    tracer._add_agent_attribute('status_code', str(response.status))
    tracer._add_agent_attribute('http_method', response._method)
    return response


def httplib_putheader_wrapper(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None:
        return wrapped(*args, **kwargs)

    def nr_header(header, *args, **kwargs):
        return header.upper() in ('fast_tracker',
                                  'X-fast_tracker-ID', 'X-fast_tracker-TRANSACTION')

    connection = instance

    if nr_header(*args, **kwargs):
        connection._nr_skip_headers = True

    return wrapped(*args, **kwargs)


def instrument(module):
    if six.PY2:
        library = 'httplib'
    else:
        library = 'http'

    module.HTTPConnection.endheaders = ObjectWrapper(
        module.HTTPConnection.endheaders,
        None,
        functools.partial(httplib_endheaders_wrapper, scheme='http',
                          library=library))

    module.HTTPSConnection.endheaders = ObjectWrapper(
        module.HTTPConnection.endheaders,
        None,
        functools.partial(httplib_endheaders_wrapper, scheme='https',
                          library=library))

    module.HTTPConnection.getresponse = ObjectWrapper(
        module.HTTPConnection.getresponse,
        None,
        httplib_getresponse_wrapper)

    module.HTTPConnection.putheader = ObjectWrapper(
        module.HTTPConnection.putheader,
        None,
        httplib_putheader_wrapper)
