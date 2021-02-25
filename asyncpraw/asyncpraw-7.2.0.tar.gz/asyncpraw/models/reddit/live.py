"""Provide the LiveThread class."""
from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, List, Optional, Union

from ...const import API_PATH
from ...util.cache import cachedproperty
from ..list.redditor import RedditorList
from ..listing.generator import ListingGenerator
from ..util import stream_generator
from .base import RedditBase
from .mixins import FullnameMixin
from .redditor import Redditor

if TYPE_CHECKING:  # pragma: no cover
    from .... import asyncpraw


class LiveContributorRelationship:
    """Provide methods to interact with live threads' contributors."""

    @staticmethod
    def _handle_permissions(permissions):
        if permissions is None:
            permissions = {"all"}
        else:
            permissions = set(permissions)
        return ",".join(f"+{x}" for x in permissions)

    def __call__(self) -> AsyncIterator["asyncpraw.models.Redditor"]:
        """Return a :class:`.RedditorList` for live threads' contributors.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            async for contributor in thread.contributor():
                print(contributor)

        """

        async def generator():
            url = API_PATH["live_contributors"].format(id=self.thread.id)
            temp = await self.thread._reddit.get(url)
            redditor_list = temp if isinstance(temp, RedditorList) else temp[0]
            for redditor in redditor_list.children:
                yield redditor

        return generator()

    def __init__(self, thread: "asyncpraw.models.LiveThread"):
        """Create a :class:`.LiveContributorRelationship` instance.

        :param thread: An instance of :class:`.LiveThread`.

        .. note::

            This class should not be initialized directly. Instead obtain an instance
            via: ``thread.contributor`` where ``thread`` is a :class:`.LiveThread`
            instance.

        """
        self.thread = thread

    async def accept_invite(self):
        """Accept an invite to contribute the live thread.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ydwwxneu7vsa")
            await thread.contributor.accept_invite()

        """
        url = API_PATH["live_accept_invite"].format(id=self.thread.id)
        await self.thread._reddit.post(url)

    async def invite(
        self,
        redditor: Union[str, "asyncpraw.models.Redditor"],
        permissions: Optional[List[str]] = None,
    ):
        """Invite a redditor to be a contributor of the live thread.

        :param redditor: A redditor name (e.g., ``"spez"``) or :class:`~.Redditor`
            instance.
        :param permissions: When provided (not ``None``), permissions should be a list
            of strings specifying which subset of permissions to grant. An empty list
            ``[]`` indicates no permissions, and when not provided (``None``), indicates
            full permissions.

        :raises: :class:`.RedditAPIException` if the invitation already exists.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            redditor = await reddit.redditor("spez", lazy=True)

            # "manage" and "settings" permissions
            await thread.contributor.invite(redditor, ["manage", "settings"])

        .. seealso::

            :meth:`.LiveContributorRelationship.remove_invite` to remove the invite for
            redditor.

        """
        url = API_PATH["live_invite"].format(id=self.thread.id)
        data = {
            "name": str(redditor),
            "type": "liveupdate_contributor_invite",
            "permissions": self._handle_permissions(permissions),
        }
        await self.thread._reddit.post(url, data=data)

    async def leave(self):
        """Abdicate the live thread contributor position (use with care).

        Usage:

        .. code-block:: python

            thread = await reddit.live("ydwwxneu7vsa")
            await thread.contributor.leave()

        """
        url = API_PATH["live_leave"].format(id=self.thread.id)
        await self.thread._reddit.post(url)

    async def remove(self, redditor: Union[str, "asyncpraw.models.Redditor"]):
        """Remove the redditor from the live thread contributors.

        :param redditor: A redditor fullname (e.g., ``"t2_1w72"``) or
            :class:`~.Redditor` instance.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            redditor = await reddit.redditor("spez", lazy=True)
            await thread.contributor.remove(redditor)
            await thread.contributor.remove("t2_1w72")  # with fullname

        """
        if isinstance(redditor, Redditor):
            fullname = redditor.fullname
        else:
            fullname = redditor
        data = {"id": fullname}
        url = API_PATH["live_remove_contrib"].format(id=self.thread.id)
        await self.thread._reddit.post(url, data=data)

    async def remove_invite(self, redditor: Union[str, "asyncpraw.models.Redditor"]):
        """Remove the invite for redditor.

        :param redditor: A redditor fullname (e.g., ``"t2_1w72"``) or
            :class:`~.Redditor` instance.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            redditor = await reddit.redditor("spez", lazy=True)
            await thread.contributor.remove_invite(redditor)
            await thread.contributor.remove_invite("t2_1w72")  # with fullname

        .. seealso::

            :meth:`.LiveContributorRelationship.invite` to invite a redditor to be a
            contributor of the live thread.

        """
        if isinstance(redditor, Redditor):
            fullname = redditor.fullname
        else:
            fullname = redditor
        data = {"id": fullname}
        url = API_PATH["live_remove_invite"].format(id=self.thread.id)
        await self.thread._reddit.post(url, data=data)

    async def update(
        self,
        redditor: Union[str, "asyncpraw.models.Redditor"],
        permissions: Optional[List[str]] = None,
    ):
        """Update the contributor permissions for ``redditor``.

        :param redditor: A redditor name (e.g., ``"spez"``) or :class:`~.Redditor`
            instance.
        :param permissions: When provided (not ``None``), permissions should be a list
            of strings specifying which subset of permissions to grant (other
            permissions are removed). An empty list ``[]`` indicates no permissions, and
            when not provided (``None``), indicates full permissions.

        For example, to grant all permissions to the contributor, try:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            await thread.contributor.update("spez")

        To grant ``"access"`` and ``"edit"`` permissions (and to remove other
        permissions), try:

        .. code-block:: python

            await thread.contributor.update("spez", ["access", "edit"])

        To remove all permissions from the contributor, try:

        .. code-block:: python

            await subreddit.moderator.update("spez", [])

        """
        url = API_PATH["live_update_perms"].format(id=self.thread.id)
        data = {
            "name": str(redditor),
            "type": "liveupdate_contributor",
            "permissions": self._handle_permissions(permissions),
        }
        await self.thread._reddit.post(url, data=data)

    async def update_invite(
        self,
        redditor: Union[str, "asyncpraw.models.Redditor"],
        permissions: Optional[List[str]] = None,
    ):
        """Update the contributor invite permissions for ``redditor``.

        :param redditor: A redditor name (e.g., ``"spez"``) or :class:`~.Redditor`
            instance.
        :param permissions: When provided (not ``None``), permissions should be a list
            of strings specifying which subset of permissions to grant (other
            permissions are removed). An empty list ``[]`` indicates no permissions, and
            when not provided (``None``), indicates full permissions.

        For example, to set all permissions to the invitation, try:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            await thread.contributor.update_invite("spez")

        To set "access" and "edit" permissions (and to remove other permissions) to the
        invitation, try:

        .. code-block:: python

            await thread.contributor.update_invite("spez", ["access", "edit"])

        To remove all permissions from the invitation, try:

        .. code-block:: python

            await thread.contributor.update_invite("spez", [])

        """
        url = API_PATH["live_update_perms"].format(id=self.thread.id)
        data = {
            "name": str(redditor),
            "type": "liveupdate_contributor_invite",
            "permissions": self._handle_permissions(permissions),
        }
        await self.thread._reddit.post(url, data=data)


