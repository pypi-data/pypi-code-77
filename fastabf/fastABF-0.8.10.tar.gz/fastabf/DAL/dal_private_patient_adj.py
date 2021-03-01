import pandas as pd

from fastabf.datatypes import (Care_Type, Hosp_State_Category,
                               care_type_to_caretypemapper)

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates


# creating private patient accommodation adjustments

filename_private_acc_adjustment = "private_acc_data.csv"
location_private_acc_adjustment = pkg_resources.open_text(
    csvstores, filename_private_acc_adjustment)
df_acc_adjustment = pd.read_csv(location_private_acc_adjustment, index_col=0)


def get_private_patient_accommodation_adjustment_perdiem(
        bool_same_day_flag: bool,
        hosp_state_val: Hosp_State_Category) -> float:
    """
    The mappings are obtained From Appendix F
    Context: holds true for **both**
    -  admitted acute as well as
    - admitted subacute and non-acute
    This is why we keep this function within this module instead of
    duplicating it inside the admitted acute or admitted subacute modules.

    Arguments:
        bool_same_day_flag {bool} -- [description]
        hosp_state_val {Hosp_State_Category} -- [description]

    Returns:
        float -- the accommodation adjustment **per diem**
    """
    if bool_same_day_flag:
        acc_adj = df_acc_adjustment.loc[hosp_state_val.name]["same_day"]
    else:
        acc_adj = df_acc_adjustment.loc[hosp_state_val.name]["overnight"]

    return acc_adj


# <start of data mapping for patient service adjustment for subacute and nonacute>
# Note: as the private patient service adjustment is for ANSNAP (admitted subacute/nonacute, this dataframe will be used
# in the dal_admitted_subandnonacute module to create the required mappings rather than
# being held here).

filename_private_service_adjustment = "private_service_data.csv"
location_private_service_adjustment = pkg_resources.open_text(
    csvstores, filename_private_service_adjustment)

df_converter = dict()
df_converter['care_type'] = lambda x: Care_Type(care_type_to_caretypemapper.get(
    x.strip()))
df_privatepatient_service_snap = pd.read_csv(location_private_service_adjustment,
                                             converters=df_converter,
                                             index_col=0
                                             ).squeeze()


def get_private_pat_service_adj(care_type: Care_Type) -> float:
    return df_privatepatient_service_snap[care_type]
