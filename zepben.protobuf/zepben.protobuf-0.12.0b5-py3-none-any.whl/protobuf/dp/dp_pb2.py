# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/dp/dp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.dp import dp_requests_pb2 as zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2
from zepben.protobuf.dp import dp_responses_pb2 as zepben_dot_protobuf_dot_dp_dot_dp__responses__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/dp/dp.proto',
  package='zepben.protobuf.dp',
  syntax='proto3',
  serialized_options=b'\n\026com.zepben.protobuf.dpP\001\252\002\022Zepben.Protobuf.DP',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bzepben/protobuf/dp/dp.proto\x12\x12zepben.protobuf.dp\x1a$zepben/protobuf/dp/dp-requests.proto\x1a%zepben/protobuf/dp/dp-responses.proto2\xe9\x03\n\x0f\x44iagramProducer\x12x\n\x14\x43reateDiagramService\x12/.zepben.protobuf.dp.CreateDiagramServiceRequest\x1a/.zepben.protobuf.dp.CreateDiagramServiceRequest\x12~\n\x16\x43ompleteDiagramService\x12\x31.zepben.protobuf.dp.CompleteDiagramServiceRequest\x1a\x31.zepben.protobuf.dp.CompleteDiagramServiceRequest\x12\x64\n\rCreateDiagram\x12(.zepben.protobuf.dp.CreateDiagramRequest\x1a).zepben.protobuf.dp.CreateDiagramResponse\x12v\n\x13\x43reateDiagramObject\x12..zepben.protobuf.dp.CreateDiagramObjectRequest\x1a/.zepben.protobuf.dp.CreateDiagramObjectResponseB/\n\x16\x63om.zepben.protobuf.dpP\x01\xaa\x02\x12Zepben.Protobuf.DPb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2.DESCRIPTOR,zepben_dot_protobuf_dot_dp_dot_dp__responses__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_DIAGRAMPRODUCER = _descriptor.ServiceDescriptor(
  name='DiagramProducer',
  full_name='zepben.protobuf.dp.DiagramProducer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=129,
  serialized_end=618,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateDiagramService',
    full_name='zepben.protobuf.dp.DiagramProducer.CreateDiagramService',
    index=0,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._CREATEDIAGRAMSERVICEREQUEST,
    output_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._CREATEDIAGRAMSERVICEREQUEST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CompleteDiagramService',
    full_name='zepben.protobuf.dp.DiagramProducer.CompleteDiagramService',
    index=1,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._COMPLETEDIAGRAMSERVICEREQUEST,
    output_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._COMPLETEDIAGRAMSERVICEREQUEST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateDiagram',
    full_name='zepben.protobuf.dp.DiagramProducer.CreateDiagram',
    index=2,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._CREATEDIAGRAMREQUEST,
    output_type=zepben_dot_protobuf_dot_dp_dot_dp__responses__pb2._CREATEDIAGRAMRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateDiagramObject',
    full_name='zepben.protobuf.dp.DiagramProducer.CreateDiagramObject',
    index=3,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_dp_dot_dp__requests__pb2._CREATEDIAGRAMOBJECTREQUEST,
    output_type=zepben_dot_protobuf_dot_dp_dot_dp__responses__pb2._CREATEDIAGRAMOBJECTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DIAGRAMPRODUCER)

DESCRIPTOR.services_by_name['DiagramProducer'] = _DIAGRAMPRODUCER

# @@protoc_insertion_point(module_scope)
