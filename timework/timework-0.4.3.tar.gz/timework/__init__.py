"""
timework 0.4.3

MIT License © bugstop

PyPI:   https://pypi.org/project/timework/
GitHub: https://github.com/bugstop/python-timework/


measure / limit execution time using with-statements or decorators, cross-platform

timework.Stopwatch()  - a with statement class for stopwatch
timework.timer()      - a decorator measuring the execution time
timework.limit()      - a decorator limiting the execution time
"""


from .timework import *

__name__ = 'timework'
__version__ = '0.4.3'
__all__ = ['Stopwatch', 'timer', 'limit']
