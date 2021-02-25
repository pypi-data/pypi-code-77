# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from mtbpy import mtb_command_rpc_pb2 as mtbpy_dot_mtb__command__rpc__pb2


class MtbCommandStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddMessage = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/AddMessage',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.AddMessageRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.SetCommandNote = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/SetCommandNote',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.SetCommandNoteRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.SetCommandTitle = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/SetCommandTitle',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.SetCommandTitleRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.AddImage = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/AddImage',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.AddImageRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.AddTable = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/AddTable',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.AddTableRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.GetVariable = channel.unary_unary(
        '/rpc.mtb_command.v1.MtbCommand/GetVariable',
        request_serializer=mtbpy_dot_mtb__command__rpc__pb2.VariableRequest.SerializeToString,
        response_deserializer=mtbpy_dot_mtb__command__rpc__pb2.VariableResponse.FromString,
        )


class MtbCommandServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def AddMessage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetCommandNote(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetCommandTitle(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddImage(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddTable(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetVariable(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MtbCommandServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddMessage': grpc.unary_unary_rpc_method_handler(
          servicer.AddMessage,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.AddMessageRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'SetCommandNote': grpc.unary_unary_rpc_method_handler(
          servicer.SetCommandNote,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.SetCommandNoteRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'SetCommandTitle': grpc.unary_unary_rpc_method_handler(
          servicer.SetCommandTitle,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.SetCommandTitleRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'AddImage': grpc.unary_unary_rpc_method_handler(
          servicer.AddImage,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.AddImageRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'AddTable': grpc.unary_unary_rpc_method_handler(
          servicer.AddTable,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.AddTableRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'GetVariable': grpc.unary_unary_rpc_method_handler(
          servicer.GetVariable,
          request_deserializer=mtbpy_dot_mtb__command__rpc__pb2.VariableRequest.FromString,
          response_serializer=mtbpy_dot_mtb__command__rpc__pb2.VariableResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'rpc.mtb_command.v1.MtbCommand', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
