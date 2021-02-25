# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import dborgproto_pb2 as dborgproto__pb2


class DashborgServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Proc = channel.unary_unary(
                '/dashborg.rpc1.DashborgService/Proc',
                request_serializer=dborgproto__pb2.ProcMessage.SerializeToString,
                response_deserializer=dborgproto__pb2.ProcResponse.FromString,
                )
        self.SendResponse = channel.unary_unary(
                '/dashborg.rpc1.DashborgService/SendResponse',
                request_serializer=dborgproto__pb2.SendResponseMessage.SerializeToString,
                response_deserializer=dborgproto__pb2.SendResponseResponse.FromString,
                )
        self.RegisterHandler = channel.unary_unary(
                '/dashborg.rpc1.DashborgService/RegisterHandler',
                request_serializer=dborgproto__pb2.RegisterHandlerMessage.SerializeToString,
                response_deserializer=dborgproto__pb2.RegisterHandlerResponse.FromString,
                )
        self.RequestStream = channel.unary_stream(
                '/dashborg.rpc1.DashborgService/RequestStream',
                request_serializer=dborgproto__pb2.RequestStreamMessage.SerializeToString,
                response_deserializer=dborgproto__pb2.RequestMessage.FromString,
                )


class DashborgServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Proc(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterHandler(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestStream(self, request, context):
        """this is backwards since the server sends requests, and the client responds to them
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DashborgServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Proc': grpc.unary_unary_rpc_method_handler(
                    servicer.Proc,
                    request_deserializer=dborgproto__pb2.ProcMessage.FromString,
                    response_serializer=dborgproto__pb2.ProcResponse.SerializeToString,
            ),
            'SendResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.SendResponse,
                    request_deserializer=dborgproto__pb2.SendResponseMessage.FromString,
                    response_serializer=dborgproto__pb2.SendResponseResponse.SerializeToString,
            ),
            'RegisterHandler': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterHandler,
                    request_deserializer=dborgproto__pb2.RegisterHandlerMessage.FromString,
                    response_serializer=dborgproto__pb2.RegisterHandlerResponse.SerializeToString,
            ),
            'RequestStream': grpc.unary_stream_rpc_method_handler(
                    servicer.RequestStream,
                    request_deserializer=dborgproto__pb2.RequestStreamMessage.FromString,
                    response_serializer=dborgproto__pb2.RequestMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dashborg.rpc1.DashborgService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DashborgService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Proc(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dashborg.rpc1.DashborgService/Proc',
            dborgproto__pb2.ProcMessage.SerializeToString,
            dborgproto__pb2.ProcResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dashborg.rpc1.DashborgService/SendResponse',
            dborgproto__pb2.SendResponseMessage.SerializeToString,
            dborgproto__pb2.SendResponseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterHandler(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dashborg.rpc1.DashborgService/RegisterHandler',
            dborgproto__pb2.RegisterHandlerMessage.SerializeToString,
            dborgproto__pb2.RegisterHandlerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RequestStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/dashborg.rpc1.DashborgService/RequestStream',
            dborgproto__pb2.RequestStreamMessage.SerializeToString,
            dborgproto__pb2.RequestMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
