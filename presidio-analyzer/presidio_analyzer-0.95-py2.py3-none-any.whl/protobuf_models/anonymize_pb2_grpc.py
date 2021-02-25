# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import anonymize_pb2 as anonymize__pb2


class AnonymizeServiceStub(object):
  """The Anonymize Service is a service that anonymizes a given the text using predefined analyzers fields and anonymize configurations.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Apply = channel.unary_unary(
        '/types.AnonymizeService/Apply',
        request_serializer=anonymize__pb2.AnonymizeRequest.SerializeToString,
        response_deserializer=anonymize__pb2.AnonymizeResponse.FromString,
        )


class AnonymizeServiceServicer(object):
  """The Anonymize Service is a service that anonymizes a given the text using predefined analyzers fields and anonymize configurations.
  """

  def Apply(self, request, context):
    """Apply method will execute on the given request and return the anonymize response with the sensitive text anonymized
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AnonymizeServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Apply': grpc.unary_unary_rpc_method_handler(
          servicer.Apply,
          request_deserializer=anonymize__pb2.AnonymizeRequest.FromString,
          response_serializer=anonymize__pb2.AnonymizeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'types.AnonymizeService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
