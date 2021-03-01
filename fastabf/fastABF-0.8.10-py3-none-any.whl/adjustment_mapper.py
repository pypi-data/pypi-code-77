import datetime as datetime
import re
from typing import List

from dateutil import relativedelta

import fastabf.Helpers.helper_remoteness_mappings as remotenessmapper
from fastabf.DAL import (admitted_acute_helper, dal_admitted_acute,
                         dal_admitted_subandnon_acute, dal_nonadmitted,
                         dal_private_patient_adj)
from fastabf.datatypes import (HOSP_PAED_FLAG, ABF_Service_Category,
                               Hosp_State_Category, Indigenous_Status_Category,
                               MDC_Type, Remoteness_Category_RA16,
                               Sex_Category, hosp_level3ICU_flag)
from fastabf.HACpackage.hac_processor import HAC_Category
from fastabf.HACpackage.hac_processor import \
    compute_adjustment_to_apply as compute_hac_adjustment_to_apply

# import (bool_meets_age_cutoff, get_paed_adj_factor_admitted_acute)


def extract_dd_mm_yyyy(input_date: str) -> datetime.date:
    try:
        dd, mm, yyyy = (
            int(item)
            for item in re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d\d\d\d)", input_date).groups()
        )
        parsed_date = datetime.date(day=int(dd), month=int(mm), year=int(yyyy))
    except Exception as E3:
        raise RuntimeError(f"Issue with date parsing. More information: {E3}")
    return parsed_date


# Constants
Paediatric_Threshold_Age = relativedelta.relativedelta(
    years=17, months=0, days=0)


def bool_meets_age_cutoff(patient_age: relativedelta.relativedelta) -> bool:
    # Total whole years from date of Birth to date of admission.
    return (patient_age.years <= Paediatric_Threshold_Age.years)
    # the code below is required only if you need to cut off the age group
    # exactly on the day
    # or
    # (
    #     (patient_age.years == Paediatric_Threshold_Age.years)
    #     and (patient_age.months == 0 and patient_age.days == 0)


def __bool_meets_paediatric_adjustment_conditions(
        patient_age: relativedelta.relativedelta,
        __hosp_paed_flag: bool = HOSP_PAED_FLAG) -> bool:
    """
    This function determines if the patient meets the
    paediatric_adjustment conditions (this condition holds for all
    service category types)
    """
    bool_age_cutoff = bool_meets_age_cutoff(patient_age)
    # HOSP_PAED_FLAG: bool indicating a specialised children’s hospital
    if bool_age_cutoff and __hosp_paed_flag:
        return True
    else:
        return False


def compute_paediatric_adj(
        ardrgv10_or_tier2cv5: str,
        patient_age: relativedelta.relativedelta,
        abf_service_cat: ABF_Service_Category,
        __hosp_paed_flag: bool = HOSP_PAED_FLAG) -> float:
    # If Paediatric conditions are not met set A_paed to 1 otherwise
    # compute it
    if not __bool_meets_paediatric_adjustment_conditions(
            patient_age, __hosp_paed_flag=__hosp_paed_flag):
        A_paed = 1.0
    else:
        # Refer to column headed paediatric adjustment in the tables of
        # admitted acute price weights (Appendix H) and non-admitted price
        # weights (Appendix K)
        if abf_service_cat == ABF_Service_Category.admitted_acute:
            ar_drg_v10 = ardrgv10_or_tier2cv5
            A_paed = dal_admitted_acute.get_paed_adj_factor_admitted_acute(
                ar_drg_v10)
        elif abf_service_cat == ABF_Service_Category.nonadmitted:
            tier2cv5 = ardrgv10_or_tier2cv5
            A_paed = dal_nonadmitted.get_paed_adj_factor(tier2cv5)
        else:
            A_paed = 1.0

    return A_paed


