"""
Connection
==========
"""
from .accounts.connection import AccountConnection
from .accounts_users.connection import AccountsUsersConnection
from .crawls.connection import CrawlConnection
from .downloads.connection import DownloadConnection
from .projects.connection import ProjectConnection
from .reports.connection import ReportConnection


class DeepCrawlConnection(
    AccountConnection, ProjectConnection, CrawlConnection, ReportConnection, DownloadConnection,
    AccountsUsersConnection
):
    """Class which contains all connection types

    >>> connection = DeepCrawlConnection("API_ID", "API_KEY", sleep=0.5)
    >>> connection.token
    <token>
    >>> connection = DeepCrawlConnection(token="TOKEN")  # Or set an existing token
    >>> connection.token
    TOKEN

    The sleep arguments represents the time between requests for paginated responses. Default value is 0.5
    """

    __instance = None

    def __init__(self, id_user="", key_pass="", token=None, sleep=0.5, auth_type_user=False):
        super(DeepCrawlConnection, self).__init__(
            id_user, key_pass, token=token, sleep=sleep, auth_type_user=auth_type_user
        )

        DeepCrawlConnection.__instance = self

    @staticmethod
    def get_instance():
        """
        Return the last created connection

        >>> DeepCrawlConnection.get_instance()
        <deepcrawl.DeepCrawlConnection at 0x10583a898>

        :return: The latest created connection
        :rtype: DeepCrawlConnection
        """
        return DeepCrawlConnection.__instance
