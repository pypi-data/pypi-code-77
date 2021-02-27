from requests_counter._redismodule import RedisDB


class ReqCounter:
    def __init__(self, url):
        self.rds = RedisDB(url)

    async def setup(self, values):
        await self.rds.init(values)

    async def decrease(self, key):
        value = await self.rds.decrease(key)
        return True if value > 0 else False

    async def reset(self, key, value):
        return await self.rds.set_key_value(key, value)

    async def destroy(self, key):
        return await self.rds.destroy(key)

    async def destroy_all(self):
        return [await self.rds.destroy(key) for key in await self.rds.all_keys()]

    async def status(self):
        return [{"key": key, "value": await self.rds.status(key)} for key in await self.rds.all_keys()]

    async def close(self):
        return await self.rds.close()
