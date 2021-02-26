#!/usr/bin/env python
# encoding: utf-8

"""
Provides methods for placing ground stations in a Ring Road scenario.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import random

from shapely.geometry import shape, Point
from fiona import collection


def _get_land_polygons(shapefile):
    with collection(shapefile, "r") as shape_collection:
        return [shape(e["geometry"]) for e in shape_collection]


def _place_groundstation_latlon(land_areas, cumulative_area):
    # Get random landmass, weighed by area
    rand_area = random.random() * cumulative_area
    for area_instance in land_areas:
        if area_instance.area >= rand_area:
            used_area = area_instance
            break
        rand_area -= area_instance.area
    # Generate a random point within the landmass
    minlon, minlat, maxlon, maxlat = used_area.bounds
    while True:
        randpoint = (random.random() * (maxlon - minlon) + minlon,
                     random.random() * (maxlat - minlat) + minlat)
        if used_area.contains(Point(*randpoint)):
            return (randpoint[1], randpoint[0])


def place_on_land(shapefile, count, prefix="gs", id_offset=1):
    """
    Places the given amount of ground stations on land masses of the Earth.
    The landmasses are derived from the provided shapefile.
    """
    land_areas = _get_land_polygons(shapefile)
    cumulative_area = sum(x.area for x in land_areas)
    result = []
    for i in range(count):
        lat, lon = _place_groundstation_latlon(land_areas, cumulative_area)
        result.append({
            "id": prefix + str(id_offset + i),
            "lat": lat,
            "lon": lon,
        })
    return result


def place_randomly(count, prefix="gs", id_offset=1):
    """Places the given amount of ground stations randomly."""
    return [{
        "id": prefix + str(id_offset + i),
        "lat": random.random() * 180 - 90,
        "lon": random.random() * 360 - 180,
    } for i in range(count)]
