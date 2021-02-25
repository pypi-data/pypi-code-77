# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/internal/more_extensions.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/protobuf/internal/more_extensions.proto',
  package='google.protobuf.internal',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n.google/protobuf/internal/more_extensions.proto\x12\x18google.protobuf.internal\"P\n\x0fTopLevelMessage\x12=\n\nsubmessage\x18\x01 \x01(\x0b\x32).google.protobuf.internal.ExtendedMessage\"K\n\x0f\x45xtendedMessage\x12\x17\n\x0eoptional_int32\x18\xe9\x07 \x01(\x05\x12\x18\n\x0frepeated_string\x18\xea\x07 \x03(\t*\x05\x08\x01\x10\xe8\x07\"-\n\x0e\x46oreignMessage\x12\x1b\n\x13\x66oreign_message_int\x18\x01 \x01(\x05:I\n\x16optional_int_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x01 \x01(\x05:w\n\x1aoptional_message_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x02 \x01(\x0b\x32(.google.protobuf.internal.ForeignMessage:I\n\x16repeated_int_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x03 \x03(\x05:w\n\x1arepeated_message_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x04 \x03(\x0b\x32(.google.protobuf.internal.ForeignMessage')
)


OPTIONAL_INT_EXTENSION_FIELD_NUMBER = 1
optional_int_extension = _descriptor.FieldDescriptor(
  name='optional_int_extension', full_name='google.protobuf.internal.optional_int_extension', index=0,
  number=1, type=5, cpp_type=1, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)
OPTIONAL_MESSAGE_EXTENSION_FIELD_NUMBER = 2
optional_message_extension = _descriptor.FieldDescriptor(
  name='optional_message_extension', full_name='google.protobuf.internal.optional_message_extension', index=1,
  number=2, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)
REPEATED_INT_EXTENSION_FIELD_NUMBER = 3
repeated_int_extension = _descriptor.FieldDescriptor(
  name='repeated_int_extension', full_name='google.protobuf.internal.repeated_int_extension', index=2,
  number=3, type=5, cpp_type=1, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)
REPEATED_MESSAGE_EXTENSION_FIELD_NUMBER = 4
repeated_message_extension = _descriptor.FieldDescriptor(
  name='repeated_message_extension', full_name='google.protobuf.internal.repeated_message_extension', index=3,
  number=4, type=11, cpp_type=10, label=3,
  has_default_value=False, default_value=[],
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)


_TOPLEVELMESSAGE = _descriptor.Descriptor(
  name='TopLevelMessage',
  full_name='google.protobuf.internal.TopLevelMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='submessage', full_name='google.protobuf.internal.TopLevelMessage.submessage', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=156,
)


_EXTENDEDMESSAGE = _descriptor.Descriptor(
  name='ExtendedMessage',
  full_name='google.protobuf.internal.ExtendedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='optional_int32', full_name='google.protobuf.internal.ExtendedMessage.optional_int32', index=0,
      number=1001, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='repeated_string', full_name='google.protobuf.internal.ExtendedMessage.repeated_string', index=1,
      number=1002, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(1, 1000), ],
  oneofs=[
  ],
  serialized_start=158,
  serialized_end=233,
)


_FOREIGNMESSAGE = _descriptor.Descriptor(
  name='ForeignMessage',
  full_name='google.protobuf.internal.ForeignMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foreign_message_int', full_name='google.protobuf.internal.ForeignMessage.foreign_message_int', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=235,
  serialized_end=280,
)

_TOPLEVELMESSAGE.fields_by_name['submessage'].message_type = _EXTENDEDMESSAGE
DESCRIPTOR.message_types_by_name['TopLevelMessage'] = _TOPLEVELMESSAGE
DESCRIPTOR.message_types_by_name['ExtendedMessage'] = _EXTENDEDMESSAGE
DESCRIPTOR.message_types_by_name['ForeignMessage'] = _FOREIGNMESSAGE
DESCRIPTOR.extensions_by_name['optional_int_extension'] = optional_int_extension
DESCRIPTOR.extensions_by_name['optional_message_extension'] = optional_message_extension
DESCRIPTOR.extensions_by_name['repeated_int_extension'] = repeated_int_extension
DESCRIPTOR.extensions_by_name['repeated_message_extension'] = repeated_message_extension
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TopLevelMessage = _reflection.GeneratedProtocolMessageType('TopLevelMessage', (_message.Message,), {
  'DESCRIPTOR' : _TOPLEVELMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.TopLevelMessage)
  })
_sym_db.RegisterMessage(TopLevelMessage)

ExtendedMessage = _reflection.GeneratedProtocolMessageType('ExtendedMessage', (_message.Message,), {
  'DESCRIPTOR' : _EXTENDEDMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.ExtendedMessage)
  })
_sym_db.RegisterMessage(ExtendedMessage)

ForeignMessage = _reflection.GeneratedProtocolMessageType('ForeignMessage', (_message.Message,), {
  'DESCRIPTOR' : _FOREIGNMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.ForeignMessage)
  })
_sym_db.RegisterMessage(ForeignMessage)

ExtendedMessage.RegisterExtension(optional_int_extension)
optional_message_extension.message_type = _FOREIGNMESSAGE
ExtendedMessage.RegisterExtension(optional_message_extension)
ExtendedMessage.RegisterExtension(repeated_int_extension)
repeated_message_extension.message_type = _FOREIGNMESSAGE
ExtendedMessage.RegisterExtension(repeated_message_extension)

# @@protoc_insertion_point(module_scope)
