"""Defaults urls for the Zinnia project"""
from django.urls import include, path, register_converter
from django.utils.translation import gettext_lazy

from zinnia.settings import TRANSLATED_URLS
from zinnia import converters


def i18n_url(url, translate=TRANSLATED_URLS):
    """
    Translate or not an URL part.
    """
    if translate:
        return gettext_lazy(url)
    return url


_ = i18n_url

# Register every user URL pattern converters
register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitMonthConverter, 'mm')
register_converter(converters.TwoDigitDayConverter, 'dd')
register_converter(converters.UsernamePathConverter, 'username')
register_converter(converters.PathPathConverter, 'path')
register_converter(converters.TagPathConverter, 'tag')
register_converter(converters.TokenPathConverter, 'token')

app_name = 'zinnia'

urlpatterns = [
    path(_('feeds/'), include('zinnia.urls.feeds')),
    path(_('tags/'), include('zinnia.urls.tags')),
    path(_('authors/'), include('zinnia.urls.authors')),
    path(_('categories/'), include('zinnia.urls.categories')),
    path(_('search/'), include('zinnia.urls.search')),
    path(_('random/'), include('zinnia.urls.random')),
    path(_('sitemap/'), include('zinnia.urls.sitemap')),
    path(_('trackback/'), include('zinnia.urls.trackback')),
    path(_('comments/'), include('zinnia.urls.comments')),
    path('', include('zinnia.urls.entries')),
    path('', include('zinnia.urls.archives')),
    path('', include('zinnia.urls.shortlink')),
    path('', include('zinnia.urls.quick_entry')),
    path('', include('zinnia.urls.capabilities')),
]
