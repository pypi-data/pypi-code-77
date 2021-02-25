# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/nc/nc-responses.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.nc import nc_data_pb2 as zepben_dot_protobuf_dot_nc_dot_nc__data__pb2
from zepben.protobuf.cim.iec61970.base.core import Terminal_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/nc/nc-responses.proto',
  package='zepben.protobuf.nc',
  syntax='proto3',
  serialized_options=b'\n\026com.zepben.protobuf.ncP\001\252\002\022Zepben.Protobuf.NC',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%zepben/protobuf/nc/nc-responses.proto\x12\x12zepben.protobuf.nc\x1a zepben/protobuf/nc/nc-data.proto\x1a\x35zepben/protobuf/cim/iec61970/base/core/Terminal.proto\"\xe2\x02\n\x1bGetNetworkHierarchyResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12S\n\x13geographicalRegions\x18\x02 \x03(\x0b\x32\x36.zepben.protobuf.nc.NetworkHierarchyGeographicalRegion\x12Y\n\x16subGeographicalRegions\x18\x03 \x03(\x0b\x32\x39.zepben.protobuf.nc.NetworkHierarchySubGeographicalRegion\x12\x43\n\x0bsubstations\x18\x04 \x03(\x0b\x32..zepben.protobuf.nc.NetworkHierarchySubstation\x12;\n\x07\x66\x65\x65\x64\x65rs\x18\x05 \x03(\x0b\x32*.zepben.protobuf.nc.NetworkHierarchyFeeder\"x\n\x1cGetIdentifiedObjectsResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x45\n\x10identifiedObject\x18\x02 \x01(\x0b\x32+.zepben.protobuf.nc.NetworkIdentifiedObject\"|\n GetEquipmentForContainerResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x45\n\x10identifiedObject\x18\x02 \x01(\x0b\x32+.zepben.protobuf.nc.NetworkIdentifiedObject\"\x80\x01\n$GetCurrentEquipmentForFeederResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x45\n\x10identifiedObject\x18\x02 \x01(\x0b\x32+.zepben.protobuf.nc.NetworkIdentifiedObject\"~\n\"GetEquipmentForRestrictionResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x45\n\x10identifiedObject\x18\x02 \x01(\x0b\x32+.zepben.protobuf.nc.NetworkIdentifiedObject\"t\n\x1bGetTerminalsForNodeResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x42\n\x08terminal\x18\x02 \x01(\x0b\x32\x30.zepben.protobuf.cim.iec61970.base.core.TerminalB/\n\x16\x63om.zepben.protobuf.ncP\x01\xaa\x02\x12Zepben.Protobuf.NCb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_nc_dot_nc__data__pb2.DESCRIPTOR,zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2.DESCRIPTOR,])




_GETNETWORKHIERARCHYRESPONSE = _descriptor.Descriptor(
  name='GetNetworkHierarchyResponse',
  full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='geographicalRegions', full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse.geographicalRegions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='subGeographicalRegions', full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse.subGeographicalRegions', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='substations', full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse.substations', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feeders', full_name='zepben.protobuf.nc.GetNetworkHierarchyResponse.feeders', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=151,
  serialized_end=505,
)


_GETIDENTIFIEDOBJECTSRESPONSE = _descriptor.Descriptor(
  name='GetIdentifiedObjectsResponse',
  full_name='zepben.protobuf.nc.GetIdentifiedObjectsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetIdentifiedObjectsResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='identifiedObject', full_name='zepben.protobuf.nc.GetIdentifiedObjectsResponse.identifiedObject', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=507,
  serialized_end=627,
)


_GETEQUIPMENTFORCONTAINERRESPONSE = _descriptor.Descriptor(
  name='GetEquipmentForContainerResponse',
  full_name='zepben.protobuf.nc.GetEquipmentForContainerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetEquipmentForContainerResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='identifiedObject', full_name='zepben.protobuf.nc.GetEquipmentForContainerResponse.identifiedObject', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=629,
  serialized_end=753,
)


_GETCURRENTEQUIPMENTFORFEEDERRESPONSE = _descriptor.Descriptor(
  name='GetCurrentEquipmentForFeederResponse',
  full_name='zepben.protobuf.nc.GetCurrentEquipmentForFeederResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetCurrentEquipmentForFeederResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='identifiedObject', full_name='zepben.protobuf.nc.GetCurrentEquipmentForFeederResponse.identifiedObject', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=756,
  serialized_end=884,
)


_GETEQUIPMENTFORRESTRICTIONRESPONSE = _descriptor.Descriptor(
  name='GetEquipmentForRestrictionResponse',
  full_name='zepben.protobuf.nc.GetEquipmentForRestrictionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetEquipmentForRestrictionResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='identifiedObject', full_name='zepben.protobuf.nc.GetEquipmentForRestrictionResponse.identifiedObject', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=886,
  serialized_end=1012,
)


