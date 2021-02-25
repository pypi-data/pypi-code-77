# -*- coding: utf-8 -*-


from fast_tracker.api.datastore_trace import wrap_datastore_trace
from fast_tracker.api.function_trace import wrap_function_trace

_pymongo_client_methods = ('save', 'insert', 'update', 'drop', 'remove',
                           'find_one', 'find', 'count', 'create_index', 'ensure_index',
                           'drop_indexes', 'drop_index', 'reindex', 'index_information',
                           'options', 'group', 'rename', 'distinct', 'map_reduce',
                           'inline_map_reduce', 'find_and_modify', 'initialize_unordered_bulk_op',
                           'initialize_ordered_bulk_op', 'bulk_write', 'insert_one', 'insert_many',
                           'replace_one', 'update_one', 'update_many', 'delete_one', 'delete_many',
                           'find_raw_batches', 'parallel_scan', 'create_indexes', 'list_indexes',
                           'aggregate', 'aggregate_raw_batches', 'find_one_and_delete',
                           'find_one_and_replace', 'find_one_and_update')


def instrument_pymongo_connection(module):
    rollup = ('Datastore/all', 'Datastore/MongoDB/all')

    wrap_function_trace(module, 'Connection.__init__',
                        name='%s:Connection.__init__' % module.__name__,
                        terminal=True, rollup=rollup)


def instrument_pymongo_mongo_client(module):
    rollup = ('Datastore/all', 'Datastore/MongoDB/all')

    wrap_function_trace(module, 'MongoClient.__init__',
                        name='%s:MongoClient.__init__' % module.__name__,
                        terminal=True, rollup=rollup)


def instrument_pymongo_collection(module):
    def _collection_name(collection, *args, **kwargs):
        return collection.name

    for name in _pymongo_client_methods:
        if hasattr(module.Collection, name):
            wrap_datastore_trace(module.Collection, name, product='MongoDB',
                                 target=_collection_name, operation=name)
