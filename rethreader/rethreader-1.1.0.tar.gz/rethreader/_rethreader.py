from time import sleep
from typing import Optional, Iterable, List, Set
from ._keythread import KeyThread
from ._utils import Key, is_collection, is_unpacked, ThreadInfo, FakeSet


class Rethreader:
    def __init__(self, target=None, queue: Optional[Iterable] = None, max_threads: int = 16, clock_delay: float = 0.01,
                 auto_quit: Optional[bool] = None, save_results=True, daemon: bool = False):
        if target is not None:
            assert callable(target)
        self._target = target
        self._main: Set[KeyThread] = set()
        self._in_delay_queue: int = 0
        self._finished: int = 0
        self._finished_set = FakeSet()
        if save_results:
            self._finished_set: Set[KeyThread] = set()
        self._daemonic: bool = daemon
        self._clock: float = clock_delay
        self._max_threads: int = 0 if max_threads < 0 else max_threads
        self._queue: List[Key] = []
        if queue:
            [self.add(_t) for _t in queue]
        self._auto_quit: bool = auto_quit if auto_quit else bool(queue)
        self._running: bool = False
        self._start_thread = None

    def __add__(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def __enter__(self):
        if not self._running:
            self.start()
        return self.auto_quit(False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def __len__(self) -> int:
        return self.remaining + self.finished

    def _unpack(self, *_object, **kwargs) -> Key:
        if isinstance(_object, tuple):
            if len(_object) == 1:
                _object = _object[0]
            if is_unpacked(_object):
                return Key(*_object)
        target, args = self._target, None
        _list = list(_object) if is_collection(_object) else None
        if target is None and _list and callable(_list[0]):
            target = _list.pop(0)
        if not kwargs and _list and type(_list[-1]) == dict:
            kwargs = _list.pop(-1)
        if _list and len(_list) == 1 and type(_list[0]) == tuple:
            args = _list[0]
        if args is None:
            if _list is not None:
                _object = _object.__class__(_list)
            if type(_object) == tuple:
                args = _object
            else:
                args = (_object,)
        return Key(len(self), target, args, kwargs)

    def _info_unpack(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], ThreadInfo):
            return args[0].key()
        return self._unpack(*args, **kwargs)

    def _get_thread(self, target=None, args=(), kwargs=None) -> KeyThread:
        if isinstance(target, Key):
            return KeyThread.of(target, self._daemonic)
        return KeyThread(None, target, args, kwargs, self._daemonic)

    def _load_target(self, target) -> KeyThread:
        if isinstance(target, KeyThread):
            return target
        return self._get_thread(self._unpack(target))

    def _start_next(self):
        next_target = self._queue.pop(0)
        next_thread = self._load_target(next_target)
        next_thread.start()
        self._main.add(next_thread)

    def run(self):
        self._running = True
        while self._running:
            for t in self._main.copy():
                if not t.is_alive():
                    self._finished_set.add(t)
                    self._finished += 1
                    self._main.remove(t.kill())
            while self._queue:
                if 0 < self._max_threads <= len(self._main):
                    break
                self._start_next()
            if self._auto_quit and self.is_empty():
                self._running = False
            else:
                sleep(self._clock)
        return self

    def _append(self, _object, _delay: int = 0):
        self._in_delay_queue += 1
        if _delay:
            sleep(_delay)
        self._queue.append(_object)
        self._in_delay_queue -= 1

    def _find(self, _thread_info: ThreadInfo):
        sets = [self._main, self._queue]
        if self._finished_set:
            sets.append(self._finished_set)
        for _list in sets:
            for thread in _list:
                if ThreadInfo.of(thread) == _thread_info:
                    return thread

    def _insert(self, _object):
        self._queue.insert(0, _object)

    def _wait_return(self, _thread_info: ThreadInfo):
        key = self._find(_thread_info)
        if isinstance(key, Key):
            while key in self._queue:
                sleep(self._clock)
        kt = self._find(_thread_info)
        if kt:
            while kt in self._main:
                sleep(self._clock)
            return kt

    def add(self, *args, **kwargs):
        self._append(self._unpack(*args, **kwargs))
        return self

    def find(self, *args, **kwargs):
        thi = ThreadInfo(self._info_unpack(*args, **kwargs))
        thread = self._find(thi)
        if thread:
            return thread

    def execute(self, *args, **kwargs):
        _key = self._unpack(*args, **kwargs)
        self._insert(_key)
        return self._wait_return(ThreadInfo.of(_key)).result

    def extend(self, _list: Iterable):
        for i in _list:
            self.add(i)
        return self

    def insert(self, *args, **kwargs):
        self._insert(self._unpack(*args, **kwargs))
        return self

    def prioritize(self, _list: Iterable):
        for i in reversed(list(_list)):
            self._insert(self._unpack(i))
        return self

    def task(self, *args, **kwargs):
        _key = self._unpack(*args, **kwargs)
        self._append(_key)
        return self._wait_return(ThreadInfo.of(_key)).result

    def remove(self, *args, **kwargs):
        _thi = ThreadInfo(self._info_unpack(*args, **kwargs))
        thread = self._find(_thi)
        if thread:
            _list = self._queue
            if isinstance(thread, KeyThread):
                thread.kill()
                _list = self._main
            try:
                _list.remove(thread)
            except KeyError:
                pass
        return self

    def postpone(self, delay, *args, **kwargs):
        _object = self._unpack(*args, **kwargs)
        self.remove(_object)
        self._get_thread(self._append, (_object, delay)).start()
        return self

    def auto_quit(self, _bool: bool = True):
        self._auto_quit = _bool
        return self

    @property
    def finished(self) -> int:
        return self._finished

    @property
    def in_queue(self) -> int:
        return len(self._queue) + self._in_delay_queue

    def is_empty(self) -> bool:
        return self.remaining == 0

    def is_alive(self) -> bool:
        return self._running

    def kill(self):
        self._queue.clear()
        for thread in self._main:
            thread.kill()
        self._main.clear()
        self._running = False
        if self._start_thread:
            self._start_thread.kill()
        return self

    def quit(self):
        self._auto_quit = True
        if self._start_thread:
            self._start_thread.join()
            self._start_thread = None
        while self._running:
            sleep(self._clock)
        return self

    @property
    def remaining(self) -> int:
        return len(self._main) + self.in_queue

    @property
    def results(self) -> list:
        if self._finished_set:
            return [i.result for i in sorted(self._finished_set, key=lambda x: x.id)]

    def start(self):
        self._start_thread = self._get_thread(self.run)
        self._start_thread.start()
        return self


if __name__ == '__main__':
    print("Hello world!")
