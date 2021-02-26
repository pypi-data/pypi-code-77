#!/usr/bin/env python
# encoding: utf-8

"""
Tool to convert an F-TVG representation to a P-TVG.
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
    ftvg = tvg.from_serializable(json.load(args.FILE))
    assert ftvg.contact_type == contact_plan.Contact
    for node_tuple in ftvg.edges:
        ftvg.edges[node_tuple] = contact_plan.fcp_to_pcp(
            ftvg.edges[node_tuple],
        )
    ftvg.contact_type = contact_plan.PredictedContact
    json.dump(
        tvg.to_serializable(ftvg),
        args.output,
        indent=(4 if args.indent else None),
        sort_keys=args.indent,
    )
    args.output.close()
    print("P-TVG with {} vertices and {} edges written.".format(
        len(ftvg.vertices),
        len(ftvg.edges),
    ), file=sys.stderr)


def _get_argument_parser():
    parser = argparse.ArgumentParser(
        description="F-TVG to P-TVG converter")
    parser.add_argument("FILE", type=argparse.FileType("r"),
                        default=sys.stdin,
                        help="the F-TVG input file")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"),
                        default=sys.stdout,
                        help="the output file for the created P-TVG")
    parser.add_argument("-i", "--indent", action="store_true",
                        help="specify this if you want pretty JSON")
    return parser


if __name__ == "__main__":
    _main(_get_argument_parser().parse_args())
