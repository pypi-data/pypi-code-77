"""Urls for the Zinnia feeds"""
from django.urls import path

from zinnia.feeds import AuthorEntries
from zinnia.feeds import CategoryEntries
from zinnia.feeds import EntryComments
from zinnia.feeds import EntryDiscussions
from zinnia.feeds import EntryPingbacks
from zinnia.feeds import EntryTrackbacks
from zinnia.feeds import LastDiscussions
from zinnia.feeds import LastEntries
from zinnia.feeds import SearchEntries
from zinnia.feeds import TagEntries
from zinnia.urls import _


urlpatterns = [
    path('',
         LastEntries(),
         name='entry_feed'),
    path(_('discussions/'),
         LastDiscussions(),
         name='discussion_feed'),
    path(_('search/'),
         SearchEntries(),
         name='entry_search_feed'),
    path(_('tags/<tag:tag>/'),
         TagEntries(),
         name='tag_feed'),
    path(_('authors/<username:username>/'),
         AuthorEntries(),
         name='author_feed'),
    path(_('categories/<path:path>/'),
         CategoryEntries(),
         name='category_feed'),
    path(_('discussions/<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/'),
         EntryDiscussions(),
         name='entry_discussion_feed'),
    path(_('comments/<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/'),
         EntryComments(),
         name='entry_comment_feed'),
    path(_('pingbacks/<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/'),
         EntryPingbacks(),
         name='entry_pingback_feed'),
    path(_('trackbacks/<yyyy:year>/<mm:month>/<dd:day>/<slug:slug>/'),
         EntryTrackbacks(),
         name='entry_trackback_feed'),
]
