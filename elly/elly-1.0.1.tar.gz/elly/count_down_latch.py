"""
say something
"""
__author__ = 'it_fk@163.com'

import logging
from datetime import datetime
from threading import Condition, Thread, currentThread
from typing import List, Callable

logging.basicConfig(level=logging.INFO)


class CountDownLatch:
    """Behavior like Java CountDownLatch
    """

    def __init__(self) -> None:
        self.__condition = Condition()
        self.__count = 0
        self.__threads: List[Thread] = []
        self.__results: List[tuple] = []

    def run(self) -> list:
        """start the targets function as a Thread

        :return: target function's result
        """
        self.__count = len(self.__threads)
        for t in self.__threads:
            t.start()
        try:
            self.__condition.acquire()
            while self.__count > 0:
                # logging.info('Undone Threads %s', self.__threads)
                self.__condition.wait()
        finally:
            self.__condition.release()
        return self.__results

    def __countdown_wrapper(self, target: Callable) -> Callable:
        """wrap the target function

        :param target: the function will be run
        :return: wrapped function
        """

        def wrapper(*args, **kwargs):
            ret = None
            try:
                ret = target(*args, **kwargs)
            except Exception as err:
                logging.warning("target function exception occurred!", exc_info=err)
            t = currentThread()
            logging.info('Done Thread %s at %s', t, datetime.now())
            self.__threads.remove(t)
            if ret is not None:
                self.__results.append(ret)
            try:
                self.__condition.acquire()
                self.__count -= 1
                self.__condition.notifyAll()
            finally:
                self.__condition.release()

        return wrapper

    def append(self, target: Callable, *args) -> None:
        """add Thread task

        :param target: the function will be run
        :param args: the function arguments
        :return: None
        """
        self.__threads.append(Thread(target=self.__countdown_wrapper(target), args=args))


if __name__ == '__main__':
    from random import randint
    from time import sleep


    def do_something(*args) -> tuple:
        logging.info('start do something with %s at %s', args, datetime.now())
        rnd = randint(0, 6000) / 1000
        logging.info('sleep %s seconds', rnd)
        sleep(rnd)
        return args[0], 'done'


    cdl = CountDownLatch()
    cdl.append(do_something, '第一个线程', 'a', 'b')
    cdl.append(do_something, '第二个线程', 1, 2, 3)
    # results = cdl.run()

    cdl.append(do_something, '第3个线程')
    cdl.append(do_something, '第4个线程')
    results = cdl.run()
    logging.info("got result %s at %s", results, datetime.now())
