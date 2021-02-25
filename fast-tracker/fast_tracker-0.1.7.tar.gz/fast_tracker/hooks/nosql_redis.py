# -*- coding: utf-8 -*-

import fast_tracker.api.function_trace

_methods_1 = ['bgrewriteaof', 'bgsave', 'config_get', 'config_set',
              'dbsize', 'debug_object', 'delete', 'echo', 'flushall',
              'flushdb', 'info', 'lastsave', 'object', 'ping', 'save',
              'shutdown', 'slaveof', 'append', 'decr', 'exists',
              'expire', 'expireat', 'get', 'getbit', 'getset', 'incr',
              'keys', 'mget', 'mset', 'msetnx', 'move', 'persist',
              'randomkey', 'rename', 'renamenx', 'set', 'setbit',
              'setex', 'setnx', 'setrange', 'strlen', 'substr', 'ttl',
              'type', 'blpop', 'brpop', 'brpoplpush', 'lindex',
              'linsert', 'llen', 'lpop', 'lpush', 'lpushx', 'lrange',
              'lrem', 'lset', 'ltrim', 'rpop', 'rpoplpush', 'rpush',
              'rpushx', 'sort', 'sadd', 'scard', 'sdiff', 'sdiffstore',
              'sinter', 'sinterstore', 'sismember', 'smembers',
              'smove', 'spop', 'srandmember', 'srem', 'sunion',
              'sunionstore', 'zadd', 'zcard', 'zcount', 'zincrby',
              'zinterstore', 'zrange', 'zrangebyscore', 'zrank', 'zrem',
              'zremrangebyrank', 'zremrangebyscore', 'zrevrange',
              'zrevrangebyscore', 'zrevrank', 'zscore', 'zunionstore',
              'hdel', 'hexists', 'hget', 'hgetall', 'hincrby', 'hkeys',
              'hlen', 'hset', 'hsetnx', 'hmset', 'hmget', 'hvals',
              'publish']

_methods_2 = ['setex', 'lrem', 'zadd']


def instrument_redis_connection(module):
    fast_tracker.api.function_trace.wrap_function_trace(
        module, 'Connection.connect')


def instrument_redis_client(module):
    if hasattr(module, 'StrictRedis'):
        for method in _methods_1:
            if hasattr(module.StrictRedis, method):
                fast_tracker.api.function_trace.wrap_function_trace(
                    module, 'StrictRedis.%s' % method)
    else:
        for method in _methods_1:
            if hasattr(module.Redis, method):
                fast_tracker.api.function_trace.wrap_function_trace(
                    module, 'Redis.%s' % method)

    for method in _methods_2:
        if hasattr(module.Redis, method):
            fast_tracker.api.function_trace.wrap_function_trace(
                module, 'Redis.%s' % method)
