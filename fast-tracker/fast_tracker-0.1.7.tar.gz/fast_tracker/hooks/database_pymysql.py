# -*- coding: utf-8 -*-

from fast_tracker.api.database_trace import register_database_client
from fast_tracker.common.object_wrapper import wrap_object

from fast_tracker.hooks.database_mysqldb import (
    ConnectionFactory as MySqlDBConnectionFactory,
    ConnectionWrapper as MySqlDBConnectionWrapper,
)

from fast_tracker.hooks.database_dbapi2 import (
    CursorWrapper as DBAPI2CursorWrapper,
)


class CursorWrapper(DBAPI2CursorWrapper):

    def __enter__(self):
        self.__wrapped__.__enter__()
        return self


class ConnectionWrapper(MySqlDBConnectionWrapper):
    __cursor_wrapper__ = CursorWrapper


class ConnectionFactory(MySqlDBConnectionFactory):
    __connection_wrapper__ = ConnectionWrapper


def instance_info(args, kwargs):
    def _bind_params(host=None, user=None, passwd=None, db=None,
                     port=None, *args, **kwargs):
        return host, port, db

    host, port, db = _bind_params(*args, **kwargs)

    return host, port, db


def instrument_pymysql(module):
    register_database_client(module, database_product='MySQL',
                             quoting_style='single+double', explain_query='explain',
                             explain_stmts=('select',), instance_info=instance_info)

    wrap_object(module, 'connect', ConnectionFactory, (module,))

    if hasattr(module, 'Connect'):
        wrap_object(module, 'Connect', ConnectionFactory, (module,))
