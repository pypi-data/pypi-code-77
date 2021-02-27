from requests_counter._redismodule import RedisDB


class ReqCounter:
    def __init__(self, url):
        self.rds = RedisDB(url)
        self.__source_internal_key = "rc_list_source"

    async def setup_api_key(self, tuple_key_threshold):
        await self.rds.setup()
        [await self.rds.create_entry(key_value[0], key_value[1]) for key_value in tuple_key_threshold]

    async def setup_source(self, list_of_source):
        await self.rds.setup()
        await self.rds.create_entry(self.__source_internal_key, ",".join(list_of_source))

    async def check_source(self, source):
        list_of_source = await self.rds.status(self.__source_internal_key)
        return source in list_of_source.decode("utf-8").split(",")

    async def decrease(self, key):
        value = await self.rds.decrease(key)
        return True if int(value) > 0 else False

    async def reset(self, key, value):
        return int(await self.rds.set_key_value(key, value))

    async def destroy(self, key):
        return await self.rds.destroy(key)

    async def destroy_all(self):
        return [await self.rds.destroy(key) for key in await self.rds.all_keys()]

    async def status(self):
        status_dict = dict()
        for key in await self.rds.all_keys():
            try:
                if key.decode("utf-8") == self.__source_internal_key:
                    status_dict[key.decode("utf-8")] = (await self.rds.status(key)).decode("utf-8")
                else:
                    status_dict[key.decode("utf-8")] = int(await self.rds.status(key))
            except Exception:
                pass
        return status_dict

    async def close(self):
        return await self.rds.close()
