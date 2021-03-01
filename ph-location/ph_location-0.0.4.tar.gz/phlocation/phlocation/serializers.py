from rest_framework.serializers import ModelSerializer

from phlocation.models import PSGC


class PSGCSerializer(ModelSerializer):
    class Meta:
        model = PSGC
        fields = (
            'code',
            'name',
        )
