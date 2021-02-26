#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest
import copy

from tvgutil import contact_plan


# Tests for the FCP contact
class TestContact(unittest.TestCase):

    def test_tuple_conversion(self):
        t = ("nodeA", "nodeB", 1, 2, 9600, 1e-6, 0.001)
        c = contact_plan.Contact.simple(*t)
        self.assertEqual(t, c.to_simple())
        tx_node, rx_node, start, end, bitrate, ber, delay = c.to_simple()

    def test_defaults(self):
        c = contact_plan.Contact.simple(
            "nodeA", "nodeB", 1, 2, 9600,
        ).to_simple()
        self.assertAlmostEqual(0.0, c.bit_error_rate)
        self.assertAlmostEqual(0.0, c.delay)


# Tests for the PCP contact
class TestPredictedContact(unittest.TestCase):

    def test_creation(self):
        t_in = ("nodeA", "nodeB", 1, 2, 1000, 0.95, 0.001)
        c = contact_plan.PredictedContact.simple(*t_in)
        t_out = ("nodeA", "nodeB", 1, 2, 1000, 0.95, 0.001)
        self.assertEqual(t_out, c.to_simple())

    def test_defaults(self):
        c = contact_plan.PredictedContact.simple("nodeA", "nodeB", 1, 2, 1000)
        t_out = ("nodeA", "nodeB", 1, 2, 1000, 1.0, 0.0)
        self.assertEqual(t_out, c.to_simple())

    def test_equality(self):
        t = ("nodeA", "nodeB", 1, 2, 1000, 0.95, 0.0)
        c1 = contact_plan.PredictedContact.simple(*t)
        c2 = contact_plan.PredictedContact.simple(*t)
        self.assertTrue(c1 == c2)

    def test_inequality(self):
        c_list = [
            ("nodeA", "nodeB", 1, 2, 1000, 0.95, 0.001),
            ("nodeB", "nodeB", 1, 2, 1000, 0.95, 0.001),
            ("nodeA", "nodeA", 1, 2, 1000, 0.95, 0.001),
            ("nodeA", "nodeB", 2, 2, 1000, 0.95, 0.001),
            ("nodeA", "nodeB", 1, 3, 1000, 0.95, 0.001),
            ("nodeA", "nodeB", 1, 2, 2000, 0.95, 0.001),
            ("nodeA", "nodeB", 1, 2, 10000, 0.95, 0.001),
            ("nodeA", "nodeB", 1, 2, 10000, 0.95, 0.002),
            ("nodeA", "nodeB", 1, 2, 1000, 0.95, 0.001),
            ("nodeA", "nodeB", 1, 2, 1000, 0.99, 0.001),
        ]
        for c1 in c_list:
            i1 = contact_plan.PredictedContact.simple(*c1)
            for c2 in c_list:
                if c1 == c2:
                    continue
                i2 = contact_plan.PredictedContact.simple(*c2)
                self.assertTrue(i1 != i2)


