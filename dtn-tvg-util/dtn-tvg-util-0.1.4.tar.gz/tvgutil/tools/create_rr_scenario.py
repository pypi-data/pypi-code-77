#!/usr/bin/env python
# encoding: utf-8

"""
Tool to create a Ring Road scenario description usable by the Ring Road
contact plan generator.
The scenario description file contains a list of satellites including TLE data,
a list of ground stations including their positions, and a start timestamp
(a UNIX timestamp in UTC). It is usually stored as a JSON document.
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
import time
import random

import requests

from tvgutil.ring_road import scenario


def _main(args):
    if args.hotspots > args.gs:
        print("Error: There are less ground stations than hotspots.",
              file=sys.stderr)
        sys.exit(1)

    if args.seed is not None:
        random.seed(args.seed)

    if args.satdbfile is None:
        if abs(args.offset - time.time()) > 604800:
            print(
                "Error: The specified offset differs more than a week from "
                "the current time and you did not provide a TLE data file. "
                "Aborting the scenario creation as most probably no accurate "
                "orbital positions may be determined, or SGP4 libraries such "
                "as pyephem may even raise runtime errors due to the "
                "epoch offset.",
                file=sys.stderr
            )
            sys.exit(1)
        print("Downloading current satellite DB...", file=sys.stderr)
        satdb = requests.get(args.satdburl).text
    else:
        satdb = args.satdbfile.read()
    sats = scenario.filter_satdb(
        args.sats,
        satdb,
        args.maxrot,
    )
    sats.sort(key=lambda e: e["id"])

    gs_list_proto = None
    if args.gsfile is not None:
        gs_list_proto = json.load(args.gsfile)
        print("Using GS list file, containing {} possible location(s).".format(
            len(gs_list_proto)
        ), file=sys.stderr)
    gs_list = scenario.place_gs(
        args.gs,
        gs_list_proto,
        args.hotspots,
        not args.noresetids,
    )
    gs_list.sort(key=lambda e: e["id"])

    result = {
        "satlist": sats,
        "gslist": gs_list,
        "time_offset": args.offset,
    }
    json.dump(
        result,
        args.output,
        indent=(4 if args.indent else None),
    )
    args.output.write("\n")
    args.output.close()
    print("Created scenario file with {} sat(s) and {} gs(s).".format(
        len(sats),
        len(gs_list),
    ), file=sys.stderr)


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="Ring Road Base Scenario Generator")
    parser.add_argument("-g", "--gs", type=int, default=50,
                        help="gs count (default=50)")
    parser.add_argument("-s", "--sats", type=int, default=50,
                        help="sat count (default=50)")
    parser.add_argument("-t", "--offset", type=float, default=time.time(),
                        help="time offset (UTC UNIX timestamp, default=cur.)")
    parser.add_argument("-H", "--hotspots", type=int, default=0,
                        help="num. of randomly selected hot spots (default=0)")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType("w"), default=sys.stdout,
                        help="output JSON file for the contact plan")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    parser.add_argument("--satdburl", default=scenario.NORAD_CUBESAT_URL,
                        help="URL for fetching TLEs (default=celestrak)")
    parser.add_argument("--satdbfile",
                        type=argparse.FileType("r"), default=None,
                        help="file to read TLE data from")
    parser.add_argument("--maxrot", type=float, default=15.0,
                        help="max. rotations/d, for filtering the TLE list")
    parser.add_argument("--seed", type=float, default=None,
                        help="random seed, to get deterministic results")
    parser.add_argument("--noresetids", action="store_true",
                        help="do not change GS IDs when taken from file")
    parser.add_argument("--gsfile",
                        type=argparse.FileType("r"), default=None,
                        help="a JSON file to read GS placements from")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
