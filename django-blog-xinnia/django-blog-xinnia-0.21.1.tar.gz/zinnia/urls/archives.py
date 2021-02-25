"""Urls for the Zinnia archives"""
from django.urls import path

from zinnia.urls import _
from zinnia.views.archives import EntryDay
from zinnia.views.archives import EntryIndex
from zinnia.views.archives import EntryMonth
from zinnia.views.archives import EntryToday
from zinnia.views.archives import EntryWeek
from zinnia.views.archives import EntryYear


index_patterns = [
    path('',
         EntryIndex.as_view(),
         name='entry_archive_index'),
    path(_('page/<int:page>/'),
         EntryIndex.as_view(),
         name='entry_archive_index_paginated')
]

year_patterns = [
    path('<yyyy:year>/',
         EntryYear.as_view(),
         name='entry_archive_year'),
    path(_('<yyyy:year>/page/<int:page>/'),
         EntryYear.as_view(),
         name='entry_archive_year_paginated'),
]

week_patterns = [
    path(_('<yyyy:year>/week/<int:week>/'),
         EntryWeek.as_view(),
         name='entry_archive_week'),
    path(_('<yyyy:year>/week/<int:week>/page/<int:page>/'),
         EntryWeek.as_view(),
         name='entry_archive_week_paginated'),
]

month_patterns = [
    path('<yyyy:year>/<mm:month>/',
         EntryMonth.as_view(),
         name='entry_archive_month'),
    path(_('<yyyy:year>/<mm:month>/page/<int:page>/'),
         EntryMonth.as_view(),
         name='entry_archive_month_paginated'),
]

day_patterns = [
    path('<yyyy:year>/<mm:month>/<dd:day>/',
         EntryDay.as_view(),
         name='entry_archive_day'),
    path(_('<yyyy:year>/<mm:month>/'
           '<dd:day>/page/<int:page>/'),
         EntryDay.as_view(),
         name='entry_archive_day_paginated'),
]

today_patterns = [
    path(_('today/'),
         EntryToday.as_view(),
         name='entry_archive_today'),
    path(_('today/page/<int:page>/'),
         EntryToday.as_view(),
         name='entry_archive_today_paginated'),
]

archive_patterns = (index_patterns + year_patterns +
                    week_patterns + month_patterns +
                    day_patterns + today_patterns)

urlpatterns = archive_patterns
