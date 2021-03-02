# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.12.00902000028
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnTopicEndpoint(object):
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
        'already_bound_bind_failure_count': 'int',
        'average_rx_byte_rate': 'int',
        'average_rx_msg_rate': 'int',
        'average_tx_byte_rate': 'int',
        'average_tx_msg_rate': 'int',
        'bind_request_count': 'int',
        'bind_success_count': 'int',
        'bind_time_forwarding_mode': 'str',
        'client_profile_denied_discarded_msg_count': 'int',
        'consumer_ack_propagation_enabled': 'bool',
        'created_by_management': 'bool',
        'dead_msg_queue': 'str',
        'deleted_msg_count': 'int',
        'destination_group_error_discarded_msg_count': 'int',
        'destination_topic': 'str',
        'disabled_bind_failure_count': 'int',
        'disabled_discarded_msg_count': 'int',
        'durable': 'bool',
        'egress_enabled': 'bool',
        'event_bind_count_threshold': 'EventThreshold',
        'event_reject_low_priority_msg_limit_threshold': 'EventThreshold',
        'event_spool_usage_threshold': 'EventThreshold',
        'highest_acked_msg_id': 'int',
        'highest_msg_id': 'int',
        'in_progress_ack_msg_count': 'int',
        'ingress_enabled': 'bool',
        'invalid_selector_bind_failure_count': 'int',
        'last_replay_complete_time': 'int',
        'last_replay_failure_reason': 'str',
        'last_replay_failure_time': 'int',
        'last_replay_start_time': 'int',
        'last_replayed_msg_tx_time': 'int',
        'last_selector_examined_msg_id': 'int',
        'last_spooled_msg_id': 'int',
        'low_priority_msg_congestion_discarded_msg_count': 'int',
        'low_priority_msg_congestion_state': 'str',
        'lowest_acked_msg_id': 'int',
        'lowest_msg_id': 'int',
        'max_bind_count': 'int',
        'max_bind_count_exceeded_bind_failure_count': 'int',
        'max_delivered_unacked_msgs_per_flow': 'int',
        'max_effective_bind_count': 'int',
        'max_msg_size': 'int',
        'max_msg_size_exceeded_discarded_msg_count': 'int',
        'max_msg_spool_usage_exceeded_discarded_msg_count': 'int',
        'max_redelivery_count': 'int',
        'max_redelivery_exceeded_discarded_msg_count': 'int',
        'max_redelivery_exceeded_to_dmq_failed_msg_count': 'int',
        'max_redelivery_exceeded_to_dmq_msg_count': 'int',
        'max_spool_usage': 'int',
        'max_ttl': 'int',
        'max_ttl_exceeded_discarded_msg_count': 'int',
        'max_ttl_expired_discarded_msg_count': 'int',
        'max_ttl_expired_to_dmq_failed_msg_count': 'int',
        'max_ttl_expired_to_dmq_msg_count': 'int',
        'msg_spool_peak_usage': 'int',
        'msg_spool_usage': 'int',
        'msg_vpn_name': 'str',
        'network_topic': 'str',
        'no_local_delivery_discarded_msg_count': 'int',
        'other_bind_failure_count': 'int',
        'owner': 'str',
        'permission': 'str',
        'redelivered_msg_count': 'int',
        'reject_low_priority_msg_enabled': 'bool',
        'reject_low_priority_msg_limit': 'int',
        'reject_msg_to_sender_on_discard_behavior': 'str',
        'replay_failure_count': 'int',
        'replay_start_count': 'int',
        'replay_state': 'str',
        'replay_success_count': 'int',
        'replayed_acked_msg_count': 'int',
        'replayed_tx_msg_count': 'int',
        'replication_active_ack_prop_tx_msg_count': 'int',
        'replication_standby_ack_prop_rx_msg_count': 'int',
        'replication_standby_acked_by_ack_prop_msg_count': 'int',
        'replication_standby_rx_msg_count': 'int',
        'respect_msg_priority_enabled': 'bool',
        'respect_ttl_enabled': 'bool',
        'rx_byte_rate': 'int',
        'rx_msg_rate': 'int',
        'rx_selector': 'bool',
        'selector': 'str',
        'selector_examined_msg_count': 'int',
        'selector_matched_msg_count': 'int',
        'selector_not_matched_msg_count': 'int',
        'spooled_byte_count': 'int',
        'spooled_msg_count': 'int',
        'topic_endpoint_name': 'str',
        'tx_byte_rate': 'int',
        'tx_msg_rate': 'int',
        'tx_unacked_msg_count': 'int',
        'virtual_router': 'str'
    }

    attribute_map = {
        'access_type': 'accessType',
        'already_bound_bind_failure_count': 'alreadyBoundBindFailureCount',
        'average_rx_byte_rate': 'averageRxByteRate',
        'average_rx_msg_rate': 'averageRxMsgRate',
        'average_tx_byte_rate': 'averageTxByteRate',
        'average_tx_msg_rate': 'averageTxMsgRate',
        'bind_request_count': 'bindRequestCount',
        'bind_success_count': 'bindSuccessCount',
        'bind_time_forwarding_mode': 'bindTimeForwardingMode',
        'client_profile_denied_discarded_msg_count': 'clientProfileDeniedDiscardedMsgCount',
        'consumer_ack_propagation_enabled': 'consumerAckPropagationEnabled',
        'created_by_management': 'createdByManagement',
        'dead_msg_queue': 'deadMsgQueue',
        'deleted_msg_count': 'deletedMsgCount',
        'destination_group_error_discarded_msg_count': 'destinationGroupErrorDiscardedMsgCount',
        'destination_topic': 'destinationTopic',
        'disabled_bind_failure_count': 'disabledBindFailureCount',
        'disabled_discarded_msg_count': 'disabledDiscardedMsgCount',
        'durable': 'durable',
        'egress_enabled': 'egressEnabled',
        'event_bind_count_threshold': 'eventBindCountThreshold',
        'event_reject_low_priority_msg_limit_threshold': 'eventRejectLowPriorityMsgLimitThreshold',
        'event_spool_usage_threshold': 'eventSpoolUsageThreshold',
        'highest_acked_msg_id': 'highestAckedMsgId',
        'highest_msg_id': 'highestMsgId',
        'in_progress_ack_msg_count': 'inProgressAckMsgCount',
        'ingress_enabled': 'ingressEnabled',
        'invalid_selector_bind_failure_count': 'invalidSelectorBindFailureCount',
        'last_replay_complete_time': 'lastReplayCompleteTime',
        'last_replay_failure_reason': 'lastReplayFailureReason',
        'last_replay_failure_time': 'lastReplayFailureTime',
        'last_replay_start_time': 'lastReplayStartTime',
        'last_replayed_msg_tx_time': 'lastReplayedMsgTxTime',
        'last_selector_examined_msg_id': 'lastSelectorExaminedMsgId',
        'last_spooled_msg_id': 'lastSpooledMsgId',
        'low_priority_msg_congestion_discarded_msg_count': 'lowPriorityMsgCongestionDiscardedMsgCount',
        'low_priority_msg_congestion_state': 'lowPriorityMsgCongestionState',
        'lowest_acked_msg_id': 'lowestAckedMsgId',
        'lowest_msg_id': 'lowestMsgId',
        'max_bind_count': 'maxBindCount',
        'max_bind_count_exceeded_bind_failure_count': 'maxBindCountExceededBindFailureCount',
        'max_delivered_unacked_msgs_per_flow': 'maxDeliveredUnackedMsgsPerFlow',
        'max_effective_bind_count': 'maxEffectiveBindCount',
        'max_msg_size': 'maxMsgSize',
        'max_msg_size_exceeded_discarded_msg_count': 'maxMsgSizeExceededDiscardedMsgCount',
        'max_msg_spool_usage_exceeded_discarded_msg_count': 'maxMsgSpoolUsageExceededDiscardedMsgCount',
        'max_redelivery_count': 'maxRedeliveryCount',
        'max_redelivery_exceeded_discarded_msg_count': 'maxRedeliveryExceededDiscardedMsgCount',
        'max_redelivery_exceeded_to_dmq_failed_msg_count': 'maxRedeliveryExceededToDmqFailedMsgCount',
        'max_redelivery_exceeded_to_dmq_msg_count': 'maxRedeliveryExceededToDmqMsgCount',
        'max_spool_usage': 'maxSpoolUsage',
        'max_ttl': 'maxTtl',
        'max_ttl_exceeded_discarded_msg_count': 'maxTtlExceededDiscardedMsgCount',
        'max_ttl_expired_discarded_msg_count': 'maxTtlExpiredDiscardedMsgCount',
        'max_ttl_expired_to_dmq_failed_msg_count': 'maxTtlExpiredToDmqFailedMsgCount',
        'max_ttl_expired_to_dmq_msg_count': 'maxTtlExpiredToDmqMsgCount',
        'msg_spool_peak_usage': 'msgSpoolPeakUsage',
        'msg_spool_usage': 'msgSpoolUsage',
        'msg_vpn_name': 'msgVpnName',
        'network_topic': 'networkTopic',
        'no_local_delivery_discarded_msg_count': 'noLocalDeliveryDiscardedMsgCount',
        'other_bind_failure_count': 'otherBindFailureCount',
        'owner': 'owner',
        'permission': 'permission',
        'redelivered_msg_count': 'redeliveredMsgCount',
        'reject_low_priority_msg_enabled': 'rejectLowPriorityMsgEnabled',
        'reject_low_priority_msg_limit': 'rejectLowPriorityMsgLimit',
        'reject_msg_to_sender_on_discard_behavior': 'rejectMsgToSenderOnDiscardBehavior',
        'replay_failure_count': 'replayFailureCount',
        'replay_start_count': 'replayStartCount',
        'replay_state': 'replayState',
        'replay_success_count': 'replaySuccessCount',
        'replayed_acked_msg_count': 'replayedAckedMsgCount',
        'replayed_tx_msg_count': 'replayedTxMsgCount',
        'replication_active_ack_prop_tx_msg_count': 'replicationActiveAckPropTxMsgCount',
        'replication_standby_ack_prop_rx_msg_count': 'replicationStandbyAckPropRxMsgCount',
        'replication_standby_acked_by_ack_prop_msg_count': 'replicationStandbyAckedByAckPropMsgCount',
        'replication_standby_rx_msg_count': 'replicationStandbyRxMsgCount',
        'respect_msg_priority_enabled': 'respectMsgPriorityEnabled',
        'respect_ttl_enabled': 'respectTtlEnabled',
        'rx_byte_rate': 'rxByteRate',
        'rx_msg_rate': 'rxMsgRate',
        'rx_selector': 'rxSelector',
        'selector': 'selector',
        'selector_examined_msg_count': 'selectorExaminedMsgCount',
        'selector_matched_msg_count': 'selectorMatchedMsgCount',
        'selector_not_matched_msg_count': 'selectorNotMatchedMsgCount',
        'spooled_byte_count': 'spooledByteCount',
        'spooled_msg_count': 'spooledMsgCount',
        'topic_endpoint_name': 'topicEndpointName',
        'tx_byte_rate': 'txByteRate',
        'tx_msg_rate': 'txMsgRate',
        'tx_unacked_msg_count': 'txUnackedMsgCount',
        'virtual_router': 'virtualRouter'
    }

    def __init__(self, access_type=None, already_bound_bind_failure_count=None, average_rx_byte_rate=None, average_rx_msg_rate=None, average_tx_byte_rate=None, average_tx_msg_rate=None, bind_request_count=None, bind_success_count=None, bind_time_forwarding_mode=None, client_profile_denied_discarded_msg_count=None, consumer_ack_propagation_enabled=None, created_by_management=None, dead_msg_queue=None, deleted_msg_count=None, destination_group_error_discarded_msg_count=None, destination_topic=None, disabled_bind_failure_count=None, disabled_discarded_msg_count=None, durable=None, egress_enabled=None, event_bind_count_threshold=None, event_reject_low_priority_msg_limit_threshold=None, event_spool_usage_threshold=None, highest_acked_msg_id=None, highest_msg_id=None, in_progress_ack_msg_count=None, ingress_enabled=None, invalid_selector_bind_failure_count=None, last_replay_complete_time=None, last_replay_failure_reason=None, last_replay_failure_time=None, last_replay_start_time=None, last_replayed_msg_tx_time=None, last_selector_examined_msg_id=None, last_spooled_msg_id=None, low_priority_msg_congestion_discarded_msg_count=None, low_priority_msg_congestion_state=None, lowest_acked_msg_id=None, lowest_msg_id=None, max_bind_count=None, max_bind_count_exceeded_bind_failure_count=None, max_delivered_unacked_msgs_per_flow=None, max_effective_bind_count=None, max_msg_size=None, max_msg_size_exceeded_discarded_msg_count=None, max_msg_spool_usage_exceeded_discarded_msg_count=None, max_redelivery_count=None, max_redelivery_exceeded_discarded_msg_count=None, max_redelivery_exceeded_to_dmq_failed_msg_count=None, max_redelivery_exceeded_to_dmq_msg_count=None, max_spool_usage=None, max_ttl=None, max_ttl_exceeded_discarded_msg_count=None, max_ttl_expired_discarded_msg_count=None, max_ttl_expired_to_dmq_failed_msg_count=None, max_ttl_expired_to_dmq_msg_count=None, msg_spool_peak_usage=None, msg_spool_usage=None, msg_vpn_name=None, network_topic=None, no_local_delivery_discarded_msg_count=None, other_bind_failure_count=None, owner=None, permission=None, redelivered_msg_count=None, reject_low_priority_msg_enabled=None, reject_low_priority_msg_limit=None, reject_msg_to_sender_on_discard_behavior=None, replay_failure_count=None, replay_start_count=None, replay_state=None, replay_success_count=None, replayed_acked_msg_count=None, replayed_tx_msg_count=None, replication_active_ack_prop_tx_msg_count=None, replication_standby_ack_prop_rx_msg_count=None, replication_standby_acked_by_ack_prop_msg_count=None, replication_standby_rx_msg_count=None, respect_msg_priority_enabled=None, respect_ttl_enabled=None, rx_byte_rate=None, rx_msg_rate=None, rx_selector=None, selector=None, selector_examined_msg_count=None, selector_matched_msg_count=None, selector_not_matched_msg_count=None, spooled_byte_count=None, spooled_msg_count=None, topic_endpoint_name=None, tx_byte_rate=None, tx_msg_rate=None, tx_unacked_msg_count=None, virtual_router=None):  # noqa: E501
        """MsgVpnTopicEndpoint - a model defined in Swagger"""  # noqa: E501

        self._access_type = None
        self._already_bound_bind_failure_count = None
        self._average_rx_byte_rate = None
        self._average_rx_msg_rate = None
        self._average_tx_byte_rate = None
        self._average_tx_msg_rate = None
        self._bind_request_count = None
        self._bind_success_count = None
        self._bind_time_forwarding_mode = None
        self._client_profile_denied_discarded_msg_count = None
        self._consumer_ack_propagation_enabled = None
        self._created_by_management = None
        self._dead_msg_queue = None
        self._deleted_msg_count = None
        self._destination_group_error_discarded_msg_count = None
        self._destination_topic = None
        self._disabled_bind_failure_count = None
        self._disabled_discarded_msg_count = None
        self._durable = None
        self._egress_enabled = None
        self._event_bind_count_threshold = None
        self._event_reject_low_priority_msg_limit_threshold = None
        self._event_spool_usage_threshold = None
        self._highest_acked_msg_id = None
        self._highest_msg_id = None
        self._in_progress_ack_msg_count = None
        self._ingress_enabled = None
        self._invalid_selector_bind_failure_count = None
        self._last_replay_complete_time = None
        self._last_replay_failure_reason = None
        self._last_replay_failure_time = None
        self._last_replay_start_time = None
        self._last_replayed_msg_tx_time = None
        self._last_selector_examined_msg_id = None
        self._last_spooled_msg_id = None
        self._low_priority_msg_congestion_discarded_msg_count = None
        self._low_priority_msg_congestion_state = None
        self._lowest_acked_msg_id = None
        self._lowest_msg_id = None
        self._max_bind_count = None
        self._max_bind_count_exceeded_bind_failure_count = None
        self._max_delivered_unacked_msgs_per_flow = None
        self._max_effective_bind_count = None
        self._max_msg_size = None
        self._max_msg_size_exceeded_discarded_msg_count = None
        self._max_msg_spool_usage_exceeded_discarded_msg_count = None
        self._max_redelivery_count = None
        self._max_redelivery_exceeded_discarded_msg_count = None
        self._max_redelivery_exceeded_to_dmq_failed_msg_count = None
        self._max_redelivery_exceeded_to_dmq_msg_count = None
        self._max_spool_usage = None
        self._max_ttl = None
        self._max_ttl_exceeded_discarded_msg_count = None
        self._max_ttl_expired_discarded_msg_count = None
        self._max_ttl_expired_to_dmq_failed_msg_count = None
        self._max_ttl_expired_to_dmq_msg_count = None
        self._msg_spool_peak_usage = None
        self._msg_spool_usage = None
        self._msg_vpn_name = None
        self._network_topic = None
        self._no_local_delivery_discarded_msg_count = None
        self._other_bind_failure_count = None
        self._owner = None
        self._permission = None
        self._redelivered_msg_count = None
        self._reject_low_priority_msg_enabled = None
        self._reject_low_priority_msg_limit = None
        self._reject_msg_to_sender_on_discard_behavior = None
        self._replay_failure_count = None
        self._replay_start_count = None
        self._replay_state = None
        self._replay_success_count = None
        self._replayed_acked_msg_count = None
        self._replayed_tx_msg_count = None
        self._replication_active_ack_prop_tx_msg_count = None
        self._replication_standby_ack_prop_rx_msg_count = None
        self._replication_standby_acked_by_ack_prop_msg_count = None
        self._replication_standby_rx_msg_count = None
        self._respect_msg_priority_enabled = None
        self._respect_ttl_enabled = None
        self._rx_byte_rate = None
        self._rx_msg_rate = None
        self._rx_selector = None
        self._selector = None
        self._selector_examined_msg_count = None
        self._selector_matched_msg_count = None
        self._selector_not_matched_msg_count = None
        self._spooled_byte_count = None
        self._spooled_msg_count = None
        self._topic_endpoint_name = None
        self._tx_byte_rate = None
        self._tx_msg_rate = None
        self._tx_unacked_msg_count = None
        self._virtual_router = None
        self.discriminator = None

        if access_type is not None:
            self.access_type = access_type
        if already_bound_bind_failure_count is not None:
            self.already_bound_bind_failure_count = already_bound_bind_failure_count
        if average_rx_byte_rate is not None:
            self.average_rx_byte_rate = average_rx_byte_rate
        if average_rx_msg_rate is not None:
            self.average_rx_msg_rate = average_rx_msg_rate
        if average_tx_byte_rate is not None:
            self.average_tx_byte_rate = average_tx_byte_rate
        if average_tx_msg_rate is not None:
            self.average_tx_msg_rate = average_tx_msg_rate
        if bind_request_count is not None:
            self.bind_request_count = bind_request_count
        if bind_success_count is not None:
            self.bind_success_count = bind_success_count
        if bind_time_forwarding_mode is not None:
            self.bind_time_forwarding_mode = bind_time_forwarding_mode
        if client_profile_denied_discarded_msg_count is not None:
            self.client_profile_denied_discarded_msg_count = client_profile_denied_discarded_msg_count
        if consumer_ack_propagation_enabled is not None:
            self.consumer_ack_propagation_enabled = consumer_ack_propagation_enabled
        if created_by_management is not None:
            self.created_by_management = created_by_management
        if dead_msg_queue is not None:
            self.dead_msg_queue = dead_msg_queue
        if deleted_msg_count is not None:
            self.deleted_msg_count = deleted_msg_count
        if destination_group_error_discarded_msg_count is not None:
            self.destination_group_error_discarded_msg_count = destination_group_error_discarded_msg_count
        if destination_topic is not None:
            self.destination_topic = destination_topic
        if disabled_bind_failure_count is not None:
            self.disabled_bind_failure_count = disabled_bind_failure_count
        if disabled_discarded_msg_count is not None:
            self.disabled_discarded_msg_count = disabled_discarded_msg_count
        if durable is not None:
            self.durable = durable
        if egress_enabled is not None:
            self.egress_enabled = egress_enabled
        if event_bind_count_threshold is not None:
            self.event_bind_count_threshold = event_bind_count_threshold
        if event_reject_low_priority_msg_limit_threshold is not None:
            self.event_reject_low_priority_msg_limit_threshold = event_reject_low_priority_msg_limit_threshold
        if event_spool_usage_threshold is not None:
            self.event_spool_usage_threshold = event_spool_usage_threshold
        if highest_acked_msg_id is not None:
            self.highest_acked_msg_id = highest_acked_msg_id
        if highest_msg_id is not None:
            self.highest_msg_id = highest_msg_id
        if in_progress_ack_msg_count is not None:
            self.in_progress_ack_msg_count = in_progress_ack_msg_count
        if ingress_enabled is not None:
            self.ingress_enabled = ingress_enabled
        if invalid_selector_bind_failure_count is not None:
            self.invalid_selector_bind_failure_count = invalid_selector_bind_failure_count
        if last_replay_complete_time is not None:
            self.last_replay_complete_time = last_replay_complete_time
        if last_replay_failure_reason is not None:
            self.last_replay_failure_reason = last_replay_failure_reason
        if last_replay_failure_time is not None:
            self.last_replay_failure_time = last_replay_failure_time
        if last_replay_start_time is not None:
            self.last_replay_start_time = last_replay_start_time
        if last_replayed_msg_tx_time is not None:
            self.last_replayed_msg_tx_time = last_replayed_msg_tx_time
        if last_selector_examined_msg_id is not None:
            self.last_selector_examined_msg_id = last_selector_examined_msg_id
        if last_spooled_msg_id is not None:
            self.last_spooled_msg_id = last_spooled_msg_id
        if low_priority_msg_congestion_discarded_msg_count is not None:
            self.low_priority_msg_congestion_discarded_msg_count = low_priority_msg_congestion_discarded_msg_count
        if low_priority_msg_congestion_state is not None:
            self.low_priority_msg_congestion_state = low_priority_msg_congestion_state
        if lowest_acked_msg_id is not None:
            self.lowest_acked_msg_id = lowest_acked_msg_id
        if lowest_msg_id is not None:
            self.lowest_msg_id = lowest_msg_id
        if max_bind_count is not None:
            self.max_bind_count = max_bind_count
        if max_bind_count_exceeded_bind_failure_count is not None:
            self.max_bind_count_exceeded_bind_failure_count = max_bind_count_exceeded_bind_failure_count
        if max_delivered_unacked_msgs_per_flow is not None:
            self.max_delivered_unacked_msgs_per_flow = max_delivered_unacked_msgs_per_flow
        if max_effective_bind_count is not None:
            self.max_effective_bind_count = max_effective_bind_count
        if max_msg_size is not None:
            self.max_msg_size = max_msg_size
        if max_msg_size_exceeded_discarded_msg_count is not None:
            self.max_msg_size_exceeded_discarded_msg_count = max_msg_size_exceeded_discarded_msg_count
        if max_msg_spool_usage_exceeded_discarded_msg_count is not None:
            self.max_msg_spool_usage_exceeded_discarded_msg_count = max_msg_spool_usage_exceeded_discarded_msg_count
        if max_redelivery_count is not None:
            self.max_redelivery_count = max_redelivery_count
        if max_redelivery_exceeded_discarded_msg_count is not None:
            self.max_redelivery_exceeded_discarded_msg_count = max_redelivery_exceeded_discarded_msg_count
        if max_redelivery_exceeded_to_dmq_failed_msg_count is not None:
            self.max_redelivery_exceeded_to_dmq_failed_msg_count = max_redelivery_exceeded_to_dmq_failed_msg_count
        if max_redelivery_exceeded_to_dmq_msg_count is not None:
            self.max_redelivery_exceeded_to_dmq_msg_count = max_redelivery_exceeded_to_dmq_msg_count
        if max_spool_usage is not None:
            self.max_spool_usage = max_spool_usage
        if max_ttl is not None:
            self.max_ttl = max_ttl
        if max_ttl_exceeded_discarded_msg_count is not None:
            self.max_ttl_exceeded_discarded_msg_count = max_ttl_exceeded_discarded_msg_count
        if max_ttl_expired_discarded_msg_count is not None:
            self.max_ttl_expired_discarded_msg_count = max_ttl_expired_discarded_msg_count
        if max_ttl_expired_to_dmq_failed_msg_count is not None:
            self.max_ttl_expired_to_dmq_failed_msg_count = max_ttl_expired_to_dmq_failed_msg_count
        if max_ttl_expired_to_dmq_msg_count is not None:
            self.max_ttl_expired_to_dmq_msg_count = max_ttl_expired_to_dmq_msg_count
        if msg_spool_peak_usage is not None:
            self.msg_spool_peak_usage = msg_spool_peak_usage
        if msg_spool_usage is not None:
            self.msg_spool_usage = msg_spool_usage
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if network_topic is not None:
            self.network_topic = network_topic
        if no_local_delivery_discarded_msg_count is not None:
            self.no_local_delivery_discarded_msg_count = no_local_delivery_discarded_msg_count
        if other_bind_failure_count is not None:
            self.other_bind_failure_count = other_bind_failure_count
        if owner is not None:
            self.owner = owner
        if permission is not None:
            self.permission = permission
        if redelivered_msg_count is not None:
            self.redelivered_msg_count = redelivered_msg_count
        if reject_low_priority_msg_enabled is not None:
            self.reject_low_priority_msg_enabled = reject_low_priority_msg_enabled
        if reject_low_priority_msg_limit is not None:
            self.reject_low_priority_msg_limit = reject_low_priority_msg_limit
        if reject_msg_to_sender_on_discard_behavior is not None:
            self.reject_msg_to_sender_on_discard_behavior = reject_msg_to_sender_on_discard_behavior
        if replay_failure_count is not None:
            self.replay_failure_count = replay_failure_count
        if replay_start_count is not None:
            self.replay_start_count = replay_start_count
        if replay_state is not None:
            self.replay_state = replay_state
        if replay_success_count is not None:
            self.replay_success_count = replay_success_count
        if replayed_acked_msg_count is not None:
            self.replayed_acked_msg_count = replayed_acked_msg_count
        if replayed_tx_msg_count is not None:
            self.replayed_tx_msg_count = replayed_tx_msg_count
        if replication_active_ack_prop_tx_msg_count is not None:
            self.replication_active_ack_prop_tx_msg_count = replication_active_ack_prop_tx_msg_count
        if replication_standby_ack_prop_rx_msg_count is not None:
            self.replication_standby_ack_prop_rx_msg_count = replication_standby_ack_prop_rx_msg_count
        if replication_standby_acked_by_ack_prop_msg_count is not None:
            self.replication_standby_acked_by_ack_prop_msg_count = replication_standby_acked_by_ack_prop_msg_count
        if replication_standby_rx_msg_count is not None:
            self.replication_standby_rx_msg_count = replication_standby_rx_msg_count
        if respect_msg_priority_enabled is not None:
            self.respect_msg_priority_enabled = respect_msg_priority_enabled
        if respect_ttl_enabled is not None:
            self.respect_ttl_enabled = respect_ttl_enabled
        if rx_byte_rate is not None:
            self.rx_byte_rate = rx_byte_rate
        if rx_msg_rate is not None:
            self.rx_msg_rate = rx_msg_rate
        if rx_selector is not None:
            self.rx_selector = rx_selector
        if selector is not None:
            self.selector = selector
        if selector_examined_msg_count is not None:
            self.selector_examined_msg_count = selector_examined_msg_count
        if selector_matched_msg_count is not None:
            self.selector_matched_msg_count = selector_matched_msg_count
        if selector_not_matched_msg_count is not None:
            self.selector_not_matched_msg_count = selector_not_matched_msg_count
        if spooled_byte_count is not None:
            self.spooled_byte_count = spooled_byte_count
        if spooled_msg_count is not None:
            self.spooled_msg_count = spooled_msg_count
        if topic_endpoint_name is not None:
            self.topic_endpoint_name = topic_endpoint_name
        if tx_byte_rate is not None:
            self.tx_byte_rate = tx_byte_rate
        if tx_msg_rate is not None:
            self.tx_msg_rate = tx_msg_rate
        if tx_unacked_msg_count is not None:
            self.tx_unacked_msg_count = tx_unacked_msg_count
        if virtual_router is not None:
            self.virtual_router = virtual_router

    @property
    def access_type(self):
        """Gets the access_type of this MsgVpnTopicEndpoint.  # noqa: E501

        The access type for delivering messages to consumer flows bound to the Topic Endpoint. The allowed values and their meaning are:  <pre> \"exclusive\" - Exclusive delivery of messages to the first bound consumer flow. \"non-exclusive\" - Non-exclusive delivery of messages to all bound consumer flows in a round-robin fashion. </pre>   # noqa: E501

        :return: The access_type of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this MsgVpnTopicEndpoint.

        The access type for delivering messages to consumer flows bound to the Topic Endpoint. The allowed values and their meaning are:  <pre> \"exclusive\" - Exclusive delivery of messages to the first bound consumer flow. \"non-exclusive\" - Non-exclusive delivery of messages to all bound consumer flows in a round-robin fashion. </pre>   # noqa: E501

        :param access_type: The access_type of this MsgVpnTopicEndpoint.  # noqa: E501
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
    def already_bound_bind_failure_count(self):
        """Gets the already_bound_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of Topic Endpoint bind failures due to being already bound.  # noqa: E501

        :return: The already_bound_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._already_bound_bind_failure_count

    @already_bound_bind_failure_count.setter
    def already_bound_bind_failure_count(self, already_bound_bind_failure_count):
        """Sets the already_bound_bind_failure_count of this MsgVpnTopicEndpoint.

        The number of Topic Endpoint bind failures due to being already bound.  # noqa: E501

        :param already_bound_bind_failure_count: The already_bound_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._already_bound_bind_failure_count = already_bound_bind_failure_count

    @property
    def average_rx_byte_rate(self):
        """Gets the average_rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The one minute average of the message rate received by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :return: The average_rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_byte_rate

    @average_rx_byte_rate.setter
    def average_rx_byte_rate(self, average_rx_byte_rate):
        """Sets the average_rx_byte_rate of this MsgVpnTopicEndpoint.

        The one minute average of the message rate received by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :param average_rx_byte_rate: The average_rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._average_rx_byte_rate = average_rx_byte_rate

    @property
    def average_rx_msg_rate(self):
        """Gets the average_rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The one minute average of the message rate received by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :return: The average_rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_msg_rate

    @average_rx_msg_rate.setter
    def average_rx_msg_rate(self, average_rx_msg_rate):
        """Sets the average_rx_msg_rate of this MsgVpnTopicEndpoint.

        The one minute average of the message rate received by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :param average_rx_msg_rate: The average_rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._average_rx_msg_rate = average_rx_msg_rate

    @property
    def average_tx_byte_rate(self):
        """Gets the average_tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The one minute average of the message rate transmitted by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :return: The average_tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_byte_rate

    @average_tx_byte_rate.setter
    def average_tx_byte_rate(self, average_tx_byte_rate):
        """Sets the average_tx_byte_rate of this MsgVpnTopicEndpoint.

        The one minute average of the message rate transmitted by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :param average_tx_byte_rate: The average_tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._average_tx_byte_rate = average_tx_byte_rate

    @property
    def average_tx_msg_rate(self):
        """Gets the average_tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The one minute average of the message rate transmitted by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :return: The average_tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_msg_rate

    @average_tx_msg_rate.setter
    def average_tx_msg_rate(self, average_tx_msg_rate):
        """Sets the average_tx_msg_rate of this MsgVpnTopicEndpoint.

        The one minute average of the message rate transmitted by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :param average_tx_msg_rate: The average_tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._average_tx_msg_rate = average_tx_msg_rate

    @property
    def bind_request_count(self):
        """Gets the bind_request_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of consumer requests to bind to the Topic Endpoint.  # noqa: E501

        :return: The bind_request_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._bind_request_count

    @bind_request_count.setter
    def bind_request_count(self, bind_request_count):
        """Sets the bind_request_count of this MsgVpnTopicEndpoint.

        The number of consumer requests to bind to the Topic Endpoint.  # noqa: E501

        :param bind_request_count: The bind_request_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._bind_request_count = bind_request_count

    @property
    def bind_success_count(self):
        """Gets the bind_success_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of successful consumer requests to bind to the Topic Endpoint.  # noqa: E501

        :return: The bind_success_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._bind_success_count

    @bind_success_count.setter
    def bind_success_count(self, bind_success_count):
        """Sets the bind_success_count of this MsgVpnTopicEndpoint.

        The number of successful consumer requests to bind to the Topic Endpoint.  # noqa: E501

        :param bind_success_count: The bind_success_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._bind_success_count = bind_success_count

    @property
    def bind_time_forwarding_mode(self):
        """Gets the bind_time_forwarding_mode of this MsgVpnTopicEndpoint.  # noqa: E501

        The forwarding mode of the Topic Endpoint at bind time. The allowed values and their meaning are:  <pre> \"store-and-forward\" - Deliver messages using the guaranteed data path. \"cut-through\" - Deliver messages using the direct and guaranteed data paths for lower latency. </pre>   # noqa: E501

        :return: The bind_time_forwarding_mode of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._bind_time_forwarding_mode

    @bind_time_forwarding_mode.setter
    def bind_time_forwarding_mode(self, bind_time_forwarding_mode):
        """Sets the bind_time_forwarding_mode of this MsgVpnTopicEndpoint.

        The forwarding mode of the Topic Endpoint at bind time. The allowed values and their meaning are:  <pre> \"store-and-forward\" - Deliver messages using the guaranteed data path. \"cut-through\" - Deliver messages using the direct and guaranteed data paths for lower latency. </pre>   # noqa: E501

        :param bind_time_forwarding_mode: The bind_time_forwarding_mode of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._bind_time_forwarding_mode = bind_time_forwarding_mode

    @property
    def client_profile_denied_discarded_msg_count(self):
        """Gets the client_profile_denied_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to being denied by the Client Profile.  # noqa: E501

        :return: The client_profile_denied_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._client_profile_denied_discarded_msg_count

    @client_profile_denied_discarded_msg_count.setter
    def client_profile_denied_discarded_msg_count(self, client_profile_denied_discarded_msg_count):
        """Sets the client_profile_denied_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to being denied by the Client Profile.  # noqa: E501

        :param client_profile_denied_discarded_msg_count: The client_profile_denied_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._client_profile_denied_discarded_msg_count = client_profile_denied_discarded_msg_count

    @property
    def consumer_ack_propagation_enabled(self):
        """Gets the consumer_ack_propagation_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN.  # noqa: E501

        :return: The consumer_ack_propagation_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._consumer_ack_propagation_enabled

    @consumer_ack_propagation_enabled.setter
    def consumer_ack_propagation_enabled(self, consumer_ack_propagation_enabled):
        """Sets the consumer_ack_propagation_enabled of this MsgVpnTopicEndpoint.

        Enable or disable the propagation of consumer acknowledgements (ACKs) received on the active replication Message VPN to the standby replication Message VPN.  # noqa: E501

        :param consumer_ack_propagation_enabled: The consumer_ack_propagation_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._consumer_ack_propagation_enabled = consumer_ack_propagation_enabled

    @property
    def created_by_management(self):
        """Gets the created_by_management of this MsgVpnTopicEndpoint.  # noqa: E501

        Indicates whether the Topic Endpoint was created by a management API (CLI or SEMP).  # noqa: E501

        :return: The created_by_management of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._created_by_management

    @created_by_management.setter
    def created_by_management(self, created_by_management):
        """Sets the created_by_management of this MsgVpnTopicEndpoint.

        Indicates whether the Topic Endpoint was created by a management API (CLI or SEMP).  # noqa: E501

        :param created_by_management: The created_by_management of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._created_by_management = created_by_management

    @property
    def dead_msg_queue(self):
        """Gets the dead_msg_queue of this MsgVpnTopicEndpoint.  # noqa: E501

        The name of the Dead Message Queue (DMQ) used by the Topic Endpoint.  # noqa: E501

        :return: The dead_msg_queue of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._dead_msg_queue

    @dead_msg_queue.setter
    def dead_msg_queue(self, dead_msg_queue):
        """Sets the dead_msg_queue of this MsgVpnTopicEndpoint.

        The name of the Dead Message Queue (DMQ) used by the Topic Endpoint.  # noqa: E501

        :param dead_msg_queue: The dead_msg_queue of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._dead_msg_queue = dead_msg_queue

    @property
    def deleted_msg_count(self):
        """Gets the deleted_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages deleted from the Topic Endpoint.  # noqa: E501

        :return: The deleted_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._deleted_msg_count

    @deleted_msg_count.setter
    def deleted_msg_count(self, deleted_msg_count):
        """Sets the deleted_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages deleted from the Topic Endpoint.  # noqa: E501

        :param deleted_msg_count: The deleted_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._deleted_msg_count = deleted_msg_count

    @property
    def destination_group_error_discarded_msg_count(self):
        """Gets the destination_group_error_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to a destination group error.  # noqa: E501

        :return: The destination_group_error_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._destination_group_error_discarded_msg_count

    @destination_group_error_discarded_msg_count.setter
    def destination_group_error_discarded_msg_count(self, destination_group_error_discarded_msg_count):
        """Sets the destination_group_error_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to a destination group error.  # noqa: E501

        :param destination_group_error_discarded_msg_count: The destination_group_error_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._destination_group_error_discarded_msg_count = destination_group_error_discarded_msg_count

    @property
    def destination_topic(self):
        """Gets the destination_topic of this MsgVpnTopicEndpoint.  # noqa: E501

        The destination topic of the Topic Endpoint.  # noqa: E501

        :return: The destination_topic of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._destination_topic

    @destination_topic.setter
    def destination_topic(self, destination_topic):
        """Sets the destination_topic of this MsgVpnTopicEndpoint.

        The destination topic of the Topic Endpoint.  # noqa: E501

        :param destination_topic: The destination_topic of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._destination_topic = destination_topic

    @property
    def disabled_bind_failure_count(self):
        """Gets the disabled_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of Topic Endpoint bind failures due to being disabled.  # noqa: E501

        :return: The disabled_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._disabled_bind_failure_count

    @disabled_bind_failure_count.setter
    def disabled_bind_failure_count(self, disabled_bind_failure_count):
        """Sets the disabled_bind_failure_count of this MsgVpnTopicEndpoint.

        The number of Topic Endpoint bind failures due to being disabled.  # noqa: E501

        :param disabled_bind_failure_count: The disabled_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._disabled_bind_failure_count = disabled_bind_failure_count

    @property
    def disabled_discarded_msg_count(self):
        """Gets the disabled_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to it being disabled.  # noqa: E501

        :return: The disabled_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._disabled_discarded_msg_count

    @disabled_discarded_msg_count.setter
    def disabled_discarded_msg_count(self, disabled_discarded_msg_count):
        """Sets the disabled_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to it being disabled.  # noqa: E501

        :param disabled_discarded_msg_count: The disabled_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._disabled_discarded_msg_count = disabled_discarded_msg_count

    @property
    def durable(self):
        """Gets the durable of this MsgVpnTopicEndpoint.  # noqa: E501

        Indicates whether the Topic Endpoint is durable and not temporary.  # noqa: E501

        :return: The durable of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._durable

    @durable.setter
    def durable(self, durable):
        """Sets the durable of this MsgVpnTopicEndpoint.

        Indicates whether the Topic Endpoint is durable and not temporary.  # noqa: E501

        :param durable: The durable of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._durable = durable

    @property
    def egress_enabled(self):
        """Gets the egress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Enable or disable the transmission of messages from the Topic Endpoint.  # noqa: E501

        :return: The egress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._egress_enabled

    @egress_enabled.setter
    def egress_enabled(self, egress_enabled):
        """Sets the egress_enabled of this MsgVpnTopicEndpoint.

        Enable or disable the transmission of messages from the Topic Endpoint.  # noqa: E501

        :param egress_enabled: The egress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._egress_enabled = egress_enabled

    @property
    def event_bind_count_threshold(self):
        """Gets the event_bind_count_threshold of this MsgVpnTopicEndpoint.  # noqa: E501


        :return: The event_bind_count_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_bind_count_threshold

    @event_bind_count_threshold.setter
    def event_bind_count_threshold(self, event_bind_count_threshold):
        """Sets the event_bind_count_threshold of this MsgVpnTopicEndpoint.


        :param event_bind_count_threshold: The event_bind_count_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: EventThreshold
        """

        self._event_bind_count_threshold = event_bind_count_threshold

    @property
    def event_reject_low_priority_msg_limit_threshold(self):
        """Gets the event_reject_low_priority_msg_limit_threshold of this MsgVpnTopicEndpoint.  # noqa: E501


        :return: The event_reject_low_priority_msg_limit_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_reject_low_priority_msg_limit_threshold

    @event_reject_low_priority_msg_limit_threshold.setter
    def event_reject_low_priority_msg_limit_threshold(self, event_reject_low_priority_msg_limit_threshold):
        """Sets the event_reject_low_priority_msg_limit_threshold of this MsgVpnTopicEndpoint.


        :param event_reject_low_priority_msg_limit_threshold: The event_reject_low_priority_msg_limit_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: EventThreshold
        """

        self._event_reject_low_priority_msg_limit_threshold = event_reject_low_priority_msg_limit_threshold

    @property
    def event_spool_usage_threshold(self):
        """Gets the event_spool_usage_threshold of this MsgVpnTopicEndpoint.  # noqa: E501


        :return: The event_spool_usage_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_spool_usage_threshold

    @event_spool_usage_threshold.setter
    def event_spool_usage_threshold(self, event_spool_usage_threshold):
        """Sets the event_spool_usage_threshold of this MsgVpnTopicEndpoint.


        :param event_spool_usage_threshold: The event_spool_usage_threshold of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: EventThreshold
        """

        self._event_spool_usage_threshold = event_spool_usage_threshold

    @property
    def highest_acked_msg_id(self):
        """Gets the highest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The highest identifier (ID) of guaranteed messages in the Topic Endpoint that were acknowledged.  # noqa: E501

        :return: The highest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._highest_acked_msg_id

    @highest_acked_msg_id.setter
    def highest_acked_msg_id(self, highest_acked_msg_id):
        """Sets the highest_acked_msg_id of this MsgVpnTopicEndpoint.

        The highest identifier (ID) of guaranteed messages in the Topic Endpoint that were acknowledged.  # noqa: E501

        :param highest_acked_msg_id: The highest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._highest_acked_msg_id = highest_acked_msg_id

    @property
    def highest_msg_id(self):
        """Gets the highest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The highest identifier (ID) of guaranteed messages in the Topic Endpoint.  # noqa: E501

        :return: The highest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._highest_msg_id

    @highest_msg_id.setter
    def highest_msg_id(self, highest_msg_id):
        """Sets the highest_msg_id of this MsgVpnTopicEndpoint.

        The highest identifier (ID) of guaranteed messages in the Topic Endpoint.  # noqa: E501

        :param highest_msg_id: The highest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._highest_msg_id = highest_msg_id

    @property
    def in_progress_ack_msg_count(self):
        """Gets the in_progress_ack_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of acknowledgement messages received by the Topic Endpoint that are in the process of updating and deleting associated guaranteed messages.  # noqa: E501

        :return: The in_progress_ack_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._in_progress_ack_msg_count

    @in_progress_ack_msg_count.setter
    def in_progress_ack_msg_count(self, in_progress_ack_msg_count):
        """Sets the in_progress_ack_msg_count of this MsgVpnTopicEndpoint.

        The number of acknowledgement messages received by the Topic Endpoint that are in the process of updating and deleting associated guaranteed messages.  # noqa: E501

        :param in_progress_ack_msg_count: The in_progress_ack_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._in_progress_ack_msg_count = in_progress_ack_msg_count

    @property
    def ingress_enabled(self):
        """Gets the ingress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Enable or disable the reception of messages to the Topic Endpoint.  # noqa: E501

        :return: The ingress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._ingress_enabled

    @ingress_enabled.setter
    def ingress_enabled(self, ingress_enabled):
        """Sets the ingress_enabled of this MsgVpnTopicEndpoint.

        Enable or disable the reception of messages to the Topic Endpoint.  # noqa: E501

        :param ingress_enabled: The ingress_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._ingress_enabled = ingress_enabled

    @property
    def invalid_selector_bind_failure_count(self):
        """Gets the invalid_selector_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of Topic Endpoint bind failures due to an invalid selector.  # noqa: E501

        :return: The invalid_selector_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._invalid_selector_bind_failure_count

    @invalid_selector_bind_failure_count.setter
    def invalid_selector_bind_failure_count(self, invalid_selector_bind_failure_count):
        """Sets the invalid_selector_bind_failure_count of this MsgVpnTopicEndpoint.

        The number of Topic Endpoint bind failures due to an invalid selector.  # noqa: E501

        :param invalid_selector_bind_failure_count: The invalid_selector_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._invalid_selector_bind_failure_count = invalid_selector_bind_failure_count

    @property
    def last_replay_complete_time(self):
        """Gets the last_replay_complete_time of this MsgVpnTopicEndpoint.  # noqa: E501

        The timestamp of the last completed replay for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_replay_complete_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_replay_complete_time

    @last_replay_complete_time.setter
    def last_replay_complete_time(self, last_replay_complete_time):
        """Sets the last_replay_complete_time of this MsgVpnTopicEndpoint.

        The timestamp of the last completed replay for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_replay_complete_time: The last_replay_complete_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_replay_complete_time = last_replay_complete_time

    @property
    def last_replay_failure_reason(self):
        """Gets the last_replay_failure_reason of this MsgVpnTopicEndpoint.  # noqa: E501

        The reason for the last replay failure for the Topic Endpoint.  # noqa: E501

        :return: The last_replay_failure_reason of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._last_replay_failure_reason

    @last_replay_failure_reason.setter
    def last_replay_failure_reason(self, last_replay_failure_reason):
        """Sets the last_replay_failure_reason of this MsgVpnTopicEndpoint.

        The reason for the last replay failure for the Topic Endpoint.  # noqa: E501

        :param last_replay_failure_reason: The last_replay_failure_reason of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._last_replay_failure_reason = last_replay_failure_reason

    @property
    def last_replay_failure_time(self):
        """Gets the last_replay_failure_time of this MsgVpnTopicEndpoint.  # noqa: E501

        The timestamp of the last replay failure for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_replay_failure_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_replay_failure_time

    @last_replay_failure_time.setter
    def last_replay_failure_time(self, last_replay_failure_time):
        """Sets the last_replay_failure_time of this MsgVpnTopicEndpoint.

        The timestamp of the last replay failure for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_replay_failure_time: The last_replay_failure_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_replay_failure_time = last_replay_failure_time

    @property
    def last_replay_start_time(self):
        """Gets the last_replay_start_time of this MsgVpnTopicEndpoint.  # noqa: E501

        The timestamp of the last replay started for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_replay_start_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_replay_start_time

    @last_replay_start_time.setter
    def last_replay_start_time(self, last_replay_start_time):
        """Sets the last_replay_start_time of this MsgVpnTopicEndpoint.

        The timestamp of the last replay started for the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_replay_start_time: The last_replay_start_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_replay_start_time = last_replay_start_time

    @property
    def last_replayed_msg_tx_time(self):
        """Gets the last_replayed_msg_tx_time of this MsgVpnTopicEndpoint.  # noqa: E501

        The timestamp of the last replayed message transmitted by the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_replayed_msg_tx_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_replayed_msg_tx_time

    @last_replayed_msg_tx_time.setter
    def last_replayed_msg_tx_time(self, last_replayed_msg_tx_time):
        """Sets the last_replayed_msg_tx_time of this MsgVpnTopicEndpoint.

        The timestamp of the last replayed message transmitted by the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_replayed_msg_tx_time: The last_replayed_msg_tx_time of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_replayed_msg_tx_time = last_replayed_msg_tx_time

    @property
    def last_selector_examined_msg_id(self):
        """Gets the last_selector_examined_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The identifier (ID) of the last message examined by the Topic Endpoint selector.  # noqa: E501

        :return: The last_selector_examined_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_selector_examined_msg_id

    @last_selector_examined_msg_id.setter
    def last_selector_examined_msg_id(self, last_selector_examined_msg_id):
        """Sets the last_selector_examined_msg_id of this MsgVpnTopicEndpoint.

        The identifier (ID) of the last message examined by the Topic Endpoint selector.  # noqa: E501

        :param last_selector_examined_msg_id: The last_selector_examined_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_selector_examined_msg_id = last_selector_examined_msg_id

    @property
    def last_spooled_msg_id(self):
        """Gets the last_spooled_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The identifier (ID) of the last guaranteed message spooled in the Topic Endpoint.  # noqa: E501

        :return: The last_spooled_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._last_spooled_msg_id

    @last_spooled_msg_id.setter
    def last_spooled_msg_id(self, last_spooled_msg_id):
        """Sets the last_spooled_msg_id of this MsgVpnTopicEndpoint.

        The identifier (ID) of the last guaranteed message spooled in the Topic Endpoint.  # noqa: E501

        :param last_spooled_msg_id: The last_spooled_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._last_spooled_msg_id = last_spooled_msg_id

    @property
    def low_priority_msg_congestion_discarded_msg_count(self):
        """Gets the low_priority_msg_congestion_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to low priority message congestion control.  # noqa: E501

        :return: The low_priority_msg_congestion_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._low_priority_msg_congestion_discarded_msg_count

    @low_priority_msg_congestion_discarded_msg_count.setter
    def low_priority_msg_congestion_discarded_msg_count(self, low_priority_msg_congestion_discarded_msg_count):
        """Sets the low_priority_msg_congestion_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to low priority message congestion control.  # noqa: E501

        :param low_priority_msg_congestion_discarded_msg_count: The low_priority_msg_congestion_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._low_priority_msg_congestion_discarded_msg_count = low_priority_msg_congestion_discarded_msg_count

    @property
    def low_priority_msg_congestion_state(self):
        """Gets the low_priority_msg_congestion_state of this MsgVpnTopicEndpoint.  # noqa: E501

        The state of the low priority message congestion in the Topic Endpoint. The allowed values and their meaning are:  <pre> \"disabled\" - Messages are not being checked for priority. \"not-congested\" - Low priority messages are being stored and delivered. \"congested\" - Low priority messages are being discarded. </pre>   # noqa: E501

        :return: The low_priority_msg_congestion_state of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._low_priority_msg_congestion_state

    @low_priority_msg_congestion_state.setter
    def low_priority_msg_congestion_state(self, low_priority_msg_congestion_state):
        """Sets the low_priority_msg_congestion_state of this MsgVpnTopicEndpoint.

        The state of the low priority message congestion in the Topic Endpoint. The allowed values and their meaning are:  <pre> \"disabled\" - Messages are not being checked for priority. \"not-congested\" - Low priority messages are being stored and delivered. \"congested\" - Low priority messages are being discarded. </pre>   # noqa: E501

        :param low_priority_msg_congestion_state: The low_priority_msg_congestion_state of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._low_priority_msg_congestion_state = low_priority_msg_congestion_state

    @property
    def lowest_acked_msg_id(self):
        """Gets the lowest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The lowest identifier (ID) of guaranteed messages in the Topic Endpoint that were acknowledged.  # noqa: E501

        :return: The lowest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._lowest_acked_msg_id

    @lowest_acked_msg_id.setter
    def lowest_acked_msg_id(self, lowest_acked_msg_id):
        """Sets the lowest_acked_msg_id of this MsgVpnTopicEndpoint.

        The lowest identifier (ID) of guaranteed messages in the Topic Endpoint that were acknowledged.  # noqa: E501

        :param lowest_acked_msg_id: The lowest_acked_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._lowest_acked_msg_id = lowest_acked_msg_id

    @property
    def lowest_msg_id(self):
        """Gets the lowest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501

        The lowest identifier (ID) of guaranteed messages in the Topic Endpoint.  # noqa: E501

        :return: The lowest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._lowest_msg_id

    @lowest_msg_id.setter
    def lowest_msg_id(self, lowest_msg_id):
        """Sets the lowest_msg_id of this MsgVpnTopicEndpoint.

        The lowest identifier (ID) of guaranteed messages in the Topic Endpoint.  # noqa: E501

        :param lowest_msg_id: The lowest_msg_id of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._lowest_msg_id = lowest_msg_id

    @property
    def max_bind_count(self):
        """Gets the max_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum number of consumer flows that can bind to the Topic Endpoint.  # noqa: E501

        :return: The max_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_bind_count

    @max_bind_count.setter
    def max_bind_count(self, max_bind_count):
        """Sets the max_bind_count of this MsgVpnTopicEndpoint.

        The maximum number of consumer flows that can bind to the Topic Endpoint.  # noqa: E501

        :param max_bind_count: The max_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_bind_count = max_bind_count

    @property
    def max_bind_count_exceeded_bind_failure_count(self):
        """Gets the max_bind_count_exceeded_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of Topic Endpoint bind failures due to the maximum bind count being exceeded.  # noqa: E501

        :return: The max_bind_count_exceeded_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_bind_count_exceeded_bind_failure_count

    @max_bind_count_exceeded_bind_failure_count.setter
    def max_bind_count_exceeded_bind_failure_count(self, max_bind_count_exceeded_bind_failure_count):
        """Sets the max_bind_count_exceeded_bind_failure_count of this MsgVpnTopicEndpoint.

        The number of Topic Endpoint bind failures due to the maximum bind count being exceeded.  # noqa: E501

        :param max_bind_count_exceeded_bind_failure_count: The max_bind_count_exceeded_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_bind_count_exceeded_bind_failure_count = max_bind_count_exceeded_bind_failure_count

    @property
    def max_delivered_unacked_msgs_per_flow(self):
        """Gets the max_delivered_unacked_msgs_per_flow of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum number of messages delivered but not acknowledged per flow for the Topic Endpoint.  # noqa: E501

        :return: The max_delivered_unacked_msgs_per_flow of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_delivered_unacked_msgs_per_flow

    @max_delivered_unacked_msgs_per_flow.setter
    def max_delivered_unacked_msgs_per_flow(self, max_delivered_unacked_msgs_per_flow):
        """Sets the max_delivered_unacked_msgs_per_flow of this MsgVpnTopicEndpoint.

        The maximum number of messages delivered but not acknowledged per flow for the Topic Endpoint.  # noqa: E501

        :param max_delivered_unacked_msgs_per_flow: The max_delivered_unacked_msgs_per_flow of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_delivered_unacked_msgs_per_flow = max_delivered_unacked_msgs_per_flow

    @property
    def max_effective_bind_count(self):
        """Gets the max_effective_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The effective maximum number of consumer flows that can bind to the Topic Endpoint.  # noqa: E501

        :return: The max_effective_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_bind_count

    @max_effective_bind_count.setter
    def max_effective_bind_count(self, max_effective_bind_count):
        """Sets the max_effective_bind_count of this MsgVpnTopicEndpoint.

        The effective maximum number of consumer flows that can bind to the Topic Endpoint.  # noqa: E501

        :param max_effective_bind_count: The max_effective_bind_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_effective_bind_count = max_effective_bind_count

    @property
    def max_msg_size(self):
        """Gets the max_msg_size of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum message size allowed in the Topic Endpoint, in bytes (B).  # noqa: E501

        :return: The max_msg_size of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_size

    @max_msg_size.setter
    def max_msg_size(self, max_msg_size):
        """Sets the max_msg_size of this MsgVpnTopicEndpoint.

        The maximum message size allowed in the Topic Endpoint, in bytes (B).  # noqa: E501

        :param max_msg_size: The max_msg_size of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_msg_size = max_msg_size

    @property
    def max_msg_size_exceeded_discarded_msg_count(self):
        """Gets the max_msg_size_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum message size being exceeded.  # noqa: E501

        :return: The max_msg_size_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_size_exceeded_discarded_msg_count

    @max_msg_size_exceeded_discarded_msg_count.setter
    def max_msg_size_exceeded_discarded_msg_count(self, max_msg_size_exceeded_discarded_msg_count):
        """Sets the max_msg_size_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum message size being exceeded.  # noqa: E501

        :param max_msg_size_exceeded_discarded_msg_count: The max_msg_size_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_msg_size_exceeded_discarded_msg_count = max_msg_size_exceeded_discarded_msg_count

    @property
    def max_msg_spool_usage_exceeded_discarded_msg_count(self):
        """Gets the max_msg_spool_usage_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum message spool usage being exceeded.  # noqa: E501

        :return: The max_msg_spool_usage_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_spool_usage_exceeded_discarded_msg_count

    @max_msg_spool_usage_exceeded_discarded_msg_count.setter
    def max_msg_spool_usage_exceeded_discarded_msg_count(self, max_msg_spool_usage_exceeded_discarded_msg_count):
        """Sets the max_msg_spool_usage_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum message spool usage being exceeded.  # noqa: E501

        :param max_msg_spool_usage_exceeded_discarded_msg_count: The max_msg_spool_usage_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_msg_spool_usage_exceeded_discarded_msg_count = max_msg_spool_usage_exceeded_discarded_msg_count

    @property
    def max_redelivery_count(self):
        """Gets the max_redelivery_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum number of times the Topic Endpoint will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever.  # noqa: E501

        :return: The max_redelivery_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_redelivery_count

    @max_redelivery_count.setter
    def max_redelivery_count(self, max_redelivery_count):
        """Sets the max_redelivery_count of this MsgVpnTopicEndpoint.

        The maximum number of times the Topic Endpoint will attempt redelivery of a message prior to it being discarded or moved to the DMQ. A value of 0 means to retry forever.  # noqa: E501

        :param max_redelivery_count: The max_redelivery_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_redelivery_count = max_redelivery_count

    @property
    def max_redelivery_exceeded_discarded_msg_count(self):
        """Gets the max_redelivery_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum redelivery attempts being exceeded.  # noqa: E501

        :return: The max_redelivery_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_redelivery_exceeded_discarded_msg_count

    @max_redelivery_exceeded_discarded_msg_count.setter
    def max_redelivery_exceeded_discarded_msg_count(self, max_redelivery_exceeded_discarded_msg_count):
        """Sets the max_redelivery_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum redelivery attempts being exceeded.  # noqa: E501

        :param max_redelivery_exceeded_discarded_msg_count: The max_redelivery_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_redelivery_exceeded_discarded_msg_count = max_redelivery_exceeded_discarded_msg_count

    @property
    def max_redelivery_exceeded_to_dmq_failed_msg_count(self):
        """Gets the max_redelivery_exceeded_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum redelivery attempts being exceeded and failing to move to the Dead Message Queue (DMQ).  # noqa: E501

        :return: The max_redelivery_exceeded_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_redelivery_exceeded_to_dmq_failed_msg_count

    @max_redelivery_exceeded_to_dmq_failed_msg_count.setter
    def max_redelivery_exceeded_to_dmq_failed_msg_count(self, max_redelivery_exceeded_to_dmq_failed_msg_count):
        """Sets the max_redelivery_exceeded_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum redelivery attempts being exceeded and failing to move to the Dead Message Queue (DMQ).  # noqa: E501

        :param max_redelivery_exceeded_to_dmq_failed_msg_count: The max_redelivery_exceeded_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_redelivery_exceeded_to_dmq_failed_msg_count = max_redelivery_exceeded_to_dmq_failed_msg_count

    @property
    def max_redelivery_exceeded_to_dmq_msg_count(self):
        """Gets the max_redelivery_exceeded_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages moved to the Dead Message Queue (DMQ) by the Topic Endpoint due to the maximum redelivery attempts being exceeded.  # noqa: E501

        :return: The max_redelivery_exceeded_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_redelivery_exceeded_to_dmq_msg_count

    @max_redelivery_exceeded_to_dmq_msg_count.setter
    def max_redelivery_exceeded_to_dmq_msg_count(self, max_redelivery_exceeded_to_dmq_msg_count):
        """Sets the max_redelivery_exceeded_to_dmq_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages moved to the Dead Message Queue (DMQ) by the Topic Endpoint due to the maximum redelivery attempts being exceeded.  # noqa: E501

        :param max_redelivery_exceeded_to_dmq_msg_count: The max_redelivery_exceeded_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_redelivery_exceeded_to_dmq_msg_count = max_redelivery_exceeded_to_dmq_msg_count

    @property
    def max_spool_usage(self):
        """Gets the max_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum message spool usage allowed by the Topic Endpoint, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking.  # noqa: E501

        :return: The max_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_spool_usage

    @max_spool_usage.setter
    def max_spool_usage(self, max_spool_usage):
        """Sets the max_spool_usage of this MsgVpnTopicEndpoint.

        The maximum message spool usage allowed by the Topic Endpoint, in megabytes (MB). A value of 0 only allows spooling of the last message received and disables quota checking.  # noqa: E501

        :param max_spool_usage: The max_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_spool_usage = max_spool_usage

    @property
    def max_ttl(self):
        """Gets the max_ttl of this MsgVpnTopicEndpoint.  # noqa: E501

        The maximum time in seconds a message can stay in the Topic Endpoint when `respectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `maxTtl` configured for the Topic Endpoint, is exceeded. A value of 0 disables expiry.  # noqa: E501

        :return: The max_ttl of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl

    @max_ttl.setter
    def max_ttl(self, max_ttl):
        """Sets the max_ttl of this MsgVpnTopicEndpoint.

        The maximum time in seconds a message can stay in the Topic Endpoint when `respectTtlEnabled` is `\"true\"`. A message expires when the lesser of the sender assigned time-to-live (TTL) in the message and the `maxTtl` configured for the Topic Endpoint, is exceeded. A value of 0 disables expiry.  # noqa: E501

        :param max_ttl: The max_ttl of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_ttl = max_ttl

    @property
    def max_ttl_exceeded_discarded_msg_count(self):
        """Gets the max_ttl_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) in hops being exceeded. The TTL hop count is incremented when the message crosses a bridge.  # noqa: E501

        :return: The max_ttl_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl_exceeded_discarded_msg_count

    @max_ttl_exceeded_discarded_msg_count.setter
    def max_ttl_exceeded_discarded_msg_count(self, max_ttl_exceeded_discarded_msg_count):
        """Sets the max_ttl_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) in hops being exceeded. The TTL hop count is incremented when the message crosses a bridge.  # noqa: E501

        :param max_ttl_exceeded_discarded_msg_count: The max_ttl_exceeded_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_ttl_exceeded_discarded_msg_count = max_ttl_exceeded_discarded_msg_count

    @property
    def max_ttl_expired_discarded_msg_count(self):
        """Gets the max_ttl_expired_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring.  # noqa: E501

        :return: The max_ttl_expired_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl_expired_discarded_msg_count

    @max_ttl_expired_discarded_msg_count.setter
    def max_ttl_expired_discarded_msg_count(self, max_ttl_expired_discarded_msg_count):
        """Sets the max_ttl_expired_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring.  # noqa: E501

        :param max_ttl_expired_discarded_msg_count: The max_ttl_expired_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_ttl_expired_discarded_msg_count = max_ttl_expired_discarded_msg_count

    @property
    def max_ttl_expired_to_dmq_failed_msg_count(self):
        """Gets the max_ttl_expired_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring and failing to move to the Dead Message Queue (DMQ).  # noqa: E501

        :return: The max_ttl_expired_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl_expired_to_dmq_failed_msg_count

    @max_ttl_expired_to_dmq_failed_msg_count.setter
    def max_ttl_expired_to_dmq_failed_msg_count(self, max_ttl_expired_to_dmq_failed_msg_count):
        """Sets the max_ttl_expired_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring and failing to move to the Dead Message Queue (DMQ).  # noqa: E501

        :param max_ttl_expired_to_dmq_failed_msg_count: The max_ttl_expired_to_dmq_failed_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_ttl_expired_to_dmq_failed_msg_count = max_ttl_expired_to_dmq_failed_msg_count

    @property
    def max_ttl_expired_to_dmq_msg_count(self):
        """Gets the max_ttl_expired_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages moved to the Dead Message Queue (DMQ) by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring.  # noqa: E501

        :return: The max_ttl_expired_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl_expired_to_dmq_msg_count

    @max_ttl_expired_to_dmq_msg_count.setter
    def max_ttl_expired_to_dmq_msg_count(self, max_ttl_expired_to_dmq_msg_count):
        """Sets the max_ttl_expired_to_dmq_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages moved to the Dead Message Queue (DMQ) by the Topic Endpoint due to the maximum time-to-live (TTL) timestamp expiring.  # noqa: E501

        :param max_ttl_expired_to_dmq_msg_count: The max_ttl_expired_to_dmq_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._max_ttl_expired_to_dmq_msg_count = max_ttl_expired_to_dmq_msg_count

    @property
    def msg_spool_peak_usage(self):
        """Gets the msg_spool_peak_usage of this MsgVpnTopicEndpoint.  # noqa: E501

        The message spool peak usage by the Topic Endpoint, in bytes (B).  # noqa: E501

        :return: The msg_spool_peak_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_peak_usage

    @msg_spool_peak_usage.setter
    def msg_spool_peak_usage(self, msg_spool_peak_usage):
        """Sets the msg_spool_peak_usage of this MsgVpnTopicEndpoint.

        The message spool peak usage by the Topic Endpoint, in bytes (B).  # noqa: E501

        :param msg_spool_peak_usage: The msg_spool_peak_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._msg_spool_peak_usage = msg_spool_peak_usage

    @property
    def msg_spool_usage(self):
        """Gets the msg_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501

        The message spool usage by the Topic Endpoint, in bytes (B).  # noqa: E501

        :return: The msg_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_usage

    @msg_spool_usage.setter
    def msg_spool_usage(self, msg_spool_usage):
        """Sets the msg_spool_usage of this MsgVpnTopicEndpoint.

        The message spool usage by the Topic Endpoint, in bytes (B).  # noqa: E501

        :param msg_spool_usage: The msg_spool_usage of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._msg_spool_usage = msg_spool_usage

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnTopicEndpoint.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnTopicEndpoint.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def network_topic(self):
        """Gets the network_topic of this MsgVpnTopicEndpoint.  # noqa: E501

        The name of the network topic for the Topic Endpoint.  # noqa: E501

        :return: The network_topic of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._network_topic

    @network_topic.setter
    def network_topic(self, network_topic):
        """Sets the network_topic of this MsgVpnTopicEndpoint.

        The name of the network topic for the Topic Endpoint.  # noqa: E501

        :param network_topic: The network_topic of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._network_topic = network_topic

    @property
    def no_local_delivery_discarded_msg_count(self):
        """Gets the no_local_delivery_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages discarded by the Topic Endpoint due to no local delivery being requested.  # noqa: E501

        :return: The no_local_delivery_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._no_local_delivery_discarded_msg_count

    @no_local_delivery_discarded_msg_count.setter
    def no_local_delivery_discarded_msg_count(self, no_local_delivery_discarded_msg_count):
        """Sets the no_local_delivery_discarded_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages discarded by the Topic Endpoint due to no local delivery being requested.  # noqa: E501

        :param no_local_delivery_discarded_msg_count: The no_local_delivery_discarded_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._no_local_delivery_discarded_msg_count = no_local_delivery_discarded_msg_count

    @property
    def other_bind_failure_count(self):
        """Gets the other_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of Topic Endpoint bind failures due to other reasons.  # noqa: E501

        :return: The other_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._other_bind_failure_count

    @other_bind_failure_count.setter
    def other_bind_failure_count(self, other_bind_failure_count):
        """Sets the other_bind_failure_count of this MsgVpnTopicEndpoint.

        The number of Topic Endpoint bind failures due to other reasons.  # noqa: E501

        :param other_bind_failure_count: The other_bind_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._other_bind_failure_count = other_bind_failure_count

    @property
    def owner(self):
        """Gets the owner of this MsgVpnTopicEndpoint.  # noqa: E501

        The Client Username that owns the Topic Endpoint and has permission equivalent to `\"delete\"`.  # noqa: E501

        :return: The owner of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this MsgVpnTopicEndpoint.

        The Client Username that owns the Topic Endpoint and has permission equivalent to `\"delete\"`.  # noqa: E501

        :param owner: The owner of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def permission(self):
        """Gets the permission of this MsgVpnTopicEndpoint.  # noqa: E501

        The permission level for all consumers of the Topic Endpoint, excluding the owner. The allowed values and their meaning are:  <pre> \"no-access\" - Disallows all access. \"read-only\" - Read-only access to the messages. \"consume\" - Consume (read and remove) messages. \"modify-topic\" - Consume messages or modify the topic/selector. \"delete\" - Consume messages, modify the topic/selector or delete the Client created endpoint altogether. </pre>   # noqa: E501

        :return: The permission of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """Sets the permission of this MsgVpnTopicEndpoint.

        The permission level for all consumers of the Topic Endpoint, excluding the owner. The allowed values and their meaning are:  <pre> \"no-access\" - Disallows all access. \"read-only\" - Read-only access to the messages. \"consume\" - Consume (read and remove) messages. \"modify-topic\" - Consume messages or modify the topic/selector. \"delete\" - Consume messages, modify the topic/selector or delete the Client created endpoint altogether. </pre>   # noqa: E501

        :param permission: The permission of this MsgVpnTopicEndpoint.  # noqa: E501
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
    def redelivered_msg_count(self):
        """Gets the redelivered_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages transmitted by the Topic Endpoint for redelivery.  # noqa: E501

        :return: The redelivered_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._redelivered_msg_count

    @redelivered_msg_count.setter
    def redelivered_msg_count(self, redelivered_msg_count):
        """Sets the redelivered_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages transmitted by the Topic Endpoint for redelivery.  # noqa: E501

        :param redelivered_msg_count: The redelivered_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._redelivered_msg_count = redelivered_msg_count

    @property
    def reject_low_priority_msg_enabled(self):
        """Gets the reject_low_priority_msg_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Enable or disable the checking of low priority messages against the `rejectLowPriorityMsgLimit`. This may only be enabled if `rejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`.  # noqa: E501

        :return: The reject_low_priority_msg_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._reject_low_priority_msg_enabled

    @reject_low_priority_msg_enabled.setter
    def reject_low_priority_msg_enabled(self, reject_low_priority_msg_enabled):
        """Sets the reject_low_priority_msg_enabled of this MsgVpnTopicEndpoint.

        Enable or disable the checking of low priority messages against the `rejectLowPriorityMsgLimit`. This may only be enabled if `rejectMsgToSenderOnDiscardBehavior` does not have a value of `\"never\"`.  # noqa: E501

        :param reject_low_priority_msg_enabled: The reject_low_priority_msg_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._reject_low_priority_msg_enabled = reject_low_priority_msg_enabled

    @property
    def reject_low_priority_msg_limit(self):
        """Gets the reject_low_priority_msg_limit of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of messages of any priority in the Topic Endpoint above which low priority messages are not admitted but higher priority messages are allowed.  # noqa: E501

        :return: The reject_low_priority_msg_limit of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._reject_low_priority_msg_limit

    @reject_low_priority_msg_limit.setter
    def reject_low_priority_msg_limit(self, reject_low_priority_msg_limit):
        """Sets the reject_low_priority_msg_limit of this MsgVpnTopicEndpoint.

        The number of messages of any priority in the Topic Endpoint above which low priority messages are not admitted but higher priority messages are allowed.  # noqa: E501

        :param reject_low_priority_msg_limit: The reject_low_priority_msg_limit of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._reject_low_priority_msg_limit = reject_low_priority_msg_limit

    @property
    def reject_msg_to_sender_on_discard_behavior(self):
        """Gets the reject_msg_to_sender_on_discard_behavior of this MsgVpnTopicEndpoint.  # noqa: E501

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-topic-endpoint-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Topic Endpoint is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :return: The reject_msg_to_sender_on_discard_behavior of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._reject_msg_to_sender_on_discard_behavior

    @reject_msg_to_sender_on_discard_behavior.setter
    def reject_msg_to_sender_on_discard_behavior(self, reject_msg_to_sender_on_discard_behavior):
        """Sets the reject_msg_to_sender_on_discard_behavior of this MsgVpnTopicEndpoint.

        Determines when to return negative acknowledgements (NACKs) to sending clients on message discards. Note that NACKs cause the message to not be delivered to any destination and Transacted Session commits to fail. The allowed values and their meaning are:  <pre> \"always\" - Always return a negative acknowledgment (NACK) to the sending client on message discard. \"when-topic-endpoint-enabled\" - Only return a negative acknowledgment (NACK) to the sending client on message discard when the Topic Endpoint is enabled. \"never\" - Never return a negative acknowledgment (NACK) to the sending client on message discard. </pre>   # noqa: E501

        :param reject_msg_to_sender_on_discard_behavior: The reject_msg_to_sender_on_discard_behavior of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """
        allowed_values = ["always", "when-topic-endpoint-enabled", "never"]  # noqa: E501
        if reject_msg_to_sender_on_discard_behavior not in allowed_values:
            raise ValueError(
                "Invalid value for `reject_msg_to_sender_on_discard_behavior` ({0}), must be one of {1}"  # noqa: E501
                .format(reject_msg_to_sender_on_discard_behavior, allowed_values)
            )

        self._reject_msg_to_sender_on_discard_behavior = reject_msg_to_sender_on_discard_behavior

    @property
    def replay_failure_count(self):
        """Gets the replay_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of replays that failed for the Topic Endpoint.  # noqa: E501

        :return: The replay_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replay_failure_count

    @replay_failure_count.setter
    def replay_failure_count(self, replay_failure_count):
        """Sets the replay_failure_count of this MsgVpnTopicEndpoint.

        The number of replays that failed for the Topic Endpoint.  # noqa: E501

        :param replay_failure_count: The replay_failure_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replay_failure_count = replay_failure_count

    @property
    def replay_start_count(self):
        """Gets the replay_start_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of replays started for the Topic Endpoint.  # noqa: E501

        :return: The replay_start_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replay_start_count

    @replay_start_count.setter
    def replay_start_count(self, replay_start_count):
        """Sets the replay_start_count of this MsgVpnTopicEndpoint.

        The number of replays started for the Topic Endpoint.  # noqa: E501

        :param replay_start_count: The replay_start_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replay_start_count = replay_start_count

    @property
    def replay_state(self):
        """Gets the replay_state of this MsgVpnTopicEndpoint.  # noqa: E501

        The state of replay for the Topic Endpoint. The allowed values and their meaning are:  <pre> \"initializing\" - All messages are being deleted from the endpoint before replay starts. \"active\" - Subscription matching logged messages are being replayed to the endpoint. \"pending-complete\" - Replay is complete, but final accounting is in progress. \"complete\" - Replay and all related activities are complete. \"failed\" - Replay has failed and is waiting for an unbind response. </pre>   # noqa: E501

        :return: The replay_state of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._replay_state

    @replay_state.setter
    def replay_state(self, replay_state):
        """Sets the replay_state of this MsgVpnTopicEndpoint.

        The state of replay for the Topic Endpoint. The allowed values and their meaning are:  <pre> \"initializing\" - All messages are being deleted from the endpoint before replay starts. \"active\" - Subscription matching logged messages are being replayed to the endpoint. \"pending-complete\" - Replay is complete, but final accounting is in progress. \"complete\" - Replay and all related activities are complete. \"failed\" - Replay has failed and is waiting for an unbind response. </pre>   # noqa: E501

        :param replay_state: The replay_state of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._replay_state = replay_state

    @property
    def replay_success_count(self):
        """Gets the replay_success_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of replays that succeeded for the Topic Endpoint.  # noqa: E501

        :return: The replay_success_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replay_success_count

    @replay_success_count.setter
    def replay_success_count(self, replay_success_count):
        """Sets the replay_success_count of this MsgVpnTopicEndpoint.

        The number of replays that succeeded for the Topic Endpoint.  # noqa: E501

        :param replay_success_count: The replay_success_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replay_success_count = replay_success_count

    @property
    def replayed_acked_msg_count(self):
        """Gets the replayed_acked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of replayed messages transmitted by the Topic Endpoint and acked by all consumers.  # noqa: E501

        :return: The replayed_acked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replayed_acked_msg_count

    @replayed_acked_msg_count.setter
    def replayed_acked_msg_count(self, replayed_acked_msg_count):
        """Sets the replayed_acked_msg_count of this MsgVpnTopicEndpoint.

        The number of replayed messages transmitted by the Topic Endpoint and acked by all consumers.  # noqa: E501

        :param replayed_acked_msg_count: The replayed_acked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replayed_acked_msg_count = replayed_acked_msg_count

    @property
    def replayed_tx_msg_count(self):
        """Gets the replayed_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of replayed messages transmitted by the Topic Endpoint.  # noqa: E501

        :return: The replayed_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replayed_tx_msg_count

    @replayed_tx_msg_count.setter
    def replayed_tx_msg_count(self, replayed_tx_msg_count):
        """Sets the replayed_tx_msg_count of this MsgVpnTopicEndpoint.

        The number of replayed messages transmitted by the Topic Endpoint.  # noqa: E501

        :param replayed_tx_msg_count: The replayed_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replayed_tx_msg_count = replayed_tx_msg_count

    @property
    def replication_active_ack_prop_tx_msg_count(self):
        """Gets the replication_active_ack_prop_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of acknowledgement messages propagated by the Topic Endpoint to the replication standby remote Message VPN.  # noqa: E501

        :return: The replication_active_ack_prop_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_ack_prop_tx_msg_count

    @replication_active_ack_prop_tx_msg_count.setter
    def replication_active_ack_prop_tx_msg_count(self, replication_active_ack_prop_tx_msg_count):
        """Sets the replication_active_ack_prop_tx_msg_count of this MsgVpnTopicEndpoint.

        The number of acknowledgement messages propagated by the Topic Endpoint to the replication standby remote Message VPN.  # noqa: E501

        :param replication_active_ack_prop_tx_msg_count: The replication_active_ack_prop_tx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replication_active_ack_prop_tx_msg_count = replication_active_ack_prop_tx_msg_count

    @property
    def replication_standby_ack_prop_rx_msg_count(self):
        """Gets the replication_standby_ack_prop_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of propagated acknowledgement messages received by the Topic Endpoint from the replication active remote Message VPN.  # noqa: E501

        :return: The replication_standby_ack_prop_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_ack_prop_rx_msg_count

    @replication_standby_ack_prop_rx_msg_count.setter
    def replication_standby_ack_prop_rx_msg_count(self, replication_standby_ack_prop_rx_msg_count):
        """Sets the replication_standby_ack_prop_rx_msg_count of this MsgVpnTopicEndpoint.

        The number of propagated acknowledgement messages received by the Topic Endpoint from the replication active remote Message VPN.  # noqa: E501

        :param replication_standby_ack_prop_rx_msg_count: The replication_standby_ack_prop_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replication_standby_ack_prop_rx_msg_count = replication_standby_ack_prop_rx_msg_count

    @property
    def replication_standby_acked_by_ack_prop_msg_count(self):
        """Gets the replication_standby_acked_by_ack_prop_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of messages acknowledged in the Topic Endpoint by acknowledgement propagation from the replication active remote Message VPN.  # noqa: E501

        :return: The replication_standby_acked_by_ack_prop_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_acked_by_ack_prop_msg_count

    @replication_standby_acked_by_ack_prop_msg_count.setter
    def replication_standby_acked_by_ack_prop_msg_count(self, replication_standby_acked_by_ack_prop_msg_count):
        """Sets the replication_standby_acked_by_ack_prop_msg_count of this MsgVpnTopicEndpoint.

        The number of messages acknowledged in the Topic Endpoint by acknowledgement propagation from the replication active remote Message VPN.  # noqa: E501

        :param replication_standby_acked_by_ack_prop_msg_count: The replication_standby_acked_by_ack_prop_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replication_standby_acked_by_ack_prop_msg_count = replication_standby_acked_by_ack_prop_msg_count

    @property
    def replication_standby_rx_msg_count(self):
        """Gets the replication_standby_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of messages received by the Topic Endpoint from the replication active remote Message VPN.  # noqa: E501

        :return: The replication_standby_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_rx_msg_count

    @replication_standby_rx_msg_count.setter
    def replication_standby_rx_msg_count(self, replication_standby_rx_msg_count):
        """Sets the replication_standby_rx_msg_count of this MsgVpnTopicEndpoint.

        The number of messages received by the Topic Endpoint from the replication active remote Message VPN.  # noqa: E501

        :param replication_standby_rx_msg_count: The replication_standby_rx_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._replication_standby_rx_msg_count = replication_standby_rx_msg_count

    @property
    def respect_msg_priority_enabled(self):
        """Gets the respect_msg_priority_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Indicates whether the respecting of message priority is enabled. When enabled, messages contained in the Topic Endpoint are delivered in priority order, from 9 (highest) to 0 (lowest).  # noqa: E501

        :return: The respect_msg_priority_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._respect_msg_priority_enabled

    @respect_msg_priority_enabled.setter
    def respect_msg_priority_enabled(self, respect_msg_priority_enabled):
        """Sets the respect_msg_priority_enabled of this MsgVpnTopicEndpoint.

        Indicates whether the respecting of message priority is enabled. When enabled, messages contained in the Topic Endpoint are delivered in priority order, from 9 (highest) to 0 (lowest).  # noqa: E501

        :param respect_msg_priority_enabled: The respect_msg_priority_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._respect_msg_priority_enabled = respect_msg_priority_enabled

    @property
    def respect_ttl_enabled(self):
        """Gets the respect_ttl_enabled of this MsgVpnTopicEndpoint.  # noqa: E501

        Enable or disable the respecting of the time-to-live (TTL) for messages in the Topic Endpoint. When enabled, expired messages are discarded or moved to the DMQ.  # noqa: E501

        :return: The respect_ttl_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._respect_ttl_enabled

    @respect_ttl_enabled.setter
    def respect_ttl_enabled(self, respect_ttl_enabled):
        """Sets the respect_ttl_enabled of this MsgVpnTopicEndpoint.

        Enable or disable the respecting of the time-to-live (TTL) for messages in the Topic Endpoint. When enabled, expired messages are discarded or moved to the DMQ.  # noqa: E501

        :param respect_ttl_enabled: The respect_ttl_enabled of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._respect_ttl_enabled = respect_ttl_enabled

    @property
    def rx_byte_rate(self):
        """Gets the rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The current message rate received by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :return: The rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_rate

    @rx_byte_rate.setter
    def rx_byte_rate(self, rx_byte_rate):
        """Sets the rx_byte_rate of this MsgVpnTopicEndpoint.

        The current message rate received by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :param rx_byte_rate: The rx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._rx_byte_rate = rx_byte_rate

    @property
    def rx_msg_rate(self):
        """Gets the rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The current message rate received by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :return: The rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_rate

    @rx_msg_rate.setter
    def rx_msg_rate(self, rx_msg_rate):
        """Sets the rx_msg_rate of this MsgVpnTopicEndpoint.

        The current message rate received by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :param rx_msg_rate: The rx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._rx_msg_rate = rx_msg_rate

    @property
    def rx_selector(self):
        """Gets the rx_selector of this MsgVpnTopicEndpoint.  # noqa: E501

        Indicates whether the Topic Endpoint has a selector to filter received messages.  # noqa: E501

        :return: The rx_selector of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: bool
        """
        return self._rx_selector

    @rx_selector.setter
    def rx_selector(self, rx_selector):
        """Sets the rx_selector of this MsgVpnTopicEndpoint.

        Indicates whether the Topic Endpoint has a selector to filter received messages.  # noqa: E501

        :param rx_selector: The rx_selector of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: bool
        """

        self._rx_selector = rx_selector

    @property
    def selector(self):
        """Gets the selector of this MsgVpnTopicEndpoint.  # noqa: E501

        The value of the receive selector for the Topic Endpoint.  # noqa: E501

        :return: The selector of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._selector

    @selector.setter
    def selector(self, selector):
        """Sets the selector of this MsgVpnTopicEndpoint.

        The value of the receive selector for the Topic Endpoint.  # noqa: E501

        :param selector: The selector of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._selector = selector

    @property
    def selector_examined_msg_count(self):
        """Gets the selector_examined_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages examined by the Topic Endpoint selector.  # noqa: E501

        :return: The selector_examined_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._selector_examined_msg_count

    @selector_examined_msg_count.setter
    def selector_examined_msg_count(self, selector_examined_msg_count):
        """Sets the selector_examined_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages examined by the Topic Endpoint selector.  # noqa: E501

        :param selector_examined_msg_count: The selector_examined_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._selector_examined_msg_count = selector_examined_msg_count

    @property
    def selector_matched_msg_count(self):
        """Gets the selector_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages for which the Topic Endpoint selector matched.  # noqa: E501

        :return: The selector_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._selector_matched_msg_count

    @selector_matched_msg_count.setter
    def selector_matched_msg_count(self, selector_matched_msg_count):
        """Sets the selector_matched_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages for which the Topic Endpoint selector matched.  # noqa: E501

        :param selector_matched_msg_count: The selector_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._selector_matched_msg_count = selector_matched_msg_count

    @property
    def selector_not_matched_msg_count(self):
        """Gets the selector_not_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages for which the Topic Endpoint selector did not match.  # noqa: E501

        :return: The selector_not_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._selector_not_matched_msg_count

    @selector_not_matched_msg_count.setter
    def selector_not_matched_msg_count(self, selector_not_matched_msg_count):
        """Sets the selector_not_matched_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages for which the Topic Endpoint selector did not match.  # noqa: E501

        :param selector_not_matched_msg_count: The selector_not_matched_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._selector_not_matched_msg_count = selector_not_matched_msg_count

    @property
    def spooled_byte_count(self):
        """Gets the spooled_byte_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The amount of guaranteed messages that were spooled in the Topic Endpoint, in bytes (B).  # noqa: E501

        :return: The spooled_byte_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._spooled_byte_count

    @spooled_byte_count.setter
    def spooled_byte_count(self, spooled_byte_count):
        """Sets the spooled_byte_count of this MsgVpnTopicEndpoint.

        The amount of guaranteed messages that were spooled in the Topic Endpoint, in bytes (B).  # noqa: E501

        :param spooled_byte_count: The spooled_byte_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._spooled_byte_count = spooled_byte_count

    @property
    def spooled_msg_count(self):
        """Gets the spooled_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages that were spooled in the Topic Endpoint.  # noqa: E501

        :return: The spooled_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._spooled_msg_count

    @spooled_msg_count.setter
    def spooled_msg_count(self, spooled_msg_count):
        """Sets the spooled_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages that were spooled in the Topic Endpoint.  # noqa: E501

        :param spooled_msg_count: The spooled_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._spooled_msg_count = spooled_msg_count

    @property
    def topic_endpoint_name(self):
        """Gets the topic_endpoint_name of this MsgVpnTopicEndpoint.  # noqa: E501

        The name of the Topic Endpoint.  # noqa: E501

        :return: The topic_endpoint_name of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._topic_endpoint_name

    @topic_endpoint_name.setter
    def topic_endpoint_name(self, topic_endpoint_name):
        """Sets the topic_endpoint_name of this MsgVpnTopicEndpoint.

        The name of the Topic Endpoint.  # noqa: E501

        :param topic_endpoint_name: The topic_endpoint_name of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._topic_endpoint_name = topic_endpoint_name

    @property
    def tx_byte_rate(self):
        """Gets the tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The current message rate transmitted by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :return: The tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_rate

    @tx_byte_rate.setter
    def tx_byte_rate(self, tx_byte_rate):
        """Sets the tx_byte_rate of this MsgVpnTopicEndpoint.

        The current message rate transmitted by the Topic Endpoint, in bytes per second (B/sec).  # noqa: E501

        :param tx_byte_rate: The tx_byte_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._tx_byte_rate = tx_byte_rate

    @property
    def tx_msg_rate(self):
        """Gets the tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501

        The current message rate transmitted by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :return: The tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_rate

    @tx_msg_rate.setter
    def tx_msg_rate(self, tx_msg_rate):
        """Sets the tx_msg_rate of this MsgVpnTopicEndpoint.

        The current message rate transmitted by the Topic Endpoint, in messages per second (msg/sec).  # noqa: E501

        :param tx_msg_rate: The tx_msg_rate of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._tx_msg_rate = tx_msg_rate

    @property
    def tx_unacked_msg_count(self):
        """Gets the tx_unacked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501

        The number of guaranteed messages in the Topic Endpoint that have been transmitted but not acknowledged by all consumers.  # noqa: E501

        :return: The tx_unacked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: int
        """
        return self._tx_unacked_msg_count

    @tx_unacked_msg_count.setter
    def tx_unacked_msg_count(self, tx_unacked_msg_count):
        """Sets the tx_unacked_msg_count of this MsgVpnTopicEndpoint.

        The number of guaranteed messages in the Topic Endpoint that have been transmitted but not acknowledged by all consumers.  # noqa: E501

        :param tx_unacked_msg_count: The tx_unacked_msg_count of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: int
        """

        self._tx_unacked_msg_count = tx_unacked_msg_count

    @property
    def virtual_router(self):
        """Gets the virtual_router of this MsgVpnTopicEndpoint.  # noqa: E501

        The virtual router used by the Topic Endpoint. The allowed values and their meaning are:  <pre> \"primary\" - The endpoint belongs to the primary virtual router. \"backup\" - The endpoint belongs to the backup virtual router. </pre>   # noqa: E501

        :return: The virtual_router of this MsgVpnTopicEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._virtual_router

    @virtual_router.setter
    def virtual_router(self, virtual_router):
        """Sets the virtual_router of this MsgVpnTopicEndpoint.

        The virtual router used by the Topic Endpoint. The allowed values and their meaning are:  <pre> \"primary\" - The endpoint belongs to the primary virtual router. \"backup\" - The endpoint belongs to the backup virtual router. </pre>   # noqa: E501

        :param virtual_router: The virtual_router of this MsgVpnTopicEndpoint.  # noqa: E501
        :type: str
        """

        self._virtual_router = virtual_router

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
        if issubclass(MsgVpnTopicEndpoint, dict):
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
        if not isinstance(other, MsgVpnTopicEndpoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
