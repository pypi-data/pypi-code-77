"""Provides measures to obtain the contact volume and Link implementations."""

import math


def get_fc_volume(factual_contact, block_size):
    """Get the factual contact volume if ideal error recovery is used."""
    return get_fc_volume_in_interval(
        factual_contact,
        block_size,
        factual_contact.start_time,
        factual_contact.end_time,
    )


def get_fc_volume_in_interval(factual_contact, block_size, start, end):
    """Get the interval volume (of an FC) if ideal error recovery is used."""
    assert start >= factual_contact.start_time
    assert end <= factual_contact.end_time
    volume = 0
    t = start
    char_i = -1
    char_count = len(factual_contact.characteristics)
    next_char_start = -math.inf
    while True:
        while next_char_start <= t:
            char_i += 1
            char_i_changed = True
            if char_i + 1 == char_count:
                next_char_start = math.inf
            else:
                next_char_start = factual_contact.characteristics[
                    char_i + 1
                ].starting_at
        if char_i_changed:
            char = factual_contact.characteristics[char_i]
            p_block_successfully_transmitted = (
                (1 - char.bit_error_rate) ** block_size
            )
            tx_duration = block_size / char.bit_rate
            vol_inc = block_size * p_block_successfully_transmitted
            char_i_changed = False
        if t + tx_duration > end:
            break
        upper_limit = min(next_char_start, end)
        update_count = (upper_limit - t) // tx_duration
        if update_count == 0:
            break
        volume += update_count * vol_inc
        t += update_count * tx_duration
    return volume
