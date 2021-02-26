import traceback

import os
import sys
from functools import partial

import logging
import time
from zmq import ContextTerminated


def _thread_wrapper(run_function, return_code):
    try:
        run_function()
    except (KeyboardInterrupt, ContextTerminated):  # pragma: no cover
        pass
    except Exception as e:  # pragma: no cover
        logging.exception(e)
        sys.stderr.flush()
        time.sleep(1)
        os._exit(return_code)


def get_thread_wrapper(function, return_code=10):
    return partial(_thread_wrapper, function, return_code)
