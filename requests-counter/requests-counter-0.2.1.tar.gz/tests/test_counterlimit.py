from requests_counter.reqcounter import ReqCounter
import pytest

values = [("test_1", 5), ("test_2", 5)]


@pytest.mark.asyncio
async def test_decrease():
    cl = ReqCounter('redis://localhost')
    await cl.setup(values)
    res = await cl.decrease("test_1")
    await cl.destroy_all()
    await cl.close()
    assert res is True


@pytest.mark.asyncio
async def test_reset():
    cl = ReqCounter('redis://localhost')
    await cl.setup(values)
    res = await cl.reset("test_1", 100)
    await cl.destroy_all()
    await cl.close()
    assert res == 100


@pytest.mark.asyncio
async def test_destroy():
    cl = ReqCounter('redis://localhost')
    await cl.setup(values)
    res = await cl.destroy_all()
    assert len(res) == len(values)
