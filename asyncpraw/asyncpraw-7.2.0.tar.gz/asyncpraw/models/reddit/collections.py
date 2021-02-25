"""Provide Collections functionality."""
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Union

from ...const import API_PATH
from ...exceptions import ClientException
from ...util.cache import cachedproperty
from ..base import AsyncPRAWBase
from .base import RedditBase
from .redditor import Redditor
from .submission import Submission
from .subreddit import Subreddit

if TYPE_CHECKING:  # pragma: no cover
    from .... import asyncpraw


class CollectionModeration(AsyncPRAWBase):
    """Class to support moderation actions on a :class:`.Collection`.

    Obtain an instance via:

    .. code-block:: python

        subreddit = await reddit.subreddit("SUBREDDIT")
        collection = await subreddit.collections("some_uuid")
        collection.mod

    """

    def _post_fullname(self, post):
        """Get a post's fullname.

        :param post: A fullname, a Submission, a permalink, or an ID.

        :returns: The fullname of the post.

        """
        if isinstance(post, Submission):
            return post.fullname
        elif not isinstance(post, str):
            raise TypeError(f"Cannot get fullname from object of type {type(post)}.")
        if post.startswith(f"{self._reddit.config.kinds['submission']}_"):
            return post
        try:
            return Submission(self._reddit, url=post).fullname
        except ClientException:
            return Submission(self._reddit, id=post).fullname

    def __init__(self, reddit: "asyncpraw.Reddit", collection_id: str):
        """Initialize an instance of CollectionModeration.

        :param collection_id: The ID of a collection.

        """
        super().__init__(reddit, _data=None)
        self.collection_id = collection_id

    async def add_post(self, submission: "asyncpraw.models.Submission"):
        """Add a post to the collection.

        :param submission: The post to add, a :class:`.Submission`, its permalink as a
            ``str``, its fullname as a ``str``, or its ID as a ``str``.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.add_post("bgibu9")

        .. seealso::

            :meth:`.remove_post`

        """
        link_fullname = self._post_fullname(submission)

        await self._reddit.post(
            API_PATH["collection_add_post"],
            data={"collection_id": self.collection_id, "link_fullname": link_fullname},
        )

    async def delete(self):
        """Delete this collection.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.delete()

        .. seealso::

            :meth:`~.SubredditCollectionsModeration.create`

        """
        await self._reddit.post(
            API_PATH["collection_delete"],
            data={"collection_id": self.collection_id},
        )

    async def remove_post(self, submission: "asyncpraw.models.Submission"):
        """Remove a post from the collection.

        :param submission: The post to remove, a :class:`.Submission`, its permalink as
            a ``str``, its fullname as a ``str``, or its ID as a ``str``.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.remove_post("bgibu9")

        .. seealso::

            :meth:`.add_post`

        """
        link_fullname = self._post_fullname(submission)

        await self._reddit.post(
            API_PATH["collection_remove_post"],
            data={"collection_id": self.collection_id, "link_fullname": link_fullname},
        )

    async def reorder(self, links: List[Union[str, "asyncpraw.models.Submission"]]):
        """Reorder posts in the collection.

        :param links: A ``list`` of submissions, as :class:`.Submission`, permalink as a
            ``str``, fullname as a ``str``, or ID as a ``str``.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            current_order = collection.link_ids
            new_order = reversed(current_order)
            await collection.mod.reorder(new_order)

        """
        link_ids = ",".join([self._post_fullname(post) for post in links])
        await self._reddit.post(
            API_PATH["collection_reorder"],
            data={"collection_id": self.collection_id, "link_ids": link_ids},
        )

    async def update_description(self, description: str):
        """Update the collection's description.

        :param description: The new description.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.update_description("Please enjoy these links")

        .. seealso::

            :meth:`.update_title`

        """
        await self._reddit.post(
            API_PATH["collection_desc"],
            data={"collection_id": self.collection_id, "description": description},
        )

    async def update_title(self, title: str):
        """Update the collection's title.

        :param title: The new title.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.update_title("Titley McTitleface")

        .. seealso::

            :meth:`.update_description`

        """
        await self._reddit.post(
            API_PATH["collection_title"],
            data={"collection_id": self.collection_id, "title": title},
        )


