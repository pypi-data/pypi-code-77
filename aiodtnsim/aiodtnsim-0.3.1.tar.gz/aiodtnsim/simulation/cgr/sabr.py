# encoding: utf-8

"""A Node allowing the use of CCSDS-SABR-CGR."""

# NOTE: Does NOT support priorities (assumes all bundles equal).
# NOTE: Does NOT support fragmentation (assumes it disabled for all bundles).
# NOTE: Does NOT support varying delay (OWLT margin).
# NOTE: Does NOT support critical bundle transmission.
# NOTE: Does NOT support changes in the predicted soft time frames. If a
#   contact interval changes, either only the volume (and other
#   characteristics) may be changed, or a new contact has to be constructed.
#   This is due to contacts being uniquely-identified by their interval.

import asyncio
import collections
import dataclasses
import logging
import math

from typing import List

from ... import timeutil
from ..scheduling_event_node import SchedulingEventNode
from ..util import StartTimeBasedDict

from tvgutil.contact_plan import SimplePredictedContactTuple

logger = logging.getLogger(__name__)

Route = collections.namedtuple("Route", [
    # This is the start time, not adjusted start time.
    # It is used to derive adjusted start time to derive ETO. (3.2.6.2)
    "start_time",
    # This is the end time of the earliest-ending contact on the route.
    # also: "termination time", 2.3.2.1
    "end_time",
    # EID of the neighbor that is the receiving node of the first contact.
    "neighbor_eid",
    # The list of contacts taken on the route, excluding notional vertices.
    "contact_path",
    # The minimum of the stop time of every contact or any following contact.
    "effective_stop_times",
    # The entry node number of the route.
    "entry_vid",
])


@dataclasses.dataclass
class SABRGraphDataBase:
    """The base data structure the SABR node operates on.

    An instance of this dataclass contains knowledge regarding one contact
    graph instance, i.e. the graph itself, the obtained applicable routes,
    the route generators, and further implementation-dependent data.
    It is valid from the timestamp given by start_time until the timestamp
    given by start_time of the next entry within the StartTimeBasedDict
    that contains it.

    Args:
        - start_time: The start of the validity interval of the prediction.
        - contact_plan: A list of all contacts that may be ordered by
                        some criterion.
        - neighbor_contact_lists: The contact plan for each neighbor EID.
        - route_lists: A cache for applicable routes, per destination EID.
        - route_lists: A cache for candidate route generators, per
                       destination EID.
    """

    # Validity interval of the graph (prediction).
    start_time: float

    # A list of all contacts, may be ordered by some criterion.
    contact_plan: List[SimplePredictedContactTuple] = dataclasses.field(
        default_factory=list,
        compare=False,
    )

    # This list associates every neighbor to a contact list.
    neighbor_contact_lists: collections.OrderedDict = dataclasses.field(
        default_factory=collections.OrderedDict,
        compare=False,
    )

    # Fields for SABR caching follow.

    # This dict caches pre-calculated CGR routes based on the graph.
    # Its keys are node eids, its values Route.
    route_lists: collections.OrderedDict = dataclasses.field(
        default_factory=collections.OrderedDict,
        compare=False,
    )
    # This dict caches the route generator.
    # Its keys are node eids, its values a generator yielding vid-path lists.
    route_gens: collections.OrderedDict = dataclasses.field(
        default_factory=collections.OrderedDict,
        compare=False,
    )


@dataclasses.dataclass
class SABRCVU:
    """A representation of the predicted and used contact volume."""

    predicted: float
    used: float


