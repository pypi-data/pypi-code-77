import pdb
import re

import pandas as pd

from fastabf.datatypes import MDC_Type

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates

filename_admitted_acute = "admitted_acute_data.csv"
location_admitted_acute = pkg_resources.open_text(
    csvstores, filename_admitted_acute)

df_admitted_acute = pd.read_csv(location_admitted_acute, index_col=0)
lookup_is_same_day_drg = df_admitted_acute["bool_same_day_payment_list"]
inlier_lb_ub_lookup = df_admitted_acute[["inlier_lb", "inlier_ub"]].to_dict(
    orient="index"
)
same_day_pw_lookup = df_admitted_acute["pwt_sameday"].fillna(0)
inlier_pw_lookup = df_admitted_acute["pwt_inlier"]
shortstay_outlier_base_perdiem_lookup = df_admitted_acute[
    ["pwt_shortstay_outlierbase", "pwt_shortstay_outlier_perdiem"]
].to_dict(orient="index")
long_stay_outlier_perdiem_lookup = df_admitted_acute["pwt_longstay_outlier_perdiem"]
admitted_acute_paed_lookup = df_admitted_acute["adj_paediatric"]

table_is_icu_bundled = df_admitted_acute.bool_bundled_icu == "YES"


def get_paed_adj_factor_admitted_acute(ar_drg_v10: str) -> float:
    """Finds and returns the pediatric adjustment factor for admitted acute

    Arguments:
        ar_drg_v10 {str} -- AR_DRG v10

    Returns:
        float -- the adjustment factor
    """
    return admitted_acute_paed_lookup[ar_drg_v10]


def bool_is_same_day_drg(ar_drg_v10: str) -> bool:
    """returns if it is a same day drg or not
    Arguments:
        ar_drg_v10 {str} -- AR_DRG v10

    Returns:
        bool -- True if same day drg
    """
    return lookup_is_same_day_drg[ar_drg_v10].strip() != ""


def get_drg_stay_bounds(ar_drg_v10: str) -> tuple:
    lb_ub_dict = inlier_lb_ub_lookup[ar_drg_v10]
    return (lb_ub_dict["inlier_lb"], lb_ub_dict["inlier_ub"])


def get_same_day_pw(ar_drg_v10: str) -> float:
    # get same day price weight
    return same_day_pw_lookup.get(ar_drg_v10)


def get_inlier_pw(ar_drg_v10: str) -> float:
    # get price weight in case of inlier
    return inlier_pw_lookup.get(ar_drg_v10)


def get_long_stay_outlier_perdiem(ar_drg_v10: str) -> float:
    return long_stay_outlier_perdiem_lookup.get(ar_drg_v10)


def get_short_outlier_pw_elements(ar_drg_v10: str) -> dict:
    outlier_base_perdiem_dict = shortstay_outlier_base_perdiem_lookup[ar_drg_v10]
    return {
        "short_stay_outlier_base": outlier_base_perdiem_dict[
            "pwt_shortstay_outlierbase"
        ],
        "short_stay_outlier_perdiem": outlier_base_perdiem_dict[
            "pwt_shortstay_outlier_perdiem"
        ],
    }


lookup_private_patient_service_adjustment = df_admitted_acute["adj_private_patient_service"]


def get_private_patient_service_adjustment(ar_drg_v10: str) -> bool:
    return lookup_private_patient_service_adjustment[ar_drg_v10]


# <start of ARDRG to MDC mapper preparation>

def parse_mdc_column_mdc(val: str) -> MDC_Type:

    try:
        intval = int(val)
        mdc_type = MDC_Type(intval)
    except:
        mdc_type = MDC_Type(val)

    return mdc_type


filename_adrg_mdc_mapper = "adrg_mdc_mapper_data.csv"
location_adrg_mdc_mapper = pkg_resources.open_text(
    csvstores, filename_adrg_mdc_mapper)
df_adrg_mdc_mapper = pd.read_csv(
    location_adrg_mdc_mapper,
    converters={"MDC": lambda x: parse_mdc_column_mdc(x)}
).set_index("ADRG").squeeze()


def get_mdc_for_ardrgv10(ar_drg_v10: str) -> MDC_Type:
    ar_drg_v10_snip = ar_drg_v10[0:3]
    return df_adrg_mdc_mapper[ar_drg_v10_snip]


# <start of designing the mapping from ARDRG to intervention checker>


filename_adrg_intervention_mapper = "adrg_intervention_mapper_data.csv"
location_adrg_intervention_mapper = pkg_resources.open_text(
    csvstores, filename_adrg_intervention_mapper)

df_adrg_intervention_mapper = pd.read_csv(
    location_adrg_intervention_mapper, index_col=0).squeeze()


def get_bool_is_intervention(ar_drg_v10: str) -> bool:
    return df_adrg_intervention_mapper[ar_drg_v10]
