#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest
import json

from tvgutil import contact_plan, tvg


# Tests for the FCP contact
class TestTVG(unittest.TestCase):

    BASIC_PCP_TUPLES_PROB = [
        ("bs1", "TESTSAT 1", 0, 4, 4, 0.95, 0.01),
        ("TESTSAT 1", "bs1", 0, 4, 12, 0.95, 0.01),
        ("bs1", "TESTSAT 2", 1, 7, 9, 1.0, 0.1),
        ("TESTSAT 2", "bs1", 1, 7, 9, 1.0, 0.1),
        ("bs5", "TESTSAT 3", 8, 10, 2, 0.2, 0.1),
        ("TESTSAT 3", "bs5", 8, 10, 2, 0.2, 0.1),
    ]

    BASIC_FCP_TUPLES_PROB = [
        ("bs1", "TESTSAT 1", 0, 4, 1, 0.05, 0.01),
        ("TESTSAT 1", "bs1", 0, 4, 3, 0.05, 0.01),
        ("bs1", "TESTSAT 2", 1, 7, 1.5, 0.0, 0.1),
        ("TESTSAT 2", "bs1", 1, 7, 1.5, 0.0, 0.1),
        ("bs5", "TESTSAT 3", 8, 10, 1, 0.8, 0.1),
        ("TESTSAT 3", "bs5", 8, 10, 1, 0.8, 0.1),
    ]

    def setUp(self):
        self.pcp_prob = [
            contact_plan.PredictedContact.simple(*t)
            for t in self.BASIC_PCP_TUPLES_PROB
        ]
        self.fcp_prob = [
            contact_plan.Contact.simple(*t)
            for t in self.BASIC_FCP_TUPLES_PROB
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
        PROPS = ("tx_node", "rx_node", "start_time", "end_time")
        self.assertEqual(len(cl1), len(cl2))
        for c1 in cl1:
            for c2 in cl2:
                if all(getattr(c1, p) == getattr(c2, p) for p in PROPS):
                    self.assertEqual(c1, c2)

    def test_from_pcp_and_back(self):
        graph = tvg.from_contact_plan(self.pcp_prob)
        self.assertEqual(contact_plan.PredictedContact, graph.contact_type)
        for t in self.BASIC_PCP_TUPLES_PROB:
            self.assertIn(t[0], graph.vertices)
            self.assertIn(t[1], graph.vertices)
            self.assertIn(t[1], graph.vertices[t[0]])
            self.assertIn(t[0], graph.vertices[t[1]])
        for nodes, clist in graph.edges.items():
            n1, n2 = nodes
            for c in clist:
                self.assertIn(c, self.pcp_prob)
                self.assertEqual(n1, c.tx_node)
                self.assertEqual(n2, c.rx_node)
            found = False
            for c in self.pcp_prob:
                if c.tx_node == n1 and c.rx_node == n2:
                    found = True
                    break
            self.assertTrue(found, "Directed edge not part of PCP: {}".format(
                (n1, n2)
            ))
        pcp = tvg.to_contact_plan(graph)
        self._assert_equal_clist(self.pcp_prob, pcp)

    def test_from_fcp_and_back(self):
        graph = tvg.from_contact_plan(self.fcp_prob,
                                      contact_type=contact_plan.Contact)
        self.assertEqual(contact_plan.Contact, graph.contact_type)
        for t in self.BASIC_FCP_TUPLES_PROB:
            self.assertIn(t[0], graph.vertices)
            self.assertIn(t[1], graph.vertices)
            self.assertIn(t[1], graph.vertices[t[0]])
            self.assertIn(t[0], graph.vertices[t[1]])
        for nodes, clist in graph.edges.items():
            n1, n2 = nodes
            for c in clist:
                self.assertIn(c, self.fcp_prob)
                self.assertEqual(n1, c.tx_node)
                self.assertEqual(n2, c.rx_node)
        fcp = tvg.to_contact_plan(graph)
        self._assert_equal_clist(self.fcp_prob, fcp)

    def test_serialize(self):
        for plan, type_ in ((self.pcp_prob, contact_plan.PredictedContact),
                            (self.fcp_prob, contact_plan.Contact)):
            graph = tvg.from_contact_plan(plan, contact_type=type_)
            graph2 = tvg.from_serializable(
                json.loads(json.dumps(
                    tvg.to_serializable(graph)
                ))
            )
            self.assertEqual(graph.contact_type, graph2.contact_type)
            for v, vout in graph.vertices.items():
                self.assertIn(v, graph2.vertices)
                for v2 in vout:
                    self.assertIn(v2, graph2.vertices[v])
            for nodes, clist in graph.edges.items():
                self.assertIn(nodes, graph2.edges)
                self._assert_equal_clist(clist, graph2.edges[nodes])
