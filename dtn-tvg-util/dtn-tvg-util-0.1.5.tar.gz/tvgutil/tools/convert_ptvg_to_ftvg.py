#!/usr/bin/env python
# encoding: utf-8

"""
Tool to convert a P-TVG representation to an F-TVG.
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
    ptvg = tvg.from_serializable(json.load(args.FILE))
    assert ptvg.contact_type == contact_plan.PredictedContact
    for node_tuple in ptvg.edges:
        ptvg.edges[node_tuple] = contact_plan.pcp_to_fcp(
            ptvg.edges[node_tuple],
            remove_probabilistic=args.probabilistic,
        )
    ptvg.contact_type = contact_plan.Contact
    json.dump(
        tvg.to_serializable(ptvg),
        args.output,
        indent=(4 if args.indent else None),
        sort_keys=args.indent,
    )
    args.output.close()
    print("F-TVG with {} vertices and {} edges written.".format(
        len(ptvg.vertices),
        len(ptvg.edges),
    ), file=sys.stderr)


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="P-TVG to F-TVG converter")
    parser.add_argument("FILE", type=argparse.FileType("r"),
                        default=sys.stdin,
                        help="the P-TVG input file")
    parser.add_argument("-p", "--probabilistic", action="store_true",
                        help="remove contacts according to probability")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"),
                        default=sys.stdout,
                        help="the output file for the created F-TVG")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
