from json import loads
from typing import Optional, Callable
from redis import Redis
from arsene.schemas.redis import RedisModel


class RedisConnection():
    def __init__(
        self, *, schema: RedisModel,
        set_data: Callable,
        resolve_data: Callable,
        object_hook: Callable,
        json_serial: Callable
    ):
        self.schema = schema
        self.status = False
        self.set_data = set_data
        self.object_hook = object_hook
        self.json_serial = json_serial
        self.resolve_data = resolve_data
        self.client = self.create_client()

    def create_client(self):
        return Redis(
            **self.schema.dict()
        )

    def test_connection(self):
        self.client.ping()
        self.status = True

    def set(self, *, key: str, expire: Optional[int] = None, data):
        data_convert = self.set_data(
            data, serializable=self.json_serial
        )
        self.client.set(key, data_convert, ex=expire)

    def get(self, *, key: str):
        if not self.client.get(key):
            return None

        data_convert = self.client.get(key).decode('utf-8')
        data_json = loads(data_convert)
        return self.resolve_data(
            data_json, object_hook=self.object_hook
        )

    def delete(self, *, key: str):
        self.client.delete(key)
