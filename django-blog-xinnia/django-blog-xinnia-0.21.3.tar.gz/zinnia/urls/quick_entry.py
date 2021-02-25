"""Url for the Zinnia quick entry view"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.quick_entry import QuickEntry


urlpatterns = [
    path(_('quick-entry/'),
         QuickEntry.as_view(),
         name='entry_quick_post'),
]
