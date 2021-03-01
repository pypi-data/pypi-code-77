import re

import pandas as pd

from fastabf.datatypes import ABF_Service_Category, MDC_Type

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates


filename_urg_department = "emergency_department_data.csv"
filename_udg_service = "emergency_service_data.csv"

location_urg_department = pkg_resources.open_text(
    csvstores, filename_urg_department)

location_udg_service = pkg_resources.open_text(
    csvstores, filename_udg_service)


df_urg = pd.read_csv(location_urg_department, index_col=0)
df_udg = pd.read_csv(location_udg_service, index_col=0)


def get_base_bw_emergency(
        abf_service_cat: ABF_Service_Category,
        urg_v1p4_or_udg_v1p3: int) -> float:

    if abf_service_cat == ABF_Service_Category.emergency_department:
        urg_v1p4 = urg_v1p4_or_udg_v1p3
        base_pw = df_urg.loc[urg_v1p4, "price_weight"]

    elif abf_service_cat == ABF_Service_Category.emergency_services:
        udg_v1p3 = urg_v1p4_or_udg_v1p3
        base_pw = df_udg.loc[udg_v1p3, "price_weight"]
    else:
        raise RuntimeError(
            "This function is for emergency department/services only")
    return base_pw
