# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.19
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnQueueMsg(object):
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
        'attachment_size': 'int',
        'content_size': 'int',
        'dmq_eligible': 'bool',
        'expiry_time': 'int',
        'msg_id': 'int',
        'msg_vpn_name': 'str',
        'priority': 'int',
        'publisher_id': 'int',
        'queue_name': 'str',
        'redelivery_count': 'int',
        'replicated_mate_msg_id': 'int',
        'replication_state': 'str',
        'spooled_time': 'int',
        'undelivered': 'bool'
    }

    attribute_map = {
        'attachment_size': 'attachmentSize',
        'content_size': 'contentSize',
        'dmq_eligible': 'dmqEligible',
        'expiry_time': 'expiryTime',
        'msg_id': 'msgId',
        'msg_vpn_name': 'msgVpnName',
        'priority': 'priority',
        'publisher_id': 'publisherId',
        'queue_name': 'queueName',
        'redelivery_count': 'redeliveryCount',
        'replicated_mate_msg_id': 'replicatedMateMsgId',
        'replication_state': 'replicationState',
        'spooled_time': 'spooledTime',
        'undelivered': 'undelivered'
    }

    def __init__(self, attachment_size=None, content_size=None, dmq_eligible=None, expiry_time=None, msg_id=None, msg_vpn_name=None, priority=None, publisher_id=None, queue_name=None, redelivery_count=None, replicated_mate_msg_id=None, replication_state=None, spooled_time=None, undelivered=None):  # noqa: E501
        """MsgVpnQueueMsg - a model defined in Swagger"""  # noqa: E501

        self._attachment_size = None
        self._content_size = None
        self._dmq_eligible = None
        self._expiry_time = None
        self._msg_id = None
        self._msg_vpn_name = None
        self._priority = None
        self._publisher_id = None
        self._queue_name = None
        self._redelivery_count = None
        self._replicated_mate_msg_id = None
        self._replication_state = None
        self._spooled_time = None
        self._undelivered = None
        self.discriminator = None

        if attachment_size is not None:
            self.attachment_size = attachment_size
        if content_size is not None:
            self.content_size = content_size
        if dmq_eligible is not None:
            self.dmq_eligible = dmq_eligible
        if expiry_time is not None:
            self.expiry_time = expiry_time
        if msg_id is not None:
            self.msg_id = msg_id
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if priority is not None:
            self.priority = priority
        if publisher_id is not None:
            self.publisher_id = publisher_id
        if queue_name is not None:
            self.queue_name = queue_name
        if redelivery_count is not None:
            self.redelivery_count = redelivery_count
        if replicated_mate_msg_id is not None:
            self.replicated_mate_msg_id = replicated_mate_msg_id
        if replication_state is not None:
            self.replication_state = replication_state
        if spooled_time is not None:
            self.spooled_time = spooled_time
        if undelivered is not None:
            self.undelivered = undelivered

    @property
    def attachment_size(self):
        """Gets the attachment_size of this MsgVpnQueueMsg.  # noqa: E501

        The size of the Message attachment, in bytes (B).  # noqa: E501

        :return: The attachment_size of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._attachment_size

    @attachment_size.setter
    def attachment_size(self, attachment_size):
        """Sets the attachment_size of this MsgVpnQueueMsg.

        The size of the Message attachment, in bytes (B).  # noqa: E501

        :param attachment_size: The attachment_size of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._attachment_size = attachment_size

    @property
    def content_size(self):
        """Gets the content_size of this MsgVpnQueueMsg.  # noqa: E501

        The size of the Message content, in bytes (B).  # noqa: E501

        :return: The content_size of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._content_size

    @content_size.setter
    def content_size(self, content_size):
        """Sets the content_size of this MsgVpnQueueMsg.

        The size of the Message content, in bytes (B).  # noqa: E501

        :param content_size: The content_size of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._content_size = content_size

    @property
    def dmq_eligible(self):
        """Gets the dmq_eligible of this MsgVpnQueueMsg.  # noqa: E501

        Indicates whether the Message is eligible for the Dead Message Queue (DMQ).  # noqa: E501

        :return: The dmq_eligible of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: bool
        """
        return self._dmq_eligible

    @dmq_eligible.setter
    def dmq_eligible(self, dmq_eligible):
        """Sets the dmq_eligible of this MsgVpnQueueMsg.

        Indicates whether the Message is eligible for the Dead Message Queue (DMQ).  # noqa: E501

        :param dmq_eligible: The dmq_eligible of this MsgVpnQueueMsg.  # noqa: E501
        :type: bool
        """

        self._dmq_eligible = dmq_eligible

    @property
    def expiry_time(self):
        """Gets the expiry_time of this MsgVpnQueueMsg.  # noqa: E501

        The timestamp of when the Message expires. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The expiry_time of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, expiry_time):
        """Sets the expiry_time of this MsgVpnQueueMsg.

        The timestamp of when the Message expires. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param expiry_time: The expiry_time of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._expiry_time = expiry_time

    @property
    def msg_id(self):
        """Gets the msg_id of this MsgVpnQueueMsg.  # noqa: E501

        The identifier (ID) of the Message.  # noqa: E501

        :return: The msg_id of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._msg_id

    @msg_id.setter
    def msg_id(self, msg_id):
        """Sets the msg_id of this MsgVpnQueueMsg.

        The identifier (ID) of the Message.  # noqa: E501

        :param msg_id: The msg_id of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._msg_id = msg_id

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnQueueMsg.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnQueueMsg.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnQueueMsg.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def priority(self):
        """Gets the priority of this MsgVpnQueueMsg.  # noqa: E501

        The priority level of the Message, from 9 (highest) to 0 (lowest).  # noqa: E501

        :return: The priority of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this MsgVpnQueueMsg.

        The priority level of the Message, from 9 (highest) to 0 (lowest).  # noqa: E501

        :param priority: The priority of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def publisher_id(self):
        """Gets the publisher_id of this MsgVpnQueueMsg.  # noqa: E501

        The identifier (ID) of the Message publisher.  # noqa: E501

        :return: The publisher_id of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._publisher_id

    @publisher_id.setter
    def publisher_id(self, publisher_id):
        """Sets the publisher_id of this MsgVpnQueueMsg.

        The identifier (ID) of the Message publisher.  # noqa: E501

        :param publisher_id: The publisher_id of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._publisher_id = publisher_id

    @property
    def queue_name(self):
        """Gets the queue_name of this MsgVpnQueueMsg.  # noqa: E501

        The name of the Queue.  # noqa: E501

        :return: The queue_name of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """Sets the queue_name of this MsgVpnQueueMsg.

        The name of the Queue.  # noqa: E501

        :param queue_name: The queue_name of this MsgVpnQueueMsg.  # noqa: E501
        :type: str
        """

        self._queue_name = queue_name

    @property
    def redelivery_count(self):
        """Gets the redelivery_count of this MsgVpnQueueMsg.  # noqa: E501

        The number of times the Message has been redelivered.  # noqa: E501

        :return: The redelivery_count of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._redelivery_count

    @redelivery_count.setter
    def redelivery_count(self, redelivery_count):
        """Sets the redelivery_count of this MsgVpnQueueMsg.

        The number of times the Message has been redelivered.  # noqa: E501

        :param redelivery_count: The redelivery_count of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._redelivery_count = redelivery_count

    @property
    def replicated_mate_msg_id(self):
        """Gets the replicated_mate_msg_id of this MsgVpnQueueMsg.  # noqa: E501

        The Message identifier (ID) on the replication mate. Applicable only to replicated messages.  # noqa: E501

        :return: The replicated_mate_msg_id of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._replicated_mate_msg_id

    @replicated_mate_msg_id.setter
    def replicated_mate_msg_id(self, replicated_mate_msg_id):
        """Sets the replicated_mate_msg_id of this MsgVpnQueueMsg.

        The Message identifier (ID) on the replication mate. Applicable only to replicated messages.  # noqa: E501

        :param replicated_mate_msg_id: The replicated_mate_msg_id of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._replicated_mate_msg_id = replicated_mate_msg_id

    @property
    def replication_state(self):
        """Gets the replication_state of this MsgVpnQueueMsg.  # noqa: E501

        The replication state of the Message. The allowed values and their meaning are:  <pre> \"replicated\" - The Message is replicated to the remote Message VPN. \"not-replicated\" - The Message is not being replicated to the remote Message VPN. \"pending-replication\" - The Message is queued for replication to the remote Message VPN. </pre>   # noqa: E501

        :return: The replication_state of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: str
        """
        return self._replication_state

    @replication_state.setter
    def replication_state(self, replication_state):
        """Sets the replication_state of this MsgVpnQueueMsg.

        The replication state of the Message. The allowed values and their meaning are:  <pre> \"replicated\" - The Message is replicated to the remote Message VPN. \"not-replicated\" - The Message is not being replicated to the remote Message VPN. \"pending-replication\" - The Message is queued for replication to the remote Message VPN. </pre>   # noqa: E501

        :param replication_state: The replication_state of this MsgVpnQueueMsg.  # noqa: E501
        :type: str
        """

        self._replication_state = replication_state

    @property
    def spooled_time(self):
        """Gets the spooled_time of this MsgVpnQueueMsg.  # noqa: E501

        The timestamp of when the Message was spooled in the Queue. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The spooled_time of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: int
        """
        return self._spooled_time

    @spooled_time.setter
    def spooled_time(self, spooled_time):
        """Sets the spooled_time of this MsgVpnQueueMsg.

        The timestamp of when the Message was spooled in the Queue. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param spooled_time: The spooled_time of this MsgVpnQueueMsg.  # noqa: E501
        :type: int
        """

        self._spooled_time = spooled_time

    @property
    def undelivered(self):
        """Gets the undelivered of this MsgVpnQueueMsg.  # noqa: E501

        Indicates whether delivery of the Message has never been attempted.  # noqa: E501

        :return: The undelivered of this MsgVpnQueueMsg.  # noqa: E501
        :rtype: bool
        """
        return self._undelivered

    @undelivered.setter
    def undelivered(self, undelivered):
        """Sets the undelivered of this MsgVpnQueueMsg.

        Indicates whether delivery of the Message has never been attempted.  # noqa: E501

        :param undelivered: The undelivered of this MsgVpnQueueMsg.  # noqa: E501
        :type: bool
        """

        self._undelivered = undelivered

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
        if issubclass(MsgVpnQueueMsg, dict):
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
        if not isinstance(other, MsgVpnQueueMsg):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
