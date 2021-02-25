from fastapi import FastAPI
from requests_counter.reqcounter import ReqCounter
import asyncio


app = FastAPI()
cl = ReqCounter("redis://localhost")
asyncio.create_task(cl.setup([]))


@app.get("/destroy/{key}")
async def destroy(key: str):
    res = await cl.destroy(key)
    res = "not found" if res is False else "ok"
    return {"destroy": res}


@app.get("/reset/{key}/{value}")
async def reset(key: str, value: int):
    res = await cl.reset(key, value)
    res = "not found" if res is None else "ok"
    return {"reset": res}


@app.get("/status")
async def status():
    values = await cl.status()
    return values
