# encoding: utf-8

"""Provides a time-varying implementation of Dijkstra's algorithm."""

import heapq


class TVDijkstraResult(object):
    """Represents a result of a tvdijkstra graph analysis."""

    def __init__(self, metrics):
        self.metrics = metrics

    def is_reachable(self, destination):
        """Get a bool indicating whether the given vertex is reachable."""
        return self.metrics[destination].predecessor is not None

    def get_metrics(self, destination):
        """Get all stored metrics for the given vertex."""
        return self.metrics[destination]

    def get_path(self, destination):
        """Obtain the path to the given destination as a 4-tuple.

        Returns: A tuple of (length, vertex, contact instance used to arrive,
                 and EAT at the vertex).

        """
        cnt = 0
        cur_node = destination
        path = []
        taken_contacts = []
        eat = []
        while self.metrics[cur_node].predecessor is not None:
            path.append(cur_node)
            taken_contacts.append(self.metrics[cur_node].taken_contact)
            eat.append(self.metrics[cur_node].eat)
            cur_node = self.metrics[cur_node].predecessor
            cnt += 1
        path.append(cur_node)
        return cnt, reversed(path), reversed(taken_contacts), reversed(eat)

    def __repr__(self):
        """Get a printable representation of this class."""
        return repr(self.metrics)


class NodeMetrics(object):
    """Provides metrics for a node in a tvdijkstra graph analysis."""

    __slots__ = (
        "predecessor",
        "taken_contact",
        "hops",
        # earliest arrival time
        "eat",
    )

    def __init__(self, *args, **kwargs):
        for i, value in enumerate(args):
            setattr(self, self.__slots__[i], value)
        for key, value in kwargs.items():
            setattr(self, key, value)


def tvdijkstra(simple_ptvg, source_node, dest_node=None, start_time=0.0,
               node_blacklist=None, contact_blacklist=None):
    """Time-variant implementation of Dijkstra's algorithm.

    Distance values are calculated by invoking dist_func with the
    current distance and the start and end times of a possible contact.

    The start times of contacts which are considered have to be greater than
    the time to reach the currently considered node from its predecessor.

    used_capacities should be a dict, associating contacts (which are
    keys) to the capacity already occupied within the contact.

    If the blacklist argument is provided, the contained vertices will not be
    evaluated. If dest is provided, the specified vertex will be considered
    as destination and the algorithm stops if the shortest path was found.

    NOTE: This does not currently support:
          - delay (transmission delay specific to each contact)
          - overlapping contacts on the path

    """
    metrics = {
        key: NodeMetrics(
            predecessor=None,
            taken_contact=None,
            hops=-1,
            eat=float("inf"),
        )
        for key in simple_ptvg.vertices
    }
    metrics[source_node].hops = 0
    metrics[source_node].eat = start_time
    # the priority queue is used to access all elements ordered by distance
    queue = list()
    heapq.heappush(queue, (0.0, source_node))
    # in addition to the priority queue, we store a set of vertices to evaluate
    todo = set(simple_ptvg.vertices.keys()) - (set(node_blacklist) or set())
    while queue:
        _, cur = heapq.heappop(queue)
        if dest_node and cur == dest_node:
            break
        if cur not in todo:
            continue
        else:
            todo.remove(cur)
        # obtain metrics tuple
        cur_metrics = metrics[cur]
        # traverse all neighbors of the current vertex
        for neigh in simple_ptvg.vertices[cur]:
            if neigh not in todo:
                continue
            neigh_metrics = metrics[neigh]
            # traverse all contacts of the current edge (from cur to neigh)
            for contact in simple_ptvg.edges.get((cur, neigh), []):
                if contact in contact_blacklist:
                    continue
                if contact.bit_rate < 1e-6:
                    continue
                # if the message arrives after the contact ends,
                # skip evaluating the contact
                if contact.end_time <= cur_metrics.eat:
                    continue
                # 3.2.4.1.1
                earliest_transmission_time = contact.start_time
                if cur_metrics.eat > earliest_transmission_time:
                    earliest_transmission_time = cur_metrics.eat
                # 3.2.4.1.2
                next_node_earliest_arrival_time = (
                    earliest_transmission_time +
                    contact.delay +
                    0.0  # OWLT margin
                )
                # if the distance is smaller than before, update the evaluated
                # node with the new path
                delta = next_node_earliest_arrival_time - neigh_metrics.eat
                if delta < 0 or (delta < 1e-3 and
                                 cur_metrics.hops + 1 < neigh_metrics.hops):
                    neigh_metrics.predecessor = cur
                    neigh_metrics.taken_contact = contact
                    neigh_metrics.hops = (cur_metrics.hops + 1)
                    neigh_metrics.eat = next_node_earliest_arrival_time
                    heapq.heappush(queue, (
                        next_node_earliest_arrival_time,
                        neigh,
                    ))
                # NOTE: That we can do the following is the main advantage of
                # this algorithm: The contacts are ordered, so we do not have
                # to check the next one. (It would just be worse...)
                break

    return TVDijkstraResult(metrics)
