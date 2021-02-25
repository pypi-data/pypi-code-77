import calendar
from datetime import datetime, timedelta
from email.utils import formatdate, parsedate_to_datetime

from cachecontrol.heuristics import BaseHeuristic


class OneHourHeuristic(BaseHeuristic):
    def update_headers(self, response):
        try:
            date = parsedate_to_datetime(response.headers["date"])
        except TypeError:
            date = datetime.now()
        expires = date + timedelta(hours=1)
        return {
            "expires": formatdate(calendar.timegm(expires.timetuple())),
            "cache-control": "public",
        }

    def warning(self, _):
        msg = "Automatically cached! Response is Stale."
        return '110 - "%s"' % msg
