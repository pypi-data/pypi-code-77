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

    def init_session(self, response) -> None:
        key = secrets.token_urlsafe(50)
        response.set_cookie("secret_key", key+self.secret_key,
                            httponly=True, max_age=self.lifetime)
        self.app.scope["session"] = {}

        self.app.scope["session"][key] = {}

    def __setitem__(self, key: str, value) -> None:
        assert "current_secret" in self.app.scope, "SessionMiddleware not activated"
        
        if self.app.scope["current_secret"] in self.app.scope["session"]:
            self.app.scope["session"][self.app.scope["current_secret"]][key] = value

    def __getitem__(self, key: str):
        assert "current_secret" in self.app.scope, "SessionMiddleware not activated"
        
        if self.app.scope["current_secret"] in self.app.scope["session"]:
            return self.app.scope["session"][self.app.scope["current_secret"]][key]


class SessionMiddleware(Middleware):
    def process_request(self, req):
        self.app.scope["current_secret"] = req.cookies.get("secret_key")
    
    def process_response(self, req, res):
        pass


