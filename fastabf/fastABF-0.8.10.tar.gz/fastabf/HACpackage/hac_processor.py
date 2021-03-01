from enum import Enum
from typing import List

import pandas as pd

from fastabf.datatypes import MDC_Type, Sex_Category


class HAC_Category(Enum):
    Pressure_injury = 1
    Falls_resulting_in_fracture_or_intracranial_injury = 2
    Healthcare_associated_infection = 3
    Surgical_complications_requiring_unplanned_return_to_theatre = 4
    # Unplanned_intensive_care_unit_admission = 5 : not used
    Respiratory_complications = 6
    Venous_thromboembolism = 7
    Renal_failure = 8
    Gastrointestinal_bleeding = 9
    Medication_complications = 10
    Delirium = 11
    Persistent_incontinence = 12
    Malnutrition = 13
    Cardiac_complications = 14
    Fourth_degree_perineal_laceration_during_delivery = 15.2

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class HAC_Complexity_Category(Enum):
    Low = 0
    Moderate = 1
    High = 2

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


def compute_adjustment_to_apply(age: int,
                                hac_cat_list: List[HAC_Category],
                                charlson_score: int,
                                mdc_cat: MDC_Type,
                                bool_is_intervention: bool,
                                sex_category: Sex_Category,
                                bool_is_emergency_admission: bool,   # METeOR id: 269986
                                bool_ICU_hours: bool,
                                bool_is_admission_transfer: bool,
                                bool_foetal_distress_flag: bool,
                                bool_instrument_use_flag: bool,
                                bool_ppop_flag: bool,
                                bool_prima_flag: bool) -> float:
    """Function that computes the HAC adjustment to apply given the several factors required to
    compute that decision. These steps are based on the detailed HAC adjustment steps described in 
    the "Pricing and funding for safety and quality" document subtitled "Risk
    adjusted model for hospital acquired complications NEP 2020-21"

    Arguments:
        age {int} -- Age
        hac_cat_list {List[HAC_Category]} --  list of enums from the HAC_Category 
        charlson_score {int} -- The Charlson score (ranges from 0-16)
        mdc_cat {MDC_Type} -- MDC category type
        bool_is_intervention {bool} -- True if the AR DRG is for a medical intervention/procedure/operation rather than for a disease
        sex_category {Sex_Category} -- Enum for Sex [METeOR id: 635126]
        bool_is_emergency_admission {bool} -- Whether admission occurred on an emergency basis, as represented by a code [METeOR id:269986]
        bool_is_admission_transfer {bool} -- The machanism by which a person begins an episode of care, as represented by a code. True if the admission was a transfer [METeOR id:269976]
        bool_foetal_distress_flag {bool} -- True if foetal distress
        bool_instrument_use_flag {bool} -- True for use of instruments 
        bool_ppop_flag {bool} -- True for Persistent posterior occiput presentation
        bool_prima_flag {bool} -- True for young_and_mature_primigravida

    Returns:
        float -- the net adjustment factor to apply (this is after damping has been applied  
        and all HACs have been considered) 
    """

    # First a quick path for an empty HAC list
    if len(hac_cat_list) == 0:
        return 0.0

    # Phase 1:
    # Calculate the overall complexity score for each HAC in an episode by summing
    # the complexity scores derived from each risk factor variable relevant to each
    # HAC (Section5.2).

    # <start phase 1>
    # We store the result of each step and then transform it into data frame. This is easy to
    # test, visualize and debug from

    # firstly generate a dict container to store the complexity scores
    # from hac_helper import get_baselinecomplexity_for_hac
    from fastabf.HACpackage import hac_helper
    df_hac_proc_dict = dict()

    # step 1: get baseline
    df_hac_proc_dict["baseline"] = {hac_helper.get_baselinecomplexity_for_hac(
        hac_cat) for hac_cat in hac_cat_list}
    # step 2: get age group complexity
    df_hac_proc_dict["agebased"] = {hac_helper.get_age_based_hac_complexity(
        age, hac_cat) for hac_cat in hac_cat_list}
    # step 3: Charlson score complexity
    df_hac_proc_dict["charlson_score"] = {hac_helper.get_charlson_hac_complexity(
        charlson_score, hac_cat) for hac_cat in hac_cat_list}
    # step 4: DRG complexity adjustment
    df_hac_proc_dict["drg_type"] = {hac_helper.get_drg_type_complexity_adjustment_for_HAC(
        hac_cat, bool_is_intervention) for hac_cat in hac_cat_list}
    # step 5: Gender complexity adjustment
    df_hac_proc_dict["gender_factor"] = {hac_helper.get_gender_complexity_adjustment_for_HAC(
        hac_cat, sex_category) for hac_cat in hac_cat_list}
    # step 6: MDC complexity adjustment
    df_hac_proc_dict["mdc_factor"] = {hac_helper.get_mdc_complexity_for_hac(
        mdc_cat=mdc_cat, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 7: Emergency admission adjustment
    df_hac_proc_dict["emergency_factor"] = {hac_helper.get_emergency_complexity_adjustment_for_HAC(
        bool_is_emergency_admission=bool_is_emergency_admission, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 8: ICU adjustment
    df_hac_proc_dict["icu_factor"] = {hac_helper.get_ICU_complexity_adjustment_for_HAC(
        bool_ICU_hours=bool_ICU_hours, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 9: transfer status adjustment
    df_hac_proc_dict["transfer_status_factor"] = {hac_helper.get_admission_transfer_complexity_adjustment_for_HAC(
        bool_is_admission_transfer=bool_is_admission_transfer, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 10: foetal distress adjustment
    # get_foetal_distress_complexity_adjustment_for_HAC
    df_hac_proc_dict["foetal_distress_factor"] = {hac_helper.get_foetal_distress_complexity_adjustment_for_HAC(
        bool_foetal_distress_flag=bool_foetal_distress_flag, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 11: get_instrument_use_complexity_adjustment_for_HAC
    df_hac_proc_dict["instrument_use_factor"] = {hac_helper.get_instrument_use_complexity_adjustment_for_HAC(
        bool_instrument_use_flag=bool_instrument_use_flag, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 11: PPOP factor (Persistent posterior occiput presentation)
    # get_ppop_complexity_adjustment_for_HAC
    df_hac_proc_dict["ppop_factor"] = {hac_helper.get_ppop_complexity_adjustment_for_HAC(
        bool_ppop_flag=bool_ppop_flag, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # step 12: get Primary : young_and_mature_primigravida flag
    df_hac_proc_dict["prima_factor"] = {hac_helper.get_primiparity_complexity_adjustment_for_HAC(
        bool_prima_flag=bool_prima_flag, hac_cat=hac_cat) for hac_cat in hac_cat_list}

    # now store the above risk factors for each of the HAC categories in a data frame
    df_hac_proc = pd.DataFrame.from_dict(
        data=df_hac_proc_dict, orient="index", columns=hac_cat_list)

    # <end phase 1>

    # Phase 2: infer complexity group from total complexity score and assign the
    # appropriate adjustment after damping
    # <start phase 2>
    # First create a container to store intermediate results for the adjustment calculations
    df_hac_adjustment_dict = dict()

    # Now sum the complexity for each HAC Category
    df_hac_adjustment_dict['total_complexity'] = df_hac_proc.sum().to_dict()

    # step 2a: infer the HAC complexity group (low/medium/high) from the category
    # type and total complexity
    df_hac_adjustment_dict["hac_complexity_group"] = {hac_cat: hac_helper.infer_complexity_group_from_score(
        hac_cat=hac_cat, score=total_complexity) for hac_cat, total_complexity in df_hac_adjustment_dict['total_complexity'].items()}

    # step 2b: now obtain the HAC adjustment fraction after damping using the hac_complexity_group found above in step 2a
    df_hac_adjustment_dict["hac_adjusted_post_damping_fraction"] = {hac_cat: hac_helper.get_adjustment_after_damping(hac_cat=hac_cat, hac_complexity_cat=hac_complexity_cat)
                                                                    for hac_cat, hac_complexity_cat in df_hac_adjustment_dict["hac_complexity_group"].items()}

    # bundle the results from phase 2 into a data frame
    df_hac_adjustment = pd.DataFrame.from_dict(
        data=df_hac_adjustment_dict, orient="index", columns=hac_cat_list)
    # <end phase 2>

    # Now, the highest adjustment is selected
    adjustment_factor_to_return = df_hac_adjustment.loc[
        "hac_adjusted_post_damping_fraction"].max()

    return adjustment_factor_to_return


if __name__ == "__main__":
    import hac_helper as hac_helper
