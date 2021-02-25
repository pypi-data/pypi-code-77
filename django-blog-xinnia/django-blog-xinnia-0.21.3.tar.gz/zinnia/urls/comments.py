"""Urls for the Zinnia comments"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.comments import CommentSuccess


urlpatterns = [
    path(_('success/'),
        CommentSuccess.as_view(),
        name='comment_success'),
]
