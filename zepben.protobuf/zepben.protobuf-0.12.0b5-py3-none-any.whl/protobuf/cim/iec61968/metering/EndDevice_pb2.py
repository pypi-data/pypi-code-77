# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61968/metering/EndDevice.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61968.assets import AssetContainer_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61968_dot_assets_dot_AssetContainer__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/cim/iec61968/metering/EndDevice.proto',
  package='zepben.protobuf.cim.iec61968.metering',
  syntax='proto3',
  serialized_options=b'\n)com.zepben.protobuf.cim.iec61968.meteringP\001\252\002%Zepben.Protobuf.CIM.IEC61968.Metering',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n5zepben/protobuf/cim/iec61968/metering/EndDevice.proto\x12%zepben.protobuf.cim.iec61968.metering\x1a\x38zepben/protobuf/cim/iec61968/assets/AssetContainer.proto\"\x98\x01\n\tEndDevice\x12?\n\x02\x61\x63\x18\x01 \x01(\x0b\x32\x33.zepben.protobuf.cim.iec61968.assets.AssetContainer\x12\x17\n\x0fusagePointMRIDs\x18\x02 \x03(\t\x12\x14\n\x0c\x63ustomerMRID\x18\x03 \x01(\t\x12\x1b\n\x13serviceLocationMRID\x18\x04 \x01(\tBU\n)com.zepben.protobuf.cim.iec61968.meteringP\x01\xaa\x02%Zepben.Protobuf.CIM.IEC61968.Meteringb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_cim_dot_iec61968_dot_assets_dot_AssetContainer__pb2.DESCRIPTOR,])




_ENDDEVICE = _descriptor.Descriptor(
  name='EndDevice',
  full_name='zepben.protobuf.cim.iec61968.metering.EndDevice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ac', full_name='zepben.protobuf.cim.iec61968.metering.EndDevice.ac', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='usagePointMRIDs', full_name='zepben.protobuf.cim.iec61968.metering.EndDevice.usagePointMRIDs', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='customerMRID', full_name='zepben.protobuf.cim.iec61968.metering.EndDevice.customerMRID', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serviceLocationMRID', full_name='zepben.protobuf.cim.iec61968.metering.EndDevice.serviceLocationMRID', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=155,
  serialized_end=307,
)

_ENDDEVICE.fields_by_name['ac'].message_type = zepben_dot_protobuf_dot_cim_dot_iec61968_dot_assets_dot_AssetContainer__pb2._ASSETCONTAINER
DESCRIPTOR.message_types_by_name['EndDevice'] = _ENDDEVICE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EndDevice = _reflection.GeneratedProtocolMessageType('EndDevice', (_message.Message,), {
  'DESCRIPTOR' : _ENDDEVICE,
  '__module__' : 'zepben.protobuf.cim.iec61968.metering.EndDevice_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61968.metering.EndDevice)
  })
_sym_db.RegisterMessage(EndDevice)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
