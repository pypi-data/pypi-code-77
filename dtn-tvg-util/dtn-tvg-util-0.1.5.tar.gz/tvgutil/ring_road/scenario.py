#!/usr/bin/env python
# encoding: utf-8

"""
Provides methods to create a Ring Road scenario description, consisting of a
list of satellites (including their TLE data for orbit predision using SGP4),
and a list of ground stations including their position(s).
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import math
import random

NORAD_CUBESAT_URL = "http://www.celestrak.com/NORAD/elements/cubesat.txt"


def filter_satdb(sat_count, satdb, max_rotations_per_day=15):
    """
    Filters the given TLE data file.
    The format should correspond to the .txt files supplied by CelesTrak.

    Returns a list of all applicable satellites as dicts with "id" speciying
    the satellite name, and "tle" containing a tuple of the TLE data.
    """
    data = satdb.strip().split("\n")

    results = []
    expect = None
    cur = {}

    for line in data:
        # small TLE parser
        if expect is None:
            cur = {
                "name": line.strip(),
                "tle1": None,
                "tle2": None,
            }
            expect = 1
        elif line.startswith(str(expect)):
            cur["tle" + str(expect)] = line.strip()
            expect += 1
            if expect == 3:
                # Filter soon decaying satellites
                if float(cur["tle2"].split()[7][0:5]) <= max_rotations_per_day:
                    results.append(cur)
                expect = None
        else:
            expect = None

    sats = [{"id": e["name"], "tle": (e["tle1"], e["tle2"])} for e in results]
    return random.sample(sats, sat_count)


def place_gs(count, gs_list=None, hotspot_count=0, reset_ids=True):
    """
    Places ground stations, either randomly or using a list where
    they are selected from randomly.

    Returns a randomly sorted list of GSs described by dicts.
    """

    def _rnd(start, end):
        return random.random() * (end - start) + start

    format_length = int(math.log10(count - 1)) + 1 if count > 1 else 1
    if gs_list is None:
        result = [
            {
                "id": ("gs{:0>" + str(format_length) + "}").format(i),
                "lat": _rnd(-90.0, 90.0),
                "lon": _rnd(-180.0, 180.0),
                "hot": False,
            }
            for i in range(count)
        ]
        random.shuffle(result)
    else:
        gs_list = random.sample(gs_list, count)
        # copy the prototype list to not modify the reference
        result = [
            {
                "id": (
                    ("gs{:0>" + str(format_length) + "}").format(i)
                    if reset_ids else gs_list[i]["id"]
                ),
                "lat": gs_list[i]["lat"],
                "lon": gs_list[i]["lon"],
                "hot": False,
            }
            for i in range(len(gs_list))
        ]

    # add "hot spot" property to the specified amount of stations
    for hotspot in random.sample(result, hotspot_count):
        hotspot["hot"] = True

    return result
