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

zfilltxt = "{:<05}"


def tier2cv5indexconverter(x):
    return zfilltxt.format(str(x)[0:5])


"""

df1col_titles = [
    "tier2cv5",
    "description",
    "price_weight",
    "adj_paediatric"
]

# Tier 2 clinic V5.0	Description	Price weights	Paediatric adjustment

file_path = "/home/app/data/national_efficient_price_determination_2020-21_-_price_weight_tables.ods"


dfconverter = {
    "Tier 2 clinic V5.0": tier2cv5indexconverter
}
df1 = pd.read_excel(
    file_path,
    engine="odf",
    sheet_name="Non-Admitted",
    header=7,
    index_col=None,
    skiprows=None,
    nrows=None,
    usecols="B:F",
    converters=dfconverter
)
df1.columns = df1col_titles
df1 = df1.set_index('tier2cv5')
df_nonadmitted = df1.dropna()

df_nonadmitted.columns = df_nonadmitted.columns.map(
    lambda x: x.strip().lower().replace(" ", "_").replace("-", "_")
)
"""

# df_nonadmitted.to_csv(location_nonadmitted)


def optional_float(x: str):
    try:
        fl = float(x)
        return fl
    except:
        return x


filename_nonadmitted = "nonadmitted_data.csv"
location_nonadmitted = pkg_resources.open_text(
    csvstores, filename_nonadmitted)


dfconverter = {
    "price_weight": lambda x: optional_float(x),
    "adj_paediatric": lambda x: optional_float(x),
    "tier2cv5": lambda x: tier2cv5indexconverter(x)
}
df_nonadmitted = pd.read_csv(location_nonadmitted,
                             converters=dfconverter,
                             ).set_index("tier2cv5")
dfconverter = None

nonadmitted_paed_lookup = df_nonadmitted["adj_paediatric"]
nonadmitted_pw_lookup = df_nonadmitted["price_weight"]


def get_paed_adj_factor(tier2_cv5: str) -> float:
    """Finds and returns the pediatric adjustment factor for non-admitted 

    Arguments:
        tier2_cv5 {str} -- tier 2 cv5 (Tier 2 clinic V5.0)

    Returns:
        float -- the adjustment factor
    """
    return nonadmitted_paed_lookup[tier2_cv5]


def get_base_nwau(tier2_cv5: str) -> float:
    """Returns the base NWAU from the relevant tables.
    Arguments:
        tier2_cv5 {str} -- [description]

    Returns:
        [float] -- base NWAU
    """
    try:
        pw = float(nonadmitted_pw_lookup[tier2_cv5])
    except Exception as E1:
        raise E1
    return pw
