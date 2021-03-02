# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.12.00902000014
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnQueue(object):
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
        'access_type': 'str',
        'consumer_ack_propagation_enabled': 'bool',
        'dead_msg_queue': 'str',
        'egress_enabled': 'bool',
        'event_bind_count_threshold': 'EventThreshold',
        'event_msg_spool_usage_threshold': 'EventThreshold',
        'event_reject_low_priority_msg_limit_threshold': 'EventThreshold',
        'ingress_enabled': 'bool',
        'max_bind_count': 'int',
        'max_delivered_unacked_msgs_per_flow': 'int',
        'max_msg_size': 'int',
        'max_msg_spool_usage': 'int',
        'max_redelivery_count': 'int',
        'max_ttl': 'int',
        'msg_vpn_name': 'str',
        'owner': 'str',
        'permission': 'str',
        'queue_name': 'str',
        'reject_low_priority_msg_enabled': 'bool',
        'reject_low_priority_msg_limit': 'int',
        'reject_msg_to_sender_on_discard_behavior': 'str',
        'respect_msg_priority_enabled': 'bool',
        'respect_ttl_enabled': 'bool'
    }

    attribute_map = {
        'access_type': 'accessType',
        'consumer_ack_propagation_enabled': 'consumerAckPropagationEnabled',
        'dead_msg_queue': 'deadMsgQueue',
        'egress_enabled': 'egressEnabled',
        'event_bind_count_threshold': 'eventBindCountThreshold',
        'event_msg_spool_usage_threshold': 'eventMsgSpoolUsageThreshold',
        'event_reject_low_priority_msg_limit_threshold': 'eventRejectLowPriorityMsgLimitThreshold',
        'ingress_enabled': 'ingressEnabled',
        'max_bind_count': 'maxBindCount',
        'max_delivered_unacked_msgs_per_flow': 'maxDeliveredUnackedMsgsPerFlow',
        'max_msg_size': 'maxMsgSize',
        'max_msg_spool_usage': 'maxMsgSpoolUsage',
        'max_redelivery_count': 'maxRedeliveryCount',
        'max_ttl': 'maxTtl',
        'msg_vpn_name': 'msgVpnName',
        'owner': 'owner',
        'permission': 'permission',
        'queue_name': 'queueName',
        'reject_low_priority_msg_enabled': 'rejectLowPriorityMsgEnabled',
        'reject_low_priority_msg_limit': 'rejectLowPriorityMsgLimit',
        'reject_msg_to_sender_on_discard_behavior': 'rejectMsgToSenderOnDiscardBehavior',
        'respect_msg_priority_enabled': 'respectMsgPriorityEnabled',
        'respect_ttl_enabled': 'respectTtlEnabled'
    }

    def __init__(self, access_type=None, consumer_ack_propagation_enabled=None, dead_msg_queue=None, egress_enabled=None, event_bind_count_threshold=None, event_msg_spool_usage_threshold=None, event_reject_low_priority_msg_limit_threshold=None, ingress_enabled=None, max_bind_count=None, max_delivered_unacked_msgs_per_flow=None, max_msg_size=None, max_msg_spool_usage=None, max_redelivery_count=None, max_ttl=None, msg_vpn_name=None, owner=None, permission=None, queue_name=None, reject_low_priority_msg_enabled=None, reject_low_priority_msg_limit=None, reject_msg_to_sender_on_discard_behavior=None, respect_msg_priority_enabled=None, respect_ttl_enabled=None):  # noqa: E501
        """MsgVpnQueue - a model defined in Swagger"""  # noqa: E501

        self._access_type = None
        self._consumer_ack_propagation_enabled = None
        self._dead_msg_queue = None
        self._egress_enabled = None
        self._event_bind_count_threshold = None
        self._event_msg_spool_usage_threshold = None
        self._event_reject_low_priority_msg_limit_threshold = None
        self._ingress_enabled = None
        self._max_bind_count = None
        self._max_delivered_unacked_msgs_per_flow = None
        self._max_msg_size = None
        self._max_msg_spool_usage = None
        self._max_redelivery_count = None
        self._max_ttl = None
        self._msg_vpn_name = None
        self._owner = None
        self._permission = None
        self._queue_name = None
        self._reject_low_priority_msg_enabled = None
        self._reject_low_priority_msg_limit = None
        self._reject_msg_to_sender_on_discard_behavior = None
        self._respect_msg_priority_enabled = None
        self._respect_ttl_enabled = None
        self.discriminator = None

        if access_type is not None:
            self.access_type = access_type
        if consumer_ack_propagation_enabled is not None:
            self.consumer_ack_propagation_enabled = consumer_ack_propagation_enabled
        if dead_msg_queue is not None:
            self.dead_msg_queue = dead_msg_queue
        if egress_enabled is not None:
            self.egress_enabled = egress_enabled
        if event_bind_count_threshold is not None:
            self.event_bind_count_threshold = event_bind_count_threshold
        if event_msg_spool_usage_threshold is not None:
            self.event_msg_spool_usage_threshold = event_msg_spool_usage_threshold
        if event_reject_low_priority_msg_limit_threshold is not None:
            self.event_reject_low_priority_msg_limit_threshold = event_reject_low_priority_msg_limit_threshold
        if ingress_enabled is not None:
            self.ingress_enabled = ingress_enabled
        if max_bind_count is not None:
            self.max_bind_count = max_bind_count
        if max_delivered_unacked_msgs_per_flow is not None:
            self.max_delivered_unacked_msgs_per_flow = max_delivered_unacked_msgs_per_flow
        if max_msg_size is not None:
            self.max_msg_size = max_msg_size
        if max_msg_spool_usage is not None:
            self.max_msg_spool_usage = max_msg_spool_usage
        if max_redelivery_count is not None:
            self.max_redelivery_count = max_redelivery_count
        if max_ttl is not None:
            self.max_ttl = max_ttl
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if owner is not None:
            self.owner = owner
        if permission is not None:
            self.permission = permission
        if queue_name is not None:
            self.queue_name = queue_name
        if reject_low_priority_msg_enabled is not None:
            self.reject_low_priority_msg_enabled = reject_low_priority_msg_enabled
        if reject_low_priority_msg_limit is not None:
            self.reject_low_priority_msg_limit = reject_low_priority_msg_limit
        if reject_msg_to_sender_on_discard_behavior is not None:
            self.reject_msg_to_sender_on_discard_behavior = reject_msg_to_sender_on_discard_behavior
        if respect_msg_priority_enabled is not None:
            self.respect_msg_priority_enabled = respect_msg_priority_enabled
        if respect_ttl_enabled is not None:
            self.respect_ttl_enabled = respect_ttl_enabled

    @property
    def access_type(self):
        """Gets the access_type of this MsgVpnQueue.  # noqa: E501

        The access type for delivering messages to consumer flows bound to the Queue. The default value is `\"exclusive\"`. The allowed values and their meaning are:  <pre> \"exclusive\" - Exclusive delivery of messages to the first bound consumer flow. \"non-exclusive\" - Non-exclusive delivery of messages to all bound consumer flows in a round-robin fashion. </pre>   # noqa: E501

        :return: The access_type of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this MsgVpnQueue.

        The access type for delivering messages to consumer flows bound to the Queue. The default value is `\"exclusive\"`. The allowed values and their meaning are:  <pre> \"exclusive\" - Exclusive delivery of messages to the first bound consumer flow. \"non-exclusive\" - Non-exclusive delivery of messages to all bound consumer flows in a round-robin fashion. </pre>   # noqa: E501

        :param access_type: The access_type of this MsgVpnQueue.  # noqa: E501
        :type: str
        """
        allowed_values = ["exclusive", "non-exclusive"]  # noqa: E501
        if access_type not in allowed_values:
            raise ValueError(
                "Invalid value for `access_type` ({0}), must be one of {1}"  # noqa: E501
                .format(access_type, allowed_values)
            )

        self._access_type = access_type

    @property
    def consumer_ack_propagation_enabled(self):
        """Gets the consumer_ack_propagation_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN. The default value is `true`.  # noqa: E501

        :return: The consumer_ack_propagation_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._consumer_ack_propagation_enabled

    @consumer_ack_propagation_enabled.setter
    def consumer_ack_propagation_enabled(self, consumer_ack_propagation_enabled):
        """Sets the consumer_ack_propagation_enabled of this MsgVpnQueue.

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN. The default value is `true`.  # noqa: E501

        :param consumer_ack_propagation_enabled: The consumer_ack_propagation_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._consumer_ack_propagation_enabled = consumer_ack_propagation_enabled

    @property
    def dead_msg_queue(self):
        """Gets the dead_msg_queue of this MsgVpnQueue.  # noqa: E501

        The name of the Dead Message Queue (DMQ) used by the Queue. The default value is `\"#DEAD_MSG_QUEUE\"`.  # noqa: E501

        :return: The dead_msg_queue of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._dead_msg_queue

    @dead_msg_queue.setter
    def dead_msg_queue(self, dead_msg_queue):
        """Sets the dead_msg_queue of this MsgVpnQueue.

        The name of the Dead Message Queue (DMQ) used by the Queue. The default value is `\"#DEAD_MSG_QUEUE\"`.  # noqa: E501

        :param dead_msg_queue: The dead_msg_queue of this MsgVpnQueue.  # noqa: E501
        :type: str
        """

        self._dead_msg_queue = dead_msg_queue

    @property
    def egress_enabled(self):
        """Gets the egress_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the transmission of messages from the Queue. The default value is `false`.  # noqa: E501

        :return: The egress_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._egress_enabled

    @egress_enabled.setter
    def egress_enabled(self, egress_enabled):
        """Sets the egress_enabled of this MsgVpnQueue.

        Enable or disable the transmission of messages from the Queue. The default value is `false`.  # noqa: E501

        :param egress_enabled: The egress_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._egress_enabled = egress_enabled

    @property
    def event_bind_count_threshold(self):
        """Gets the event_bind_count_threshold of this MsgVpnQueue.  # noqa: E501


        :return: The event_bind_count_threshold of this MsgVpnQueue.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_bind_count_threshold

    @event_bind_count_threshold.setter
    def event_bind_count_threshold(self, event_bind_count_threshold):
        """Sets the event_bind_count_threshold of this MsgVpnQueue.


        :param event_bind_count_threshold: The event_bind_count_threshold of this MsgVpnQueue.  # noqa: E501
        :type: EventThreshold
        """

        self._event_bind_count_threshold = event_bind_count_threshold

    @property
    def event_msg_spool_usage_threshold(self):
        """Gets the event_msg_spool_usage_threshold of this MsgVpnQueue.  # noqa: E501


        :return: The event_msg_spool_usage_threshold of this MsgVpnQueue.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_msg_spool_usage_threshold

    @event_msg_spool_usage_threshold.setter
    def event_msg_spool_usage_threshold(self, event_msg_spool_usage_threshold):
        """Sets the event_msg_spool_usage_threshold of this MsgVpnQueue.


        :param event_msg_spool_usage_threshold: The event_msg_spool_usage_threshold of this MsgVpnQueue.  # noqa: E501
        :type: EventThreshold
        """

        self._event_msg_spool_usage_threshold = event_msg_spool_usage_threshold

    @property
    def event_reject_low_priority_msg_limit_threshold(self):
        """Gets the event_reject_low_priority_msg_limit_threshold of this MsgVpnQueue.  # noqa: E501


        :return: The event_reject_low_priority_msg_limit_threshold of this MsgVpnQueue.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_reject_low_priority_msg_limit_threshold

    @event_reject_low_priority_msg_limit_threshold.setter
    def event_reject_low_priority_msg_limit_threshold(self, event_reject_low_priority_msg_limit_threshold):
        """Sets the event_reject_low_priority_msg_limit_threshold of this MsgVpnQueue.


        :param event_reject_low_priority_msg_limit_threshold: The event_reject_low_priority_msg_limit_threshold of this MsgVpnQueue.  # noqa: E501
        :type: EventThreshold
        """

        self._event_reject_low_priority_msg_limit_threshold = event_reject_low_priority_msg_limit_threshold

    @property
    def ingress_enabled(self):
        """Gets the ingress_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the reception of messages to the Queue. The default value is `false`.  # noqa: E501

        :return: The ingress_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._ingress_enabled

    @ingress_enabled.setter
    def ingress_enabled(self, ingress_enabled):
        """Sets the ingress_enabled of this MsgVpnQueue.

        Enable or disable the reception of messages to the Queue. The default value is `false`.  # noqa: E501

        :param ingress_enabled: The ingress_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._ingress_enabled = ingress_enabled

    @property
    def max_bind_count(self):
        """Gets the max_bind_count of this MsgVpnQueue.  # noqa: E501

        The maximum number of consumer flows that can bind to the Queue. The default value is `1000`.  # noqa: E501

        :return: The max_bind_count of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_bind_count

    @max_bind_count.setter
    def max_bind_count(self, max_bind_count):
        """Sets the max_bind_count of this MsgVpnQueue.

        The maximum number of consumer flows that can bind to the Queue. The default value is `1000`.  # noqa: E501

        :param max_bind_count: The max_bind_count of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_bind_count = max_bind_count

    @property
    def max_delivered_unacked_msgs_per_flow(self):
        """Gets the max_delivered_unacked_msgs_per_flow of this MsgVpnQueue.  # noqa: E501

        The maximum number of messages delivered but not acknowledged per flow for the Queue. The default is the max value supported by the platform.  # noqa: E501

        :return: The max_delivered_unacked_msgs_per_flow of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_delivered_unacked_msgs_per_flow

    @max_delivered_unacked_msgs_per_flow.setter
    def max_delivered_unacked_msgs_per_flow(self, max_delivered_unacked_msgs_per_flow):
        """Sets the max_delivered_unacked_msgs_per_flow of this MsgVpnQueue.

        The maximum number of messages delivered but not acknowledged per flow for the Queue. The default is the max value supported by the platform.  # noqa: E501

        :param max_delivered_unacked_msgs_per_flow: The max_delivered_unacked_msgs_per_flow of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_delivered_unacked_msgs_per_flow = max_delivered_unacked_msgs_per_flow

    @property
    def max_msg_size(self):
        """Gets the max_msg_size of this MsgVpnQueue.  # noqa: E501

        The maximum message size allowed in the Queue, in bytes (B). The default value is `10000000`.  # noqa: E501

        :return: The max_msg_size of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_size

    @max_msg_size.setter
    def max_msg_size(self, max_msg_size):
        """Sets the max_msg_size of this MsgVpnQueue.

        The maximum message size allowed in the Queue, in bytes (B). The default value is `10000000`.  # noqa: E501

        :param max_msg_size: The max_msg_size of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_msg_size = max_msg_size

    @property
    def max_msg_spool_usage(self):
        """Gets the max_msg_spool_usage of this MsgVpnQueue.  # noqa: E501

        The maximum message spool usage allowed by the Queue, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking. The default varies by platform.  # noqa: E501

        :return: The max_msg_spool_usage of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_spool_usage

    @max_msg_spool_usage.setter
    def max_msg_spool_usage(self, max_msg_spool_usage):
        """Sets the max_msg_spool_usage of this MsgVpnQueue.

        The maximum message spool usage allowed by the Queue, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking. The default varies by platform.  # noqa: E501

        :param max_msg_spool_usage: The max_msg_spool_usage of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_msg_spool_usage = max_msg_spool_usage

    @property
    def max_redelivery_count(self):
        """Gets the max_redelivery_count of this MsgVpnQueue.  # noqa: E501

        The maximum number of times the Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever. The default value is `0`.  # noqa: E501

        :return: The max_redelivery_count of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_redelivery_count

    @max_redelivery_count.setter
    def max_redelivery_count(self, max_redelivery_count):
        """Sets the max_redelivery_count of this MsgVpnQueue.

        The maximum number of times the Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever. The default value is `0`.  # noqa: E501

        :param max_redelivery_count: The max_redelivery_count of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_redelivery_count = max_redelivery_count

    @property
    def max_ttl(self):
        """Gets the max_ttl of this MsgVpnQueue.  # noqa: E501

        The maximum time in seconds a message can stay in the Queue when `respectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `maxTtl` configured for the Queue, is exceeded. A value of 0 disables expiry. The default value is `0`.  # noqa: E501

        :return: The max_ttl of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl

    @max_ttl.setter
    def max_ttl(self, max_ttl):
        """Sets the max_ttl of this MsgVpnQueue.

        The maximum time in seconds a message can stay in the Queue when `respectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `maxTtl` configured for the Queue, is exceeded. A value of 0 disables expiry. The default value is `0`.  # noqa: E501

        :param max_ttl: The max_ttl of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._max_ttl = max_ttl

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnQueue.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnQueue.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnQueue.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def owner(self):
        """Gets the owner of this MsgVpnQueue.  # noqa: E501

        The Client Username that owns the Queue and has permission equivalent to `\"delete\"`. The default value is `\"\"`.  # noqa: E501

        :return: The owner of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this MsgVpnQueue.

        The Client Username that owns the Queue and has permission equivalent to `\"delete\"`. The default value is `\"\"`.  # noqa: E501

        :param owner: The owner of this MsgVpnQueue.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def permission(self):
        """Gets the permission of this MsgVpnQueue.  # noqa: E501

        The permission level for all consumers of the Queue, excluding the owner. The default value is `\"no-access\"`. The allowed values and their meaning are:  <pre> \"no-access\" - Disallows all access. \"read-only\" - Read-only access to the messages. \"consume\" - Consume (read and remove) messages. \"modify-topic\" - Consume messages or modify the topic/selector. \"delete\" - Consume messages, modify the topic/selector or delete the Client created endpoint altogether. </pre>   # noqa: E501

        :return: The permission of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """Sets the permission of this MsgVpnQueue.

        The permission level for all consumers of the Queue, excluding the owner. The default value is `\"no-access\"`. The allowed values and their meaning are:  <pre> \"no-access\" - Disallows all access. \"read-only\" - Read-only access to the messages. \"consume\" - Consume (read and remove) messages. \"modify-topic\" - Consume messages or modify the topic/selector. \"delete\" - Consume messages, modify the topic/selector or delete the Client created endpoint altogether. </pre>   # noqa: E501

        :param permission: The permission of this MsgVpnQueue.  # noqa: E501
        :type: str
        """
        allowed_values = ["no-access", "read-only", "consume", "modify-topic", "delete"]  # noqa: E501
        if permission not in allowed_values:
            raise ValueError(
                "Invalid value for `permission` ({0}), must be one of {1}"  # noqa: E501
                .format(permission, allowed_values)
            )

        self._permission = permission

    @property
    def queue_name(self):
        """Gets the queue_name of this MsgVpnQueue.  # noqa: E501

        The name of the Queue.  # noqa: E501

        :return: The queue_name of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """Sets the queue_name of this MsgVpnQueue.

        The name of the Queue.  # noqa: E501

        :param queue_name: The queue_name of this MsgVpnQueue.  # noqa: E501
        :type: str
        """

        self._queue_name = queue_name

    @property
    def reject_low_priority_msg_enabled(self):
        """Gets the reject_low_priority_msg_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the checking of low priority messages against the `rejectLowPriorityMsgLimit`. This may only be enabled if `rejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`. The default value is `false`.  # noqa: E501

        :return: The reject_low_priority_msg_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._reject_low_priority_msg_enabled

    @reject_low_priority_msg_enabled.setter
    def reject_low_priority_msg_enabled(self, reject_low_priority_msg_enabled):
        """Sets the reject_low_priority_msg_enabled of this MsgVpnQueue.

        Enable or disable the checking of low priority messages against the `rejectLowPriorityMsgLimit`. This may only be enabled if `rejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`. The default value is `false`.  # noqa: E501

        :param reject_low_priority_msg_enabled: The reject_low_priority_msg_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._reject_low_priority_msg_enabled = reject_low_priority_msg_enabled

    @property
    def reject_low_priority_msg_limit(self):
        """Gets the reject_low_priority_msg_limit of this MsgVpnQueue.  # noqa: E501

        The number of messages of any priority in the Queue above which low priority messages are not admitted but higher priority messages are allowed. The default value is `0`.  # noqa: E501

        :return: The reject_low_priority_msg_limit of this MsgVpnQueue.  # noqa: E501
        :rtype: int
        """
        return self._reject_low_priority_msg_limit

    @reject_low_priority_msg_limit.setter
    def reject_low_priority_msg_limit(self, reject_low_priority_msg_limit):
        """Sets the reject_low_priority_msg_limit of this MsgVpnQueue.

        The number of messages of any priority in the Queue above which low priority messages are not admitted but higher priority messages are allowed. The default value is `0`.  # noqa: E501

        :param reject_low_priority_msg_limit: The reject_low_priority_msg_limit of this MsgVpnQueue.  # noqa: E501
        :type: int
        """

        self._reject_low_priority_msg_limit = reject_low_priority_msg_limit

    @property
    def reject_msg_to_sender_on_discard_behavior(self):
        """Gets the reject_msg_to_sender_on_discard_behavior of this MsgVpnQueue.  # noqa: E501

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The default value is `\"when-queue-enabled\"`. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :return: The reject_msg_to_sender_on_discard_behavior of this MsgVpnQueue.  # noqa: E501
        :rtype: str
        """
        return self._reject_msg_to_sender_on_discard_behavior

    @reject_msg_to_sender_on_discard_behavior.setter
    def reject_msg_to_sender_on_discard_behavior(self, reject_msg_to_sender_on_discard_behavior):
        """Sets the reject_msg_to_sender_on_discard_behavior of this MsgVpnQueue.

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The default value is `\"when-queue-enabled\"`. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :param reject_msg_to_sender_on_discard_behavior: The reject_msg_to_sender_on_discard_behavior of this MsgVpnQueue.  # noqa: E501
        :type: str
        """
        allowed_values = ["always", "when-queue-enabled", "never"]  # noqa: E501
        if reject_msg_to_sender_on_discard_behavior not in allowed_values:
            raise ValueError(
                "Invalid value for `reject_msg_to_sender_on_discard_behavior` ({0}), must be one of {1}"  # noqa: E501
                .format(reject_msg_to_sender_on_discard_behavior, allowed_values)
            )

        self._reject_msg_to_sender_on_discard_behavior = reject_msg_to_sender_on_discard_behavior

    @property
    def respect_msg_priority_enabled(self):
        """Gets the respect_msg_priority_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the respecting of message priority. When enabled, messages contained in the Queue are delivered in priority order, from 9 (highest) to 0 (lowest). MQTT queues do not support enabling message priority. The default value is `false`. Available since 2.8.  # noqa: E501

        :return: The respect_msg_priority_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._respect_msg_priority_enabled

    @respect_msg_priority_enabled.setter
    def respect_msg_priority_enabled(self, respect_msg_priority_enabled):
        """Sets the respect_msg_priority_enabled of this MsgVpnQueue.

        Enable or disable the respecting of message priority. When enabled, messages contained in the Queue are delivered in priority order, from 9 (highest) to 0 (lowest). MQTT queues do not support enabling message priority. The default value is `false`. Available since 2.8.  # noqa: E501

        :param respect_msg_priority_enabled: The respect_msg_priority_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._respect_msg_priority_enabled = respect_msg_priority_enabled

    @property
    def respect_ttl_enabled(self):
        """Gets the respect_ttl_enabled of this MsgVpnQueue.  # noqa: E501

        Enable or disable the respecting of the time-to-live (TTL) for messages in the Queue. When enabled, expired messages are discarded or moved to the DMQ. The default value is `false`.  # noqa: E501

        :return: The respect_ttl_enabled of this MsgVpnQueue.  # noqa: E501
        :rtype: bool
        """
        return self._respect_ttl_enabled

    @respect_ttl_enabled.setter
    def respect_ttl_enabled(self, respect_ttl_enabled):
        """Sets the respect_ttl_enabled of this MsgVpnQueue.

        Enable or disable the respecting of the time-to-live (TTL) for messages in the Queue. When enabled, expired messages are discarded or moved to the DMQ. The default value is `false`.  # noqa: E501

        :param respect_ttl_enabled: The respect_ttl_enabled of this MsgVpnQueue.  # noqa: E501
        :type: bool
        """

        self._respect_ttl_enabled = respect_ttl_enabled

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
        if issubclass(MsgVpnQueue, dict):
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
        if not isinstance(other, MsgVpnQueue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
