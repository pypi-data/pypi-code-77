""" main """
from pathlib import Path

import QLog
from QLog import QLogHighlight, QLogDebug, QLogInfo, QLogWarning, QLogError, LogLevel
from QLog.console_logger import ConsoleLogger
from QLog.file_logger import FileLogger


def main():
    """ main """

    QLog.loggers = [ConsoleLogger(), FileLogger(log_level=LogLevel.DEBUG, path=Path('log/test.log'))]
    QLogHighlight('Highlight')
    QLogDebug('Debug')
    QLogInfo('Info')
    QLogWarning('Warning')
    QLogError('Error')


if __name__ == '__main__':
    main()
