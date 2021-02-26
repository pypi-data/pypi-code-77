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


def _get_test_fcp():
    c1_char = [
        contact_plan.ContactCharacteristics(
            0.0,
            9600.,
            1.5e-6,
            0.25,
        ),
        contact_plan.ContactCharacteristics(
            starting_at=1.75,
            bit_rate=1200.,
            bit_error_rate=1.0e-6,
            delay=0.20,
        ),
    ]
    c1 = contact_plan.Contact(
        "nodeA",
        "nodeB",
        1,
        2,
        c1_char,
    )
    c2_char = [
        contact_plan.ContactCharacteristics(
            0.0,
            1e6,
            0.0,
            0.0,
        ),
    ]
    c2 = contact_plan.Contact(
        tx_node="nodeA",
        rx_node="nodeC",
        start_time=1,
        end_time=5,
        characteristics=c2_char,
    )
    return [c1, c2]


def _get_test_pcp():
    c1_gen1_char = [
        contact_plan.PredictedContactCharacteristics(
            0.0,
            9600.,
            0.25,
        ),
        contact_plan.PredictedContactCharacteristics(
            starting_at=1.75,
            bit_rate=1200.,
            delay=0.20,
        ),
    ]
    c1_gen2_char = [
        contact_plan.PredictedContactCharacteristics(
            0.0,
            9600.,
            0.25,
        ),
        contact_plan.PredictedContactCharacteristics(
            starting_at=1.5,
            bit_rate=1200.,
            delay=0.20,
        ),
    ]
    c1_gen1 = contact_plan.PredictedContactGeneration(
        0.0,
        0.95,
        c1_gen1_char,
    )
    c1_gen2 = contact_plan.PredictedContactGeneration(
        valid_from=1.0,
        probability=1.0,
        characteristics=c1_gen2_char,
    )
    c1 = contact_plan.PredictedContact(
        "nodeA",
        "nodeB",
        1,
        2,
        [c1_gen1, c1_gen2],
    )
    c2_gen1_char = [
        contact_plan.PredictedContactCharacteristics(
            0.0,
            1e6,
            0.1,
        ),
    ]
    c2_gen1 = contact_plan.PredictedContactGeneration(
        0.0,
        1.0,
        c2_gen1_char,
    )
    c2_gen2_char = [
        contact_plan.PredictedContactCharacteristics(
            0.0,
            1e5,
            0.2,
        ),
    ]
    c2_gen2 = contact_plan.PredictedContactGeneration(
        0.1,
        1.0,
        c2_gen2_char,
    )
    c2 = contact_plan.PredictedContact(
        tx_node="nodeA",
        rx_node="nodeC",
        start_time=1,
        end_time=5,
        generations=[c2_gen1, c2_gen2],
    )
    return [c1, c2]


# Tests for the FCP contact with characteristics
class TestExtendedContact(unittest.TestCase):

    def test_characteristics_validations(self):
        contact_plan.ContactCharacteristics(0, 9600, 0.0, 0.25)
        with self.assertRaises(ValueError):
            contact_plan.ContactCharacteristics(0, -0.1, 1.5e-6, 0.25)
        with self.assertRaises(ValueError):
            contact_plan.ContactCharacteristics(0, 9600, -0.01, 0.25)
        with self.assertRaises(ValueError):
            contact_plan.ContactCharacteristics(0, 9600, 1.01, 0.25)
        with self.assertRaises(ValueError):
            contact_plan.ContactCharacteristics(0, 9600, 1.5e-6, -0.1)

    def test_contact_validations(self):
        char1 = contact_plan.ContactCharacteristics(0, 9600, 0.0, 0.25)
        contact_plan.Contact("nodeA", "nodeB", 0, 5, [char1])
        with self.assertRaises(ValueError):
            contact_plan.Contact("nodeA", "nodeB", -1, 5, [char1])
        with self.assertRaises(ValueError):
            contact_plan.Contact("nodeA", "nodeB", 1, 0.9, [char1])
        with self.assertRaises(ValueError):
            contact_plan.Contact("nodeA", "nodeB", 0, 5, [])
        char2 = contact_plan.ContactCharacteristics(1, 9600, 0.0, 0.25)
        with self.assertRaises(ValueError):
            contact_plan.Contact("nodeA", "nodeB", 0, 5, [char2])
        contact_plan.Contact("nodeA", "nodeB", 0, 5, [char1, char2])
        with self.assertRaises(ValueError):
            contact_plan.Contact("nodeA", "nodeB", 0, 5, [char1, char2, char1])

    def test_defaults(self):
        with self.assertRaises(TypeError):
            contact_plan.Contact()
        char = contact_plan.ContactCharacteristics()
        self.assertEqual(0.0, char.starting_at)
        self.assertEqual(0.0, char.bit_rate)
        self.assertEqual(0.0, char.bit_error_rate)
        self.assertEqual(0.0, char.delay)
        ct = contact_plan.Contact("nodeA", "nodeB", 0, 5)
        self.assertIsInstance(ct.characteristics, list)
        self.assertEqual(1, len(ct.characteristics))
        self.assertEqual(char, ct.characteristics[0])

    def test_to_simple(self):
        fcp = _get_test_fcp()
        sc1 = fcp[1].to_simple()
        self.assertEqual(
            contact_plan.SimpleContactTuple(
                "nodeA", "nodeC", 1, 5, 1e6, 0.0, 0.0
            ),
            sc1,
        )

    def test_get_characteristics(self):
        fcp = _get_test_fcp()
        with self.assertRaises(ValueError):
            self.assertEqual(1200, fcp[0].get_characteristics_at(-1).bit_rate)
        self.assertEqual(9600, fcp[0].get_characteristics_at(0).bit_rate)
        self.assertEqual(9600, fcp[0].get_characteristics_at(1.74999).bit_rate)
        self.assertEqual(1200, fcp[0].get_characteristics_at(1.75).bit_rate)
        self.assertEqual(1200, fcp[0].get_characteristics_at(1e7).bit_rate)


