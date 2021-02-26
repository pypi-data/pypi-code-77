"""
OpenTMI module for Metadata details
"""
from opentmi_client.utils.Base import BaseApi


class Metadata(BaseApi):
    """
    Metadata class
    """

    def append(self, key: str, value: str):
        """
        Setter for test case keywords
        :param key: String
        :param value: String
        """
        self.set(key, value)
