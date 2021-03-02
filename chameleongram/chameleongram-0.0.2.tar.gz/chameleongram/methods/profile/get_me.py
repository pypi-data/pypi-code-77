from ...raw import functions, types


class GetMe:
    __call__ = lambda *_: ...

    async def get_me(self):
        return await self(functions.users.GetFullUser(id=types.InputUserSelf()))
