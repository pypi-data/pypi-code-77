from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .server import session


class SameDomainServer(MiddlewareMixin):

    def process_response(self, request, response):
        session.update(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response


class SameDomainClient(MiddlewareMixin):

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if session_key is None:
            return redirect(to='{}/?redirect_url={}/'.format(settings.AUTHENTICATION_SERVER_URL, settings.APP_URL))
