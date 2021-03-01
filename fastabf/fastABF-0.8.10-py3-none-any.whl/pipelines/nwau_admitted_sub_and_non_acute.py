import re as re
from typing import Dict, List

from dateutil import relativedelta

from fastabf import adjustment_mapper
from fastabf.adjustment_mapper import extract_dd_mm_yyyy
from fastabf.DAL import dal_admitted_subandnon_acute
from fastabf.datatypes import (HOSP_PAED_FLAG, ABF_Service_Category, Care_Type,
                               Indigenous_Status_Category,
                               Remoteness_Category_RA16, Sex_Category,
                               Stay_Category, global_NEP, hosp_level3ICU_flag,
                               hosp_state_constant)
from fastabf.Helpers import helper_remoteness_mappings as remotenessmapper


class Admitted_Subacute_Record:
    def __init__(
        self,
        Birth_Date: str,
        Admission_Date: str,
        Separation_Date: str,
        AN_SNAP_v4: str,

        # [METeOR id: 269976] True if admitted patient transferred from another hospital.

        # [METeOR id: 269986] True if admission occurred on an emergency basis
        patient_leave_days: float = 0,
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
            care_type: Care_Type = Care_Type.acute_care_admitted_care):

        self.__adjustments: Dict = dict()
        self.__abf_service_cat = ABF_Service_Category.admitted_acute
        self.__patient_leave_days = patient_leave_days
        self.__Pat_Postcode = Pat_Postcode
        self.__Pat_SA2 = Pat_SA2
        self.__Pat_Radiotherapy_Flag = Pat_Radiotherapy_Flag
        self.__Pat_Dialysis_Flag = Pat_Dialysis_Flag
        self.__Pat_private_Flag = Pat_private_Flag
        self.__Pat_Covid19_Flag = Pat_Covid19_Flag

        if EST_Remoteness_Cat is not Remoteness_Category_RA16.Unknown:
            self.__EST_Remoteness_Cat = EST_Remoteness_Cat
        else:
            raise ValueError("Invalid EST_Remoteness")

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
            # TODO: validate AN_SNAP_v4
            self.__AN_SNAP_v4 = AN_SNAP_v4
        except:
            raise ValueError("ANSNAPV4")

        if self.__patient_admission_date == self.__patient_separation_date:
            self.__bool_same_day_flag = True
        else:
            self.__bool_same_day_flag = False

        self.__base_los_norm = relativedelta.relativedelta(
            self.__patient_separation_date, self.__patient_admission_date
        ).normalized()

        self.__los_days = self.__get_full_los_days_minus_leavedays()

        # now compute the best estimate of the patients remoteness type
        remoteness_type = adjustment_mapper.estimate_remoteness_category(
            postcode_str=self.__Pat_Postcode,
            SA2=self.__Pat_SA2,
            establishment_remoteness=self.__EST_Remoteness_Cat)
        self.__computed_pat_remoteness_type = remoteness_type

        # now set the base NWAU (i.e. base price weight)
        self.__PW = self.__get_base_nwau()
        self.__abf_price = 0.0

        # TODO:assert that sep date >= admission date

    def __get_full_los_days_minus_leavedays(self) -> int:
        """Computes the non-ICU length of stay (LOS) in days **rounded down**
        to the closest 24hrs and **after removing patient leave days**
        Returns:
            [int] -- LOS in days
        """
        non_leave_los = self.__base_los_norm - (
            relativedelta.relativedelta(
                days=self.__patient_leave_days).normalized()
        )
        non_leave_los_norm = non_leave_los.normalized()
        return int(non_leave_los_norm.days + non_leave_los_norm.hours // 24)

    def __get_base_nwau(self):
        """Returns the base NWAU from the relevant tables.

        - Infer stay category
        - Lookup PW based on same day status.
        - Apply outlier adjustments if needed based on stay duration and
        perdiems

        Returns:
            [float] -- base NWAU with length of stay based adjustments
        """

        self.__stay_cat = dal_admitted_subandnon_acute.helper_get_stay_category(
            self.__AN_SNAP_v4, self.__bool_same_day_flag, self.__los_days
        )
        base_pw = dal_admitted_subandnon_acute.get_base_nwau(
            an_snap_v4=self.__AN_SNAP_v4,
            stay_cat=self.__stay_cat,
            los_days=self.__los_days)

        return base_pw

    def __step1_compute_pat_residential_remoteness_adj(self):
        """
        Computes the Patient residential remoteness area adjustment.
        Makes a note of it to the list of adjustments applied
        """
        # Gather variables for decision making
        A_res = adjustment_mapper.compute_patient_residential_remoteness_adj(
            remoteness_type=self.__computed_pat_remoteness_type,
            abf_service_cat=self.__abf_service_cat)

        self.__adjustments.update({"A_res": A_res})

    def __step2_compute_indigenous_adj(self):
        """
        Computes the Patient Indigenous  adjustment.
        Makes a note of it to the list of adjustments applied
        """
        A_ind = adjustment_mapper.compute_indigenous_adj(
            ind_stat=self.__Indigenous_Status,
            abf_service_cat=self.__abf_service_cat
        )
        self.__adjustments.update({"A_ind": A_ind})

    def __step3_compute_radiotherapy_adjustment(self):
        """
        Computes the radiotherapy adjustment.
        Makes a note of it to the list of adjustments applied
        """
        A_rt = adjustment_mapper.compute_radiotherapy_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_radiotherapy_flag=self.__Pat_Radiotherapy_Flag
        )
        self.__adjustments.update({"A_rt": A_rt})

    def __step4_compute_dialysis_adjustment(self):
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

    def __step5_treatment_remoteness_adjustment(self):
        """
        Computes the treatment remoteness adjustment and
        Makes a note of it to the list of adjustments applied
        """
        A_treat = adjustment_mapper.compute_treatment_remoteness_adjustment(
            abf_service_cat=self.__abf_service_cat,
            EST_Remoteness=self.__EST_Remoteness_Cat
        )
        self.__adjustments.update({"A_treat": A_treat})

    def __step6_Private_patient_service_adjustment(self):
        """
        Computes the Private patient service adjustment and makes a note of it to the list of
        adjustments applied
        """
        A_pps = adjustment_mapper.compute_private_patient_service_adjustment(
            abf_service_cat=self.__abf_service_cat,
            bool_pat_private_flag=self.__Pat_private_Flag,
            ar_drg_v10_or_an_snap_v4=self.__AN_SNAP_v4
        )

        self.__adjustments.update({"A_pps": A_pps})

    def __step7_Private_patient_accommodation_adjustment(self):
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
            full_LOS_days=self.__los_days
        )
        self.__adjustments.update({"A_acc_los": A_acc_los})

    def compute_all_adjustments(self) -> None:
        # __step through and compute all the adjustments required for this ABF type
        self.__step1_compute_pat_residential_remoteness_adj()
        self.__step2_compute_indigenous_adj()
        self.__step3_compute_radiotherapy_adjustment()
        self.__step4_compute_dialysis_adjustment()
        self.__step5_treatment_remoteness_adjustment()
        self.__step6_Private_patient_service_adjustment()
        self.__step7_Private_patient_accommodation_adjustment()

    def get_abf_price(self) -> float:
        """
        Performs the net adjustment for the NWAU admitted acute  and returns the price for
        the admitted acute ABF activity as per the formula


        __step 1: adjustedNWAU = 
        {
                [
                    PW x (1 + A_Ind + A_Res + A_RT + A_Dia) x (1 + A_Treat)
                ] 
                - 
                [
                    PW x APPS + LOS x AAcc
                ]
        }

        __step 2: price = adjustedNWAU * NEP

        Returns:
            float -- the ABF price for the admitted sub-acute activity
        """
        self.compute_all_adjustments()

        adjustment_dict = self.__adjustments
        A_res = adjustment_dict["A_res"]
        A_ind = adjustment_dict["A_ind"]
        A_rt = adjustment_dict["A_rt"]
        A_dia = adjustment_dict["A_dia"]
        A_treat = adjustment_dict["A_treat"]
        A_pps = adjustment_dict["A_pps"]
        A_acc_los = adjustment_dict["A_acc_los"]

        adjustedNWAU = (
            (
                self.__PW * (1+A_ind + A_res + A_rt + A_dia) * (1 + A_treat)
            )
            -
            (
                self.__PW * A_pps + A_acc_los

            )
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
