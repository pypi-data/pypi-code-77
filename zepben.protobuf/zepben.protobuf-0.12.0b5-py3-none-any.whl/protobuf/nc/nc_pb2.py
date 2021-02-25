# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/nc/nc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.nc import nc_requests_pb2 as zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2
from zepben.protobuf.nc import nc_responses_pb2 as zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/nc/nc.proto',
  package='zepben.protobuf.nc',
  syntax='proto3',
  serialized_options=b'\n\026com.zepben.protobuf.ncP\001\252\002\022Zepben.Protobuf.NC',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bzepben/protobuf/nc/nc.proto\x12\x12zepben.protobuf.nc\x1a$zepben/protobuf/nc/nc-requests.proto\x1a%zepben/protobuf/nc/nc-responses.proto2\xb0\x06\n\x0fNetworkConsumer\x12{\n\x14getIdentifiedObjects\x12/.zepben.protobuf.nc.GetIdentifiedObjectsRequest\x1a\x30.zepben.protobuf.nc.GetIdentifiedObjectsResponse0\x01\x12v\n\x13getNetworkHierarchy\x12..zepben.protobuf.nc.GetNetworkHierarchyRequest\x1a/.zepben.protobuf.nc.GetNetworkHierarchyResponse\x12\x87\x01\n\x18getEquipmentForContainer\x12\x33.zepben.protobuf.nc.GetEquipmentForContainerRequest\x1a\x34.zepben.protobuf.nc.GetEquipmentForContainerResponse0\x01\x12\x93\x01\n\x1cgetCurrentEquipmentForFeeder\x12\x37.zepben.protobuf.nc.GetCurrentEquipmentForFeederRequest\x1a\x38.zepben.protobuf.nc.GetCurrentEquipmentForFeederResponse0\x01\x12\x8d\x01\n\x1agetEquipmentForRestriction\x12\x35.zepben.protobuf.nc.GetEquipmentForRestrictionRequest\x1a\x36.zepben.protobuf.nc.GetEquipmentForRestrictionResponse0\x01\x12x\n\x13getTerminalsForNode\x12..zepben.protobuf.nc.GetTerminalsForNodeRequest\x1a/.zepben.protobuf.nc.GetTerminalsForNodeResponse0\x01\x42/\n\x16\x63om.zepben.protobuf.ncP\x01\xaa\x02\x12Zepben.Protobuf.NCb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2.DESCRIPTOR,zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_NETWORKCONSUMER = _descriptor.ServiceDescriptor(
  name='NetworkConsumer',
  full_name='zepben.protobuf.nc.NetworkConsumer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=129,
  serialized_end=945,
  methods=[
  _descriptor.MethodDescriptor(
    name='getIdentifiedObjects',
    full_name='zepben.protobuf.nc.NetworkConsumer.getIdentifiedObjects',
    index=0,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETIDENTIFIEDOBJECTSREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETIDENTIFIEDOBJECTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getNetworkHierarchy',
    full_name='zepben.protobuf.nc.NetworkConsumer.getNetworkHierarchy',
    index=1,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETNETWORKHIERARCHYREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETNETWORKHIERARCHYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getEquipmentForContainer',
    full_name='zepben.protobuf.nc.NetworkConsumer.getEquipmentForContainer',
    index=2,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETEQUIPMENTFORCONTAINERREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETEQUIPMENTFORCONTAINERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getCurrentEquipmentForFeeder',
    full_name='zepben.protobuf.nc.NetworkConsumer.getCurrentEquipmentForFeeder',
    index=3,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETCURRENTEQUIPMENTFORFEEDERREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETCURRENTEQUIPMENTFORFEEDERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getEquipmentForRestriction',
    full_name='zepben.protobuf.nc.NetworkConsumer.getEquipmentForRestriction',
    index=4,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETEQUIPMENTFORRESTRICTIONREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETEQUIPMENTFORRESTRICTIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='getTerminalsForNode',
    full_name='zepben.protobuf.nc.NetworkConsumer.getTerminalsForNode',
    index=5,
    containing_service=None,
    input_type=zepben_dot_protobuf_dot_nc_dot_nc__requests__pb2._GETTERMINALSFORNODEREQUEST,
    output_type=zepben_dot_protobuf_dot_nc_dot_nc__responses__pb2._GETTERMINALSFORNODERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_NETWORKCONSUMER)

DESCRIPTOR.services_by_name['NetworkConsumer'] = _NETWORKCONSUMER

# @@protoc_insertion_point(module_scope)
