import re as re
from typing import Dict, List

from dateutil import relativedelta

from fastabf import adjustment_mapper
from fastabf.adjustment_mapper import extract_dd_mm_yyyy
from fastabf.DAL import dal_emergency
from fastabf.datatypes import (HOSP_PAED_FLAG, ABF_Service_Category, Care_Type,
                               Indigenous_Status_Category,
                               Remoteness_Category_RA16, Sex_Category,
                               Stay_Category, global_NEP, hosp_level3ICU_flag,
                               hosp_state_constant)
from fastabf.Helpers import helper_remoteness_mappings as remotenessmapper


class Emergency_Record:
    def __init__(
        self,
        Birth_Date: str,
        Admission_Date: str,
        URG_1p4_or_UDG_v1p3: int,
        Emergency_Care_Level: str,
        Pat_Postcode: str = "",  # Format PCNNNN, METeOR id: 429894
        Pat_SA2: int = 0,  # NNNNNNNNN (9 digit), METeOR id: 469909
        # Establishment's Remoteness Category
        EST_Remoteness_Cat: Remoteness_Category_RA16 = Remoteness_Category_RA16.Unknown,
        Indigenous_Status: Indigenous_Status_Category = \
            Indigenous_Status_Category.Unknown_or_not_stated,

        Pat_Covid19_Flag: bool = False,
            care_type: Care_Type = Care_Type.acute_care_admitted_care):

        self.__adjustments: Dict = dict()

        self.__abf_service_cat = self.__emergency_level_to_abf_mapper(
            Emergency_Care_Level)
        self.__Pat_Postcode = Pat_Postcode
        self.__Pat_SA2 = Pat_SA2
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

        self.__patient_age = relativedelta.relativedelta(
            self.__patient_admission_date, self.__patient_birth_date
        ).normalized()

        try:
            # TODO: validate URG_1p4_UDG_v1p3
            self.__urg_v1p4_or_udg_v1p3 = int(URG_1p4_or_UDG_v1p3)
        except:
            raise ValueError("invalid URG_UDG")

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

    def __get_base_nwau(self):
        """Returns the base NWAU from the relevant tables.

        - Infer stay category
        - Lookup PW based on same day status.
        - Apply outlier adjustments if needed based on stay duration and
        perdiems

        Returns:
            [float] -- base NWAU with length of stay based adjustments
        """

        base_pw = dal_emergency.get_base_bw_emergency(
            abf_service_cat=self.__abf_service_cat,
            urg_v1p4_or_udg_v1p3=self.__urg_v1p4_or_udg_v1p3
        )

        return base_pw

    def __emergency_level_to_abf_mapper(self, x: str) -> ABF_Service_Category:
        if x in ("1", "2", "3A"):
            return ABF_Service_Category.emergency_services
        elif x in ("3B", "4", "5", "6"):
            return ABF_Service_Category.emergency_department
        else:
            raise ValueError('unexpected value for emergency level')

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

    def __step3_treatment_remoteness_adjustment(self):
        """
        Computes the treatment remoteness adjustment and
        Makes a note of it to the list of adjustments applied
        """
        A_treat = adjustment_mapper.compute_treatment_remoteness_adjustment(
            abf_service_cat=self.__abf_service_cat,
            EST_Remoteness=self.__EST_Remoteness_Cat
        )
        self.__adjustments.update({"A_treat": A_treat})

    def __step4_emergency_care_age_adjustment(self):
        A_eca = adjustment_mapper.compute_emergency_care_age_adjustment(
            abf_service_cat=self.__abf_service_cat,
            patient_age_years=self.__patient_age.years
        )

        self.__adjustments.update({"A_eca": A_eca})

    def compute_all_adjustments(self) -> None:
        # __step through and compute all the adjustments required for this ABF type
        self.__step1_compute_pat_residential_remoteness_adj()
        self.__step2_compute_indigenous_adj()
        self.__step3_treatment_remoteness_adjustment()
        self.__step4_emergency_care_age_adjustment()

    def get_abf_price(self) -> float:
        """
        Performs the net adjustment for the NWAU admitted acute  and returns the price for
        the admitted acute ABF activity as per the formula


        __step 1: adjustedNWAU = 

        {
            [
                PW x (1 + A_Ind + A_Res + A_ECA) x (1 + ATreat)

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
        A_treat = adjustment_dict["A_treat"]
        A_eca = adjustment_dict["A_eca"]

        adjustedNWAU = (
            self.__PW * (1+A_ind + A_res + A_eca) * (1 + A_treat)
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
