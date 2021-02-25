# -*- coding: utf-8 -*-

import re

from fast_tracker.api.datastore_trace import DatastoreTrace
from fast_tracker.api.transaction import current_transaction
from fast_tracker.common.object_wrapper import wrap_function_wrapper
from fast_tracker.common.span_enum import SpanLayerAtrr, SpanType

_redis_client_methods = ('bgrewriteaof', 'bgsave', 'client_kill',
                         'client_list', 'client_getname', 'client_setname', 'config_get',
                         'config_set', 'config_resetstat', 'config_rewrite', 'dbsize',
                         'debug_object', 'echo', 'flushall', 'flushdb', 'info', 'lastsave',
                         'object', 'ping', 'save', 'sentinel', 'sentinel_get_master_addr_by_name',
                         'sentinel_master', 'sentinel_masters', 'sentinel_monitor',
                         'sentinel_remove', 'sentinel_sentinels', 'sentinel_set',
                         'sentinel_slaves', 'shutdown', 'slaveof', 'slowlog_get',
                         'slowlog_reset', 'time', 'append', 'bitcount', 'bitop', 'bitpos',
                         'decr', 'delete', 'dump', 'exists', 'expire', 'expireat', 'get',
                         'getbit', 'getrange', 'getset', 'incr', 'incrby', 'incrbyfloat',
                         'keys', 'mget', 'mset', 'msetnx', 'move', 'persist', 'pexpire',
                         'pexpireat', 'psetex', 'pttl', 'randomkey', 'rename', 'renamenx',
                         'restore', 'set', 'setbit', 'setex', 'setnx', 'setrange', 'strlen',
                         'substr', 'ttl', 'type', 'watch', 'unwatch', 'blpop', 'brpop',
                         'brpoplpush', 'lindex', 'linsert', 'llen', 'lpop', 'lpush',
                         'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'rpop', 'rpoplpush',
                         'rpush', 'rpushx', 'sort', 'scan', 'scan_iter', 'sscan',
                         'sscan_iter', 'hscan', 'hscan_inter', 'zscan', 'zscan_iter', 'sadd',
                         'scard', 'sdiff', 'sdiffstore', 'sinter', 'sinterstore',
                         'sismember', 'smembers', 'smove', 'spop', 'srandmember', 'srem',
                         'sunion', 'sunionstore', 'zadd', 'zcard', 'zcount', 'zincrby',
                         'zinterstore', 'zlexcount', 'zrange', 'zrangebylex',
                         'zrangebyscore', 'zrank', 'zrem', 'zremrangebylex',
                         'zremrangebyrank', 'zremrangebyscore', 'zrevrange',
                         'zrevrangebyscore', 'zrevrank', 'zscore', 'zunionstore', 'pfadd',
                         'pfcount', 'pfmerge', 'hdel', 'hexists', 'hget', 'hgetall',
                         'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hset', 'hsetnx',
                         'hmset', 'hmget', 'hvals', 'publish', 'eval', 'evalsha',
                         'script_exists', 'script_flush', 'script_kill', 'script_load',
                         'setex', 'lrem', 'zadd')

_redis_multipart_commands = set(['client', 'cluster', 'command', 'config',
                                 'debug', 'sentinel', 'slowlog', 'script'])

_redis_operation_re = re.compile('[-\s]+')


def _conn_attrs_to_dict(connection):
    return {
        'host': getattr(connection, 'host', None),
        'port': getattr(connection, 'port', None),
        'path': getattr(connection, 'path', None),
        'db': getattr(connection, 'db', None),
    }


def _instance_info(kwargs):
    host = kwargs.get('host') or 'localhost'
    port_path_or_id = str(kwargs.get('port') or kwargs.get('path', 'unknown'))
    db = str(kwargs.get('db') or 0)

    return (host, port_path_or_id, db)


def _wrap_Redis_method_wrapper_(module, instance_class_name, operation):
    def _nr_wrapper_Redis_method_(wrapped, instance, args, kwargs):
        transaction = current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        dt = DatastoreTrace(
            product='Redis',
            target=None,
            operation=operation,
            span_type=SpanType.Exit.value,
            span_layer=SpanLayerAtrr.CACHE.value
        )

        transaction._nr_datastore_instance_info = (None, None, None)

        with dt:
            result = wrapped(*args, **kwargs)

            host, port_path_or_id, db = transaction._nr_datastore_instance_info
            dt.host = host
            dt.port_path_or_id = port_path_or_id
            dt.database_name = db

            return result

    name = '%s.%s' % (instance_class_name, operation)
    wrap_function_wrapper(module, name, _nr_wrapper_Redis_method_)


def instrument_redis_client(module):
    if hasattr(module, 'StrictRedis'):
        for name in _redis_client_methods:
            if name in vars(module.StrictRedis):
                _wrap_Redis_method_wrapper_(module, 'StrictRedis', name)

    if hasattr(module, 'Redis'):
        for name in _redis_client_methods:
            if name in vars(module.Redis):
                _wrap_Redis_method_wrapper_(module, 'Redis', name)


def _nr_Connection_send_command_wrapper_(wrapped, instance, args, kwargs):
    transaction = current_transaction()

    if transaction is None or not args:
        return wrapped(*args, **kwargs)

    host, port_path_or_id, db = (None, None, None)

    try:
        dt = transaction.settings.datastore_tracer
        if (dt.instance_reporting.enabled or
                dt.database_name_reporting.enabled):
            conn_kwargs = _conn_attrs_to_dict(instance)
            host, port_path_or_id, db = _instance_info(conn_kwargs)
    except:
        pass

    transaction._nr_datastore_instance_info = (host, port_path_or_id, db)

    operation = args[0].strip().lower()

    if operation.split()[0] not in _redis_multipart_commands:
        return wrapped(*args, **kwargs)

    if operation in _redis_multipart_commands and len(args) > 1:
        operation = '%s %s' % (operation, args[1].strip().lower())

    operation = _redis_operation_re.sub('_', operation)

    with DatastoreTrace(
            product='Redis',
            target=None,
            operation=operation,
            host=host,
            port_path_or_id=port_path_or_id,
            database_name=db,
            span_type=SpanType.Exit.value,
            span_layer=SpanLayerAtrr.CACHE.value
    ):
        return wrapped(*args, **kwargs)


def instrument_redis_connection(module):
    wrap_function_wrapper(module, 'Connection.send_command',
                          _nr_Connection_send_command_wrapper_)
