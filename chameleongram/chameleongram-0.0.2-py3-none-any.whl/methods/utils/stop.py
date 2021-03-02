from ..base import Base


class Stop(Base):
    async def stop(self):
        """Run a client instance."""

        try:
            await self.connection.close()
        except AttributeError:
            pass
        self.connection = None
        self.server_salt = None
