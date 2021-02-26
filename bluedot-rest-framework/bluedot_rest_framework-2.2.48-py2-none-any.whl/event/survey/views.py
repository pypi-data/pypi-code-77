from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.event.survey.models import SurveyUser
from bluedot_rest_framework.event.survey.serializers import SurveyUserSerializer
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler, jwt_get_userid_handler


class SurveyUserView(CustomModelViewSet):
    model_class = SurveyUser
    serializer_class = SurveyUserSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        }
    }
