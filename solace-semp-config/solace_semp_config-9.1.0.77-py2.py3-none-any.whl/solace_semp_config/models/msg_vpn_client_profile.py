# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the  action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is a hidden maximum as to prevent overloading the system. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.11.00901000077
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnClientProfile(object):
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
        'allow_bridge_connections_enabled': 'bool',
        'allow_cut_through_forwarding_enabled': 'bool',
        'allow_guaranteed_endpoint_create_enabled': 'bool',
        'allow_guaranteed_msg_receive_enabled': 'bool',
        'allow_guaranteed_msg_send_enabled': 'bool',
        'allow_shared_subscriptions_enabled': 'bool',
        'allow_transacted_sessions_enabled': 'bool',
        'api_queue_management_copy_from_on_create_name': 'str',
        'api_topic_endpoint_management_copy_from_on_create_name': 'str',
        'client_profile_name': 'str',
        'compression_enabled': 'bool',
        'eliding_delay': 'int',
        'eliding_enabled': 'bool',
        'eliding_max_topic_count': 'int',
        'event_client_provisioned_endpoint_spool_usage_threshold': 'EventThresholdByPercent',
        'event_connection_count_per_client_username_threshold': 'EventThreshold',
        'event_egress_flow_count_threshold': 'EventThreshold',
        'event_endpoint_count_per_client_username_threshold': 'EventThreshold',
        'event_ingress_flow_count_threshold': 'EventThreshold',
        'event_service_smf_connection_count_per_client_username_threshold': 'EventThreshold',
        'event_service_web_connection_count_per_client_username_threshold': 'EventThreshold',
        'event_subscription_count_threshold': 'EventThreshold',
        'event_transacted_session_count_threshold': 'EventThreshold',
        'event_transaction_count_threshold': 'EventThreshold',
        'max_connection_count_per_client_username': 'int',
        'max_egress_flow_count': 'int',
        'max_endpoint_count_per_client_username': 'int',
        'max_ingress_flow_count': 'int',
        'max_subscription_count': 'int',
        'max_transacted_session_count': 'int',
        'max_transaction_count': 'int',
        'msg_vpn_name': 'str',
        'queue_control1_max_depth': 'int',
        'queue_control1_min_msg_burst': 'int',
        'queue_direct1_max_depth': 'int',
        'queue_direct1_min_msg_burst': 'int',
        'queue_direct2_max_depth': 'int',
        'queue_direct2_min_msg_burst': 'int',
        'queue_direct3_max_depth': 'int',
        'queue_direct3_min_msg_burst': 'int',
        'queue_guaranteed1_max_depth': 'int',
        'queue_guaranteed1_min_msg_burst': 'int',
        'reject_msg_to_sender_on_no_subscription_match_enabled': 'bool',
        'replication_allow_client_connect_when_standby_enabled': 'bool',
        'service_smf_max_connection_count_per_client_username': 'int',
        'service_web_inactive_timeout': 'int',
        'service_web_max_connection_count_per_client_username': 'int',
        'service_web_max_payload': 'int',
        'tcp_congestion_window_size': 'int',
        'tcp_keepalive_count': 'int',
        'tcp_keepalive_idle_time': 'int',
        'tcp_keepalive_interval': 'int',
        'tcp_max_segment_size': 'int',
        'tcp_max_window_size': 'int',
        'tls_allow_downgrade_to_plain_text_enabled': 'bool'
    }

    attribute_map = {
        'allow_bridge_connections_enabled': 'allowBridgeConnectionsEnabled',
        'allow_cut_through_forwarding_enabled': 'allowCutThroughForwardingEnabled',
        'allow_guaranteed_endpoint_create_enabled': 'allowGuaranteedEndpointCreateEnabled',
        'allow_guaranteed_msg_receive_enabled': 'allowGuaranteedMsgReceiveEnabled',
        'allow_guaranteed_msg_send_enabled': 'allowGuaranteedMsgSendEnabled',
        'allow_shared_subscriptions_enabled': 'allowSharedSubscriptionsEnabled',
        'allow_transacted_sessions_enabled': 'allowTransactedSessionsEnabled',
        'api_queue_management_copy_from_on_create_name': 'apiQueueManagementCopyFromOnCreateName',
        'api_topic_endpoint_management_copy_from_on_create_name': 'apiTopicEndpointManagementCopyFromOnCreateName',
        'client_profile_name': 'clientProfileName',
        'compression_enabled': 'compressionEnabled',
        'eliding_delay': 'elidingDelay',
        'eliding_enabled': 'elidingEnabled',
        'eliding_max_topic_count': 'elidingMaxTopicCount',
        'event_client_provisioned_endpoint_spool_usage_threshold': 'eventClientProvisionedEndpointSpoolUsageThreshold',
        'event_connection_count_per_client_username_threshold': 'eventConnectionCountPerClientUsernameThreshold',
        'event_egress_flow_count_threshold': 'eventEgressFlowCountThreshold',
        'event_endpoint_count_per_client_username_threshold': 'eventEndpointCountPerClientUsernameThreshold',
        'event_ingress_flow_count_threshold': 'eventIngressFlowCountThreshold',
        'event_service_smf_connection_count_per_client_username_threshold': 'eventServiceSmfConnectionCountPerClientUsernameThreshold',
        'event_service_web_connection_count_per_client_username_threshold': 'eventServiceWebConnectionCountPerClientUsernameThreshold',
        'event_subscription_count_threshold': 'eventSubscriptionCountThreshold',
        'event_transacted_session_count_threshold': 'eventTransactedSessionCountThreshold',
        'event_transaction_count_threshold': 'eventTransactionCountThreshold',
        'max_connection_count_per_client_username': 'maxConnectionCountPerClientUsername',
        'max_egress_flow_count': 'maxEgressFlowCount',
        'max_endpoint_count_per_client_username': 'maxEndpointCountPerClientUsername',
        'max_ingress_flow_count': 'maxIngressFlowCount',
        'max_subscription_count': 'maxSubscriptionCount',
        'max_transacted_session_count': 'maxTransactedSessionCount',
        'max_transaction_count': 'maxTransactionCount',
        'msg_vpn_name': 'msgVpnName',
        'queue_control1_max_depth': 'queueControl1MaxDepth',
        'queue_control1_min_msg_burst': 'queueControl1MinMsgBurst',
        'queue_direct1_max_depth': 'queueDirect1MaxDepth',
        'queue_direct1_min_msg_burst': 'queueDirect1MinMsgBurst',
        'queue_direct2_max_depth': 'queueDirect2MaxDepth',
        'queue_direct2_min_msg_burst': 'queueDirect2MinMsgBurst',
        'queue_direct3_max_depth': 'queueDirect3MaxDepth',
        'queue_direct3_min_msg_burst': 'queueDirect3MinMsgBurst',
        'queue_guaranteed1_max_depth': 'queueGuaranteed1MaxDepth',
        'queue_guaranteed1_min_msg_burst': 'queueGuaranteed1MinMsgBurst',
        'reject_msg_to_sender_on_no_subscription_match_enabled': 'rejectMsgToSenderOnNoSubscriptionMatchEnabled',
        'replication_allow_client_connect_when_standby_enabled': 'replicationAllowClientConnectWhenStandbyEnabled',
        'service_smf_max_connection_count_per_client_username': 'serviceSmfMaxConnectionCountPerClientUsername',
        'service_web_inactive_timeout': 'serviceWebInactiveTimeout',
        'service_web_max_connection_count_per_client_username': 'serviceWebMaxConnectionCountPerClientUsername',
        'service_web_max_payload': 'serviceWebMaxPayload',
        'tcp_congestion_window_size': 'tcpCongestionWindowSize',
        'tcp_keepalive_count': 'tcpKeepaliveCount',
        'tcp_keepalive_idle_time': 'tcpKeepaliveIdleTime',
        'tcp_keepalive_interval': 'tcpKeepaliveInterval',
        'tcp_max_segment_size': 'tcpMaxSegmentSize',
        'tcp_max_window_size': 'tcpMaxWindowSize',
        'tls_allow_downgrade_to_plain_text_enabled': 'tlsAllowDowngradeToPlainTextEnabled'
    }

    def __init__(self, allow_bridge_connections_enabled=None, allow_cut_through_forwarding_enabled=None, allow_guaranteed_endpoint_create_enabled=None, allow_guaranteed_msg_receive_enabled=None, allow_guaranteed_msg_send_enabled=None, allow_shared_subscriptions_enabled=None, allow_transacted_sessions_enabled=None, api_queue_management_copy_from_on_create_name=None, api_topic_endpoint_management_copy_from_on_create_name=None, client_profile_name=None, compression_enabled=None, eliding_delay=None, eliding_enabled=None, eliding_max_topic_count=None, event_client_provisioned_endpoint_spool_usage_threshold=None, event_connection_count_per_client_username_threshold=None, event_egress_flow_count_threshold=None, event_endpoint_count_per_client_username_threshold=None, event_ingress_flow_count_threshold=None, event_service_smf_connection_count_per_client_username_threshold=None, event_service_web_connection_count_per_client_username_threshold=None, event_subscription_count_threshold=None, event_transacted_session_count_threshold=None, event_transaction_count_threshold=None, max_connection_count_per_client_username=None, max_egress_flow_count=None, max_endpoint_count_per_client_username=None, max_ingress_flow_count=None, max_subscription_count=None, max_transacted_session_count=None, max_transaction_count=None, msg_vpn_name=None, queue_control1_max_depth=None, queue_control1_min_msg_burst=None, queue_direct1_max_depth=None, queue_direct1_min_msg_burst=None, queue_direct2_max_depth=None, queue_direct2_min_msg_burst=None, queue_direct3_max_depth=None, queue_direct3_min_msg_burst=None, queue_guaranteed1_max_depth=None, queue_guaranteed1_min_msg_burst=None, reject_msg_to_sender_on_no_subscription_match_enabled=None, replication_allow_client_connect_when_standby_enabled=None, service_smf_max_connection_count_per_client_username=None, service_web_inactive_timeout=None, service_web_max_connection_count_per_client_username=None, service_web_max_payload=None, tcp_congestion_window_size=None, tcp_keepalive_count=None, tcp_keepalive_idle_time=None, tcp_keepalive_interval=None, tcp_max_segment_size=None, tcp_max_window_size=None, tls_allow_downgrade_to_plain_text_enabled=None):  # noqa: E501
        """MsgVpnClientProfile - a model defined in Swagger"""  # noqa: E501

        self._allow_bridge_connections_enabled = None
        self._allow_cut_through_forwarding_enabled = None
        self._allow_guaranteed_endpoint_create_enabled = None
        self._allow_guaranteed_msg_receive_enabled = None
        self._allow_guaranteed_msg_send_enabled = None
        self._allow_shared_subscriptions_enabled = None
        self._allow_transacted_sessions_enabled = None
        self._api_queue_management_copy_from_on_create_name = None
        self._api_topic_endpoint_management_copy_from_on_create_name = None
        self._client_profile_name = None
        self._compression_enabled = None
        self._eliding_delay = None
        self._eliding_enabled = None
        self._eliding_max_topic_count = None
        self._event_client_provisioned_endpoint_spool_usage_threshold = None
        self._event_connection_count_per_client_username_threshold = None
        self._event_egress_flow_count_threshold = None
        self._event_endpoint_count_per_client_username_threshold = None
        self._event_ingress_flow_count_threshold = None
        self._event_service_smf_connection_count_per_client_username_threshold = None
        self._event_service_web_connection_count_per_client_username_threshold = None
        self._event_subscription_count_threshold = None
        self._event_transacted_session_count_threshold = None
        self._event_transaction_count_threshold = None
        self._max_connection_count_per_client_username = None
        self._max_egress_flow_count = None
        self._max_endpoint_count_per_client_username = None
        self._max_ingress_flow_count = None
        self._max_subscription_count = None
        self._max_transacted_session_count = None
        self._max_transaction_count = None
        self._msg_vpn_name = None
        self._queue_control1_max_depth = None
        self._queue_control1_min_msg_burst = None
        self._queue_direct1_max_depth = None
        self._queue_direct1_min_msg_burst = None
        self._queue_direct2_max_depth = None
        self._queue_direct2_min_msg_burst = None
        self._queue_direct3_max_depth = None
        self._queue_direct3_min_msg_burst = None
        self._queue_guaranteed1_max_depth = None
        self._queue_guaranteed1_min_msg_burst = None
        self._reject_msg_to_sender_on_no_subscription_match_enabled = None
        self._replication_allow_client_connect_when_standby_enabled = None
        self._service_smf_max_connection_count_per_client_username = None
        self._service_web_inactive_timeout = None
        self._service_web_max_connection_count_per_client_username = None
        self._service_web_max_payload = None
        self._tcp_congestion_window_size = None
        self._tcp_keepalive_count = None
        self._tcp_keepalive_idle_time = None
        self._tcp_keepalive_interval = None
        self._tcp_max_segment_size = None
        self._tcp_max_window_size = None
        self._tls_allow_downgrade_to_plain_text_enabled = None
        self.discriminator = None

        if allow_bridge_connections_enabled is not None:
            self.allow_bridge_connections_enabled = allow_bridge_connections_enabled
        if allow_cut_through_forwarding_enabled is not None:
            self.allow_cut_through_forwarding_enabled = allow_cut_through_forwarding_enabled
        if allow_guaranteed_endpoint_create_enabled is not None:
            self.allow_guaranteed_endpoint_create_enabled = allow_guaranteed_endpoint_create_enabled
        if allow_guaranteed_msg_receive_enabled is not None:
            self.allow_guaranteed_msg_receive_enabled = allow_guaranteed_msg_receive_enabled
        if allow_guaranteed_msg_send_enabled is not None:
            self.allow_guaranteed_msg_send_enabled = allow_guaranteed_msg_send_enabled
        if allow_shared_subscriptions_enabled is not None:
            self.allow_shared_subscriptions_enabled = allow_shared_subscriptions_enabled
        if allow_transacted_sessions_enabled is not None:
            self.allow_transacted_sessions_enabled = allow_transacted_sessions_enabled
        if api_queue_management_copy_from_on_create_name is not None:
            self.api_queue_management_copy_from_on_create_name = api_queue_management_copy_from_on_create_name
        if api_topic_endpoint_management_copy_from_on_create_name is not None:
            self.api_topic_endpoint_management_copy_from_on_create_name = api_topic_endpoint_management_copy_from_on_create_name
        if client_profile_name is not None:
            self.client_profile_name = client_profile_name
        if compression_enabled is not None:
            self.compression_enabled = compression_enabled
        if eliding_delay is not None:
            self.eliding_delay = eliding_delay
        if eliding_enabled is not None:
            self.eliding_enabled = eliding_enabled
        if eliding_max_topic_count is not None:
            self.eliding_max_topic_count = eliding_max_topic_count
        if event_client_provisioned_endpoint_spool_usage_threshold is not None:
            self.event_client_provisioned_endpoint_spool_usage_threshold = event_client_provisioned_endpoint_spool_usage_threshold
        if event_connection_count_per_client_username_threshold is not None:
            self.event_connection_count_per_client_username_threshold = event_connection_count_per_client_username_threshold
        if event_egress_flow_count_threshold is not None:
            self.event_egress_flow_count_threshold = event_egress_flow_count_threshold
        if event_endpoint_count_per_client_username_threshold is not None:
            self.event_endpoint_count_per_client_username_threshold = event_endpoint_count_per_client_username_threshold
        if event_ingress_flow_count_threshold is not None:
            self.event_ingress_flow_count_threshold = event_ingress_flow_count_threshold
        if event_service_smf_connection_count_per_client_username_threshold is not None:
            self.event_service_smf_connection_count_per_client_username_threshold = event_service_smf_connection_count_per_client_username_threshold
        if event_service_web_connection_count_per_client_username_threshold is not None:
            self.event_service_web_connection_count_per_client_username_threshold = event_service_web_connection_count_per_client_username_threshold
        if event_subscription_count_threshold is not None:
            self.event_subscription_count_threshold = event_subscription_count_threshold
        if event_transacted_session_count_threshold is not None:
            self.event_transacted_session_count_threshold = event_transacted_session_count_threshold
        if event_transaction_count_threshold is not None:
            self.event_transaction_count_threshold = event_transaction_count_threshold
        if max_connection_count_per_client_username is not None:
            self.max_connection_count_per_client_username = max_connection_count_per_client_username
        if max_egress_flow_count is not None:
            self.max_egress_flow_count = max_egress_flow_count
        if max_endpoint_count_per_client_username is not None:
            self.max_endpoint_count_per_client_username = max_endpoint_count_per_client_username
        if max_ingress_flow_count is not None:
            self.max_ingress_flow_count = max_ingress_flow_count
        if max_subscription_count is not None:
            self.max_subscription_count = max_subscription_count
        if max_transacted_session_count is not None:
            self.max_transacted_session_count = max_transacted_session_count
        if max_transaction_count is not None:
            self.max_transaction_count = max_transaction_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if queue_control1_max_depth is not None:
            self.queue_control1_max_depth = queue_control1_max_depth
        if queue_control1_min_msg_burst is not None:
            self.queue_control1_min_msg_burst = queue_control1_min_msg_burst
        if queue_direct1_max_depth is not None:
            self.queue_direct1_max_depth = queue_direct1_max_depth
        if queue_direct1_min_msg_burst is not None:
            self.queue_direct1_min_msg_burst = queue_direct1_min_msg_burst
        if queue_direct2_max_depth is not None:
            self.queue_direct2_max_depth = queue_direct2_max_depth
        if queue_direct2_min_msg_burst is not None:
            self.queue_direct2_min_msg_burst = queue_direct2_min_msg_burst
        if queue_direct3_max_depth is not None:
            self.queue_direct3_max_depth = queue_direct3_max_depth
        if queue_direct3_min_msg_burst is not None:
            self.queue_direct3_min_msg_burst = queue_direct3_min_msg_burst
        if queue_guaranteed1_max_depth is not None:
            self.queue_guaranteed1_max_depth = queue_guaranteed1_max_depth
        if queue_guaranteed1_min_msg_burst is not None:
            self.queue_guaranteed1_min_msg_burst = queue_guaranteed1_min_msg_burst
        if reject_msg_to_sender_on_no_subscription_match_enabled is not None:
            self.reject_msg_to_sender_on_no_subscription_match_enabled = reject_msg_to_sender_on_no_subscription_match_enabled
        if replication_allow_client_connect_when_standby_enabled is not None:
            self.replication_allow_client_connect_when_standby_enabled = replication_allow_client_connect_when_standby_enabled
        if service_smf_max_connection_count_per_client_username is not None:
            self.service_smf_max_connection_count_per_client_username = service_smf_max_connection_count_per_client_username
        if service_web_inactive_timeout is not None:
            self.service_web_inactive_timeout = service_web_inactive_timeout
        if service_web_max_connection_count_per_client_username is not None:
            self.service_web_max_connection_count_per_client_username = service_web_max_connection_count_per_client_username
        if service_web_max_payload is not None:
            self.service_web_max_payload = service_web_max_payload
        if tcp_congestion_window_size is not None:
            self.tcp_congestion_window_size = tcp_congestion_window_size
        if tcp_keepalive_count is not None:
            self.tcp_keepalive_count = tcp_keepalive_count
        if tcp_keepalive_idle_time is not None:
            self.tcp_keepalive_idle_time = tcp_keepalive_idle_time
        if tcp_keepalive_interval is not None:
            self.tcp_keepalive_interval = tcp_keepalive_interval
        if tcp_max_segment_size is not None:
            self.tcp_max_segment_size = tcp_max_segment_size
        if tcp_max_window_size is not None:
            self.tcp_max_window_size = tcp_max_window_size
        if tls_allow_downgrade_to_plain_text_enabled is not None:
            self.tls_allow_downgrade_to_plain_text_enabled = tls_allow_downgrade_to_plain_text_enabled

    @property
    def allow_bridge_connections_enabled(self):
        """Gets the allow_bridge_connections_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing Bridge clients using the Client Profile to connect. Changing this setting does not affect existing Bridge client connections. The default value is `false`.  # noqa: E501

        :return: The allow_bridge_connections_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_bridge_connections_enabled

    @allow_bridge_connections_enabled.setter
    def allow_bridge_connections_enabled(self, allow_bridge_connections_enabled):
        """Sets the allow_bridge_connections_enabled of this MsgVpnClientProfile.

        Enable or disable allowing Bridge clients using the Client Profile to connect. Changing this setting does not affect existing Bridge client connections. The default value is `false`.  # noqa: E501

        :param allow_bridge_connections_enabled: The allow_bridge_connections_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_bridge_connections_enabled = allow_bridge_connections_enabled

    @property
    def allow_cut_through_forwarding_enabled(self):
        """Gets the allow_cut_through_forwarding_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to bind to endpoints with the cut-through forwarding delivery mode. Changing this value does not affect existing client connections. The default value is `false`.  # noqa: E501

        :return: The allow_cut_through_forwarding_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_cut_through_forwarding_enabled

    @allow_cut_through_forwarding_enabled.setter
    def allow_cut_through_forwarding_enabled(self, allow_cut_through_forwarding_enabled):
        """Sets the allow_cut_through_forwarding_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to bind to endpoints with the cut-through forwarding delivery mode. Changing this value does not affect existing client connections. The default value is `false`.  # noqa: E501

        :param allow_cut_through_forwarding_enabled: The allow_cut_through_forwarding_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_cut_through_forwarding_enabled = allow_cut_through_forwarding_enabled

    @property
    def allow_guaranteed_endpoint_create_enabled(self):
        """Gets the allow_guaranteed_endpoint_create_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to create topic endponts or queues. Changing this value does not affect existing client connections. The default value is `false`.  # noqa: E501

        :return: The allow_guaranteed_endpoint_create_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_guaranteed_endpoint_create_enabled

    @allow_guaranteed_endpoint_create_enabled.setter
    def allow_guaranteed_endpoint_create_enabled(self, allow_guaranteed_endpoint_create_enabled):
        """Sets the allow_guaranteed_endpoint_create_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to create topic endponts or queues. Changing this value does not affect existing client connections. The default value is `false`.  # noqa: E501

        :param allow_guaranteed_endpoint_create_enabled: The allow_guaranteed_endpoint_create_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_guaranteed_endpoint_create_enabled = allow_guaranteed_endpoint_create_enabled

    @property
    def allow_guaranteed_msg_receive_enabled(self):
        """Gets the allow_guaranteed_msg_receive_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to receive guaranteed messages. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :return: The allow_guaranteed_msg_receive_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_guaranteed_msg_receive_enabled

    @allow_guaranteed_msg_receive_enabled.setter
    def allow_guaranteed_msg_receive_enabled(self, allow_guaranteed_msg_receive_enabled):
        """Sets the allow_guaranteed_msg_receive_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to receive guaranteed messages. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :param allow_guaranteed_msg_receive_enabled: The allow_guaranteed_msg_receive_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_guaranteed_msg_receive_enabled = allow_guaranteed_msg_receive_enabled

    @property
    def allow_guaranteed_msg_send_enabled(self):
        """Gets the allow_guaranteed_msg_send_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to send guaranteed messages. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :return: The allow_guaranteed_msg_send_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_guaranteed_msg_send_enabled

    @allow_guaranteed_msg_send_enabled.setter
    def allow_guaranteed_msg_send_enabled(self, allow_guaranteed_msg_send_enabled):
        """Sets the allow_guaranteed_msg_send_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to send guaranteed messages. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :param allow_guaranteed_msg_send_enabled: The allow_guaranteed_msg_send_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_guaranteed_msg_send_enabled = allow_guaranteed_msg_send_enabled

    @property
    def allow_shared_subscriptions_enabled(self):
        """Gets the allow_shared_subscriptions_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing shared subscriptions. The default value is `false`. Available since 2.11.  # noqa: E501

        :return: The allow_shared_subscriptions_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_shared_subscriptions_enabled

    @allow_shared_subscriptions_enabled.setter
    def allow_shared_subscriptions_enabled(self, allow_shared_subscriptions_enabled):
        """Sets the allow_shared_subscriptions_enabled of this MsgVpnClientProfile.

        Enable or disable allowing shared subscriptions. The default value is `false`. Available since 2.11.  # noqa: E501

        :param allow_shared_subscriptions_enabled: The allow_shared_subscriptions_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_shared_subscriptions_enabled = allow_shared_subscriptions_enabled

    @property
    def allow_transacted_sessions_enabled(self):
        """Gets the allow_transacted_sessions_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to establish transacted sessions. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :return: The allow_transacted_sessions_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._allow_transacted_sessions_enabled

    @allow_transacted_sessions_enabled.setter
    def allow_transacted_sessions_enabled(self, allow_transacted_sessions_enabled):
        """Sets the allow_transacted_sessions_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to establish transacted sessions. Changing this setting does not affect existing client connections. The default value is `false`.  # noqa: E501

        :param allow_transacted_sessions_enabled: The allow_transacted_sessions_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._allow_transacted_sessions_enabled = allow_transacted_sessions_enabled

    @property
    def api_queue_management_copy_from_on_create_name(self):
        """Gets the api_queue_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501

        The name of a queue to copy settings from when a new queue is created by a client using the Client Profile. The referenced queue must exist in the Message VPN. The default value is `\"\"`.  # noqa: E501

        :return: The api_queue_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501
        :rtype: str
        """
        return self._api_queue_management_copy_from_on_create_name

    @api_queue_management_copy_from_on_create_name.setter
    def api_queue_management_copy_from_on_create_name(self, api_queue_management_copy_from_on_create_name):
        """Sets the api_queue_management_copy_from_on_create_name of this MsgVpnClientProfile.

        The name of a queue to copy settings from when a new queue is created by a client using the Client Profile. The referenced queue must exist in the Message VPN. The default value is `\"\"`.  # noqa: E501

        :param api_queue_management_copy_from_on_create_name: The api_queue_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501
        :type: str
        """

        self._api_queue_management_copy_from_on_create_name = api_queue_management_copy_from_on_create_name

    @property
    def api_topic_endpoint_management_copy_from_on_create_name(self):
        """Gets the api_topic_endpoint_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501

        The name of a topic endpoint to copy settings from when a new topic endpoint is created by a client using the Client Profile. The referenced topic endpoint must exist in the Message VPN. The default value is `\"\"`.  # noqa: E501

        :return: The api_topic_endpoint_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501
        :rtype: str
        """
        return self._api_topic_endpoint_management_copy_from_on_create_name

    @api_topic_endpoint_management_copy_from_on_create_name.setter
    def api_topic_endpoint_management_copy_from_on_create_name(self, api_topic_endpoint_management_copy_from_on_create_name):
        """Sets the api_topic_endpoint_management_copy_from_on_create_name of this MsgVpnClientProfile.

        The name of a topic endpoint to copy settings from when a new topic endpoint is created by a client using the Client Profile. The referenced topic endpoint must exist in the Message VPN. The default value is `\"\"`.  # noqa: E501

        :param api_topic_endpoint_management_copy_from_on_create_name: The api_topic_endpoint_management_copy_from_on_create_name of this MsgVpnClientProfile.  # noqa: E501
        :type: str
        """

        self._api_topic_endpoint_management_copy_from_on_create_name = api_topic_endpoint_management_copy_from_on_create_name

    @property
    def client_profile_name(self):
        """Gets the client_profile_name of this MsgVpnClientProfile.  # noqa: E501

        The name of the Client Profile.  # noqa: E501

        :return: The client_profile_name of this MsgVpnClientProfile.  # noqa: E501
        :rtype: str
        """
        return self._client_profile_name

    @client_profile_name.setter
    def client_profile_name(self, client_profile_name):
        """Sets the client_profile_name of this MsgVpnClientProfile.

        The name of the Client Profile.  # noqa: E501

        :param client_profile_name: The client_profile_name of this MsgVpnClientProfile.  # noqa: E501
        :type: str
        """

        self._client_profile_name = client_profile_name

    @property
    def compression_enabled(self):
        """Gets the compression_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to use compression. The default value is `true`. Available since 2.10.  # noqa: E501

        :return: The compression_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._compression_enabled

    @compression_enabled.setter
    def compression_enabled(self, compression_enabled):
        """Sets the compression_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to use compression. The default value is `true`. Available since 2.10.  # noqa: E501

        :param compression_enabled: The compression_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._compression_enabled = compression_enabled

    @property
    def eliding_delay(self):
        """Gets the eliding_delay of this MsgVpnClientProfile.  # noqa: E501

        The amount of time to delay the delivery of messages to clients using the Client Profile after the initial message has been delivered (the eliding delay interval), in milliseconds. A value of 0 means there is no delay in delivering messages to clients. The default value is `0`.  # noqa: E501

        :return: The eliding_delay of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._eliding_delay

    @eliding_delay.setter
    def eliding_delay(self, eliding_delay):
        """Sets the eliding_delay of this MsgVpnClientProfile.

        The amount of time to delay the delivery of messages to clients using the Client Profile after the initial message has been delivered (the eliding delay interval), in milliseconds. A value of 0 means there is no delay in delivering messages to clients. The default value is `0`.  # noqa: E501

        :param eliding_delay: The eliding_delay of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._eliding_delay = eliding_delay

    @property
    def eliding_enabled(self):
        """Gets the eliding_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable message eliding for clients using the Client Profile. The default value is `false`.  # noqa: E501

        :return: The eliding_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._eliding_enabled

    @eliding_enabled.setter
    def eliding_enabled(self, eliding_enabled):
        """Sets the eliding_enabled of this MsgVpnClientProfile.

        Enable or disable message eliding for clients using the Client Profile. The default value is `false`.  # noqa: E501

        :param eliding_enabled: The eliding_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._eliding_enabled = eliding_enabled

    @property
    def eliding_max_topic_count(self):
        """Gets the eliding_max_topic_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of topics tracked for message eliding per client connection using the Client Profile. The default value is `256`.  # noqa: E501

        :return: The eliding_max_topic_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._eliding_max_topic_count

    @eliding_max_topic_count.setter
    def eliding_max_topic_count(self, eliding_max_topic_count):
        """Sets the eliding_max_topic_count of this MsgVpnClientProfile.

        The maximum number of topics tracked for message eliding per client connection using the Client Profile. The default value is `256`.  # noqa: E501

        :param eliding_max_topic_count: The eliding_max_topic_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._eliding_max_topic_count = eliding_max_topic_count

    @property
    def event_client_provisioned_endpoint_spool_usage_threshold(self):
        """Gets the event_client_provisioned_endpoint_spool_usage_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_client_provisioned_endpoint_spool_usage_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._event_client_provisioned_endpoint_spool_usage_threshold

    @event_client_provisioned_endpoint_spool_usage_threshold.setter
    def event_client_provisioned_endpoint_spool_usage_threshold(self, event_client_provisioned_endpoint_spool_usage_threshold):
        """Sets the event_client_provisioned_endpoint_spool_usage_threshold of this MsgVpnClientProfile.


        :param event_client_provisioned_endpoint_spool_usage_threshold: The event_client_provisioned_endpoint_spool_usage_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._event_client_provisioned_endpoint_spool_usage_threshold = event_client_provisioned_endpoint_spool_usage_threshold

    @property
    def event_connection_count_per_client_username_threshold(self):
        """Gets the event_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_connection_count_per_client_username_threshold

    @event_connection_count_per_client_username_threshold.setter
    def event_connection_count_per_client_username_threshold(self, event_connection_count_per_client_username_threshold):
        """Sets the event_connection_count_per_client_username_threshold of this MsgVpnClientProfile.


        :param event_connection_count_per_client_username_threshold: The event_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_connection_count_per_client_username_threshold = event_connection_count_per_client_username_threshold

    @property
    def event_egress_flow_count_threshold(self):
        """Gets the event_egress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_egress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_egress_flow_count_threshold

    @event_egress_flow_count_threshold.setter
    def event_egress_flow_count_threshold(self, event_egress_flow_count_threshold):
        """Sets the event_egress_flow_count_threshold of this MsgVpnClientProfile.


        :param event_egress_flow_count_threshold: The event_egress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_egress_flow_count_threshold = event_egress_flow_count_threshold

    @property
    def event_endpoint_count_per_client_username_threshold(self):
        """Gets the event_endpoint_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_endpoint_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_endpoint_count_per_client_username_threshold

    @event_endpoint_count_per_client_username_threshold.setter
    def event_endpoint_count_per_client_username_threshold(self, event_endpoint_count_per_client_username_threshold):
        """Sets the event_endpoint_count_per_client_username_threshold of this MsgVpnClientProfile.


        :param event_endpoint_count_per_client_username_threshold: The event_endpoint_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_endpoint_count_per_client_username_threshold = event_endpoint_count_per_client_username_threshold

    @property
    def event_ingress_flow_count_threshold(self):
        """Gets the event_ingress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_ingress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_ingress_flow_count_threshold

    @event_ingress_flow_count_threshold.setter
    def event_ingress_flow_count_threshold(self, event_ingress_flow_count_threshold):
        """Sets the event_ingress_flow_count_threshold of this MsgVpnClientProfile.


        :param event_ingress_flow_count_threshold: The event_ingress_flow_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_ingress_flow_count_threshold = event_ingress_flow_count_threshold

    @property
    def event_service_smf_connection_count_per_client_username_threshold(self):
        """Gets the event_service_smf_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_service_smf_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_smf_connection_count_per_client_username_threshold

    @event_service_smf_connection_count_per_client_username_threshold.setter
    def event_service_smf_connection_count_per_client_username_threshold(self, event_service_smf_connection_count_per_client_username_threshold):
        """Sets the event_service_smf_connection_count_per_client_username_threshold of this MsgVpnClientProfile.


        :param event_service_smf_connection_count_per_client_username_threshold: The event_service_smf_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_smf_connection_count_per_client_username_threshold = event_service_smf_connection_count_per_client_username_threshold

    @property
    def event_service_web_connection_count_per_client_username_threshold(self):
        """Gets the event_service_web_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_service_web_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_web_connection_count_per_client_username_threshold

    @event_service_web_connection_count_per_client_username_threshold.setter
    def event_service_web_connection_count_per_client_username_threshold(self, event_service_web_connection_count_per_client_username_threshold):
        """Sets the event_service_web_connection_count_per_client_username_threshold of this MsgVpnClientProfile.


        :param event_service_web_connection_count_per_client_username_threshold: The event_service_web_connection_count_per_client_username_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_web_connection_count_per_client_username_threshold = event_service_web_connection_count_per_client_username_threshold

    @property
    def event_subscription_count_threshold(self):
        """Gets the event_subscription_count_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_subscription_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_subscription_count_threshold

    @event_subscription_count_threshold.setter
    def event_subscription_count_threshold(self, event_subscription_count_threshold):
        """Sets the event_subscription_count_threshold of this MsgVpnClientProfile.


        :param event_subscription_count_threshold: The event_subscription_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_subscription_count_threshold = event_subscription_count_threshold

    @property
    def event_transacted_session_count_threshold(self):
        """Gets the event_transacted_session_count_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_transacted_session_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_transacted_session_count_threshold

    @event_transacted_session_count_threshold.setter
    def event_transacted_session_count_threshold(self, event_transacted_session_count_threshold):
        """Sets the event_transacted_session_count_threshold of this MsgVpnClientProfile.


        :param event_transacted_session_count_threshold: The event_transacted_session_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_transacted_session_count_threshold = event_transacted_session_count_threshold

    @property
    def event_transaction_count_threshold(self):
        """Gets the event_transaction_count_threshold of this MsgVpnClientProfile.  # noqa: E501


        :return: The event_transaction_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_transaction_count_threshold

    @event_transaction_count_threshold.setter
    def event_transaction_count_threshold(self, event_transaction_count_threshold):
        """Sets the event_transaction_count_threshold of this MsgVpnClientProfile.


        :param event_transaction_count_threshold: The event_transaction_count_threshold of this MsgVpnClientProfile.  # noqa: E501
        :type: EventThreshold
        """

        self._event_transaction_count_threshold = event_transaction_count_threshold

    @property
    def max_connection_count_per_client_username(self):
        """Gets the max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_connection_count_per_client_username

    @max_connection_count_per_client_username.setter
    def max_connection_count_per_client_username(self, max_connection_count_per_client_username):
        """Sets the max_connection_count_per_client_username of this MsgVpnClientProfile.

        The maximum number of client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param max_connection_count_per_client_username: The max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_connection_count_per_client_username = max_connection_count_per_client_username

    @property
    def max_egress_flow_count(self):
        """Gets the max_egress_flow_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of transmit flows per client using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The max_egress_flow_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_egress_flow_count

    @max_egress_flow_count.setter
    def max_egress_flow_count(self, max_egress_flow_count):
        """Sets the max_egress_flow_count of this MsgVpnClientProfile.

        The maximum number of transmit flows per client using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param max_egress_flow_count: The max_egress_flow_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_egress_flow_count = max_egress_flow_count

    @property
    def max_endpoint_count_per_client_username(self):
        """Gets the max_endpoint_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of queues and topic endpoints per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The max_endpoint_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_endpoint_count_per_client_username

    @max_endpoint_count_per_client_username.setter
    def max_endpoint_count_per_client_username(self, max_endpoint_count_per_client_username):
        """Sets the max_endpoint_count_per_client_username of this MsgVpnClientProfile.

        The maximum number of queues and topic endpoints per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param max_endpoint_count_per_client_username: The max_endpoint_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_endpoint_count_per_client_username = max_endpoint_count_per_client_username

    @property
    def max_ingress_flow_count(self):
        """Gets the max_ingress_flow_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of receive flows per client using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The max_ingress_flow_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_ingress_flow_count

    @max_ingress_flow_count.setter
    def max_ingress_flow_count(self, max_ingress_flow_count):
        """Sets the max_ingress_flow_count of this MsgVpnClientProfile.

        The maximum number of receive flows per client using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param max_ingress_flow_count: The max_ingress_flow_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_ingress_flow_count = max_ingress_flow_count

    @property
    def max_subscription_count(self):
        """Gets the max_subscription_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of subscriptions per client using the Client Profile. The default varies by platform.  # noqa: E501

        :return: The max_subscription_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_subscription_count

    @max_subscription_count.setter
    def max_subscription_count(self, max_subscription_count):
        """Sets the max_subscription_count of this MsgVpnClientProfile.

        The maximum number of subscriptions per client using the Client Profile. The default varies by platform.  # noqa: E501

        :param max_subscription_count: The max_subscription_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_subscription_count = max_subscription_count

    @property
    def max_transacted_session_count(self):
        """Gets the max_transacted_session_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of transacted sessions per client using the Client Profile. The default value is `10`.  # noqa: E501

        :return: The max_transacted_session_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_transacted_session_count

    @max_transacted_session_count.setter
    def max_transacted_session_count(self, max_transacted_session_count):
        """Sets the max_transacted_session_count of this MsgVpnClientProfile.

        The maximum number of transacted sessions per client using the Client Profile. The default value is `10`.  # noqa: E501

        :param max_transacted_session_count: The max_transacted_session_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_transacted_session_count = max_transacted_session_count

    @property
    def max_transaction_count(self):
        """Gets the max_transaction_count of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of transactions per client using the Client Profile. The default varies by platform.  # noqa: E501

        :return: The max_transaction_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._max_transaction_count

    @max_transaction_count.setter
    def max_transaction_count(self, max_transaction_count):
        """Sets the max_transaction_count of this MsgVpnClientProfile.

        The maximum number of transactions per client using the Client Profile. The default varies by platform.  # noqa: E501

        :param max_transaction_count: The max_transaction_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._max_transaction_count = max_transaction_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnClientProfile.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnClientProfile.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnClientProfile.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnClientProfile.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def queue_control1_max_depth(self):
        """Gets the queue_control1_max_depth of this MsgVpnClientProfile.  # noqa: E501

        The maximum depth of the \"Control 1\" (C-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :return: The queue_control1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_control1_max_depth

    @queue_control1_max_depth.setter
    def queue_control1_max_depth(self, queue_control1_max_depth):
        """Sets the queue_control1_max_depth of this MsgVpnClientProfile.

        The maximum depth of the \"Control 1\" (C-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :param queue_control1_max_depth: The queue_control1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_control1_max_depth = queue_control1_max_depth

    @property
    def queue_control1_min_msg_burst(self):
        """Gets the queue_control1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501

        The number of messages that are always allowed entry into the \"Control 1\" (C-1) priority queue, regardless of the \"queueControl1MaxDepth\" value. The default value is `4`.  # noqa: E501

        :return: The queue_control1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_control1_min_msg_burst

    @queue_control1_min_msg_burst.setter
    def queue_control1_min_msg_burst(self, queue_control1_min_msg_burst):
        """Sets the queue_control1_min_msg_burst of this MsgVpnClientProfile.

        The number of messages that are always allowed entry into the \"Control 1\" (C-1) priority queue, regardless of the \"queueControl1MaxDepth\" value. The default value is `4`.  # noqa: E501

        :param queue_control1_min_msg_burst: The queue_control1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_control1_min_msg_burst = queue_control1_min_msg_burst

    @property
    def queue_direct1_max_depth(self):
        """Gets the queue_direct1_max_depth of this MsgVpnClientProfile.  # noqa: E501

        The maximum depth of the \"Direct 1\" (D-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :return: The queue_direct1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct1_max_depth

    @queue_direct1_max_depth.setter
    def queue_direct1_max_depth(self, queue_direct1_max_depth):
        """Sets the queue_direct1_max_depth of this MsgVpnClientProfile.

        The maximum depth of the \"Direct 1\" (D-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :param queue_direct1_max_depth: The queue_direct1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct1_max_depth = queue_direct1_max_depth

    @property
    def queue_direct1_min_msg_burst(self):
        """Gets the queue_direct1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 1\" (D-1) priority queue, regardless of the \"queueDirect1MaxDepth\" value. The default value is `4`.  # noqa: E501

        :return: The queue_direct1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct1_min_msg_burst

    @queue_direct1_min_msg_burst.setter
    def queue_direct1_min_msg_burst(self, queue_direct1_min_msg_burst):
        """Sets the queue_direct1_min_msg_burst of this MsgVpnClientProfile.

        The number of messages that are always allowed entry into the \"Direct 1\" (D-1) priority queue, regardless of the \"queueDirect1MaxDepth\" value. The default value is `4`.  # noqa: E501

        :param queue_direct1_min_msg_burst: The queue_direct1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct1_min_msg_burst = queue_direct1_min_msg_burst

    @property
    def queue_direct2_max_depth(self):
        """Gets the queue_direct2_max_depth of this MsgVpnClientProfile.  # noqa: E501

        The maximum depth of the \"Direct 2\" (D-2) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :return: The queue_direct2_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct2_max_depth

    @queue_direct2_max_depth.setter
    def queue_direct2_max_depth(self, queue_direct2_max_depth):
        """Sets the queue_direct2_max_depth of this MsgVpnClientProfile.

        The maximum depth of the \"Direct 2\" (D-2) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :param queue_direct2_max_depth: The queue_direct2_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct2_max_depth = queue_direct2_max_depth

    @property
    def queue_direct2_min_msg_burst(self):
        """Gets the queue_direct2_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 2\" (D-2) priority queue, regardless of the \"queueDirect2MaxDepth\" value. The default value is `4`.  # noqa: E501

        :return: The queue_direct2_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct2_min_msg_burst

    @queue_direct2_min_msg_burst.setter
    def queue_direct2_min_msg_burst(self, queue_direct2_min_msg_burst):
        """Sets the queue_direct2_min_msg_burst of this MsgVpnClientProfile.

        The number of messages that are always allowed entry into the \"Direct 2\" (D-2) priority queue, regardless of the \"queueDirect2MaxDepth\" value. The default value is `4`.  # noqa: E501

        :param queue_direct2_min_msg_burst: The queue_direct2_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct2_min_msg_burst = queue_direct2_min_msg_burst

    @property
    def queue_direct3_max_depth(self):
        """Gets the queue_direct3_max_depth of this MsgVpnClientProfile.  # noqa: E501

        The maximum depth of the \"Direct 3\" (D-3) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :return: The queue_direct3_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct3_max_depth

    @queue_direct3_max_depth.setter
    def queue_direct3_max_depth(self, queue_direct3_max_depth):
        """Sets the queue_direct3_max_depth of this MsgVpnClientProfile.

        The maximum depth of the \"Direct 3\" (D-3) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :param queue_direct3_max_depth: The queue_direct3_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct3_max_depth = queue_direct3_max_depth

    @property
    def queue_direct3_min_msg_burst(self):
        """Gets the queue_direct3_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501

        The number of messages that are always allowed entry into the \"Direct 3\" (D-3) priority queue, regardless of the \"queueDirect3MaxDepth\" value. The default value is `4`.  # noqa: E501

        :return: The queue_direct3_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_direct3_min_msg_burst

    @queue_direct3_min_msg_burst.setter
    def queue_direct3_min_msg_burst(self, queue_direct3_min_msg_burst):
        """Sets the queue_direct3_min_msg_burst of this MsgVpnClientProfile.

        The number of messages that are always allowed entry into the \"Direct 3\" (D-3) priority queue, regardless of the \"queueDirect3MaxDepth\" value. The default value is `4`.  # noqa: E501

        :param queue_direct3_min_msg_burst: The queue_direct3_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_direct3_min_msg_burst = queue_direct3_min_msg_burst

    @property
    def queue_guaranteed1_max_depth(self):
        """Gets the queue_guaranteed1_max_depth of this MsgVpnClientProfile.  # noqa: E501

        The maximum depth of the \"Guaranteed 1\" (G-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :return: The queue_guaranteed1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_guaranteed1_max_depth

    @queue_guaranteed1_max_depth.setter
    def queue_guaranteed1_max_depth(self, queue_guaranteed1_max_depth):
        """Sets the queue_guaranteed1_max_depth of this MsgVpnClientProfile.

        The maximum depth of the \"Guaranteed 1\" (G-1) priority queue, in work units. Each work unit is 2048 bytes of message data. The default value is `20000`.  # noqa: E501

        :param queue_guaranteed1_max_depth: The queue_guaranteed1_max_depth of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_guaranteed1_max_depth = queue_guaranteed1_max_depth

    @property
    def queue_guaranteed1_min_msg_burst(self):
        """Gets the queue_guaranteed1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501

        The number of messages that are always allowed entry into the \"Guaranteed 1\" (G-3) priority queue, regardless of the \"queueGuaranteed1MaxDepth\" value. The default value is `255`.  # noqa: E501

        :return: The queue_guaranteed1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._queue_guaranteed1_min_msg_burst

    @queue_guaranteed1_min_msg_burst.setter
    def queue_guaranteed1_min_msg_burst(self, queue_guaranteed1_min_msg_burst):
        """Sets the queue_guaranteed1_min_msg_burst of this MsgVpnClientProfile.

        The number of messages that are always allowed entry into the \"Guaranteed 1\" (G-3) priority queue, regardless of the \"queueGuaranteed1MaxDepth\" value. The default value is `255`.  # noqa: E501

        :param queue_guaranteed1_min_msg_burst: The queue_guaranteed1_min_msg_burst of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._queue_guaranteed1_min_msg_burst = queue_guaranteed1_min_msg_burst

    @property
    def reject_msg_to_sender_on_no_subscription_match_enabled(self):
        """Gets the reject_msg_to_sender_on_no_subscription_match_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable the sending of a negative acknowledgement (NACK) to a client using the Client Profile when discarding a guaranteed message due to no matching subscription found. The default value is `false`.  # noqa: E501

        :return: The reject_msg_to_sender_on_no_subscription_match_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._reject_msg_to_sender_on_no_subscription_match_enabled

    @reject_msg_to_sender_on_no_subscription_match_enabled.setter
    def reject_msg_to_sender_on_no_subscription_match_enabled(self, reject_msg_to_sender_on_no_subscription_match_enabled):
        """Sets the reject_msg_to_sender_on_no_subscription_match_enabled of this MsgVpnClientProfile.

        Enable or disable the sending of a negative acknowledgement (NACK) to a client using the Client Profile when discarding a guaranteed message due to no matching subscription found. The default value is `false`.  # noqa: E501

        :param reject_msg_to_sender_on_no_subscription_match_enabled: The reject_msg_to_sender_on_no_subscription_match_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._reject_msg_to_sender_on_no_subscription_match_enabled = reject_msg_to_sender_on_no_subscription_match_enabled

    @property
    def replication_allow_client_connect_when_standby_enabled(self):
        """Gets the replication_allow_client_connect_when_standby_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing clients using the Client Profile to connect to the Message VPN when its replication state is standby. The default value is `false`.  # noqa: E501

        :return: The replication_allow_client_connect_when_standby_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._replication_allow_client_connect_when_standby_enabled

    @replication_allow_client_connect_when_standby_enabled.setter
    def replication_allow_client_connect_when_standby_enabled(self, replication_allow_client_connect_when_standby_enabled):
        """Sets the replication_allow_client_connect_when_standby_enabled of this MsgVpnClientProfile.

        Enable or disable allowing clients using the Client Profile to connect to the Message VPN when its replication state is standby. The default value is `false`.  # noqa: E501

        :param replication_allow_client_connect_when_standby_enabled: The replication_allow_client_connect_when_standby_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._replication_allow_client_connect_when_standby_enabled = replication_allow_client_connect_when_standby_enabled

    @property
    def service_smf_max_connection_count_per_client_username(self):
        """Gets the service_smf_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of SMF client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The service_smf_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_max_connection_count_per_client_username

    @service_smf_max_connection_count_per_client_username.setter
    def service_smf_max_connection_count_per_client_username(self, service_smf_max_connection_count_per_client_username):
        """Sets the service_smf_max_connection_count_per_client_username of this MsgVpnClientProfile.

        The maximum number of SMF client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param service_smf_max_connection_count_per_client_username: The service_smf_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._service_smf_max_connection_count_per_client_username = service_smf_max_connection_count_per_client_username

    @property
    def service_web_inactive_timeout(self):
        """Gets the service_web_inactive_timeout of this MsgVpnClientProfile.  # noqa: E501

        The timeout for inactive Web Transport client sessions using the Client Profile, in seconds. The default value is `30`.  # noqa: E501

        :return: The service_web_inactive_timeout of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._service_web_inactive_timeout

    @service_web_inactive_timeout.setter
    def service_web_inactive_timeout(self, service_web_inactive_timeout):
        """Sets the service_web_inactive_timeout of this MsgVpnClientProfile.

        The timeout for inactive Web Transport client sessions using the Client Profile, in seconds. The default value is `30`.  # noqa: E501

        :param service_web_inactive_timeout: The service_web_inactive_timeout of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._service_web_inactive_timeout = service_web_inactive_timeout

    @property
    def service_web_max_connection_count_per_client_username(self):
        """Gets the service_web_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501

        The maximum number of Web Transport client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :return: The service_web_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._service_web_max_connection_count_per_client_username

    @service_web_max_connection_count_per_client_username.setter
    def service_web_max_connection_count_per_client_username(self, service_web_max_connection_count_per_client_username):
        """Sets the service_web_max_connection_count_per_client_username of this MsgVpnClientProfile.

        The maximum number of Web Transport client connections per Client Username using the Client Profile. The default is the max value supported by the platform.  # noqa: E501

        :param service_web_max_connection_count_per_client_username: The service_web_max_connection_count_per_client_username of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._service_web_max_connection_count_per_client_username = service_web_max_connection_count_per_client_username

    @property
    def service_web_max_payload(self):
        """Gets the service_web_max_payload of this MsgVpnClientProfile.  # noqa: E501

        The maximum Web Transport payload size before fragmentation occurs for clients using the Client Profile, in bytes. The size of the header is not included. The default value is `1000000`.  # noqa: E501

        :return: The service_web_max_payload of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._service_web_max_payload

    @service_web_max_payload.setter
    def service_web_max_payload(self, service_web_max_payload):
        """Sets the service_web_max_payload of this MsgVpnClientProfile.

        The maximum Web Transport payload size before fragmentation occurs for clients using the Client Profile, in bytes. The size of the header is not included. The default value is `1000000`.  # noqa: E501

        :param service_web_max_payload: The service_web_max_payload of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._service_web_max_payload = service_web_max_payload

    @property
    def tcp_congestion_window_size(self):
        """Gets the tcp_congestion_window_size of this MsgVpnClientProfile.  # noqa: E501

        The TCP initial congestion window size for clients using the Client Profile, in multiples of the TCP Maximum Segment Size (MSS). Changing the value from its default of 2 results in non-compliance with RFC 2581. Contact Solace Support before changing this value. The default value is `2`.  # noqa: E501

        :return: The tcp_congestion_window_size of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_congestion_window_size

    @tcp_congestion_window_size.setter
    def tcp_congestion_window_size(self, tcp_congestion_window_size):
        """Sets the tcp_congestion_window_size of this MsgVpnClientProfile.

        The TCP initial congestion window size for clients using the Client Profile, in multiples of the TCP Maximum Segment Size (MSS). Changing the value from its default of 2 results in non-compliance with RFC 2581. Contact Solace Support before changing this value. The default value is `2`.  # noqa: E501

        :param tcp_congestion_window_size: The tcp_congestion_window_size of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_congestion_window_size = tcp_congestion_window_size

    @property
    def tcp_keepalive_count(self):
        """Gets the tcp_keepalive_count of this MsgVpnClientProfile.  # noqa: E501

        The number of TCP keepalive retransmissions to a client using the Client Profile before declaring that it is not available. The default value is `5`.  # noqa: E501

        :return: The tcp_keepalive_count of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_keepalive_count

    @tcp_keepalive_count.setter
    def tcp_keepalive_count(self, tcp_keepalive_count):
        """Sets the tcp_keepalive_count of this MsgVpnClientProfile.

        The number of TCP keepalive retransmissions to a client using the Client Profile before declaring that it is not available. The default value is `5`.  # noqa: E501

        :param tcp_keepalive_count: The tcp_keepalive_count of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_keepalive_count = tcp_keepalive_count

    @property
    def tcp_keepalive_idle_time(self):
        """Gets the tcp_keepalive_idle_time of this MsgVpnClientProfile.  # noqa: E501

        The amount of time a client connection using the Client Profile must remain idle before TCP begins sending keepalive probes, in seconds. The default value is `3`.  # noqa: E501

        :return: The tcp_keepalive_idle_time of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_keepalive_idle_time

    @tcp_keepalive_idle_time.setter
    def tcp_keepalive_idle_time(self, tcp_keepalive_idle_time):
        """Sets the tcp_keepalive_idle_time of this MsgVpnClientProfile.

        The amount of time a client connection using the Client Profile must remain idle before TCP begins sending keepalive probes, in seconds. The default value is `3`.  # noqa: E501

        :param tcp_keepalive_idle_time: The tcp_keepalive_idle_time of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_keepalive_idle_time = tcp_keepalive_idle_time

    @property
    def tcp_keepalive_interval(self):
        """Gets the tcp_keepalive_interval of this MsgVpnClientProfile.  # noqa: E501

        The amount of time between TCP keepalive retransmissions to a client using the Client Profile when no acknowledgement is received, in seconds. The default value is `1`.  # noqa: E501

        :return: The tcp_keepalive_interval of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_keepalive_interval

    @tcp_keepalive_interval.setter
    def tcp_keepalive_interval(self, tcp_keepalive_interval):
        """Sets the tcp_keepalive_interval of this MsgVpnClientProfile.

        The amount of time between TCP keepalive retransmissions to a client using the Client Profile when no acknowledgement is received, in seconds. The default value is `1`.  # noqa: E501

        :param tcp_keepalive_interval: The tcp_keepalive_interval of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_keepalive_interval = tcp_keepalive_interval

    @property
    def tcp_max_segment_size(self):
        """Gets the tcp_max_segment_size of this MsgVpnClientProfile.  # noqa: E501

        The TCP maximum segment size for clients using the Client Profile, in kilobytes. Changes are applied to all existing connections. The default value is `1460`.  # noqa: E501

        :return: The tcp_max_segment_size of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_max_segment_size

    @tcp_max_segment_size.setter
    def tcp_max_segment_size(self, tcp_max_segment_size):
        """Sets the tcp_max_segment_size of this MsgVpnClientProfile.

        The TCP maximum segment size for clients using the Client Profile, in kilobytes. Changes are applied to all existing connections. The default value is `1460`.  # noqa: E501

        :param tcp_max_segment_size: The tcp_max_segment_size of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_max_segment_size = tcp_max_segment_size

    @property
    def tcp_max_window_size(self):
        """Gets the tcp_max_window_size of this MsgVpnClientProfile.  # noqa: E501

        The TCP maximum window size for clients using the Client Profile, in kilobytes. Changes are applied to all existing connections. The default value is `256`.  # noqa: E501

        :return: The tcp_max_window_size of this MsgVpnClientProfile.  # noqa: E501
        :rtype: int
        """
        return self._tcp_max_window_size

    @tcp_max_window_size.setter
    def tcp_max_window_size(self, tcp_max_window_size):
        """Sets the tcp_max_window_size of this MsgVpnClientProfile.

        The TCP maximum window size for clients using the Client Profile, in kilobytes. Changes are applied to all existing connections. The default value is `256`.  # noqa: E501

        :param tcp_max_window_size: The tcp_max_window_size of this MsgVpnClientProfile.  # noqa: E501
        :type: int
        """

        self._tcp_max_window_size = tcp_max_window_size

    @property
    def tls_allow_downgrade_to_plain_text_enabled(self):
        """Gets the tls_allow_downgrade_to_plain_text_enabled of this MsgVpnClientProfile.  # noqa: E501

        Enable or disable allowing a client using the Client Profile to downgrade an encrypted connection to plain text. The default value is `true`. Available since 2.8.  # noqa: E501

        :return: The tls_allow_downgrade_to_plain_text_enabled of this MsgVpnClientProfile.  # noqa: E501
        :rtype: bool
        """
        return self._tls_allow_downgrade_to_plain_text_enabled

    @tls_allow_downgrade_to_plain_text_enabled.setter
    def tls_allow_downgrade_to_plain_text_enabled(self, tls_allow_downgrade_to_plain_text_enabled):
        """Sets the tls_allow_downgrade_to_plain_text_enabled of this MsgVpnClientProfile.

        Enable or disable allowing a client using the Client Profile to downgrade an encrypted connection to plain text. The default value is `true`. Available since 2.8.  # noqa: E501

        :param tls_allow_downgrade_to_plain_text_enabled: The tls_allow_downgrade_to_plain_text_enabled of this MsgVpnClientProfile.  # noqa: E501
        :type: bool
        """

        self._tls_allow_downgrade_to_plain_text_enabled = tls_allow_downgrade_to_plain_text_enabled

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
        if issubclass(MsgVpnClientProfile, dict):
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
        if not isinstance(other, MsgVpnClientProfile):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
