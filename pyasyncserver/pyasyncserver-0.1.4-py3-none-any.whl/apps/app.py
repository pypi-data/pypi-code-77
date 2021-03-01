import asyncio
import uvloop

from pyasyncserver.core.logger import get_logger


logger = get_logger(__name__)

class App:
    def __init__(self, pipepool):
        uvloop.install()

        self._loop = asyncio.get_event_loop()

        self._pipepool = pipepool

    def add_pipe(self, pipe):
        self._pipes[pipe.name] = pipe

    def init_app(self):
        pass

    async def _run(self):
        for _, pipe in self._pipepool.pipes.items():
            await pipe.init_pipe(self)
        logger.info('Run')

    def run(self):
        self._loop.run_until_complete(self._run())
        self._loop.run_forever()
        self._loop.close()
