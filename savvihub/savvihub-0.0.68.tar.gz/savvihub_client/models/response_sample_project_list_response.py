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


class ResponseSampleProjectListResponse(object):
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
        'end_cursor': 'str',
        'results': 'list[ResponseSampleProject]',
        'start_cursor': 'str',
        'total': 'int'
    }

    attribute_map = {
        'end_cursor': 'end_cursor',
        'results': 'results',
        'start_cursor': 'start_cursor',
        'total': 'total'
    }

    def __init__(self, end_cursor=None, results=None, start_cursor=None, total=None, local_vars_configuration=None):  # noqa: E501
        """ResponseSampleProjectListResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._end_cursor = None
        self._results = None
        self._start_cursor = None
        self._total = None
        self.discriminator = None

        self.end_cursor = end_cursor
        self.results = results
        self.start_cursor = start_cursor
        self.total = total

    @property
    def end_cursor(self):
        """Gets the end_cursor of this ResponseSampleProjectListResponse.  # noqa: E501


        :return: The end_cursor of this ResponseSampleProjectListResponse.  # noqa: E501
        :rtype: str
        """
        return self._end_cursor

    @end_cursor.setter
    def end_cursor(self, end_cursor):
        """Sets the end_cursor of this ResponseSampleProjectListResponse.


        :param end_cursor: The end_cursor of this ResponseSampleProjectListResponse.  # noqa: E501
        :type end_cursor: str
        """

        self._end_cursor = end_cursor

    @property
    def results(self):
        """Gets the results of this ResponseSampleProjectListResponse.  # noqa: E501


        :return: The results of this ResponseSampleProjectListResponse.  # noqa: E501
        :rtype: list[ResponseSampleProject]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this ResponseSampleProjectListResponse.


        :param results: The results of this ResponseSampleProjectListResponse.  # noqa: E501
        :type results: list[ResponseSampleProject]
        """
        if self.local_vars_configuration.client_side_validation and results is None:  # noqa: E501
            raise ValueError("Invalid value for `results`, must not be `None`")  # noqa: E501

        self._results = results

    @property
    def start_cursor(self):
        """Gets the start_cursor of this ResponseSampleProjectListResponse.  # noqa: E501


        :return: The start_cursor of this ResponseSampleProjectListResponse.  # noqa: E501
        :rtype: str
        """
        return self._start_cursor

    @start_cursor.setter
    def start_cursor(self, start_cursor):
        """Sets the start_cursor of this ResponseSampleProjectListResponse.


        :param start_cursor: The start_cursor of this ResponseSampleProjectListResponse.  # noqa: E501
        :type start_cursor: str
        """

        self._start_cursor = start_cursor

    @property
    def total(self):
        """Gets the total of this ResponseSampleProjectListResponse.  # noqa: E501


        :return: The total of this ResponseSampleProjectListResponse.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ResponseSampleProjectListResponse.


        :param total: The total of this ResponseSampleProjectListResponse.  # noqa: E501
        :type total: int
        """
        if self.local_vars_configuration.client_side_validation and total is None:  # noqa: E501
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

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
        if not isinstance(other, ResponseSampleProjectListResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseSampleProjectListResponse):
            return True

        return self.to_dict() != other.to_dict()