def compute_psychiatric_age_adj(
        patient_age: relativedelta.relativedelta,
        mdc_type: MDC_Type, psych_days: float,
        abf_service_cat: ABF_Service_Category,
        __hosp_paed_flag: bool = HOSP_PAED_FLAG) -> float:
    """
    Computes the psychiatric age adjustment and applies it.
    Makes a note of it to the list of adjustments applied
    """
    if not(abf_service_cat == ABF_Service_Category.admitted_acute):
        raise RuntimeError(
            "psychiatric age adjustment is only for admitted acute")
    # Gather variables for decision making
    bool_age_cutoff = bool_meets_age_cutoff(patient_age)
    bool_mentalhealth_MDC = mdc_type in [MDC_Type(19), MDC_Type(20)]
    bool_psych_care_days = psych_days >= 1

    # Meets age and care days  and mental health MDC
    if all([bool_age_cutoff, bool_mentalhealth_MDC, bool_psych_care_days]):
        A_spa = 0.44 if not __hosp_paed_flag else 0.18

    # Meets age,and care days but not mental health MDC
    elif all([
        bool_age_cutoff, not bool_mentalhealth_MDC, bool_psych_care_days
    ]):
        A_spa = 0.77 if not __hosp_paed_flag else 0.71

    # Does not meet age req, has care days but no mental health MDC
    elif all(
        [not bool_age_cutoff, not bool_mentalhealth_MDC, bool_psych_care_days]
    ):
        A_spa = 0.33

    else:
        A_spa = 0

    return A_spa


def estimate_remoteness_category(postcode_str: str = "", SA2: int = 0, establishment_remoteness: Remoteness_Category_RA16 = Remoteness_Category_RA16.Unknown) -> Remoteness_Category_RA16:
    """ The NWAU calculation includes an adjustment for patients who reside in
    Outer Regional, Remote, and Very Remote areas. The remoteness is calculated based
    on the patient postcode. If the patient postcode is invalid or unavailable,
    then the patient SLA is used. If the patient SLA is invalid or unavailable,
    then the hospital remoteness is used (RA16).


    Keyword Arguments:
        postcode_str {str} -- [description] (default: {""})
        SA2 {int} --  NNNNNNNNN (9 digit), METeOR id: 469909 (default: {0})
        establishment_remoteness {Remoteness_Category_RA16} -- [description] (default: {Remoteness_Category_RA16.Unknown})

    Raises:
        an: exception
        ValueError: If the remoteness category can not be determined, raise an exception

    Returns:
        Remoteness_Category_RA16 -- The RA2016 remoteness category
    """
    postcode_found = re.search(r"PC(\d{3,4})", postcode_str)
    remoteness_type = Remoteness_Category_RA16.Unknown

    if postcode_found:
        postcode = int(postcode_found.groups()[0])
        remoteness_type = remotenessmapper.get_remoteness_cat_for_postcode(
            postcode)

    if (
        remoteness_type == Remoteness_Category_RA16.Unknown
    ):  # if no postcode found, use SA2 if it exists
        remoteness_type = remotenessmapper.get_remoteness_cat_for_SA2(
            SA2)

    # The fallback estimation from the establishment EST_Remoteness
    # As specified in the `Variable definitions` sheet of the IHPA excel
    # based NWAU computation:
    # the EST_Remoteness is "<snip> Used to assign a
    # Remoteness Area classification to the patient when previous
    # geographic variables are missing and/or invalid.</snip>"
    if (
        remoteness_type == Remoteness_Category_RA16.Unknown
    ):  # postcode and SA2 yielded no useful info
        remoteness_type = establishment_remoteness

    if remoteness_type == Remoteness_Category_RA16.Unknown:
        raise ValueError("Unable to determine remoteness category")

    return remoteness_type


def compute_patient_residential_remoteness_adj(
        remoteness_type: Remoteness_Category_RA16,
        abf_service_cat: ABF_Service_Category) -> float:
    """
    Computes the Patient residential remoteness area adjustment.
    Makes a note of it to the list of adjustments applied
    """

    A_res = 0.0
    # Case1: a person whose residential address is within an area that is
    # classified as being outer regional
    # Admitted acute, admitted subacute or non-admitted patient: 8 per cent
    if remoteness_type == Remoteness_Category_RA16.Outer_Regional:
        if abf_service_cat in [
                ABF_Service_Category.admitted_acute,
                ABF_Service_Category.admitted_subacute,
                ABF_Service_Category.admitted_nonacute,
                ABF_Service_Category.nonadmitted]:
            A_res = 0.08

    # Case 2 a person whose residential address is within an area that is
    # classified as being remote.
    # - Admitted acute, admitted subacute or non-admitted patient: 27 per cent
    # - Emergency department patient: 25per cent
    elif remoteness_type == Remoteness_Category_RA16.Remote:
        if abf_service_cat in [
                ABF_Service_Category.admitted_acute,
                ABF_Service_Category.admitted_subacute,
                ABF_Service_Category.admitted_nonacute,
                ABF_Service_Category.nonadmitted]:
            A_res = 0.27
        elif abf_service_cat in [
                ABF_Service_Category.emergency_department,
                ABF_Service_Category.emergency_services]:
            A_res = 0.25

    # Case 3 a person whose residential address is within an area that is
    # classified as being very remote.
    # - Admitted acute, admitted subacute or non-admitted patient: 30 per cent
    # - Emergency department patient: 25per cent
    elif remoteness_type == Remoteness_Category_RA16.Very_Remote:
        if abf_service_cat in [
                ABF_Service_Category.admitted_acute,
                ABF_Service_Category.admitted_subacute,
                ABF_Service_Category.admitted_nonacute,
                ABF_Service_Category.nonadmitted]:
            A_res = 0.30
        elif abf_service_cat in [
                ABF_Service_Category.emergency_services,
                ABF_Service_Category.emergency_department]:
            A_res = 0.25
    else:
        A_res = 0.0

    return A_res


