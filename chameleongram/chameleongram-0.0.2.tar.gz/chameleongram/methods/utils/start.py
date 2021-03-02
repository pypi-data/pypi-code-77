import pathlib
from importlib import import_module

from chameleongram.exceptions import NeededSignUp, ClientAlreadyStarted
from ..base import Base


class Start(Base):
    async def start(self):
        """Start the client."""

        self.show_message()

        if self.connection:
            raise ClientAlreadyStarted()

        if self.blueprint:
            for path in (pathlib.Path(x).rglob("*.py") for x in self.blueprint if x):
                for file in path:
                    module_path = ".".join(file.parent.parts + (file.stem,))
                    import_module(module_path)

        await self.connect()
        try:
            return await self.sign_in()
        except NeededSignUp as rpc_error:
            return await self.sign_up(
                phone_number=rpc_error.phone_number,
                phone_code_hash=rpc_error.phone_code_hash,
            )
