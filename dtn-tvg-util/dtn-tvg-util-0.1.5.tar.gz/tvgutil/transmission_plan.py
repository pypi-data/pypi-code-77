#!/usr/bin/env python
# encoding: utf-8

"""
This module allows for flexible and straight-forward generation of so-called
transmission plans (TP), based on a specified network topology (a TVG).
A transmission plan models the creation of individual messages in the
network, containing properties such as the source and destination nodes, the
message size, its creation time ("start time") at the source, and a deadline.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import random
import itertools
import collections

import numpy

Message = collections.namedtuple("Message", (
    "start_time",
    "source",
    "destination",
    "size",
    "deadline",
))
"""Represents a message created in the network."""


def _next_contact_start(edges, node, time):

    def _nmin(seq):
        try:
            first = next(seq)
        except StopIteration:
            return float("inf")
        return min(itertools.chain([first], seq))

    return _nmin(c.start_time for vertices, contacts in edges.items()
                 for c in contacts
                 if node in vertices and c.start_time >= time)


def generate(graph, starttime=None, stoptime=None,
             minsize=100000, maxsize=100000, lifetime=86400,
             interval=30, intervaldev=0.0, srcmode="random", dstmode="random",
             maxcount=None, srccount=1, dstcount=1,
             validsrc=None, validdst=None, invalidsrc=None, invaliddst=None,
             maxtimebeforesrccontact=None, maxtimebeforedstcontact=None):
    """
    Generate a list of Message instances representing individual
    messages created in the network corresponding to the provided TVG.
    Compatible with both FCP and PCP-based TVGs.
    """
    srcs = [n for n in (validsrc or graph.vertices)
            if n not in (invalidsrc or [])]
    dsts = [n for n in (validdst or graph.vertices)
            if n not in (invaliddst or [])]
    start_t = (starttime if starttime is not None else min(
        c.start_time for ev, ec in graph.edges.items() for c in ec
    ))
    stop_t = (stoptime if stoptime is not None else max(
        c.end_time for ev, ec in graph.edges.items() for c in ec
    ))
    tplan = []
    msgidx = 0
    time = start_t
    while time < stop_t and (not maxcount or msgidx < maxcount):
        cur_srcs = [s for s in srcs
                    if (maxtimebeforesrccontact is None or
                        _next_contact_start(graph.edges, s, time) - time <=
                        maxtimebeforesrccontact)]
        cur_srccount = min(srccount, len(cur_srcs))
        if cur_srccount > 0:
            if srcmode == "random":
                source_list = random.sample(cur_srcs, cur_srccount)
            elif srcmode == "all":
                source_list = cur_srcs

            for cur_src in source_list:
                cur_dsts = [d for d in dsts if d != cur_src and (
                    maxtimebeforedstcontact is None or
                    (_next_contact_start(graph.edges, d, time) - time <=
                     maxtimebeforedstcontact)
                )]
                cur_dstcount = min(dstcount, len(cur_dsts))
                if dstmode == "random":
                    dest_list = random.sample(cur_dsts, cur_dstcount)
                elif dstmode == "all":
                    dest_list = cur_dsts
                for cur_dst in dest_list:
                    tplan.append(Message(
                        start_time=time,
                        source=cur_src,
                        destination=cur_dst,
                        size=random.randrange(minsize, maxsize + 1),
                        deadline=time + lifetime,
                    ))
                    msgidx += 1
        # NOTE that the offset may be negative! -> ensure we are not < start_t
        time = max(start_t, time + numpy.random.normal(interval, intervaldev))
    return list(sorted(tplan, key=lambda m: m.start_time))