class LiveThread(RedditBase):
    """An individual LiveThread object.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this class.
    Since attributes are dynamically provided (see
    :ref:`determine-available-attributes-of-an-object`), there is not a guarantee that
    these attributes will always be present, nor is this list necessarily complete.

    ==================== =========================================================
    Attribute            Description
    ==================== =========================================================
    ``created_utc``      The creation time of the live thread, in `Unix Time`_.
    ``description``      Description of the live thread, as Markdown.
    ``description_html`` Description of the live thread, as HTML.
    ``id``               The ID of the live thread.
    ``nsfw``             A ``bool`` representing whether or not the live thread is
                         marked as NSFW.
    ==================== =========================================================

    .. _unix time: https://en.wikipedia.org/wiki/Unix_time

    """

    STR_FIELD = "id"

    @cachedproperty
    def contrib(self) -> "asyncpraw.models.reddit.live.LiveThreadContribution":
        """Provide an instance of :class:`.LiveThreadContribution`.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            await thread.contrib.add("### update")

        """
        return LiveThreadContribution(self)

    @cachedproperty
    def contributor(self) -> "asyncpraw.models.reddit.live.LiveContributorRelationship":
        """Provide an instance of :class:`.LiveContributorRelationship`.

        You can call the instance to get a list of contributors which is represented as
        :class:`.RedditorList` instance consists of :class:`.Redditor` instances. Those
        Redditor instances have ``permissions`` attributes as contributors:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            async for contributor in thread.contributor():
                # prints `(Redditor(name="Acidtwist"), [u"all"])`
                print(contributor, contributor.permissions)

        """
        return LiveContributorRelationship(self)

    @cachedproperty
    def stream(self) -> "asyncpraw.models.reddit.live.LiveThreadStream":
        """Provide an instance of :class:`.LiveThreadStream`.

        Streams are used to indefinitely retrieve new updates made to a live thread,
        like:

        .. code-block:: python

            for live_update in reddit.live("ta535s1hq2je").stream.updates():
                print(live_update.body)

        Updates are yielded oldest first as :class:`.LiveUpdate`. Up to 100 historical
        updates will initially be returned. To only retrieve new updates starting from
        when the stream is created, pass ``skip_existing=True``:

        .. code-block:: python

            live_thread = await reddit.live("ta535s1hq2je")
            async for live_update in live_thread.stream.updates(skip_existing=True):
                print(live_update.author)

        """
        return LiveThreadStream(self)

    def __eq__(self, other: Union[str, "asyncpraw.models.LiveThread"]) -> bool:
        """Return whether the other instance equals the current.

        .. note::

            This comparison is case sensitive.

        """
        if isinstance(other, str):
            return other == str(self)
        return isinstance(other, self.__class__) and str(self) == str(other)

    async def get_update(
        self, update_id: str, lazy: bool = False
    ) -> "asyncpraw.models.LiveUpdate":
        """Return a :class:`.LiveUpdate` instance.

        :param update_id: A live update ID, e.g.,
            ``"7827987a-c998-11e4-a0b9-22000b6a88d2"``.
        :param lazy: If True, object is loaded lazily (default: False).

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            update = await thread.get_update("7827987a-c998-11e4-a0b9-22000b6a88d2")
            update.thread  # LiveThread(id="ukaeu1ik4sw5")
            update.id  # "7827987a-c998-11e4-a0b9-22000b6a88d2"
            update.author  # "umbrae"

        If you don't need the object fetched right away (e.g., to utilize a class
        method) you can do:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            update = await thread.get_update("7827987a-c998-11e4-a0b9-22000b6a88d2", lazy=True)
            update.contrib  # LiveUpdateContribution instance

        """
        update = LiveUpdate(self._reddit, self.id, update_id)
        if not lazy:
            await update._fetch()
        return update

    def __hash__(self) -> int:
        """Return the hash of the current instance."""
        return hash(self.__class__.__name__) ^ hash(str(self))

    def __init__(
        self,
        reddit: "asyncpraw.Reddit",
        id: Optional[str] = None,
        _data: Optional[Dict[str, Any]] = None,  # pylint: disable=redefined-builtin
    ):
        """Initialize a lazy :class:`.LiveThread` instance.

        :param reddit: An instance of :class:`.Reddit`.
        :param id: A live thread ID, e.g., ``"ukaeu1ik4sw5"``

        """
        if (id, _data).count(None) != 1:
            raise TypeError("Either `id` or `_data` must be provided.")
        if id:
            self.id = id
        super().__init__(reddit, _data=_data)

    def _fetch_info(self):
        return "liveabout", {"id": self.id}, None

    async def _fetch_data(self):
        name, fields, params = self._fetch_info()
        path = API_PATH[name].format(**fields)
        return await self._reddit.request("GET", path, params)

    async def _fetch(self):
        data = await self._fetch_data()
        data = data["data"]
        other = type(self)(self._reddit, _data=data)
        self.__dict__.update(other.__dict__)
        self._fetched = True

    def discussions(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.Submission"]:
        """Get submissions linking to the thread.

        :param generator_kwargs: keyword arguments passed to :class:`.ListingGenerator`
            constructor.

        :returns: A :class:`.ListingGenerator` object which yields :class:`.Submission`
            object.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            async for submission in thread.discussions(limit=None):
                print(submission.title)

        """
        url = API_PATH["live_discussions"].format(id=self.id)
        return ListingGenerator(self._reddit, url, **generator_kwargs)

    async def report(self, type: str):  # pylint: disable=redefined-builtin
        """Report the thread violating the Reddit rules.

        :param type: One of ``"spam"``, ``"vote-manipulation"``,
            ``"personal-information"``, ``"sexualizing-minors"``, ``"site-breaking"``.

        Usage:

        .. code-block:: python

            thread = await reddit.live("xyu8kmjvfrww")
            await thread.report("spam")

        """
        url = API_PATH["live_report"].format(id=self.id)
        await self._reddit.post(url, data={"type": type})

    async def updates(
        self, **generator_kwargs: Union[str, int, Dict[str, str]]
    ) -> AsyncIterator["asyncpraw.models.LiveUpdate"]:
        """Return a :class:`.ListingGenerator` yields :class:`.LiveUpdate` s.

        :param generator_kwargs: keyword arguments passed to :class:`.ListingGenerator`
            constructor.

        :returns: A :class:`.ListingGenerator` object which yields :class:`.LiveUpdate`
            object.

        Additional keyword arguments are passed in the initialization of
        :class:`.ListingGenerator`.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            after = "LiveUpdate_fefb3dae-7534-11e6-b259-0ef8c7233633"
            async for submission in thread.updates(limit=5, params={"after": after}):
                print(submission.body)

        """
        url = API_PATH["live_updates"].format(id=self.id)
        async for update in ListingGenerator(self._reddit, url, **generator_kwargs):
            update._thread = self
            yield update


class LiveThreadContribution:
    """Provides a set of contribution functions to a LiveThread."""

    def __init__(self, thread: "asyncpraw.models.LiveThread"):
        """Create an instance of :class:`.LiveThreadContribution`.

        :param thread: An instance of :class:`.LiveThread`.

        This instance can be retrieved through ``thread.contrib`` where thread is a
        :class:`.LiveThread` instance. E.g.,

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            await thread.contrib.add("### update")

        """
        self.thread = thread

    async def add(self, body: str):
        """Add an update to the live thread.

        :param body: The Markdown formatted content for the update.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ydwwxneu7vsa")
            await thread.contrib.add("test `LiveThreadContribution.add()`")

        """
        url = API_PATH["live_add_update"].format(id=self.thread.id)
        await self.thread._reddit.post(url, data={"body": body})

    async def close(self):
        """Close the live thread permanently (cannot be undone).

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            await thread.contrib.close()

        """
        url = API_PATH["live_close"].format(id=self.thread.id)
        await self.thread._reddit.post(url)

    async def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        nsfw: Optional[bool] = None,
        resources: Optional[str] = None,
        **other_settings: Optional[str],
    ):
        """Update settings of the live thread.

        :param title: (Optional) The title of the live thread (default: None).
        :param description: (Optional) The live thread's description (default: None).
        :param nsfw: (Optional) Indicate whether this thread is not safe for work
            (default: None).
        :param resources: (Optional) Markdown formatted information that is useful for
            the live thread (default: None).

        Does nothing if no arguments are provided.

        Each setting will maintain its current value if ``None`` is specified.

        Additional keyword arguments can be provided to handle new settings as Reddit
        introduces them.

        Usage:

        .. code-block:: python

            thread = await reddit.live("xyu8kmjvfrww")

            # update `title` and `nsfw`
            updated_thread = await thread.contrib.update(title=new_title, nsfw=True)

        If Reddit introduces new settings, you must specify ``None`` for the setting you
        want to maintain:

        .. code-block:: python

            # update `nsfw` and maintain new setting `foo`
            await thread.contrib.update(nsfw=True, foo=None)

        """
        settings = {
            "title": title,
            "description": description,
            "nsfw": nsfw,
            "resources": resources,
        }
        settings.update(other_settings)
        if all(value is None for value in settings.values()):
            return
        # get settings from Reddit (not cache)
        thread = LiveThread(self.thread._reddit, self.thread.id)
        await thread._fetch()
        data = {
            key: getattr(thread, key) if value is None else value
            for key, value in settings.items()
        }

        url = API_PATH["live_update_thread"].format(id=self.thread.id)
        await self.thread._reddit.post(url, data=data.copy())
        self.thread._reset_attributes(*data.keys())


