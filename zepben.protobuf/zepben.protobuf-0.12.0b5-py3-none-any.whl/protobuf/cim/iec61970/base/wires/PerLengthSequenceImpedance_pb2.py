# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61970.base.wires import PerLengthImpedance_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthImpedance__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto',
  package='zepben.protobuf.cim.iec61970.base.wires',
  syntax='proto3',
  serialized_options=b'\n+com.zepben.protobuf.cim.iec61970.base.wiresP\001\252\002\'Zepben.Protobuf.CIM.IEC61970.Base.Wires',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nHzepben/protobuf/cim/iec61970/base/wires/PerLengthSequenceImpedance.proto\x12\'zepben.protobuf.cim.iec61970.base.wires\x1a@zepben/protobuf/cim/iec61970/base/wires/PerLengthImpedance.proto\"\xca\x01\n\x1aPerLengthSequenceImpedance\x12H\n\x03pli\x18\x01 \x01(\x0b\x32;.zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance\x12\t\n\x01r\x18\x02 \x01(\x01\x12\t\n\x01x\x18\x03 \x01(\x01\x12\n\n\x02r0\x18\x04 \x01(\x01\x12\n\n\x02x0\x18\x05 \x01(\x01\x12\x0b\n\x03\x62\x63h\x18\x06 \x01(\x01\x12\x0c\n\x04\x62\x30\x63h\x18\x07 \x01(\x01\x12\x0b\n\x03gch\x18\x08 \x01(\x01\x12\x0c\n\x04g0ch\x18\t \x01(\x01\x42Y\n+com.zepben.protobuf.cim.iec61970.base.wiresP\x01\xaa\x02\'Zepben.Protobuf.CIM.IEC61970.Base.Wiresb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthImpedance__pb2.DESCRIPTOR,])




_PERLENGTHSEQUENCEIMPEDANCE = _descriptor.Descriptor(
  name='PerLengthSequenceImpedance',
  full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pli', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.pli', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='r', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.r', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.x', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='r0', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.r0', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x0', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.x0', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bch', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.bch', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b0ch', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.b0ch', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gch', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.gch', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='g0ch', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance.g0ch', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=184,
  serialized_end=386,
)

_PERLENGTHSEQUENCEIMPEDANCE.fields_by_name['pli'].message_type = zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthImpedance__pb2._PERLENGTHIMPEDANCE
DESCRIPTOR.message_types_by_name['PerLengthSequenceImpedance'] = _PERLENGTHSEQUENCEIMPEDANCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PerLengthSequenceImpedance = _reflection.GeneratedProtocolMessageType('PerLengthSequenceImpedance', (_message.Message,), {
  'DESCRIPTOR' : _PERLENGTHSEQUENCEIMPEDANCE,
  '__module__' : 'zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance)
  })
_sym_db.RegisterMessage(PerLengthSequenceImpedance)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
