"""Urls for the Zinnia tags"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.tags import TagDetail
from zinnia.views.tags import TagList


urlpatterns = [
    path('',
         TagList.as_view(),
         name='tag_list'),
    path('<tag:tag>/',
         TagDetail.as_view(),
         name='tag_detail'),
    path(_('<tag:tag>/page/<int:page>/'),
         TagDetail.as_view(),
         name='tag_detail_paginated'),
]
