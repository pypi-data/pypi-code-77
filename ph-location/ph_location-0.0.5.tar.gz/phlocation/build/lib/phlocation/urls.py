from django.urls import path

from phlocation.views import RegionListAPIView, DistrictProvinceListAPIView, CityMunicipalityListAPIView, \
    BarangayListAPIView, BarangayRetrieveAPIView

urlpatterns = [
    path(
        '',
        RegionListAPIView.as_view(),
        name='region_list',
    ),
    path(
        '<int:region_code>/',
        DistrictProvinceListAPIView.as_view(),
        name='district_province_list',
    ),
    path(
        '<int:region_code>/<int:province_code>/',
        CityMunicipalityListAPIView.as_view(),
        name='city_municipality_list',
    ),
    path(
        '<int:region_code>/<int:province_code>/<int:municipality_code>/',
        BarangayListAPIView.as_view(),
        name='barangay_list',
    ),
    path(
        '<int:region_code>/<int:province_code>/<int:municipality_code>/<int:barangay_code>',
        BarangayRetrieveAPIView.as_view(),
        name='barangay_list',
    ),
]