def compute_indigenous_adj(
        ind_stat: Indigenous_Status_Category,
        abf_service_cat: ABF_Service_Category) -> float:
    """Return the ABF indigenous adjustment
    Context: for a person who identifies as being of Aboriginal and/or
    Torres Strait Islander origin.
    Adjustment: For admitted acute, admitted subacute, emergency department
    or non-admitted patient: 4 per cent

    Arguments:
        ind_stat {Indigenous_Status_Category} -- [description]
        abf_service_cat {ABF_Service_Category} -- [description]

    Returns:
        float -- A_ind (indigenous adjustment)
    """
    if ind_stat in [Indigenous_Status_Category.Aboriginal_not_TSislander,
                    Indigenous_Status_Category.TSislander_not_Aboriginal,
                    Indigenous_Status_Category.Both_Aboriginal_and_TSislander,
                    ]:
        A_ind = 0.04
    else:
        A_ind = 0

    return A_ind


def get_bool_is_radiotherapy_flag(ACHI_code: str) -> bool:
    #  has a specified Australian Classification of Health Interventions (ACHI)
    #  Eleventh Edition radiotherapy intervention code been assigned? Ref appendix B/C
    # https://www.ihpa.gov.au/sites/default/files/publications/national_efficient_price_determination_2020-21.pdf
    raise NotImplementedError()


def compute_radiotherapy_adjustment(
        abf_service_cat: ABF_Service_Category,
        bool_radiotherapy_flag: bool) -> float:
    """
    Computes the radiotherapy adjustment.
    Makes a note of it to the list of adjustments applied
    """
    # Context: Admitted acute or admitted subacute patient with
    # - a specified Australian Classification of Health Interventions
    # (ACHI) Eleventh Edition radiotherapy intervention code assigned

    # Adjustment: For admitted acute or admitted subacute patient: 39 per cent

    if bool_radiotherapy_flag:
        if abf_service_cat in [
                ABF_Service_Category.admitted_acute,
                ABF_Service_Category.admitted_nonacute,
                ABF_Service_Category.admitted_subacute]:
            A_rt = 0.39
    else:
        A_rt = 0
    return A_rt


def compute_dialysis_adjustment(
        abf_service_cat: ABF_Service_Category,
        bool_dialysis_flag: bool) -> float:
    # Context:
    # Admitted acute or admitted subacute patient with a specified ACHI
    # Eleventh Edition renal dialysis code who is **not** assigned to the
    # Australian Refined Diagnosis Related Groups
    # - (AR-DRG) L61Z Haemodialysis
    # or
    # - AR-DRG L68Z Peritoneal Dialysis
    #
    # Adjustment:
    # Admitted acute or admitted subacute patient: 28 per cent

    # set the default value, which will be changed if the adjustment conditions are met
    A_dia = 0.0
    if bool_dialysis_flag and abf_service_cat in [
            ABF_Service_Category.admitted_acute,
            ABF_Service_Category.admitted_subacute,
            ABF_Service_Category.admitted_nonacute]:

        A_dia = 0.28

    return A_dia


