"""
The below is COMING SOON
"""


from arc.middleware import Middleware
from starlette.requests import Request
import secrets


class SessionHandler:
    def __init__(self, app, secret_key=None):
        self.app = app
        self.lifetime = self.app.to_seconds(1, "hour")

        self.secret_key = secrets.token_urlsafe()

        self._dict = {}

    def init_session(self, response):
        key = secrets.token_urlsafe(50)
        response.set_cookie("secret_key", key+self.secret_key,
                            httponly=True, max_age=self.lifetime)

        self.app.scope["session"][key] = {}

        # self._dict[key] = {}

    def __call__(self, request):
        assert request.cookies.get(
            "secret_key") in self.app.scope["session"], "Session Not Intialized"
        return self.app.scope["session"][request.cookies.get("secret_key")]
        # return self._dict[request.cookies.get("secret_key")]


class SessionMiddleware:
    def __init__(self, app, session):
        self.app = app
        self.session = session

    async def __call__(self, scope, receive, send):
        request = Request(scope=scope, receive=receive)

        response = await self.app.handle_request(request)

        scope["session"] = {}

        await response(scope, receive, send)

    def add(self, middleware_cls, *args):
        if args == []:
            args = None
        self.app = middleware_cls(self.app, *args)

    async def process_request(self, req, res):
        if not req.cookies.get("secret_key"):
            self.session.init_session(res)

    async def process_response(self, req, res):
        if not req.cookies.get("secret_key"):
            self.session.init_session(res)
            
    async def handle_request(self, request):
        response = await self.app.handle_request(request)

        await self.process_request(request, response)

        await self.process_response(request, response)

        return response
