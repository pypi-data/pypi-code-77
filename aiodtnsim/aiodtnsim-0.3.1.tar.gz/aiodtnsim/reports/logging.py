# encoding: utf-8

"""Module providing an EventHandler for generating log output."""

import logging

from .. import EventHandler

logger = logging.getLogger(__name__)


class LoggingReport(EventHandler):
    """A simple event handler, logging all events that occur."""

    def contact_started(self, time, contact):
        """Log a contact_started event."""
        logger.debug("Contact started: %s", contact)

    def contact_ended(self, time, contact):
        """Log a contact_ended event."""
        logger.debug("Contact ended: %s", contact)

    def message_transmission_started(self, time, message, contact):
        """Log a message_transmission_started event."""
        logger.debug("Message tx started via %s: %s", contact, message)

    def message_received(self, time, rx_node, message, tx_node):
        """Log a message_received event."""
        logger.debug("Message received at %s from %s: %s",
                     rx_node.eid, tx_node.eid, message)

    def message_dropped(self, time, node, message):
        """Log a message_dropped event."""
        logger.debug("Message dropped at %s: %s", node.eid, message)

    def message_rejected(self, time, node, message):
        """Log a message_rejected event."""
        logger.debug("Message rejected at %s: %s", node.eid, message)

    def message_delivered(self, time, node, message):
        """Log a message_delivered event."""
        logger.debug("Message delivered at %s: %s", node.eid, message)

    def message_deleted(self, time, node, message):
        """Log a message_deleted event."""
        logger.debug("Message deleted at %s: %s", node.eid, message)

    def message_injected(self, time, node, message):
        """Log a message_injected event."""
        logger.debug("Message injected at %s: %s", node.eid, message)

    def message_scheduled(self, time, node, message):
        """Log a message_scheduled event."""
        logger.debug("Message scheduled at %s: %s", node.eid, message)

    def message_transmission_completed(self, time, message, contact):
        """Log a message_transmission_completed event."""
        logger.debug("Sent via %s: %s", contact, message)

    def message_transmission_aborted(self, time, message, contact):
        """Log a message_transmission_aborted event."""
        logger.debug("Transfer via %s aborted: %s", contact, message)