# Tests for FCP <-> PCP conversion
class FCPPCPConversionTest(unittest.TestCase):

    # a message size of 1 makes the BER be equal to (1 - probability)
    MESSAGE_SIZE_BITS = 1

    BASIC_FCP_TUPLES = [
        ("bs1", "TESTSAT 1", 0, 4, 1, 0.0),
        ("TESTSAT 1", "bs1", 0, 4, 3, 0.0),
        ("bs1", "TESTSAT 2", 1, 7, 1.5, 0.0),
        ("bs5", "TESTSAT 3", 8, 10, 1, 0.0),
    ]

    BASIC_PCP_TUPLES = [
        ("bs1", "TESTSAT 1", 0, 4, 1, 1.0),
        ("TESTSAT 1", "bs1", 0, 4, 3, 1.0),
        ("bs1", "TESTSAT 2", 1, 7, 1.5, 1.0),
        ("bs5", "TESTSAT 3", 8, 10, 1, 1.0),
    ]

    BASIC_PCP_TUPLES_PROB = [
        ("bs1", "TESTSAT 1", 0, 4, 1, 1.0),
        ("TESTSAT 1", "bs1", 0, 4, 3, 0.2),
        ("bs1", "TESTSAT 2", 1, 7, 1.5, 0.0),
        ("bs5", "TESTSAT 3", 8, 10, 1, 1.0),
    ]

    def setUp(self):
        self.pcp = [
            contact_plan.PredictedContact.simple(*t)
            for t in self.BASIC_PCP_TUPLES
        ]
        self.pcp_prob = [
            contact_plan.PredictedContact.simple(*t)
            for t in self.BASIC_PCP_TUPLES_PROB
        ]
        self.fcp = [
            contact_plan.Contact.simple(*t)
            for t in self.BASIC_FCP_TUPLES
        ]
        self.addTypeEqualityFunc(contact_plan.Contact,
                                 self._contact_almost_equal)
        self.addTypeEqualityFunc(contact_plan.PredictedContact,
                                 self._contact_almost_equal)

    def _contact_almost_equal(self, c1, c2, msg=None):
        c1 = c1.to_simple()
        c2 = c2.to_simple()
        if not all(
                    abs(x - y) < 1e-7
                    for x, y in zip(tuple(list(c1)[2:]), tuple(list(c2)[2:]))
                    if not isinstance(x, tuple)
                ):
            raise self.failureException(
                msg or "Contacts differ: {}, {}".format(c1, c2)
            )

    def _assert_equal_clist(self, cl1, cl2):
        self.assertEqual(len(cl1), len(cl2))
        for i in range(len(cl1)):
            self.assertEqual(cl1[i], cl2[i])

    def test_pcp_to_fcp(self):
        fcp = contact_plan.pcp_to_fcp(self.pcp)
        self._assert_equal_clist(self.fcp, fcp)
        fcp = contact_plan.pcp_to_fcp(
            self.pcp_prob,
            remove_probabilistic=True,
        )
        self.assertLess(len(fcp), len(self.pcp_prob))

    def test_fcp_to_pcp(self):
        pcp = contact_plan.fcp_to_pcp(self.fcp)
        self._assert_equal_clist(self.pcp, pcp)

    def test_bidirectional_conversion(self):
        fcp = contact_plan.pcp_to_fcp(self.pcp)
        pcp = contact_plan.fcp_to_pcp(fcp)
        self._assert_equal_clist(self.pcp, pcp)
        fcp2 = contact_plan.pcp_to_fcp(pcp)
        self._assert_equal_clist(self.fcp, fcp2)


