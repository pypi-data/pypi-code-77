import re as re
from typing import Dict, List

from dateutil import relativedelta

from fastabf import adjustment_mapper
from fastabf.adjustment_mapper import extract_dd_mm_yyyy
from fastabf.DAL import dal_nonadmitted
from fastabf.datatypes import (HOSP_PAED_FLAG, ABF_Service_Category, Care_Type,
                               Indigenous_Status_Category,
                               Remoteness_Category_RA16, Sex_Category,
                               Stay_Category, global_NEP, hosp_level3ICU_flag,
                               hosp_state_constant)
from fastabf.Helpers import helper_remoteness_mappings as remotenessmapper


class Nonadmitted_Record:
    def __init__(
        self,
        Birth_Date: str,
        Event_Service_Date: str,
        Tier2_CV5: str,
        patient_leave_days: float = 0,
        Pat_Postcode: str = "",  # Format PCNNNN, METeOR id: 429894
        Pat_SA2: int = 0,  # NNNNNNNNN (9 digit), METeOR id: 469909
        # Establishment's Remoteness Category
        EST_Remoteness_Cat: Remoteness_Category_RA16 = Remoteness_Category_RA16.Unknown,
        Indigenous_Status: Indigenous_Status_Category = \
            Indigenous_Status_Category.Unknown_or_not_stated,
        Multiple_Healthcare_Provider_Indicator: bool = False,

        Pat_Covid19_Flag: bool = False,
            care_type: Care_Type = Care_Type.acute_care_admitted_care):

        self.__adjustments: Dict = dict()
        self.__abf_service_cat = ABF_Service_Category.admitted_acute
        self.__Pat_Postcode = Pat_Postcode
        self.__Pat_SA2 = Pat_SA2
        self.__Pat_Covid19_Flag = Pat_Covid19_Flag

        if EST_Remoteness_Cat is not Remoteness_Category_RA16.Unknown:
            self.__EST_Remoteness_Cat = EST_Remoteness_Cat
        else:
            raise ValueError("Invalid EST_Remoteness")

        self.__Indigenous_Status = Indigenous_Status
        self.__Multiple_Healthcare_Provider_Indicator = Multiple_Healthcare_Provider_Indicator
        try:
            # parse Birth_Date of patient
            self.__patient_birth_date = extract_dd_mm_yyyy(
                Birth_Date)
        except Exception as E1:
            raise ValueError(f"invalid birth_Date: {E1}")

        try:
            # parse Admission_Date of patient
            self.__patient_event_service_date = extract_dd_mm_yyyy(
                Event_Service_Date)
        except Exception as E1:
            raise ValueError(f"Invalid Admission_Date {E1}")

        self.__patient_age = relativedelta.relativedelta(
            self.__patient_event_service_date, self.__patient_birth_date
        ).normalized()

        try:
            # TODO: validate Tier2_CV5
            self.__Tier2_CV5 = Tier2_CV5
        except:
            raise ValueError("Tier2CV5")

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

        base_pw = dal_nonadmitted.get_base_nwau(tier2_cv5=self.__Tier2_CV5)

        return base_pw

    def __step1_compute_paed_adj(self):
        """
        Computes the Paediatric adjustment. Makes a note of it to the list of
        adjustments applied
        """
        A_paed = adjustment_mapper.compute_paediatric_adj(self.__Tier2_CV5,
                                                          self.__patient_age,
                                                          self.__abf_service_cat)
        self.__adjustments.update({"A_paed": A_paed})

    def __step2_compute_pat_residential_remoteness_adj(self):
        """
        Computes the Patient residential remoteness area adjustment.
        Makes a note of it to the list of adjustments applied
        """
        # Gather variables for decision making
        A_res = adjustment_mapper.compute_patient_residential_remoteness_adj(
            remoteness_type=self.__computed_pat_remoteness_type,
            abf_service_cat=self.__abf_service_cat)

        self.__adjustments.update({"A_res": A_res})

    def __step3_compute_indigenous_adj(self):
        """
        Computes the Patient Indigenous  adjustment.
        Makes a note of it to the list of adjustments applied
        """
        A_ind = adjustment_mapper.compute_indigenous_adj(
            ind_stat=self.__Indigenous_Status,
            abf_service_cat=self.__abf_service_cat
        )
        self.__adjustments.update({"A_ind": A_ind})

    def __step4_treatment_remoteness_adjustment(self):
        """
        Computes the treatment remoteness adjustment and
        Makes a note of it to the list of adjustments applied
        """
        A_treat = adjustment_mapper.compute_treatment_remoteness_adjustment(
            abf_service_cat=self.__abf_service_cat,
            EST_Remoteness=self.__EST_Remoteness_Cat
        )
        self.__adjustments.update({"A_treat": A_treat})

    def __step5_multidisciplinary_clinic_adjustment(self):
        A_nmc = adjustment_mapper.compute_multidisciplinary_clinic_adj(
            abf_service_cat=ABF_Service_Category.nonadmitted,
            bool_non_admitted_multi_hcp_flag=self.__Multiple_Healthcare_Provider_Indicator
        )
        self.__adjustments.update({"A_nmc": A_nmc})

    def compute_all_adjustments(self) -> None:
        # Step through and compute all the adjustments required for this ABF type
        self.__step1_compute_paed_adj()
        self.__step2_compute_pat_residential_remoteness_adj()
        self.__step3_compute_indigenous_adj()
        self.__step4_treatment_remoteness_adjustment()
        self.__step5_multidisciplinary_clinic_adjustment()

    def get_abf_price(self) -> float:
        """
        Performs the net adjustment for the NWAU admitted acute  and returns the price for
        the admitted acute ABF activity as per the formula
        __step 1: adjustedNWAU = 
            {
                [
                    PW x A_Paed x (1 + A_Ind + A_Res+ A_NMC) x (1 + ATreat)

                ]
            }

        __step 2: price = adjustedNWAU * NEP

        Returns:
            float -- the ABF price for the non-admitted activity
        """
        self.compute_all_adjustments()

        adjustment_dict = self.__adjustments
        A_paed = adjustment_dict["A_paed"]
        A_res = adjustment_dict["A_res"]
        A_ind = adjustment_dict["A_ind"]
        A_treat = adjustment_dict["A_treat"]
        A_nmc = adjustment_dict["A_nmc"]

        adjustedNWAU = (
            (
                self.__PW * A_paed*(1+A_ind + A_res + A_nmc) * (1 + A_treat)
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
