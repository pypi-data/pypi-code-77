# -*- coding: utf-8 -*-

import functools
import sys

from fast_tracker.api.application import Application, application_instance
from fast_tracker.core.attribute import create_agent_attributes
from fast_tracker.api.background_task import BackgroundTask
from fast_tracker.api.message_trace import MessageTrace
from fast_tracker.api.transaction import current_transaction
from fast_tracker.common.object_wrapper import FunctionWrapper, wrap_object
from fast_tracker.common.async_proxy import async_proxy, TransactionContext


class MessageTransaction(BackgroundTask):

    def __init__(self, library, destination_type,
                 destination_name, application, routing_key=None,
                 exchange_type=None, headers=None, queue_name=None, reply_to=None,
                 correlation_id=None):

        name, group = self.get_transaction_name(library, destination_type,
                                                destination_name)

        super(MessageTransaction, self).__init__(application, name,
                                                 group=group)

        cat_id, cat_transaction = None, None

        self.headers = headers

        if self.settings is not None:
            if self.settings.distributed_tracing.enabled:
                self.accept_distributed_trace_headers(
                    self.headers, transport_type='AMQP')
            elif self.settings.cross_application_tracer.enabled:
                self._process_incoming_cat_headers(cat_id, cat_transaction)

        self.routing_key = routing_key
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        self.reply_to = reply_to
        self.correlation_id = correlation_id

    @staticmethod
    def get_transaction_name(library, destination_type, destination_name):
        group = 'Message/%s/%s' % (library, destination_type)
        name = 'Named/%s' % destination_name
        return name, group

    @property
    def agent_attributes(self):
        ms_attrs = {}

        if self.exchange_type is not None:
            ms_attrs['message.exchangeType'] = self.exchange_type
        if self.queue_name is not None:
            ms_attrs['message.queueName'] = self.queue_name
        if self.reply_to is not None:
            ms_attrs['message.replyTo'] = self.reply_to
        if self.correlation_id is not None:
            ms_attrs['message.correlationId'] = self.correlation_id
        if self.headers:
            for k, v in self.headers.items():
                new_key = 'message.headers.%s' % k
                new_val = str(v)
                ms_attrs[new_key] = new_val
        if self.routing_key is not None:
            ms_attrs['message.routingKey'] = self.routing_key

        messagebroker_attributes = create_agent_attributes(ms_attrs,
                                                           self.attribute_filter)

        attributes = super(MessageTransaction, self).agent_attributes
        attributes.extend(messagebroker_attributes)

        return attributes


def MessageTransactionWrapper(wrapped, library, destination_type,
                              destination_name, application=None, routing_key=None,
                              exchange_type=None, headers=None, queue_name=None, reply_to=None,
                              correlation_id=None):
    def wrapper(wrapped, instance, args, kwargs):
        if callable(library):
            if instance is not None:
                _library = library(instance, *args, **kwargs)
            else:
                _library = library(*args, **kwargs)
        else:
            _library = library

        if callable(destination_type):
            if instance is not None:
                _destination_type = destination_type(instance, *args, **kwargs)
            else:
                _destination_type = destination_type(*args, **kwargs)
        else:
            _destination_type = destination_type

        if callable(destination_name):
            if instance is not None:
                _destination_name = destination_name(instance, *args, **kwargs)
            else:
                _destination_name = destination_name(*args, **kwargs)
        else:
            _destination_name = destination_name

        if callable(routing_key):
            if instance is not None:
                _routing_key = routing_key(instance, *args, **kwargs)
            else:
                _routing_key = routing_key(*args, **kwargs)
        else:
            _routing_key = routing_key

        if callable(exchange_type):
            if instance is not None:
                _exchange_type = exchange_type(instance, *args, **kwargs)
            else:
                _exchange_type = exchange_type(*args, **kwargs)
        else:
            _exchange_type = exchange_type

        if callable(headers):
            if instance is not None:
                _headers = headers(instance, *args, **kwargs)
            else:
                _headers = headers(*args, **kwargs)
        else:
            _headers = headers

        if callable(queue_name):
            if instance is not None:
                _queue_name = queue_name(instance, *args, **kwargs)
            else:
                _queue_name = queue_name(*args, **kwargs)
        else:
            _queue_name = queue_name

        if callable(reply_to):
            if instance is not None:
                _reply_to = reply_to(instance, *args, **kwargs)
            else:
                _reply_to = reply_to(*args, **kwargs)
        else:
            _reply_to = reply_to

        if callable(correlation_id):
            if instance is not None:
                _correlation_id = correlation_id(instance, *args, **kwargs)
            else:
                _correlation_id = correlation_id(*args, **kwargs)
        else:
            _correlation_id = correlation_id

        transaction = current_transaction(active_only=False)

        if transaction:

            if transaction.ignore_transaction or transaction.stopped:
                return wrapped(*args, **kwargs)

            if not transaction.background_task:
                transaction.background_task = True
                transaction.set_transaction_name(
                    *MessageTransaction.get_transaction_name(
                        _library, _destination_type,
                        _destination_name))

            return wrapped(*args, **kwargs)

        if type(application) != Application:
            _application = application_instance(application)
        else:
            _application = application

        manager = MessageTransaction(
            library=_library,
            destination_type=_destination_type,
            destination_name=_destination_name,
            application=_application,
            routing_key=_routing_key,
            exchange_type=_exchange_type,
            headers=_headers,
            queue_name=_queue_name,
            reply_to=_reply_to,
            correlation_id=_correlation_id)

        proxy = async_proxy(wrapped)
        if proxy:
            context_manager = TransactionContext(manager)
            return proxy(wrapped(*args, **kwargs), context_manager)

        success = True

        try:
            manager.__enter__()
            try:
                return wrapped(*args, **kwargs)
            except:  # Catch all
                success = False
                if not manager.__exit__(*sys.exc_info()):
                    raise
        finally:
            if success and manager._ref_count == 0:
                manager._is_finalized = True
                manager.__exit__(None, None, None)
            else:
                manager._request_handler_finalize = True
                manager._server_adapter_finalize = True

                old_transaction = current_transaction()
                if old_transaction is not None:
                    old_transaction.drop_transaction()

    return FunctionWrapper(wrapped, wrapper)


def message_transaction(library, destination_type, destination_name,
                        application=None, routing_key=None, exchange_type=None, headers=None,
                        queue_name=None, reply_to=None, correlation_id=None):
    return functools.partial(MessageTransactionWrapper,
                             library=library, destination_type=destination_type,
                             destination_name=destination_name, application=application,
                             routing_key=routing_key, exchange_type=exchange_type,
                             headers=headers, queue_name=queue_name, reply_to=reply_to,
                             correlation_id=correlation_id)


def wrap_message_transaction(module, object_path, library, destination_type,
                             destination_name, application=None, routing_key=None,
                             exchange_type=None, headers=None, queue_name=None, reply_to=None,
                             correlation_id=None):
    wrap_object(module, object_path, MessageTransactionWrapper,
                (library, destination_type, destination_name, application,
                 routing_key, exchange_type, headers, queue_name, reply_to,
                 correlation_id))
