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


class AccountSignInCliCheckResponse(object):
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
        'access_token': 'str',
        'signin_success': 'bool'
    }

    attribute_map = {
        'access_token': 'access_token',
        'signin_success': 'signin_success'
    }

    def __init__(self, access_token=None, signin_success=None, local_vars_configuration=None):  # noqa: E501
        """AccountSignInCliCheckResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._access_token = None
        self._signin_success = None
        self.discriminator = None

        self.access_token = access_token
        self.signin_success = signin_success

    @property
    def access_token(self):
        """Gets the access_token of this AccountSignInCliCheckResponse.  # noqa: E501


        :return: The access_token of this AccountSignInCliCheckResponse.  # noqa: E501
        :rtype: str
        """
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        """Sets the access_token of this AccountSignInCliCheckResponse.


        :param access_token: The access_token of this AccountSignInCliCheckResponse.  # noqa: E501
        :type access_token: str
        """
        if self.local_vars_configuration.client_side_validation and access_token is None:  # noqa: E501
            raise ValueError("Invalid value for `access_token`, must not be `None`")  # noqa: E501

        self._access_token = access_token

    @property
    def signin_success(self):
        """Gets the signin_success of this AccountSignInCliCheckResponse.  # noqa: E501


        :return: The signin_success of this AccountSignInCliCheckResponse.  # noqa: E501
        :rtype: bool
        """
        return self._signin_success

    @signin_success.setter
    def signin_success(self, signin_success):
        """Sets the signin_success of this AccountSignInCliCheckResponse.


        :param signin_success: The signin_success of this AccountSignInCliCheckResponse.  # noqa: E501
        :type signin_success: bool
        """
        if self.local_vars_configuration.client_side_validation and signin_success is None:  # noqa: E501
            raise ValueError("Invalid value for `signin_success`, must not be `None`")  # noqa: E501

        self._signin_success = signin_success

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
        if not isinstance(other, AccountSignInCliCheckResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccountSignInCliCheckResponse):
            return True

        return self.to_dict() != other.to_dict()
