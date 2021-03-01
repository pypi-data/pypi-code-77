from django.contrib.auth import views
import urllib.parse as urlparse
from urllib.parse import parse_qs
from .server import token

from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


class ServerLogin(views.LoginView):
    template_name = 'django_single_auth/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(to=self.get_success_url(), permanent=True)
        return super(ServerLogin, self).get(self, request, *args, **kwargs)

    def get_success_url(self):
        url = super(ServerLogin, self).get_success_url()
        if self.request.GET.get('redirect_url') is not None:
            if self.request.session.session_key is not None:
                token_key = token.encrypt(self.request.session.session_key)
                parsed = urlparse.urlparse(self.request.GET.get('redirect_url'))
                if parse_qs(parsed.query).get('next') is None:
                    url = self.request.GET.get('redirect_url') + '?token={}'.format(token_key)
                else:
                    url = self.request.GET.get('redirect_url') + '&token={}'.format(token_key)
                print(url)
                return url
            return self.request.GET.get('redirect_url')
        return url


def ClientAuthenticate(request):
    if request.method == 'GET':
        if request.GET.get('token') is not None:
            url = redirect(to=reverse(viewname=settings.LOGIN_REDIRECT_URL))
            if request.GET.get('next') is not None:
                url = redirect(to=request.GET.get('next'))
            try:
                se = Session.objects.get(session_key=token.decrypt(request.GET.get('token')))
                url.set_cookie(
                    settings.SESSION_COOKIE_NAME,
                    se.session_key, max_age=None,
                    expires=None, domain=settings.SESSION_COOKIE_DOMAIN,
                    path=settings.SESSION_COOKIE_PATH,
                    secure=settings.SESSION_COOKIE_SECURE or None,
                    httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
                return url
            except Session.DoesNotExist:
                next_url = '/'
                if request.GET.get('next') is not None:
                    next_url = request.GET.get('next')
                return redirect(to='{}/?redirect_url={}?next={}'.format(settings.AUTHENTICATION_SERVER_URL,
                                                                        settings.APP_URL + reverse(
                                                                            viewname=settings.LOGIN_URL),
                                                                        next_url))
        url = '{}/?redirect_url={}'.format(settings.AUTHENTICATION_SERVER_URL, request.get_raw_uri())
        return redirect(to=url)
    else:
        return HttpResponse('invalid request')
