from rest_framework.generics import ListAPIView, RetrieveAPIView

from phlocation.models import PSGC
from phlocation.serializers import PSGCSerializer


class RegionListAPIView(ListAPIView):
    queryset = PSGC.objects.regions()
    serializer_class = PSGCSerializer


class DistrictProvinceListAPIView(ListAPIView):
    serializer_class = PSGCSerializer

    def get_queryset(self):
        region_code = self.kwargs['region_code']
        return PSGC.objects.districts_provinces(region_code)


class CityMunicipalityListAPIView(ListAPIView):
    serializer_class = PSGCSerializer

    def get_queryset(self):
        province_code = self.kwargs['province_code']
        return PSGC.objects.cities_municipalities(province_code)


class BarangayListAPIView(ListAPIView):
    serializer_class = PSGCSerializer

    def get_queryset(self):
        municipality_code = self.kwargs['municipality_code']
        return PSGC.objects.barangays(municipality_code)


class BarangayRetrieveAPIView(RetrieveAPIView):
    serializer_class = PSGCSerializer

    def get_object(self):
        barangay_code = self.kwargs['barangay_code']
        return PSGC.objects.get(code=barangay_code)
