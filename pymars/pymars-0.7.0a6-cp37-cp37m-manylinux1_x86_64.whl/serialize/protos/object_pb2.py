# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mars/serialize/protos/object.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mars.serialize.protos import value_pb2 as mars_dot_serialize_dot_protos_dot_value__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mars/serialize/protos/object.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\"mars/serialize/protos/object.proto\x1a!mars/serialize/protos/value.proto\"~\n\x0eObjectChunkDef\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x11\n\x05index\x18\x02 \x03(\rB\x02\x10\x01\x12\x12\n\x02op\x18\x03 \x01(\x0b\x32\x06.Value\x12\x0e\n\x06\x63\x61\x63hed\x18\x04 \x01(\x08\x12\x1c\n\x0c\x65xtra_params\x18\x05 \x01(\x0b\x32\x06.Value\x12\n\n\x02id\x18\x06 \x01(\t\"\x90\x01\n\tObjectDef\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x12\n\x02op\x18\x03 \x01(\x0b\x32\x06.Value\x12\x17\n\x07nsplits\x18\x05 \x01(\x0b\x32\x06.Value\x12\x1f\n\x06\x63hunks\x18\x06 \x03(\x0b\x32\x0f.ObjectChunkDef\x12\x1c\n\x0c\x65xtra_params\x18\x07 \x01(\x0b\x32\x06.Value\x12\n\n\x02id\x18\x08 \x01(\tb\x06proto3')
  ,
  dependencies=[mars_dot_serialize_dot_protos_dot_value__pb2.DESCRIPTOR,])




_OBJECTCHUNKDEF = _descriptor.Descriptor(
  name='ObjectChunkDef',
  full_name='ObjectChunkDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ObjectChunkDef.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='index', full_name='ObjectChunkDef.index', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\020\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op', full_name='ObjectChunkDef.op', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cached', full_name='ObjectChunkDef.cached', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra_params', full_name='ObjectChunkDef.extra_params', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='ObjectChunkDef.id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=73,
  serialized_end=199,
)


_OBJECTDEF = _descriptor.Descriptor(
  name='ObjectDef',
  full_name='ObjectDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ObjectDef.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op', full_name='ObjectDef.op', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nsplits', full_name='ObjectDef.nsplits', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunks', full_name='ObjectDef.chunks', index=3,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra_params', full_name='ObjectDef.extra_params', index=4,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='ObjectDef.id', index=5,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=202,
  serialized_end=346,
)

_OBJECTCHUNKDEF.fields_by_name['op'].message_type = mars_dot_serialize_dot_protos_dot_value__pb2._VALUE
_OBJECTCHUNKDEF.fields_by_name['extra_params'].message_type = mars_dot_serialize_dot_protos_dot_value__pb2._VALUE
_OBJECTDEF.fields_by_name['op'].message_type = mars_dot_serialize_dot_protos_dot_value__pb2._VALUE
_OBJECTDEF.fields_by_name['nsplits'].message_type = mars_dot_serialize_dot_protos_dot_value__pb2._VALUE
_OBJECTDEF.fields_by_name['chunks'].message_type = _OBJECTCHUNKDEF
_OBJECTDEF.fields_by_name['extra_params'].message_type = mars_dot_serialize_dot_protos_dot_value__pb2._VALUE
DESCRIPTOR.message_types_by_name['ObjectChunkDef'] = _OBJECTCHUNKDEF
DESCRIPTOR.message_types_by_name['ObjectDef'] = _OBJECTDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObjectChunkDef = _reflection.GeneratedProtocolMessageType('ObjectChunkDef', (_message.Message,), dict(
  DESCRIPTOR = _OBJECTCHUNKDEF,
  __module__ = 'mars.serialize.protos.object_pb2'
  # @@protoc_insertion_point(class_scope:ObjectChunkDef)
  ))
_sym_db.RegisterMessage(ObjectChunkDef)

ObjectDef = _reflection.GeneratedProtocolMessageType('ObjectDef', (_message.Message,), dict(
  DESCRIPTOR = _OBJECTDEF,
  __module__ = 'mars.serialize.protos.object_pb2'
  # @@protoc_insertion_point(class_scope:ObjectDef)
  ))
_sym_db.RegisterMessage(ObjectDef)


_OBJECTCHUNKDEF.fields_by_name['index']._options = None
# @@protoc_insertion_point(module_scope)
