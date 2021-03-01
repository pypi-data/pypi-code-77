from pyasyncserver.core.logger import get_logger


logger = get_logger(__name__)


class Pipe:
    def __init__(self, name, **kwargs):
        self._pipe_name = name
        self._app = None

    @property
    def name(self): return self._pipe_name

    async def _init(self):
        pass

    async def init_pipe(self, app):
        self._app = app
        
        await self._init()
        logger.info(f'Init pipe: {self}')