# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from savvihub_client.configuration import Configuration


class SignInCliConfirmAPI(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'cli_token': 'str'
    }

    attribute_map = {
        'cli_token': 'cli_token'
    }

    def __init__(self, cli_token=None, local_vars_configuration=None):  # noqa: E501
        """SignInCliConfirmAPI - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cli_token = None
        self.discriminator = None

        if cli_token is not None:
            self.cli_token = cli_token

    @property
    def cli_token(self):
        """Gets the cli_token of this SignInCliConfirmAPI.  # noqa: E501


        :return: The cli_token of this SignInCliConfirmAPI.  # noqa: E501
        :rtype: str
        """
        return self._cli_token

    @cli_token.setter
    def cli_token(self, cli_token):
        """Sets the cli_token of this SignInCliConfirmAPI.


        :param cli_token: The cli_token of this SignInCliConfirmAPI.  # noqa: E501
        :type cli_token: str
        """

        self._cli_token = cli_token

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SignInCliConfirmAPI):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SignInCliConfirmAPI):
            return True

        return self.to_dict() != other.to_dict()