class Collection(RedditBase):
    """Class to represent a Collection.

    Obtain an instance via:

    .. code-block:: python

        subreddit = await reddit.subreddit("SUBREDDIT")
        collection = await subreddit.collections("some_uuid")

    or

    .. code-block:: python

        subreddit = await reddit.subreddit("SUBREDDIT")
        collection = await subreddit.collections(
            permalink="https://reddit.com/r/SUBREDDIT/collection/some_uuid"
        )

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this class.
    Since attributes are dynamically provided (see
    :ref:`determine-available-attributes-of-an-object`), there is not a guarantee that
    these attributes will always be present, nor that they will be the only attributes
    present.

    =================== =============================================================
    Attribute           Description
    =================== =============================================================
    ``author``          The :class:`.Redditor` who created the collection.
    ``collection_id``   The UUID of the collection.
    ``created_at_utc``  Time the collection was created, represented in `Unix Time`_.
    ``description``     The collection description.
    ``last_update_utc`` Time the collection was last updated, represented in `Unix
                        Time`_.
    ``link_ids``        A ``list`` of :class:`.Submission` fullnames.
    ``permalink``       The collection's permalink (to view on the web).
    ``sorted_links``    An iterable listing of the posts in this collection.
    ``title``           The title of the collection.
    =================== =============================================================

    .. _unix time: https://en.wikipedia.org/wiki/Unix_time

    """

    STR_FIELD = "collection_id"

    @cachedproperty
    def mod(self) -> CollectionModeration:
        """Get an instance of :class:`.CollectionModeration`.

        Provides access to various methods, including
        :meth:`~reddit.collections.CollectionModeration.add_post`,
        :meth:`~reddit.collections.CollectionModeration.delete`,
        :meth:`~reddit.collections.CollectionModeration.reorder`, and
        :meth:`~reddit.collections.CollectionModeration.update_title`.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.mod.update_title("My new title!")

        """
        return CollectionModeration(self._reddit, self.collection_id)

    async def subreddit(self) -> "asyncpraw.models.Subreddit":
        """Get the subreddit that this collection belongs to.

        For example:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            print(await collection.subreddit())

        """
        async for subreddit in self._reddit.info([self.subreddit_id]):
            return subreddit

    def __init__(
        self,
        reddit: "asyncpraw.Reddit",
        _data: Dict[str, Any] = None,
        collection_id: Optional[str] = None,
        permalink: Optional[str] = None,
    ):
        """Initialize this collection.

        :param reddit: An instance of :class:`.Reddit`.
        :param _data: Any data associated with the Collection (optional).
        :param collection_id: The ID of the Collection (optional).
        :param permalink: The permalink of the Collection (optional).

        """
        if (_data, collection_id, permalink).count(None) != 2:
            raise TypeError(
                "Exactly one of _data, collection_id, or permalink must be provided."
            )

        if permalink:
            collection_id = self._url_parts(permalink)[4]

        if collection_id:
            self.collection_id = collection_id  # set from _data otherwise

        super().__init__(reddit, _data)

        self._info_params = {
            "collection_id": self.collection_id,
            "include_links": True,
        }

    def __iter__(self) -> Generator[Any, None, None]:
        """Provide a way to iterate over the posts in this Collection.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            for submission in collection:
                print(submission.title, submission.permalink)

        """
        for item in self.sorted_links:
            yield item

    def __len__(self) -> int:
        """Get the number of posts in this Collection.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            print(len(collection))

        """
        return len(self.link_ids)

    def __setattr__(self, attribute: str, value: Any):
        """Objectify author, subreddit, and sorted_links attributes."""
        if attribute == "author_name":
            self.author = Redditor(self._reddit, name=attribute)
        elif attribute == "sorted_links":
            value = self._reddit._objector.objectify(value)
        super().__setattr__(attribute, value)

    def _fetch_info(self):
        return "collection", {}, self._info_params

    async def _fetch_data(self):
        name, fields, params = self._fetch_info()
        path = API_PATH[name].format(**fields)
        return await self._reddit.request("GET", path, params)

    async def _fetch(self):
        data = await self._fetch_data()
        try:
            self._reddit._objector.check_error(data)
        except ClientException:
            # A well-formed but invalid Collections ID during fetch time
            # causes Reddit to return something that looks like an error
            # but with no content.
            raise ClientException(
                f"Error during fetch. Check collection ID {self.collection_id!r} is"
                " correct."
            )

        other = type(self)(self._reddit, _data=data)
        self.__dict__.update(other.__dict__)
        self._fetched = True

    async def follow(self):
        """Follow this Collection.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.follow()

        .. seealso::

            :meth:`~.unfollow`

        """
        await self._reddit.post(
            API_PATH["collection_follow"],
            data={"collection_id": self.collection_id, "follow": True},
        )

    async def unfollow(self):
        """Unfollow this Collection.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            collection = await subreddit.collections("some_uuid")
            await collection.unfollow()

        .. seealso::

            :meth:`~.follow`

        """
        await self._reddit.post(
            API_PATH["collection_follow"],
            data={"collection_id": self.collection_id, "follow": False},
        )


