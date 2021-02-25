# @Time   : 2021-02-25
# @Author : zhangxinhao
if False:
    import numpy as np

    class SharedNumpy:
        def __init__(self):
            self.uuid = None
            self.shape = None
            self.dtype = None
            self.shm = None
            self.data = None

        def info(self):
            return {
                'uuid': self.uuid,
                'shape': self.shape,
                'dtype': self.dtype
            }

        @property
        def ndarray(self) -> np.ndarray:
            pass

        @staticmethod
        def Name(shape, dtype) -> str:
            pass

        @property
        def name(self) -> str:
            pass

        def release(self):
            pass

        def _release(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def new_shared_numpy(shape, dtype, max_pool_size=0) -> SharedNumpy:
        pass

    def make_shared_numpy(array, max_pool_size=0) -> SharedNumpy:
        pass

    def load_shared_numpy(info) -> SharedNumpy:
        pass

from .shared_numpy import *
