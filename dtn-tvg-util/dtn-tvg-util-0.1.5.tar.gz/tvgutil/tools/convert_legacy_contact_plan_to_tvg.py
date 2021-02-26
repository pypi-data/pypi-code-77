#!/usr/bin/env python
# encoding: utf-8

"""
Tool to convert a legacy (e.g. the ONE) contact plan to a TVG representation.
The resulting TVG is either a P-TVG or an F-TVG (if --factual is specified).
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import argparse
import json
import sys

from tvgutil import contact_plan, tvg


def _main(args):
    legacy_cplan = [c for in_file in args.FILE for c in json.load(in_file)]
    pcp = contact_plan.legacy_to_pcp(
        legacy_cplan,
        unidirectional=args.unidirectional,
        bit_rate=args.bitrate,
    )
    if args.factual:
        cplan = contact_plan.pcp_to_fcp(
            pcp,
            remove_probabilistic=args.rmprob,
        )
    else:
        cplan = pcp
    graph = tvg.from_contact_plan(cplan, contact_type=(
        contact_plan.Contact if args.factual else contact_plan.PredictedContact
    ))
    json.dump(
        tvg.to_serializable(graph),
        args.output,
        indent=(4 if args.indent else None),
        sort_keys=args.indent,
    )
    args.output.close()
    print("{}-TVG with {} vertices and {} edges ({} contacts) written.".format(
        "F" if args.factual else "P",
        len(graph.vertices),
        len(graph.edges),
        len(cplan),
    ), file=sys.stderr)


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="Legacy Contact Plan to TVG Converter")
    parser.add_argument("FILE", type=argparse.FileType("r"),
                        nargs="*", default=[sys.stdin],
                        help="the contact plan input files")
    parser.add_argument("-f", "--factual", action="store_true",
                        help="convert as factual contact plan (FCP)")
    parser.add_argument("-u", "--unidirectional", action="store_true",
                        help="assume the contact plan is NOT bidirectional")
    parser.add_argument("-r", "--bitrate", type=float, default=None,
                        help="enforce a specific bit rate and calc. capacity")
    parser.add_argument("--rmprob", action="store_true",
                        help="FCP: remove contacts probabilistically")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"),
                        default=sys.stdout, help="the output file for the TVG")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
