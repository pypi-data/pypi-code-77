from typing import Optional, Union, Type

import dateutil.parser
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, MaltegoEntity
from stix2.base import _STIXBase
from stix2.parsing import dict_to_stix2, _detect_spec_version, STIX2_OBJ_MAPS
from stix2.properties import TimestampProperty

from maltego_stix2.config import (
    _partial_reverse_type_map,
    _reverse_property_maps,
    _heritage_config,
)

def get_stix_type(stix_dict):
    v = _detect_spec_version(stix_dict)
    OBJ_MAP = dict(STIX2_OBJ_MAPS[v]['objects'], **STIX2_OBJ_MAPS[v]['observables'])
    return OBJ_MAP.get(stix_dict['type'])

normalizers = {
    TimestampProperty: dateutil.parser.parse
}


def maltego_to_stix2(
    entity: MaltegoMsg, allow_custom_types=True, allow_custom_fields=True, allow_skipping_stix2_coercion=False
) -> Optional[Union[_STIXBase, dict]]:
    """
    Try to convert any incoming Maltego entity to the closest corresponding STIX2 entity.

    If the input is a "proper" STIX2 entity (i.e. it is in the "maltego.STIX2." namespace), the recovered entity will be
    (at least nearly) equivalent to the STIX2 JSON object that would have been used to generate the Maltego entity.

    If the input is any other Maltego entity, a best guess is applied to generate an equivalent STIX2 object. If no
    matching STIX2 type is found, None is returned unless allow_custom_types is set to True. If allow_custom_types is
    used, this function will generate arbitrary STIX2-like objects will be generated (e.g. a maltego.Person entity will
    result in a 'maltego-person' STIX2 object.

    Properties will be translated according to an internally defined mapping. For instance, in Maltego, the STIX field
    "value" of "domain-name" is instead called "fqdn" on the "STIX2.domain-name" Entity. This mapping will be undone by
    this function, to translate the "fqdn" field back to "value". If allow_custom_fields is True, *all* fields will be
    added to the output object,

    :param entity: an incoming MaltegoMsg object (see maltego-trx library)
    :param allow_custom_types: if True, arbitrary new types may be returned regardless of input type, if False (default)
        only return a result where an "official" STIX2 types can be found.
    :param allow_custom_fields: if True, *all* properties on the Maltego entitiy will be added to the output STIX
        object, no matter if a mapping exists for it or not. If False (default), only properties that can be explicitly
        mapped are kept on the output STIX object.
    :param allow_skipping_stix2_coercion: if True, the final dict is directly returned without being converted to a
        _STIXBase object first. By default, this is turned off.
    :return: The resulting _STIXBase object, or the equivalent dictionary if skip_stix2_coercion is True (or None).
    """
    is_proper_stix2 = False
    stix2_type = None
    for type_ in entity.Geneaology:
        if type_.startswith("maltego.STIX2."):
            is_proper_stix2 = True
            stix2_type = type_
            break
        elif type_ in _partial_reverse_type_map:
            stix2_type = _partial_reverse_type_map[type_]
            break
    if stix2_type is None:
        if allow_custom_types:
            stix2_type = (
                entity.Geneaology[0].lower().replace(".", "-")
            )
        else:
            return None
    reverse_property_map = _reverse_property_maps.get(stix2_type, {})
    if is_proper_stix2:
        # We assume all fields will be valid in the spec, might be better to actually verify that
        res_dict = {
            reverse_property_map.get(
                k, k
            ): v  # all fields are valid in STIX2, but some need to be renamed
            for k, v in entity.Properties.items()
            if k
        }
    else:
        # We assume no fields except the mapped ones will be valid in the spec, might be better to actually verify that
        res_dict = {
            # Only some fields are mapped to STIX2, rest is discarded (unless custom is allowed)
            reverse_property_map.get(k, k): v
            for k, v in entity.Properties.items()
            if (k in reverse_property_map or allow_custom_fields)
            if k
            != "id"  # if it's not a "proper" STIX entity, don't assume the mapped ID field is a proper STIX ID
            and k
        }
        res_dict.update({"type": stix2_type, "spec_version": "2.1"})
    # Handle default values
    mapping = _heritage_config.get(stix2_type)
    if mapping is not None and mapping.default_values is not None:
        for k, v in mapping.default_values.items():
            if k not in res_dict:
                res_dict.update({k: v})

    obj_type: Type[_STIXBase] = get_stix_type(res_dict)
    for prop_name, prop_def in obj_type._properties.items():
        prop_value = res_dict.get(prop_name)
        if not prop_value:
            continue

        normalizer = normalizers.get(prop_def.__class__)
        if normalizer:
            try:
                res_dict[prop_name] = normalizer(prop_value)
            except:
                del res_dict[prop_name]
                if allow_custom_fields:
                    res_dict[f"x_{prop_name}_unparseable"] = prop_value

    try:
        stix2_object = dict_to_stix2(
            res_dict, allow_custom=allow_custom_types or allow_custom_fields
        )
    except Exception as e:
        if allow_skipping_stix2_coercion:
            stix2_object = res_dict
        else:
            raise e

    return stix2_object


def stix2_to_maltego(stix2_object_or_dict: Union[_STIXBase, dict]) -> MaltegoEntity:
    """
    Given some STIX2 object (either as a _STIXBase object or equivalent dictionary), this function generates a new
    MaltegoEntity object that closely corresponds to the input STIX object.

    Objects, Properties and Value are automatically mapped from STIX to the closest corresponding internal Maltego
    equivalent to provide compatibility with other Maltego Transforms.

    :param stix2_object_or_dict: the _STIXBase object or dict to Translate
    :return: the created MaltegoEntity object
    """
    if not isinstance(stix2_object_or_dict, dict):
        stix2_object_as_dict: dict = stix2_object_or_dict._inner
    else:
        stix2_object_as_dict = stix2_object_or_dict

    stix_id = stix2_object_as_dict.get("id")
    if stix_id is None:
        raise ValueError("STIX2 objects must have an 'id' property.")

    mapping = _heritage_config.get(stix2_object_as_dict["type"])
    ent = MaltegoEntity(
        type=f"maltego.STIX2.{stix2_object_as_dict['type']}",
        value=stix_id  # value is always the STIX ID so that entities will merge properly
    )

    for key, value in stix2_object_as_dict.items():
        if mapping is not None:
            key = mapping.translate_prop_name(key)
        if not key:
            continue
        ent.addProperty(
            displayName=key, fieldName=key, value=value, matchingRule="loose"
        )
    if mapping.maltego_from_stix_property_map_extra is not None:
        for maltego_prop_name, stix_prop_name in mapping.maltego_from_stix_property_map_extra.items():
            ent.addProperty(
                displayName=maltego_prop_name, fieldName=maltego_prop_name,
                value=stix2_object_as_dict[stix_prop_name],
                matchingRule="loose"
            )
    return ent