# Tests for converting legacy contact plans
class TestLegacyPCPConversion(unittest.TestCase):

    LEGACY_TEST_PLAN = [
        {
            "mBaseStation": "bs1",
            "mSatellite": "TESTSAT 1",
            "mContactBegin": 0,
            "mContactEnd": 4,
        },
        # Some other contact
        {
            "mBaseStation": "bs1",
            "mSatellite": "TESTSAT 2",
            "mContactBegin": 1,
            "mContactEnd": 7,
        },
        # Duplicate of first
        {
            "mBaseStation": "bs1",
            "mSatellite": "TESTSAT 1",
            "mContactBegin": 0,
            "mContactEnd": 4,
        },
        # Reverse of first, using other scheme
        {
            "node2": "bs1",
            "node1": "TESTSAT 1",
            "start": 0,
            "end": 4,
        },
        # Reverse of first, using other scheme
        {
            "node2": "bs1",
            "node1": "TESTSAT 1",
            "start": 0,
            "end": 4,
        },
        # Some further contact
        {
            "node1": "bs5",
            "node2": "TESTSAT 3",
            "start": 8,
            "end": 10,
        },
    ]

    LEGACY_TEST_PLAN_PCP_TUPLES_BIDIRECTIONAL = [
        ("bs1", "TESTSAT 1", 0, 4),
        ("TESTSAT 1", "bs1", 0, 4),
        ("bs1", "TESTSAT 2", 1, 7),
        ("TESTSAT 2", "bs1", 1, 7),
        ("bs5", "TESTSAT 3", 8, 10),
        ("TESTSAT 3", "bs5", 8, 10),
    ]

    LEGACY_TEST_PLAN_PCP_TUPLES_UNIDIRECTIONAL = [
        ("bs1", "TESTSAT 1", 0, 4),
        ("TESTSAT 1", "bs1", 0, 4),
        ("bs1", "TESTSAT 2", 1, 7),
        ("bs5", "TESTSAT 3", 8, 10),
    ]

    def _contact_interval_in_plan(self, plan, contact):
        PROPS = ("tx_node", "rx_node", "start_time", "end_time")
        for c in plan:
            if all(getattr(c, prop) == getattr(contact, prop)
                   for prop in PROPS):
                return True
        return False

    def setUp(self):
        self.pcp = [
            contact_plan.PredictedContact.simple(*e)
            for e in self.LEGACY_TEST_PLAN_PCP_TUPLES_BIDIRECTIONAL
        ]
        self.pcp_unidirectional = [
            contact_plan.PredictedContact.simple(*e)
            for e in self.LEGACY_TEST_PLAN_PCP_TUPLES_UNIDIRECTIONAL
        ]

    def test_legacy_to_pcp_simple(self):
        pcp = contact_plan.legacy_to_pcp(self.LEGACY_TEST_PLAN)
        self.assertEqual(len(self.pcp), len(pcp))
        for c in pcp:
            sc = c.to_simple()
            self.assertTrue(self._contact_interval_in_plan(self.pcp, c),
                            "Contact {} not expected".format(c))
            self.assertAlmostEqual(0.0, sc.bit_rate)
            self.assertAlmostEqual(1.0, sc.probability)
            self.assertAlmostEqual(0.0, sc.delay)

    def test_legacy_to_pcp_bit_rate(self):
        pcp = contact_plan.legacy_to_pcp(self.LEGACY_TEST_PLAN, bit_rate=1.0)
        self.assertEqual(len(self.pcp), len(pcp))
        for c in pcp:
            sc = c.to_simple()
            self.assertTrue(self._contact_interval_in_plan(self.pcp, c),
                            "Contact {} not expected".format(c))
            self.assertAlmostEqual(1.0, sc.bit_rate)
            self.assertAlmostEqual(1.0, sc.probability)

    def test_legacy_to_pcp_capacity(self):
        test_plan = copy.deepcopy(self.LEGACY_TEST_PLAN)
        for contact in test_plan:
            contact["capacity"] = 42.0
        pcp = contact_plan.legacy_to_pcp(test_plan)
        self.assertEqual(len(self.pcp), len(pcp))
        for c in pcp:
            sc = c.to_simple()
            self.assertTrue(self._contact_interval_in_plan(self.pcp, c),
                            "Contact {} not expected".format(c))
            self.assertAlmostEqual(
                42.0 / (sc.end_time - sc.start_time),
                sc.bit_rate
            )
            self.assertAlmostEqual(1.0, sc.probability)

    def test_legacy_to_pcp_probability(self):
        test_plan = copy.deepcopy(self.LEGACY_TEST_PLAN)
        for contact in test_plan:
            contact["prob"] = 0.5
        pcp = contact_plan.legacy_to_pcp(test_plan)
        self.assertEqual(len(self.pcp), len(pcp))
        for c in pcp:
            sc = c.to_simple()
            self.assertTrue(self._contact_interval_in_plan(self.pcp, c),
                            "Contact {} not expected".format(c))
            self.assertAlmostEqual(0.5, sc.probability)

    def test_legacy_to_pcp_unidirectional(self):
        pcp = contact_plan.legacy_to_pcp(self.LEGACY_TEST_PLAN,
                                         unidirectional=True)
        self.assertEqual(len(self.pcp_unidirectional), len(pcp))
        for c in pcp:
            sc = c.to_simple()
            self.assertTrue(
                self._contact_interval_in_plan(self.pcp_unidirectional, c),
                "Contact {} not expected".format(c)
            )
            self.assertAlmostEqual(0.0, sc.bit_rate)
            self.assertAlmostEqual(1.0, sc.probability)


