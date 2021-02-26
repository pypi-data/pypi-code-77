#!/usr/bin/env python
# encoding: utf-8

"""
Module allowing to generate contact plan predictions for Ring Road scenarios
of types RR0, RRi, RRs, RRp, plus all combinations of them.
The intermediary representation is a bi-directional contact representation
as a list of tuples of the form (node1, node2, start, end), allowing to be
processed with functions in the tvgutil.contact_plan module.
"""

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
)

import math
import datetime
import ephem
import numpy as np
from scipy import optimize

# === RR0 ===


def _create_gs(lat, lon):
    obs = ephem.Observer()
    obs.lat = str(lat)  # pylint: disable=assigning-non-slot
    obs.lon = str(lon)  # pylint: disable=assigning-non-slot
    return obs


def _altitude(gsobj, satobj, unixtime):
    gsobj.date = datetime.datetime.utcfromtimestamp(unixtime)
    satobj.compute(gsobj)
    return satobj.alt


def _maximize_alt(gsobj, satobj, rough_time, delta, precision):
    bracket_interval = [rough_time - delta, rough_time, rough_time + delta]
    return optimize.minimize_scalar(
        lambda x: -_altitude(gsobj, satobj, x),
        bracket=bracket_interval,
        tol=precision,
    ).x


def _get_zeros(gsobj, satobj, rough_time, half_period, min_elev_rad):
    return (
        optimize.brentq(
            lambda x: _altitude(gsobj, satobj, x) - min_elev_rad,
            rough_time - half_period,
            rough_time,
        ),
        optimize.brentq(
            lambda x: _altitude(gsobj, satobj, x) - min_elev_rad,
            rough_time,
            rough_time + half_period,
        ),
    )


def get_rr0_contact_tuples(sat_list, gs_list, start_time, duration,
                           min_elevation=10.0,
                           precision=0.1, half_period=2700.0, step=300.0,
                           strip_start_end=True):
    """
    Creates a list of contact tuples of the form (node1, node2, start, end)
    for all sat-to-gs contacts in the given scenario.
    The tuples represent bi-directional contacts.

    Arguments:
        - sat_list: [{"id": "abc", "tle": ["...", "..."]}, ...]
        - gs_list: [{"id": "abc", "lat": <rad>, "lon": <rad>,
                "hot": <bool>}, ...]
        - start_time: UNIX timestamp
        - duration: [in seconds]
        - min_elev: minimum elevation, in degrees
        - precision: fitting / maximization precision, in seconds
        - half_period: assumed half orbit period for zero fitting, in seconds
        - step: simulation step, in seconds
        - strip_start_end: remove contacts which start or end outside of
          the specified interval

    Returned tuple:
        - node1, node2 are the node IDs (each pair is only added once!)
        - [start, end] is the contact interval in seconds
    """

    w_sats = [
        (
            e["id"],
            ephem.readtle(str(e["id"]), *[str(s) for s in e["tle"]]),
        )
        for e in sat_list
    ]
    w_gs = [
        (
            e["id"],
            _create_gs(e["lat"], e["lon"]),
        )
        for e in gs_list
    ]

    # Python maximization and solving for zeros loosely taken from here:
    # https://github.com/skyfielders/astronomy-notebooks/

    times = np.arange(start_time, start_time + duration, step)
    min_elev_rad = min_elevation / 180.0 * math.pi
    # For each Sat-GS combination, this calculates the maxima of the altitude
    # function and the zeros surrounding them, which identify the contact
    # start and end times.
    result = []
    for satid, satobj in w_sats:
        for gsid, gsobj in w_gs:
            # First, find "rough maxima" where the sign of the difference
            # between consecutive array elements changes.
            rough_alt = [_altitude(gsobj, satobj, d) for d in times]
            ldiff = np.ediff1d(rough_alt, to_begin=0.0)
            rdiff = np.ediff1d(rough_alt, to_end=0.0)
            rough_maxima = times[(ldiff > 0.0) & (rdiff < 0.0)]
            # Secondly, maximize the altitudes with sufficient precision.
            precise_maxima = [
                _maximize_alt(gsobj, satobj, x, step, precision)
                for x in rough_maxima
            ]
            # Thirdly, reduce the set of maxima to those which reach the
            # minimum altitude.
            contact_maxima = [
                x
                for x in precise_maxima
                if _altitude(gsobj, satobj, x) >= min_elev_rad
            ]
            # Fourthly, determine the zeros surrounding the maxima and store
            # them in the list of resulting contacts.
            contacts = [
                _get_zeros(gsobj, satobj, x, half_period, min_elev_rad)
                for x in contact_maxima
            ]
            result += [
                (
                    gsid,
                    satid,
                    start,
                    end,
                )
                for start, end in contacts
                if (not strip_start_end or (start >= start_time and
                                            end <= start_time + duration))
            ]

    return result


# === RRs ===


def _isl_distance(sat1, sat2, time):
    dt_obj = datetime.datetime.utcfromtimestamp(time)
    # get the position of sat1 at given time
    sat1.compute(dt_obj)
    # create an observer for sat2 at the position of sat1
    sat2_obs = ephem.Observer()
    # pylint: disable=assigning-non-slot
    sat2_obs.lat = str(sat1.sublat)
    sat2_obs.lon = str(sat1.sublong)
    sat2_obs.elevation = sat1.elevation
    sat2_obs.date = dt_obj
    # pylint: enable=assigning-non-slot
    # compute range from observer at sat1 to sat2, in km
    sat2.compute(sat2_obs)
    return sat2.range / 1000.0