# Tests for the PCP contact with characteristics
class TestExtendedPredictedContact(unittest.TestCase):

    def test_characteristics_validations(self):
        contact_plan.PredictedContactCharacteristics(
            0, 9600, 0.25
        )
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactCharacteristics(
                0, -0.1, 0.25
            )
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactCharacteristics(
                0, 9600, -0.1
            )

    def test_generation_validations(self):
        char1 = contact_plan.PredictedContactCharacteristics(
            0, 9600, 0.25
        )
        char2 = contact_plan.PredictedContactCharacteristics(
            1, 9600, 0.25
        )
        contact_plan.PredictedContactGeneration(0.0, 1.0, [char1])
        contact_plan.PredictedContactGeneration(0.0, 1.0, [char1, char2])
        contact_plan.PredictedContactGeneration(0.0, 1.0, [char2])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactGeneration(0.0, -0.1, [char1])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactGeneration(0.0, 1.00001, [char1])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactGeneration(0.0, 1.0, [])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactGeneration(0.0, 1.0, ())
        with self.assertRaises(ValueError):
            contact_plan.PredictedContactGeneration(
                0.0, 1.0, [char1, char2, char1]
            )

    def test_contact_validations(self):
        char1 = contact_plan.PredictedContactCharacteristics(
            1, 9600, 0.25
        )
        char2 = contact_plan.PredictedContactCharacteristics(
            2, 9600, 0.25
        )
        gen1 = contact_plan.PredictedContactGeneration(
            0.0, 1.0, [char1, char2]
        )
        gen2 = contact_plan.PredictedContactGeneration(
            1.0, 1.0, [char1, char2]
        )
        gen3 = contact_plan.PredictedContactGeneration(
            0.0, 1.0, [char2]
        )
        contact_plan.PredictedContact("nodeA", "nodeC", 1, 5)
        contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, [])
        contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, [gen1])
        contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, [gen1, gen2])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, ())
        with self.assertRaises(ValueError):
            contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, [gen3])
        with self.assertRaises(ValueError):
            contact_plan.PredictedContact("nodeA", "nodeC", 1, 5, [gen2])

    def test_defaults(self):
        with self.assertRaises(TypeError):
            contact_plan.PredictedContact()
        char = contact_plan.PredictedContactCharacteristics()
        self.assertEqual(0.0, char.starting_at)
        self.assertEqual(0.0, char.bit_rate)
        self.assertEqual(0.0, char.delay)
        gen = contact_plan.PredictedContactGeneration()
        self.assertEqual(0.0, gen.valid_from)
        self.assertEqual(1.0, gen.probability)
        self.assertIsInstance(gen.characteristics, list)
        self.assertEqual(1, len(gen.characteristics))
        self.assertEqual(char, gen.characteristics[0])
        ct = contact_plan.PredictedContact("nodeA", "nodeB", 0, 5)
        self.assertIsInstance(ct.generations, list)
        self.assertEqual(1, len(ct.generations))
        self.assertEqual(gen, ct.generations[0])

    def test_to_simple(self):
        pcp = _get_test_pcp()
        self.assertEqual(
            contact_plan.SimplePredictedContactTuple(
                "nodeA", "nodeC", 1, 5, 1e6, 1.0, 0.1
            ),
            pcp[1].to_simple(),
        )

    def test_get_characteristics(self):
        pcp = _get_test_pcp()
        gen = pcp[0].get_generation_at(0)
        with self.assertRaises(ValueError):
            self.assertEqual(1200, gen.get_characteristics_at(-1).bit_rate)
        self.assertEqual(9600, gen.get_characteristics_at(0).bit_rate)
        self.assertEqual(9600, gen.get_characteristics_at(1.74999).bit_rate)
        self.assertEqual(1200, gen.get_characteristics_at(1.75).bit_rate)
        self.assertEqual(1200, gen.get_characteristics_at(1e7).bit_rate)

    def test_get_generation_at(self):
        pcp = _get_test_pcp()
        with self.assertRaises(ValueError):
            pcp[0].get_generation_at(-1)
        self.assertAlmostEqual(0.95, pcp[0].get_generation_at(0.0).probability)
        self.assertAlmostEqual(0.95, pcp[0].get_generation_at(0.9).probability)
        self.assertAlmostEqual(1.0, pcp[0].get_generation_at(1.0).probability)
        self.assertAlmostEqual(1.0, pcp[0].get_generation_at(1e6).probability)

    def test_get_volume(self):
        pcp = _get_test_pcp()
        c1 = pcp[0]
        c1gen1 = c1.get_generation_at(0.0)
        self.assertAlmostEqual(7500., c1gen1.get_volume(c1))
        self.assertAlmostEqual(7500., c1gen1.get_avg_bit_rate(c1))

    def test_get_delay(self):
        pcp = _get_test_pcp()
        c1gen1 = pcp[0].get_generation_at(0.0)
        c2gen1 = pcp[1].get_generation_at(0.0)
        self.assertAlmostEqual(0.2375, c1gen1.get_avg_delay(pcp[0]))
        self.assertAlmostEqual(0.1, c2gen1.get_avg_delay(pcp[1]))


