# pylint: disable=C0103
""" QLog logger """

import inspect
import os
from datetime import datetime

from QLog.log_entry import LogEntry

__version__ = "0.1.0"

from QLog.log_level import LogLevel
from QLog.logger import Logger


def QLogHighlight(data):
    """ Log highlight """

    log(LogLevel.HIGHLIGHT, data)


def QLogDebug(data):
    """ Log debug """

    log(LogLevel.DEBUG, data)


def QLogInfo(data):
    """ Log info """

    log(LogLevel.INFO, data)


def QLogWarning(data):
    """ Log warning """

    log(LogLevel.WARNING, data)


def QLogError(data):
    """ Log error """

    log(LogLevel.ERROR, data)


loggers: [Logger] = []


def log(level: LogLevel, data):
    """ log """

    caller = inspect.stack()[2]
    entry = LogEntry(
        datetime.now(),
        os.path.splitext(os.path.basename(caller.filename))[0],
        caller.function,
        caller.lineno,
        level,
        str(data)
    )
    for active_logger in loggers:
        active_logger.log(entry)
