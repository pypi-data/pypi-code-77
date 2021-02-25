"""Urls for the Zinnia authors"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.authors import AuthorDetail
from zinnia.views.authors import AuthorList


urlpatterns = [
    path('',
         AuthorList.as_view(),
         name='author_list'),
    path(_('<username:username>/page/<int:page>/'),
         AuthorDetail.as_view(),
         name='author_detail_paginated'),
    path('<username:username>/',
         AuthorDetail.as_view(),
         name='author_detail'),
]
