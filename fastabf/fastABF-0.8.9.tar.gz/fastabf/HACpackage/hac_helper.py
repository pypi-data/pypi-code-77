import bisect
from enum import Enum


import pandas as pd

from fastabf.datatypes import MDC_Type, Sex_Category
from fastabf.HACpackage.hac_processor import (HAC_Category,
                                              HAC_Complexity_Category)

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates

# <Defining HAC helper functions>

# <Start of defining Age complexity adjustment functions>
# Reading data and creating functions for HAC age based complexity

# The following reads data for HACs except HAC 15.2 (as HAC 15.2 has different age range slots).
# To see the raw data you can open up the excel/ODS file `path_to_age_group_file`


filename_hac_except15p2csv = "hac_except15p2data.csv"
path_to_hac_except15p2csv = pkg_resources.open_text(
    csvstores, filename_hac_except15p2csv)

df_hac_except15p2_age = pd.read_csv(path_to_hac_except15p2csv, index_col=0)
# now map the column names from hacN to the respective HAC category
df_hac_except15p2_age.columns = [
    HAC_Category(int(_.strip("hac"))) for _ in df_hac_except15p2_age.columns
]

# To match an age with the age-ranges we allocate ages using a bisection splitting approach
# First we create the breakpoints

# Explanation for the line below: take all the index values (which would be of the form
# Number1toNumber2 and use the higher bound (Number2) to construct the cutoff - which would be
# (1+Number2). We add  +1 to the bound to account for the fact
# that the cutoff is inclusive i.e. an age of 4 should fall into the 01to04 age range
upper_inclusive_bounds_breakpoints = [
    int(_.split("to")[1]) + 1 for _ in list(df_hac_except15p2_age.index.values)
]

# We load the age ranges and adjustments and specific breakpoints for HAC 15.2
# (which has separate age ranges that are not aligned with the age-ranges for
# the other HACs)


filename_hac_15p2csv = "hac_15p2data.csv"
path_to_hac_15p2csv = pkg_resources.open_text(
    csvstores, filename_hac_15p2csv)
df_hac_age_15p2 = pd.read_csv(path_to_hac_15p2csv, index_col=0)

df_hac_age_15p2.columns = [HAC_Category(15.2)]
upper_inclusive_bounds_breakpoints_15p2 = [
    int(_.split("to")[1]) + 1 for _ in list(df_hac_age_15p2.index.values)
]
index_to_get_for_15p2 = range(len(df_hac_age_15p2))


def get_range_indx(score, breakpoints):
    index_to_get = bisect.bisect(breakpoints, score)
    return index_to_get


def get_age_based_hac_complexity(age: int, hac_cat: HAC_Category) -> float:
    """Given patient age and the HAC_Category, return the age based complexity

    Arguments:
        age {int} -- Patient age
        hac_cat {HAC_Category} -- HAC_Category

    Returns:
        float -- the age complexity
    """
    if hac_cat == HAC_Category.Fourth_degree_perineal_laceration_during_delivery:
        breakpoints_to_use = upper_inclusive_bounds_breakpoints_15p2
        df_to_use = df_hac_age_15p2
    else:
        breakpoints_to_use = upper_inclusive_bounds_breakpoints
        df_to_use = df_hac_except15p2_age

    dfindx = get_range_indx(age, breakpoints_to_use)
    age_complexity = df_to_use.iloc[dfindx].get(hac_cat, 0)
    return age_complexity


# <End of defining Age complexity adjustment functions>


# <Start of defining Charlson complexity adjustment functions>
# first read the data

filename_charlson_data = "charlson_data.csv"
path_to_charlson_data = pkg_resources.open_text(
    csvstores, filename_charlson_data)

df_charlson = pd.read_csv(path_to_charlson_data, index_col=0)

# map the column names to HAC_Categories
df_charlson.columns = [HAC_Category(int(_.strip("hac")))
                       for _ in df_charlson.columns]


def get_charlson_hac_complexity(charlson_score: int, hac_cat: HAC_Category):
    return df_charlson.loc[10].get(hac_cat, 0)


# <End of defining Charlson complexity adjustment functions>


# <Start of defining MDC complexity adjustment functions>
# start by reading the data and mapping the columns to HAC categories


filename_mdc_factor_data = "mdc_factor_data.csv"
path_to_mdc_factor_file = pkg_resources.open_text(
    csvstores, filename_mdc_factor_data)
df_mcd_factor = pd.read_csv(path_to_mdc_factor_file, index_col=0)

df_mcd_factor.columns = [
    HAC_Category(float(_.strip("hac"))) for _ in df_mcd_factor.columns
]
# now replace the index using the MDC enum values
df_mcd_factor.index = [
    MDC_Type[mdcname]
    for mdcname in [
        f"{_.lower().replace(' ', '_').split('(')[0]}"
        for k, _ in enumerate(df_mcd_factor.index)
    ]
]


def get_mdc_complexity_for_hac(mdc_cat: MDC_Type, hac_cat: HAC_Category) -> float:
    return df_mcd_factor.loc[mdc_cat].get(hac_cat, 0)


# <END of defining MDC complexity adjustment functions>


# <Start of function to get baseline complexity>


filename_hac_baseline_data = "hac_table_baseline_data.csv"
path_to_hac_baseline_data = pkg_resources.open_text(
    csvstores, filename_hac_baseline_data)
df_baseline = pd.read_csv(path_to_hac_baseline_data, index_col=0)

df_baseline.columns = [HAC_Category(float(_.strip("hac")))
                       for _ in df_baseline.columns]


