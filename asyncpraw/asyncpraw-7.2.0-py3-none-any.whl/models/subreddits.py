"""Provide the Subreddits class."""
from typing import TYPE_CHECKING, AsyncIterator, Dict, List, Optional, Union
from warnings import warn

from ..const import API_PATH
from . import Subreddit
from .base import AsyncPRAWBase
from .listing.generator import ListingGenerator
from .util import stream_generator

if TYPE_CHECKING:  # pragma: no cover
    from ... import asyncpraw


class Subreddits(AsyncPRAWBase):
    """Subreddits is a Listing class that provides various subreddit lists."""

    @staticmethod
    def _to_list(subreddit_list):
        return ",".join([str(x) for x in subreddit_list])

    def default(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return a :class:`.ListingGenerator` for default subreddits.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        """
        return ListingGenerator(
            self._reddit, API_PATH["subreddits_default"], **generator_kwargs
        )

    def gold(self, **generator_kwargs) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Alias for :meth:`.premium` to maintain backwards compatibility."""
        warn(
            "`subreddits.gold` has be renamed to `subreddits.premium`.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.premium(**generator_kwargs)

    def premium(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return a :class:`.ListingGenerator` for premium subreddits.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        """
        return ListingGenerator(
            self._reddit, API_PATH["subreddits_gold"], **generator_kwargs
        )

    def new(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return a :class:`.ListingGenerator` for new subreddits.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        """
        return ListingGenerator(
            self._reddit, API_PATH["subreddits_new"], **generator_kwargs
        )

    def popular(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return a :class:`.ListingGenerator` for popular subreddits.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        """
        return ListingGenerator(
            self._reddit, API_PATH["subreddits_popular"], **generator_kwargs
        )

    async def recommended(
        self,
        subreddits: List[Union[str, "asyncpraw.models.Subreddit"]],
        omit_subreddits: Optional[
            List[Union[str, "asyncpraw.models.Subreddit"]]
        ] = None,
    ) -> List["asyncpraw.models.Subreddit"]:
        """Return subreddits recommended for the given list of subreddits.

        :param subreddits: A list of Subreddit instances and/or subreddit names.
        :param omit_subreddits: A list of Subreddit instances and/or subreddit names to
            exclude from the results (Reddit's end may not work as expected).

        """
        if not isinstance(subreddits, list):
            raise TypeError("subreddits must be a list")
        if omit_subreddits is not None and not isinstance(omit_subreddits, list):
            raise TypeError("omit_subreddits must be a list or None")

        params = {"omit": self._to_list(omit_subreddits or [])}
        url = API_PATH["sub_recommended"].format(subreddits=self._to_list(subreddits))
        return [
            Subreddit(self._reddit, sub["sr_name"])
            for sub in await self._reddit.get(url, params=params)
        ]

    def search(
        self, query: str, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return a :class:`.ListingGenerator` of subreddits matching ``query``.

        Subreddits are searched by both their title and description.

        :param query: The query string to filter subreddits by.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        .. seealso::

            :meth:`~.search_by_name` to search by subreddit names

        """
        self._safely_add_arguments(generator_kwargs, "params", q=query)
        return ListingGenerator(
            self._reddit, API_PATH["subreddits_search"], **generator_kwargs
        )

    async def search_by_name(
        self, query: str, include_nsfw: bool = True, exact: bool = False
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Return list of Subreddits whose names begin with ``query``.

        :param query: Search for subreddits beginning with this string.
        :param include_nsfw: Include subreddits labeled NSFW (default: True).
        :param exact: Return only exact matches to ``query`` (default: False).

        """
        results = await self._reddit.post(
            API_PATH["subreddits_name_search"],
            data={"include_over_18": include_nsfw, "exact": exact, "query": query},
        )
        for result in results["names"]:
            yield await self._reddit.subreddit(result)

    async def search_by_topic(
        self, query: str
    ) -> AsyncIterator[
        "asyncpraw.models.Subreddit"
    ]:  # pragma: no cover; TODO: not currently working
        """Return list of Subreddits whose topics match ``query``.

        :param query: Search for subreddits relevant to the search topic.

        .. note::

            As of 09/01/2020, this endpoint always returns 404.

        """
        results = await self._reddit.get(
            API_PATH["subreddits_by_topic"], params={"query": query}
        )
        for result in results:
            subreddit = await self._reddit.subreddit(result["name"])
            yield subreddit

    def stream(
        self, **stream_options: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Subreddit"]:
        """Yield new subreddits as they are created.

        Subreddits are yielded oldest first. Up to 100 historical subreddits will
        initially be returned.

        Keyword arguments are passed to :func:`.stream_generator`.

        """
        return stream_generator(self.new, **stream_options)
