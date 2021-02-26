#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest

from tvgutil.ring_road.scenario import filter_satdb, place_gs

TLE_FILE = """
OPTICUBE 04
1 41851U 16067D   18189.78557037  .00000398  00000-0  40140-4 0  9991
2 41851  97.9236 278.1823 0010445  94.3995 265.8420 14.96677984 90323
SEEDS II (CO-66)
1 32791U 08021J   18190.08814034  .00000180  00000-0  23773-4 0  9995
2 32791  97.5350 206.6283 0012099 310.4422  49.5741 14.90581326552772
VELOX 2
1 41171U 15077F   18189.76717668  .00001185  00000-0  30509-4 0  9995
2 41171  14.9906 239.2385 0008985 300.1038  59.8391 15.10691346141504
"""

START_TIMESTAMP = 1531124341

SATLIST_15_0ROT = ("OPTICUBE 04", "SEEDS II (CO-66)")
SATLIST_15_2ROT = ("OPTICUBE 04", "SEEDS II (CO-66)", "VELOX 2")
SATLIST_ALL = SATLIST_15_2ROT

TLE1_REGEX = r"^1 [0-9]+U [0-9]+\w\s+[0-9\s\.\-]+$"
TLE2_REGEX = r"^2 [0-9]+  [0-9\s\.\-]+$"


class RingRoadScenarioGenerationTest(unittest.TestCase):

    def __init__(self, methodName="runTest"):
        super(RingRoadScenarioGenerationTest, self).__init__(methodName)
        if not hasattr(self, "assertRegex"):
            self.assertRegex = self.assertRegexpMatches

    def test_filter_satdb_format(self):
        satdb = filter_satdb(1, TLE_FILE, 15)
        self.assertEqual(1, len(satdb))
        self.assertIn("id", satdb[0])
        self.assertIn("tle", satdb[0])
        self.assertIn(satdb[0]["id"], SATLIST_ALL)
        self.assertEqual(2, len(satdb[0]["tle"]))
        self.assertEqual(69, len(satdb[0]["tle"][0]))
        self.assertEqual(69, len(satdb[0]["tle"][1]))
        self.assertRegex(satdb[0]["tle"][0], TLE1_REGEX)
        self.assertRegex(satdb[0]["tle"][1], TLE2_REGEX)

    def test_filter_satdb_count(self):
        satdb = filter_satdb(2, TLE_FILE, 15)
        self.assertEqual(2, len(satdb))
        with self.assertRaises(ValueError):
            satdb = filter_satdb(3, TLE_FILE, 15)
        satdb = filter_satdb(2, TLE_FILE, 15)
        satlist_15_0_fset = frozenset(SATLIST_15_0ROT)
        ids = {e["id"] for e in satdb}
        self.assertEqual(0, len(satlist_15_0_fset - frozenset(ids)))
        satdb = filter_satdb(3, TLE_FILE, 15.2)
        satlist_15_2_fset = frozenset(SATLIST_15_0ROT)
        ids = {e["id"] for e in satdb}
        self.assertEqual(0, len(satlist_15_2_fset - frozenset(ids)))

    def test_place_gs_random(self):
        gslist = place_gs(0, gs_list=None, hotspot_count=0, reset_ids=True)
        self.assertEqual(0, len(gslist))
        gslist = place_gs(1, gs_list=None, hotspot_count=0, reset_ids=True)
        self.assertEqual(1, len(gslist))
        self.assertEqual("gs0", gslist[0]["id"])
        gslist = place_gs(5, gs_list=None, hotspot_count=0, reset_ids=True)
        self.assertEqual(5, len(gslist))
        for gs in gslist:
            self.assertEqual(3, len(gs["id"]))
            self.assertEqual("gs", gs["id"][0:2])
            self.assertEqual(False, gs["hot"])
        gslist = place_gs(100, gs_list=None, hotspot_count=0, reset_ids=True)
        self.assertEqual(100, len(gslist))
        for gs in gslist:
            self.assertEqual(4, len(gs["id"]))
            self.assertEqual("gs", gs["id"][0:2])
            self.assertEqual(False, gs["hot"])
        gslist = place_gs(101, gs_list=None, hotspot_count=0, reset_ids=True)
        self.assertEqual(101, len(gslist))
        for gs in gslist:
            self.assertEqual(5, len(gs["id"]))
            self.assertEqual("gs", gs["id"][0:2])
            self.assertEqual(False, gs["hot"])
        gslist = place_gs(1001, gs_list=None, hotspot_count=10, reset_ids=True)
        self.assertEqual(1001, len(gslist))
        hotcount = 0
        for gs in gslist:
            self.assertEqual(6, len(gs["id"]))
            self.assertEqual("gs", gs["id"][0:2])
            self.assertGreaterEqual(1000, int(gs["id"][2:]))
            self.assertLessEqual(0, int(gs["id"][2:]))
            if gs["hot"]:
                hotcount += 1
            self.assertGreaterEqual(90.0, gs["lat"])
            self.assertLessEqual(-90.0, gs["lat"])
            self.assertGreaterEqual(180.0, gs["lon"])
            self.assertLessEqual(-180.0, gs["lon"])
        self.assertEqual(10, hotcount)

    def test_place_gs_from_list(self):
        TEST_GS_LIST = [
            {"id": "mygs12", "lat": 1, "lon": 2, "hot": True},
            {"id": "mygs13", "lat": 1, "lon": 2, "hot": True},
        ]
        with self.assertRaises(ValueError):
            place_gs(3, gs_list=TEST_GS_LIST)
        gslist = place_gs(2, gs_list=TEST_GS_LIST,
                          hotspot_count=0, reset_ids=True)
        for gs in gslist:
            self.assertEqual(3, len(gs["id"]))
            self.assertEqual("gs", gs["id"][0:2])
            self.assertGreaterEqual(1, int(gs["id"][2:]))
            self.assertLessEqual(0, int(gs["id"][2:]))
            self.assertEqual(False, gs["hot"])
            self.assertEqual(1, gs["lat"])
            self.assertEqual(2, gs["lon"])
        gslist = place_gs(2, gs_list=TEST_GS_LIST,
                          hotspot_count=2, reset_ids=False)
        for gs in gslist:
            self.assertEqual(6, len(gs["id"]))
            self.assertEqual("mygs", gs["id"][0:4])
            self.assertGreaterEqual(13, int(gs["id"][4:]))
            self.assertLessEqual(12, int(gs["id"][4:]))
            self.assertEqual(True, gs["hot"])
            self.assertEqual(1, gs["lat"])
            self.assertEqual(2, gs["lon"])
