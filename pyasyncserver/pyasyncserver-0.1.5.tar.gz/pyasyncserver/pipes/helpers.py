from .http_pipe import HTTPPipe
from .nats_pipe import NATSPipe
from .directions import PipeDirections


class PipePool:
    def __init__(self):
        self._pipes = {}
        self._next_pipe_type = None
        self._next_direction = None
        self._next_handler = None
        self._next_models = None
        self._next_pipe_id = None
        self._next_start_point = None
        self._next_end_point = None

    def _add_pipe(self):
        init_params = {
            'handler': self._next_handler,
            'direction': self._next_direction,
            'models': self._next_models,
        }

        if self._next_pipe_type == 'http':
            if self._next_start_point:
                init_params['socket'] = self._next_start_point
            if self._next_end_point:
                init_params['endpoint'] = self._next_end_point

            cls = HTTPPipe
        elif self._next_pipe_type == 'nats':
            cls = NATSPipe

        pipe = cls(self._next_pipe_id, **init_params)
        self._pipes[pipe.name] = pipe

        self._next_pipe_type = None
        self._next_direction = None
        self._next_handler = None
        self._next_models = None
        self._next_pipe_id = None
        self._next_start_point = None
        self._next_end_point = None

    @property
    def pipes(self): return self._pipes

    async def _handler(self, *args):
        print('handler')

    def pipe(self, *args):
        def decorator(func):
            self._next_pipe_type = args[0]
            self._next_pipe_id = args[1]
            self._next_models = args[2]
            self._add_pipe()

            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def recipient(self, *args):
        def decorator(func):
            self._next_direction = PipeDirections.receiving
            self._next_start_point = args[0]
            self._next_handler = func

            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def sender(self, *args):
        def decorator(func):
            self._next_direction = PipeDirections.sending
            self._next_end_point = args[0]
            self._next_handler = func

            async def wrapper(obj, message, **kwargs):
                _message = message
                func_kwargs = {
                    'message': _message,
                }

                func_result = await func(obj, **func_kwargs)
                if func_result:
                    _message = func_result

                print('Sending message...')
            return wrapper
        return decorator