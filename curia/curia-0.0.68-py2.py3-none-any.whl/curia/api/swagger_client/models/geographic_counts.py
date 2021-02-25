# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class GeographicCounts(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'outcome_count_by_zip': 'list[str]',
        'outcome_count_by_state': 'list[str]',
        'intervention_count_by_zip': 'list[str]',
        'intervention_count_by_state': 'list[str]',
        'cohort_count_by_zip': 'list[str]',
        'cohort_count_by_state': 'list[str]'
    }

    attribute_map = {
        'outcome_count_by_zip': 'outcomeCountByZip',
        'outcome_count_by_state': 'outcomeCountByState',
        'intervention_count_by_zip': 'interventionCountByZip',
        'intervention_count_by_state': 'interventionCountByState',
        'cohort_count_by_zip': 'cohortCountByZip',
        'cohort_count_by_state': 'cohortCountByState'
    }

    def __init__(self, outcome_count_by_zip=None, outcome_count_by_state=None, intervention_count_by_zip=None, intervention_count_by_state=None, cohort_count_by_zip=None, cohort_count_by_state=None):  # noqa: E501
        """GeographicCounts - a model defined in Swagger"""  # noqa: E501
        self._outcome_count_by_zip = None
        self._outcome_count_by_state = None
        self._intervention_count_by_zip = None
        self._intervention_count_by_state = None
        self._cohort_count_by_zip = None
        self._cohort_count_by_state = None
        self.discriminator = None
        if outcome_count_by_zip is not None:
            self.outcome_count_by_zip = outcome_count_by_zip
        if outcome_count_by_state is not None:
            self.outcome_count_by_state = outcome_count_by_state
        if intervention_count_by_zip is not None:
            self.intervention_count_by_zip = intervention_count_by_zip
        if intervention_count_by_state is not None:
            self.intervention_count_by_state = intervention_count_by_state
        if cohort_count_by_zip is not None:
            self.cohort_count_by_zip = cohort_count_by_zip
        if cohort_count_by_state is not None:
            self.cohort_count_by_state = cohort_count_by_state

    @property
    def outcome_count_by_zip(self):
        """Gets the outcome_count_by_zip of this GeographicCounts.  # noqa: E501


        :return: The outcome_count_by_zip of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._outcome_count_by_zip

    @outcome_count_by_zip.setter
    def outcome_count_by_zip(self, outcome_count_by_zip):
        """Sets the outcome_count_by_zip of this GeographicCounts.


        :param outcome_count_by_zip: The outcome_count_by_zip of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._outcome_count_by_zip = outcome_count_by_zip

    @property
    def outcome_count_by_state(self):
        """Gets the outcome_count_by_state of this GeographicCounts.  # noqa: E501


        :return: The outcome_count_by_state of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._outcome_count_by_state

    @outcome_count_by_state.setter
    def outcome_count_by_state(self, outcome_count_by_state):
        """Sets the outcome_count_by_state of this GeographicCounts.


        :param outcome_count_by_state: The outcome_count_by_state of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._outcome_count_by_state = outcome_count_by_state

    @property
    def intervention_count_by_zip(self):
        """Gets the intervention_count_by_zip of this GeographicCounts.  # noqa: E501


        :return: The intervention_count_by_zip of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._intervention_count_by_zip

    @intervention_count_by_zip.setter
    def intervention_count_by_zip(self, intervention_count_by_zip):
        """Sets the intervention_count_by_zip of this GeographicCounts.


        :param intervention_count_by_zip: The intervention_count_by_zip of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._intervention_count_by_zip = intervention_count_by_zip

    @property
    def intervention_count_by_state(self):
        """Gets the intervention_count_by_state of this GeographicCounts.  # noqa: E501


        :return: The intervention_count_by_state of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._intervention_count_by_state

    @intervention_count_by_state.setter
    def intervention_count_by_state(self, intervention_count_by_state):
        """Sets the intervention_count_by_state of this GeographicCounts.


        :param intervention_count_by_state: The intervention_count_by_state of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._intervention_count_by_state = intervention_count_by_state

    @property
    def cohort_count_by_zip(self):
        """Gets the cohort_count_by_zip of this GeographicCounts.  # noqa: E501


        :return: The cohort_count_by_zip of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._cohort_count_by_zip

    @cohort_count_by_zip.setter
    def cohort_count_by_zip(self, cohort_count_by_zip):
        """Sets the cohort_count_by_zip of this GeographicCounts.


        :param cohort_count_by_zip: The cohort_count_by_zip of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._cohort_count_by_zip = cohort_count_by_zip

    @property
    def cohort_count_by_state(self):
        """Gets the cohort_count_by_state of this GeographicCounts.  # noqa: E501


        :return: The cohort_count_by_state of this GeographicCounts.  # noqa: E501
        :rtype: list[str]
        """
        return self._cohort_count_by_state

    @cohort_count_by_state.setter
    def cohort_count_by_state(self, cohort_count_by_state):
        """Sets the cohort_count_by_state of this GeographicCounts.


        :param cohort_count_by_state: The cohort_count_by_state of this GeographicCounts.  # noqa: E501
        :type: list[str]
        """

        self._cohort_count_by_state = cohort_count_by_state

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GeographicCounts, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GeographicCounts):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
