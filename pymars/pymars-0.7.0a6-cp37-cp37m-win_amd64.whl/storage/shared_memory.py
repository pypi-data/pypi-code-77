# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import random
import weakref
from string import ascii_letters, digits
from typing import Any, Dict, List, Tuple, Optional
try:
    from multiprocessing.shared_memory import SharedMemory
except ImportError:  # pragma: no cover
    # shared_memory is available for Python 3.8+
    # until we decide to backport this module
    # we just let it go for python<3.8
    SharedMemory = None

from ..serialization import AioSerializer, AioDeserializer
from ..utils import implements
from .base import StorageBackend, StorageLevel, ObjectInfo
from .core import BufferWrappedFileObject, StorageFileObject


class SharedMemoryFileObject(BufferWrappedFileObject):
    def __init__(self,
                 object_id: Any,
                 mode: str,
                 size: Optional[int] = None):
        self._object_id = object_id
        self.shm = None
        super().__init__(mode, size=size)

    def _write_init(self):
        self.shm = shm = SharedMemory(
            name=self._object_id, create=True, size=self._size)
        self._buffer = self._mv = shm.buf

    def _read_init(self):
        self.shm = shm = SharedMemory(name=self._object_id)
        self._buffer = self._mv = buf = shm.buf
        self._size = buf.nbytes

    def _write_close(self):
        pass

    def _read_close(self):
        pass


class _SharedMemoryManager:
    def __init__(self):
        self._object_id_to_shms = dict()
        self._object_id_to_buffer = dict()

    def register(self, object_id: Any, shm: SharedMemory):
        # SharedMemory will release buffer when it's gc collected
        # here we create the reference from buffer to SharedMemory
        def _cb(_):
            del self._object_id_to_shms[object_id]
            del self._object_id_to_buffer[object_id]
        self._object_id_to_shms[object_id] = shm
        self._object_id_to_buffer[object_id] = weakref.ref(shm.buf, _cb)


_shared_memory_manager = _SharedMemoryManager()


class SharedMemoryStorage(StorageBackend):
    def __init__(self, **kw):
        if kw:  # pragma: no cover
            raise TypeError(f'SharedMemoryStorage got unexpected arguments: {",".join(kw)}')
        # for test purpose, in real usage,
        # each storage object holds different object ids,
        # we cannot do any operation according to
        # this property only
        self._object_ids = set()

    @classmethod
    @implements(StorageBackend.setup)
    async def setup(cls, **kwargs) -> Tuple[Dict, Dict]:
        if kwargs:  # pragma: no cover
            raise TypeError(f'SharedMemoryStorage got unexpected config: {",".join(kwargs)}')

        return dict(), dict()

    @staticmethod
    @implements(StorageBackend.teardown)
    async def teardown(**kwargs):
        object_ids = kwargs.get('object_ids')
        for object_id in object_ids:
            shm = SharedMemory(name=object_id)
            shm.unlink()
            await asyncio.sleep(0)

    @property
    @implements(StorageBackend.level)
    def level(self) -> StorageLevel:
        return StorageLevel.MEMORY

    @classmethod
    def _generate_object_id(cls):
        return ''.join(random.choice(ascii_letters + digits) for _ in range(30))

    @implements(StorageBackend.get)
    async def get(self, object_id, **kwargs) -> object:
        shm_file = SharedMemoryFileObject(object_id, mode='r')

        async with StorageFileObject(shm_file, object_id) as f:
            deserializer = AioDeserializer(f)
            result = await deserializer.run()
            # SharedMemory will release buffer when it's gc collected
            # so we create the reference from buffer to SharedMemory
            _shared_memory_manager.register(object_id, shm_file.shm)
            return result

    @implements(StorageBackend.put)
    async def put(self, obj, importance=0) -> ObjectInfo:
        object_id = self._generate_object_id()

        serializer = AioSerializer(obj)
        buffers = await serializer.run()
        buffer_size = sum(getattr(buf, 'nbytes', len(buf))
                          for buf in buffers)

        shm_file = SharedMemoryFileObject(object_id, mode='w',
                                          size=buffer_size)
        async with StorageFileObject(shm_file, object_id) as f:
            for buffer in buffers:
                await f.write(buffer)

        self._object_ids.add(object_id)
        return ObjectInfo(size=buffer_size, object_id=object_id)

    @implements(StorageBackend.delete)
    async def delete(self, object_id):
        shm = SharedMemory(name=object_id)
        shm.unlink()
        self._object_ids.remove(object_id)

    @implements(StorageBackend.object_info)
    async def object_info(self, object_id) -> ObjectInfo:
        shm_file = SharedMemoryFileObject(object_id, mode='r')

        async with StorageFileObject(shm_file, object_id) as f:
            deserializer = AioDeserializer(f)
            size = await deserializer.get_size()
        return ObjectInfo(size=size, object_id=object_id)

    @implements(StorageBackend.open_writer)
    async def open_writer(self, size=None) -> StorageFileObject:
        if size is None:  # pragma: no cover
            raise ValueError('size must be provided for shared memory backend')

        new_id = self._generate_object_id()
        shm_file = SharedMemoryFileObject(new_id, size=size, mode='w')
        return StorageFileObject(shm_file, object_id=new_id)

    @implements(StorageBackend.open_reader)
    async def open_reader(self, object_id) -> StorageFileObject:
        shm_file = SharedMemoryFileObject(object_id, mode='r')
        return StorageFileObject(shm_file, object_id=object_id)

    @implements(StorageBackend.list)
    async def list(self) -> List:  # pragma: no cover
        raise NotImplementedError("Shared memory storage does not support list")
