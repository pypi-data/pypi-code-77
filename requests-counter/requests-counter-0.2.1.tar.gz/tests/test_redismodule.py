from requests_counter._redismodule import RedisDB
import pytest


@pytest.mark.asyncio
async def test_decrease_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init([("mykey", 100)])
    res = await dbredis.decrease("mykey")
    await dbredis.close()
    assert res == 99


@pytest.mark.asyncio
async def test_status_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init([("mykey", 100), ("mykey2", 100)])
    res = await dbredis.status("mykey")
    await dbredis.close()
    assert res == 99


@pytest.mark.asyncio
async def test_two_keys_decreased_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init([("mykey", 100), ("mykey2", 100)])
    res1 = await dbredis.decrease("mykey2")
    res2 = await dbredis.decrease("mykey2")
    await dbredis.close()
    assert res1 == 99 and res2 == 98


@pytest.mark.asyncio
async def test_destroy_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init([("mykey", 100), ("mykey2", 100)])
    await dbredis.destroy("mykey")
    await dbredis.destroy("mykey2")
    res1 = await dbredis.status("mykey")
    res2 = await dbredis.status("mykey2")
    await dbredis.close()
    assert res1 is None and res2 is None
