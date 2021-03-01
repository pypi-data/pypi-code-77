import re as re
from typing import Dict, List

from dateutil import relativedelta

from fastabf import adjustment_mapper
from fastabf.adjustment_mapper import extract_dd_mm_yyyy
from fastabf.DAL import admitted_acute_helper, dal_admitted_acute
from fastabf.datatypes import (HOSP_PAED_FLAG, ABF_Service_Category, Care_Type,
                               Indigenous_Status_Category,
                               Remoteness_Category_RA16, Sex_Category,
                               Stay_Category, global_NEP, hosp_level3ICU_flag,
                               hosp_state_constant)
from fastabf.HACpackage import hac_processor
from fastabf.HACpackage.hac_processor import HAC_Category, MDC_Type
from fastabf.Helpers import helper_remoteness_mappings as remotenessmapper


class Admitted_Acute_Record:
    def __init__(
        self,
        Birth_Date: str,
        Admission_Date: str,
        Separation_Date: str,
        AR_DRG_v10: str,

        # [METeOR id: 269976] True if admitted patient transferred from another hospital.
        bool_transfer_status: bool,
        sex: int,  # [METeOR id: 635126]

        # [METeOR id: 269986] True if admission occurred on an emergency basis
        bool_is_emergency_admission: bool,
        bool_foetal_distress_flag: bool,
        bool_instrument_use_flag: bool,
        bool_ppop_flag: bool,
        bool_prima_flag: bool,
        HAC1: bool,
        HAC2: bool,
        HAC3: bool,
        HAC4: bool,
        HAC6: bool,
        HAC7: bool,
        HAC8: bool,
        HAC9: bool,
        HAC10: bool,
        HAC11: bool,
        HAC12: bool,
        HAC13: bool,
        HAC14: bool,
        HAC15p2: bool,
        Charlson_Score: int,
        patient_leave_days: float = 0,
        ICU_hours_L3: float = -1,
        ICU_hours_other: float = 0,
        Psych_Days: float = 0,  # METeOR id: 552375
        Pat_Postcode: str = "",  # Format PCNNNN, METeOR id: 429894
        Pat_SA2: int = 0,  # NNNNNNNNN (9 digit), METeOR id: 469909
        # Establishment's Remoteness Category
        EST_Remoteness_Cat: Remoteness_Category_RA16 = Remoteness_Category_RA16.Unknown,
        Indigenous_Status: Indigenous_Status_Category = \
            Indigenous_Status_Category.Unknown_or_not_stated,

        Pat_Radiotherapy_Flag: bool = False,
        #  Set to True if the patient has any of the ACHI 11th Edition codes
        #  listed in Appendices B and C of the `national efficient
        #  price determination 2020-21` document for radiotherapy relevant codes
        #  else False
        Pat_Dialysis_Flag: bool = False,
        #  Set to True if the patient has any of the ACHI 11th Edition codes
        #  listed in Appendices B and C of the `national efficient
        #  price determination 2020-21` document for dialysis relevant codes
        #  else False

        # Set to True if the patient is an eligible private patient
        Pat_private_Flag: bool = False,

        Pat_Covid19_Flag: bool = False,

        care_type: Care_Type = Care_Type.acute_care_admitted_care
    ):
        self.__adjustments: Dict = dict()
        self.__abf_service_cat = ABF_Service_Category.admitted_acute
        self.__patient_leave_days = patient_leave_days
        self.__bool_transfer_status = bool_transfer_status
        # If level 3 hospital, the level 3 icu hours can not be kept empty
        if ICU_hours_L3 < 0 and hosp_level3ICU_flag:
            raise ValueError(
                "ICU_hours_L3 must be supplied for Hospitals with Level 3 ICU")
        else:
            self.__ICU_hours_L3 = ICU_hours_L3

        self.__ICU_hours_other = ICU_hours_other
        self.__Psych_Days = Psych_Days
        self.__Pat_Postcode = Pat_Postcode
        self.__Pat_SA2 = Pat_SA2
        self.__Pat_Radiotherapy_Flag = Pat_Radiotherapy_Flag
        self.__Pat_Dialysis_Flag = Pat_Dialysis_Flag
        self.__Pat_private_Flag = Pat_private_Flag
        self.__Pat_Covid19_Flag = Pat_Covid19_Flag
        self.__charlson_score = Charlson_Score
        hac_flag_list = [HAC1, HAC2, HAC3, HAC4, HAC6, HAC7,
                         HAC8, HAC9, HAC10, HAC11, HAC12, HAC13, HAC14, HAC15p2]

        hac_cat_list = list((hac_cat for hac_cat, hac_flag in zip(
            HAC_Category, hac_flag_list) if hac_flag))
        self.__hac_cat_list = hac_cat_list

        if EST_Remoteness_Cat is not Remoteness_Category_RA16.Unknown:
            self.__EST_Remoteness_Cat = EST_Remoteness_Cat
        else:
            raise ValueError("Invalid EST_Remoteness")

        self.__bool_is_emergency_admission = bool_is_emergency_admission
        self.__bool_foetal_distress_flag = bool_foetal_distress_flag
        self.__bool_instrument_use_flag = bool_instrument_use_flag
        self.__bool_ppop_flag = bool_ppop_flag
        self.__bool_prima_flag = bool_prima_flag
        self.__sex_category = Sex_Category(sex)

        self.__Indigenous_Status = Indigenous_Status
        try:
            # parse Birth_Date of patient
            self.__patient_birth_date = extract_dd_mm_yyyy(
                Birth_Date)
        except Exception as E1:
            raise ValueError(f"invalid birth_Date: {E1}")

        try:
            # parse Admission_Date of patient
            self.__patient_admission_date = extract_dd_mm_yyyy(
                Admission_Date)
        except Exception as E1:
            raise ValueError(f"Invalid Admission_Date {E1}")

        try:
            # parse Separation_Date
            self.__patient_separation_date = extract_dd_mm_yyyy(
                Separation_Date)
        except Exception as E1:
            raise ValueError(f"Invalid Separation_Date: {E1}")

        self.__patient_age = relativedelta.relativedelta(
            self.__patient_admission_date, self.__patient_birth_date
        ).normalized()

        try:
            # TODO: validate AR_DRG_v10
            self.__AR_DRG_v10 = AR_DRG_v10
        except:
            raise ValueError("ARDRG10")

        self.__mdc_type = dal_admitted_acute.get_mdc_for_ardrgv10(
            self.__AR_DRG_v10)

        if self.__patient_admission_date == self.__patient_separation_date:
            self.__bool_same_day_flag = True
        else:
            self.__bool_same_day_flag = False

        self.__base_los_norm = relativedelta.relativedelta(
            self.__patient_separation_date, self.__patient_admission_date
        ).normalized()

        self.__non_icu_los = self.__get_non_icu_los_days()

        # now compute the best estimate of the patients remoteness type
        remoteness_type = adjustment_mapper.estimate_remoteness_category(
            postcode_str=self.__Pat_Postcode, SA2=self.__Pat_SA2, establishment_remoteness=self.__EST_Remoteness_Cat)
        self.__computed_pat_remoteness_type = remoteness_type

        # now set the base NWAU (i.e. base price weight)
        self.__PW = self.__get_base_nwau()
        self.__abf_price = 0.0

        # TODO:assert that sep date >= admission date

    def __get_full_los_days(self) -> int:
        """
        Computes the length of stay (LOS) in days **rounded down** to the
        closest 24hrs (note this includes ICU + non-ICU + leave days)
        Returns:
            [int] -- LOS_days
        """
        return int(self.__base_los_norm.days + self.__base_los_norm.hours // 24)

    def __get_non_icu_los_days(self) -> int:
        """Computes the non-ICU length of stay (LOS) in days **rounded down**
        to the closest 24hrs and **after removing patient leave days**
        Returns:
            [int] -- LOS in days
        """
        non_icu_los = self.__base_los_norm - (
            relativedelta.relativedelta(hours=self.__ICU_hours_other)
            + relativedelta.relativedelta(hours=self.__ICU_hours_L3)
            + relativedelta.relativedelta(days=self.__patient_leave_days)
        )
        non_icu_los_norm = non_icu_los.normalized()
        return int(non_icu_los_norm.days + non_icu_los_norm.hours // 24)

    def __get_base_nwau(self):
        """Returns the base NWAU from the relevant tables.

        - Infer stay category
        - Lookup PW based on same day status.
        - Apply outlier adjustments if needed based on stay duration and
        perdiems

        Returns:
            [float] -- base NWAU with length of stay based adjustments
        """
        self.__stay_cat = admitted_acute_helper.helper_get_stay_category(
            self.__AR_DRG_v10, self.__bool_same_day_flag, self.__non_icu_los
        )
        base_pw = admitted_acute_helper.get_base_nwau(
            ar_drg_v10=self.__AR_DRG_v10,
            stay_cat=self.__stay_cat,
            non_icu_los_days=self.__non_icu_los)
        return base_pw

    def __step1_compute_paed_adj(self):
        """
        Computes the Paediatric adjustment. Makes a note of it to the list of
        adjustments applied
        """
        A_paed = adjustment_mapper.compute_paediatric_adj(self.__AR_DRG_v10,
                                                          self.__patient_age,
                                                          self.__abf_service_cat)
        self.__adjustments.update({"A_paed": A_paed})

    def __step2_compute_psychiatric_age_adj(self):
        """
        Computes the psychiatric age adjustment and applies it.
        Makes a note of it to the list of adjustments applied
        """
        A_spa = adjustment_mapper.compute_psychiatric_age_adj(
            patient_age=self.__patient_age,
            mdc_type=self.__mdc_type,
            psych_days=self.__Psych_Days,
            abf_service_cat=self.__abf_service_cat)
        self.__adjustments.update({"A_spa": A_spa})

    def __step3_compute_pat_residential_remoteness_adj(self):
        """
        Computes the Patient residential remoteness area adjustment.
        Makes a note of it to the list of adjustments applied
        """
        # Gather variables for decision making
        A_res = adjustment_mapper.compute_patient_residential_remoteness_adj(
            remoteness_type=self.__computed_pat_remoteness_type,
            abf_service_cat=self.__abf_service_cat)

        self.__adjustments.update({"A_res": A_res})

    def __step4_compute_indigenous_adj(self):
        """
        Computes the Patient Indigenous  adjustment.
        Makes a note of it to the list of adjustments applied
        """
        A_ind = adjustment_mapper.compute_indigenous_adj(
            ind_stat=self.__Indigenous_Status,
            abf_service_cat=self.__abf_service_cat
        )
        self.__adjustments.update({"A_ind": A_ind})

    def __step5_compute_radiotherapy_adjustment(self):
        """
        Computes the radiotherapy adjustment.
        Makes a note of it to the list of adjustments applied
        """
        A_rt = adjustment_mapper.compute_radiotherapy_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_radiotherapy_flag=self.__Pat_Radiotherapy_Flag
        )
        self.__adjustments.update({"A_rt": A_rt})

    def __step6_compute_dialysis_adjustment(self):
        """
        Computes the dialysis adjustment
        Makes a note of it to the list of adjustments applied
        """
        # Context:
        # Admitted acute or admitted subacute patient with a specified ACHI
        # Eleventh Edition renal dialysis code
        A_dia = adjustment_mapper.compute_dialysis_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_dialysis_flag=self.__Pat_Dialysis_Flag)
        self.__adjustments.update({"A_dia": A_dia})

    def __step7_treatment_remoteness_adjustment(self):
        """
        Computes the treatment remoteness adjustment and
        Makes a note of it to the list of adjustments applied
        """
        A_treat = adjustment_mapper.compute_treatment_remoteness_adjustment(
            abf_service_cat=self.__abf_service_cat,
            EST_Remoteness=self.__EST_Remoteness_Cat
        )
        self.__adjustments.update({"A_treat": A_treat})

    def __step8_ICU_adjustment(self):
        """
        Computes the ICU adjustment and makes a note of it to the list of
        adjustments applied
        """
        A_net_icu_adjustment = adjustment_mapper.compute_ICU_adjustment(
            abf_service_cat=self.__abf_service_cat,
            ar_drg_v10=self.__AR_DRG_v10,
            ICU_hours_L3=self.__ICU_hours_L3
        )
        self.__adjustments.update(
            {"A_net_icu_adjustment": A_net_icu_adjustment})

    def __step9_Private_patient_service_adjustment(self):
        """
        Computes the Private patient service adjustment and makes a note of it to the list of
        adjustments applied
        """
        A_pps = adjustment_mapper.compute_private_patient_service_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_pat_private_flag=self.__Pat_private_Flag,
            ar_drg_v10_or_an_snap_v4=self.__AR_DRG_v10
        )

        self.__adjustments.update({"A_pps": A_pps})

    def __step10_Private_patient_accommodation_adjustment(self):
        """
        Computes the Private patient accommodation adjustment and makes a
        note of it to the list of adjustments applied.
        **Note**: this function already multiples the A_acc
        with the Length of stay
        """
        A_acc_los = adjustment_mapper.compute_private_patient_accommodation_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_pat_private_flag=self.__Pat_private_Flag,
            bool_same_day_flag=self.__bool_same_day_flag,
            hosp_state_val=hosp_state_constant,
            full_LOS_days=self.__non_icu_los
        )
        self.__adjustments.update({"A_acc_los": A_acc_los})

    def __step11_multidisciplinary_clinic_adjustment(self):
        pass

    def __step12_emergency_care_age_adjustment(self):
        pass

    def __step13_HAC_adjustments(self) -> None:
        """
        Computes the HAC accommodation adjustments and makes a
        note of it to the list of adjustments applied.
        """

        # Context:
        # For an admitted acute episode where one or more HAC is present. **If more than one
        # HAC is present, the largest of the HAC adjustments applies.**

        # Adjustment:
        # Admitted acute episode with one or more HAC: refer to Appendix N for
        # applicable adjustments
        A_hac = hac_processor.compute_adjustment_to_apply(
            age=self.__patient_age.years,
            hac_cat_list=self.__hac_cat_list,
            charlson_score=self.__charlson_score,
            mdc_cat=self.__mdc_type,
            bool_is_intervention=admitted_acute_helper.bool_is_drg_intervention(
                self.__AR_DRG_v10),
            sex_category=self.__sex_category,
            bool_is_emergency_admission=self.__bool_is_emergency_admission,
            bool_ICU_hours=(self.__ICU_hours_L3 >
                            0 or self.__ICU_hours_other > 0),
            bool_is_admission_transfer=self.__bool_transfer_status,
            bool_foetal_distress_flag=self.__bool_foetal_distress_flag,
            bool_instrument_use_flag=self.__bool_instrument_use_flag,
            bool_ppop_flag=self.__bool_ppop_flag,
            bool_prima_flag=self.__bool_prima_flag
        )
        self.__adjustments.update({"A_hac": A_hac})

    def compute_all_adjustments(self) -> None:
        # __step through and compute all the adjustments required for this ABF type
        self.__step1_compute_paed_adj()
        self.__step2_compute_psychiatric_age_adj()
        self.__step3_compute_pat_residential_remoteness_adj()
        self.__step4_compute_indigenous_adj()
        self.__step5_compute_radiotherapy_adjustment()
        self.__step6_compute_dialysis_adjustment()
        self.__step7_treatment_remoteness_adjustment()
        self.__step8_ICU_adjustment()
        self.__step9_Private_patient_service_adjustment()
        self.__step10_Private_patient_accommodation_adjustment()
        self.__step11_multidisciplinary_clinic_adjustment()
        self.__step12_emergency_care_age_adjustment()
        self.__step13_HAC_adjustments()

    def get_abf_price(self) -> float:
        """
        Performs the net adjustment for the NWAU admitted acute  and returns the price for
        the admitted acute ABF activity as per the formula
        __step 1: adjustedNWAU = {
            [
                PW x A_Paed x(1 + A_SPA + A_Ind + A_Res + A_RT + A_Dia) x(1 + A_Treat)
                + (A_ICU x ICU hours)
            ]
            -
            [
                (PW + AICU x ICU hours) x A_PPS + LOS x AAcc
            ]
            - PW x AHAC
            }
        __step 2: price = adjustedNWAU * NEP

        Returns:
            float -- the ABF price for the admitted acute activity
        """
        self.compute_all_adjustments()
        adjustment_dict = self.__adjustments
        A_paed = adjustment_dict["A_paed"]
        A_spa = adjustment_dict["A_spa"]
        A_res = adjustment_dict["A_res"]
        A_ind = adjustment_dict["A_ind"]
        A_rt = adjustment_dict["A_rt"]
        A_dia = adjustment_dict["A_dia"]
        A_treat = adjustment_dict["A_treat"]
        A_net_icu_adjustment = adjustment_dict["A_net_icu_adjustment"]
        A_pps = adjustment_dict["A_pps"]
        A_acc_los = adjustment_dict["A_acc_los"]
        A_hac = adjustment_dict["A_hac"]

        adjustedNWAU = (
            (
                self.__PW * A_paed * (1+A_spa + A_ind + A_res +
                                      A_rt + A_dia) * (1+A_treat)
                + A_net_icu_adjustment
            )
            -
            (
                (self.__PW + A_net_icu_adjustment) * A_pps + A_acc_los

            )
            -
            (self.__PW * A_hac)  # base price weight * HAC adjustment factor
        )

        # now we clip the adjusted NWAU to 0 (in case it is negative)
        adjustedNWAUpostfloor = max(0, adjustedNWAU)
        self.__adjustednwau = adjustedNWAU
        self.__adjustednwaupostfloor = adjustedNWAUpostfloor
        price = adjustedNWAUpostfloor*global_NEP
        self.__abf_price = price
        return price

    def DEBUG_get_adjustments(self) -> Dict:
        # useful for debugging
        return {
            "pw": self.__PW,
            "adjustment_steps": self.__adjustments,
            "adjustednwau": self.__adjustednwau,
            "adjustednwau_postfloor": self.__adjustednwaupostfloor,
            "abfprice": self.__abf_price
        }


if __name__ == "__main__":
    pass
