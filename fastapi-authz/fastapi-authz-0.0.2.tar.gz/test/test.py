import base64
import binascii
import os
import time

import uvicorn
import casbin
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires, AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser

from fastapi_authz import CasbinMiddleware

app = FastAPI()


def get_examples(path):
    examples_path = os.path.split(os.path.realpath(__file__))[0] + "/../examples/"
    return os.path.abspath(examples_path + path)


class BasicAuth(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")
        return AuthCredentials(["authenticated"]), SimpleUser(username)


enforcer = casbin.Enforcer(get_examples("model.conf"), get_examples("policy.csv"))

app.add_middleware(CasbinMiddleware, enforcer=enforcer)
app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())


@app.get('/')
async def main():
    return 'ok'


if __name__ == '__main__':
    uvicorn.run('test:app', debug=True)
