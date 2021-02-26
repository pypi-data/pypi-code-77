# encoding: utf-8

"""A Node allowing to use NG-SABR."""

import dataclasses
import logging
import math

import asyncio

from typing import Optional

from tvgutil.contact_plan import SimplePredictedContactTuple
from tvgutil.tvg import TVG

from . import sabr, tvdijkstra
from ..util import StartTimeBasedDict

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class NGSABRGraphData(sabr.SABRGraphDataBase):
    """A class encapsulating knowledge about the network at a given time."""

    # This structure contains the graph object.
    ptvg: Optional[TVG] = dataclasses.field(
        default=None,
        compare=False,
    )


class NGSABRNode(sabr.SABRNodeBase):
    """A Node allowing the use of NG-SABR."""

    def __init__(self, eid, buffer_size, event_dispatcher,
                 routing_algorithm, ptvg, graph_update_min_interval,
                 volume_limited=False, **kwargs):
        """Initialize the NG-SABR Node.

        Args:
            - See args of sabr.SABRNodeBase.
            - volume_limited: Use the earliest-depleted instead of the
                              earliest-ending contact as a limiting contact.

        """
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            routing_algorithm,
            ptvg,
            graph_update_min_interval,
            **kwargs
        )
        self.volume_limited = volume_limited

    def initialize_cgr_data(self, ptvg, update_min_interval, own_eid):
        """Initialize the graph data structures from the given P-TVG."""
        # Pre-initialize graph data dict while merging based on timestamp
        generation_start_times = []
        for edge, predicted_contact_list in ptvg.edges.items():
            for predicted_contact in predicted_contact_list:
                for generation in predicted_contact.generations:
                    generation_start_times.append(generation.valid_from)

        # Initialize empty instances based on user-defined granularity
        graph_data = {}
        last_ts = -math.inf
        for ts in sorted(generation_start_times):
            if ts - last_ts > update_min_interval:
                graph_data[ts] = NGSABRGraphData(
                    start_time=ts,
                )
                last_ts = ts

        logger.debug("Will generate %d graph(s) for node %s",
                     len(graph_data), own_eid)

        # Add ContactGraph to instances
        for gen_start_time, gd in graph_data.items():
            # Copy the PTVG to a simple edge-tuple representation
            edges = {}
            full_contact_list = []
            for edge, predicted_contact_list in ptvg.edges.items():
                tx_node, rx_node = edge
                cur_contact_list = []
                for predicted_contact in predicted_contact_list:
                    # A hashable tuple representation, used for indexing
                    # (This calculates an average bit rate.)
                    contact_identifier = predicted_contact.to_simple(
                        generation_at=gen_start_time,
                        characteristics_at=None,
                    )
                    cur_contact_list.append(contact_identifier)
                    if tx_node == own_eid:
                        if rx_node not in gd.neighbor_contact_lists:
                            gd.neighbor_contact_lists[rx_node] = []
                        gd.neighbor_contact_lists[rx_node].append(
                            contact_identifier
                        )
                edges[edge] = cur_contact_list
                full_contact_list.extend(cur_contact_list)
            gd.ptvg = TVG(
                ptvg.vertices.copy(),
                edges,
                contact_type=SimplePredictedContactTuple,
            )
            gd.contact_plan = full_contact_list

        logger.info(
            "Initialized %d graph(s) for node %s", len(graph_data), self.eid,
        )

        return StartTimeBasedDict(graph_data)

    def route_generator_factory(self, gd, source_eid, dest_eid, excluded_eids):
        """Create a route generator for NG-SABR."""
        excluded_contacts = set()

        while True:
            dr = tvdijkstra.tvdijkstra(
                gd.ptvg,
                source_eid,
                dest_node=dest_eid,
                node_blacklist=excluded_eids,
                contact_blacklist=excluded_contacts,
                start_time=asyncio.get_running_loop().time()
            )

            path_length, _, contact_path, _ = dr.get_path(dest_eid)

            # Any route found?
            if not path_length:
                break

            contact_path = list(contact_path)

            # Determine the time at which the route becomes invalid.
            limiting_contact_index = None
            if self.volume_limited:
                route_vol = math.inf
                for i, contact in enumerate(contact_path):
                    vol = (
                        (contact.end_time - contact.start_time) *
                        contact.bit_rate
                    )
                    if vol >= route_vol:
                        continue
                    route_vol = vol
                    limiting_contact_index = i
            else:
                route_end_time = math.inf
                limiting_contact_index = None
                for i, contact in enumerate(contact_path):
                    if contact.end_time >= route_end_time:
                        continue
                    route_end_time = contact.end_time
                    limiting_contact_index = i
                excluded_contacts.add(contact_path[limiting_contact_index])
            excluded_contacts.add(contact_path[limiting_contact_index])

            yield contact_path