class SABRNodeBase(SchedulingEventNode):
    """A Node allowing the use of SABR."""

    def __init__(self, eid, buffer_size, event_dispatcher,
                 routing_algorithm, ptvg, graph_update_min_interval,
                 max_routes=math.inf, max_order_routes=6,
                 re_schedule_delayed=True, re_schedule_overbooked=True,
                 reject_looping=False, no_alt_for_looping=False,
                 **kwargs):
        """Initialize the CGR Node.

        Args:
            - eid: The Node's unique identifier.
            - buffer_size: The assumed simulated maximum buffer size in bits.
                           Can be set to -1 to assume an infinite buffer size.
            - event_dispatcher: The aiodtnsim event dispatcher to monitor the
                                simulation process.
            - routing_algorithm: A compatible routing algorithm.
            - ptvg: The predicted time-varying graph.
            - graph_update_min_interval: The minimum interval, in seconds,
                                         between two graph updates.
            - max_routes: The maximum amount of routes to be examined for
                          getting applicable routes. Should not be limited in
                          most cases.
            - max_order_routes: The maximum amount of applicable routes to be
                                examined to get the best route.
            - re_schedule_delayed: Re-schedule bundles that are still in the
                                   queue after the contact has ended for which
                                   they were booked.
            - re_schedule_overbooked: Re-schedule bundles that are booked for
                                      contacts for which the predicted volume
                                      has decreased.
            - reject_looping: Remember transmitted bundles and drop them if
                              received again.
            - no_alt_for_looping: Do not provide alternative routes for known
                                  (formerly-routed) bundles.
            - link_factory: The (optional) callable to obtain a Link.

        """
        super().__init__(eid, buffer_size, event_dispatcher, **kwargs)
        self.routing_algorithm = routing_algorithm
        self.max_routes = max_routes
        self.max_order_routes = max_order_routes
        self.re_schedule_delayed = re_schedule_delayed
        self.re_schedule_overbooked = re_schedule_overbooked
        self.reject_looping = reject_looping
        self.no_alt_for_looping = no_alt_for_looping
        self.track_looping = reject_looping or no_alt_for_looping
        self.known_bundles = set()
        self.cgr_data = self.initialize_cgr_data(
            ptvg,
            graph_update_min_interval,
            eid,
        )
        self.sched_refcount = {}
        assert isinstance(self.cgr_data, StartTimeBasedDict)
        assert isinstance(self.cgr_data.get_entry_for(0), SABRGraphDataBase)
        self._initialize_queues(
            ptvg,
            eid,
            self.cgr_data.get_entry_for(0).contact_plan,
        )
        # Schedule watching Tasks
        for (tx_node, rx_node), edge_contacts in ptvg.edges.items():
            # only watch our own contacts
            if tx_node != self.eid:
                continue
            for contact in edge_contacts:
                asyncio.ensure_future(self.schedule_predicted_contact_end(
                    contact,
                ))
        for i, start_time in enumerate(self.cgr_data.base_dict_keys):
            # For the first item, the graph did not yet change.
            if i == 0:
                continue
            asyncio.ensure_future(self.schedule_graph_change(
                self.cgr_data.base_dict[start_time],
            ))

    async def schedule_predicted_contact_end(self, contact):
        """Wait until the contact end and trigger predicted_contact_ended()."""
        await timeutil.sleep_until(contact.end_time)
        self.predicted_contact_ended(contact.rx_node, contact.end_time)

    async def schedule_graph_change(self, new_cgr_data):
        """Wait until a graph change and trigger graph_changed()."""
        await timeutil.sleep_until(new_cgr_data.start_time)
        self.graph_changed(new_cgr_data)

    def initialize_cgr_data(self, ptvg, update_min_interval, own_eid):
        """Initialize and return the graph data for the routing algorithm."""
        raise NotImplementedError()

    def route_generator_factory(self, gd, source_eid, dest_eid, excluded_eids):
        """Initialize a new route generator for the routing algorithm."""
        raise NotImplementedError()

    def predicted_contact_ended(self, rx_node, end_time):
        """Perform actions necessary when a predicted contact has ended."""
        if self.re_schedule_delayed:
            # NOTE: queue has to stay, it may be still referenced,
            #       e.g. in get_messages.
            for cur_queue_contact_end, cur_queue in self.tx_queues[rx_node]:
                if cur_queue_contact_end > end_time:
                    # queue ends later
                    break
                # queue ends earlier
                while cur_queue:
                    message, route = cur_queue.popleft()
                    self.re_schedule(message, route)

    def graph_changed(self, new_cgr_data):
        """Perform actions necessary when the TVG prediction changed."""
        # Update the contact_volume_usage stats
        for contact_tuple in new_cgr_data.contact_plan:
            if new_cgr_data.start_time > contact_tuple.start_time:
                # do not update old or running contacts
                continue
            cvu = self.get_cvu(contact_tuple)
            cvu.predicted = (
                (contact_tuple.end_time - contact_tuple.start_time) *
                contact_tuple.bit_rate
            )
        # Re-schedule bundles that are overbooking the graph
        if not self.re_schedule_overbooked:
            return
        time = asyncio.get_running_loop().time()
        for contact_tuple in new_cgr_data.contact_plan:
            # other mechanisms take care of expired and running contacts
            if contact_tuple.start_time <= time:
                continue
            # check volume usage, reschedule if exceeds
            cvu = self.get_cvu(contact_tuple)
            if cvu.used > cvu.predicted and contact_tuple.tx_node == self.eid:
                for end_time, cand in self.tx_queues[contact_tuple.rx_node]:
                    if end_time == contact_tuple.end_time:
                        queue = cand
                volume_to_be_re_scheduled = cvu.used - cvu.predicted
                # remove bundles at the end of the contact
                while volume_to_be_re_scheduled > 0 and queue:
                    message, route = queue.pop()
                    volume_to_be_re_scheduled -= (
                        _get_estimated_volume_consumption(message.size)
                    )
                    self.re_schedule(message, route)

    def re_schedule(self, message, route):
        """Re-schedule a bundle previously scheduled for the given route."""
        # Expiry check
        loop_time = asyncio.get_running_loop().time()
        if loop_time > message.deadline:
            self._drop_copy(message)
            return

        # Revert changes to the buffer and scheduling count.
        assert self.sched_refcount[message] > 0
        self.sched_refcount[message] -= 1
        if self.sched_refcount[message]:
            # NOTE Re-scheduling for still-scheduled messages is not supported.
            return

        # NOTE: No drop event here, this will be invoked by store_and_schedule
        # if necessary.
        if message in self.buf:
            self.buf.remove(message)

        evc = _get_estimated_volume_consumption(message.size)
        self.node_tx_queue_volumes[route.neighbor_eid] -= evc

        # Revert changes to volume usage record
        self.update_cvu(
            route.contact_path,
            -_get_estimated_volume_consumption(message.size),
        )

        # Call store_and_schedule as if the message was just injected here.
        self.store_and_schedule(message, None)

    def _initialize_queues(self, ptvg, eid, contact_tuple_list):
        tx_queues = {}
        node_tx_queue_volumes = {}
        for (tx_node, rx_node), edge_contacts in ptvg.edges.items():
            if tx_node != eid:
                continue
            # The TX queue has to remember the contact for which the bundle
            # has been scheduled, to be able to control possible max. volume
            # exhaustion. Thus, it is a list of tuples (LTT, bundle-queue),
            # where LTT is the latest applicable transmission time (i.e.
            # the end-time of the contact for which the bundle has been
            # scheduled. If a contact ends, this list is checked for issues.
            # If a bundle could not be transmitted during the contact, it will
            # either be re-scheduled using the CGR procedures or simply remain
            # in the queue, according to the `re_schedule_delayed` parameter.
            tx_queues[rx_node] = [
                (contact.end_time, collections.deque())
                for contact in sorted(
                    edge_contacts,
                    key=lambda c: c.start_time,
                )
            ]
            node_tx_queue_volumes[rx_node] = 0.0
        self.tx_queues = tx_queues
        self.node_tx_queue_volumes = node_tx_queue_volumes
        # NOTE: This value has to be cached across all graph changes.
        # Check the re_schedule_overbooked parameter for an approach to deal
        # with it changing during the simulation run.
        # TUPLES: (predicted, used) for each contact
        contact_volume_usage = {}
        for contact_tuple in contact_tuple_list:
            key = (contact_tuple.tx_node, contact_tuple.rx_node)
            if key not in contact_volume_usage:
                contact_volume_usage[key] = {}
            # 3.2.6.8.8
            contact_volume_usage[key][contact_tuple.end_time] = SABRCVU(
                predicted=(
                    (contact_tuple.end_time - contact_tuple.start_time) *
                    contact_tuple.bit_rate
                ),
                used=0.0,
            )
        self.contact_volume_usage = contact_volume_usage

    def get_cvu(self, contact):
        """Get the SABRCVU instance (volume usage) for the given contact."""
        return self.contact_volume_usage[
            (contact.tx_node, contact.rx_node)
        ][contact.end_time]

    def update_cvu(self, contact_path, size):
        """Increment the volume usage for the given contact by size."""
        # 3.2.8.1.2
        for contact in contact_path:
            cvu = self.get_cvu(contact)
            cvu.used += size
            assert cvu.used >= 0

    def add_to_tx_queue(self, message, route):
        """Add the given bundle to the TX queue for the given route."""
        contact = route.contact_path[0]
        for end_time, candidate in self.tx_queues[contact.rx_node]:
            if end_time == contact.end_time:
                queue = candidate
                break
        queue.append((message, route))
        evc = _get_estimated_volume_consumption(message.size)
        self.update_cvu(route.contact_path, evc)
        self.node_tx_queue_volumes[contact.rx_node] += evc

    def get_tx_queue_volume(self, eid):
        """Get the volume (size) of the TX queue to the given EID."""
        return self.node_tx_queue_volumes[eid]

    def get_max_tx_volume(self, contact):
        """Get the maximum usable (remaining) volume for the given contact."""
        cvu = self.get_cvu(contact)
        if cvu.used > cvu.predicted:
            return 0.0
        return cvu.predicted - cvu.used

    def store_and_schedule(self, message, tx_node):
        """Store the provided message in the buffer and try to schedule it."""
        loop_time = asyncio.get_running_loop().time()
        assert loop_time >= message.start_time
        assert loop_time <= message.deadline
        if message in self.sched_refcount and self.sched_refcount[message]:
            # We have it already -> reject
            self.event_dispatcher.message_rejected(self, message)
            return
        if tx_node and self.reject_looping and message in self.known_bundles:
            # We know it already -> reject
            self.event_dispatcher.message_rejected(self, message)
            return
        # get the correct graph...
        gd = self.cgr_data.get_entry_and_drop_predecessors(loop_time)
        # cache_before = (
        #     len(gd.route_lists[message.destination])
        #     if message.destination in gd.route_lists else 0
        # )
        order_routes = self.max_order_routes
        if self.no_alt_for_looping and message in self.known_bundles:
            order_routes = 1  # NOTE: wanted also on re-scheduling??
        routes = self.routing_algorithm(
            gd=gd,
            bundle=message,
            cur_eid=self.eid,
            cur_time=loop_time,
            excluded_eids=([tx_node.eid] if tx_node else []),
            tx_queue_volume_f=self.get_tx_queue_volume,
            max_transmission_volume_f=self.get_max_tx_volume,
            route_generator_factory=self.route_generator_factory,
            max_routes=self.max_routes,
            max_order_routes=order_routes,
        )
        # cache_after = len(gd.route_lists[message.destination])
        if routes:
            for route in routes:
                self.add_to_tx_queue(message, route)
            cur_refcount = self.sched_refcount.get(message, 0)
            assert cur_refcount == 0  # NOTE: modify if implementing re-sched.
            self.sched_refcount[message] = cur_refcount + len(routes)
            # Accepted!
            self.buf.add(message)
            # Message has been scheduled
            self.event_dispatcher.message_scheduled(self, message)
            # In case get_messages is waiting, unblock it.
            self.set_message_scheduled()
        else:
            # No route was found -> reject
            self.event_dispatcher.message_rejected(self, message)

    async def get_messages(self, rx_node):
        """Asynchronously yield messages to be transmitted."""
        # we run in an endless loop - even if no messages can be sent
        # anymore, we await the next reception event
        queue_list = self.tx_queues[rx_node.eid]
        while True:
            while True:
                # We send all messages queued for the neighbor node.
                # Just get the first message from the first queue.
                # NOTE: It may happen by this mechanism that a bundle which is
                # scheduled for a later contact is transmitted earlier
                # (expected behavior of SABR) and this transmission blocks the
                # TRX for a bundle that is scheduled while the bundle is being
                # transmitted, which SABR is not aware of. This may lead to
                # re-scheduling the bundle just scheduled.
                # Example: Contacts [c1, c2], Bundle b1 scheduled at t0 for c2,
                #   b1 is transmitted at t1-t3 in c1, Bundle b2 scheduled at t2
                #   in c1 for c1, c1 ends at t4, Bundle b2 re-scheduled at t4.
                message = None
                for cur_queue_contact_end, cur_queue in queue_list:
                    if cur_queue:
                        message, route = cur_queue.popleft()
                        break
                if not message:
                    # All queues empty, no bundle found.
                    break
                if not self.buf.contains(message):
                    # message may be dropped due to expiry
                    continue
                try:
                    yield message, None
                except GeneratorExit:
                    # This is a pretty standard case as we do best-effort
                    # transmission of everything in the queue for the
                    # neighboring network node.
                    # Thus, we prepend the bundle to the existing queue.
                    # NOTE: It may get evicted later if re_schedule_delayed
                    # is set. This is performed at the predicted contact end.
                    cur_queue.appendleft((message, route))
                    raise
                else:
                    self._message_transmitted(message, rx_node)
            await self.wait_until_new_message_scheduled()

    def _message_transmitted(self, message, rx_node):
        self._drop_copy(message)
        evc = _get_estimated_volume_consumption(message.size)
        self.node_tx_queue_volumes[rx_node.eid] -= evc
        if self.track_looping and message not in self.known_bundles:
            self.known_bundles.add(message)

    def _drop_copy(self, message):
        assert self.sched_refcount[message] > 0
        self.sched_refcount[message] -= 1
        if not self.sched_refcount[message]:
            # Message was sent via all channels, drop it
            if message in self.buf:
                self.event_dispatcher.message_deleted(self, message)
                self.buf.remove(message)


