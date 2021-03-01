import os
from enum import Enum


class Sex_Category(Enum):
    """
    # METeOR id: 635126  

    """
    Male = 1
    Female = 2
    Other = 3
    Missing = 9

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class MDC_Type(Enum):
    """
    This class describes the various MDC types
    """
    diseases_and_disorders_of_the_nervous_system = 1
    diseases_and_disorders_of_the_eye = 2
    diseases_and_disorders_of_the_ear_nose_mouth_and_throat = 3
    diseases_and_disorders_of_the_respiratory_system = 4
    diseases_and_disorders_of_the_circulatory_system = 5
    diseases_and_disorders_of_the_digestive_system = 6
    diseases_and_disorders_of_the_hepatobiliary_system_and_pancreas = 7
    diseases_and_disorders_of_the_musculoskeletal_system_and_connective_tissue = 8
    diseases_and_disorders_of_the_skin_subcutaneous_tissue_and_breast = 9
    endocrine_nutritional_and_metabolic_diseases_and_disorders = 10
    diseases_and_disorders_of_the_kidney_and_urinary_tract = 11
    diseases_and_disorders_of_the_male_reproductive_system = 12
    diseases_and_disorders_of_the_female_reproductive_system = 13
    pregnancy_childbirth_and_the_puerperium = 14
    newborns_and_other_neonates = 15
    diseases_and_disorders_of_blood_blood_forming_organs_immunological_disorders = 16
    neoplastic_disorders = 17
    infectious_and_parasitic_diseases = 18
    mental_diseases_and_disorders = 19
    alc_drug_use_and_alc_induced_organic_mental_disorders = 20
    injuries_poisonings_and_toxic_effects_of_drugs = "21B"
    injuries_poisonings_and_toxic_effects_of_drugs_MultipleTrauma = "21A"
    burns = 22
    factors_influencing_health_status_and_other_contacts_with_health_services = 23
    Error = -1

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class ABF_Service_Category(Enum):
    admitted_acute = 1
    admitted_subacute = 2
    admitted_nonacute = 3
    nonadmitted = 4
    emergency_department = 5
    emergency_services = 6

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Remoteness_Category_RA16(Enum):
    Unknown = 9
    Major_City = 0
    Inner_Regional = 1
    Outer_Regional = 2
    Remote = 3
    Very_Remote = 4
    Migratory = 5

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Hosp_State_Category(Enum):
    New_South_Wales = 1
    Victoria = 2
    Queensland = 3
    South_Australia = 4
    Western_Australia = 5
    Tasmania = 6
    Northern_Territory = 7
    Australian_Capital_Territory = 8

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Care_Type_General(Enum):  # METeOR id: 270174
    """
    Patient Care Type - The overall nature of a clinical service provided to an
    admitted patient during an episode of care (admitted care), or the type of
    service provided by the hospital for boarders or posthumous organ procurement
    (other care), as represented by a code.
    """
    acute_care_admitted_care = 01.0
    rehabilitation_care_cannot_be_further_categorised = 02.0
    rehabilitation_care_delivered_in_designated_unit = 02.1
    rehabilitation_care_according_to_designated_program = 02.2
    rehabilitation_care_is_principal_clinical_intent = 02.3
    palliative_care_cannot_be_further_categorised = 03.0
    palliative_care_delivered_in_designated_unit = 03.1
    palliative_care_according_to_designated_program = 03.2
    palliative_care_is_principal_clinical_intent = 03.3
    geriatric_evaluation_and_management = 04.0
    psychogeriatric_care = 05.0
    maintenance_care = 06.0
    newborn_with_full_qualified_days = 07.1
    newborn_with_partial_qualified_days = 07.2
    other_admitted_patient_care = 08.0
    organ_procurement_posthumous = 09.0
    hospital_boarder = 10.0
    mental_health = 11.0

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Care_Type(Enum):
    """
    As the original METeOR id: 270174 has
    several care types that have no mappings to be used here, we create a
    restricted version to avoid confusion
    """
    acute_care_admitted_care = 01.0
    rehabilitation_care_cannot_be_further_categorised = 02.0
    palliative_care_cannot_be_further_categorised = 03.0
    geriatric_evaluation_and_management = 04.0
    psychogeriatric_care = 05.0
    maintenance_care = 06.0

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Indigenous_Status_Category(Enum):
    Aboriginal_not_TSislander = 1
    TSislander_not_Aboriginal = 2
    Both_Aboriginal_and_TSislander = 3
    Neither_Aboriginal_nor_TSislander = 4
    Unknown_or_not_stated = 9

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Stay_Category(Enum):
    same_day = 0
    short_stay_outlier = 1
    inlier = 2
    long_stay_outlier = 3

    def __eq__(self, other):
        if self.__class__.__name__ is other.__class__.__name__:
            return self.value == other.value
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.name)


care_type_to_caretypemapper = {
    "Rehabilitation": Care_Type.rehabilitation_care_cannot_be_further_categorised.value,
    "Palliative Care": Care_Type.palliative_care_cannot_be_further_categorised.value,
    "GEM": Care_Type.geriatric_evaluation_and_management.value,
    "Psychogeriatric Care": Care_Type.psychogeriatric_care.value,
    "Maintenance": Care_Type.maintenance_care.value
}


# Constants fixed for the hospital during setup
hosp_state_constant: Hosp_State_Category = Hosp_State_Category(
    int(os.getenv("HOSPITAL_STATE_INT", default='3')))
HOSP_PAED_FLAG: bool = bool(int(os.getenv("HOSP_PAED_FLAG", '0')))
hosp_level3ICU_flag: bool = bool(int(os.getenv("HOSP_L3_ICU_FLAG", '0')))
global_NEP = float(os.getenv("NEP", "5320.0"))
