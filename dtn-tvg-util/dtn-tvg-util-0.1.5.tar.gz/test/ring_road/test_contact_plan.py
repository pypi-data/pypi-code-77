#!/usr/bin/env python
# encoding: utf-8

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import unittest

from tvgutil.ring_road.scenario import filter_satdb
from tvgutil.ring_road.contact_plan import (
    get_rr0_contact_tuples,
    get_isl_contact_tuples,
    get_hot_spot_contact_tuples,
)

START_TIMESTAMP = 1531124341
DURATION = 21600
MIN_ELEVATION = 5

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
SAT_LIST = filter_satdb(3, TLE_FILE, 15.2)

GS_LIST = [
    {
        "id": "gs0",
        "lat": 12.389475254905022,
        "lon": -121.52801095712852,
        # should not be needed for basic tuple list generation
        "hot": False,
    },
    {
        "id": "gs1",
        "lat": 79.21599833493417,
        "lon": 3.3633351176119106,
        "hot": True,
    },
    {
        "id": "gs2",
        "lat": -37.43129740203971,
        "lon": -64.108127819292,
        "hot": True,
    },
    {
        "id": "gs3",
        "lat": -73.55543545294637,
        "lon": 8.589945131313158,
        "hot": True,
    },
    {
        "id": "gs4",
        "lat": 75.18135841631366,
        "lon": -2.5592890896559197,
    },
]

# contact tuples have been obtained using a linear time loop and pyephem,
# checking every second in the contact interval whether there is a contact,
# i.e. whether the computed elevation is above the given minimum elevation
# of 5 degrees
RR0_TUPLES = [
    (a, b, s + START_TIMESTAMP, e + START_TIMESTAMP)
    for a, b, s, e in [
        ("gs3", "OPTICUBE 04", 1529.0, 2160.0),
        ("gs0", "VELOX 2", 2022.0, 2641.0),
        ("gs1", "SEEDS II (CO-66)", 2142.0, 2777.0),
        ("gs4", "SEEDS II (CO-66)", 2206.0, 2841.0),
        ("gs2", "SEEDS II (CO-66)", 4181.0, 4696.0),
        ("gs1", "OPTICUBE 04", 4880.0, 5372.0),
        ("gs4", "OPTICUBE 04", 4975.0, 5386.0),
        ("gs3", "OPTICUBE 04", 7278.0, 7887.0),
        ("gs1", "SEEDS II (CO-66)", 7888.0, 8518.0),
        ("gs4", "SEEDS II (CO-66)", 7947.0, 8559.0),
        ("gs0", "VELOX 2", 8131.0, 8748.0),
        ("gs2", "SEEDS II (CO-66)", 9868.0, 10459.0),
        ("gs1", "OPTICUBE 04", 10627.0, 11198.0),
        ("gs4", "OPTICUBE 04", 10701.0, 11256.0),
        ("gs3", "OPTICUBE 04", 13112.0, 13612.0),
        ("gs1", "SEEDS II (CO-66)", 13622.0, 14246.0),
        ("gs4", "SEEDS II (CO-66)", 13667.0, 14257.0),
        ("gs0", "VELOX 2", 14235.0, 14858.0),
        ("gs1", "OPTICUBE 04", 16366.0, 16972.0),
        ("gs4", "OPTICUBE 04", 16432.0, 17040.0),
        ("gs3", "OPTICUBE 04", 19078.0, 19300.0),
        ("gs1", "SEEDS II (CO-66)", 19350.0, 19977.0),
        ("gs4", "SEEDS II (CO-66)", 19368.0, 19961.0),
        ("gs0", "VELOX 2", 20341.0, 20954.0),
        ("gs0", "SEEDS II (CO-66)", 20734.0, 21272.0),
    ]
]

RRI_TUPLES = [
    ("gs1", "gs2", START_TIMESTAMP + 0.0, START_TIMESTAMP + DURATION),
    ("gs1", "gs3", START_TIMESTAMP + 0.0, START_TIMESTAMP + DURATION),
    ("gs2", "gs3", START_TIMESTAMP + 0.0, START_TIMESTAMP + DURATION),
]

# contact tuples have been obtained using a linear time loop and pyephem,
# checking every second in the contact interval whether the distance between
# the satellites is below the minum range
RRS_TUPLES_500KM = [
    ('SEEDS II (CO-66)', 'VELOX 2', 1531125128, 1531125162),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531127979, 1531128066),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531130852, 1531130950),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531133739, 1531133820),
]
RRS_TUPLES_2500KM = [
    ('SEEDS II (CO-66)', 'VELOX 2', 1531124900, 1531125389),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531127774, 1531128271),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531130652, 1531131151),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531133531, 1531134028),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531136414, 1531136901),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531139299, 1531139773),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531142188, 1531142642),
    ('SEEDS II (CO-66)', 'VELOX 2', 1531145078, 1531145507),
]

# maximum delta for SGP4-predicted contacts, in seconds
MAX_DELTA_SGP4 = 10.0


class RingRoadContactPlanGenerationTest(unittest.TestCase):

    def _assert_tuple_list_equal(self, expected, actual, nodes_unordered=False,
                                 max_delta=MAX_DELTA_SGP4):
        for actual_node1, actual_node2, actual_start, actual_end in actual:
            found = False
            for exp_node1, exp_node2, exp_start, exp_end in expected:
                if ((exp_node1 == actual_node1 and exp_node2 == actual_node2)
                        or (nodes_unordered and exp_node1 == actual_node2 and
                            exp_node2 == actual_node1)):
                    if (abs(exp_start - actual_start) < max_delta and
                            abs(exp_end - actual_end) < max_delta):
                        found = True
                        break
            self.assertTrue(found, "Contact {} not found in list".format(
                (actual_node1, actual_node2, actual_start, actual_end)
            ))
        self.assertEqual(len(expected), len(actual))

    def test_get_rr0_contact_tuples(self):
        # default settings should yield all contacts almost exactly
        tuples = get_rr0_contact_tuples(
            SAT_LIST, GS_LIST, START_TIMESTAMP, DURATION,
            min_elevation=MIN_ELEVATION,
        )
        self._assert_tuple_list_equal(RR0_TUPLES, tuples)

    def test_get_isl_contact_tuples(self):
        # default settings should yield all contacts almost exactly
        tuples = get_isl_contact_tuples(
            SAT_LIST, START_TIMESTAMP, DURATION, 500.0,
        )
        self._assert_tuple_list_equal(
            RRS_TUPLES_500KM, tuples,
            nodes_unordered=True,
        )
        # test different range
        tuples = get_isl_contact_tuples(
            SAT_LIST, START_TIMESTAMP, DURATION, 2500.0,
        )
        self._assert_tuple_list_equal(
            RRS_TUPLES_2500KM, tuples,
            nodes_unordered=True,
        )

    def test_get_hot_spot_contact_tuples(self):
        tuples = get_hot_spot_contact_tuples(
            GS_LIST, START_TIMESTAMP, DURATION,
        )
        self._assert_tuple_list_equal(
            RRI_TUPLES,
            tuples,
            nodes_unordered=True,
            max_delta=1e-6,
        )
