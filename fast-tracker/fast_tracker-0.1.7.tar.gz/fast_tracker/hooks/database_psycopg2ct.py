# -*- coding: utf-8 -*-


from fast_tracker.api.database_trace import register_database_client
from fast_tracker.common.object_wrapper import wrap_object

from fast_tracker.hooks.database_dbapi2 import ConnectionFactory
from fast_tracker.hooks.database_psycopg2 import (instance_info,
                                                  instrument_psycopg2_extensions)


def instrument_psycopg2ct(module):
    register_database_client(module, database_product='Postgres',
                             quoting_style='single+dollar', explain_query='explain',
                             explain_stmts=('select', 'insert', 'update', 'delete'),
                             instance_info=instance_info)

    wrap_object(module, 'connect', ConnectionFactory, (module,))


def instrument_psycopg2ct_extensions(module):
    instrument_psycopg2_extensions(module)
