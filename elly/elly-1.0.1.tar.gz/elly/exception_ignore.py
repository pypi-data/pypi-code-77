"""
say something
"""
__author__ = 'it_fk@163.com'
import logging
import sys

from count_down_latch import CountDownLatch


class IgnoreException:
    """Behavior like Spring ExceptionHandler
    """

    def __init__(self, *args):
        self.__ignored_exc_type: tuple = args

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """True indicate the exception will not be raised up

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if not self.__ignored_exc_type or exc_type in self.__ignored_exc_type:
            logging.warning("Ignored Exception %s Occurred", exc_type.__name__, exc_info=(exc_type, exc_val, exc_tb))
            return True
        return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # with IgnoreException(FileExistsError, FileNotFoundError):
    #     open('exception.txt')
    # print('always run...')
    # try:
    #     open('exception.txt')
    # except:
    #     print('exception occurred!')
    # finally:
    #     print('always run???')

    # def openfile():
    #     with IgnoreException():
    #         open('xx.txt')
    # # cdl = CountDownLatch()
    # cdl.append(openfile)
    # cdl.run()

    try:
        open('exception.txt')
    except:
        err = sys.exc_info()
        for e in err:
            print(e)
