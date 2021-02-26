#!/usr/bin/env python
# encoding: utf-8

"""
Tool to create a Ring Road transmission plan, i.e. a list of messages to be
transmitted in a simulation run. The interval, sources, destinations, sizes,
and further parameters can be selected.
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
import random

import numpy

from tvgutil import tvg, transmission_plan


def _main(args):
    if args.seed is not None:
        random.seed(args.seed)
        numpy.random.seed(args.seed)
    graph = tvg.from_serializable(json.load(args.FILE))
    contacts = [c for ev, ec in graph.edges.items() for c in ec]
    start = min(c.start_time for c in contacts)
    end = max(c.end_time for c in contacts)
    print("Found {} contacts of {} nodes in [{}, {}] ({} days)".format(
        len(contacts),
        len(graph.vertices),
        start,
        end,
        (end - start) / 86400,
    ), file=sys.stderr)
    maxsize = args.maxsize or args.minsize
    starttime = start if args.starttime is None else args.starttime
    stoptime = end if args.stoptime is None else args.stoptime
    if args.startpercentoffset is not None:
        starttime += (end - start) * (args.startpercentoffset / 100)
    if args.maxgenpercent is not None:
        stoptime = starttime + (end - start) * (args.maxgenpercent / 100)
    print((
        "Generating transmission plan:\n"
        "    -> in interval [{}, {}] ({} days)\n"
        "    -> {} +/- {} generations/h\n"
        "    -> lifetime: {} s\n"
        "    -> size within interval: [{}, {}] bytes"
    ).format(
        starttime,
        stoptime,
        (stoptime - starttime) / 86400,
        round(3600 / args.interval, 2),
        round(
            3600 / (args.interval - args.intervaldev) - 3600 / args.interval,
            2
        ),
        args.lifetime,
        args.minsize / 8,
        maxsize / 8,
    ), file=sys.stderr)
    tplan = transmission_plan.generate(
        graph,
        starttime=starttime,
        stoptime=stoptime,
        minsize=args.minsize,
        maxsize=maxsize,
        lifetime=args.lifetime,
        interval=args.interval,
        intervaldev=args.intervaldev,
        srcmode=args.srcmode,
        dstmode=args.dstmode,
        maxcount=args.maxcount,
        srccount=args.srccount,
        dstcount=args.dstcount,
        validsrc=args.validsrc,
        validdst=args.validdst,
        invalidsrc=args.invalidsrc,
        invaliddst=args.invaliddst,
        maxtimebeforesrccontact=args.maxtimebeforesrccontact,
        maxtimebeforedstcontact=args.maxtimebeforedstcontact,
    )
    json.dump(
        tplan,
        args.output,
        indent=(4 if args.indent else None),
    )
    args.output.write("\n")
    args.output.close()
    print("Transmission plan with {} entries written.".format(
        len(tplan),
    ), file=sys.stderr)


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="Transmission Plan Generator for the TVG Tools")
    parser.add_argument("FILE", nargs="?", type=argparse.FileType("r"),
                        default=sys.stdin, help="the TVG JSON file")
    parser.add_argument("--validsrc", nargs="*", default=[],
                        help="a list of valid src nodes")
    parser.add_argument("--validdst", nargs="*", default=[],
                        help="a list of valid dst nodes")
    parser.add_argument("--invalidsrc", nargs="*", default=[],
                        help="a list of invalid src nodes")
    parser.add_argument("--invaliddst", nargs="*", default=[],
                        help="a list of invalid dst nodes")
    parser.add_argument("-s", "--starttime", type=int, default=None,
                        help="the start time for message generation")
    parser.add_argument("-e", "--stoptime", type=int, default=None,
                        help="the stop time for message generation")
    parser.add_argument("-p", "--maxgenpercent", type=int, default=None,
                        help="calculate the stop time as a percentage")
    parser.add_argument("--startpercentoffset", type=int, default=None,
                        help="calculate the start time as a percentage")
    parser.add_argument("-m", "--maxcount", type=int, default=None,
                        help="the maximum count of messages")
    parser.add_argument("-t", "--interval", type=float, default=30.0,
                        help="the message generation interval")
    parser.add_argument("-l", "--lifetime", type=float, default=86400.0,
                        help="the message lifetime, default=1 day")
    parser.add_argument("--intervaldev", type=float, default=0.0,
                        help="std. dev. of the message generation interval")
    parser.add_argument("--srcmode", default="random",
                        choices=["random", "all"],
                        help="the message generation mode")
    parser.add_argument("--dstmode", default="random",
                        choices=["random", "all"],
                        help="the message addressing mode")
    parser.add_argument("--srccount", type=int, default=1,
                        help="the count of sources taken at each interval")
    parser.add_argument("--dstcount", type=int, default=1,
                        help="the count of dests taken at each interval")
    parser.add_argument("--minsize", type=int, default=100000,
                        help="the minimum message size in bit, default=100K")
    parser.add_argument("--maxsize", type=int, default=None,
                        help="the maximum message size in bit, default=<min>")
    parser.add_argument("--maxtimebeforesrccontact", type=float, default=None,
                        help="the maximum time before the next src contact")
    parser.add_argument("--maxtimebeforedstcontact", type=float, default=None,
                        help="the maximum time before the next dst contact")
    parser.add_argument("--seed", type=float, default=None,
                        help="random seed to get deterministic results")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType("w"), default=sys.stdout,
                        help="output JSON file for the transmission plan")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
