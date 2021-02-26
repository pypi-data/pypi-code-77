# encoding: utf-8

from aiodtnsim import Contact

from .util import get_empty_node


def test_contact_args():
    """Test equality of Contact instance using args or kwargs."""
    n1 = get_empty_node()
    n2 = get_empty_node()

    # Test our assumptions about the signature of the Contact constructor.
    c1 = Contact(
        n1,
        n2,
        123.456,
        456.789,
        987.123,
        11.22,
        n1,  # arbitrary param
    )
    c2 = Contact(
        tx_node=n1,
        rx_node=n2,
        start_time=123.456,
        end_time=456.789,
        bit_rate=987.123,
        delay=11.22,
        param=n2,  # arbitrary param
    )

    assert c1 == c2
    assert not (c1 != c2)
    assert not (c1 < c2)
    assert not (c1 > c2)


def test_contact_is_frozen():
    """Test that we can compute a hash of Contact instances."""
    c1 = Contact(
        get_empty_node(),
        get_empty_node(),
        # TODO

