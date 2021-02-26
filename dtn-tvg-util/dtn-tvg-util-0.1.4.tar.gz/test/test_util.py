#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest

from tvgutil import util


class TestKeyedListView(unittest.TestCase):

    def test_keyed_list_view(self):
        LIST = [("A", "B", "C"), ("D", "E", "F")]
        klv = util.KeyedListView(LIST, key=lambda x: x[1])
        self.assertEqual("B", klv[0])
        self.assertEqual("E", klv[1])
        self.assertEqual("E", klv[-1])
        with self.assertRaises(IndexError):
            klv[2]
