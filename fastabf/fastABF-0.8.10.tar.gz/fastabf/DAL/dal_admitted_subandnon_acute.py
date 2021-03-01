import re

import pandas as pd

from fastabf.DAL import dal_private_patient_adj
from fastabf.datatypes import (Care_Type, Stay_Category,
                               care_type_to_caretypemapper)

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates


def map_care_type_to_enum(caretype: str) -> Care_Type:
    try:
        care_type_val = care_type_to_caretypemapper[caretype.strip()]
    except:
        raise RuntimeError("Unsupported care type string")
    return care_type_val


def bool_payment_list_mapper(bool_string: str) -> bool:
    return bool_string.strip().lower() == "yes"


df_ansnap_converters = dict()
df_ansnap_converters["inlier_lb"] = lambda x: int(x)
df_ansnap_converters["inlier_ub"] = lambda x: int(x)
df_ansnap_converters['care_type'] = lambda x: Care_Type(float(x))


filename_admitted_subacute = "admitted_subacute_data.csv"
location_admitted_subacute = pkg_resources.open_text(
    csvstores, filename_admitted_subacute)


df_an_snap = pd.read_csv(location_admitted_subacute,
                         converters=df_ansnap_converters,
                         engine="python",
                         index_col=0)

lookup_bool_is_on_same_day_list = (
    df_an_snap["bool_same_day_payment_list"] == True)
inlier_lb_ub_lookup = df_an_snap[["inlier_lb", "inlier_ub"]].to_dict(
    orient="index"
)
same_day_pw_lookup = df_an_snap["pwt_sameday"]
inlier_pw_lookup = df_an_snap["pwt_inlier"]
care_type_lookup = df_an_snap['care_type']
long_stay_outlier_perdiem_lookup = df_an_snap["pwt_longstay_outlier_perdiem"]
shortstay_outlier_base_perdiem_lookup = df_an_snap["pwt_shortstay_outlier_perdiem"]


def get_care_type(an_snap_v4: str) -> Care_Type:
    return care_type_lookup[an_snap_v4]


def get_private_patient_service_adjustment(an_snap_v4: str) -> float:
    # map an_snap to caretype
    # then map caretype to adjustment
    care_type = get_care_type(an_snap_v4)
    return dal_private_patient_adj.get_private_pat_service_adj(care_type)


def bool_is_same_day_ansnap(an_snap_v4: str) -> bool:
    """returns if it is a same day drg or not
    Arguments:
        an_snap_v4 {str} -- AR_DRG v10

    Returns:
        bool -- True if same day drg
    """
    return lookup_bool_is_on_same_day_list[an_snap_v4]


def get_ansnap_stay_bounds(an_snap_v4: str) -> tuple:
    lb_ub_dict = inlier_lb_ub_lookup[an_snap_v4]
    return (lb_ub_dict["inlier_lb"], lb_ub_dict["inlier_ub"])


def get_same_day_pw(an_snap_v4: str) -> float:
    # get same day price weight
    return same_day_pw_lookup.get(an_snap_v4)


def get_inlier_pw(an_snap_v4: str) -> float:
    # get price weight in case of inlier
    return inlier_pw_lookup.get(an_snap_v4)


def get_long_stay_outlier_perdiem(an_snap_v4: str) -> float:
    return long_stay_outlier_perdiem_lookup[an_snap_v4]


def get_short_say_outlier_perdiem(an_snap_v4: str) -> float:
    return shortstay_outlier_base_perdiem_lookup[an_snap_v4]


def helper_get_stay_category(
    an_snap_v4: str, bool_same_day_flag: bool,
        los_days: int) -> Stay_Category:
    """Generates stay category from AN_SNAP_v4 and same day flag

    Arguments:
        an_snap_v4{str} -- AN SNAP v4
        bool_same_day_flag {bool} -- 
        los_days {int} -- length of stay 

    Raises:
        ValueError: if an unexpected error occurs

    Returns:
        Stay_Category -- [description]
    """
    # same day stay cat
    if bool_same_day_flag and bool_is_same_day_ansnap(an_snap_v4):
        stay_cat = Stay_Category.same_day

    else:
        ansnaplowerbound, ansnapupperbound = get_ansnap_stay_bounds(
            an_snap_v4)

        if los_days < ansnaplowerbound:
            stay_cat = Stay_Category.short_stay_outlier

        elif ansnaplowerbound <= los_days <= ansnapupperbound:
            stay_cat = Stay_Category.inlier

        elif los_days > ansnapupperbound:
            stay_cat = Stay_Category.long_stay_outlier
        else:
            raise ValueError("unexpected case")

    return stay_cat


def get_base_nwau(an_snap_v4: str, stay_cat: Stay_Category,
                  los_days: float) -> float:
    """Returns the base NWAU from the relevant tables.

    - Infer stay category
    - Lookup PW based on same day status.
    - Apply outlier adjustments if needed based on stay duration and
    perdiems

    Returns:
        [float] -- base NWAU with length of stay based adjustments
    """
    if stay_cat == Stay_Category.same_day:
        base_pw = get_same_day_pw(an_snap_v4)
    elif stay_cat == Stay_Category.short_stay_outlier:
        short_stay_outlier_perdiem = get_short_say_outlier_perdiem(an_snap_v4)

        base_pw = (
            short_stay_outlier_perdiem * los_days
        )
    elif stay_cat == Stay_Category.inlier:
        base_pw = get_inlier_pw(an_snap_v4)
    elif stay_cat == Stay_Category.long_stay_outlier:
        inlier_pw = get_inlier_pw(an_snap_v4)
        _, upper_bound = get_ansnap_stay_bounds(
            an_snap_v4)
        long_stay_outlier_perdiem = get_long_stay_outlier_perdiem(
            an_snap_v4)
        base_pw = (
            inlier_pw + (los_days - upper_bound) * long_stay_outlier_perdiem
        )
    else:
        raise RuntimeError("Unexpected stay category")

    return base_pw
