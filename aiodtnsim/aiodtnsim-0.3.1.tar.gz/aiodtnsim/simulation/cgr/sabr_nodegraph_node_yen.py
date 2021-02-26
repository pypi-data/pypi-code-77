# encoding: utf-8

"""A Node allowing to use NG-SABR with Yen's algorithm."""

import collections
import heapq

import asyncio

from . import tvdijkstra
from .sabr_nodegraph_node import NGSABRNode

RouteInfo = collections.namedtuple(
    "RouteInfo",
    ["contact_path", "arrival_times"],
)


class NGSABRNodeYen(NGSABRNode):
    """A Node allowing to use NG-SABR and Yen's algorithm."""

    def __init__(self, eid, buffer_size, event_dispatcher,
                 routing_algorithm, ptvg, graph_update_min_interval,
                 max_routes_yen=1000, **kwargs):
        super().__init__(
            eid,
            buffer_size,
            event_dispatcher,
            routing_algorithm,
            ptvg,
            graph_update_min_interval,
            **kwargs
        )
        self.max_routes_yen = max_routes_yen

    def route_generator_factory(self, gd, source_eid, dest_eid, excluded_eids):
        """Create a route generator for NG-SABR with Yen's algorithm."""
        K = self.max_routes_yen

        # The list of returned (best) routes.
        A = []
        # The heap of candidates for the next-best route.
        B = []

        # Copy the excluded EIDs to a set.
        excluded_eids = set(excluded_eids)
        # Search for the first-best route.
        start_time = asyncio.get_running_loop().time()
        dr = tvdijkstra.tvdijkstra(
            gd.ptvg,
            source_eid,
            dest_node=dest_eid,
            node_blacklist=excluded_eids,
            contact_blacklist=set(),
            start_time=start_time,
        )
        path_length, _, contact_path, eat = dr.get_path(dest_eid)
        if not path_length:
            # Nothing found...
            return
        # tvdijkstra does not use a notional root contact, so we emulate it by
        # adding "None" to the path with arrival time == start time.
        first_route = RouteInfo(
            list(contact_path),
            list(eat),
        )
        A.append(first_route)
        # Yield the contact path without the emulated notional root.
        yield first_route.contact_path

        for k in range(K):
            # NOTE: Could be worth considering to update start_time here...
            # start_time = asyncio.get_running_loop().time()
            # Take apart the last-best route to find the next-best route.
            for i, spur_contact in enumerate(A[-1].contact_path):
                spur_node = spur_contact.tx_node
                # The path to the spur node (at which the spur contact starts).
                root_path = A[-1].contact_path[:i]
                arrival_times = A[-1].arrival_times[:i]
                arrival_time = (
                    arrival_times[-1] if arrival_times else start_time
                )
                # Blacklist the path leading to the spur node, excluding the
                # spur contact as it is outgoing.
                contact_blacklist = set(root_path)
                # All contacts that are reachable from the same root path and
                # already contained in existing routes are blacklisted.
                # This also includes the spur contact.
                for route in A:
                    if root_path == route.contact_path[:i]:
                        contact_blacklist.add(route.contact_path[i])
                # Blacklist nodes on the root path.
                node_blacklist = excluded_eids.copy()
                for contact in root_path:
                    node_blacklist.add(contact.tx_node)
                # Search for the next-best route starting at the spur node.
                dr = tvdijkstra.tvdijkstra(
                    gd.ptvg,
                    spur_node,
                    dest_node=dest_eid,
                    node_blacklist=node_blacklist,
                    contact_blacklist=contact_blacklist,
                    start_time=arrival_time,
                )
                path_length, _, contact_path, eat = dr.get_path(dest_eid)
                # If a new route has been found, add it to the heap.
                if path_length:
                    heapq.heappush(B, (
                        list(eat)[-1],
                        RouteInfo(
                            root_path + list(contact_path),
                            arrival_times + list(eat),
                        )
                    ))

            # No candidates found, terminate.
            if not B:
                break
            # Pop the best candidate from the heap, add it to A, and yield it.
            _, new_route = heapq.heappop(B)
            A.append(new_route)
            yield new_route.contact_path
