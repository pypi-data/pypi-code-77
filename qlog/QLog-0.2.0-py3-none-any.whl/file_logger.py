"""  Logger to log into files """

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from QLog.log_entry import LogEntry
from QLog.log_level import LogLevel
from QLog.logger import Logger


class FileLogger(Logger):
    """  Logger to log into files """

    def __init__(self, log_level=LogLevel.INFO, path=Path('log/log')):
        self.log_level = log_level
        os.makedirs(path.parent.absolute(), exist_ok=True)
        self.logger = logging.getLogger('File Logger')
        self.logger.setLevel(log_level.python_log_level)
        self.logger.addHandler(TimedRotatingFileHandler(path.absolute(), when='D'))

    def do_log(self, log_entry: LogEntry):
        text = '\n' + log_entry.log_level.text + ' ' + log_entry.meta_text + log_entry.text
        if self.log_level is LogLevel.INFO:
            return self.logger.info(text)
        if self.log_level is LogLevel.WARNING:
            return self.logger.warning(text)
        if self.log_level is LogLevel.ERROR:
            return self.logger.error(text)
        return self.logger.debug(text)
