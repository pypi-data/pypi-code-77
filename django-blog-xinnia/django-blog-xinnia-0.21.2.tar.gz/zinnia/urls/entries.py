"""Urls for the Zinnia entries"""
from django.urls import path

from zinnia.views.entries import EntryDetail


urlpatterns = [
    path('<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/',
        EntryDetail.as_view(),
        name='entry_detail'),
]