def get_baselinecomplexity_for_hac(hac_cat: HAC_Category) -> float:
    return df_baseline.loc["Baseline"].get(hac_cat, 0)


# <End of function to get baseline complexity>


# <start of function to get complexity adjustment depending on if the DRG is
# for an intervention or medical type>


def get_drg_type_complexity_adjustment_for_HAC(
    hac_cat: HAC_Category, bool_is_intervention=False
) -> float:
    """ Function to get complexity adjustment depending on if the DRG is for
    an intervention or medical type
    Arguments:
        hac_cat {HAC_Category} -- HAC_Category

    Keyword Arguments:
        bool_is_intervention {bool} -- True if it is of type intervention,
            False if it is of type medical (default: {False})

    Returns:
        float -- [description]
    """
    if bool_is_intervention:
        return df_baseline.loc["AR_DRG_10_Type_Intervention"].get(hac_cat, 0)
    else:
        return df_baseline.loc["AR_DRG_10_Type_Medical"].get(hac_cat, 0)


# <end of function to get complexity adjustment depending on if the DRG is for
# an intervention or medical type>


# <Start of gender complexity adjustment function>
def get_gender_complexity_adjustment_for_HAC(
        hac_cat: HAC_Category, sex_category: Sex_Category) -> float:
    if sex_category == Sex_Category.Male:
        return df_baseline.loc["Male"].get(hac_cat)
    elif sex_category == Sex_Category.Female:
        return df_baseline.loc["Female"].get(hac_cat)
    else:
        raise ValueError(
            "Non binary sex type not supported in HAC module/ NWAU HAC tables"
        )


# <end of gender complexity adjustment function>

# <start of short functions to get adjustments for various other boolean flags>
# Apply Emergency (boolean), ICU, transfer complexity


def get_emergency_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_is_emergency_admission: bool) -> float:
    if not bool_is_emergency_admission:
        return 0.0
    else:
        return df_baseline.loc["Emergency_admission"].get(hac_cat)


def get_ICU_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_ICU_hours: bool) -> float:
    if not bool_ICU_hours:
        return 0.0
    else:
        return df_baseline.loc["ICU_hours"].get(hac_cat, 0)


def get_admission_transfer_complexity_adjustment_for_HAC(
        hac_cat: HAC_Category, bool_is_admission_transfer: bool) -> float:
    if not bool_is_admission_transfer:
        return 0.0
    else:
        return df_baseline.loc["Admission_transfer"].get(hac_cat, 0)


def get_foetal_distress_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_foetal_distress_flag: bool) -> float:
    if not bool_foetal_distress_flag:
        return 0.0
    else:
        return df_baseline.loc["foetal_distress"].get(hac_cat, 0)


def get_instrument_use_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_instrument_use_flag: bool) -> float:
    if not bool_instrument_use_flag:
        return 0.0
    else:
        return df_baseline.loc["instrument_use"].get(hac_cat, 0)


def get_ppop_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_ppop_flag: bool) -> float:
    # For Persistent posterior occiput presentation
    if not bool_ppop_flag:
        return 0.0
    else:
        return df_baseline.loc["ppop_flag"].get(hac_cat, 0)


def get_primiparity_complexity_adjustment_for_HAC(hac_cat: HAC_Category, bool_prima_flag: bool) -> float:
    # young_and_mature_primigravida flag
    if not bool_prima_flag:
        return 0.0
    else:
        return df_baseline.loc["young_and_mature_primigravida"].get(hac_cat, 0)


# <end  of short functions to get adjustments for various other boolean flags>


# <Start of functions related to assigning HAC complexity categories from HAC scores>

filename_hac_complexity_data = "hac_complexity_mapping_data.csv"
path_to_hac_complexity_data_file = pkg_resources.open_text(
    csvstores, filename_hac_complexity_data)

df_complexity_assignment = pd.read_csv(
    path_to_hac_complexity_data_file, index_col=0)

df_complexity_assignment.columns = [
    HAC_Category(float(_.strip("hac"))) for _ in df_complexity_assignment.columns
]

#  infer complexity group from complexity score and assign the appropriate
#  adjustment after damping

# First load the data

filename_hac_adj_data = "hac_adjustments_mapping_data.csv"
path_to_hac_adj_data_file = pkg_resources.open_text(
    csvstores, filename_hac_adj_data)
df_after_damping = pd.read_csv(
    path_to_hac_adj_data_file, index_col=0)


# remap the columns to HAC Categories
df_after_damping.columns = [
    HAC_Category(float(_.strip("hac"))) for _ in df_after_damping.columns
]
# remap the index (rows) to HAC_complexity categories
df_after_damping.index = [HAC_Complexity_Category[_]
                          for _ in df_after_damping.index]


def infer_complexity_group_from_score(
    hac_cat: HAC_Category, score: float
) -> HAC_Complexity_Category:
    df_breakpoints = df_complexity_assignment[hac_cat]
    breakpoints = [df_breakpoints.Moderate, df_breakpoints.High]
    return HAC_Complexity_Category(get_range_indx(score, breakpoints))


def get_adjustment_after_damping(
    hac_cat: HAC_Category, hac_complexity_cat: HAC_Complexity_Category
) -> float:
    """Given the HAC category and HAC complexity category return the
    adjustment after damping (as a float)
    Arguments:
        hac_cat {HAC_Category} -- HAC category
        hac_complexity_cat {HAC_Complexity_Category} -- i.e The Enum for Low,
        Medium or High complexity.

    Returns:
        float --  the % adjustment expressed as a float
    """
    return df_after_damping.loc[hac_complexity_cat].get(hac_cat) / 100.0


if __name__ == "__main__":
    pass
