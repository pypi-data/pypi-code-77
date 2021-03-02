# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the  action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is a hidden maximum as to prevent overloading the system. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.11.00901000201
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnReplayLog(object):
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
        'egress_enabled': 'bool',
        'ingress_enabled': 'bool',
        'max_spool_usage': 'int',
        'msg_spool_usage': 'int',
        'msg_vpn_name': 'str',
        'replay_log_name': 'str'
    }

    attribute_map = {
        'egress_enabled': 'egressEnabled',
        'ingress_enabled': 'ingressEnabled',
        'max_spool_usage': 'maxSpoolUsage',
        'msg_spool_usage': 'msgSpoolUsage',
        'msg_vpn_name': 'msgVpnName',
        'replay_log_name': 'replayLogName'
    }

    def __init__(self, egress_enabled=None, ingress_enabled=None, max_spool_usage=None, msg_spool_usage=None, msg_vpn_name=None, replay_log_name=None):  # noqa: E501
        """MsgVpnReplayLog - a model defined in Swagger"""  # noqa: E501

        self._egress_enabled = None
        self._ingress_enabled = None
        self._max_spool_usage = None
        self._msg_spool_usage = None
        self._msg_vpn_name = None
        self._replay_log_name = None
        self.discriminator = None

        if egress_enabled is not None:
            self.egress_enabled = egress_enabled
        if ingress_enabled is not None:
            self.ingress_enabled = ingress_enabled
        if max_spool_usage is not None:
            self.max_spool_usage = max_spool_usage
        if msg_spool_usage is not None:
            self.msg_spool_usage = msg_spool_usage
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if replay_log_name is not None:
            self.replay_log_name = replay_log_name

    @property
    def egress_enabled(self):
        """Gets the egress_enabled of this MsgVpnReplayLog.  # noqa: E501

        Enable or disable the transmission of messages from the Replay Log.  # noqa: E501

        :return: The egress_enabled of this MsgVpnReplayLog.  # noqa: E501
        :rtype: bool
        """
        return self._egress_enabled

    @egress_enabled.setter
    def egress_enabled(self, egress_enabled):
        """Sets the egress_enabled of this MsgVpnReplayLog.

        Enable or disable the transmission of messages from the Replay Log.  # noqa: E501

        :param egress_enabled: The egress_enabled of this MsgVpnReplayLog.  # noqa: E501
        :type: bool
        """

        self._egress_enabled = egress_enabled

    @property
    def ingress_enabled(self):
        """Gets the ingress_enabled of this MsgVpnReplayLog.  # noqa: E501

        Enable or disable the reception of messages to the Replay Log.  # noqa: E501

        :return: The ingress_enabled of this MsgVpnReplayLog.  # noqa: E501
        :rtype: bool
        """
        return self._ingress_enabled

    @ingress_enabled.setter
    def ingress_enabled(self, ingress_enabled):
        """Sets the ingress_enabled of this MsgVpnReplayLog.

        Enable or disable the reception of messages to the Replay Log.  # noqa: E501

        :param ingress_enabled: The ingress_enabled of this MsgVpnReplayLog.  # noqa: E501
        :type: bool
        """

        self._ingress_enabled = ingress_enabled

    @property
    def max_spool_usage(self):
        """Gets the max_spool_usage of this MsgVpnReplayLog.  # noqa: E501

        The maximum spool usage allowed by the Replay Log, in megabytes (MB). If this limit is exceeded, old messages will be trimmed.  # noqa: E501

        :return: The max_spool_usage of this MsgVpnReplayLog.  # noqa: E501
        :rtype: int
        """
        return self._max_spool_usage

    @max_spool_usage.setter
    def max_spool_usage(self, max_spool_usage):
        """Sets the max_spool_usage of this MsgVpnReplayLog.

        The maximum spool usage allowed by the Replay Log, in megabytes (MB). If this limit is exceeded, old messages will be trimmed.  # noqa: E501

        :param max_spool_usage: The max_spool_usage of this MsgVpnReplayLog.  # noqa: E501
        :type: int
        """

        self._max_spool_usage = max_spool_usage

    @property
    def msg_spool_usage(self):
        """Gets the msg_spool_usage of this MsgVpnReplayLog.  # noqa: E501

        The spool usage of the Replay Log, in bytes (B).  # noqa: E501

        :return: The msg_spool_usage of this MsgVpnReplayLog.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_usage

    @msg_spool_usage.setter
    def msg_spool_usage(self, msg_spool_usage):
        """Sets the msg_spool_usage of this MsgVpnReplayLog.

        The spool usage of the Replay Log, in bytes (B).  # noqa: E501

        :param msg_spool_usage: The msg_spool_usage of this MsgVpnReplayLog.  # noqa: E501
        :type: int
        """

        self._msg_spool_usage = msg_spool_usage

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnReplayLog.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnReplayLog.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnReplayLog.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnReplayLog.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def replay_log_name(self):
        """Gets the replay_log_name of this MsgVpnReplayLog.  # noqa: E501

        The name of the Replay Log.  # noqa: E501

        :return: The replay_log_name of this MsgVpnReplayLog.  # noqa: E501
        :rtype: str
        """
        return self._replay_log_name

    @replay_log_name.setter
    def replay_log_name(self, replay_log_name):
        """Sets the replay_log_name of this MsgVpnReplayLog.

        The name of the Replay Log.  # noqa: E501

        :param replay_log_name: The replay_log_name of this MsgVpnReplayLog.  # noqa: E501
        :type: str
        """

        self._replay_log_name = replay_log_name

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
        if issubclass(MsgVpnReplayLog, dict):
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
        if not isinstance(other, MsgVpnReplayLog):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
