"""Urls for the Zinnia entries short link"""
from django.urls import path

from zinnia.views.shortlink import EntryShortLink


urlpatterns = [
    path('<token:token>',
         EntryShortLink.as_view(),
         name='entry_shortlink'),
]
