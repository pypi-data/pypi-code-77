from datetime import datetime

import pandas as pd
from pandas import Timestamp

from cccalendar import _get_date_square_coordinates, _extend_data, _apply_colours


def test_get_date_square_coordinates():
    # e.g. 01/01/2021
    day_of_week = 4  # Friday
    week_of_month = 0  # First week
    scale = 10  # Arbitrary
    corners, centre = _get_date_square_coordinates(day_of_week, week_of_month, scale)
    assert corners[0] == (40, 0)
    assert corners[1] == (40, 5)
    assert corners[2] == (45, 5)
    assert corners[3] == (45, 0)
    assert centre == (42.5, 2.5)

    # e.g. 30/11/2020
    day_of_week = 0  # Monday
    week_of_month = 5  # Sixth week
    scale = 10  # Arbitrary
    corners, centre = _get_date_square_coordinates(day_of_week, week_of_month, scale)
    assert corners[0] == (0, 50)
    assert corners[1] == (0, 55)
    assert corners[2] == (5, 55)
    assert corners[3] == (5, 50)
    assert centre == (2.5, 52.5)


def test_extend_data():
    s = pd.Series({
        '2021-01-31': 'a',
        '2021-03-01': 'b',
        '2021-02-01': 'a',
        '2021-01-15': 'b'
    })
    s.index = pd.to_datetime(s.index)
    s = _extend_data(s, s.index.min(), s.index.max())
    assert pd.to_datetime(s.index.values[0]) == datetime(2021, 1, 1)
    assert pd.to_datetime(s.index.values[-1]) == datetime(2021, 3, 31)
    assert len(s.index) == 90  # 31 + 28 + 31


def test_apply_colours():
    data = pd.Series({
        '2021-01-01': None,
        '2021-01-05': 'event_a',
        '2021-01-15': 'event_b',
        '2021-01-16': None,
        '2021-01-25': 'event_c',
        '2021-02-05': 'event_d',
        '2021-02-10': None,
        '2021-02-15': 'event_a',
        '2021-02-25': 'event_b',
        '2021-03-05': 'event_c',
        '2021-03-15': 'event_d',
        '2021-03-31': None
    })
    data.index = pd.to_datetime(data.index)
    cmap = {
        'event_a': '#ff001e',
        'event_b': '#65001e',
        'event_c': '#42d1a4',
        'event_d': '#7bff1a'
    }
    res_one = _apply_colours(data, cmap, '#ffffff', '#000000', False, datetime(2021, 1, 16), datetime(2021, 3, 1))
    res_two = _apply_colours(data, cmap, '#ffffff', '#000000', True, datetime(2021, 1, 16), datetime(2021, 3, 1))

    assert res_one.to_dict() == {
        Timestamp('2021-01-01 00:00:00'): '#000000',  # Empty date - excluded
        Timestamp('2021-01-05 00:00:00'): '#ff001e',  # Outside of range but not excluded
        Timestamp('2021-01-15 00:00:00'): '#65001e',
        Timestamp('2021-01-16 00:00:00'): '#ffffff',  # First date within range
        Timestamp('2021-01-25 00:00:00'): '#42d1a4',
        Timestamp('2021-02-05 00:00:00'): '#7bff1a',
        Timestamp('2021-02-10 00:00:00'): '#ffffff',  # Empty date in range - default colour
        Timestamp('2021-02-15 00:00:00'): '#ff001e',
        Timestamp('2021-02-25 00:00:00'): '#65001e',
        Timestamp('2021-03-05 00:00:00'): '#42d1a4',
        Timestamp('2021-03-15 00:00:00'): '#7bff1a',
        Timestamp('2021-03-31 00:00:00'): '#000000'
    }

    assert res_two.to_dict() == {
        Timestamp('2021-01-01 00:00:00'): '#000000',
        Timestamp('2021-01-05 00:00:00'): '#000000',  # Outside of range - excluded
        Timestamp('2021-01-15 00:00:00'): '#000000',
        Timestamp('2021-01-16 00:00:00'): '#ffffff',
        Timestamp('2021-01-25 00:00:00'): '#42d1a4',
        Timestamp('2021-02-05 00:00:00'): '#7bff1a',
        Timestamp('2021-02-10 00:00:00'): '#ffffff',
        Timestamp('2021-02-15 00:00:00'): '#ff001e',
        Timestamp('2021-02-25 00:00:00'): '#65001e',
        Timestamp('2021-03-05 00:00:00'): '#000000',
        Timestamp('2021-03-15 00:00:00'): '#000000',
        Timestamp('2021-03-31 00:00:00'): '#000000'
    }
