from django.utils.deprecation import MiddlewareMixin
from .server import session
import urllib.parse as urlparse
from urllib.parse import parse_qs


class SameDomainServer(MiddlewareMixin):

    def process_response(self, request, response):
        try:
            parsed = urlparse.urlparse(response.url)
            if parse_qs(parsed.query).get('token') is not None:
                session.update(request)
        except:
            pass
        return response
