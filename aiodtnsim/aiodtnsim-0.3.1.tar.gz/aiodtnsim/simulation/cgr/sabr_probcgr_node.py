# encoding: utf-8

"""A Node allowing to use probabilistic NG-SABR."""

import functools
import itertools
import logging
import math

import asyncio

from . import sabr, tvdijkstra
from .sabr_nodegraph_node import NGSABRNode

logger = logging.getLogger(__name__)


class ProbNGSABRNode(NGSABRNode):
    """A Node allowing to use probabilistic NG-SABR."""

    def __init__(self, eid, buffer_size, event_dispatcher,
                 routing_algorithm, ptvg, graph_update_min_interval,
                 max_routes=math.inf, max_order_routes=5,
                 re_schedule_delayed=True, re_schedule_overbooked=True,
                 reject_looping=False, no_alt_for_looping=True,
                 route_min_confidence=0.1, always_drop_prob=False,
                 first_contact_filter=False, **kwargs):
        """Initialize the Prob-NG-SABR Node.

        Args:
            - See args of NGSABRNode.
            - route_min_confidence: The minimum confidence value for a route
                                    to be included.
            - always_drop_prob: Always drop the minimum-confidence route. If
                                False, only drop if threshold is not achieved.
            - first_contact_filter: Filter routes based on the first-contact
                                    confidence only.

        """
        super().__init__(
            eid=eid,
            buffer_size=buffer_size,
            event_dispatcher=event_dispatcher,
            routing_algorithm=routing_algorithm,
            ptvg=ptvg,
            graph_update_min_interval=graph_update_min_interval,
            max_routes=max_routes,
            max_order_routes=max_order_routes,
            re_schedule_delayed=re_schedule_delayed,
            re_schedule_overbooked=re_schedule_overbooked,
            reject_looping=reject_looping,
            no_alt_for_looping=no_alt_for_looping,
            **kwargs
        )
        self.route_min_confidence = route_min_confidence
        self.always_drop_prob = always_drop_prob
        self.first_contact_filter = first_contact_filter

    def route_generator_factory(self, gd, source_eid, dest_eid, excluded_eids):
        """Create a route generator for Prob-NG-SABR."""
        excluded_contacts = set()

        while True:
            dr = tvdijkstra.tvdijkstra(
                gd.ptvg,
                source_eid,
                dest_node=dest_eid,
                node_blacklist=excluded_eids,
                contact_blacklist=excluded_contacts,
                start_time=asyncio.get_running_loop().time(),
            )

            path_length, _, contact_path, _ = dr.get_path(dest_eid)

            # Any route found?
            if not path_length:
                break

            contact_path = list(contact_path)

            # Determine the time at which the route becomes invalid.
            # ### Find out earliest-ending and least-probable contact
            route_end_time = math.inf
            route_min_vol = math.inf
            limiting_contact_index = None
            volume_limiting_contact_index = None
            route_min_probability = 1.0
            prob_route_end_time = math.inf
            prob_limiting_contact_index = None
            for i, contact in enumerate(contact_path):
                if contact.end_time < route_end_time:
                    route_end_time = contact.end_time
                    limiting_contact_index = i
                contact_volume = (
                    (contact.end_time - contact.start_time) *
                    contact.bit_rate
                )
                if contact_volume < route_min_vol:
                    route_min_vol = contact_volume
                    volume_limiting_contact_index = i
                if route_min_probability - contact.probability >= -1e-4:
                    if route_min_probability - contact.probability < 1e-4:
                        # If the prob. are (almost) equal, compare end time
                        if contact.end_time < prob_route_end_time:
                            route_min_probability = contact.probability
                            prob_limiting_contact_index = i
                            prob_route_end_time = contact.end_time
                    else:
                        route_min_probability = contact.probability
                        prob_limiting_contact_index = i
                        prob_route_end_time = contact.end_time

            if self.volume_limited:
                limiting_contact_index = volume_limiting_contact_index

            # ### Get route confidence
            if self.first_contact_filter:
                route_success_prob = contact_path[0].probability
            else:
                route_success_prob = 1.0
                for contact in contact_path:
                    route_success_prob *= contact.probability

            # ### Only return the route if Pr >= Pr_min
            if route_success_prob < self.route_min_confidence:
                excluded_contacts.add(
                    contact_path[prob_limiting_contact_index]
                )
            else:
                if self.always_drop_prob:
                    excluded_contacts.add(
                        contact_path[prob_limiting_contact_index]
                    )
                else:
                    excluded_contacts.add(
                        contact_path[limiting_contact_index]
                    )
                yield contact_path


