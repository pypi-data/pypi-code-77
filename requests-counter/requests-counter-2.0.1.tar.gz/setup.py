# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_counter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'flake8>=3.8.4,<4.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest>=6.2.2,<7.0.0']

setup_kwargs = {
    'name': 'requests-counter',
    'version': '2.0.1',
    'description': 'A tool to monitor the number of HTTP requests through an _apiKey_ in the HTTP Header.',
    'long_description': '# requests-counter\n\nA tool to monitor the number of HTTP requests.\n\nIt uses a key as extra parameter in the HTTP header, and optionally can filter the HTTP request per _source_ (like origin).\n\n\n![ci/cd](https://github.com/Arfius/requests-counter/actions/workflows/request-counter.yml/badge.svg)\n\n#### Use cases\n\nScenario: A Company that sell a Service that is limited by a max amount of requests and/or filtered by source HTTP request parameter.\n\n- As a Company, I want to set a request limit for an _apiKey_and/or by source.\n- As a Company, I want to update/destroy/inspect the status of subscription via api.\n\n### Installation\n\n#### Requirement\n\n Install *redis* or run a docker container as below\n\n```bash\n$> docker run --name test-redis -p6379:6379 -ti redis redis-server --appendonly yes\n```\n\n### Package Installation\n\n```bash\n$> pip install requests-counter\n```\n\n## Usage\n\n### As request counter for fastapi\n\n```python\nfrom fastapi import Depends, FastAPI, HTTPException, Header\n\n# 1. Import the library\nfrom requests_counter.reqcounter import ReqCounter\n\nimport asyncio\napp = FastAPI()\n\n# 2. Create an ReqCounter object with the url to redis instance as parameter\ncl = ReqCounter("redis://localhost")\n\n# 3. populate the Object with a list of tuple (key, max_value)\nasyncio.create_task(cl.setup_api_key([("my-api-key-test", 100)]))\nasyncio.create_task(cl.setup_source(["source1", "source2"]))\n\n\n# 4. Declare a function to be injected into Depends module. \n# It will decrease the max_value for each request. It will raise a 429 HTTPException when max_value is 0.\n# It will raise a 403 HTTPException when source is not in the list.\nasync def check_key(apiKey: str = Header(None), source: str = Header(None)):\n    res = await cl.decrease(apiKey)\n    if res is False:\n        raise HTTPException(400, "User Requests Limit Exceeded")\n    if await cl.check_source(source) is False:\n        raise HTTPException(403, "Forbidden")\n    return apiKey\n\n\n# 5. Inject the check_key function to endpoint\n@app.get("/consume")\nasync def consume_key(apiKey=Depends(check_key)):\n    return {"job": "done", "apiKey": apiKey}\n```\nTo run this example\n```bash\n$> uvicorn requests_counter.example:app --reload --port 8080\n```\n\n### As endpoint \n\nCommand below run the server to interact with your redis instance for\n\n- Destroy a key\n- Update the value (i.e. renewal)\n- Get the status of all keys\n\n\n```bash\n$> uvicorn requests_counter.api:app --reload --port 8080\n```\n\nRun `http://locahost:8080/docs` for documentation.\n',
    'author': 'Alfonso Farruggia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arfius/requests-counter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
