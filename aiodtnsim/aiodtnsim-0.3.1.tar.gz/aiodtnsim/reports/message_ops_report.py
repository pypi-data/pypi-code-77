# encoding: utf-8

"""Module providing an EventHandler for generating comparable logs."""

import sys

from .. import EventHandler


class MessageOpsReport(EventHandler):
    """An report providing a diff-able list of the most relevant events."""

    def __init__(self):
        self.ops = []
        self.msgs = {}  # ids
        self.next_msg_id = 0

    def _get_id(self, message):
        return self.msgs[message]

    def contact_started(self, time, contact):
        """Add a contact_started event to the list of events."""
        self.ops.append(
            f"{_time(time)} {contact.tx_node.eid} "
            f"c_start {contact.rx_node.eid}"
        )

    def contact_ended(self, time, contact):
        """Add a contact_ended event to the list of events."""
        self.ops.append(
            f"{_time(time)} {contact.tx_node.eid} "
            f"c_end {contact.rx_node.eid}"
        )

    def message_received(self, time, rx_node, message, tx_node):
        """Add a message_received event to the list of events."""
        if message not in self.msgs:
            return
        self.ops.append(
            f"{_time(time)} {rx_node.eid} recv {self._get_id(message)} "
            f"from {tx_node.eid}"
        )

    def message_delivered(self, time, node, message):
        """Add a message_delivered event to the list of events."""
        self.ops.append(
            f"{_time(time)} {node.eid} deliver {self._get_id(message)}"
        )

    def message_rejected(self, time, node, message):
        """Add a message_rejected event to the list of events."""
        self.ops.append(
            f"{_time(time)} {node.eid} reject {self._get_id(message)}"
        )

    def message_dropped(self, time, node, message):
        """Add a message_dropped event to the list of events."""
        self.ops.append(
            f"{_time(time)} {node.eid} drop {self._get_id(message)}"
        )

    def message_transmission_aborted(self, time, message, contact):
        """Add a message_transmission_aborted event to the list of events."""
        if message not in self.msgs:
            return
        self.ops.append(
            f"{_time(time)} {contact.tx_node.eid} "
            f"abort {self._get_id(message)}"
        )

    def message_injected(self, time, node, message):
        """Add a message_injected event to the list of events."""
        self.msgs[message] = self.next_msg_id
        self.next_msg_id += 1
        self.ops.append(
            f"{_time(time)} {node.eid} inject {self._get_id(message)} "
            f"({message.source} -> {message.destination})"
        )

    def print(self, file=sys.stdout):
        """Print the report to the specified file. Defaults to stdout."""
        for operation in sorted(self.ops):
            print(operation, file=file)


def _time(time):
    return round(time * 1000)
