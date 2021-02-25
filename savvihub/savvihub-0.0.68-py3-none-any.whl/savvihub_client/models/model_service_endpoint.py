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


class ModelServiceEndpoint(object):
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
        'endpoint': 'str',
        'health_check_path': 'str',
        'port': 'int'
    }

    attribute_map = {
        'endpoint': 'endpoint',
        'health_check_path': 'health_check_path',
        'port': 'port'
    }

    def __init__(self, endpoint=None, health_check_path=None, port=None, local_vars_configuration=None):  # noqa: E501
        """ModelServiceEndpoint - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._endpoint = None
        self._health_check_path = None
        self._port = None
        self.discriminator = None

        if endpoint is not None:
            self.endpoint = endpoint
        if health_check_path is not None:
            self.health_check_path = health_check_path
        if port is not None:
            self.port = port

    @property
    def endpoint(self):
        """Gets the endpoint of this ModelServiceEndpoint.  # noqa: E501


        :return: The endpoint of this ModelServiceEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint of this ModelServiceEndpoint.


        :param endpoint: The endpoint of this ModelServiceEndpoint.  # noqa: E501
        :type endpoint: str
        """

        self._endpoint = endpoint

    @property
    def health_check_path(self):
        """Gets the health_check_path of this ModelServiceEndpoint.  # noqa: E501


        :return: The health_check_path of this ModelServiceEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._health_check_path

    @health_check_path.setter
    def health_check_path(self, health_check_path):
        """Sets the health_check_path of this ModelServiceEndpoint.


        :param health_check_path: The health_check_path of this ModelServiceEndpoint.  # noqa: E501
        :type health_check_path: str
        """

        self._health_check_path = health_check_path

    @property
    def port(self):
        """Gets the port of this ModelServiceEndpoint.  # noqa: E501


        :return: The port of this ModelServiceEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this ModelServiceEndpoint.


        :param port: The port of this ModelServiceEndpoint.  # noqa: E501
        :type port: int
        """

        self._port = port

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
        if not isinstance(other, ModelServiceEndpoint):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelServiceEndpoint):
            return True

        return self.to_dict() != other.to_dict()
