import datetime
import re
from enum import Enum
from typing import List, Tuple

import pandas as pd
from dateutil import relativedelta

from fastabf.DAL import dal_admitted_acute
from fastabf.datatypes import MDC_Type, Stay_Category

# TODO fill in METeOR ids for inputs where available


# Get stay category
def helper_get_stay_category(
        AR_DRG_v10: str, bool_same_day_flag: bool, non_icu_los: int) -> Stay_Category:
    """Generates stay category from ARDRGv10, same day flag and non_ICU length of stay

    Arguments:
        AR_DRG_v10 {str} -- AR DRG v10
        bool_same_day_flag {bool} -- 
        non_icu_los {int} -- length of stay (excluding ICU) in days

    Raises:
        ValueError: if an unexpected error occurs

    Returns:
        Stay_Category -- [description]
    """
    # same day stay cat
    if bool_same_day_flag and dal_admitted_acute.bool_is_same_day_drg(AR_DRG_v10):
        stay_cat = Stay_Category.same_day

    else:
        drglowerbound, drgupperbound = dal_admitted_acute.get_drg_stay_bounds(
            AR_DRG_v10)

        if non_icu_los < drglowerbound:
            stay_cat = Stay_Category.short_stay_outlier

        elif drglowerbound <= non_icu_los <= drgupperbound:
            stay_cat = Stay_Category.inlier

        elif non_icu_los > drgupperbound:
            stay_cat = Stay_Category.long_stay_outlier
        else:
            raise ValueError("unexpected case")

    return stay_cat


def get_mdc_for_ardrgv10(ar_drg_v10: str) -> MDC_Type:

    ar_drg_v10_snip = ar_drg_v10[0:3]
    try:
        mdc_type = dal_admitted_acute.get_mdc_for_ardrgv10(ar_drg_v10_snip)
    except Exception as E1:
        raise ValueError(f"Invalid DRG for map to MDC: {E1}")
    return mdc_type
# <end of ARDRG to MDC mapper preparation>


def bool_is_icu_bundled(ar_drg_v10: str) -> bool:
    return dal_admitted_acute.table_is_icu_bundled.get(ar_drg_v10)


def bool_is_drg_intervention(ar_drg_v10: str) -> bool:
    # lookup mapping tables for this ar_drg_v10:
    # if intervention return True else if medical return False
    ar_drg_v10_snip = ar_drg_v10[0:3]
    try:
        bool_is_intervention = dal_admitted_acute.get_bool_is_intervention(
            ar_drg_v10_snip)
    except Exception as E1:
        raise ValueError(f"Invalid DRG for map to MDC: {E1}")
    return bool_is_intervention


def get_base_nwau(ar_drg_v10: str, stay_cat: Stay_Category,
                  non_icu_los_days: float) -> float:
    """Returns the base NWAU from the relevant tables.

    - Infer stay category
    - Lookup PW based on same day status.
    - Apply outlier adjustments if needed based on stay duration and
    perdiems

    Returns:
        [float] -- base NWAU with length of stay based adjustments
    """
    if stay_cat == Stay_Category.same_day:
        base_pw = dal_admitted_acute.get_same_day_pw(ar_drg_v10)
    elif stay_cat == Stay_Category.short_stay_outlier:
        base_pw_elements = dal_admitted_acute.get_short_outlier_pw_elements(
            ar_drg_v10)
        short_stay_outlier_base = base_pw_elements["short_stay_outlier_base"]
        short_stay_outlier_perdiem = base_pw_elements["short_stay_outlier_perdiem"]
        base_pw = (
            short_stay_outlier_base + short_stay_outlier_perdiem * non_icu_los_days
        )
    elif stay_cat == Stay_Category.inlier:
        base_pw = dal_admitted_acute.get_inlier_pw(ar_drg_v10)
    elif stay_cat == Stay_Category.long_stay_outlier:
        inlier_pw = dal_admitted_acute.get_inlier_pw(ar_drg_v10)
        _, upper_bound = dal_admitted_acute.get_drg_stay_bounds(
            ar_drg_v10)
        long_stay_outlier_perdiem = dal_admitted_acute.get_long_stay_outlier_perdiem(
            ar_drg_v10)
        base_pw = (
            inlier_pw + (non_icu_los_days - upper_bound) *
            long_stay_outlier_perdiem
        )
    else:
        raise RuntimeError("Unexpected stay category")

    return base_pw


if __name__ == "__main__":
    pass
