"""
This module contains the set of haipproxy2's exceptions.
"""


class HttpError(Exception):
    """Raise when status code >= 400"""


class DownloadException(Exception):
    """A download error happends when downloading a api page"""
