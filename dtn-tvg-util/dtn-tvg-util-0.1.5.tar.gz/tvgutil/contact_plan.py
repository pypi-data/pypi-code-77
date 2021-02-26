#!/usr/bin/env python
# encoding: utf-8

"""
This module provides two basic contact representations and contact plan
conversion methods.

Formerly, there was only one type of contact plan as no routing algorithms
were tested, but only theoretical analyses of the network graph had been
performed. However, this has changed with the addition of more and more
simulation functionalities.

Now, there is a clear separation between two types of contact plan:
    * Factual Contact Plan (FCP): A list of Contact instances, representing
      the actually-happening contacts (as they are observed by the nodes).
      This representation could be obtained, for example, by observing a real
      network topology and recording the concrete links.
    * Predicted Contact Plan (PCP): A list of PredictedContact instances,
      representing the contacts predicted by a node.
      Every node may have an individual PCP. This representation is supplied
      to routing algorithms such as CGR.

In fully deterministic scenarios, a PCP can be converted into an FCP and
vice versa. In that case, the predicted characteristics are equal to the
factual characteristics and there is only one generation of predicted
characteristics.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import bisect
import collections
import random
import attr

from tvgutil import util


class InvalidContactPlanError(ValueError):
    """
    An error to be raised if an invalid contact plan is provided
    to a function of this module.
    """


# namedtuple representation, kept for compatibility
SimpleContactTuple = collections.namedtuple(
    "SimpleContactTuple", [
        "tx_node",
        "rx_node",
        "start_time",
        "end_time",
        "bit_rate",
        "bit_error_rate",
        "delay",
    ]
)

# namedtuple representation, kept for compatibility
SimplePredictedContactTuple = collections.namedtuple(
    "SimplePredictedContactTuple", [
        "tx_node",
        "rx_node",
        "start_time",
        "end_time",
        "bit_rate",
        "probability",
        "delay",
    ]
)


@attr.s(slots=True)
class ContactCharacteristics(object):
    """Represents characteristics of a factual contact in a specific interval.

    NOTE that these characteristics may be only valid for a specific
    sub-timeframe (interval) _during_ the contact. This timeframe starts at
    the timestamp indicated by `starting_at` and ends at the timestamp
    indicated by the `starting_at`-Attribute of the next list entry.

    Attributes:
        starting_at: The start time for this set of characteristics during
            the contact, i.e. the time they supersede the previous set.
        bit_rate: The transmission rate for the contact, in bit/s.
        bit_error_rate: The residual bit error rate (probability) during the
            contact, i.e. after link-layer corrections; element of [0; 1].
        delay: The transmission delay, in seconds.

    """

    starting_at = attr.ib(default=0.0)
    bit_rate = attr.ib(default=0.0)
    bit_error_rate = attr.ib(default=0.0)
    delay = attr.ib(default=0.0)

    @bit_rate.validator
    def _validate_bit_rate(self, _, value):
        if value < 0.0:
            raise ValueError("bit_rate may not be negative")

    @bit_error_rate.validator
    def _validate_bit_error_rate(self, _, value):
        if value < 0.0:
            raise ValueError("bit_error_rate may not be < 0.0")
        elif value > 1.0:
            raise ValueError("bit_error_rate may not be > 1.0")

    @delay.validator
    def _validate_delay(self, _, value):
        if value < 0.0:
            raise ValueError("delay may not be negative")


@attr.s(slots=True)
class Contact(object):
    """Represents a factual contact, which is e.g. applicable for simulation.

    Attributes:
        tx_node: The transmitting node (data depart from here).
        rx_node: The receiving node (data arrive here).
        start_time: The start timestamp of the contact in seconds.
        end_time: The end timestamp of the contact in seconds.
        characteristics: A list of ContactCharacteristics instances,
            indicating the observed/factual characteristics of the contact.
            These values may change during the contact.
            Subsequent entries override each other. The validity period is
            defined by the `starting_at` attribute.

    """

    tx_node = attr.ib()
    rx_node = attr.ib()
    start_time = attr.ib()
    end_time = attr.ib()
    characteristics = attr.ib(
        default=attr.Factory(lambda: [ContactCharacteristics()]),
        repr=lambda v: "list(<len=" + str(len(v)) + ">)",
    )

    @start_time.validator
    def _validate_start(self, _, value):
        if value < 0.0:
            raise ValueError("start_time has to be >= 0")

    @end_time.validator
    def _validate_end(self, _, value):
        if value < self.start_time:
            raise ValueError("end_time has to be >= start_time")

    @characteristics.validator
    def _validate_characteristics(self, _, value):
        if not isinstance(value, list):
            raise ValueError("characteristics has to be an instance of list")
        if not value:
            raise ValueError("characteristics cannot be empty")
        if value[0].starting_at > self.start_time:
            raise ValueError(
                "characteristics has to contain an element valid"
                "from the start"
            )
        last_starting = 0.0
        for char in value:
            if char.starting_at < last_starting:
                raise ValueError(
                    "characteristics have to be provided in order"
                )
            last_starting = char.starting_at

    @classmethod
    def simple(cls, tx_node, rx_node, start_time, end_time,
               bit_rate=0.0, bit_error_rate=0.0, delay=0.0):
        """Creates a new instance using deprecated simple syntax."""
        return cls(tx_node, rx_node, start_time, end_time, [
            ContactCharacteristics(
                starting_at=start_time,
                bit_rate=bit_rate,
                bit_error_rate=bit_error_rate,
                delay=delay,
            )
        ])

    def _characteristics_index_at(self, time):
        if not time:
            return 0
        return bisect.bisect(
            util.KeyedListView(
                self.characteristics,
                key=lambda x: x.starting_at,
            ),
            time,
        ) - 1

    def get_characteristics_at(self, time):
        """Returns the characteristics at the given timestamp in-contact."""
        index = self._characteristics_index_at(time)
        if index < 0:
            raise ValueError("no valid characteristics entry found")
        return self.characteristics[index]

    def characteristics_in_time_frame(self, start, end):
        """Yields a list of tuples with valid characteristic sub-intervals."""
        cur_idx = self._characteristics_index_at(start)
        if cur_idx < 0:
            raise ValueError("no valid characteristics entry found")
        cur_start = start
        while (cur_idx + 1 < len(self.characteristics) and
               self.characteristics[cur_idx + 1].starting_at < end):
            cur_end = self.characteristics[cur_idx + 1].starting_at
            yield (cur_start, cur_end, self.characteristics[cur_idx])
            cur_start = cur_end
            cur_idx += 1
        yield (cur_start, end, self.characteristics[cur_idx])

    def to_simple(self, characteristics_at=None):
        """Returns a simple namedtuple representation."""
        char = self.get_characteristics_at(characteristics_at)
        return SimpleContactTuple(
            tx_node=self.tx_node,
            rx_node=self.rx_node,
            start_time=self.start_time,
            end_time=self.end_time,
            bit_rate=char.bit_rate,
            bit_error_rate=char.bit_error_rate,
            delay=char.delay,
        )

    @classmethod
    def from_list(cls, lst):
        """Creates a new instance from a list."""
        return cls(lst[0], lst[1], lst[2], lst[3], [
            ContactCharacteristics(*char_lst)
            for char_lst in lst[4]
        ])

    def to_list(self):
        """Converts the instance to a list representation for serialization."""
        return [
            self.tx_node,
            self.rx_node,
            self.start_time,
            self.end_time,
            [
                [
                    char.starting_at,
                    char.bit_rate,
                    char.bit_error_rate,
                    char.delay,
                ]
                for char in self.characteristics
            ],
        ]

    @classmethod
    def from_v1(cls, lst):
        """Creates a new instance from a v1 representation provided as list."""
        return cls.simple(*lst)

    def basic_tuple(self):
        """Returns a 4-tuple of the basic contact properties."""
        return (self.tx_node, self.rx_node, self.start_time, self.end_time)


@attr.s(slots=True)
class PredictedContactCharacteristics(object):
    """Represents predicted characteristics of a contact in a time interval.

    NOTE that these characteristics may be only valid for a specific
    sub-timeframe (interval) _during_ the contact. This timeframe starts at
    the timestamp indicated by `starting_at` and ends at the timestamp
    indicated by the `starting_at`-Attribute of the next list entry.

    Attributes:
        starting_at: The start time for this set of characteristics during
            the contact, i.e. the time they supersede the previous set.
        bit_rate: The predicted mean data rate during the interval, in bit/s.
        delay: The transmission delay, in seconds.

    """

    starting_at = attr.ib(default=0.0)
    bit_rate = attr.ib(default=0.0)
    delay = attr.ib(default=0.0)

    @bit_rate.validator
    def _validate_bit_rate(self, _, value):
        if value < 0.0:
            raise ValueError("bit_rate may not be negative")

    @delay.validator
    def _validate_delay(self, _, value):
        if value < 0.0:
            raise ValueError("delay may not be negative")


@attr.s(slots=True)
class PredictedContactGeneration(object):
    """Represents a single contact prediction which is available at a time.

    Attributes:
        valid_from: The timestamp from which the prediction generation becomes
            valid, i.e. the time the prediction becomes available.
        probability: The predicted overall contact probability, i.e. how likely
            it is that the contact will be observed in reality.
        characteristics: A list of PredictedContactCharacteristics instances,
            indicating the predicted characteristics of the contact.
            These values may change during the contact.
            Subsequent entries override each other. The validity period is
            defined by the `starting_at` attribute.

    """

    valid_from = attr.ib(default=0.0)
    probability = attr.ib(default=1.0)
    characteristics = attr.ib(
        default=attr.Factory(lambda: [PredictedContactCharacteristics()]),
        repr=lambda v: "list(<len=" + str(len(v)) + ">)",
    )

    @probability.validator
    def _validate_probability(self, _, value):
        if value < 0.0:
            raise ValueError("probability may not be < 0.0")
        elif value > 1.0:
            raise ValueError("probability may not be > 1.0")

    @characteristics.validator
    def _validate_characteristics(self, _, value):
        if not isinstance(value, list):
            raise ValueError("characteristics has to be an instance of list")
        if not value:
            raise ValueError("characteristics must not be empty")
        last_starting = 0.0
        for char in value:
            if char.starting_at < last_starting:
                raise ValueError(
                    "characteristics have to be provided in order"
                )
            last_starting = char.starting_at

    def _characteristics_index_at(self, time):
        if not time:
            return 0
        return bisect.bisect(
            util.KeyedListView(
                self.characteristics,
                key=lambda x: x.starting_at,
            ),
            time,
        ) - 1

    def get_characteristics_at(self, time):
        """Returns the characteristics at the given timestamp in-contact."""
        index = self._characteristics_index_at(time)
        if index < 0:
            raise ValueError("no valid characteristics entry found")
        return self.characteristics[index]

    def characteristics_in_time_frame(self, start, end):
        """Yields a list of tuples with valid characteristic sub-intervals."""
        cur_idx = self._characteristics_index_at(start)
        if cur_idx < 0:
            raise ValueError("no valid characteristics entry found")
        cur_start = start
        while (cur_idx + 1 < len(self.characteristics) and
               self.characteristics[cur_idx + 1].starting_at < end):
            cur_end = self.characteristics[cur_idx + 1].starting_at
            yield (cur_start, cur_end, self.characteristics[cur_idx])
            cur_start = cur_end
            cur_idx += 1
        yield (cur_start, end, self.characteristics[cur_idx])

    def _get_attr_duration_sum(self, getter, start_time, end_time):
        value = 0.0
        for i, char in enumerate(self.characteristics):
            # The first characteristics entry might be valid earlier than the
            # contact starts. This ensures we only take into account the
            # contact time frame itself.
            char_start = max(
                start_time,
                char.starting_at,
            )
            try:
                char_end = min(
                    end_time,
                    self.characteristics[i + 1].starting_at,
                )
            except IndexError:
                # The end of the last entry is the contact end time.
                char_end = end_time
            if char_end <= char_start:
                continue
            value += (char_end - char_start) * getter(char)
            if char_end == end_time:
                break
        return value

    def get_volume(self, contact):
        """Calculates the volume of the contact from its characteristics."""
        return self._get_attr_duration_sum(
            lambda char: char.bit_rate,
            contact.start_time,
            contact.end_time,
        )

    def get_avg_bit_rate(self, contact):
        """Calculates the average data rate from the characteristics."""
        return (
            self.get_volume(contact=contact) /
            (contact.end_time - contact.start_time)
        )

    def get_avg_delay(self, contact):
        """Calculates the average delay from the characteristics."""
        return self._get_attr_duration_sum(
            lambda char: char.delay,
            contact.start_time,
            contact.end_time,
        ) / (contact.end_time - contact.start_time)

    @classmethod
    def from_list(cls, lst):
        """Creates a new instance from a list."""
        return cls(lst[0], lst[1], [
            PredictedContactCharacteristics(*char_lst)
            for char_lst in lst[2]
        ])

    def to_list(self):
        """Converts the instance to a list representation for serialization."""
        return [
            self.valid_from,
            self.probability,
            [
                [
                    char.starting_at,
                    char.bit_rate,
                    char.delay,
                ]
                for char in self.characteristics
            ],
        ]


@attr.s(slots=True)
class PredictedContact(object):
    """Represents a predicted contact, which is e.g. applicable for routing.

    Attributes:
        tx_node: The transmitting node (data depart from here).
        rx_node: The receiving node (data arrive here).
        start_time: The start timestamp of the contact in seconds.
        end_time: The end timestamp of the contact in seconds.
        generations: A list of PredictedContactGeneration instances,
            representing individual predictions of the contact properties.
            Each generation is valid from a point in time specified by the
            `valid_from` attribute. Subsequent generations override each other.
            By this feature it becomes possible to represent the evolution
            of contact predictions within a single contact plan.

    """

    tx_node = attr.ib()
    rx_node = attr.ib()
    start_time = attr.ib()
    end_time = attr.ib()
    generations = attr.ib(
        default=attr.Factory(lambda: [PredictedContactGeneration()]),
        repr=lambda v: "list(<len=" + str(len(v)) + ">)",
    )

    @start_time.validator
    def _validate_start(self, _, value):
        if value < 0.0:
            raise ValueError("start_time has to be >= 0")

    @end_time.validator
    def _validate_end(self, _, value):
        if value < self.start_time:
            raise ValueError("end_time has to be >= start_time")

    @generations.validator
    def _validate_generations(self, _, value):
        if not isinstance(value, list):
            raise ValueError("generations has to be an instance of list")
        if value and value[0].valid_from > 0.0:
            raise ValueError(
                "generations has to contain an element valid"
                "from the beginning, i.e. time 0.0"
            )
        last_validity = 0.0
        for gen in value:
            if gen.valid_from < last_validity:
                raise ValueError(
                    "generations have to be provided in order"
                )
            last_validity = gen.valid_from
            if gen.characteristics[0].starting_at > self.start_time:
                raise ValueError(
                    "each generation has to contain a characteristics instance"
                    "valid from the start of the contact"
                )

    # NOTE Argument order is retained for compatibility.
    @classmethod
    def simple(cls, tx_node, rx_node, start_time, end_time,
               bit_rate=None, probability=1.0, delay=0.0, volume=None):
        """Creates a new instance using deprecated simple syntax."""
        if volume is not None and bit_rate is not None:
            raise ValueError(
                "only one of volume and bit_rate args can be specified"
            )
        elif volume is None and bit_rate is None:
            bit_rate = 0.0
        elif bit_rate is None:
            bit_rate = float(volume) / (end_time - start_time)
        return cls(tx_node, rx_node, start_time, end_time, [
            PredictedContactGeneration(
                valid_from=0.0,
                probability=probability,
                characteristics=[
                    PredictedContactCharacteristics(
                        starting_at=start_time,
                        bit_rate=bit_rate,
                        delay=delay,
                    ),
                ],
            ),
        ])

    def get_generation_at(self, time):
        """Returns the generation valid at the specified timestamp."""
        if time is None:
            list_index = 0
        else:
            list_index = bisect.bisect(
                util.KeyedListView(
                    self.generations,
                    key=lambda x: x.valid_from,
                ),
                time,
            ) - 1
            if list_index < 0:
                raise ValueError("no valid generation found")
        return self.generations[list_index]

    def get_characteristics_at(self, time, generation_at=None):
        """Returns the characteristics at the given timestamp in-contact."""
        generation = self.get_generation_at(generation_at)
        return generation.get_characteristics_at(time)

    def characteristics_in_time_frame(self, start, end, generation_at=None):
        """Yields a list of tuples with valid characteristic sub-intervals."""
        generation = self.get_generation_at(generation_at)
        for char in generation.characteristics_in_time_frame(start, end):
            yield char

    def to_simple(self, generation_at=None, characteristics_at=None):
        """Returns a simple namedtuple representation."""
        generation = self.get_generation_at(generation_at)
        return SimplePredictedContactTuple(
            tx_node=self.tx_node,
            rx_node=self.rx_node,
            start_time=self.start_time,
            end_time=self.end_time,
            bit_rate=generation.get_avg_bit_rate(self),
            probability=generation.probability,
            # Just for the delay we have to use the specified timestamp.
            delay=generation.get_characteristics_at(characteristics_at).delay,
        )

    @classmethod
    def from_list(cls, lst):
        """Creates a new instance from a list."""
        return cls(lst[0], lst[1], lst[2], lst[3], [
            PredictedContactGeneration.from_list(gen_lst)
            for gen_lst in lst[4]
        ])

    def to_list(self):
        """Converts the instance to a list representation for serialization."""
        return [
            self.tx_node,
            self.rx_node,
            self.start_time,
            self.end_time,
            [gen.to_list() for gen in self.generations],
        ]

    @classmethod
    def from_v1(cls, lst):
        """Creates a new instance from a v1 representation provided as list."""
        return cls(lst[0], lst[1], lst[2], lst[3], [
            PredictedContactGeneration(
                valid_from,
                lst[5],
                [
                    PredictedContactCharacteristics(
                        starting_at=lst[2],
                        bit_rate=(volume / (lst[3] - lst[2])),
                        delay=lst[6],
                    ),
                ],
            )
            for valid_from, volume in lst[4]
        ])

    def basic_tuple(self):
        """Returns a 4-tuple of the basic contact properties."""
        return (self.tx_node, self.rx_node, self.start_time, self.end_time)


def fcp_to_pcp(fcp):
    """
    Convert a factual contact plan (FCP) representation to a PCP usable
    by tvgutil methods. NOTE: The bit error rate metric is dropped.
    """
    return [
        PredictedContact(
            tx_node=factual_contact.tx_node,
            rx_node=factual_contact.rx_node,
            start_time=factual_contact.start_time,
            end_time=factual_contact.end_time,
            generations=[
                PredictedContactGeneration(
                    valid_from=0.0,
                    probability=1.0,
                    characteristics=[
                        PredictedContactCharacteristics(
                            starting_at=char.starting_at,
                            bit_rate=char.bit_rate,
                            delay=char.delay,
                        )
                        for char in factual_contact.characteristics
                    ],
                ),
            ],
        )
        for factual_contact in fcp
    ]


def pcp_to_fcp(pcp, remove_probabilistic=False, timestamp=None):
    """
    Convert a predicted contact plan (PCP) representation to an FCP usable
    by tvgutil methods, under the assumption that the duration of the contact
    is fully utilized with a constant bit rate.
    If remove_probabilistic is specified, the predicted probability is used
    (and, thus, assumed correct) for randomly deleting contacts with the
    corresponding probability. Else, the probability value is removed.
    If timestamp is set, the prediction generations available at the specified
    time will be used for defining the factual contact.
    If not, the latest prediction generation will always be used.
    """
    fcp = []
    for predicted_contact in pcp:
        generation = (
            predicted_contact.get_generation_at(timestamp)
            if timestamp is not None
            else predicted_contact.generations[-1]
        )
        if (remove_probabilistic and
                random.random() >= generation.probability):
            continue
        fcp.append(Contact(
            tx_node=predicted_contact.tx_node,
            rx_node=predicted_contact.rx_node,
            start_time=predicted_contact.start_time,
            end_time=predicted_contact.end_time,
            characteristics=[
                ContactCharacteristics(
                    starting_at=char.starting_at,
                    bit_rate=char.bit_rate,
                    delay=char.delay,
                )
                for char in generation.characteristics
            ],
        ))
    return fcp


def legacy_to_pcp(legacy_contact_plan, unidirectional=False, bit_rate=None):
    """
    Convert a legacy contact plan representation (e.g. from the ONE)
    to a PCP usable by tvgutil methods.
    - unidirectional specifies whether the supplied contact plan is
      unidirectional, i.e. contains one contact per direction. If this is not
      the case, mirrored unidirectional contacts will be added.
    - bit_rate allows to override the bit rate of all contacts
    """
    default_keys = {
        "node1": ["mBaseStation", "node1", "nodeA"],
        "node2": ["mSatellite", "node2", "nodeB"],
        "start_time": ["mContactBegin", "start", "start_time", "begin"],
        "end_time": ["mContactEnd", "end", "end_time"],
        "probability": ["prob", "p", "probability"],
        "bit_rate": ["capacity", "measured_capacity", "volume"],
    }
    defaults = {
        "probability": 1.0,
        "bit_rate": 0.0,
    }
    # first build a dict mapping node pairs to contact_vars dicts
    edges = {}
    for contact_dict in legacy_contact_plan:
        contact_vars = {}
        for key, aliases in default_keys.items():
            for alias in aliases:
                if (alias in contact_dict and
                        str(contact_dict[alias]).strip() != ""):
                    contact_vars[key] = contact_dict[alias]
                    break
            if key not in contact_vars:
                val = defaults.get(key, None)
                if val is None:
                    return None
                contact_vars[key] = val
        if contact_vars["end_time"] < contact_vars["start_time"]:
            raise InvalidContactPlanError("Contact ends before it starts")
        if bit_rate is not None:
            contact_vars["bit_rate"] = bit_rate
        else:
            # NOTE: By default there is a volume prediction in the v1 CP.
            contact_vars["bit_rate"] /= (
                contact_vars["end_time"] - contact_vars["start_time"]
            )
        # see below
        _add_node_pair_to_edge_dict(edges, contact_vars, unidirectional)
    return _build_pcp_from_edges_dict(edges, unidirectional)


# integrates a contact_vars dict as contained in a legacy contact plan
# into the edges dictionary (which associates graph edges to a contact_vars-
# like dict without node ids)
def _add_node_pair_to_edge_dict(edges, contact_vars, unidirectional):
    if unidirectional:
        node_pair = (contact_vars["node1"], contact_vars["node2"])
    else:
        # it is important to neglect the order in case unidirectional=False
        node_pair = frozenset({
            contact_vars["node1"],
            contact_vars["node2"],
        })
    del contact_vars["node1"]
    del contact_vars["node2"]
    # this also performs deduplication in case unidirectional=False
    if node_pair in edges:
        duplicate = False
        for contact in edges[node_pair]:
            if (contact["start_time"] <= contact_vars["end_time"] and
                    contact["end_time"] >= contact_vars["start_time"]):
                # we do not support not-fully-overlapping contacts
                if (abs(contact["start_time"] -
                        contact_vars["start_time"]) > 1e-3 or
                        abs(contact["end_time"] -
                            contact_vars["end_time"]) > 1e-3):
                    raise InvalidContactPlanError((
                        "Unmatching overlaps detected for contact at {} - "
                        "unidirectional contact plan supplied?"
                    ).format(node_pair))
                duplicate = True
        if not duplicate:
            edges[node_pair].append(contact_vars)
    else:
        edges[node_pair] = [contact_vars]


# take the edges dict (see above) and build a PCP from it
def _build_pcp_from_edges_dict(edges, unidirectional):
    pcp = []
    for node_pair, contacts in edges.items():
        for contact_vars in contacts:
            # unpack either frozenset or tuple with the two nodes
            node1, node2 = node_pair
            pcp.append(
                PredictedContact.simple(node1, node2, **contact_vars)
            )
            # if the legacy plan is bidirectional, we add the reverse contact
            if not unidirectional:
                pcp.append(
                    PredictedContact.simple(node2, node1, **contact_vars)
                )
    return pcp


def contact_tuples_to_pcp(contact_tuple_list, time_offset=0.0,
                          uplink_rate=0.0, downlink_rate=0.0,
                          prob_min=1.0, prob_max=1.0, symmetric_prob=True,
                          only_first_node_probabilistic=False):
    """
    Creates a list of PredictedContact instances from the given list of
    bi-directional contact tuples of the form (node1, node2, start, end).
    Uplink means transmissions from node1 to node2, downlink is the
    reverse direction.

    Arguments:
        - contact_tuple_list: the list of contact tuples to be processed
        - time_offset: a time offset in seconds, to be subtracted from
          start and end times of the provided contacts
        - uplink_rate: bit rate (in bit/s) uplink (see above)
        - downlink_rate: bit rate (in bit/s) downlink (see above)
        - prob_min: minimum probability to be assigned for the links
        - prob_max: maximum probability to be assigned for the links
        - symmetric_prob: whether the same prob. should be assigned for
          the up- and downlink of one contact
        - only_first_node_probabilistic: whether the same prob. should be
          assigned for the up- and downlinks of all contacts with the same
          first node (normally a ground station)
    """
    assert time_offset >= 0
    assert prob_max >= prob_min

    def _rnd(start, end):
        return random.random() * (end - start) + start

    result = []
    if only_first_node_probabilistic:
        node_probs = {}
    for node1, node2, start, end in contact_tuple_list:
        assert start >= time_offset
        assert end >= time_offset
        assert end >= start
        if only_first_node_probabilistic:
            if node1 not in node_probs:
                node_probs[node1] = _rnd(prob_min, prob_max)
            uplink_prob = node_probs[node1]
            downlink_prob = node_probs[node1]
        elif symmetric_prob:
            uplink_prob = _rnd(prob_min, prob_max)
            downlink_prob = uplink_prob
        else:
            uplink_prob = _rnd(prob_min, prob_max)
            downlink_prob = _rnd(prob_min, prob_max)
        result.append(PredictedContact.simple(
            node1,
            node2,
            start - time_offset,
            end - time_offset,
            bit_rate=uplink_rate,
            probability=uplink_prob,
        ))
        result.append(PredictedContact.simple(
            node2,
            node1,
            start - time_offset,
            end - time_offset,
            bit_rate=downlink_rate,
            probability=downlink_prob,
        ))
    return result


def contact_tuples_to_fcp(contact_tuple_list, time_offset=0.0,
                          uplink_rate=0.0, downlink_rate=0.0,
                          ber_min=0.0, ber_max=0.0, symmetric_ber=True):
    """
    Creates a list of Contact instances from the given list of
    bi-directional contact tuples of the form (node1, node2, start, end).
    Uplink means transmissions from node1 to node2, downlink is the
    reverse direction.

    Arguments:
        - contact_tuple_list: the list of contact tuples to be processed
        - time_offset: a time offset in seconds, to be subtracted from
          start and end times of the provided contacts
        - uplink_rate: bit rate (in bit/s) uplink (see above)
        - downlink_rate: bit rate (in bit/s) downlink (see above)
        - ber_min: minimum bit error rate to be assigned for the links
        - ber_max: maximum bit error rate to be assigned for the links
        - symmetric_ber: whether the same bit error rate should be assigned
          for the up- and downlink of one contact
    """
    assert time_offset >= 0
    assert ber_max >= ber_min

    def _rnd(start, end):
        return random.random() * (end - start) + start

    result = []
    for node1, node2, start, end in contact_tuple_list:
        assert start >= time_offset
        assert end >= time_offset
        assert end >= start
        if symmetric_ber:
            uplink_ber = _rnd(ber_min, ber_max)
            downlink_ber = uplink_ber
        else:
            uplink_ber = _rnd(ber_min, ber_max)
            downlink_ber = _rnd(ber_min, ber_max)
        result.append(Contact.simple(
            node1,
            node2,
            start - time_offset,
            end - time_offset,
            bit_rate=uplink_rate,
            bit_error_rate=uplink_ber,
        ))
        result.append(Contact.simple(
            node2,
            node1,
            start - time_offset,
            end - time_offset,
            bit_rate=downlink_rate,
            bit_error_rate=downlink_ber,
        ))
    return result


def contact_plan_to_contact_tuples(cplan, time_offset=0.0):
    """
    Convert the given FCP or PCP to (bidirectional) contact tuples of the form
    (node1, node2, start, end)
    """
    result = []
    edges = {}
    for contact in cplan:
        node_pair = frozenset({contact.tx_node, contact.rx_node})
        if node_pair in edges:
            duplicate = False
            for start, end in edges[node_pair]:
                if (contact.start_time <= end and contact.end_time >= start):
                    # we do not support not-fully-overlapping contacts
                    if (abs(contact.start_time - start) > 1e-3 or
                            abs(contact.end_time - end) > 1e-3):
                        raise InvalidContactPlanError((
                            "Unmatching overlaps detected for contact at {} - "
                            "unidirectional contact plan supplied?"
                        ).format(node_pair))
                    duplicate = True
            if not duplicate:
                edges[node_pair].append((contact.start_time, contact.end_time))
        else:
            edges[node_pair] = [(contact.start_time, contact.end_time)]
    result = []
    for pair, contact_tuples in edges.items():
        node1, node2 = pair
        for start, end in contact_tuples:
            result.append((
                node1,
                node2,
                start + time_offset,
                end + time_offset,
            ))
    return result
