from fastapi import Depends, FastAPI, HTTPException, Header

# 1. Import the library
from requests_counter.reqcounter import ReqCounter

import asyncio
app = FastAPI()

# 2. Create an ReqCounter object with the url to redis instance as parameter
cl = ReqCounter("redis://localhost")

# 3. populate the Object with a list of tuple (key, max_value)
asyncio.create_task(cl.setup_api_key([("my-api-key-test", 100)]))
asyncio.create_task(cl.setup_source(["source1", "source2"]))


# 4. Declare a function to inject to Depends module. It will decrease the max_value for each request. It will raise a 429 HTTPException when max_value is 0.
async def check_key(apiKey: str = Header(None), source: str = Header(None)):
    res = await cl.decrease(apiKey)
    if res is False:
        raise HTTPException(400, "User Requests Limit Exceeded")
    if await cl.check_source(source) is False:
        raise HTTPException(403, "Forbidden")
    return apiKey


# 5. Inject the check_key function to endpoint
@app.get("/consume")
async def consume_key(apiKey=Depends(check_key)):
    return {"job": "done", "apiKey": apiKey}