class TestContactTupleConversion(unittest.TestCase):

    TUPLES = [
        ("A", "B", 1.0, 3.0),
        ("B", "C", 5.3, 7.3),
        ("A", "B", 5.3, 7.3),
        ("D", "E", 9.5, 11.5),
        ("F", "E", 9.5, 11.5),
    ]

    def setUp(self):
        self.addTypeEqualityFunc(contact_plan.Contact,
                                 self._contact_almost_equal)
        self.addTypeEqualityFunc(contact_plan.PredictedContact,
                                 self._contact_almost_equal)

    def _contact_almost_equal(self, c1, c2, msg=None):
        c1 = c1.to_simple()
        c2 = c2.to_simple()
        if not all(
                    abs(x - y) < 1e-7
                    for x, y in zip(tuple(list(c1)[2:]), tuple(list(c2)[2:]))
                    if not isinstance(x, tuple)
                ):
            raise self.failureException(
                msg or "Contacts differ: {}, {}".format(c1, c2)
            )

    def _assert_equal_clist(self, cl1, cl2):
        PROPS = ("tx_node", "rx_node", "start_time", "end_time")
        self.assertEqual(len(cl1), len(cl2))
        for c1 in cl1:
            for c2 in cl2:
                if all(getattr(c1, p) == getattr(c2, p) for p in PROPS):
                    self.assertEqual(c1, c2)

    def _assert_within(self, min_, max_, value):
        self.assertGreaterEqual(value, min_)
        self.assertLessEqual(value, max_)

    def test_contact_tuples_to_pcp_fcp(self):
        OFF = 1.0
        PCP = [
            contact_plan.PredictedContact.simple(tx, rx, s - OFF, e - OFF,
                                                 bit_rate=1.0)
            for tx, rx, s, e in self.TUPLES
        ]
        PCP += [
            contact_plan.PredictedContact.simple(tx, rx, s - OFF, e - OFF,
                                                 bit_rate=2.0)
            for rx, tx, s, e in self.TUPLES
        ]
        pcp = contact_plan.contact_tuples_to_pcp(
            self.TUPLES,
            time_offset=OFF,
            uplink_rate=1.0,
            downlink_rate=2.0,
        )
        self._assert_equal_clist(PCP, pcp)
        fcp = contact_plan.contact_tuples_to_fcp(
            self.TUPLES,
            time_offset=OFF,
            uplink_rate=1.0,
            downlink_rate=2.0,
        )
        pcp2 = contact_plan.fcp_to_pcp(fcp)
        self._assert_equal_clist(pcp, pcp2)

    def test_contact_tuples_to_pcp_prob(self):
        OFF = 1.0
        pcp = contact_plan.contact_tuples_to_pcp(
            self.TUPLES,
            time_offset=OFF,
            uplink_rate=1.0,
            downlink_rate=2.0,
            prob_min=0.5,
            prob_max=1.0,
            symmetric_prob=False,
        )
        node_pairs = {}
        diff_found = False
        for c in pcp:
            sc = c.to_simple()
            pair = (c.tx_node, c.rx_node)
            if pair in node_pairs:
                if node_pairs[pair] != sc.probability:
                    diff_found = True
            else:
                node_pairs[pair] = sc.probability
            self._assert_within(0.5, 1.0, sc.probability)
        self.assertTrue(diff_found)
        pcp = contact_plan.contact_tuples_to_pcp(
            self.TUPLES,
            time_offset=OFF,
            uplink_rate=1.0,
            downlink_rate=2.0,
            prob_min=0.5,
            prob_max=1.0,
            symmetric_prob=True,
        )
        contact_pairs = {}
        for c in pcp:
            sc = c.to_simple()
            pair = (c.tx_node, c.rx_node, c.start_time, c.end_time)
            pair_reverse = (c.rx_node, c.tx_node, c.start_time, c.end_time)
            if pair in contact_pairs:
                self.assertAlmostEqual(contact_pairs[pair], sc.probability)
            else:
                contact_pairs[pair_reverse] = sc.probability
            self._assert_within(0.5, 1.0, sc.probability)

    def test_back_conversion(self):
        OFF = 1.0
        pcp = contact_plan.contact_tuples_to_pcp(
            self.TUPLES,
            time_offset=OFF,
            uplink_rate=1.0,
            downlink_rate=2.0,
            prob_min=0.5,
            prob_max=1.0,
            symmetric_prob=False,
        )
        tuples = contact_plan.contact_plan_to_contact_tuples(pcp, OFF)
        self.assertEqual(len(pcp) / 2, len(tuples))
        self.assertEqual(len(self.TUPLES), len(tuples))
        for n1, n2, s, e in self.TUPLES:
            found = False
            for g_n1, g_n2, g_s, g_e in tuples:
                if (abs(s - g_s) < 1e-6 and abs(e - g_e) < 1e-6 and
                        (n1 == g_n1 or n1 == g_n2) and
                        (n2 == g_n1 or n2 == g_n2)):
                    found = True
            self.assertTrue(found)
