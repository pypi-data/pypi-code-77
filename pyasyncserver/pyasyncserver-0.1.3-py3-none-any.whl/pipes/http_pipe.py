import json

from aiohttp import web
from message_prototypes import BaseMessage
from message_prototypes.pipe_messages import RequestMessage, ResponseMessage

from .pipe import Pipe
from .directions import PipeDirections


class HTTPPipe(Pipe):
    def __init__(self, name, **kwargs):
        self._http_handler = kwargs.get('handler', None)
        self._socket = kwargs.get('socket', None)
        self._direction = kwargs.get('direction', None)
        self._endpoint = kwargs.get('endpoint', None)
        self._models = kwargs.get('models', tuple([]))

        Pipe.__init__(self, name, **kwargs)

    async def _handler(self, *args):
        request = args[0]

        if request.method not in ('POST', 'OPTIONS') or \
                request.path != '/_pipe':
            return web.Response(
                status=400,
                text='HTTP Method or url path is not allowed!')

        if request.method == 'OPTIONS':
            pipe_info = {
                'allowed_models': [m.__name__ for m in self._models],
            }
            return web.Response(
                status=200,
                body=json.dumps(pipe_info),
                content_type='application/json')

        try:
            data = await request.json()
        except Exception:
            return web.Response(
                status=400,
                text='Bad request body!')

        message_model = BaseMessage.detect_model(data)
        if message_model not in self._models:
            return web.Response(
                status=400, 
                text='Incorrect or invalid model!')

        result = await self._http_handler(
            self._app, message=message_model.unpack(data))
        if result.__class__ == ResponseMessage:
            response = result.pack()
        else:
            response = {}

        return web.Response(
            status=200,
            body=json.dumps(response),
            content_type='application/json')

    def __str__(self):
        result = []

        result.append(f'name={self.name}')

        if self._direction in \
            [PipeDirections.sending, PipeDirections.duplex]:
            result.append(f'endpoint={self._endpoint}')

        if self._direction in \
            [PipeDirections.receiving, PipeDirections.duplex]:
            result.append(f'socket={self._socket}')

        return f'[HTTPPipe {" ".join(result)}]'

    async def _init(self):
        if self._direction == PipeDirections.receiving:
            host, port = self._socket.split(':')
            server = web.Server(self._handler)
            runner = web.ServerRunner(server)

            await runner.setup()

            site = web.TCPSite(runner, host, int(port))

            await site.start()
