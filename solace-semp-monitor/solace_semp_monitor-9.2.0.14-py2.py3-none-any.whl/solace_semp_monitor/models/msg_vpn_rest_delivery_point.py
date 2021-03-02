# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.12.00902000014
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnRestDeliveryPoint(object):
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
        'client_name': 'str',
        'client_profile_name': 'str',
        'enabled': 'bool',
        'last_failure_reason': 'str',
        'last_failure_time': 'int',
        'msg_vpn_name': 'str',
        'rest_delivery_point_name': 'str',
        'time_connections_blocked': 'int',
        'up': 'bool'
    }

    attribute_map = {
        'client_name': 'clientName',
        'client_profile_name': 'clientProfileName',
        'enabled': 'enabled',
        'last_failure_reason': 'lastFailureReason',
        'last_failure_time': 'lastFailureTime',
        'msg_vpn_name': 'msgVpnName',
        'rest_delivery_point_name': 'restDeliveryPointName',
        'time_connections_blocked': 'timeConnectionsBlocked',
        'up': 'up'
    }

    def __init__(self, client_name=None, client_profile_name=None, enabled=None, last_failure_reason=None, last_failure_time=None, msg_vpn_name=None, rest_delivery_point_name=None, time_connections_blocked=None, up=None):  # noqa: E501
        """MsgVpnRestDeliveryPoint - a model defined in Swagger"""  # noqa: E501

        self._client_name = None
        self._client_profile_name = None
        self._enabled = None
        self._last_failure_reason = None
        self._last_failure_time = None
        self._msg_vpn_name = None
        self._rest_delivery_point_name = None
        self._time_connections_blocked = None
        self._up = None
        self.discriminator = None

        if client_name is not None:
            self.client_name = client_name
        if client_profile_name is not None:
            self.client_profile_name = client_profile_name
        if enabled is not None:
            self.enabled = enabled
        if last_failure_reason is not None:
            self.last_failure_reason = last_failure_reason
        if last_failure_time is not None:
            self.last_failure_time = last_failure_time
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if rest_delivery_point_name is not None:
            self.rest_delivery_point_name = rest_delivery_point_name
        if time_connections_blocked is not None:
            self.time_connections_blocked = time_connections_blocked
        if up is not None:
            self.up = up

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The name of the Client for the REST Delivery Point.  # noqa: E501

        :return: The client_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnRestDeliveryPoint.

        The name of the Client for the REST Delivery Point.  # noqa: E501

        :param client_name: The client_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def client_profile_name(self):
        """Gets the client_profile_name of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The name of the Client Profile for the REST Delivery Point.  # noqa: E501

        :return: The client_profile_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: str
        """
        return self._client_profile_name

    @client_profile_name.setter
    def client_profile_name(self, client_profile_name):
        """Sets the client_profile_name of this MsgVpnRestDeliveryPoint.

        The name of the Client Profile for the REST Delivery Point.  # noqa: E501

        :param client_profile_name: The client_profile_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: str
        """

        self._client_profile_name = client_profile_name

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnRestDeliveryPoint.  # noqa: E501

        Indicates whether the REST Delivery Point is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnRestDeliveryPoint.

        Indicates whether the REST Delivery Point is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def last_failure_reason(self):
        """Gets the last_failure_reason of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The reason for the last REST Delivery Point failure.  # noqa: E501

        :return: The last_failure_reason of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: str
        """
        return self._last_failure_reason

    @last_failure_reason.setter
    def last_failure_reason(self, last_failure_reason):
        """Sets the last_failure_reason of this MsgVpnRestDeliveryPoint.

        The reason for the last REST Delivery Point failure.  # noqa: E501

        :param last_failure_reason: The last_failure_reason of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: str
        """

        self._last_failure_reason = last_failure_reason

    @property
    def last_failure_time(self):
        """Gets the last_failure_time of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The timestamp of the last REST Delivery Point failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_failure_time of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: int
        """
        return self._last_failure_time

    @last_failure_time.setter
    def last_failure_time(self, last_failure_time):
        """Sets the last_failure_time of this MsgVpnRestDeliveryPoint.

        The timestamp of the last REST Delivery Point failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_failure_time: The last_failure_time of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: int
        """

        self._last_failure_time = last_failure_time

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnRestDeliveryPoint.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def rest_delivery_point_name(self):
        """Gets the rest_delivery_point_name of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The name of the REST Delivery Point.  # noqa: E501

        :return: The rest_delivery_point_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: str
        """
        return self._rest_delivery_point_name

    @rest_delivery_point_name.setter
    def rest_delivery_point_name(self, rest_delivery_point_name):
        """Sets the rest_delivery_point_name of this MsgVpnRestDeliveryPoint.

        The name of the REST Delivery Point.  # noqa: E501

        :param rest_delivery_point_name: The rest_delivery_point_name of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: str
        """

        self._rest_delivery_point_name = rest_delivery_point_name

    @property
    def time_connections_blocked(self):
        """Gets the time_connections_blocked of this MsgVpnRestDeliveryPoint.  # noqa: E501

        The percentage of time the REST Delivery Point connections are blocked from transmitting data.  # noqa: E501

        :return: The time_connections_blocked of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: int
        """
        return self._time_connections_blocked

    @time_connections_blocked.setter
    def time_connections_blocked(self, time_connections_blocked):
        """Sets the time_connections_blocked of this MsgVpnRestDeliveryPoint.

        The percentage of time the REST Delivery Point connections are blocked from transmitting data.  # noqa: E501

        :param time_connections_blocked: The time_connections_blocked of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: int
        """

        self._time_connections_blocked = time_connections_blocked

    @property
    def up(self):
        """Gets the up of this MsgVpnRestDeliveryPoint.  # noqa: E501

        Indicates whether the operational state of the REST Delivery Point is up.  # noqa: E501

        :return: The up of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :rtype: bool
        """
        return self._up

    @up.setter
    def up(self, up):
        """Sets the up of this MsgVpnRestDeliveryPoint.

        Indicates whether the operational state of the REST Delivery Point is up.  # noqa: E501

        :param up: The up of this MsgVpnRestDeliveryPoint.  # noqa: E501
        :type: bool
        """

        self._up = up

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
        if issubclass(MsgVpnRestDeliveryPoint, dict):
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
        if not isinstance(other, MsgVpnRestDeliveryPoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
