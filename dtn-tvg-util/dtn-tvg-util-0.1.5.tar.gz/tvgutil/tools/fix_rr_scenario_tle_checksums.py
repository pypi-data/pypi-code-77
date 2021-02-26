#!/usr/bin/env python
# encoding: utf-8

"""
Tool to re-calculate all checksums within the TLE data provided in the
input scenario file. This simplifies experiments with TLE data (e.g. changing
the satellite's inclination). STDIN is used for input, STDOUT for output;
an RR scenario JSON representation as provided by the "create_rr_scenario"
tool is assumed.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import sys
import json


def _main(indent=False):
    data = json.load(sys.stdin)
    for sat in data["satlist"]:
        for i in range(len(sat["tle"])):
            line = sat["tle"][i]
            # calculate TLE checksum: a minus sign ("-") counts as one
            checksum = (
                sum(int(n) for n in line[:-1] if n in "123456789") +
                sum(1 for c in line[:-1] if c == "-")
            ) % 10
            sat["tle"][i] = line[:-1] + str(checksum)
    print(json.dumps(data, indent=(4 if indent else None)))


if __name__ == "__main__":
    _main(len(sys.argv) > 1 and sys.argv[1] == "-i")
