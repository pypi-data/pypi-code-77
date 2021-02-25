"""
Package utility
"""
from collections import UserDict
from contextlib import contextmanager


class Dict(UserDict):
    """
    Support access key via attribute style.

    >>> d = Dict(bar='foo')
    >>> d.bar == 'foo'
    True
    """
    def __getattr__(self, key):
        return self[key]


@contextmanager
def open_file(value):
    """Receive a file_obj or filename, return a file_obj.
    """
    if hasattr(value, 'read') or hasattr(value, 'write'):
        yield value
    else:
        with open(value) as f:
            yield f
