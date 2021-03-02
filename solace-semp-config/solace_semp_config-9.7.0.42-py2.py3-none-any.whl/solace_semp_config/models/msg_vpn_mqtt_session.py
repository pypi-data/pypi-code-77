# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.18
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnMqttSession(object):
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
        'enabled': 'bool',
        'mqtt_session_client_id': 'str',
        'mqtt_session_virtual_router': 'str',
        'msg_vpn_name': 'str',
        'owner': 'str',
        'queue_consumer_ack_propagation_enabled': 'bool',
        'queue_dead_msg_queue': 'str',
        'queue_event_bind_count_threshold': 'EventThreshold',
        'queue_event_msg_spool_usage_threshold': 'EventThreshold',
        'queue_event_reject_low_priority_msg_limit_threshold': 'EventThreshold',
        'queue_max_bind_count': 'int',
        'queue_max_delivered_unacked_msgs_per_flow': 'int',
        'queue_max_msg_size': 'int',
        'queue_max_msg_spool_usage': 'int',
        'queue_max_redelivery_count': 'int',
        'queue_max_ttl': 'int',
        'queue_reject_low_priority_msg_enabled': 'bool',
        'queue_reject_low_priority_msg_limit': 'int',
        'queue_reject_msg_to_sender_on_discard_behavior': 'str',
        'queue_respect_ttl_enabled': 'bool'
    }

    attribute_map = {
        'enabled': 'enabled',
        'mqtt_session_client_id': 'mqttSessionClientId',
        'mqtt_session_virtual_router': 'mqttSessionVirtualRouter',
        'msg_vpn_name': 'msgVpnName',
        'owner': 'owner',
        'queue_consumer_ack_propagation_enabled': 'queueConsumerAckPropagationEnabled',
        'queue_dead_msg_queue': 'queueDeadMsgQueue',
        'queue_event_bind_count_threshold': 'queueEventBindCountThreshold',
        'queue_event_msg_spool_usage_threshold': 'queueEventMsgSpoolUsageThreshold',
        'queue_event_reject_low_priority_msg_limit_threshold': 'queueEventRejectLowPriorityMsgLimitThreshold',
        'queue_max_bind_count': 'queueMaxBindCount',
        'queue_max_delivered_unacked_msgs_per_flow': 'queueMaxDeliveredUnackedMsgsPerFlow',
        'queue_max_msg_size': 'queueMaxMsgSize',
        'queue_max_msg_spool_usage': 'queueMaxMsgSpoolUsage',
        'queue_max_redelivery_count': 'queueMaxRedeliveryCount',
        'queue_max_ttl': 'queueMaxTtl',
        'queue_reject_low_priority_msg_enabled': 'queueRejectLowPriorityMsgEnabled',
        'queue_reject_low_priority_msg_limit': 'queueRejectLowPriorityMsgLimit',
        'queue_reject_msg_to_sender_on_discard_behavior': 'queueRejectMsgToSenderOnDiscardBehavior',
        'queue_respect_ttl_enabled': 'queueRespectTtlEnabled'
    }

    def __init__(self, enabled=None, mqtt_session_client_id=None, mqtt_session_virtual_router=None, msg_vpn_name=None, owner=None, queue_consumer_ack_propagation_enabled=None, queue_dead_msg_queue=None, queue_event_bind_count_threshold=None, queue_event_msg_spool_usage_threshold=None, queue_event_reject_low_priority_msg_limit_threshold=None, queue_max_bind_count=None, queue_max_delivered_unacked_msgs_per_flow=None, queue_max_msg_size=None, queue_max_msg_spool_usage=None, queue_max_redelivery_count=None, queue_max_ttl=None, queue_reject_low_priority_msg_enabled=None, queue_reject_low_priority_msg_limit=None, queue_reject_msg_to_sender_on_discard_behavior=None, queue_respect_ttl_enabled=None):  # noqa: E501
        """MsgVpnMqttSession - a model defined in Swagger"""  # noqa: E501

        self._enabled = None
        self._mqtt_session_client_id = None
        self._mqtt_session_virtual_router = None
        self._msg_vpn_name = None
        self._owner = None
        self._queue_consumer_ack_propagation_enabled = None
        self._queue_dead_msg_queue = None
        self._queue_event_bind_count_threshold = None
        self._queue_event_msg_spool_usage_threshold = None
        self._queue_event_reject_low_priority_msg_limit_threshold = None
        self._queue_max_bind_count = None
        self._queue_max_delivered_unacked_msgs_per_flow = None
        self._queue_max_msg_size = None
        self._queue_max_msg_spool_usage = None
        self._queue_max_redelivery_count = None
        self._queue_max_ttl = None
        self._queue_reject_low_priority_msg_enabled = None
        self._queue_reject_low_priority_msg_limit = None
        self._queue_reject_msg_to_sender_on_discard_behavior = None
        self._queue_respect_ttl_enabled = None
        self.discriminator = None

        if enabled is not None:
            self.enabled = enabled
        if mqtt_session_client_id is not None:
            self.mqtt_session_client_id = mqtt_session_client_id
        if mqtt_session_virtual_router is not None:
            self.mqtt_session_virtual_router = mqtt_session_virtual_router
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if owner is not None:
            self.owner = owner
        if queue_consumer_ack_propagation_enabled is not None:
            self.queue_consumer_ack_propagation_enabled = queue_consumer_ack_propagation_enabled
        if queue_dead_msg_queue is not None:
            self.queue_dead_msg_queue = queue_dead_msg_queue
        if queue_event_bind_count_threshold is not None:
            self.queue_event_bind_count_threshold = queue_event_bind_count_threshold
        if queue_event_msg_spool_usage_threshold is not None:
            self.queue_event_msg_spool_usage_threshold = queue_event_msg_spool_usage_threshold
        if queue_event_reject_low_priority_msg_limit_threshold is not None:
            self.queue_event_reject_low_priority_msg_limit_threshold = queue_event_reject_low_priority_msg_limit_threshold
        if queue_max_bind_count is not None:
            self.queue_max_bind_count = queue_max_bind_count
        if queue_max_delivered_unacked_msgs_per_flow is not None:
            self.queue_max_delivered_unacked_msgs_per_flow = queue_max_delivered_unacked_msgs_per_flow
        if queue_max_msg_size is not None:
            self.queue_max_msg_size = queue_max_msg_size
        if queue_max_msg_spool_usage is not None:
            self.queue_max_msg_spool_usage = queue_max_msg_spool_usage
        if queue_max_redelivery_count is not None:
            self.queue_max_redelivery_count = queue_max_redelivery_count
        if queue_max_ttl is not None:
            self.queue_max_ttl = queue_max_ttl
        if queue_reject_low_priority_msg_enabled is not None:
            self.queue_reject_low_priority_msg_enabled = queue_reject_low_priority_msg_enabled
        if queue_reject_low_priority_msg_limit is not None:
            self.queue_reject_low_priority_msg_limit = queue_reject_low_priority_msg_limit
        if queue_reject_msg_to_sender_on_discard_behavior is not None:
            self.queue_reject_msg_to_sender_on_discard_behavior = queue_reject_msg_to_sender_on_discard_behavior
        if queue_respect_ttl_enabled is not None:
            self.queue_respect_ttl_enabled = queue_respect_ttl_enabled

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnMqttSession.  # noqa: E501

        Enable or disable the MQTT Session. When disabled, the client is disconnected, new messages matching QoS 0 subscriptions are discarded, and new messages matching QoS 1 subscriptions are stored for future delivery. The default value is `false`.  # noqa: E501

        :return: The enabled of this MsgVpnMqttSession.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnMqttSession.

        Enable or disable the MQTT Session. When disabled, the client is disconnected, new messages matching QoS 0 subscriptions are discarded, and new messages matching QoS 1 subscriptions are stored for future delivery. The default value is `false`.  # noqa: E501

        :param enabled: The enabled of this MsgVpnMqttSession.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def mqtt_session_client_id(self):
        """Gets the mqtt_session_client_id of this MsgVpnMqttSession.  # noqa: E501

        The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet.  # noqa: E501

        :return: The mqtt_session_client_id of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._mqtt_session_client_id

    @mqtt_session_client_id.setter
    def mqtt_session_client_id(self, mqtt_session_client_id):
        """Sets the mqtt_session_client_id of this MsgVpnMqttSession.

        The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet.  # noqa: E501

        :param mqtt_session_client_id: The mqtt_session_client_id of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """

        self._mqtt_session_client_id = mqtt_session_client_id

    @property
    def mqtt_session_virtual_router(self):
        """Gets the mqtt_session_virtual_router of this MsgVpnMqttSession.  # noqa: E501

        The virtual router of the MQTT Session. The allowed values and their meaning are:  <pre> \"primary\" - The MQTT Session belongs to the primary virtual router. \"backup\" - The MQTT Session belongs to the backup virtual router. </pre>   # noqa: E501

        :return: The mqtt_session_virtual_router of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._mqtt_session_virtual_router

    @mqtt_session_virtual_router.setter
    def mqtt_session_virtual_router(self, mqtt_session_virtual_router):
        """Sets the mqtt_session_virtual_router of this MsgVpnMqttSession.

        The virtual router of the MQTT Session. The allowed values and their meaning are:  <pre> \"primary\" - The MQTT Session belongs to the primary virtual router. \"backup\" - The MQTT Session belongs to the backup virtual router. </pre>   # noqa: E501

        :param mqtt_session_virtual_router: The mqtt_session_virtual_router of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """
        allowed_values = ["primary", "backup"]  # noqa: E501
        if mqtt_session_virtual_router not in allowed_values:
            raise ValueError(
                "Invalid value for `mqtt_session_virtual_router` ({0}), must be one of {1}"  # noqa: E501
                .format(mqtt_session_virtual_router, allowed_values)
            )

        self._mqtt_session_virtual_router = mqtt_session_virtual_router

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnMqttSession.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnMqttSession.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def owner(self):
        """Gets the owner of this MsgVpnMqttSession.  # noqa: E501

        The owner of the MQTT Session. For externally-created sessions this defaults to the Client Username of the connecting client. For management-created sessions this defaults to empty. The default value is `\"\"`.  # noqa: E501

        :return: The owner of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this MsgVpnMqttSession.

        The owner of the MQTT Session. For externally-created sessions this defaults to the Client Username of the connecting client. For management-created sessions this defaults to empty. The default value is `\"\"`.  # noqa: E501

        :param owner: The owner of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def queue_consumer_ack_propagation_enabled(self):
        """Gets the queue_consumer_ack_propagation_enabled of this MsgVpnMqttSession.  # noqa: E501

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN. The default value is `true`. Available since 2.14.  # noqa: E501

        :return: The queue_consumer_ack_propagation_enabled of this MsgVpnMqttSession.  # noqa: E501
        :rtype: bool
        """
        return self._queue_consumer_ack_propagation_enabled

    @queue_consumer_ack_propagation_enabled.setter
    def queue_consumer_ack_propagation_enabled(self, queue_consumer_ack_propagation_enabled):
        """Sets the queue_consumer_ack_propagation_enabled of this MsgVpnMqttSession.

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN. The default value is `true`. Available since 2.14.  # noqa: E501

        :param queue_consumer_ack_propagation_enabled: The queue_consumer_ack_propagation_enabled of this MsgVpnMqttSession.  # noqa: E501
        :type: bool
        """

        self._queue_consumer_ack_propagation_enabled = queue_consumer_ack_propagation_enabled

    @property
    def queue_dead_msg_queue(self):
        """Gets the queue_dead_msg_queue of this MsgVpnMqttSession.  # noqa: E501

        The name of the Dead Message Queue (DMQ) used by the MQTT Session Queue. The default value is `\"#DEAD_MSG_QUEUE\"`. Available since 2.14.  # noqa: E501

        :return: The queue_dead_msg_queue of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._queue_dead_msg_queue

    @queue_dead_msg_queue.setter
    def queue_dead_msg_queue(self, queue_dead_msg_queue):
        """Sets the queue_dead_msg_queue of this MsgVpnMqttSession.

        The name of the Dead Message Queue (DMQ) used by the MQTT Session Queue. The default value is `\"#DEAD_MSG_QUEUE\"`. Available since 2.14.  # noqa: E501

        :param queue_dead_msg_queue: The queue_dead_msg_queue of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """

        self._queue_dead_msg_queue = queue_dead_msg_queue

    @property
    def queue_event_bind_count_threshold(self):
        """Gets the queue_event_bind_count_threshold of this MsgVpnMqttSession.  # noqa: E501


        :return: The queue_event_bind_count_threshold of this MsgVpnMqttSession.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._queue_event_bind_count_threshold

    @queue_event_bind_count_threshold.setter
    def queue_event_bind_count_threshold(self, queue_event_bind_count_threshold):
        """Sets the queue_event_bind_count_threshold of this MsgVpnMqttSession.


        :param queue_event_bind_count_threshold: The queue_event_bind_count_threshold of this MsgVpnMqttSession.  # noqa: E501
        :type: EventThreshold
        """

        self._queue_event_bind_count_threshold = queue_event_bind_count_threshold

    @property
    def queue_event_msg_spool_usage_threshold(self):
        """Gets the queue_event_msg_spool_usage_threshold of this MsgVpnMqttSession.  # noqa: E501


        :return: The queue_event_msg_spool_usage_threshold of this MsgVpnMqttSession.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._queue_event_msg_spool_usage_threshold

    @queue_event_msg_spool_usage_threshold.setter
    def queue_event_msg_spool_usage_threshold(self, queue_event_msg_spool_usage_threshold):
        """Sets the queue_event_msg_spool_usage_threshold of this MsgVpnMqttSession.


        :param queue_event_msg_spool_usage_threshold: The queue_event_msg_spool_usage_threshold of this MsgVpnMqttSession.  # noqa: E501
        :type: EventThreshold
        """

        self._queue_event_msg_spool_usage_threshold = queue_event_msg_spool_usage_threshold

    @property
    def queue_event_reject_low_priority_msg_limit_threshold(self):
        """Gets the queue_event_reject_low_priority_msg_limit_threshold of this MsgVpnMqttSession.  # noqa: E501


        :return: The queue_event_reject_low_priority_msg_limit_threshold of this MsgVpnMqttSession.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._queue_event_reject_low_priority_msg_limit_threshold

    @queue_event_reject_low_priority_msg_limit_threshold.setter
    def queue_event_reject_low_priority_msg_limit_threshold(self, queue_event_reject_low_priority_msg_limit_threshold):
        """Sets the queue_event_reject_low_priority_msg_limit_threshold of this MsgVpnMqttSession.


        :param queue_event_reject_low_priority_msg_limit_threshold: The queue_event_reject_low_priority_msg_limit_threshold of this MsgVpnMqttSession.  # noqa: E501
        :type: EventThreshold
        """

        self._queue_event_reject_low_priority_msg_limit_threshold = queue_event_reject_low_priority_msg_limit_threshold

    @property
    def queue_max_bind_count(self):
        """Gets the queue_max_bind_count of this MsgVpnMqttSession.  # noqa: E501

        The maximum number of consumer flows that can bind to the MQTT Session Queue. The default value is `1000`. Available since 2.14.  # noqa: E501

        :return: The queue_max_bind_count of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_bind_count

    @queue_max_bind_count.setter
    def queue_max_bind_count(self, queue_max_bind_count):
        """Sets the queue_max_bind_count of this MsgVpnMqttSession.

        The maximum number of consumer flows that can bind to the MQTT Session Queue. The default value is `1000`. Available since 2.14.  # noqa: E501

        :param queue_max_bind_count: The queue_max_bind_count of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_bind_count = queue_max_bind_count

    @property
    def queue_max_delivered_unacked_msgs_per_flow(self):
        """Gets the queue_max_delivered_unacked_msgs_per_flow of this MsgVpnMqttSession.  # noqa: E501

        The maximum number of messages delivered but not acknowledged per flow for the MQTT Session Queue. The default value is `10000`. Available since 2.14.  # noqa: E501

        :return: The queue_max_delivered_unacked_msgs_per_flow of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_delivered_unacked_msgs_per_flow

    @queue_max_delivered_unacked_msgs_per_flow.setter
    def queue_max_delivered_unacked_msgs_per_flow(self, queue_max_delivered_unacked_msgs_per_flow):
        """Sets the queue_max_delivered_unacked_msgs_per_flow of this MsgVpnMqttSession.

        The maximum number of messages delivered but not acknowledged per flow for the MQTT Session Queue. The default value is `10000`. Available since 2.14.  # noqa: E501

        :param queue_max_delivered_unacked_msgs_per_flow: The queue_max_delivered_unacked_msgs_per_flow of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_delivered_unacked_msgs_per_flow = queue_max_delivered_unacked_msgs_per_flow

    @property
    def queue_max_msg_size(self):
        """Gets the queue_max_msg_size of this MsgVpnMqttSession.  # noqa: E501

        The maximum message size allowed in the MQTT Session Queue, in bytes (B). The default value is `10000000`. Available since 2.14.  # noqa: E501

        :return: The queue_max_msg_size of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_msg_size

    @queue_max_msg_size.setter
    def queue_max_msg_size(self, queue_max_msg_size):
        """Sets the queue_max_msg_size of this MsgVpnMqttSession.

        The maximum message size allowed in the MQTT Session Queue, in bytes (B). The default value is `10000000`. Available since 2.14.  # noqa: E501

        :param queue_max_msg_size: The queue_max_msg_size of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_msg_size = queue_max_msg_size

    @property
    def queue_max_msg_spool_usage(self):
        """Gets the queue_max_msg_spool_usage of this MsgVpnMqttSession.  # noqa: E501

        The maximum message spool usage allowed by the MQTT Session Queue, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking. The default value is `1500`. Available since 2.14.  # noqa: E501

        :return: The queue_max_msg_spool_usage of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_msg_spool_usage

    @queue_max_msg_spool_usage.setter
    def queue_max_msg_spool_usage(self, queue_max_msg_spool_usage):
        """Sets the queue_max_msg_spool_usage of this MsgVpnMqttSession.

        The maximum message spool usage allowed by the MQTT Session Queue, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking. The default value is `1500`. Available since 2.14.  # noqa: E501

        :param queue_max_msg_spool_usage: The queue_max_msg_spool_usage of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_msg_spool_usage = queue_max_msg_spool_usage

    @property
    def queue_max_redelivery_count(self):
        """Gets the queue_max_redelivery_count of this MsgVpnMqttSession.  # noqa: E501

        The maximum number of times the MQTT Session Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever. The default value is `0`. Available since 2.14.  # noqa: E501

        :return: The queue_max_redelivery_count of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_redelivery_count

    @queue_max_redelivery_count.setter
    def queue_max_redelivery_count(self, queue_max_redelivery_count):
        """Sets the queue_max_redelivery_count of this MsgVpnMqttSession.

        The maximum number of times the MQTT Session Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever. The default value is `0`. Available since 2.14.  # noqa: E501

        :param queue_max_redelivery_count: The queue_max_redelivery_count of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_redelivery_count = queue_max_redelivery_count

    @property
    def queue_max_ttl(self):
        """Gets the queue_max_ttl of this MsgVpnMqttSession.  # noqa: E501

        The maximum time in seconds a message can stay in the MQTT Session Queue when `queueRespectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `queueMaxTtl` configured for the MQTT Session Queue, is exceeded. A value of 0 disables expiry. The default value is `0`. Available since 2.14.  # noqa: E501

        :return: The queue_max_ttl of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_ttl

    @queue_max_ttl.setter
    def queue_max_ttl(self, queue_max_ttl):
        """Sets the queue_max_ttl of this MsgVpnMqttSession.

        The maximum time in seconds a message can stay in the MQTT Session Queue when `queueRespectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `queueMaxTtl` configured for the MQTT Session Queue, is exceeded. A value of 0 disables expiry. The default value is `0`. Available since 2.14.  # noqa: E501

        :param queue_max_ttl: The queue_max_ttl of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_max_ttl = queue_max_ttl

    @property
    def queue_reject_low_priority_msg_enabled(self):
        """Gets the queue_reject_low_priority_msg_enabled of this MsgVpnMqttSession.  # noqa: E501

        Enable or disable the checking of low priority messages against the `queueRejectLowPriorityMsgLimit`. This may only be enabled if `queueRejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`. The default value is `false`. Available since 2.14.  # noqa: E501

        :return: The queue_reject_low_priority_msg_enabled of this MsgVpnMqttSession.  # noqa: E501
        :rtype: bool
        """
        return self._queue_reject_low_priority_msg_enabled

    @queue_reject_low_priority_msg_enabled.setter
    def queue_reject_low_priority_msg_enabled(self, queue_reject_low_priority_msg_enabled):
        """Sets the queue_reject_low_priority_msg_enabled of this MsgVpnMqttSession.

        Enable or disable the checking of low priority messages against the `queueRejectLowPriorityMsgLimit`. This may only be enabled if `queueRejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`. The default value is `false`. Available since 2.14.  # noqa: E501

        :param queue_reject_low_priority_msg_enabled: The queue_reject_low_priority_msg_enabled of this MsgVpnMqttSession.  # noqa: E501
        :type: bool
        """

        self._queue_reject_low_priority_msg_enabled = queue_reject_low_priority_msg_enabled

    @property
    def queue_reject_low_priority_msg_limit(self):
        """Gets the queue_reject_low_priority_msg_limit of this MsgVpnMqttSession.  # noqa: E501

        The number of messages of any priority in the MQTT Session Queue above which low priority messages are not admitted but higher priority messages are allowed. The default value is `0`. Available since 2.14.  # noqa: E501

        :return: The queue_reject_low_priority_msg_limit of this MsgVpnMqttSession.  # noqa: E501
        :rtype: int
        """
        return self._queue_reject_low_priority_msg_limit

    @queue_reject_low_priority_msg_limit.setter
    def queue_reject_low_priority_msg_limit(self, queue_reject_low_priority_msg_limit):
        """Sets the queue_reject_low_priority_msg_limit of this MsgVpnMqttSession.

        The number of messages of any priority in the MQTT Session Queue above which low priority messages are not admitted but higher priority messages are allowed. The default value is `0`. Available since 2.14.  # noqa: E501

        :param queue_reject_low_priority_msg_limit: The queue_reject_low_priority_msg_limit of this MsgVpnMqttSession.  # noqa: E501
        :type: int
        """

        self._queue_reject_low_priority_msg_limit = queue_reject_low_priority_msg_limit

    @property
    def queue_reject_msg_to_sender_on_discard_behavior(self):
        """Gets the queue_reject_msg_to_sender_on_discard_behavior of this MsgVpnMqttSession.  # noqa: E501

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The default value is `\"when-queue-enabled\"`. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>  Available since 2.14.  # noqa: E501

        :return: The queue_reject_msg_to_sender_on_discard_behavior of this MsgVpnMqttSession.  # noqa: E501
        :rtype: str
        """
        return self._queue_reject_msg_to_sender_on_discard_behavior

    @queue_reject_msg_to_sender_on_discard_behavior.setter
    def queue_reject_msg_to_sender_on_discard_behavior(self, queue_reject_msg_to_sender_on_discard_behavior):
        """Sets the queue_reject_msg_to_sender_on_discard_behavior of this MsgVpnMqttSession.

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The default value is `\"when-queue-enabled\"`. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>  Available since 2.14.  # noqa: E501

        :param queue_reject_msg_to_sender_on_discard_behavior: The queue_reject_msg_to_sender_on_discard_behavior of this MsgVpnMqttSession.  # noqa: E501
        :type: str
        """
        allowed_values = ["always", "when-queue-enabled", "never"]  # noqa: E501
        if queue_reject_msg_to_sender_on_discard_behavior not in allowed_values:
            raise ValueError(
                "Invalid value for `queue_reject_msg_to_sender_on_discard_behavior` ({0}), must be one of {1}"  # noqa: E501
                .format(queue_reject_msg_to_sender_on_discard_behavior, allowed_values)
            )

        self._queue_reject_msg_to_sender_on_discard_behavior = queue_reject_msg_to_sender_on_discard_behavior

    @property
    def queue_respect_ttl_enabled(self):
        """Gets the queue_respect_ttl_enabled of this MsgVpnMqttSession.  # noqa: E501

        Enable or disable the respecting of the time-to-live (TTL) for messages in the MQTT Session Queue. When enabled, expired messages are discarded or moved to the DMQ. The default value is `false`. Available since 2.14.  # noqa: E501

        :return: The queue_respect_ttl_enabled of this MsgVpnMqttSession.  # noqa: E501
        :rtype: bool
        """
        return self._queue_respect_ttl_enabled

    @queue_respect_ttl_enabled.setter
    def queue_respect_ttl_enabled(self, queue_respect_ttl_enabled):
        """Sets the queue_respect_ttl_enabled of this MsgVpnMqttSession.

        Enable or disable the respecting of the time-to-live (TTL) for messages in the MQTT Session Queue. When enabled, expired messages are discarded or moved to the DMQ. The default value is `false`. Available since 2.14.  # noqa: E501

        :param queue_respect_ttl_enabled: The queue_respect_ttl_enabled of this MsgVpnMqttSession.  # noqa: E501
        :type: bool
        """

        self._queue_respect_ttl_enabled = queue_respect_ttl_enabled

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
        if issubclass(MsgVpnMqttSession, dict):
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
        if not isinstance(other, MsgVpnMqttSession):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
