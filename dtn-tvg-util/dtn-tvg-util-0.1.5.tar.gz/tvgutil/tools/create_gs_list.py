#!/usr/bin/env python
# encoding: utf-8

"""
Tool to create a ground station list by positioning ground stations randomly
on the Earth's landmasses.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import sys
import json
import argparse

from tvgutil.ring_road.gslist import place_on_land


def _main(args):
    gs_list = place_on_land(
        args.shapefile,
        args.groundstations,
        args.prefix,
        args.startid,
    )
    json.dump(
        gs_list,
        args.output,
        indent=(4 if args.indent else None),
    )
    args.output.write("\n")
    args.output.close()


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="GS list generator for the RR scenario generator")
    parser.add_argument("-g", "--groundstations", type=int, default=200,
                        help="count of ground stations (default=200)")
    parser.add_argument("-p", "--prefix", default="gs",
                        help="id prefix (default='gs')")
    parser.add_argument("-s", "--startid", type=int, default=1,
                        help="id offset (default=1)")
    parser.add_argument("-f", "--shapefile", type=str,
                        default=("test_data/shape_earth_land_110m/"
                                 "ne_110m_land.shp"),
                        help="shapefile to be used for GS positioning")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType("w"), default=sys.stdout,
                        help="output JSON file for the GS list")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
