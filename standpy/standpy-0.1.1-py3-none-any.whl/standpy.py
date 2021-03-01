## Standard Library
import abc
import subprocess
from functools import wraps
from multiprocessing import Lock

## Third-party
from oswhich import linux, windows, macosx

#pylint: disable=function-redefined
class _StandbyLock(object, metaclass=abc.ABCMeta):
    """
    """

    __ref__ = None

    def __new__(cls):
        if cls.__ref__ is None:
            cls.__ref__ = object.__new__(cls)
        return cls.__ref__

    __wait = 0
    __lock = Lock()

    @classmethod
    def wait_acquire(cls) -> bool:
        with cls.__lock:
            cls.__wait += 1
            if cls.__wait == 1:
                return True
            elif cls.__wait > 1:
                return False
            else:
                raise RuntimeError("Inconsistent wait count.")

    @classmethod
    def wait_release(cls) -> bool:
        with cls.__lock:
            cls.__wait -= 1
            if cls.__wait == 0:
                return True
            elif cls.__wait > 0:
                return False
            else:
                cls.__wait = 0
                return False

    @abc.abstractclassmethod
    def inhibit(cls):
        ...

    @abc.abstractclassmethod
    def release(cls):
        ...

    def __enter__(self):
        if self.wait_acquire():
            self.inhibit()
        return self

    def __exit__(self, *args, **kwargs):
        if self.wait_release():
            self.release()

@windows
class StandbyLock(_StandbyLock):
    """
    """

    ES_CONTINUOUS      = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    INHIBIT = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    RELEASE = ES_CONTINUOUS

    @classmethod
    def inhibit(cls):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(cls.INHIBIT)

    @classmethod
    def release(cls):
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(cls.RELEASE)

@linux
class StandbyLock(_StandbyLock):
    """
    """

    COMMAND = 'systemctl'
    ARGS = ['sleep.target', 'suspend.target', 'hibernate.target', 'hybrid-sleep.target']

    @classmethod
    def inhibit(cls):
        subprocess.run([cls.COMMAND, 'mask', *cls.ARGS])

    @classmethod
    def release(cls):
        subprocess.run([cls.COMMAND, 'unmask', *cls.ARGS])

@macosx
class StandbyLock(_StandbyLock):
    """
    """

    COMMAND = 'caffeinate'
    BREAK = b'\003'

    _process = None

    @classmethod
    def inhibit(cls):
        cls._process = subprocess.Popen([cls.COMMAND], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    @classmethod
    def release(cls):
        if cls._process is not None:
            cls._process.stdin.write(cls.BREAK)
            cls._process.stdin.flush()
            cls._process.stdin.close()
            cls._process.wait()
        else:
            raise RuntimeError("Fatal: release() called before inhibit().")

def standby_lock(callback):
    """ This decorator guarantees that the system will not enter standby mode while 'callable' is running.
    """
    @wraps(callback)
    def new_callback(*args, **kwargs):
        with StandbyLock():
            return callback(*args, **kwargs)
    return new_callback