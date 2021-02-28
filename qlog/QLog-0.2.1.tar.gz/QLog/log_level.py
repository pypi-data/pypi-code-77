""" The enum defining the log levels """
import logging
from enum import Enum


class LogLevel(Enum):
    """ The enum defining the log levels """

    HIGHLIGHT = 4
    DEBUG = 3
    INFO = 2
    WARNING = 1
    ERROR = 0

    @property
    def ansi_color(self):
        """ Associates an ansi color with each log level """

        return ansi_colors[self]

    @property
    def ansi_color_sequence(self):
        """ Returns ANSI color sequence """

        return u'\u001b' + '[' + str(self.ansi_color)

    @property
    def python_log_level(self):
        """ Associates a python log level with each log level """

        return python_log_levels[self]

    @property
    def text(self):
        """ Associates a text with each log level """

        return texts[self]

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            # pylint: disable=W0143
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            # pylint: disable=W0143
            return self.value <= other.value
        return NotImplemented


ansi_colors = {
    LogLevel.HIGHLIGHT: '35m',
    LogLevel.DEBUG: '34m',
    LogLevel.INFO: '32m',
    LogLevel.WARNING: '33m',
    LogLevel.ERROR: '31m'
}

python_log_levels = {
    LogLevel.HIGHLIGHT: logging.DEBUG,
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR
}

texts = {
    LogLevel.HIGHLIGHT: '[HIGH] ',
    LogLevel.DEBUG: '[DEBUG]',
    LogLevel.INFO: '[INFO] ',
    LogLevel.WARNING: '[WARN] ',
    LogLevel.ERROR: '[ERROR]'
}
