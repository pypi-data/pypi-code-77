# encoding: utf-8

"""Module providing an EventHandler for printing message stats."""

import sys
import time
import numpy as np  # type: ignore

from .. import EventHandler


class MessageStatsReport(EventHandler):
    """An event handler providing message routing statistics."""

    def __init__(self):
        self.messages = {}
        self.contacts = {}
        self.buffers = {}
        self.buffer_history = {}
        self.init_time = time.time()

    def contact_started(self, time, contact):
        """Record a contact_started event."""
        self.contacts[contact] = {
            "time_usage": 0,
            "volume_usage": 0,  # NOTE: this is link-layer volume!
            "last_tx_start": None,
        }
        # Add a sample to the node buffer history before each contact...
        eid = contact.tx_node.eid
        if eid in self.buffers:
            self.buffer_history[eid].append((time, self.buffers[eid]))

    def contact_ended(self, time, contact):
        """Record a contact_ended event."""
        # Add a sample to the node buffer history after each contact...
        eid = contact.tx_node.eid
        if eid in self.buffers:
            self.buffer_history[eid].append((time, self.buffers[eid]))

    def message_transmission_started(self, time, message, contact):
        """Record a message_transmission_started event."""
        self.contacts[contact]["last_tx_start"] = (time, message)
        original = message.original_message  # if fragmented, use original
        record = self.messages.get(original, None)
        # This supports "untracked" messages, e.g. ACKs from Epidemic
        if not record:
            return
        record["tx_count"] += 1
        record["tx_volume"] += message.size

    def message_transmission_completed(self, time, message, contact):
        """Record a message_transmission_completed event."""
        contact_record = self.contacts[contact]
        tx_time, tx_message = contact_record["last_tx_start"]
        assert message is tx_message
        contact_record["time_usage"] += (time - tx_time)
        contact_record["volume_usage"] += (time - tx_time) * contact.bit_rate

    def message_transmission_aborted(self, time, message, contact):
        """Record a message_transmission_aborted event."""
        contact_record = self.contacts[contact]
        tx_time, tx_message = contact_record["last_tx_start"]
        assert message is tx_message
        contact_record["time_usage"] += (time - tx_time)
        contact_record["volume_usage"] += (time - tx_time) * contact.bit_rate

    def message_received(self, time, rx_node, message, tx_node):
        """Record message reception at the specified node."""
        original = message.original_message  # if fragmented, use original
        record = self.messages.get(original, None)
        # This supports "untracked" messages, e.g. ACKs from Epidemic
        if not record:
            return
        self._add_to_buffer(time, rx_node.eid, message)
        record["rx_count"] += 1
        record["rx_volume"] += message.size
        if tx_node.eid not in record["instances_sent"]:
            record["instances_sent"][tx_node.eid] = 1
        else:
            record["instances_sent"][tx_node.eid] += 1
        if rx_node.eid not in record["instances_received"]:
            record["instances_received"][rx_node.eid] = 1
        else:
            record["instances_received"][rx_node.eid] += 1
        if rx_node.eid != original.destination:
            return
        if record["delivered"]:
            return
        record["delivered_fragments"].add(message)
        if not message.is_fragmented or self._is_delivered(original):
            record["delivered"] = {
                "node": rx_node.eid,
                "time": time,
            }

    def _is_delivered(self, original):
        delivery_info = []
        for frag in self.messages[original]["delivered_fragments"]:
            # if it is the full message, it's delivered!
            if not frag.is_fragmented:
                return True
            delivery_info.append((frag.fragment_offset, frag.size))
        # walk through the set of fragments and check whether we have all
        # of them
        cur_offset = 0
        for start, length in sorted(delivery_info, key=lambda x: x[0]):
            if start > cur_offset:
                return False
            cur_offset = max(cur_offset, start + length)
        total_size = original.size
        assert not cur_offset > total_size
        return cur_offset == total_size

    def message_injected(self, time, node, message):
        """Record message injection at the specified node."""
        original = message.original_message  # if fragmented, use original
        self.messages[original] = {
            "created": original.start_time,
            "size": original.size,
            "delivered": None,
            "delivered_fragments": set(),
            "previous_hop": {node.eid: [None]},
            "previous_hop_pending": {},
            "tx_count": 0,
            "rx_count": 0,
            "tx_volume": 0,
            "rx_volume": 0,
            "scheduled_at": {},
            "instances_sent": {},
            "instances_received": {node.eid: 1},
        }
        self._add_to_buffer(time, node.eid, message)

    def message_scheduled(self, time, node, message):
        """Record message scheduling at the specified node."""
        original = message.original_message  # if fragmented, use original
        schedlist = self.messages[original]["scheduled_at"]
        schedlist[node.eid] = (
            1 if node.eid not in schedlist else schedlist[node.eid] + 1
        )

    def _add_to_buffer(self, time, eid, message):
        if eid not in self.buffers:
            self.buffers[eid] = message.size
            self.buffer_history[eid] = []
        else:
            self.buffers[eid] += message.size

    def _delete_from_buffer(self, time, eid, message):
        self.buffers[eid] -= message.size

    def message_dropped(self, time, node, message):
        """Record a message_dropped event."""
        self._delete_from_buffer(time, node.eid, message)

    def message_rejected(self, time, node, message):
        """Record a message_rejected event."""
        self._delete_from_buffer(time, node.eid, message)

    def message_delivered(self, time, node, message):
        """Record a message_delivered event."""
        self._delete_from_buffer(time, node.eid, message)

    def message_deleted(self, time, node, message):
        """Record a message_deleted event."""
        self._delete_from_buffer(time, node.eid, message)

    def _get_delivery_times(self):
        return [
            msg["delivered"]["time"] - msg["created"]
            for msg in self.messages.values()
            if msg["delivered"] is not None
        ]

    def _get_value(self, key, delivered=False):
        return [
            msg[key]
            for msg in self.messages.values()
            if not delivered or msg["delivered"] is not None
        ]

    def _get_scheduling_counts(self):
        return [
            count
            for _, m in self.messages.items()
            for _, count in m["scheduled_at"].items()
        ]

    def _get_replica_counts(self):
        # The estimated amount of replicas that existed of a message are the
        # count of outgoing copies minus the count of incoming copies on each
        # node on the path - if a node creates 1 replica, it will send out 1
        # more message than it has received. This adds 1 to the replica count.
        # NOTE that only successfully-sent messages are counted.
        # WARNING: This is only an approximation as the node behavior cannot
        # be fully controlled. For example, a node A using "Spray and Wait" may
        # receive 2 copies from B at once and send back two times one copy.
        # This will be counted as message replication although replication
        # has already occurred earlier. Copies in buffers in example (A|B):
        # 6|0, 3|3, 2|4, 1|5, 3|3, 2|4, 1|5 - last 3 steps repeatedly do +1
        return [
            1 + sum(
                max(
                    0,
                    msg["instances_sent"][eid] - msg["instances_received"][eid]
                )
                for eid in msg["instances_sent"].keys()
            )
            for msg in self.messages.values()
        ]

    def _get_contact_utilization(self):
        # This is the ratio of contact time used for transmitting messages
        # (or fragments) or at least performing transmission attempts.
        return [
            (
                contact.tx_node.eid,
                contact.rx_node.eid,
                contact.start_time,
                contact.end_time,
                ci["time_usage"] / (contact.end_time - contact.start_time),
                ci["volume_usage"],
            )
            for contact, ci in self.contacts.items()
        ]

    def print(self):
        """Print the report to the console."""
        runtime = time.time() - self.init_time
        print(f"> Simulation runtime: {round(runtime, 3)} s", file=sys.stderr)
        print("> Message stats:", file=sys.stderr)

        d_times = self._get_delivery_times()
        if self.messages:
            print(f"Delivered: {len(d_times)} of {len(self.messages)} "
                  f"({round(len(d_times) / len(self.messages) * 100, 2)} %)",
                  file=sys.stderr)
        else:
            print("Nothing sent, nothing delivered.", file=sys.stderr)

        sched_counts = self._get_scheduling_counts()
        if sched_counts:
            print_stat("Average sched. count", sched_counts)
            schedrate = sum(1 for c in sched_counts if c == 1)
            print(f"Rate of msgs. initially scheduled successfully: "
                  f"{schedrate} of {len(sched_counts)} "
                  f"({round(schedrate / len(sched_counts) * 100, 2)} %)",
                  file=sys.stderr)

        tx_counts = self._get_value("tx_count", True)
        rx_counts = self._get_value("rx_count", True)
        tx_counts_all = self._get_value("tx_count", False)
        rx_counts_all = self._get_value("rx_count", False)
        tx_volumes = self._get_value("tx_volume", True)
        rx_volumes = self._get_value("rx_volume", True)
        tx_volumes_all = self._get_value("tx_volume", False)
        rx_volumes_all = self._get_value("rx_volume", False)
        print("### BUFFER STATS", file=sys.stderr)
        # Contact Utilization, overall
        contact_utilization = [
            cu
            for _, _, _, _, cu, _ in self._get_contact_utilization()
        ]
        print_stat(
            "Contact utilization",
            np.array(contact_utilization),
            0.01,
            " %",
        )
        # Buffer Utilization, overall (after every contact)
        buffer_utilization = [
            bu
            for bu_list in self.buffer_history.values()
            for _, bu in bu_list
        ]
        print_stat(
            "Buffer utilization",
            np.array(buffer_utilization),
            1_000_000,
            " Mb",
        )
        print("### TRANSMISSION / RECEPTION STATS", file=sys.stderr)
        if sum(tx_counts_all) == 0:
            print("No messages have been transmitted.", file=sys.stderr)
            return
        replicas = self._get_replica_counts()
        print_stat("Average msg. replica count", replicas)
        print_stat("Average TX count", tx_counts_all)
        print_stat("Average RX count", rx_counts_all)
        print(f"Total TX count: {sum(tx_counts_all)} txs", file=sys.stderr)
        print(f"Total RX count: {sum(rx_counts_all)} rxs", file=sys.stderr)
        print_stat("Average TX volume", tx_volumes_all, 1_000_000, " Mb")
        print_stat("Average RX volume", rx_volumes_all, 1_000_000, " Mb")
        loss_ratio_all_pct = round(
            100 - np.mean(rx_counts_all) / np.mean(tx_counts_all) * 100, 2
        )
        print(f"=> Overall link loss ratio: {loss_ratio_all_pct} %",
              file=sys.stderr)
        print("### DELIVERY STATS", file=sys.stderr)
        if not d_times:
            print("No messages have been delivered.", file=sys.stderr)
            return
        print_stat("Average delivery delay", d_times, 1, "s")
        # Amount and Volume of Messages Delivered
        print_stat("Average delivered TX count", tx_counts)
        print_stat("Average delivered RX count", rx_counts)
        print(f"Total delivered TX count: {sum(tx_counts)} txs",
              file=sys.stderr)
        print(f"Total delivered RX count: {sum(rx_counts)} rxs",
              file=sys.stderr)
        print_stat("Average delivered TX volume", tx_volumes, 1_000_000, " Mb")
        print_stat("Average delivered RX volume", rx_volumes, 1_000_000, " Mb")
        # Loss Ratio / Retransmissions & Energy Efficiency
        loss_ratio_pct = round(
            100 - np.mean(rx_counts) / np.mean(tx_counts) * 100, 2
        )
        print(f"=> Link loss ratio for delivered msgs.: {loss_ratio_pct} %",
              file=sys.stderr)
        eeff_pct = round(len(d_times) / sum(replicas) * 100, 2)
        print(f"=> Energy efficiency (delivered): {eeff_pct} %",
              file=sys.stderr)

    def serializable(self):
        """Provide a serializable form of the report."""
        runtime = time.time() - self.init_time
        # NOTE: Overhead ratio is transmissions / hops
        return {
            "delays": self._get_delivery_times(),
            "tx_counts_delivered": self._get_value("tx_count", True),
            "tx_counts_all": self._get_value("tx_count", False),
            "rx_counts_delivered": self._get_value("rx_count", True),
            "rx_counts_all": self._get_value("rx_count", False),
            "tx_volumes_delivered": self._get_value("tx_volume", True),
            "tx_volumes_all": self._get_value("tx_volume", False),
            "rx_volumes_delivered": self._get_value("rx_volume", True),
            "rx_volumes_all": self._get_value("rx_volume", False),
            "scheduling_counts": self._get_scheduling_counts(),
            "replica_counts": self._get_replica_counts(),
            "contact_utilization": self._get_contact_utilization(),
            "buffer_utilization": self.buffer_history,
            "runtimes": [runtime],
        }


def print_stat(name, stat_array, divide_by=1, suffix="", digits=2):
    """Print a statistic over an array, with std. dev. and percentiles."""
    PCT = [0, 5, 10, 20, 50, 80, 90, 95, 100]
    print(
        f"{name}: {round(np.mean(stat_array) / divide_by, digits)}{suffix} ~ "
        f"std = {round(np.std(stat_array) / divide_by, digits)}{suffix};",
        ", ".join(
            f"{pct}% = {round(val / divide_by, digits)}{suffix}"
            for pct, val in zip(PCT, np.percentile(stat_array, PCT))
        ),
        file=sys.stderr
    )