# Standard comparison function to rank routes from an applicable route list
# according to the SABR specification.
# 3.2.8.1.1-4 Route ranking using projected bundle arrival time (3.2.6.7)
def sabr_cmp(candidate_tuple, route_tuple):
    """Compare two routes as specified in SABR 3.2.8.1.1-4."""
    candidate, candidate_pbat = candidate_tuple
    route, route_pbat = route_tuple
    # 3.2.8.1.4 a) 1)
    if candidate_pbat < route_pbat:
        return -1
    elif abs(candidate_pbat - route_pbat) < 1e-6:
        # 3.2.8.1.4 a) 2)
        if len(candidate.contact_path) < len(route.contact_path):
            return -1
        elif len(candidate.contact_path) == len(route.contact_path):
            # 3.2.8.1.4 a) 3)
            if candidate.end_time > route.end_time:
                return -1
            elif abs(candidate.end_time - route.end_time) < 1e-6:
                # 3.2.8.1.4 a) 4)
                if candidate.entry_vid < route.entry_vid:
                    return -1
    return 1


# 3.2.8.1, modified
def probsabr(gd, bundle, cur_eid, cur_time, excluded_eids,
             tx_queue_volume_f, max_transmission_volume_f,
             route_generator_factory, max_routes, max_order_routes,
             target_confidence=0.7, first_contact_prob=True):
    """Perform a modified SABR routing based on the Prob-CGR extensions.

    Args:
        - See args of sabr.sabr.
        - target_confidence: The minimum confidence threshold to be achieved
                             by selecting multiple routes.
        - first_contact_prob: Determine the route confidence based on the first
                              contact only.

    """
    candidate_routes = sabr.get_candidate_route_gen(
        gd=gd,
        bundle=bundle,
        cur_eid=cur_eid,
        cur_time=cur_time,
        excluded_eids=excluded_eids,
        tx_queue_volume_f=tx_queue_volume_f,
        max_transmission_volume_f=max_transmission_volume_f,
        route_generator_factory=route_generator_factory,
        max_routes=max_routes,
    )

    # NOTE: We are free to consider any amount of candidates, according to
    #   3.2.6.9.1. We consider a fixed amount for now.
    order_candidates = list(
        itertools.islice(candidate_routes, max_order_routes)
    )

    # ### Sample the best routes from the list until either the threshold or
    # the max. count is reached.
    # NOTE this uses a very simple total probability estimation strategy,
    # which does not consider overlaps on the individual routes, though,
    # can be sufficient to improve delivery ratios in many cases.
    # For an improved strategy, the following resources could be helpful:
    # https://cs.stackexchange.com/questions/16439
    # https://math.stackexchange.com/questions/2242640
    # https://math.stackexchange.com/questions/845916
    taken_routes = []
    failure_prob = 1.0
    for candidate, pbat in sorted(order_candidates,
                                  key=functools.cmp_to_key(sabr_cmp)):
        if first_contact_prob:
            route_success_prob = candidate.contact_path[0].probability
        else:
            route_success_prob = 1.0
            for contact in candidate.contact_path:
                route_success_prob *= contact.probability
        taken_routes.append(candidate)
        failure_prob *= (1 - route_success_prob)
        if failure_prob <= 1 - target_confidence:
            break

    return taken_routes
