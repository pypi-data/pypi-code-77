#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest

from tvgutil import contact_plan, tvg, transmission_plan


class TestTransmissionPlan(unittest.TestCase):

    BASIC_PCP_TUPLES_PROB = [
        ("bs1", "TESTSAT 1", 0, 4, 4, 0.95, 0.01),
        ("TESTSAT 1", "bs1", 0, 4, 12, 0.95, 0.01),
        ("bs1", "TESTSAT 2", 1, 7, 9, 1.0, 0.1),
        ("bs5", "TESTSAT 3", 8, 10, 2, 0.2, 0.1),
    ]

    def setUp(self):
        self.graph = tvg.from_contact_plan([
            contact_plan.PredictedContact.simple(*t)
            for t in self.BASIC_PCP_TUPLES_PROB
        ])

    def _is_known_node(self, node):
        if node == "TESTSAT 3":
            return False
        for c in self.BASIC_PCP_TUPLES_PROB:
            if c[0] == node or c[1] == node:
                return True
        return False

    def test_generate(self):
        tplan = transmission_plan.generate(
            self.graph,
            starttime=2,
            stoptime=9,
            minsize=20,
            maxsize=20000,
            lifetime=400,
            interval=0.01,
            invalidsrc=["TESTSAT 3"],
            invaliddst=["TESTSAT 3"],
        )
        last = 1.99
        for msg in tplan:
            self.assertIsInstance(msg, transmission_plan.Message)
            self.assertAlmostEqual(last + 0.01, msg.start_time)
            self.assertTrue(self._is_known_node(msg.source))
            self.assertTrue(self._is_known_node(msg.destination))
            self.assertAlmostEqual(msg.start_time + 400, msg.deadline)
            self.assertLessEqual(msg.size, 20000)
            self.assertGreaterEqual(msg.size, 20)
            last = msg.start_time
        self.assertAlmostEqual(9, last)

    def test_ordered(self):
        tplan = transmission_plan.generate(
            self.graph,
            starttime=2,
            stoptime=90,
            minsize=20,
            maxsize=20000,
            lifetime=400,
            interval=0.01,
            intervaldev=0.01,
            invalidsrc=["TESTSAT 3"],
            invaliddst=["TESTSAT 3"],
        )
        last = 2
        for msg in tplan:
            self.assertGreaterEqual(msg.start_time, last)
            last = msg.start_time
