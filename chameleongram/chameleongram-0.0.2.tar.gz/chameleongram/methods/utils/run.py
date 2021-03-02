import trio

from chameleongram.exceptions import Propagate, NowStop
from ..base import Base


class Run(Base):
    async def run(self):
        """Run a client instance."""

        await self.start()

        while True:
            if self.handlers:
                try:
                    update = await self.recv()
                except AttributeError:
                    break

                for handler in self.handlers:
                    _update = update

                    if handler.filters is not None:
                        if not handler(_update, self):
                            continue
                    try:
                        await handler.callback(self, _update)
                        continue
                    except NowStop:
                        continue
                    except Propagate:
                        ...

            else:
                await trio.sleep(1)
