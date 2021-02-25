"""Urls for the Zinnia categories"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.categories import CategoryDetail
from zinnia.views.categories import CategoryList


urlpatterns = [
    path('',
        CategoryList.as_view(),
        name='category_list'),
    path(_('<path:path>/page/<int:page>/'),
        CategoryDetail.as_view(),
        name='category_detail_paginated'),
    path('<path:path>/',
        CategoryDetail.as_view(),
        name='category_detail'),
]