_GETTERMINALSFORNODERESPONSE = _descriptor.Descriptor(
  name='GetTerminalsForNodeResponse',
  full_name='zepben.protobuf.nc.GetTerminalsForNodeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.nc.GetTerminalsForNodeResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='terminal', full_name='zepben.protobuf.nc.GetTerminalsForNodeResponse.terminal', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1014,
  serialized_end=1130,
)

_GETNETWORKHIERARCHYRESPONSE.fields_by_name['geographicalRegions'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKHIERARCHYGEOGRAPHICALREGION
_GETNETWORKHIERARCHYRESPONSE.fields_by_name['subGeographicalRegions'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKHIERARCHYSUBGEOGRAPHICALREGION
_GETNETWORKHIERARCHYRESPONSE.fields_by_name['substations'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKHIERARCHYSUBSTATION
_GETNETWORKHIERARCHYRESPONSE.fields_by_name['feeders'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKHIERARCHYFEEDER
_GETIDENTIFIEDOBJECTSRESPONSE.fields_by_name['identifiedObject'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKIDENTIFIEDOBJECT
_GETEQUIPMENTFORCONTAINERRESPONSE.fields_by_name['identifiedObject'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKIDENTIFIEDOBJECT
_GETCURRENTEQUIPMENTFORFEEDERRESPONSE.fields_by_name['identifiedObject'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKIDENTIFIEDOBJECT
_GETEQUIPMENTFORRESTRICTIONRESPONSE.fields_by_name['identifiedObject'].message_type = zepben_dot_protobuf_dot_nc_dot_nc__data__pb2._NETWORKIDENTIFIEDOBJECT
_GETTERMINALSFORNODERESPONSE.fields_by_name['terminal'].message_type = zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_core_dot_Terminal__pb2._TERMINAL
DESCRIPTOR.message_types_by_name['GetNetworkHierarchyResponse'] = _GETNETWORKHIERARCHYRESPONSE
DESCRIPTOR.message_types_by_name['GetIdentifiedObjectsResponse'] = _GETIDENTIFIEDOBJECTSRESPONSE
DESCRIPTOR.message_types_by_name['GetEquipmentForContainerResponse'] = _GETEQUIPMENTFORCONTAINERRESPONSE
DESCRIPTOR.message_types_by_name['GetCurrentEquipmentForFeederResponse'] = _GETCURRENTEQUIPMENTFORFEEDERRESPONSE
DESCRIPTOR.message_types_by_name['GetEquipmentForRestrictionResponse'] = _GETEQUIPMENTFORRESTRICTIONRESPONSE
DESCRIPTOR.message_types_by_name['GetTerminalsForNodeResponse'] = _GETTERMINALSFORNODERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetNetworkHierarchyResponse = _reflection.GeneratedProtocolMessageType('GetNetworkHierarchyResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETNETWORKHIERARCHYRESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetNetworkHierarchyResponse)
  })
_sym_db.RegisterMessage(GetNetworkHierarchyResponse)

GetIdentifiedObjectsResponse = _reflection.GeneratedProtocolMessageType('GetIdentifiedObjectsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETIDENTIFIEDOBJECTSRESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetIdentifiedObjectsResponse)
  })
_sym_db.RegisterMessage(GetIdentifiedObjectsResponse)

GetEquipmentForContainerResponse = _reflection.GeneratedProtocolMessageType('GetEquipmentForContainerResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETEQUIPMENTFORCONTAINERRESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetEquipmentForContainerResponse)
  })
_sym_db.RegisterMessage(GetEquipmentForContainerResponse)

GetCurrentEquipmentForFeederResponse = _reflection.GeneratedProtocolMessageType('GetCurrentEquipmentForFeederResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCURRENTEQUIPMENTFORFEEDERRESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetCurrentEquipmentForFeederResponse)
  })
_sym_db.RegisterMessage(GetCurrentEquipmentForFeederResponse)

GetEquipmentForRestrictionResponse = _reflection.GeneratedProtocolMessageType('GetEquipmentForRestrictionResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETEQUIPMENTFORRESTRICTIONRESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetEquipmentForRestrictionResponse)
  })
_sym_db.RegisterMessage(GetEquipmentForRestrictionResponse)

GetTerminalsForNodeResponse = _reflection.GeneratedProtocolMessageType('GetTerminalsForNodeResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTERMINALSFORNODERESPONSE,
  '__module__' : 'zepben.protobuf.nc.nc_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.nc.GetTerminalsForNodeResponse)
  })
_sym_db.RegisterMessage(GetTerminalsForNodeResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
