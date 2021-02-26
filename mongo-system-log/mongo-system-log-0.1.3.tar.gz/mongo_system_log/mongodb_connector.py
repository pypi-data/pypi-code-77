from pymongo import MongoClient
from os import getenv

MONGO_URL = getenv('MONGO_URL')
MONGO_DB = getenv('MONGO_DB')


def connect():
    if not MONGO_URL or not MONGO_DB:
        raise Exception('Need to setup MONGO_URL and MONGO_DB environments variables')

    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    return client[MONGO_DB]


def singleton(my_class):
    instances = dict()

    def get_instances(*args, **kwargs):
        if my_class not in instances:
            instances[my_class] = my_class(*args, *kwargs)
        return instances[my_class]

    return get_instances


@singleton
class ConnectMongo(object):

    def __init__(self):
        self.mongo_url = MONGO_URL
        self.mongo_db = MONGO_DB
        self.db = connect()