class LiveThreadStream:
    """Provides a :class:`.LiveThread` stream.

    Usually used via:

    .. code-block:: python

        for live_update in reddit.live("ta535s1hq2je").stream.updates():
            print(live_update.body)

    """

    def __init__(self, live_thread: "asyncpraw.models.LiveThread"):
        """Create a LiveThreadStream instance.

        :param live_thread: The live thread associated with the stream.

        """
        self.live_thread = live_thread

    def updates(
        self, **stream_options: Dict[str, Any]
    ) -> AsyncIterator["asyncpraw.models.LiveUpdate"]:
        """Yield new updates to the live thread as they become available.

        :param skip_existing: Set to ``True`` to only fetch items created after the
            stream (default: ``False``).

        As with :meth:`.LiveThread.updates()`, updates are yielded as
        :class:`.LiveUpdate`.

        Updates are yielded oldest first. Up to 100 historical updates will initially be
        returned.

        Keyword arguments are passed to :func:`.stream_generator`.

        For example, to retrieve all new updates made to the ``"ta535s1hq2je"`` live
        thread, try:

        .. code-block:: python

            live_thread = await reddit.live("ta535s1hq2je")
            async for live_update in live.stream.updates():
                print(live_update.body)

        To only retrieve new updates starting from when the stream is created, pass
        ``skip_existing=True``:

        .. code-block:: python

            live_thread = await reddit.live("ta535s1hq2je")
            async for live_update in live_thread.stream.updates(skip_existing=True):
                print(live_update.author)

        """
        return stream_generator(self.live_thread.updates, **stream_options)


