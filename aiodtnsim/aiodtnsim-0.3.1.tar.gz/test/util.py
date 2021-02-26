# encoding: utf-8

import uuid

from aiodtnsim import BaseNode, EventDispatcher


def get_empty_node():
    """Get an empty but distinct BaseNode instance useable in tests."""
    return BaseNode(
        uuid.uuid4(),
        event_dispatcher=EventDispatcher(),
    )
