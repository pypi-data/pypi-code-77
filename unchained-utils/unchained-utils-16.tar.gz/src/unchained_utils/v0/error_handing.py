import logging
import traceback
import os

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse


def unchained_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    response = exception_handler(exc, context)
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN', ''),
        integrations=[DjangoIntegration()]
    )

    if response is not None:
        response.data['status_code'] = response.status_code
    elif isinstance(exc, AssertionError):
        err_data = {'error': str(exc)}
        logging.warning(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=500)
    elif isinstance(exc, IntegrityError):
        err_data = {'error': 'Already exist!'}
        logging.error(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, ObjectDoesNotExist):
        err_data = {'error': 'Doesn\'t exist'}
        logging.warning(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, Exception):
        tb = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        err_data = {'error': f'Something wrong in our side!', 'tb': tb}
        logging.error(tb)
        with sentry_sdk.configure_scope() as scope:
            scope.level = 'error'
            sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=500)

    return response