# 3.2.8.1
def sabr(gd, bundle, cur_eid, cur_time, excluded_eids,
         tx_queue_volume_f, max_transmission_volume_f,
         route_generator_factory, max_routes, max_order_routes):
    """Return the chosen route based on SABR 3.2.8.1.

    Args:
        - gd: The graph data object for the time at which routing is performed.
        - bundle: The bundle to be routed.
        - cur_eid: The EID of the node at which the bundle is routed.
        - cur_time: The timestamp at which routing is performed.
        - excluded_eids: An iterable of EIDs to be excluded from routes.
        - tx_queue_volume_f: A function mapping an EID to a TX queue.
        - max_transmission_volume_f: A function returning the maximum
                                     transmission volume for a given contact.
        - route_generator_factory: The factory function of the route generator,
                                   defining how next-best routes are selected.
        - max_routes: The maximum number of routes to be generated.
        - max_order_routes: The maximum number of candidate routes to be
                            compared against each other.
    """
    candidate_routes = get_candidate_route_gen(
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

    best_pbat = math.inf
    best_route = None
    # 3.2.8.1.1-4 Route ranking using projected bundle arrival time (3.2.6.7)
    for i, (candidate, pbat) in enumerate(candidate_routes):
        # 3.2.8.1.4 a) 1)
        if pbat < best_pbat:
            best_pbat = pbat
            best_route = candidate
        elif abs(pbat - best_pbat) < 1e-6:
            # 3.2.8.1.4 a) 2)
            if len(candidate.contact_path) < len(best_route.contact_path):
                best_pbat = pbat
                best_route = candidate
            elif len(candidate.contact_path) == len(best_route.contact_path):
                # 3.2.8.1.4 a) 3)
                if candidate.end_time > best_route.end_time:
                    best_pbat = pbat
                    best_route = candidate
                elif abs(candidate.end_time - best_route.end_time) < 1e-6:
                    # 3.2.8.1.4 a) 4)
                    if candidate.entry_vid < best_route.entry_vid:
                        best_pbat = pbat
                        best_route = candidate
        if i >= max_order_routes:
            break
    return [best_route] if best_route else []


# 2.4.3
def _get_estimated_volume_consumption(bundle_size):
    # NOTE: The simulator assumes the size already includes the CL overhead.
    return bundle_size


# 3.2.6.2 a)
def _get_adjusted_start_time(contact, cur_time):
    return contact.start_time if contact.start_time > cur_time else cur_time


# 3.2.6.2
def _get_backlog_lien(node_contact_list, node_tx_queue_evc,
                      initial_contact, cur_time):
    # b)
    applicable_backlog = 0
    applicable_backlog += node_tx_queue_evc
    # c)
    # TODO: Evaluate turning this into a generator function that exits early.
    applicable_prior_contacts = (
        c
        for c in node_contact_list
        if c.end_time > cur_time and c.start_time < initial_contact.start_time
    ) if initial_contact.start_time > cur_time else []
    # d), e), f)
    applicable_backlog_relief = 0
    for c in applicable_prior_contacts:
        applicable_backlog_relief += (
            (c.end_time - _get_adjusted_start_time(c, cur_time)) * c.bit_rate
        )
    # g)
    residual_backlog = applicable_backlog - applicable_backlog_relief
    if residual_backlog < 0:
        residual_backlog = 0
    # h)
    backlog_lien = residual_backlog / initial_contact.bit_rate
    return backlog_lien


# 2.4.2
def _get_owlt_margin(contact):
    # NOTE: We assume the OWLT (contact delay) does not change during contact.
    return 0


# 3.2.6.6
def _get_last_byte_arrival_time(contact, bundle_size,
                                first_byte_transmission_time):
    # 3.2.6.4
    applicable_radiation_latency = (
        _get_estimated_volume_consumption(bundle_size) /
        contact.bit_rate
    )
    last_byte_transmission_time = (
        first_byte_transmission_time +
        applicable_radiation_latency
    )
    # 3.2.6.6
    return (
        last_byte_transmission_time +
        contact.delay +
        _get_owlt_margin(contact)
    )


def _get_last_byte_arrival_times(contact_path, bundle_size,
                                 earliest_transmission_opportunity):
    # Assert that the route is non-empty
    assert contact_path
    # Calculate LBAT for first contact as it uses ETO as FBTT (3.2.6.3)
    last_byte_arrival_times = [
        _get_last_byte_arrival_time(
            contact_path[0],
            bundle_size,
            earliest_transmission_opportunity,
        )
    ]
    # Iteratively update the LBAT until we're at the end of the route.
    for contact in contact_path[1:]:
        last_byte_arrival_times.append(_get_last_byte_arrival_time(
            contact,
            bundle_size,
            # 3.2.6.3
            (
                contact.start_time
                if contact.start_time > last_byte_arrival_times[-1]
                else last_byte_arrival_times[-1]
            ),
        ))
    return last_byte_arrival_times


# 3.2.6.8.10
def _get_route_volume_limit(contact_path, effective_stop_times,
                            last_byte_arrival_times,
                            earliest_transmission_opportunity,
                            max_transmission_volume_f):
    route_volume_limit = math.inf
    for i, contact in enumerate(contact_path):
        # 3.2.6.8.5, 3.2.6.3
        effective_start_time = contact.start_time
        if i > 0 and last_byte_arrival_times[i - 1] > effective_start_time:
            effective_start_time = last_byte_arrival_times[i - 1]
        elif earliest_transmission_opportunity > effective_start_time:
            effective_start_time = earliest_transmission_opportunity
        # 3.2.6.8.6
        effective_stop_time = effective_stop_times[i]
        # 3.2.6.8.7
        effective_duration = effective_stop_time - effective_start_time
        # 3.2.6.8.8
        # TODO: Evaluate replacing this by the volume (or math.inf).
        maximum_transmission_volume = max_transmission_volume_f(contact)
        # 3.2.6.8.9
        effective_volume_limit = effective_duration * contact.bit_rate
        if maximum_transmission_volume < effective_volume_limit:
            effective_volume_limit = maximum_transmission_volume
        # 3.2.6.8.10
        if effective_volume_limit < route_volume_limit:
            route_volume_limit = effective_volume_limit
    return route_volume_limit


# 3.2.4.2
def _get_best_case_delivery_time(contact_path, cur_time):
    # 3.2.4.1.1
    cur_earliest_arrival_time = cur_time
    for contact in contact_path:
        cur_earliest_arrival_time = _get_earliest_arrival_time(
            contact,
            cur_earliest_arrival_time,
        )
    return cur_earliest_arrival_time


# 3.2.6.9 - determine candidate routes
def get_candidate_route_gen(gd, bundle, cur_eid, cur_time, excluded_eids,
                            tx_queue_volume_f, max_transmission_volume_f,
                            route_generator_factory, max_routes):
    """Yield candidate routes as per SABR 3.2.6.9.

    Args:
        - gd: The graph data object for the time at which routing is performed.
        - bundle: The bundle to be routed.
        - cur_eid: The EID of the node at which the bundle is routed.
        - cur_time: The timestamp at which routing is performed.
        - excluded_eids: An iterable of EIDs to be excluded from routes.
        - tx_queue_volume_f: A function mapping an EID to a TX queue.
        - max_transmission_volume_f: A function returning the maximum
                                     transmission volume for a given contact.
        - route_generator_factory: The factory function of the route generator,
                                   defining how next-best routes are selected.
        - max_routes: The maximum number of routes to be generated.

    """
    # route_lists as well as route_gens cache specific properties:
    # The former are already-generated "best routes", in-order. The latter
    # is a generator performing Yen's k-shortest-path algorithm, holding the
    # current state of that algorithm in local variables, such that the
    # next-best route can easily generated invoking next() on the genrator.
    # NOTE: Both variables **must** be invalidated on any graph change!
    if bundle.destination not in gd.route_gens:
        gd.route_gens[bundle.destination] = route_generator_factory(
            gd,
            cur_eid,
            bundle.destination,
            excluded_eids,
        )
        gd.route_lists[bundle.destination] = []
    # This function combines iterating through route_list and then adding and
    # returning new routes from the route generator into a single generator.
    route_wrapper_gen = _route_wrapper(
        gd,
        bundle.destination,
        cur_time,
        max_routes=max_routes,
    )

    # Pre-filtering according to 3.2.6.2
    for route in route_wrapper_gen:

        # logger.debug("  -> Considering route to %s: %s", bundle.destination,
        #              str(route.contact_path))

        # 3.2.6.2 a)
        adj_start_time = cur_time
        if route.start_time > adj_start_time:
            adj_start_time = route.start_time

        # 3.2.6.9. a)
        best_case_delivery_time = _get_best_case_delivery_time(
            route.contact_path,
            cur_time,
        )
        if best_case_delivery_time > bundle.deadline:
            continue

        # 3.2.6.9. b), 3.2.6.9. c)
        if route.neighbor_eid in excluded_eids:
            continue

        # 3.2.6.2 i)
        earliest_transmission_opportunity = (
            adj_start_time +
            _get_backlog_lien(
                gd.neighbor_contact_lists[route.neighbor_eid],
                tx_queue_volume_f(route.neighbor_eid),
                route.contact_path[0],
                cur_time,
            )
        )
        # 3.2.6.9. d)
        # NOTE: This also checks the volume limit of the initial contact.
        if earliest_transmission_opportunity > route.contact_path[0].end_time:
            continue

        # 3.2.6.9. e)
        last_byte_arrival_times = _get_last_byte_arrival_times(
            route.contact_path,
            bundle.size,
            earliest_transmission_opportunity,
        )
        # 3.2.6.7
        # "the contact immediately preceding the terminal vertex contact"
        # is equal to the last contact in route.contact_path.
        if last_byte_arrival_times[-1] > bundle.deadline:
            continue

        # 3.2.6.9. f), 3.2.6.8.11
        route_volume_limit = _get_route_volume_limit(
            route.contact_path,
            route.effective_stop_times,
            last_byte_arrival_times,
            earliest_transmission_opportunity,
            max_transmission_volume_f,
        )
        if route_volume_limit <= 0:
            continue

        # 3.2.6.9. g)
        # NOTE: Fragmentation is assumed disabled.
        evc = _get_estimated_volume_consumption(bundle.size)
        if route_volume_limit <= evc:
            continue

        # logger.debug("  -> Returning route to %s: %s", bundle.destination,
        #              str(route.contact_path))
        # 3.2.6.9. h)
        # Return the route and the projected bundle arrival time
        yield route, last_byte_arrival_times[-1]

    logger.info("  -> Route list to %s exhausted!", bundle.destination)


def _route_wrapper(gd, destination, time, max_routes):
    route_list = gd.route_lists[destination]

    # Pre-filter to reduce amount of work
    # NOTE: This modifies route_list in-place!
    route_list[:] = [r for r in route_list if r.end_time >= time]

    for route in route_list:
        yield route

    max_routes -= len(route_list)
    if max_routes <= 0:
        return

    route_gen = gd.route_gens[destination]

    for i, contact_path in enumerate(route_gen):
        route = _get_route(contact_path)
        route_list.append(route)
        yield route
        max_routes -= 1
        if max_routes <= 0:
            break


def _get_route(contact_path):
    route_start_time = contact_path[0].start_time

    # 3.2.6.8.6
    min_stop_time = math.inf
    effective_stop_times = []
    for contact in reversed(contact_path):
        if contact.end_time < min_stop_time:
            min_stop_time = contact.end_time
        effective_stop_times.append(min_stop_time)
    # Reverse it, such that each element corresponds to a path entry.
    effective_stop_times = list(reversed(effective_stop_times))

    # Determine the time at which the route becomes invalid.
    route_end_time = math.inf
    for i, contact in enumerate(contact_path):
        if contact.end_time < route_end_time:
            route_end_time = contact.end_time

    return Route(
        start_time=route_start_time,
        end_time=route_end_time,
        neighbor_eid=contact_path[0].rx_node,
        contact_path=contact_path,
        effective_stop_times=effective_stop_times,
        entry_vid=hash(contact_path[0]),
    )


def _get_earliest_arrival_time(contact, earliest_arrival_time_at_tx_node):
    # 3.2.4.1.1
    earliest_transmission_time = contact.start_time
    if earliest_arrival_time_at_tx_node > earliest_transmission_time:
        earliest_transmission_time = earliest_arrival_time_at_tx_node
    # 3.2.4.1.2
    earliest_arrival_time = (
        earliest_transmission_time +
        contact.delay +
        _get_owlt_margin(contact)
    )
    return earliest_arrival_time
