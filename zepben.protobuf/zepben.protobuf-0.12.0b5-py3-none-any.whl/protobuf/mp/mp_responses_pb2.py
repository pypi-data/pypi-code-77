# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/mp/mp-responses.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/mp/mp-responses.proto',
  package='zepben.protobuf.mp',
  syntax='proto3',
  serialized_options=b'\n\026com.zepben.protobuf.mpP\001\252\002\022Zepben.Protobuf.MP',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%zepben/protobuf/mp/mp-responses.proto\x12\x12zepben.protobuf.mp\".\n\x19\x43reateAnalogValueResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\"3\n\x1e\x43reateAccumulatorValueResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\"0\n\x1b\x43reateDiscreteValueResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\"/\n\x1a\x43reateAnalogValuesResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\"4\n\x1f\x43reateAccumulatorValuesResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\"1\n\x1c\x43reateDiscreteValuesResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x42/\n\x16\x63om.zepben.protobuf.mpP\x01\xaa\x02\x12Zepben.Protobuf.MPb\x06proto3'
)




_CREATEANALOGVALUERESPONSE = _descriptor.Descriptor(
  name='CreateAnalogValueResponse',
  full_name='zepben.protobuf.mp.CreateAnalogValueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateAnalogValueResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=61,
  serialized_end=107,
)


_CREATEACCUMULATORVALUERESPONSE = _descriptor.Descriptor(
  name='CreateAccumulatorValueResponse',
  full_name='zepben.protobuf.mp.CreateAccumulatorValueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateAccumulatorValueResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=109,
  serialized_end=160,
)


_CREATEDISCRETEVALUERESPONSE = _descriptor.Descriptor(
  name='CreateDiscreteValueResponse',
  full_name='zepben.protobuf.mp.CreateDiscreteValueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateDiscreteValueResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=162,
  serialized_end=210,
)


_CREATEANALOGVALUESRESPONSE = _descriptor.Descriptor(
  name='CreateAnalogValuesResponse',
  full_name='zepben.protobuf.mp.CreateAnalogValuesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateAnalogValuesResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=212,
  serialized_end=259,
)


_CREATEACCUMULATORVALUESRESPONSE = _descriptor.Descriptor(
  name='CreateAccumulatorValuesResponse',
  full_name='zepben.protobuf.mp.CreateAccumulatorValuesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateAccumulatorValuesResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=261,
  serialized_end=313,
)


_CREATEDISCRETEVALUESRESPONSE = _descriptor.Descriptor(
  name='CreateDiscreteValuesResponse',
  full_name='zepben.protobuf.mp.CreateDiscreteValuesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageId', full_name='zepben.protobuf.mp.CreateDiscreteValuesResponse.messageId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=315,
  serialized_end=364,
)

DESCRIPTOR.message_types_by_name['CreateAnalogValueResponse'] = _CREATEANALOGVALUERESPONSE
DESCRIPTOR.message_types_by_name['CreateAccumulatorValueResponse'] = _CREATEACCUMULATORVALUERESPONSE
DESCRIPTOR.message_types_by_name['CreateDiscreteValueResponse'] = _CREATEDISCRETEVALUERESPONSE
DESCRIPTOR.message_types_by_name['CreateAnalogValuesResponse'] = _CREATEANALOGVALUESRESPONSE
DESCRIPTOR.message_types_by_name['CreateAccumulatorValuesResponse'] = _CREATEACCUMULATORVALUESRESPONSE
DESCRIPTOR.message_types_by_name['CreateDiscreteValuesResponse'] = _CREATEDISCRETEVALUESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateAnalogValueResponse = _reflection.GeneratedProtocolMessageType('CreateAnalogValueResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEANALOGVALUERESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateAnalogValueResponse)
  })
_sym_db.RegisterMessage(CreateAnalogValueResponse)

CreateAccumulatorValueResponse = _reflection.GeneratedProtocolMessageType('CreateAccumulatorValueResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCUMULATORVALUERESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateAccumulatorValueResponse)
  })
_sym_db.RegisterMessage(CreateAccumulatorValueResponse)

CreateDiscreteValueResponse = _reflection.GeneratedProtocolMessageType('CreateDiscreteValueResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEDISCRETEVALUERESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateDiscreteValueResponse)
  })
_sym_db.RegisterMessage(CreateDiscreteValueResponse)

CreateAnalogValuesResponse = _reflection.GeneratedProtocolMessageType('CreateAnalogValuesResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEANALOGVALUESRESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateAnalogValuesResponse)
  })
_sym_db.RegisterMessage(CreateAnalogValuesResponse)

CreateAccumulatorValuesResponse = _reflection.GeneratedProtocolMessageType('CreateAccumulatorValuesResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCUMULATORVALUESRESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateAccumulatorValuesResponse)
  })
_sym_db.RegisterMessage(CreateAccumulatorValuesResponse)

CreateDiscreteValuesResponse = _reflection.GeneratedProtocolMessageType('CreateDiscreteValuesResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEDISCRETEVALUESRESPONSE,
  '__module__' : 'zepben.protobuf.mp.mp_responses_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.mp.CreateDiscreteValuesResponse)
  })
_sym_db.RegisterMessage(CreateDiscreteValuesResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
