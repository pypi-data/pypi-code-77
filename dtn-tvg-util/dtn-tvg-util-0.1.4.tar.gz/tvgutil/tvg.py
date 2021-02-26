#!/usr/bin/env python
# encoding: utf-8

"""
Module providing functions for handling a time-varying graph (TVG)
representation of a DTN.

The TVG consists basically of two important data structures:
- The vertices dict: Contains the IDs of all vertices of the graph
  (which are the network nodes) as keys, associated to a set of the vertices
  they are connected to.
- The edges dict: Contains tuples of (node1, node2) if a directed edge exists
  from node1 to node2 as keys, associated to a list of contacts (i.e.
  instances of either Contact or PredictedContact representing when the
  edge exists).

Corresponding to the contained contact objects, a TVG can either be a factual
TVG (F-TVG, contains Contact instances), or a predicted TVG (P-TVG, contains
PredictedContact instances).
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import sys

from tvgutil.contact_plan import Contact, PredictedContact


class TVG(object):

    """
    The TVG base class, containing the vertices, edges, and the type of
    contact instances contained in the graph.
    """

    __slots__ = (
        "vertices",
        "edges",
        "contact_type",
    )

    def __init__(self, vertices, edges, contact_type=PredictedContact):
        self.vertices = vertices
        self.edges = edges
        self.contact_type = contact_type


def to_contact_plan(tvg):
    """
    Converts the provided tvg instance to a contact plan.
    F-TVGs are converted to FCPs, while P-TVGs are converted to PCPs.
    """
    return sorted(
        [c for nodes, contacts in tvg.edges.items() for c in contacts],
        key=lambda c: c.start_time,
    )


def from_contact_plan(plan, contact_type=PredictedContact):
    """
    Converts the provided contact plan (either an FCP or a PCP) to a TVG.
    The type of contact instances in the contact plan has to be provided.
    For PCPs, the type is PredictedContact (which is the default), for FCPs,
    the type is Contact.
    """
    vertices_set = set()
    edges = {}
    for contact in plan:
        assert isinstance(contact, contact_type)
        vertices_set.add(contact.tx_node)
        vertices_set.add(contact.rx_node)
        nodes = (contact.tx_node, contact.rx_node)
        if nodes in edges:
            edges[nodes].append(contact)
        else:
            edges[nodes] = [contact]
    vertices_dict = {
        id_: {neigh for neigh in vertices_set if (id_, neigh) in edges}
        for id_ in vertices_set
    }
    # Sort contacts by start time
    for nodes, contacts in edges.items():
        contacts.sort(key=lambda e: e.start_time)
    return TVG(vertices_dict, edges, contact_type)


def to_serializable(tvg):
    """
    Converts the provided TVG to a JSON-serializable dict/list representation.
    """
    contact_type_str = {
        "Contact": "Contact_v2",
        "PredictedContact": "PredictedContact_v2",
    }[tvg.contact_type.__name__]
    return {
        "vertices": {
            key: list(value) for key, value in tvg.vertices.items()
        },
        "edges": [
            {
                "vertices": list(key),
                "contacts": [contact.to_list() for contact in value],
            }
            for key, value in tvg.edges.items()
        ],
        "contact_type": contact_type_str,
    }


def from_serializable(data):
    """
    Creates a TVG instance from the provided JSON-serializable dict/list
    representation obtained by calling to_serializable.
    """
    if "_v2" not in data["contact_type"]:
        print(
            "WARNING: Loading TVG file using v1 compatibility mode!",
            file=sys.stderr,
        )
    contact_type, contact_factory = {
        "Contact_v2": (Contact, Contact.from_list),
        "PredictedContact_v2": (PredictedContact, PredictedContact.from_list),
        "Contact": (Contact, Contact.from_v1),
        "PredictedContact": (PredictedContact, PredictedContact.from_v1),
    }[data["contact_type"]]
    vertices = {
        key: set(value) for key, value in data["vertices"].items()
    }
    edges = {
        tuple(edge["vertices"]): sorted(
            [contact_factory(c) for c in edge["contacts"]],
            key=lambda contact: contact.start_time,
        )
        for edge in data["edges"]
    }
    return TVG(vertices, edges, contact_type)
