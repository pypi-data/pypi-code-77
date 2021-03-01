import logging
from typing import Dict, List, Optional

from cognite.well_model.model.model_utils import deserialize_model
from cognite.well_model.model.models import GetSequenceColumnDTO, GetSequenceDTO

logger = logging.getLogger("deserializing")


def deserialize_object(dict, cls):
    """
    Deserialize a json into a class object

    @param dict: key-word arguments
    @param cls: class type we want to deserialize
    @return: cls object
    """
    try:
        if cls == GetSequenceDTO:
            return deserialize_sequence(dict)

        return deserialize_model(
            model_data=dict,
            model_class=cls,
            path_to_item=[*dict],
            check_type=False,
            configuration=None,
            spec_property_naming=True,
        )
    except Exception as e:
        obj_id = dict.get("id")
        logger.info(f"object type{cls.__class__.__name__} with the id: {obj_id} could not parse due to: {e}")

    return None


def deserialize_sequence(dict):
    """Hack to support deserializing sequences with the generated openapi classes"""
    columns = []
    for c in dict["columns"]:
        col = deserialize_model(
            model_data=c,
            model_class=GetSequenceColumnDTO,
            path_to_item=[*c],
            check_type=False,
            configuration=None,
            spec_property_naming=True,
        )
        columns.append(col)
    dict["columns"] = columns

    return deserialize_model(
        model_data=dict,
        model_class=GetSequenceDTO,
        path_to_item=[*dict],
        check_type=False,
        configuration=None,
        spec_property_naming=True,
    )


def deserialize_list(list_of_dict: List[Dict[str, str]], cls) -> List:
    """
    deserialize a json dictionary to a list of class objects

    @param list_of_dict: List of key-word arguments to deserialize
    @param cls: class type we want to deserialize
    @return: List of class objects
    """

    objects: List[cls] = []  # type: ignore
    try:
        for item in list_of_dict:
            obj: Optional[cls] = deserialize_object(item, cls)  # type: ignore
            if obj is not None:
                objects.append(obj)
    except Exception as e:
        logger.info(f"Could not parse {cls.__class__.__name__} items due to: {e}")

    return objects