# Tests for FCP <-> PCP conversion
class ExtendedFCPPCPConversionTest(unittest.TestCase):

    def test_bidirectional_conversion(self):
        # No information from the FCP should get lost
        fcp = _get_test_fcp()
        pcp = contact_plan.fcp_to_pcp(fcp)
        fcp2 = contact_plan.pcp_to_fcp(pcp, False, 0)
        self.assertEqual(len(fcp), len(fcp2))
        for i in range(len(fcp)):
            self.assertEqual(fcp[i].start_time, fcp2[i].start_time)
            self.assertEqual(fcp[i].end_time, fcp2[i].end_time)
            self.assertEqual(fcp[i].tx_node, fcp2[i].tx_node)
            self.assertEqual(fcp[i].rx_node, fcp2[i].rx_node)
            self.assertEqual(
                len(fcp[i].characteristics),
                len(fcp2[i].characteristics)
            )
            for j in range(len(fcp[i].characteristics)):
                self.assertEqual(
                    fcp[i].characteristics[j].starting_at,
                    fcp2[i].characteristics[j].starting_at
                )
                self.assertEqual(
                    fcp[i].characteristics[j].bit_rate,
                    fcp2[i].characteristics[j].bit_rate
                )
                self.assertEqual(
                    fcp[i].characteristics[j].delay,
                    fcp2[i].characteristics[j].delay
                )
                self.assertEqual(
                    0.0,
                    fcp2[i].characteristics[j].bit_error_rate
                )


class SerializationTest(unittest.TestCase):

    def test_serialize_fcp(self):
        fcp = _get_test_fcp()
        lst = [fc.to_list() for fc in fcp]
        fcp2 = [contact_plan.Contact.from_list(l) for l in lst]
        self.assertEqual(fcp, fcp2)

    def test_serialize_pcp(self):
        pcp = _get_test_pcp()
        lst = [fc.to_list() for fc in pcp]
        pcp2 = [contact_plan.PredictedContact.from_list(l) for l in lst]
        self.assertEqual(pcp, pcp2)
