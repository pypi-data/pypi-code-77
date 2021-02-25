"""Urls for the zinnia capabilities"""
from django.urls import path

from zinnia.views.capabilities import HumansTxt
from zinnia.views.capabilities import OpenSearchXml
from zinnia.views.capabilities import RsdXml
from zinnia.views.capabilities import WLWManifestXml


urlpatterns = [
    path('rsd.xml', RsdXml.as_view(),
         name='rsd'),
    path('humans.txt', HumansTxt.as_view(),
         name='humans'),
    path('opensearch.xml', OpenSearchXml.as_view(),
         name='opensearch'),
    path('wlwmanifest.xml', WLWManifestXml.as_view(),
         name='wlwmanifest'),
]
