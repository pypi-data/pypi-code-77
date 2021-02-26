"""
timework 0.4.1

MIT License © bugstop

PyPI:   https://pypi.org/project/timework/
GitHub: https://github.com/bugstop/python-timework/


measure / limit execution time using with-statements or decorators, cross-platform

timework.timer()      - a decorator measuring the execution time
timework.limit()      - a decorator limiting the execution time
timework.Stopwatch()  - a with statement class for stopwatch
"""


from .timework import *

__name__ = 'timework'
__version__ = '0.4.1'
__all__ = ['timer', 'limit', 'Stopwatch']
