# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.14
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class DmrClusterLink(object):
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
        'authentication_scheme': 'str',
        'client_profile_name': 'str',
        'client_profile_queue_control1_max_depth': 'int',
        'client_profile_queue_control1_min_msg_burst': 'int',
        'client_profile_queue_direct1_max_depth': 'int',
        'client_profile_queue_direct1_min_msg_burst': 'int',
        'client_profile_queue_direct2_max_depth': 'int',
        'client_profile_queue_direct2_min_msg_burst': 'int',
        'client_profile_queue_direct3_max_depth': 'int',
        'client_profile_queue_direct3_min_msg_burst': 'int',
        'client_profile_queue_guaranteed1_max_depth': 'int',
        'client_profile_queue_guaranteed1_min_msg_burst': 'int',
        'client_profile_tcp_congestion_window_size': 'int',
        'client_profile_tcp_keepalive_count': 'int',
        'client_profile_tcp_keepalive_idle_time': 'int',
        'client_profile_tcp_keepalive_interval': 'int',
        'client_profile_tcp_max_segment_size': 'int',
        'client_profile_tcp_max_window_size': 'int',
        'dmr_cluster_name': 'str',
        'egress_flow_window_size': 'int',
        'enabled': 'bool',
        'failure_reason': 'str',
        'initiator': 'str',
        'queue_dead_msg_queue': 'str',
        'queue_event_spool_usage_threshold': 'EventThreshold',
        'queue_max_delivered_unacked_msgs_per_flow': 'int',
        'queue_max_msg_spool_usage': 'int',
        'queue_max_redelivery_count': 'int',
        'queue_max_ttl': 'int',
        'queue_reject_msg_to_sender_on_discard_behavior': 'str',
        'queue_respect_ttl_enabled': 'bool',
        'remote_node_name': 'str',
        'span': 'str',
        'transport_compressed_enabled': 'bool',
        'transport_tls_enabled': 'bool',
        'up': 'bool',
        'uptime': 'int'
    }

    attribute_map = {
        'authentication_scheme': 'authenticationScheme',
        'client_profile_name': 'clientProfileName',
        'client_profile_queue_control1_max_depth': 'clientProfileQueueControl1MaxDepth',
        'client_profile_queue_control1_min_msg_burst': 'clientProfileQueueControl1MinMsgBurst',
        'client_profile_queue_direct1_max_depth': 'clientProfileQueueDirect1MaxDepth',
        'client_profile_queue_direct1_min_msg_burst': 'clientProfileQueueDirect1MinMsgBurst',
        'client_profile_queue_direct2_max_depth': 'clientProfileQueueDirect2MaxDepth',
        'client_profile_queue_direct2_min_msg_burst': 'clientProfileQueueDirect2MinMsgBurst',
        'client_profile_queue_direct3_max_depth': 'clientProfileQueueDirect3MaxDepth',
        'client_profile_queue_direct3_min_msg_burst': 'clientProfileQueueDirect3MinMsgBurst',
        'client_profile_queue_guaranteed1_max_depth': 'clientProfileQueueGuaranteed1MaxDepth',
        'client_profile_queue_guaranteed1_min_msg_burst': 'clientProfileQueueGuaranteed1MinMsgBurst',
        'client_profile_tcp_congestion_window_size': 'clientProfileTcpCongestionWindowSize',
        'client_profile_tcp_keepalive_count': 'clientProfileTcpKeepaliveCount',
        'client_profile_tcp_keepalive_idle_time': 'clientProfileTcpKeepaliveIdleTime',
        'client_profile_tcp_keepalive_interval': 'clientProfileTcpKeepaliveInterval',
        'client_profile_tcp_max_segment_size': 'clientProfileTcpMaxSegmentSize',
        'client_profile_tcp_max_window_size': 'clientProfileTcpMaxWindowSize',
        'dmr_cluster_name': 'dmrClusterName',
        'egress_flow_window_size': 'egressFlowWindowSize',
        'enabled': 'enabled',
        'failure_reason': 'failureReason',
        'initiator': 'initiator',
        'queue_dead_msg_queue': 'queueDeadMsgQueue',
        'queue_event_spool_usage_threshold': 'queueEventSpoolUsageThreshold',
        'queue_max_delivered_unacked_msgs_per_flow': 'queueMaxDeliveredUnackedMsgsPerFlow',
        'queue_max_msg_spool_usage': 'queueMaxMsgSpoolUsage',
        'queue_max_redelivery_count': 'queueMaxRedeliveryCount',
        'queue_max_ttl': 'queueMaxTtl',
        'queue_reject_msg_to_sender_on_discard_behavior': 'queueRejectMsgToSenderOnDiscardBehavior',
        'queue_respect_ttl_enabled': 'queueRespectTtlEnabled',
        'remote_node_name': 'remoteNodeName',
        'span': 'span',
        'transport_compressed_enabled': 'transportCompressedEnabled',
        'transport_tls_enabled': 'transportTlsEnabled',
        'up': 'up',
        'uptime': 'uptime'
    }

    def __init__(self, authentication_scheme=None, client_profile_name=None, client_profile_queue_control1_max_depth=None, client_profile_queue_control1_min_msg_burst=None, client_profile_queue_direct1_max_depth=None, client_profile_queue_direct1_min_msg_burst=None, client_profile_queue_direct2_max_depth=None, client_profile_queue_direct2_min_msg_burst=None, client_profile_queue_direct3_max_depth=None, client_profile_queue_direct3_min_msg_burst=None, client_profile_queue_guaranteed1_max_depth=None, client_profile_queue_guaranteed1_min_msg_burst=None, client_profile_tcp_congestion_window_size=None, client_profile_tcp_keepalive_count=None, client_profile_tcp_keepalive_idle_time=None, client_profile_tcp_keepalive_interval=None, client_profile_tcp_max_segment_size=None, client_profile_tcp_max_window_size=None, dmr_cluster_name=None, egress_flow_window_size=None, enabled=None, failure_reason=None, initiator=None, queue_dead_msg_queue=None, queue_event_spool_usage_threshold=None, queue_max_delivered_unacked_msgs_per_flow=None, queue_max_msg_spool_usage=None, queue_max_redelivery_count=None, queue_max_ttl=None, queue_reject_msg_to_sender_on_discard_behavior=None, queue_respect_ttl_enabled=None, remote_node_name=None, span=None, transport_compressed_enabled=None, transport_tls_enabled=None, up=None, uptime=None):  # noqa: E501
        """DmrClusterLink - a model defined in Swagger"""  # noqa: E501

        self._authentication_scheme = None
        self._client_profile_name = None
        self._client_profile_queue_control1_max_depth = None
        self._client_profile_queue_control1_min_msg_burst = None
        self._client_profile_queue_direct1_max_depth = None
        self._client_profile_queue_direct1_min_msg_burst = None
        self._client_profile_queue_direct2_max_depth = None
        self._client_profile_queue_direct2_min_msg_burst = None
        self._client_profile_queue_direct3_max_depth = None
        self._client_profile_queue_direct3_min_msg_burst = None
        self._client_profile_queue_guaranteed1_max_depth = None
        self._client_profile_queue_guaranteed1_min_msg_burst = None
        self._client_profile_tcp_congestion_window_size = None
        self._client_profile_tcp_keepalive_count = None
        self._client_profile_tcp_keepalive_idle_time = None
        self._client_profile_tcp_keepalive_interval = None
        self._client_profile_tcp_max_segment_size = None
        self._client_profile_tcp_max_window_size = None
        self._dmr_cluster_name = None
        self._egress_flow_window_size = None
        self._enabled = None
        self._failure_reason = None
        self._initiator = None
        self._queue_dead_msg_queue = None
        self._queue_event_spool_usage_threshold = None
        self._queue_max_delivered_unacked_msgs_per_flow = None
        self._queue_max_msg_spool_usage = None
        self._queue_max_redelivery_count = None
        self._queue_max_ttl = None
        self._queue_reject_msg_to_sender_on_discard_behavior = None
        self._queue_respect_ttl_enabled = None
        self._remote_node_name = None
        self._span = None
        self._transport_compressed_enabled = None
        self._transport_tls_enabled = None
        self._up = None
        self._uptime = None
        self.discriminator = None

        if authentication_scheme is not None:
            self.authentication_scheme = authentication_scheme
        if client_profile_name is not None:
            self.client_profile_name = client_profile_name
        if client_profile_queue_control1_max_depth is not None:
            self.client_profile_queue_control1_max_depth = client_profile_queue_control1_max_depth
        if client_profile_queue_control1_min_msg_burst is not None:
            self.client_profile_queue_control1_min_msg_burst = client_profile_queue_control1_min_msg_burst
        if client_profile_queue_direct1_max_depth is not None:
            self.client_profile_queue_direct1_max_depth = client_profile_queue_direct1_max_depth
        if client_profile_queue_direct1_min_msg_burst is not None:
            self.client_profile_queue_direct1_min_msg_burst = client_profile_queue_direct1_min_msg_burst
        if client_profile_queue_direct2_max_depth is not None:
            self.client_profile_queue_direct2_max_depth = client_profile_queue_direct2_max_depth
        if client_profile_queue_direct2_min_msg_burst is not None:
            self.client_profile_queue_direct2_min_msg_burst = client_profile_queue_direct2_min_msg_burst
        if client_profile_queue_direct3_max_depth is not None:
            self.client_profile_queue_direct3_max_depth = client_profile_queue_direct3_max_depth
        if client_profile_queue_direct3_min_msg_burst is not None:
            self.client_profile_queue_direct3_min_msg_burst = client_profile_queue_direct3_min_msg_burst
        if client_profile_queue_guaranteed1_max_depth is not None:
            self.client_profile_queue_guaranteed1_max_depth = client_profile_queue_guaranteed1_max_depth
        if client_profile_queue_guaranteed1_min_msg_burst is not None:
            self.client_profile_queue_guaranteed1_min_msg_burst = client_profile_queue_guaranteed1_min_msg_burst
        if client_profile_tcp_congestion_window_size is not None:
            self.client_profile_tcp_congestion_window_size = client_profile_tcp_congestion_window_size
        if client_profile_tcp_keepalive_count is not None:
            self.client_profile_tcp_keepalive_count = client_profile_tcp_keepalive_count
        if client_profile_tcp_keepalive_idle_time is not None:
            self.client_profile_tcp_keepalive_idle_time = client_profile_tcp_keepalive_idle_time
        if client_profile_tcp_keepalive_interval is not None:
            self.client_profile_tcp_keepalive_interval = client_profile_tcp_keepalive_interval
        if client_profile_tcp_max_segment_size is not None:
            self.client_profile_tcp_max_segment_size = client_profile_tcp_max_segment_size
        if client_profile_tcp_max_window_size is not None:
            self.client_profile_tcp_max_window_size = client_profile_tcp_max_window_size
        if dmr_cluster_name is not None:
            self.dmr_cluster_name = dmr_cluster_name
        if egress_flow_window_size is not None:
            self.egress_flow_window_size = egress_flow_window_size
        if enabled is not None:
            self.enabled = enabled
        if failure_reason is not None:
            self.failure_reason = failure_reason
        if initiator is not None:
            self.initiator = initiator
        if queue_dead_msg_queue is not None:
            self.queue_dead_msg_queue = queue_dead_msg_queue
        if queue_event_spool_usage_threshold is not None:
            self.queue_event_spool_usage_threshold = queue_event_spool_usage_threshold
        if queue_max_delivered_unacked_msgs_per_flow is not None:
            self.queue_max_delivered_unacked_msgs_per_flow = queue_max_delivered_unacked_msgs_per_flow
        if queue_max_msg_spool_usage is not None:
            self.queue_max_msg_spool_usage = queue_max_msg_spool_usage
        if queue_max_redelivery_count is not None:
            self.queue_max_redelivery_count = queue_max_redelivery_count
        if queue_max_ttl is not None:
            self.queue_max_ttl = queue_max_ttl
        if queue_reject_msg_to_sender_on_discard_behavior is not None:
            self.queue_reject_msg_to_sender_on_discard_behavior = queue_reject_msg_to_sender_on_discard_behavior
        if queue_respect_ttl_enabled is not None:
            self.queue_respect_ttl_enabled = queue_respect_ttl_enabled
        if remote_node_name is not None:
            self.remote_node_name = remote_node_name
        if span is not None:
            self.span = span
        if transport_compressed_enabled is not None:
            self.transport_compressed_enabled = transport_compressed_enabled
        if transport_tls_enabled is not None:
            self.transport_tls_enabled = transport_tls_enabled
        if up is not None:
            self.up = up
        if uptime is not None:
            self.uptime = uptime

    @property
    def authentication_scheme(self):
        """Gets the authentication_scheme of this DmrClusterLink.  # noqa: E501

        The authentication scheme to be used by the Link which initiates connections to the remote node. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>   # noqa: E501

        :return: The authentication_scheme of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._authentication_scheme

    @authentication_scheme.setter
    def authentication_scheme(self, authentication_scheme):
        """Sets the authentication_scheme of this DmrClusterLink.

        The authentication scheme to be used by the Link which initiates connections to the remote node. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>   # noqa: E501

        :param authentication_scheme: The authentication_scheme of this DmrClusterLink.  # noqa: E501
        :type: str
        """
        allowed_values = ["basic", "client-certificate"]  # noqa: E501
        if authentication_scheme not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_scheme` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_scheme, allowed_values)
            )

        self._authentication_scheme = authentication_scheme

    @property
    def client_profile_name(self):
        """Gets the client_profile_name of this DmrClusterLink.  # noqa: E501

        The name of the Client Profile used by the Link.  # noqa: E501

        :return: The client_profile_name of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._client_profile_name

    @client_profile_name.setter
    def client_profile_name(self, client_profile_name):
        """Sets the client_profile_name of this DmrClusterLink.

        The name of the Client Profile used by the Link.  # noqa: E501

        :param client_profile_name: The client_profile_name of this DmrClusterLink.  # noqa: E501
        :type: str
        """

        self._client_profile_name = client_profile_name

    @property
    def client_profile_queue_control1_max_depth(self):
        """Gets the client_profile_queue_control1_max_depth of this DmrClusterLink.  # noqa: E501

        The maximum depth of the \"Control 1\" (C-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :return: The client_profile_queue_control1_max_depth of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_control1_max_depth

    @client_profile_queue_control1_max_depth.setter
    def client_profile_queue_control1_max_depth(self, client_profile_queue_control1_max_depth):
        """Sets the client_profile_queue_control1_max_depth of this DmrClusterLink.

        The maximum depth of the \"Control 1\" (C-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :param client_profile_queue_control1_max_depth: The client_profile_queue_control1_max_depth of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_control1_max_depth = client_profile_queue_control1_max_depth

    @property
    def client_profile_queue_control1_min_msg_burst(self):
        """Gets the client_profile_queue_control1_min_msg_burst of this DmrClusterLink.  # noqa: E501

        The number of messages that are always allowed entry into the \"Control 1\" (C-1) priority queue, regardless of the `clientProfileQueueControl1MaxDepth` value.  # noqa: E501

        :return: The client_profile_queue_control1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_control1_min_msg_burst

    @client_profile_queue_control1_min_msg_burst.setter
    def client_profile_queue_control1_min_msg_burst(self, client_profile_queue_control1_min_msg_burst):
        """Sets the client_profile_queue_control1_min_msg_burst of this DmrClusterLink.

        The number of messages that are always allowed entry into the \"Control 1\" (C-1) priority queue, regardless of the `clientProfileQueueControl1MaxDepth` value.  # noqa: E501

        :param client_profile_queue_control1_min_msg_burst: The client_profile_queue_control1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_control1_min_msg_burst = client_profile_queue_control1_min_msg_burst

    @property
    def client_profile_queue_direct1_max_depth(self):
        """Gets the client_profile_queue_direct1_max_depth of this DmrClusterLink.  # noqa: E501

        The maximum depth of the \"Direct 1\" (D-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :return: The client_profile_queue_direct1_max_depth of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct1_max_depth

    @client_profile_queue_direct1_max_depth.setter
    def client_profile_queue_direct1_max_depth(self, client_profile_queue_direct1_max_depth):
        """Sets the client_profile_queue_direct1_max_depth of this DmrClusterLink.

        The maximum depth of the \"Direct 1\" (D-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :param client_profile_queue_direct1_max_depth: The client_profile_queue_direct1_max_depth of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct1_max_depth = client_profile_queue_direct1_max_depth

    @property
    def client_profile_queue_direct1_min_msg_burst(self):
        """Gets the client_profile_queue_direct1_min_msg_burst of this DmrClusterLink.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 1\" (D-1) priority queue, regardless of the `clientProfileQueueDirect1MaxDepth` value.  # noqa: E501

        :return: The client_profile_queue_direct1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct1_min_msg_burst

    @client_profile_queue_direct1_min_msg_burst.setter
    def client_profile_queue_direct1_min_msg_burst(self, client_profile_queue_direct1_min_msg_burst):
        """Sets the client_profile_queue_direct1_min_msg_burst of this DmrClusterLink.

        The number of messages that are always allowed entry into the \"Direct 1\" (D-1) priority queue, regardless of the `clientProfileQueueDirect1MaxDepth` value.  # noqa: E501

        :param client_profile_queue_direct1_min_msg_burst: The client_profile_queue_direct1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct1_min_msg_burst = client_profile_queue_direct1_min_msg_burst

    @property
    def client_profile_queue_direct2_max_depth(self):
        """Gets the client_profile_queue_direct2_max_depth of this DmrClusterLink.  # noqa: E501

        The maximum depth of the \"Direct 2\" (D-2) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :return: The client_profile_queue_direct2_max_depth of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct2_max_depth

    @client_profile_queue_direct2_max_depth.setter
    def client_profile_queue_direct2_max_depth(self, client_profile_queue_direct2_max_depth):
        """Sets the client_profile_queue_direct2_max_depth of this DmrClusterLink.

        The maximum depth of the \"Direct 2\" (D-2) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :param client_profile_queue_direct2_max_depth: The client_profile_queue_direct2_max_depth of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct2_max_depth = client_profile_queue_direct2_max_depth

    @property
    def client_profile_queue_direct2_min_msg_burst(self):
        """Gets the client_profile_queue_direct2_min_msg_burst of this DmrClusterLink.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 2\" (D-2) priority queue, regardless of the `clientProfileQueueDirect2MaxDepth` value.  # noqa: E501

        :return: The client_profile_queue_direct2_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct2_min_msg_burst

    @client_profile_queue_direct2_min_msg_burst.setter
    def client_profile_queue_direct2_min_msg_burst(self, client_profile_queue_direct2_min_msg_burst):
        """Sets the client_profile_queue_direct2_min_msg_burst of this DmrClusterLink.

        The number of messages that are always allowed entry into the \"Direct 2\" (D-2) priority queue, regardless of the `clientProfileQueueDirect2MaxDepth` value.  # noqa: E501

        :param client_profile_queue_direct2_min_msg_burst: The client_profile_queue_direct2_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct2_min_msg_burst = client_profile_queue_direct2_min_msg_burst

    @property
    def client_profile_queue_direct3_max_depth(self):
        """Gets the client_profile_queue_direct3_max_depth of this DmrClusterLink.  # noqa: E501

        The maximum depth of the \"Direct 3\" (D-3) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :return: The client_profile_queue_direct3_max_depth of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct3_max_depth

    @client_profile_queue_direct3_max_depth.setter
    def client_profile_queue_direct3_max_depth(self, client_profile_queue_direct3_max_depth):
        """Sets the client_profile_queue_direct3_max_depth of this DmrClusterLink.

        The maximum depth of the \"Direct 3\" (D-3) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :param client_profile_queue_direct3_max_depth: The client_profile_queue_direct3_max_depth of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct3_max_depth = client_profile_queue_direct3_max_depth

    @property
    def client_profile_queue_direct3_min_msg_burst(self):
        """Gets the client_profile_queue_direct3_min_msg_burst of this DmrClusterLink.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 3\" (D-3) priority queue, regardless of the `clientProfileQueueDirect3MaxDepth` value.  # noqa: E501

        :return: The client_profile_queue_direct3_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_direct3_min_msg_burst

    @client_profile_queue_direct3_min_msg_burst.setter
    def client_profile_queue_direct3_min_msg_burst(self, client_profile_queue_direct3_min_msg_burst):
        """Sets the client_profile_queue_direct3_min_msg_burst of this DmrClusterLink.

        The number of messages that are always allowed entry into the \"Direct 3\" (D-3) priority queue, regardless of the `clientProfileQueueDirect3MaxDepth` value.  # noqa: E501

        :param client_profile_queue_direct3_min_msg_burst: The client_profile_queue_direct3_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_direct3_min_msg_burst = client_profile_queue_direct3_min_msg_burst

    @property
    def client_profile_queue_guaranteed1_max_depth(self):
        """Gets the client_profile_queue_guaranteed1_max_depth of this DmrClusterLink.  # noqa: E501

        The maximum depth of the \"Guaranteed 1\" (G-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :return: The client_profile_queue_guaranteed1_max_depth of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_guaranteed1_max_depth

    @client_profile_queue_guaranteed1_max_depth.setter
    def client_profile_queue_guaranteed1_max_depth(self, client_profile_queue_guaranteed1_max_depth):
        """Sets the client_profile_queue_guaranteed1_max_depth of this DmrClusterLink.

        The maximum depth of the \"Guaranteed 1\" (G-1) priority queue, in work units. Each work unit is 2048 bytes of message data.  # noqa: E501

        :param client_profile_queue_guaranteed1_max_depth: The client_profile_queue_guaranteed1_max_depth of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_guaranteed1_max_depth = client_profile_queue_guaranteed1_max_depth

    @property
    def client_profile_queue_guaranteed1_min_msg_burst(self):
        """Gets the client_profile_queue_guaranteed1_min_msg_burst of this DmrClusterLink.  # noqa: E501

        The number of messages that are always allowed entry into the \"Guaranteed 1\" (G-3) priority queue, regardless of the `clientProfileQueueGuaranteed1MaxDepth` value.  # noqa: E501

        :return: The client_profile_queue_guaranteed1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_queue_guaranteed1_min_msg_burst

    @client_profile_queue_guaranteed1_min_msg_burst.setter
    def client_profile_queue_guaranteed1_min_msg_burst(self, client_profile_queue_guaranteed1_min_msg_burst):
        """Sets the client_profile_queue_guaranteed1_min_msg_burst of this DmrClusterLink.

        The number of messages that are always allowed entry into the \"Guaranteed 1\" (G-3) priority queue, regardless of the `clientProfileQueueGuaranteed1MaxDepth` value.  # noqa: E501

        :param client_profile_queue_guaranteed1_min_msg_burst: The client_profile_queue_guaranteed1_min_msg_burst of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_queue_guaranteed1_min_msg_burst = client_profile_queue_guaranteed1_min_msg_burst

    @property
    def client_profile_tcp_congestion_window_size(self):
        """Gets the client_profile_tcp_congestion_window_size of this DmrClusterLink.  # noqa: E501

        The TCP initial congestion window size, in multiples of the TCP Maximum Segment Size (MSS). Changing the value from its default of 2 results in non-compliance with RFC 2581. Contact Solace Support before changing this value.  # noqa: E501

        :return: The client_profile_tcp_congestion_window_size of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_congestion_window_size

    @client_profile_tcp_congestion_window_size.setter
    def client_profile_tcp_congestion_window_size(self, client_profile_tcp_congestion_window_size):
        """Sets the client_profile_tcp_congestion_window_size of this DmrClusterLink.

        The TCP initial congestion window size, in multiples of the TCP Maximum Segment Size (MSS). Changing the value from its default of 2 results in non-compliance with RFC 2581. Contact Solace Support before changing this value.  # noqa: E501

        :param client_profile_tcp_congestion_window_size: The client_profile_tcp_congestion_window_size of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_congestion_window_size = client_profile_tcp_congestion_window_size

    @property
    def client_profile_tcp_keepalive_count(self):
        """Gets the client_profile_tcp_keepalive_count of this DmrClusterLink.  # noqa: E501

        The number of TCP keepalive retransmissions to be carried out before declaring that the remote end is not available.  # noqa: E501

        :return: The client_profile_tcp_keepalive_count of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_keepalive_count

    @client_profile_tcp_keepalive_count.setter
    def client_profile_tcp_keepalive_count(self, client_profile_tcp_keepalive_count):
        """Sets the client_profile_tcp_keepalive_count of this DmrClusterLink.

        The number of TCP keepalive retransmissions to be carried out before declaring that the remote end is not available.  # noqa: E501

        :param client_profile_tcp_keepalive_count: The client_profile_tcp_keepalive_count of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_keepalive_count = client_profile_tcp_keepalive_count

    @property
    def client_profile_tcp_keepalive_idle_time(self):
        """Gets the client_profile_tcp_keepalive_idle_time of this DmrClusterLink.  # noqa: E501

        The amount of time a connection must remain idle before TCP begins sending keepalive probes, in seconds.  # noqa: E501

        :return: The client_profile_tcp_keepalive_idle_time of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_keepalive_idle_time

    @client_profile_tcp_keepalive_idle_time.setter
    def client_profile_tcp_keepalive_idle_time(self, client_profile_tcp_keepalive_idle_time):
        """Sets the client_profile_tcp_keepalive_idle_time of this DmrClusterLink.

        The amount of time a connection must remain idle before TCP begins sending keepalive probes, in seconds.  # noqa: E501

        :param client_profile_tcp_keepalive_idle_time: The client_profile_tcp_keepalive_idle_time of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_keepalive_idle_time = client_profile_tcp_keepalive_idle_time

    @property
    def client_profile_tcp_keepalive_interval(self):
        """Gets the client_profile_tcp_keepalive_interval of this DmrClusterLink.  # noqa: E501

        The amount of time between TCP keepalive retransmissions when no acknowledgement is received, in seconds.  # noqa: E501

        :return: The client_profile_tcp_keepalive_interval of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_keepalive_interval

    @client_profile_tcp_keepalive_interval.setter
    def client_profile_tcp_keepalive_interval(self, client_profile_tcp_keepalive_interval):
        """Sets the client_profile_tcp_keepalive_interval of this DmrClusterLink.

        The amount of time between TCP keepalive retransmissions when no acknowledgement is received, in seconds.  # noqa: E501

        :param client_profile_tcp_keepalive_interval: The client_profile_tcp_keepalive_interval of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_keepalive_interval = client_profile_tcp_keepalive_interval

    @property
    def client_profile_tcp_max_segment_size(self):
        """Gets the client_profile_tcp_max_segment_size of this DmrClusterLink.  # noqa: E501

        The TCP maximum segment size, in kilobytes. Changes are applied to all existing connections.  # noqa: E501

        :return: The client_profile_tcp_max_segment_size of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_max_segment_size

    @client_profile_tcp_max_segment_size.setter
    def client_profile_tcp_max_segment_size(self, client_profile_tcp_max_segment_size):
        """Sets the client_profile_tcp_max_segment_size of this DmrClusterLink.

        The TCP maximum segment size, in kilobytes. Changes are applied to all existing connections.  # noqa: E501

        :param client_profile_tcp_max_segment_size: The client_profile_tcp_max_segment_size of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_max_segment_size = client_profile_tcp_max_segment_size

    @property
    def client_profile_tcp_max_window_size(self):
        """Gets the client_profile_tcp_max_window_size of this DmrClusterLink.  # noqa: E501

        The TCP maximum window size, in kilobytes. Changes are applied to all existing connections.  # noqa: E501

        :return: The client_profile_tcp_max_window_size of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_tcp_max_window_size

    @client_profile_tcp_max_window_size.setter
    def client_profile_tcp_max_window_size(self, client_profile_tcp_max_window_size):
        """Sets the client_profile_tcp_max_window_size of this DmrClusterLink.

        The TCP maximum window size, in kilobytes. Changes are applied to all existing connections.  # noqa: E501

        :param client_profile_tcp_max_window_size: The client_profile_tcp_max_window_size of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._client_profile_tcp_max_window_size = client_profile_tcp_max_window_size

    @property
    def dmr_cluster_name(self):
        """Gets the dmr_cluster_name of this DmrClusterLink.  # noqa: E501

        The name of the Cluster.  # noqa: E501

        :return: The dmr_cluster_name of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._dmr_cluster_name

    @dmr_cluster_name.setter
    def dmr_cluster_name(self, dmr_cluster_name):
        """Sets the dmr_cluster_name of this DmrClusterLink.

        The name of the Cluster.  # noqa: E501

        :param dmr_cluster_name: The dmr_cluster_name of this DmrClusterLink.  # noqa: E501
        :type: str
        """

        self._dmr_cluster_name = dmr_cluster_name

    @property
    def egress_flow_window_size(self):
        """Gets the egress_flow_window_size of this DmrClusterLink.  # noqa: E501

        The number of outstanding guaranteed messages that can be sent over the Link before acknowledgement is received by the sender.  # noqa: E501

        :return: The egress_flow_window_size of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._egress_flow_window_size

    @egress_flow_window_size.setter
    def egress_flow_window_size(self, egress_flow_window_size):
        """Sets the egress_flow_window_size of this DmrClusterLink.

        The number of outstanding guaranteed messages that can be sent over the Link before acknowledgement is received by the sender.  # noqa: E501

        :param egress_flow_window_size: The egress_flow_window_size of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._egress_flow_window_size = egress_flow_window_size

    @property
    def enabled(self):
        """Gets the enabled of this DmrClusterLink.  # noqa: E501

        Indicates whether the Link is enabled. When disabled, subscription sets of this and the remote node are not kept up-to-date, and messages are not exchanged with the remote node. Published guaranteed messages will be queued up for future delivery based on current subscription sets.  # noqa: E501

        :return: The enabled of this DmrClusterLink.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this DmrClusterLink.

        Indicates whether the Link is enabled. When disabled, subscription sets of this and the remote node are not kept up-to-date, and messages are not exchanged with the remote node. Published guaranteed messages will be queued up for future delivery based on current subscription sets.  # noqa: E501

        :param enabled: The enabled of this DmrClusterLink.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def failure_reason(self):
        """Gets the failure_reason of this DmrClusterLink.  # noqa: E501

        The failure reason for the Link being down.  # noqa: E501

        :return: The failure_reason of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """Sets the failure_reason of this DmrClusterLink.

        The failure reason for the Link being down.  # noqa: E501

        :param failure_reason: The failure_reason of this DmrClusterLink.  # noqa: E501
        :type: str
        """

        self._failure_reason = failure_reason

    @property
    def initiator(self):
        """Gets the initiator of this DmrClusterLink.  # noqa: E501

        The initiator of the Link's TCP connections. The allowed values and their meaning are:  <pre> \"lexical\" - The \"higher\" node-name initiates. \"local\" - The local node initiates. \"remote\" - The remote node initiates. </pre>   # noqa: E501

        :return: The initiator of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._initiator

    @initiator.setter
    def initiator(self, initiator):
        """Sets the initiator of this DmrClusterLink.

        The initiator of the Link's TCP connections. The allowed values and their meaning are:  <pre> \"lexical\" - The \"higher\" node-name initiates. \"local\" - The local node initiates. \"remote\" - The remote node initiates. </pre>   # noqa: E501

        :param initiator: The initiator of this DmrClusterLink.  # noqa: E501
        :type: str
        """
        allowed_values = ["lexical", "local", "remote"]  # noqa: E501
        if initiator not in allowed_values:
            raise ValueError(
                "Invalid value for `initiator` ({0}), must be one of {1}"  # noqa: E501
                .format(initiator, allowed_values)
            )

        self._initiator = initiator

    @property
    def queue_dead_msg_queue(self):
        """Gets the queue_dead_msg_queue of this DmrClusterLink.  # noqa: E501

        The name of the Dead Message Queue (DMQ) used by the Queue for discarded messages.  # noqa: E501

        :return: The queue_dead_msg_queue of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._queue_dead_msg_queue

    @queue_dead_msg_queue.setter
    def queue_dead_msg_queue(self, queue_dead_msg_queue):
        """Sets the queue_dead_msg_queue of this DmrClusterLink.

        The name of the Dead Message Queue (DMQ) used by the Queue for discarded messages.  # noqa: E501

        :param queue_dead_msg_queue: The queue_dead_msg_queue of this DmrClusterLink.  # noqa: E501
        :type: str
        """

        self._queue_dead_msg_queue = queue_dead_msg_queue

    @property
    def queue_event_spool_usage_threshold(self):
        """Gets the queue_event_spool_usage_threshold of this DmrClusterLink.  # noqa: E501


        :return: The queue_event_spool_usage_threshold of this DmrClusterLink.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._queue_event_spool_usage_threshold

    @queue_event_spool_usage_threshold.setter
    def queue_event_spool_usage_threshold(self, queue_event_spool_usage_threshold):
        """Sets the queue_event_spool_usage_threshold of this DmrClusterLink.


        :param queue_event_spool_usage_threshold: The queue_event_spool_usage_threshold of this DmrClusterLink.  # noqa: E501
        :type: EventThreshold
        """

        self._queue_event_spool_usage_threshold = queue_event_spool_usage_threshold

    @property
    def queue_max_delivered_unacked_msgs_per_flow(self):
        """Gets the queue_max_delivered_unacked_msgs_per_flow of this DmrClusterLink.  # noqa: E501

        The maximum number of messages delivered but not acknowledged per flow for the Queue.  # noqa: E501

        :return: The queue_max_delivered_unacked_msgs_per_flow of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_delivered_unacked_msgs_per_flow

    @queue_max_delivered_unacked_msgs_per_flow.setter
    def queue_max_delivered_unacked_msgs_per_flow(self, queue_max_delivered_unacked_msgs_per_flow):
        """Sets the queue_max_delivered_unacked_msgs_per_flow of this DmrClusterLink.

        The maximum number of messages delivered but not acknowledged per flow for the Queue.  # noqa: E501

        :param queue_max_delivered_unacked_msgs_per_flow: The queue_max_delivered_unacked_msgs_per_flow of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._queue_max_delivered_unacked_msgs_per_flow = queue_max_delivered_unacked_msgs_per_flow

    @property
    def queue_max_msg_spool_usage(self):
        """Gets the queue_max_msg_spool_usage of this DmrClusterLink.  # noqa: E501

        The maximum message spool usage by the Queue (quota), in megabytes (MB).  # noqa: E501

        :return: The queue_max_msg_spool_usage of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_msg_spool_usage

    @queue_max_msg_spool_usage.setter
    def queue_max_msg_spool_usage(self, queue_max_msg_spool_usage):
        """Sets the queue_max_msg_spool_usage of this DmrClusterLink.

        The maximum message spool usage by the Queue (quota), in megabytes (MB).  # noqa: E501

        :param queue_max_msg_spool_usage: The queue_max_msg_spool_usage of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._queue_max_msg_spool_usage = queue_max_msg_spool_usage

    @property
    def queue_max_redelivery_count(self):
        """Gets the queue_max_redelivery_count of this DmrClusterLink.  # noqa: E501

        The maximum number of times the Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever.  # noqa: E501

        :return: The queue_max_redelivery_count of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_redelivery_count

    @queue_max_redelivery_count.setter
    def queue_max_redelivery_count(self, queue_max_redelivery_count):
        """Sets the queue_max_redelivery_count of this DmrClusterLink.

        The maximum number of times the Queue will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever.  # noqa: E501

        :param queue_max_redelivery_count: The queue_max_redelivery_count of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._queue_max_redelivery_count = queue_max_redelivery_count

    @property
    def queue_max_ttl(self):
        """Gets the queue_max_ttl of this DmrClusterLink.  # noqa: E501

        The maximum time in seconds a message can stay in the Queue when `queueRespectTtlEnabled` is `true`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `queueMaxTtl` configured for the Queue, is exceeded. A value of 0 disables expiry.  # noqa: E501

        :return: The queue_max_ttl of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._queue_max_ttl

    @queue_max_ttl.setter
    def queue_max_ttl(self, queue_max_ttl):
        """Sets the queue_max_ttl of this DmrClusterLink.

        The maximum time in seconds a message can stay in the Queue when `queueRespectTtlEnabled` is `true`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `queueMaxTtl` configured for the Queue, is exceeded. A value of 0 disables expiry.  # noqa: E501

        :param queue_max_ttl: The queue_max_ttl of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._queue_max_ttl = queue_max_ttl

    @property
    def queue_reject_msg_to_sender_on_discard_behavior(self):
        """Gets the queue_reject_msg_to_sender_on_discard_behavior of this DmrClusterLink.  # noqa: E501

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :return: The queue_reject_msg_to_sender_on_discard_behavior of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._queue_reject_msg_to_sender_on_discard_behavior

    @queue_reject_msg_to_sender_on_discard_behavior.setter
    def queue_reject_msg_to_sender_on_discard_behavior(self, queue_reject_msg_to_sender_on_discard_behavior):
        """Sets the queue_reject_msg_to_sender_on_discard_behavior of this DmrClusterLink.

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-queue-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Queue is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :param queue_reject_msg_to_sender_on_discard_behavior: The queue_reject_msg_to_sender_on_discard_behavior of this DmrClusterLink.  # noqa: E501
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
        """Gets the queue_respect_ttl_enabled of this DmrClusterLink.  # noqa: E501

        Indicates whether the the time-to-live (TTL) for messages in the Queue is respected. When enabled, expired messages are discarded or moved to the DMQ.  # noqa: E501

        :return: The queue_respect_ttl_enabled of this DmrClusterLink.  # noqa: E501
        :rtype: bool
        """
        return self._queue_respect_ttl_enabled

    @queue_respect_ttl_enabled.setter
    def queue_respect_ttl_enabled(self, queue_respect_ttl_enabled):
        """Sets the queue_respect_ttl_enabled of this DmrClusterLink.

        Indicates whether the the time-to-live (TTL) for messages in the Queue is respected. When enabled, expired messages are discarded or moved to the DMQ.  # noqa: E501

        :param queue_respect_ttl_enabled: The queue_respect_ttl_enabled of this DmrClusterLink.  # noqa: E501
        :type: bool
        """

        self._queue_respect_ttl_enabled = queue_respect_ttl_enabled

    @property
    def remote_node_name(self):
        """Gets the remote_node_name of this DmrClusterLink.  # noqa: E501

        The name of the node at the remote end of the Link.  # noqa: E501

        :return: The remote_node_name of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._remote_node_name

    @remote_node_name.setter
    def remote_node_name(self, remote_node_name):
        """Sets the remote_node_name of this DmrClusterLink.

        The name of the node at the remote end of the Link.  # noqa: E501

        :param remote_node_name: The remote_node_name of this DmrClusterLink.  # noqa: E501
        :type: str
        """

        self._remote_node_name = remote_node_name

    @property
    def span(self):
        """Gets the span of this DmrClusterLink.  # noqa: E501

        The span of the Link, either internal or external. Internal Links connect nodes within the same Cluster. External Links connect nodes within different Clusters. The allowed values and their meaning are:  <pre> \"internal\" - Link to same cluster. \"external\" - Link to other cluster. </pre>   # noqa: E501

        :return: The span of this DmrClusterLink.  # noqa: E501
        :rtype: str
        """
        return self._span

    @span.setter
    def span(self, span):
        """Sets the span of this DmrClusterLink.

        The span of the Link, either internal or external. Internal Links connect nodes within the same Cluster. External Links connect nodes within different Clusters. The allowed values and their meaning are:  <pre> \"internal\" - Link to same cluster. \"external\" - Link to other cluster. </pre>   # noqa: E501

        :param span: The span of this DmrClusterLink.  # noqa: E501
        :type: str
        """
        allowed_values = ["internal", "external"]  # noqa: E501
        if span not in allowed_values:
            raise ValueError(
                "Invalid value for `span` ({0}), must be one of {1}"  # noqa: E501
                .format(span, allowed_values)
            )

        self._span = span

    @property
    def transport_compressed_enabled(self):
        """Gets the transport_compressed_enabled of this DmrClusterLink.  # noqa: E501

        Indicates whether compression is enabled on the Link.  # noqa: E501

        :return: The transport_compressed_enabled of this DmrClusterLink.  # noqa: E501
        :rtype: bool
        """
        return self._transport_compressed_enabled

    @transport_compressed_enabled.setter
    def transport_compressed_enabled(self, transport_compressed_enabled):
        """Sets the transport_compressed_enabled of this DmrClusterLink.

        Indicates whether compression is enabled on the Link.  # noqa: E501

        :param transport_compressed_enabled: The transport_compressed_enabled of this DmrClusterLink.  # noqa: E501
        :type: bool
        """

        self._transport_compressed_enabled = transport_compressed_enabled

    @property
    def transport_tls_enabled(self):
        """Gets the transport_tls_enabled of this DmrClusterLink.  # noqa: E501

        Indicates whether encryption (TLS) is enabled on the Link.  # noqa: E501

        :return: The transport_tls_enabled of this DmrClusterLink.  # noqa: E501
        :rtype: bool
        """
        return self._transport_tls_enabled

    @transport_tls_enabled.setter
    def transport_tls_enabled(self, transport_tls_enabled):
        """Sets the transport_tls_enabled of this DmrClusterLink.

        Indicates whether encryption (TLS) is enabled on the Link.  # noqa: E501

        :param transport_tls_enabled: The transport_tls_enabled of this DmrClusterLink.  # noqa: E501
        :type: bool
        """

        self._transport_tls_enabled = transport_tls_enabled

    @property
    def up(self):
        """Gets the up of this DmrClusterLink.  # noqa: E501

        Indicates whether the Link is operationally up.  # noqa: E501

        :return: The up of this DmrClusterLink.  # noqa: E501
        :rtype: bool
        """
        return self._up

    @up.setter
    def up(self, up):
        """Sets the up of this DmrClusterLink.

        Indicates whether the Link is operationally up.  # noqa: E501

        :param up: The up of this DmrClusterLink.  # noqa: E501
        :type: bool
        """

        self._up = up

    @property
    def uptime(self):
        """Gets the uptime of this DmrClusterLink.  # noqa: E501

        The amount of time in seconds since the Link was up.  # noqa: E501

        :return: The uptime of this DmrClusterLink.  # noqa: E501
        :rtype: int
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """Sets the uptime of this DmrClusterLink.

        The amount of time in seconds since the Link was up.  # noqa: E501

        :param uptime: The uptime of this DmrClusterLink.  # noqa: E501
        :type: int
        """

        self._uptime = uptime

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
        if issubclass(DmrClusterLink, dict):
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
        if not isinstance(other, DmrClusterLink):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