class SubredditCollectionsModeration(AsyncPRAWBase):
    """Class to represent moderator actions on a Subreddit's Collections.

    Obtain an instance via:

    .. code-block:: python

        subreddit = await reddit.subreddit("SUBREDDIT")
        subreddit.collections.mod

    """

    def __init__(
        self,
        reddit: "asyncpraw.Reddit",
        subreddit: "asyncpraw.models.Subreddit",
        _data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the SubredditCollectionsModeration instance."""
        super().__init__(reddit, _data)
        self.subreddit = subreddit

    async def create(self, title: str, description: str):
        """Create a new :class:`.Collection`.

        The authenticated account must have appropriate moderator permissions in the
        subreddit this collection belongs to.

        :param title: The title of the collection, up to 300 characters.
        :param description: The description, up to 500 characters.

        :returns: The newly created :class:`.Collection`.

        Example usage:

        .. code-block:: python

            sub = await reddit.subreddit("SUBREDDIT")
            new_collection = await sub.collections.mod.create("Title", "desc")
            await new_collection.mod.add_post("bgibu9")

        .. seealso::

            :meth:`~CollectionModeration.delete`

        """
        if not self.subreddit._fetched:
            await self.subreddit._fetch()
        return await self._reddit.post(
            API_PATH["collection_create"],
            data={
                "sr_fullname": self.subreddit.fullname,
                "title": title,
                "description": description,
            },
        )


class SubredditCollections(AsyncPRAWBase):
    r"""Class to represent a Subreddit's :class:`.Collection`\ s.

    Obtain an instance via:

    .. code-block:: python

        subreddit = await reddit.subreddit("SUBREDDIT")
        subreddit.collections

    """

    @cachedproperty
    def mod(self) -> SubredditCollectionsModeration:
        """Get an instance of :class:`.SubredditCollectionsModeration`.

        Provides :meth:`~SubredditCollectionsModeration.create`:

        .. code-block:: python

            my_sub = await reddit.subreddit("SUBREDDIT", fetch=True)
            new_collection = await my_sub.collections.mod.create("Title", "desc")

        """
        return SubredditCollectionsModeration(self._reddit, self.subreddit)

    async def __call__(
        self,
        collection_id: Optional[str] = None,
        permalink: Optional[str] = None,
        lazy: bool = False,
    ):
        """Return the :class:`.Collection` with the specified ID.

        :param collection_id: The ID of a Collection (default: None).
        :param permalink: The permalink of a Collection (default: None).
        :param lazy: If True, object is loaded lazily (default: False)

        :returns: The specified Collection.

        Exactly one of ``collection_id`` and ``permalink`` is required.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")

            uuid = "847e4548-a3b5-4ad7-afb4-edbfc2ed0a6b"
            collection = await subreddit.collections(uuid)
            print(collection.title)
            print(collection.description)

            permalink = "https://www.reddit.com/r/SUBREDDIT/collection/" + uuid
            collection = await subreddit.collections(permalink=permalink)
            print(collection.title)
            print(collection.description)

        If you don't need the object fetched right away (e.g., to utilize a class
        method) you can do:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT", fetch=True)
            collection = await subreddit.collections(uuid, lazy=True)
            await collection.mod.add("submission_id")

        """
        if (collection_id is None) == (permalink is None):
            raise TypeError(
                "Exactly one of collection_id or permalink must be provided."
            )
        collection = Collection(
            self._reddit, collection_id=collection_id, permalink=permalink
        )
        if not lazy:
            await collection._fetch()
        return collection

    def __init__(
        self,
        reddit: "asyncpraw.Reddit",
        subreddit: "asyncpraw.models.Subreddit",
        _data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize an instance of SubredditCollections."""
        super().__init__(reddit, _data)
        self.subreddit = subreddit

    async def __aiter__(self):
        r"""Iterate over the Subreddit's :class:`.Collection`\ s.

        Example usage:

        .. code-block:: python

            subreddit = await reddit.subreddit("SUBREDDIT")
            async for collection in subreddit.collections:
                print(collection.permalink)

        """
        if not self.subreddit._fetched:
            await self.subreddit._fetch()
        request = await self._reddit.get(
            API_PATH["collection_subreddit"],
            params={"sr_fullname": self.subreddit.fullname},
        )
        for collection in request:
            yield collection


Subreddit._subreddit_collections_class = SubredditCollections