def compute_treatment_remoteness_adjustment(
        abf_service_cat: ABF_Service_Category,
        EST_Remoteness: Remoteness_Category_RA16) -> float:
    """
    Computes the treatment remoteness adjustment based on the establishment
    remoteness
    """
    # set the default value that will be modified if adjustment conditions
    # are met
    A_treat = 0.0

    # Case 1:
    # a person who receives care in a hospital which is within an area that
    # is classified as being remote
    if EST_Remoteness == Remoteness_Category_RA16.Remote:
        # Adjustment:
        # - Admitted acute, admitted subacute or non-admitted
        # patient: 7 per cent
        # - Emergency department or emergency service patient: 6per cent
        if abf_service_cat in [ABF_Service_Category.admitted_acute,
                               ABF_Service_Category.admitted_subacute,
                               ABF_Service_Category.admitted_nonacute,
                               ABF_Service_Category.nonadmitted]:
            A_treat = 0.07
        elif abf_service_cat in [
                ABF_Service_Category.emergency_services,
                ABF_Service_Category.emergency_department]:
            A_treat = 0.06

    # Case2: a person who receives care in a hospital which is within an
    # area that is classified as being very remote
    elif EST_Remoteness == Remoteness_Category_RA16.Very_Remote:
        # Adjustment:
        # - Admitted acute, admitted subacute or non-admitted
        # patient: 14 per cent
        # - Emergency department or emergency service patient: 6per cent
        if abf_service_cat in [ABF_Service_Category.admitted_acute,
                               ABF_Service_Category.admitted_subacute,
                               ABF_Service_Category.admitted_nonacute,
                               ABF_Service_Category.nonadmitted]:
            A_treat = 0.14

        elif abf_service_cat in [
                ABF_Service_Category.emergency_services,
                ABF_Service_Category.emergency_department]:
            A_treat = 0.06
    else:
        A_treat = 0.0

    return A_treat


def compute_ICU_adjustment(
        abf_service_cat: ABF_Service_Category,
        ar_drg_v10: str,
        ICU_hours_L3: float) -> float:
    """
    Computes the ICU adjustment.
    NOTE: **This incorporates the number of ICD L3 hours into the computation**
    """
    # Context:
    # The ABF
    # - is **not** represented by a newborn/neonate AR-DRG identified as ‘bundled
    # ICU’ in the tables of price weights (Appendix H);
    # - AND **is** in respect of a person who has spent time within a
    # specified ICU that is listed in Appendix D
    assert abf_service_cat == ABF_Service_Category.admitted_acute, "Only admitted acute service category is eligible for ICU adjustment"
    if (
            (not admitted_acute_helper.bool_is_icu_bundled(ar_drg_v10))
        and
            hosp_level3ICU_flag
    ):
        # Adjustment: 0.0440 NWAU(20) per hour spent by that person within
        # the specified ICU
        A_net_icu_adjustment = ICU_hours_L3 * 0.0440
    else:
        A_net_icu_adjustment = 0.0

    return A_net_icu_adjustment


def compute_private_patient_service_adjustment(
        abf_service_cat: ABF_Service_Category,
        bool_pat_private_flag: bool,
        ar_drg_v10_or_an_snap_v4: str) -> float:
    """
    Computes the Private patient service adjustment
    """
    # Context: The ABF is for an eligible admitted private patient.
    if abf_service_cat == ABF_Service_Category.admitted_acute:
        if bool_pat_private_flag:
            # Adjustment:
            # - Admitted acute patient: column headed private patient service
            # adjustment in the table of price weights at Appendix H
            ar_drg_v10 = ar_drg_v10_or_an_snap_v4
            A_pps = dal_admitted_acute.get_private_patient_service_adjustment(
                ar_drg_v10)
        else:
            A_pps = 0.0
    elif abf_service_cat in [
            ABF_Service_Category.admitted_nonacute,
            ABF_Service_Category.admitted_subacute]:
        if bool_pat_private_flag:
            # Adjustment:
            # - Admitted subacute or non-acute patient: refer to Appendix F for
            # applicable adjustment
            an_snap_v4 = ar_drg_v10_or_an_snap_v4
            A_pps = dal_admitted_subandnon_acute.get_private_patient_service_adjustment(
                an_snap_v4)
        else:
            A_pps = 0.0
    else:
        raise RuntimeError(
            "Only admitted service categories are eligible for private patient adjustment")

    return A_pps