class LiveUpdate(FullnameMixin, RedditBase):
    """An individual :class:`.LiveUpdate` object.

    **Typical Attributes**

    This table describes attributes that typically belong to objects of this class.
    Since attributes are dynamically provided (see
    :ref:`determine-available-attributes-of-an-object`), there is not a guarantee that
    these attributes will always be present, nor is this list necessarily complete.

    =============== ===================================================================
    Attribute       Description
    =============== ===================================================================
    ``author``      The :class:`.Redditor` who made the update.
    ``body``        Body of the update, as Markdown.
    ``body_html``   Body of the update, as HTML.
    ``created_utc`` The time the update was created, as `Unix Time`_.
    ``stricken``    A ``bool`` representing whether or not the update was stricken (see
                    :meth:`.strike`).
    =============== ===================================================================

    .. _unix time: https://en.wikipedia.org/wiki/Unix_time

    """

    STR_FIELD = "id"
    _kind = "LiveUpdate"

    @cachedproperty
    def contrib(self) -> "asyncpraw.models.reddit.live.LiveUpdateContribution":
        """Provide an instance of :class:`.LiveUpdateContribution`.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            update = await thread.get_update("7827987a-c998-11e4-a0b9-22000b6a88d2", lazy=True)
            update.contrib  # LiveUpdateContribution instance

        """
        return LiveUpdateContribution(self)

    @property
    def thread(self) -> LiveThread:
        """Return :class:`.LiveThread` object the update object belongs to."""
        return self._thread

    def __init__(
        self,
        reddit: "asyncpraw.Reddit",
        thread_id: Optional[str] = None,
        update_id: Optional[str] = None,
        _data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a lazy :class:`.LiveUpdate` instance.

        Either ``thread_id`` and ``update_id``, or ``_data`` must be provided.

        :param reddit: An instance of :class:`.Reddit`.
        :param thread_id: A live thread ID, e.g., ``"ukaeu1ik4sw5"``.
        :param update_id: A live update ID, e.g.,
            ``"7827987a-c998-11e4-a0b9-22000b6a88d2"``.

        Usage:

        .. code-block:: python

            update = LiveUpdate(reddit, "ukaeu1ik4sw5", "7827987a-c998-11e4-a0b9-22000b6a88d2")
            await update.load()
            update.thread  # LiveThread(id="ukaeu1ik4sw5")
            update.id  # "7827987a-c998-11e4-a0b9-22000b6a88d2"
            update.author  # "umbrae"

        """
        if _data is not None:
            # Since _data (part of JSON returned from reddit) have no thread ID,
            # self._thread must be set by the caller of LiveUpdate(). See the code of
            # LiveThread.updates() for example.
            super().__init__(reddit, _data=_data, _fetched=True)
        elif thread_id and update_id:
            self.id = update_id
            super().__init__(reddit, _data=None)
            self._thread = LiveThread(self._reddit, thread_id)
        else:
            raise TypeError(
                "Either `thread_id` and `update_id`, or `_data` must be provided."
            )

    def __setattr__(self, attribute: str, value: Any):
        """Objectify author."""
        if attribute == "author":
            value = Redditor(self._reddit, name=value)
        super().__setattr__(attribute, value)

    async def _fetch(self):
        url = API_PATH["live_focus"].format(thread_id=self.thread.id, update_id=self.id)
        response = await self._reddit.get(url)
        other = response[0]
        self.__dict__.update(other.__dict__)
        self._fetched = True


class LiveUpdateContribution:
    """Provides a set of contribution functions to LiveUpdate."""

    def __init__(self, update: "asyncpraw.models.LiveUpdate"):
        """Create an instance of :class:`.LiveUpdateContribution`.

        :param update: An instance of :class:`.LiveUpdate`.

        This instance can be retrieved through ``update.contrib`` where update is a
        :class:`.LiveUpdate` instance. E.g.,

        .. code-block:: python

            thread = await reddit.live("ukaeu1ik4sw5")
            update = await thread.get_update("7827987a-c998-11e4-a0b9-22000b6a88d2")
            update.contrib  # LiveUpdateContribution instance
            await update.contrib.remove()

        """
        self.update = update

    async def remove(self):
        """Remove a live update.

        Usage:

        .. code-block:: python

            thread = await reddit.live("ydwwxneu7vsa")
            update = await thread.get_update("6854605a-efec-11e6-b0c7-0eafac4ff094")
            await update.contrib.remove()

        """
        url = API_PATH["live_remove_update"].format(id=self.update.thread.id)
        data = {"id": self.update.fullname}
        await self.update.thread._reddit.post(url, data=data)

    async def strike(self):
        """Strike a content of a live update.

        .. code-block:: python

            thread = await reddit.live("xyu8kmjvfrww")
            update = await thread.get_update("cb5fe532-dbee-11e6-9a91-0e6d74fabcc4")
            await update.contrib.strike()

        To check whether the update is stricken or not, use ``update.stricken``
        attribute.

        .. note::

            Accessing lazy attributes on updates (includes ``update.stricken``) may
            raise :py:class:`AttributeError`. See :class:`.LiveUpdate` for details.

        """
        url = API_PATH["live_strike"].format(id=self.update.thread.id)
        data = {"id": self.update.fullname}
        await self.update.thread._reddit.post(url, data=data)
