from enum import Enum
from typing import List


class Charlson_Type(Enum):
    Acute_Myocardial_Infarction = 0
    I21 = 0
    I22 = 0
    I252 = 0
    Congestive_Heart_Failure = 1
    I50 = 1
    Peripheral_Vascular_Disease = 2
    I71 = 2
    I790 = 2
    I739 = 2
    R02 = 2
    Z958 = 2
    Z959 = 2
    Cerebral_Vascular_Accident = 3
    I60 = 3
    I61 = 3
    I62 = 3
    I63 = 3
    I65 = 3
    I66 = 3
    G450 = 3
    G451 = 3
    G452 = 3
    G458 = 3
    G459 = 3
    G46 = 3
    I64 = 3
    G454 = 3
    I670 = 3
    I671 = 3
    I672 = 3
    I674 = 3
    I675 = 3
    I676 = 3
    I677 = 3
    I678 = 3
    I679 = 3
    I681 = 3
    I682 = 3
    I688 = 3
    I69 = 3
    Dementia = 4
    F00 = 4
    F01 = 4
    F02 = 4
    F051 = 4
    Pulmonary_Disease = 5
    J40 = 5
    J41 = 5
    J42 = 5
    J43 = 5
    J45 = 5
    J46 = 5
    J47 = 5
    J67 = 5
    J44 = 5
    J60 = 5
    J61 = 5
    J62 = 5
    J63 = 5
    J66 = 5
    J64 = 5
    J65 = 5
    Connective_Tissue_Disorder = 6
    M32 = 6
    M34 = 6
    M332 = 6
    M053 = 6
    M058 = 6
    M059 = 6
    M060 = 6
    M063 = 6
    M069 = 6
    M050 = 6
    M052 = 6
    M051 = 6
    M353 = 6
    Peptic_Ulcer = 7
    K25 = 7
    K26 = 7
    K27 = 7
    K28 = 7
    Liver_Disease = 8
    K702 = 8
    K703 = 8
    K73 = 8
    K717 = 8
    K740 = 8
    K742 = 8
    K746 = 8
    K743 = 8
    K744 = 8
    K745 = 8
    Diabetes = 9
    E109 = 9
    E119 = 9
    E139 = 9
    E149 = 9
    E101 = 9
    E111 = 9
    E131 = 9
    E141 = 9
    E105 = 9
    E115 = 9
    E135 = 9
    E145 = 9
    Diabetes_Complications = 10
    E102 = 10
    E112 = 10
    E132 = 10
    E142 = 10
    E103 = 10
    E113 = 10
    E133 = 10
    E143 = 10
    E104 = 10
    E114 = 10
    E134 = 10
    E144 = 10
    Paraplegia = 11
    G81 = 11
    G041 = 11
    G820 = 11
    G821 = 11
    G822 = 11
    Renal_Disease = 12
    N03 = 12
    N052 = 12
    N053 = 12
    N054 = 12
    N055 = 12
    N056 = 12
    N072 = 12
    N073 = 12
    N074 = 12
    N01 = 12
    N18 = 12
    N19 = 12
    N25 = 12
    Cancer = 13
    C0 = 13
    C1 = 13
    C2 = 13
    C3 = 13
    C40 = 13
    C41 = 13
    C43 = 13
    C45 = 13
    C46 = 13
    C47 = 13
    C48 = 13
    C49 = 13
    C5 = 13
    C6 = 13
    C70 = 13
    C71 = 13
    C72 = 13
    C73 = 13
    C74 = 13
    C75 = 13
    C76 = 13
    C81 = 13
    C82 = 13
    C83 = 13
    C84 = 13
    C85 = 13
    C883 = 13
    C887 = 13
    C889 = 13
    C900 = 13
    C901 = 13
    C91 = 13
    C92 = 13
    C93 = 13
    C940 = 13
    C941 = 13
    C942 = 13
    C943 = 13
    C9451 = 13
    C947 = 13
    C95 = 13
    C96 = 13
    C80 = 13
    Metastatic_Cancer = 14
    C77 = 14
    C78 = 14
    C79 = 14
    Severe_Liver_Cancer = 15
    K729 = 15
    K766 = 15
    K767 = 15
    K721 = 15
    HIV = 16
    B20 = 16
    B21 = 16
    B22 = 16
    B23 = 16
    B24 = 16


map_charlson_score_type_to_val = {
    "Acute_Myocardial_Infarction": 2,
    "Congestive_Heart_Failure": 1,
    "Peripheral_Vascular_Disease": 1,
    "Cerebral_Vascular_Accident": 1,
    "Dementia": 1,
    "Pulmonary_Disease": 1,
    "Connective_Tissue_Disorder": 1,
    "Peptic_Ulcer": 1,
    "Liver_Disease": 1,
    "Diabetes": 1,
    "Diabetes_Complications": 2,
    "Paraplegia": 2,
    "Renal_Disease": 2,
    "Cancer": 2,
    "Metastatic_Cancer": 2,
    "Severe_Liver_Cancer": 3,
    "HIV": 6,
}


def _alt_compute_charlson_score_for_ICD10AM_list(icd10amlist: List[str]) -> int:
    list_of_charlson_score_compatible_conditions = []
    for icd10amitem in icd10amlist:
        # the codes used in the charlson score computation has 3 or 4 digits hence
        # we remove the decimal point and then try both 3 and 4 digits
        optionstocheck = icd10amlist.replace(".", "")
        set_to_check = set(optionstocheck[0:3], optionstocheck[0:4])
        for icdoption in set_to_check:
            try:
                charlson_class = Charlson_Type[icdoption]

                list_of_charlson_score_compatible_conditions.append(
                    charlson_class)
            # if the value is not a Charlson compatible condition then move on
            # to the next value
            except:
                pass

    set_of_type_of_charlson_score_conditions = set(
        list_of_charlson_score_compatible_conditions
    )
    charlson_weights = [
        map_charlson_score_type_to_val.get(_, 0)
        for _ in set_of_type_of_charlson_score_conditions
    ]
    charlson_score = min(sum(charlson_weights), 16)
    return charlson_score


def compute_charlson_score_for_ICD10AM_list(icd10amlist: List[str]) -> int:
    list_of_charlson_score_compatible_conditions = []
    for icd10amitem in icd10amlist:
        # the codes used in the charlson score computation has 2 or 3 digits hence
        # we remove the decimal point and then try both 2 and 3 digits
        icdoption = icd10amitem.replace(".", "")
        try:
            charlson_class = Charlson_Type[icdoption]

            list_of_charlson_score_compatible_conditions.append(charlson_class)
        # if the value is not in the list of conditions for the Charlson index computation
        # then move on to the next value
        except:
            pass

    # count each category only once - by using a set to remove more than 1 occurrance
    set_of_type_of_charlson_score_conditions = set(
        list_of_charlson_score_compatible_conditions
    )

    # now compute the weights for the classes that occur
    charlson_weights = [
        map_charlson_score_type_to_val.get(_.name, 0)
        for _ in set_of_type_of_charlson_score_conditions
    ]
    # set the upper bound at 16
    charlson_score = min(sum(charlson_weights), 16)
    return charlson_score


if __name__ == "__main__":
    assert compute_charlson_score_for_ICD10AM_list(["C80", ""]) == 2
