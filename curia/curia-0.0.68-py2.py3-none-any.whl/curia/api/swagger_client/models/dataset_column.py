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

class DatasetColumn(object):
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
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'metadata': 'str',
        'dataset_id': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'metadata': 'metadata',
        'dataset_id': 'datasetId',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, type=None, metadata=None, dataset_id=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """DatasetColumn - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._type = None
        self._metadata = None
        self._dataset_id = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        self.type = type
        self.metadata = metadata
        self.dataset_id = dataset_id
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this DatasetColumn.  # noqa: E501


        :return: The id of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DatasetColumn.


        :param id: The id of this DatasetColumn.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this DatasetColumn.  # noqa: E501


        :return: The name of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DatasetColumn.


        :param name: The name of this DatasetColumn.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this DatasetColumn.  # noqa: E501


        :return: The type of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DatasetColumn.


        :param type: The type of this DatasetColumn.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def metadata(self):
        """Gets the metadata of this DatasetColumn.  # noqa: E501


        :return: The metadata of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DatasetColumn.


        :param metadata: The metadata of this DatasetColumn.  # noqa: E501
        :type: str
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def dataset_id(self):
        """Gets the dataset_id of this DatasetColumn.  # noqa: E501


        :return: The dataset_id of this DatasetColumn.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this DatasetColumn.


        :param dataset_id: The dataset_id of this DatasetColumn.  # noqa: E501
        :type: str
        """
        if dataset_id is None:
            raise ValueError("Invalid value for `dataset_id`, must not be `None`")  # noqa: E501

        self._dataset_id = dataset_id

    @property
    def created_at(self):
        """Gets the created_at of this DatasetColumn.  # noqa: E501


        :return: The created_at of this DatasetColumn.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DatasetColumn.


        :param created_at: The created_at of this DatasetColumn.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this DatasetColumn.  # noqa: E501


        :return: The updated_at of this DatasetColumn.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DatasetColumn.


        :param updated_at: The updated_at of this DatasetColumn.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this DatasetColumn.  # noqa: E501


        :return: The version of this DatasetColumn.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DatasetColumn.


        :param version: The version of this DatasetColumn.  # noqa: E501
        :type: float
        """

        self._version = version

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
        if issubclass(DatasetColumn, dict):
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
        if not isinstance(other, DatasetColumn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