def compute_private_patient_accommodation_adjustment(
        abf_service_cat: ABF_Service_Category,
        bool_pat_private_flag: bool,
        bool_same_day_flag: bool,
        hosp_state_val: Hosp_State_Category,
        full_LOS_days: int = 1
) -> float:
    """
    Computes the Private patient accommodation adjustment and makes a
    note of it to the list of adjustments applied.
    **Note**: this function already multiples the A_acc
    with the Length of stay
    """

    # Context: The ABF is for an eligible admitted private patient.
    if abf_service_cat in [
            ABF_Service_Category.admitted_acute,
            ABF_Service_Category.admitted_nonacute,
            ABF_Service_Category.admitted_subacute]:
        if bool_pat_private_flag:
            A_acc_los = dal_private_patient_adj.get_private_patient_accommodation_adjustment_perdiem(
                bool_same_day_flag, hosp_state_val)
            if not bool_same_day_flag:
                A_acc_los = A_acc_los * full_LOS_days
        else:
            A_acc_los = 0.0

    else:
        raise RuntimeError(
            "Only admitted (acute/subacute/nonacute) service categories are eligible for private patient accommodation adjustment")

    return A_acc_los


def compute_multidisciplinary_clinic_adj(
        abf_service_cat: ABF_Service_Category,
        bool_non_admitted_multi_hcp_flag: bool) -> float:
    if abf_service_cat == ABF_Service_Category.nonadmitted:
        if bool_non_admitted_multi_hcp_flag:
            A_nmc = 0.45
        else:
            A_nmc = 0.0
    else:
        raise RuntimeError(
            "Only non-admitted service categories are eligible for the MDC adjustment")

    return A_nmc


def compute_emergency_care_age_adjustment(
        abf_service_cat: ABF_Service_Category,
        patient_age_years: int) -> float:
    """Computes the emergency care age adjustment
    Context: in respect of an emergency department patient, with the rate of
    adjustment dependent on the person’s age.
    Adjustment: Emergency department patient who is aged:
    - 65 to 79 years: 13 per cent
    - Over 79 years: 19 per cent

    Arguments:
        abf_service_cat {ABF_Service_Category} -- [description]
        patient_age {int} -- [description]

    Returns:
        float -- emergency care age adjustment
    """
    if abf_service_cat in [
            ABF_Service_Category.emergency_department,
            ABF_Service_Category.emergency_services]:
        if 65 <= patient_age_years <= 79:
            A_eca = 0.13
        elif 79 < patient_age_years:
            A_eca = 0.19
        else:  # age criteria not met
            A_eca = 0.0

    else:
        raise RuntimeError(
            "Only emergency department/service categories are eligible \
                 for the emergency care age adjustment")

    return A_eca


def compute_HAC_adjustments(
        abf_service_cat: ABF_Service_Category,
        patient_age_years: int,
        hac_cat_list: List[HAC_Category],
        charlson_score: int,
        mdc_type: MDC_Type,
        bool_is_intervention: bool,
        sex_category: Sex_Category,
        bool_is_emergency_admission: bool,
        bool_ICU_hours: bool,
        bool_is_admission_transfer: bool,
        bool_foetal_distress_flag: bool,
        bool_instrument_use_flag: bool,
        bool_ppop_flag: bool,
        bool_prima_flag: bool) -> float:
    """
    Computes the HAC accommodation adjustments 
    """

    # Context:
    # For an admitted acute episode where one or more HAC is present. **If more than one
    # HAC is present, the largest of the HAC adjustments applies.**

    if not(abf_service_cat == ABF_Service_Category.admitted_acute):
        raise RuntimeError(
            "HAC adjustments are only for the `admitted acute` service category")

    # Adjustment:
    # Admitted acute episode with one or more HAC: refer to Appendix N for
    # applicable adjustments
    A_hac = compute_hac_adjustment_to_apply(
        age=patient_age_years,
        hac_cat_list=hac_cat_list,
        charlson_score=charlson_score,
        mdc_cat=mdc_type,
        bool_is_intervention=bool_is_intervention,
        sex_category=sex_category,
        bool_is_emergency_admission=bool_is_emergency_admission,
        bool_ICU_hours=bool_ICU_hours,
        bool_is_admission_transfer=bool_is_admission_transfer,
        bool_foetal_distress_flag=bool_foetal_distress_flag,
        bool_instrument_use_flag=bool_instrument_use_flag,
        bool_ppop_flag=bool_ppop_flag,
        bool_prima_flag=bool_prima_flag
    )
    return A_hac
