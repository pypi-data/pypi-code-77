#!/usr/bin/env python
# encoding: utf-8

"""
Provides miscellaneous utilites for tvgutil classes.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)


class KeyedListView(object):

    """
    A "view" of a list containing custom objects. When obtaining values by
    index, first, the "key" function is evaluated on the list element and
    its result is returned. This allows having functionality similar to the
    "key" parameter of list.sort() for other functions not supporting such
    a parameter.
    """

    __slots__ = ("base_list", "key")

    def __init__(self, base_list, key):
        self.base_list = base_list
        self.key = key

    def __len__(self):
        return len(self.base_list)

    def __getitem__(self, index):
        return self.key(self.base_list[index])
