from starlette.requests import Request


class Middleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope=scope, receive=receive)

        response = await self.app.handle_request(request)

        await response(scope, receive, send)

    def add(self, middleware_cls, *args):
        if args == []:
            args = None
        self.app = middleware_cls(self.app, *args)

    async def process_request(self, req):
        pass

    async def process_response(self, req, res):
        pass

    async def handle_request(self, request):
        await self.process_request(request)

        response = await self.app.handle_request(request)
        await self.process_response(request, response)

        return response