def _minimize_isl_distance(sat1, sat2, rough_time, delta, precision):
    bracket_interval = [
        rough_time - delta, rough_time, rough_time + delta
    ]
    return optimize.minimize_scalar(
        lambda x: _isl_distance(sat1, sat2, x),
        bracket=bracket_interval,
        tol=precision,
    ).x


def _get_isl_zeros(sat1, sat2, lower, minx, upper, isl_range):
    return (
        optimize.brentq(
            lambda x: _isl_distance(sat1, sat2, x) - isl_range,
            lower,
            minx,
        ),
        optimize.brentq(
            lambda x: _isl_distance(sat1, sat2, x) - isl_range,
            minx,
            upper,
        ),
    )


def _get_isl_contacts(satid1, satid2, satobj1, satobj2,
                      dist_contact_minima, tested_time_offsets,
                      start_time, duration, max_duration, isl_range,
                      strip_start_end):
    highest = start_time - max_duration
    result = []
    for cur_min in dist_contact_minima:
        lower = None
        for off in tested_time_offsets:
            if _isl_distance(satobj1, satobj2, cur_min - off) > isl_range:
                lower = cur_min - off
                break
        if lower is None or lower < highest:
            # not found or overlap
            continue
        upper = None
        for off in tested_time_offsets:
            if _isl_distance(satobj1, satobj2, cur_min + off) > isl_range:
                upper = cur_min + off
                highest = upper + 1e-3
                break
        if upper is None:
            continue
        start, end = _get_isl_zeros(
            satobj1,
            satobj2,
            lower,
            cur_min,
            upper,
            isl_range,
        )
        # only add contact if start and end not outside interval
        # (or strip_start_end is False)
        if (not strip_start_end or (start >= start_time and
                                    end <= start_time + duration)):
            result.append((
                satid1,
                satid2,
                start,
                end,
            ))
    return result


def get_isl_contact_tuples(sat_list, start_time, duration, isl_range,
                           precision=0.1, max_duration=600.0, step=100.0,
                           bracket_step=50.0, strip_start_end=True):
    """
    Creates a list of contact tuples of the form (node1, node2, start, end)
    for all ISL contacts (RRs) in the given scenario.
    The tuples represent bi-directional contacts.

    NOTE: Depending on which values you choose for max_duration, step,
    and bracket_step, this may not find all contacts or may get
    overly CPU-intensive.

    Arguments:
        - sat_list: [{"id": "abc", "tle": ["...", "..."]}, ...]
        - start_time: UNIX timestamp
        - duration: [in seconds]
        - isl_range: minimum range for ISLs to be established, in km
        - precision: fitting / maximization precision, in seconds
        - max_duration: maximum assumed duration of ISLs, in seconds
          Note: If this is too long, the zero-finding algorithm will fail.
        - step: simulation step, in seconds
        - bracket_step: The step, in seconds, to find the bracketing interval
          for determining the zeros/roots (the contact start and end-time)
          around the range minimum in the center of the contact
        - strip_start_end: remove contacts which start or end outside of
          the specified interval
    """

    w_sats = [
        (
            e["id"],
            ephem.readtle(str(e["id"]), *[str(s) for s in e["tle"]]),
        )
        for e in sat_list
    ]

    # We test a set of offsets from the minimum, which grows linearly.
    # -> This improves results but has a performance penalty.
    # It is planned to improve performance by using a better root-finding
    # approach.
    tested_time_offsets = tuple([
        bracket_step * (i + 1)
        for i in range(int(max_duration / bracket_step))
    ])

    times = np.arange(start_time, start_time + duration, step)
    result = []
    for satnum1, (satid1, satobj1) in enumerate(w_sats):
        for satnum2, (satid2, satobj2) in enumerate(w_sats):
            # each pair should only be analyzed once
            if satnum1 >= satnum2:
                continue
            # get some samples
            dist_windows = [_isl_distance(satobj1, satobj2, t) for t in times]
            # get samples for approximate distance minima based on changes
            # in sign of difference between subsequent array values
            ldiff = np.ediff1d(dist_windows, to_begin=0.0)
            rdiff = np.ediff1d(dist_windows, to_end=0.0)
            dist_rough_minima = times[(ldiff < 0.0) & (rdiff > 0.0)]
            # search around approximate minima to find the precise minima
            dist_precise_minima = [
                _minimize_isl_distance(satobj1, satobj2, x, step, precision)
                for x in dist_rough_minima
            ]
            # filter contacts by maximum distance
            dist_contact_minima = [
                x
                for x in dist_precise_minima
                if _isl_distance(satobj1, satobj2, x) < isl_range
            ]
            # start and end are the zeros around the minimum
            result += _get_isl_contacts(
                satid1,
                satid2,
                satobj1,
                satobj2,
                dist_contact_minima,
                tested_time_offsets,
                start_time,
                duration,
                max_duration,
                isl_range,
                strip_start_end,
            )
    return result


# RRi
def get_hot_spot_contact_tuples(gs_list, start_time, duration):
    """
    Creates a list of contact tuples of the form (node1, node2, start, end)
    for all hot spots in the given scenario.
    The tuples represent bi-directional contacts.

    Arguments:
        - gs_list: [{"id": "abc", "lat": <rad>, "lon": <rad>,
                "hot": <bool>}, ...]
        - start_time: UNIX timestamp
        - duration: [in seconds]
    """
    # interconnect all "hot" gs with one another during
    # [start_time, start_time + duration]
    hot = [
        station
        for station in gs_list
        if "hot" in station and station["hot"]
    ]
    result = []
    for num1, station1 in enumerate(hot):
        for num2, station2 in enumerate(hot):
            # each pair should only be analyzed once
            if num1 >= num2:
                continue
            result.append((
                station1["id"],
                station2["id"],
                start_time,
                start_time + duration,
            ))
    return result
