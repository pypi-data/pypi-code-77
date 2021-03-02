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


class MsgVpnClient(object):
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
        'acl_profile_name': 'str',
        'already_bound_bind_failure_count': 'int',
        'authorization_group_name': 'str',
        'average_rx_byte_rate': 'int',
        'average_rx_msg_rate': 'int',
        'average_tx_byte_rate': 'int',
        'average_tx_msg_rate': 'int',
        'bind_request_count': 'int',
        'bind_success_count': 'int',
        'client_address': 'str',
        'client_id': 'int',
        'client_name': 'str',
        'client_profile_name': 'str',
        'client_username': 'str',
        'control_rx_byte_count': 'int',
        'control_rx_msg_count': 'int',
        'control_tx_byte_count': 'int',
        'control_tx_msg_count': 'int',
        'cut_through_denied_bind_failure_count': 'int',
        'data_rx_byte_count': 'int',
        'data_rx_msg_count': 'int',
        'data_tx_byte_count': 'int',
        'data_tx_msg_count': 'int',
        'description': 'str',
        'disabled_bind_failure_count': 'int',
        'dto_local_priority': 'int',
        'dto_network_priority': 'int',
        'eliding': 'bool',
        'eliding_topic_count': 'int',
        'eliding_topic_peak_count': 'int',
        'guaranteed_denied_bind_failure_count': 'int',
        'invalid_selector_bind_failure_count': 'int',
        'large_msg_event_raised': 'bool',
        'login_rx_msg_count': 'int',
        'login_tx_msg_count': 'int',
        'max_bind_count_exceeded_bind_failure_count': 'int',
        'max_eliding_topic_count_event_raised': 'bool',
        'mqtt_connack_error_tx_count': 'int',
        'mqtt_connack_tx_count': 'int',
        'mqtt_connect_rx_count': 'int',
        'mqtt_disconnect_rx_count': 'int',
        'mqtt_pingreq_rx_count': 'int',
        'mqtt_pingresp_tx_count': 'int',
        'mqtt_puback_rx_count': 'int',
        'mqtt_puback_tx_count': 'int',
        'mqtt_pubcomp_tx_count': 'int',
        'mqtt_publish_qos0_rx_count': 'int',
        'mqtt_publish_qos0_tx_count': 'int',
        'mqtt_publish_qos1_rx_count': 'int',
        'mqtt_publish_qos1_tx_count': 'int',
        'mqtt_publish_qos2_rx_count': 'int',
        'mqtt_pubrec_tx_count': 'int',
        'mqtt_pubrel_rx_count': 'int',
        'mqtt_suback_error_tx_count': 'int',
        'mqtt_suback_tx_count': 'int',
        'mqtt_subscribe_rx_count': 'int',
        'mqtt_unsuback_tx_count': 'int',
        'mqtt_unsubscribe_rx_count': 'int',
        'msg_spool_congestion_rx_discarded_msg_count': 'int',
        'msg_spool_rx_discarded_msg_count': 'int',
        'msg_vpn_name': 'str',
        'no_local_delivery': 'bool',
        'no_subscription_match_rx_discarded_msg_count': 'int',
        'original_client_username': 'str',
        'other_bind_failure_count': 'int',
        'platform': 'str',
        'publish_topic_acl_rx_discarded_msg_count': 'int',
        'rest_http_request_rx_byte_count': 'int',
        'rest_http_request_rx_msg_count': 'int',
        'rest_http_request_tx_byte_count': 'int',
        'rest_http_request_tx_msg_count': 'int',
        'rest_http_response_error_rx_msg_count': 'int',
        'rest_http_response_error_tx_msg_count': 'int',
        'rest_http_response_rx_byte_count': 'int',
        'rest_http_response_rx_msg_count': 'int',
        'rest_http_response_success_rx_msg_count': 'int',
        'rest_http_response_success_tx_msg_count': 'int',
        'rest_http_response_timeout_rx_msg_count': 'int',
        'rest_http_response_timeout_tx_msg_count': 'int',
        'rest_http_response_tx_byte_count': 'int',
        'rest_http_response_tx_msg_count': 'int',
        'rx_byte_count': 'int',
        'rx_byte_rate': 'int',
        'rx_discarded_msg_count': 'int',
        'rx_msg_count': 'int',
        'rx_msg_rate': 'int',
        'slow_subscriber': 'bool',
        'software_date': 'str',
        'software_version': 'str',
        'tls_cipher_description': 'str',
        'tls_downgraded_to_plain_text': 'bool',
        'tls_version': 'str',
        'topic_parse_error_rx_discarded_msg_count': 'int',
        'tx_byte_count': 'int',
        'tx_byte_rate': 'int',
        'tx_discarded_msg_count': 'int',
        'tx_msg_count': 'int',
        'tx_msg_rate': 'int',
        'uptime': 'int',
        'user': 'str',
        'virtual_router': 'str',
        'web_inactive_timeout': 'int',
        'web_max_payload': 'int',
        'web_parse_error_rx_discarded_msg_count': 'int',
        'web_remaining_timeout': 'int',
        'web_rx_byte_count': 'int',
        'web_rx_encoding': 'str',
        'web_rx_msg_count': 'int',
        'web_rx_protocol': 'str',
        'web_rx_request_count': 'int',
        'web_rx_response_count': 'int',
        'web_rx_tcp_state': 'str',
        'web_rx_tls_cipher_description': 'str',
        'web_rx_tls_version': 'str',
        'web_session_id': 'str',
        'web_tx_byte_count': 'int',
        'web_tx_encoding': 'str',
        'web_tx_msg_count': 'int',
        'web_tx_protocol': 'str',
        'web_tx_request_count': 'int',
        'web_tx_response_count': 'int',
        'web_tx_tcp_state': 'str',
        'web_tx_tls_cipher_description': 'str',
        'web_tx_tls_version': 'str'
    }

    attribute_map = {
        'acl_profile_name': 'aclProfileName',
        'already_bound_bind_failure_count': 'alreadyBoundBindFailureCount',
        'authorization_group_name': 'authorizationGroupName',
        'average_rx_byte_rate': 'averageRxByteRate',
        'average_rx_msg_rate': 'averageRxMsgRate',
        'average_tx_byte_rate': 'averageTxByteRate',
        'average_tx_msg_rate': 'averageTxMsgRate',
        'bind_request_count': 'bindRequestCount',
        'bind_success_count': 'bindSuccessCount',
        'client_address': 'clientAddress',
        'client_id': 'clientId',
        'client_name': 'clientName',
        'client_profile_name': 'clientProfileName',
        'client_username': 'clientUsername',
        'control_rx_byte_count': 'controlRxByteCount',
        'control_rx_msg_count': 'controlRxMsgCount',
        'control_tx_byte_count': 'controlTxByteCount',
        'control_tx_msg_count': 'controlTxMsgCount',
        'cut_through_denied_bind_failure_count': 'cutThroughDeniedBindFailureCount',
        'data_rx_byte_count': 'dataRxByteCount',
        'data_rx_msg_count': 'dataRxMsgCount',
        'data_tx_byte_count': 'dataTxByteCount',
        'data_tx_msg_count': 'dataTxMsgCount',
        'description': 'description',
        'disabled_bind_failure_count': 'disabledBindFailureCount',
        'dto_local_priority': 'dtoLocalPriority',
        'dto_network_priority': 'dtoNetworkPriority',
        'eliding': 'eliding',
        'eliding_topic_count': 'elidingTopicCount',
        'eliding_topic_peak_count': 'elidingTopicPeakCount',
        'guaranteed_denied_bind_failure_count': 'guaranteedDeniedBindFailureCount',
        'invalid_selector_bind_failure_count': 'invalidSelectorBindFailureCount',
        'large_msg_event_raised': 'largeMsgEventRaised',
        'login_rx_msg_count': 'loginRxMsgCount',
        'login_tx_msg_count': 'loginTxMsgCount',
        'max_bind_count_exceeded_bind_failure_count': 'maxBindCountExceededBindFailureCount',
        'max_eliding_topic_count_event_raised': 'maxElidingTopicCountEventRaised',
        'mqtt_connack_error_tx_count': 'mqttConnackErrorTxCount',
        'mqtt_connack_tx_count': 'mqttConnackTxCount',
        'mqtt_connect_rx_count': 'mqttConnectRxCount',
        'mqtt_disconnect_rx_count': 'mqttDisconnectRxCount',
        'mqtt_pingreq_rx_count': 'mqttPingreqRxCount',
        'mqtt_pingresp_tx_count': 'mqttPingrespTxCount',
        'mqtt_puback_rx_count': 'mqttPubackRxCount',
        'mqtt_puback_tx_count': 'mqttPubackTxCount',
        'mqtt_pubcomp_tx_count': 'mqttPubcompTxCount',
        'mqtt_publish_qos0_rx_count': 'mqttPublishQos0RxCount',
        'mqtt_publish_qos0_tx_count': 'mqttPublishQos0TxCount',
        'mqtt_publish_qos1_rx_count': 'mqttPublishQos1RxCount',
        'mqtt_publish_qos1_tx_count': 'mqttPublishQos1TxCount',
        'mqtt_publish_qos2_rx_count': 'mqttPublishQos2RxCount',
        'mqtt_pubrec_tx_count': 'mqttPubrecTxCount',
        'mqtt_pubrel_rx_count': 'mqttPubrelRxCount',
        'mqtt_suback_error_tx_count': 'mqttSubackErrorTxCount',
        'mqtt_suback_tx_count': 'mqttSubackTxCount',
        'mqtt_subscribe_rx_count': 'mqttSubscribeRxCount',
        'mqtt_unsuback_tx_count': 'mqttUnsubackTxCount',
        'mqtt_unsubscribe_rx_count': 'mqttUnsubscribeRxCount',
        'msg_spool_congestion_rx_discarded_msg_count': 'msgSpoolCongestionRxDiscardedMsgCount',
        'msg_spool_rx_discarded_msg_count': 'msgSpoolRxDiscardedMsgCount',
        'msg_vpn_name': 'msgVpnName',
        'no_local_delivery': 'noLocalDelivery',
        'no_subscription_match_rx_discarded_msg_count': 'noSubscriptionMatchRxDiscardedMsgCount',
        'original_client_username': 'originalClientUsername',
        'other_bind_failure_count': 'otherBindFailureCount',
        'platform': 'platform',
        'publish_topic_acl_rx_discarded_msg_count': 'publishTopicAclRxDiscardedMsgCount',
        'rest_http_request_rx_byte_count': 'restHttpRequestRxByteCount',
        'rest_http_request_rx_msg_count': 'restHttpRequestRxMsgCount',
        'rest_http_request_tx_byte_count': 'restHttpRequestTxByteCount',
        'rest_http_request_tx_msg_count': 'restHttpRequestTxMsgCount',
        'rest_http_response_error_rx_msg_count': 'restHttpResponseErrorRxMsgCount',
        'rest_http_response_error_tx_msg_count': 'restHttpResponseErrorTxMsgCount',
        'rest_http_response_rx_byte_count': 'restHttpResponseRxByteCount',
        'rest_http_response_rx_msg_count': 'restHttpResponseRxMsgCount',
        'rest_http_response_success_rx_msg_count': 'restHttpResponseSuccessRxMsgCount',
        'rest_http_response_success_tx_msg_count': 'restHttpResponseSuccessTxMsgCount',
        'rest_http_response_timeout_rx_msg_count': 'restHttpResponseTimeoutRxMsgCount',
        'rest_http_response_timeout_tx_msg_count': 'restHttpResponseTimeoutTxMsgCount',
        'rest_http_response_tx_byte_count': 'restHttpResponseTxByteCount',
        'rest_http_response_tx_msg_count': 'restHttpResponseTxMsgCount',
        'rx_byte_count': 'rxByteCount',
        'rx_byte_rate': 'rxByteRate',
        'rx_discarded_msg_count': 'rxDiscardedMsgCount',
        'rx_msg_count': 'rxMsgCount',
        'rx_msg_rate': 'rxMsgRate',
        'slow_subscriber': 'slowSubscriber',
        'software_date': 'softwareDate',
        'software_version': 'softwareVersion',
        'tls_cipher_description': 'tlsCipherDescription',
        'tls_downgraded_to_plain_text': 'tlsDowngradedToPlainText',
        'tls_version': 'tlsVersion',
        'topic_parse_error_rx_discarded_msg_count': 'topicParseErrorRxDiscardedMsgCount',
        'tx_byte_count': 'txByteCount',
        'tx_byte_rate': 'txByteRate',
        'tx_discarded_msg_count': 'txDiscardedMsgCount',
        'tx_msg_count': 'txMsgCount',
        'tx_msg_rate': 'txMsgRate',
        'uptime': 'uptime',
        'user': 'user',
        'virtual_router': 'virtualRouter',
        'web_inactive_timeout': 'webInactiveTimeout',
        'web_max_payload': 'webMaxPayload',
        'web_parse_error_rx_discarded_msg_count': 'webParseErrorRxDiscardedMsgCount',
        'web_remaining_timeout': 'webRemainingTimeout',
        'web_rx_byte_count': 'webRxByteCount',
        'web_rx_encoding': 'webRxEncoding',
        'web_rx_msg_count': 'webRxMsgCount',
        'web_rx_protocol': 'webRxProtocol',
        'web_rx_request_count': 'webRxRequestCount',
        'web_rx_response_count': 'webRxResponseCount',
        'web_rx_tcp_state': 'webRxTcpState',
        'web_rx_tls_cipher_description': 'webRxTlsCipherDescription',
        'web_rx_tls_version': 'webRxTlsVersion',
        'web_session_id': 'webSessionId',
        'web_tx_byte_count': 'webTxByteCount',
        'web_tx_encoding': 'webTxEncoding',
        'web_tx_msg_count': 'webTxMsgCount',
        'web_tx_protocol': 'webTxProtocol',
        'web_tx_request_count': 'webTxRequestCount',
        'web_tx_response_count': 'webTxResponseCount',
        'web_tx_tcp_state': 'webTxTcpState',
        'web_tx_tls_cipher_description': 'webTxTlsCipherDescription',
        'web_tx_tls_version': 'webTxTlsVersion'
    }

    def __init__(self, acl_profile_name=None, already_bound_bind_failure_count=None, authorization_group_name=None, average_rx_byte_rate=None, average_rx_msg_rate=None, average_tx_byte_rate=None, average_tx_msg_rate=None, bind_request_count=None, bind_success_count=None, client_address=None, client_id=None, client_name=None, client_profile_name=None, client_username=None, control_rx_byte_count=None, control_rx_msg_count=None, control_tx_byte_count=None, control_tx_msg_count=None, cut_through_denied_bind_failure_count=None, data_rx_byte_count=None, data_rx_msg_count=None, data_tx_byte_count=None, data_tx_msg_count=None, description=None, disabled_bind_failure_count=None, dto_local_priority=None, dto_network_priority=None, eliding=None, eliding_topic_count=None, eliding_topic_peak_count=None, guaranteed_denied_bind_failure_count=None, invalid_selector_bind_failure_count=None, large_msg_event_raised=None, login_rx_msg_count=None, login_tx_msg_count=None, max_bind_count_exceeded_bind_failure_count=None, max_eliding_topic_count_event_raised=None, mqtt_connack_error_tx_count=None, mqtt_connack_tx_count=None, mqtt_connect_rx_count=None, mqtt_disconnect_rx_count=None, mqtt_pingreq_rx_count=None, mqtt_pingresp_tx_count=None, mqtt_puback_rx_count=None, mqtt_puback_tx_count=None, mqtt_pubcomp_tx_count=None, mqtt_publish_qos0_rx_count=None, mqtt_publish_qos0_tx_count=None, mqtt_publish_qos1_rx_count=None, mqtt_publish_qos1_tx_count=None, mqtt_publish_qos2_rx_count=None, mqtt_pubrec_tx_count=None, mqtt_pubrel_rx_count=None, mqtt_suback_error_tx_count=None, mqtt_suback_tx_count=None, mqtt_subscribe_rx_count=None, mqtt_unsuback_tx_count=None, mqtt_unsubscribe_rx_count=None, msg_spool_congestion_rx_discarded_msg_count=None, msg_spool_rx_discarded_msg_count=None, msg_vpn_name=None, no_local_delivery=None, no_subscription_match_rx_discarded_msg_count=None, original_client_username=None, other_bind_failure_count=None, platform=None, publish_topic_acl_rx_discarded_msg_count=None, rest_http_request_rx_byte_count=None, rest_http_request_rx_msg_count=None, rest_http_request_tx_byte_count=None, rest_http_request_tx_msg_count=None, rest_http_response_error_rx_msg_count=None, rest_http_response_error_tx_msg_count=None, rest_http_response_rx_byte_count=None, rest_http_response_rx_msg_count=None, rest_http_response_success_rx_msg_count=None, rest_http_response_success_tx_msg_count=None, rest_http_response_timeout_rx_msg_count=None, rest_http_response_timeout_tx_msg_count=None, rest_http_response_tx_byte_count=None, rest_http_response_tx_msg_count=None, rx_byte_count=None, rx_byte_rate=None, rx_discarded_msg_count=None, rx_msg_count=None, rx_msg_rate=None, slow_subscriber=None, software_date=None, software_version=None, tls_cipher_description=None, tls_downgraded_to_plain_text=None, tls_version=None, topic_parse_error_rx_discarded_msg_count=None, tx_byte_count=None, tx_byte_rate=None, tx_discarded_msg_count=None, tx_msg_count=None, tx_msg_rate=None, uptime=None, user=None, virtual_router=None, web_inactive_timeout=None, web_max_payload=None, web_parse_error_rx_discarded_msg_count=None, web_remaining_timeout=None, web_rx_byte_count=None, web_rx_encoding=None, web_rx_msg_count=None, web_rx_protocol=None, web_rx_request_count=None, web_rx_response_count=None, web_rx_tcp_state=None, web_rx_tls_cipher_description=None, web_rx_tls_version=None, web_session_id=None, web_tx_byte_count=None, web_tx_encoding=None, web_tx_msg_count=None, web_tx_protocol=None, web_tx_request_count=None, web_tx_response_count=None, web_tx_tcp_state=None, web_tx_tls_cipher_description=None, web_tx_tls_version=None):  # noqa: E501
        """MsgVpnClient - a model defined in Swagger"""  # noqa: E501

        self._acl_profile_name = None
        self._already_bound_bind_failure_count = None
        self._authorization_group_name = None
        self._average_rx_byte_rate = None
        self._average_rx_msg_rate = None
        self._average_tx_byte_rate = None
        self._average_tx_msg_rate = None
        self._bind_request_count = None
        self._bind_success_count = None
        self._client_address = None
        self._client_id = None
        self._client_name = None
        self._client_profile_name = None
        self._client_username = None
        self._control_rx_byte_count = None
        self._control_rx_msg_count = None
        self._control_tx_byte_count = None
        self._control_tx_msg_count = None
        self._cut_through_denied_bind_failure_count = None
        self._data_rx_byte_count = None
        self._data_rx_msg_count = None
        self._data_tx_byte_count = None
        self._data_tx_msg_count = None
        self._description = None
        self._disabled_bind_failure_count = None
        self._dto_local_priority = None
        self._dto_network_priority = None
        self._eliding = None
        self._eliding_topic_count = None
        self._eliding_topic_peak_count = None
        self._guaranteed_denied_bind_failure_count = None
        self._invalid_selector_bind_failure_count = None
        self._large_msg_event_raised = None
        self._login_rx_msg_count = None
        self._login_tx_msg_count = None
        self._max_bind_count_exceeded_bind_failure_count = None
        self._max_eliding_topic_count_event_raised = None
        self._mqtt_connack_error_tx_count = None
        self._mqtt_connack_tx_count = None
        self._mqtt_connect_rx_count = None
        self._mqtt_disconnect_rx_count = None
        self._mqtt_pingreq_rx_count = None
        self._mqtt_pingresp_tx_count = None
        self._mqtt_puback_rx_count = None
        self._mqtt_puback_tx_count = None
        self._mqtt_pubcomp_tx_count = None
        self._mqtt_publish_qos0_rx_count = None
        self._mqtt_publish_qos0_tx_count = None
        self._mqtt_publish_qos1_rx_count = None
        self._mqtt_publish_qos1_tx_count = None
        self._mqtt_publish_qos2_rx_count = None
        self._mqtt_pubrec_tx_count = None
        self._mqtt_pubrel_rx_count = None
        self._mqtt_suback_error_tx_count = None
        self._mqtt_suback_tx_count = None
        self._mqtt_subscribe_rx_count = None
        self._mqtt_unsuback_tx_count = None
        self._mqtt_unsubscribe_rx_count = None
        self._msg_spool_congestion_rx_discarded_msg_count = None
        self._msg_spool_rx_discarded_msg_count = None
        self._msg_vpn_name = None
        self._no_local_delivery = None
        self._no_subscription_match_rx_discarded_msg_count = None
        self._original_client_username = None
        self._other_bind_failure_count = None
        self._platform = None
        self._publish_topic_acl_rx_discarded_msg_count = None
        self._rest_http_request_rx_byte_count = None
        self._rest_http_request_rx_msg_count = None
        self._rest_http_request_tx_byte_count = None
        self._rest_http_request_tx_msg_count = None
        self._rest_http_response_error_rx_msg_count = None
        self._rest_http_response_error_tx_msg_count = None
        self._rest_http_response_rx_byte_count = None
        self._rest_http_response_rx_msg_count = None
        self._rest_http_response_success_rx_msg_count = None
        self._rest_http_response_success_tx_msg_count = None
        self._rest_http_response_timeout_rx_msg_count = None
        self._rest_http_response_timeout_tx_msg_count = None
        self._rest_http_response_tx_byte_count = None
        self._rest_http_response_tx_msg_count = None
        self._rx_byte_count = None
        self._rx_byte_rate = None
        self._rx_discarded_msg_count = None
        self._rx_msg_count = None
        self._rx_msg_rate = None
        self._slow_subscriber = None
        self._software_date = None
        self._software_version = None
        self._tls_cipher_description = None
        self._tls_downgraded_to_plain_text = None
        self._tls_version = None
        self._topic_parse_error_rx_discarded_msg_count = None
        self._tx_byte_count = None
        self._tx_byte_rate = None
        self._tx_discarded_msg_count = None
        self._tx_msg_count = None
        self._tx_msg_rate = None
        self._uptime = None
        self._user = None
        self._virtual_router = None
        self._web_inactive_timeout = None
        self._web_max_payload = None
        self._web_parse_error_rx_discarded_msg_count = None
        self._web_remaining_timeout = None
        self._web_rx_byte_count = None
        self._web_rx_encoding = None
        self._web_rx_msg_count = None
        self._web_rx_protocol = None
        self._web_rx_request_count = None
        self._web_rx_response_count = None
        self._web_rx_tcp_state = None
        self._web_rx_tls_cipher_description = None
        self._web_rx_tls_version = None
        self._web_session_id = None
        self._web_tx_byte_count = None
        self._web_tx_encoding = None
        self._web_tx_msg_count = None
        self._web_tx_protocol = None
        self._web_tx_request_count = None
        self._web_tx_response_count = None
        self._web_tx_tcp_state = None
        self._web_tx_tls_cipher_description = None
        self._web_tx_tls_version = None
        self.discriminator = None

        if acl_profile_name is not None:
            self.acl_profile_name = acl_profile_name
        if already_bound_bind_failure_count is not None:
            self.already_bound_bind_failure_count = already_bound_bind_failure_count
        if authorization_group_name is not None:
            self.authorization_group_name = authorization_group_name
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
        if client_address is not None:
            self.client_address = client_address
        if client_id is not None:
            self.client_id = client_id
        if client_name is not None:
            self.client_name = client_name
        if client_profile_name is not None:
            self.client_profile_name = client_profile_name
        if client_username is not None:
            self.client_username = client_username
        if control_rx_byte_count is not None:
            self.control_rx_byte_count = control_rx_byte_count
        if control_rx_msg_count is not None:
            self.control_rx_msg_count = control_rx_msg_count
        if control_tx_byte_count is not None:
            self.control_tx_byte_count = control_tx_byte_count
        if control_tx_msg_count is not None:
            self.control_tx_msg_count = control_tx_msg_count
        if cut_through_denied_bind_failure_count is not None:
            self.cut_through_denied_bind_failure_count = cut_through_denied_bind_failure_count
        if data_rx_byte_count is not None:
            self.data_rx_byte_count = data_rx_byte_count
        if data_rx_msg_count is not None:
            self.data_rx_msg_count = data_rx_msg_count
        if data_tx_byte_count is not None:
            self.data_tx_byte_count = data_tx_byte_count
        if data_tx_msg_count is not None:
            self.data_tx_msg_count = data_tx_msg_count
        if description is not None:
            self.description = description
        if disabled_bind_failure_count is not None:
            self.disabled_bind_failure_count = disabled_bind_failure_count
        if dto_local_priority is not None:
            self.dto_local_priority = dto_local_priority
        if dto_network_priority is not None:
            self.dto_network_priority = dto_network_priority
        if eliding is not None:
            self.eliding = eliding
        if eliding_topic_count is not None:
            self.eliding_topic_count = eliding_topic_count
        if eliding_topic_peak_count is not None:
            self.eliding_topic_peak_count = eliding_topic_peak_count
        if guaranteed_denied_bind_failure_count is not None:
            self.guaranteed_denied_bind_failure_count = guaranteed_denied_bind_failure_count
        if invalid_selector_bind_failure_count is not None:
            self.invalid_selector_bind_failure_count = invalid_selector_bind_failure_count
        if large_msg_event_raised is not None:
            self.large_msg_event_raised = large_msg_event_raised
        if login_rx_msg_count is not None:
            self.login_rx_msg_count = login_rx_msg_count
        if login_tx_msg_count is not None:
            self.login_tx_msg_count = login_tx_msg_count
        if max_bind_count_exceeded_bind_failure_count is not None:
            self.max_bind_count_exceeded_bind_failure_count = max_bind_count_exceeded_bind_failure_count
        if max_eliding_topic_count_event_raised is not None:
            self.max_eliding_topic_count_event_raised = max_eliding_topic_count_event_raised
        if mqtt_connack_error_tx_count is not None:
            self.mqtt_connack_error_tx_count = mqtt_connack_error_tx_count
        if mqtt_connack_tx_count is not None:
            self.mqtt_connack_tx_count = mqtt_connack_tx_count
        if mqtt_connect_rx_count is not None:
            self.mqtt_connect_rx_count = mqtt_connect_rx_count
        if mqtt_disconnect_rx_count is not None:
            self.mqtt_disconnect_rx_count = mqtt_disconnect_rx_count
        if mqtt_pingreq_rx_count is not None:
            self.mqtt_pingreq_rx_count = mqtt_pingreq_rx_count
        if mqtt_pingresp_tx_count is not None:
            self.mqtt_pingresp_tx_count = mqtt_pingresp_tx_count
        if mqtt_puback_rx_count is not None:
            self.mqtt_puback_rx_count = mqtt_puback_rx_count
        if mqtt_puback_tx_count is not None:
            self.mqtt_puback_tx_count = mqtt_puback_tx_count
        if mqtt_pubcomp_tx_count is not None:
            self.mqtt_pubcomp_tx_count = mqtt_pubcomp_tx_count
        if mqtt_publish_qos0_rx_count is not None:
            self.mqtt_publish_qos0_rx_count = mqtt_publish_qos0_rx_count
        if mqtt_publish_qos0_tx_count is not None:
            self.mqtt_publish_qos0_tx_count = mqtt_publish_qos0_tx_count
        if mqtt_publish_qos1_rx_count is not None:
            self.mqtt_publish_qos1_rx_count = mqtt_publish_qos1_rx_count
        if mqtt_publish_qos1_tx_count is not None:
            self.mqtt_publish_qos1_tx_count = mqtt_publish_qos1_tx_count
        if mqtt_publish_qos2_rx_count is not None:
            self.mqtt_publish_qos2_rx_count = mqtt_publish_qos2_rx_count
        if mqtt_pubrec_tx_count is not None:
            self.mqtt_pubrec_tx_count = mqtt_pubrec_tx_count
        if mqtt_pubrel_rx_count is not None:
            self.mqtt_pubrel_rx_count = mqtt_pubrel_rx_count
        if mqtt_suback_error_tx_count is not None:
            self.mqtt_suback_error_tx_count = mqtt_suback_error_tx_count
        if mqtt_suback_tx_count is not None:
            self.mqtt_suback_tx_count = mqtt_suback_tx_count
        if mqtt_subscribe_rx_count is not None:
            self.mqtt_subscribe_rx_count = mqtt_subscribe_rx_count
        if mqtt_unsuback_tx_count is not None:
            self.mqtt_unsuback_tx_count = mqtt_unsuback_tx_count
        if mqtt_unsubscribe_rx_count is not None:
            self.mqtt_unsubscribe_rx_count = mqtt_unsubscribe_rx_count
        if msg_spool_congestion_rx_discarded_msg_count is not None:
            self.msg_spool_congestion_rx_discarded_msg_count = msg_spool_congestion_rx_discarded_msg_count
        if msg_spool_rx_discarded_msg_count is not None:
            self.msg_spool_rx_discarded_msg_count = msg_spool_rx_discarded_msg_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if no_local_delivery is not None:
            self.no_local_delivery = no_local_delivery
        if no_subscription_match_rx_discarded_msg_count is not None:
            self.no_subscription_match_rx_discarded_msg_count = no_subscription_match_rx_discarded_msg_count
        if original_client_username is not None:
            self.original_client_username = original_client_username
        if other_bind_failure_count is not None:
            self.other_bind_failure_count = other_bind_failure_count
        if platform is not None:
            self.platform = platform
        if publish_topic_acl_rx_discarded_msg_count is not None:
            self.publish_topic_acl_rx_discarded_msg_count = publish_topic_acl_rx_discarded_msg_count
        if rest_http_request_rx_byte_count is not None:
            self.rest_http_request_rx_byte_count = rest_http_request_rx_byte_count
        if rest_http_request_rx_msg_count is not None:
            self.rest_http_request_rx_msg_count = rest_http_request_rx_msg_count
        if rest_http_request_tx_byte_count is not None:
            self.rest_http_request_tx_byte_count = rest_http_request_tx_byte_count
        if rest_http_request_tx_msg_count is not None:
            self.rest_http_request_tx_msg_count = rest_http_request_tx_msg_count
        if rest_http_response_error_rx_msg_count is not None:
            self.rest_http_response_error_rx_msg_count = rest_http_response_error_rx_msg_count
        if rest_http_response_error_tx_msg_count is not None:
            self.rest_http_response_error_tx_msg_count = rest_http_response_error_tx_msg_count
        if rest_http_response_rx_byte_count is not None:
            self.rest_http_response_rx_byte_count = rest_http_response_rx_byte_count
        if rest_http_response_rx_msg_count is not None:
            self.rest_http_response_rx_msg_count = rest_http_response_rx_msg_count
        if rest_http_response_success_rx_msg_count is not None:
            self.rest_http_response_success_rx_msg_count = rest_http_response_success_rx_msg_count
        if rest_http_response_success_tx_msg_count is not None:
            self.rest_http_response_success_tx_msg_count = rest_http_response_success_tx_msg_count
        if rest_http_response_timeout_rx_msg_count is not None:
            self.rest_http_response_timeout_rx_msg_count = rest_http_response_timeout_rx_msg_count
        if rest_http_response_timeout_tx_msg_count is not None:
            self.rest_http_response_timeout_tx_msg_count = rest_http_response_timeout_tx_msg_count
        if rest_http_response_tx_byte_count is not None:
            self.rest_http_response_tx_byte_count = rest_http_response_tx_byte_count
        if rest_http_response_tx_msg_count is not None:
            self.rest_http_response_tx_msg_count = rest_http_response_tx_msg_count
        if rx_byte_count is not None:
            self.rx_byte_count = rx_byte_count
        if rx_byte_rate is not None:
            self.rx_byte_rate = rx_byte_rate
        if rx_discarded_msg_count is not None:
            self.rx_discarded_msg_count = rx_discarded_msg_count
        if rx_msg_count is not None:
            self.rx_msg_count = rx_msg_count
        if rx_msg_rate is not None:
            self.rx_msg_rate = rx_msg_rate
        if slow_subscriber is not None:
            self.slow_subscriber = slow_subscriber
        if software_date is not None:
            self.software_date = software_date
        if software_version is not None:
            self.software_version = software_version
        if tls_cipher_description is not None:
            self.tls_cipher_description = tls_cipher_description
        if tls_downgraded_to_plain_text is not None:
            self.tls_downgraded_to_plain_text = tls_downgraded_to_plain_text
        if tls_version is not None:
            self.tls_version = tls_version
        if topic_parse_error_rx_discarded_msg_count is not None:
            self.topic_parse_error_rx_discarded_msg_count = topic_parse_error_rx_discarded_msg_count
        if tx_byte_count is not None:
            self.tx_byte_count = tx_byte_count
        if tx_byte_rate is not None:
            self.tx_byte_rate = tx_byte_rate
        if tx_discarded_msg_count is not None:
            self.tx_discarded_msg_count = tx_discarded_msg_count
        if tx_msg_count is not None:
            self.tx_msg_count = tx_msg_count
        if tx_msg_rate is not None:
            self.tx_msg_rate = tx_msg_rate
        if uptime is not None:
            self.uptime = uptime
        if user is not None:
            self.user = user
        if virtual_router is not None:
            self.virtual_router = virtual_router
        if web_inactive_timeout is not None:
            self.web_inactive_timeout = web_inactive_timeout
        if web_max_payload is not None:
            self.web_max_payload = web_max_payload
        if web_parse_error_rx_discarded_msg_count is not None:
            self.web_parse_error_rx_discarded_msg_count = web_parse_error_rx_discarded_msg_count
        if web_remaining_timeout is not None:
            self.web_remaining_timeout = web_remaining_timeout
        if web_rx_byte_count is not None:
            self.web_rx_byte_count = web_rx_byte_count
        if web_rx_encoding is not None:
            self.web_rx_encoding = web_rx_encoding
        if web_rx_msg_count is not None:
            self.web_rx_msg_count = web_rx_msg_count
        if web_rx_protocol is not None:
            self.web_rx_protocol = web_rx_protocol
        if web_rx_request_count is not None:
            self.web_rx_request_count = web_rx_request_count
        if web_rx_response_count is not None:
            self.web_rx_response_count = web_rx_response_count
        if web_rx_tcp_state is not None:
            self.web_rx_tcp_state = web_rx_tcp_state
        if web_rx_tls_cipher_description is not None:
            self.web_rx_tls_cipher_description = web_rx_tls_cipher_description
        if web_rx_tls_version is not None:
            self.web_rx_tls_version = web_rx_tls_version
        if web_session_id is not None:
            self.web_session_id = web_session_id
        if web_tx_byte_count is not None:
            self.web_tx_byte_count = web_tx_byte_count
        if web_tx_encoding is not None:
            self.web_tx_encoding = web_tx_encoding
        if web_tx_msg_count is not None:
            self.web_tx_msg_count = web_tx_msg_count
        if web_tx_protocol is not None:
            self.web_tx_protocol = web_tx_protocol
        if web_tx_request_count is not None:
            self.web_tx_request_count = web_tx_request_count
        if web_tx_response_count is not None:
            self.web_tx_response_count = web_tx_response_count
        if web_tx_tcp_state is not None:
            self.web_tx_tcp_state = web_tx_tcp_state
        if web_tx_tls_cipher_description is not None:
            self.web_tx_tls_cipher_description = web_tx_tls_cipher_description
        if web_tx_tls_version is not None:
            self.web_tx_tls_version = web_tx_tls_version

    @property
    def acl_profile_name(self):
        """Gets the acl_profile_name of this MsgVpnClient.  # noqa: E501

        The name of the access control list (ACL) profile of the Client.  # noqa: E501

        :return: The acl_profile_name of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._acl_profile_name

    @acl_profile_name.setter
    def acl_profile_name(self, acl_profile_name):
        """Sets the acl_profile_name of this MsgVpnClient.

        The name of the access control list (ACL) profile of the Client.  # noqa: E501

        :param acl_profile_name: The acl_profile_name of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._acl_profile_name = acl_profile_name

    @property
    def already_bound_bind_failure_count(self):
        """Gets the already_bound_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to endpoint being already bound.  # noqa: E501

        :return: The already_bound_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._already_bound_bind_failure_count

    @already_bound_bind_failure_count.setter
    def already_bound_bind_failure_count(self, already_bound_bind_failure_count):
        """Sets the already_bound_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to endpoint being already bound.  # noqa: E501

        :param already_bound_bind_failure_count: The already_bound_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._already_bound_bind_failure_count = already_bound_bind_failure_count

    @property
    def authorization_group_name(self):
        """Gets the authorization_group_name of this MsgVpnClient.  # noqa: E501

        The name of the authorization group of the Client.  # noqa: E501

        :return: The authorization_group_name of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._authorization_group_name

    @authorization_group_name.setter
    def authorization_group_name(self, authorization_group_name):
        """Sets the authorization_group_name of this MsgVpnClient.

        The name of the authorization group of the Client.  # noqa: E501

        :param authorization_group_name: The authorization_group_name of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._authorization_group_name = authorization_group_name

    @property
    def average_rx_byte_rate(self):
        """Gets the average_rx_byte_rate of this MsgVpnClient.  # noqa: E501

        The one minute average of the message rate received from the Client, in bytes per second (B/sec).  # noqa: E501

        :return: The average_rx_byte_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_byte_rate

    @average_rx_byte_rate.setter
    def average_rx_byte_rate(self, average_rx_byte_rate):
        """Sets the average_rx_byte_rate of this MsgVpnClient.

        The one minute average of the message rate received from the Client, in bytes per second (B/sec).  # noqa: E501

        :param average_rx_byte_rate: The average_rx_byte_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._average_rx_byte_rate = average_rx_byte_rate

    @property
    def average_rx_msg_rate(self):
        """Gets the average_rx_msg_rate of this MsgVpnClient.  # noqa: E501

        The one minute average of the message rate received from the Client, in messages per second (msg/sec).  # noqa: E501

        :return: The average_rx_msg_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_msg_rate

    @average_rx_msg_rate.setter
    def average_rx_msg_rate(self, average_rx_msg_rate):
        """Sets the average_rx_msg_rate of this MsgVpnClient.

        The one minute average of the message rate received from the Client, in messages per second (msg/sec).  # noqa: E501

        :param average_rx_msg_rate: The average_rx_msg_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._average_rx_msg_rate = average_rx_msg_rate

    @property
    def average_tx_byte_rate(self):
        """Gets the average_tx_byte_rate of this MsgVpnClient.  # noqa: E501

        The one minute average of the message rate transmitted to the Client, in bytes per second (B/sec).  # noqa: E501

        :return: The average_tx_byte_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_byte_rate

    @average_tx_byte_rate.setter
    def average_tx_byte_rate(self, average_tx_byte_rate):
        """Sets the average_tx_byte_rate of this MsgVpnClient.

        The one minute average of the message rate transmitted to the Client, in bytes per second (B/sec).  # noqa: E501

        :param average_tx_byte_rate: The average_tx_byte_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._average_tx_byte_rate = average_tx_byte_rate

    @property
    def average_tx_msg_rate(self):
        """Gets the average_tx_msg_rate of this MsgVpnClient.  # noqa: E501

        The one minute average of the message rate transmitted to the Client, in messages per second (msg/sec).  # noqa: E501

        :return: The average_tx_msg_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_msg_rate

    @average_tx_msg_rate.setter
    def average_tx_msg_rate(self, average_tx_msg_rate):
        """Sets the average_tx_msg_rate of this MsgVpnClient.

        The one minute average of the message rate transmitted to the Client, in messages per second (msg/sec).  # noqa: E501

        :param average_tx_msg_rate: The average_tx_msg_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._average_tx_msg_rate = average_tx_msg_rate

    @property
    def bind_request_count(self):
        """Gets the bind_request_count of this MsgVpnClient.  # noqa: E501

        The number of Client requests to bind to an endpoint.  # noqa: E501

        :return: The bind_request_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._bind_request_count

    @bind_request_count.setter
    def bind_request_count(self, bind_request_count):
        """Sets the bind_request_count of this MsgVpnClient.

        The number of Client requests to bind to an endpoint.  # noqa: E501

        :param bind_request_count: The bind_request_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._bind_request_count = bind_request_count

    @property
    def bind_success_count(self):
        """Gets the bind_success_count of this MsgVpnClient.  # noqa: E501

        The number of successful Client requests to bind to an endpoint.  # noqa: E501

        :return: The bind_success_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._bind_success_count

    @bind_success_count.setter
    def bind_success_count(self, bind_success_count):
        """Sets the bind_success_count of this MsgVpnClient.

        The number of successful Client requests to bind to an endpoint.  # noqa: E501

        :param bind_success_count: The bind_success_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._bind_success_count = bind_success_count

    @property
    def client_address(self):
        """Gets the client_address of this MsgVpnClient.  # noqa: E501

        The IP address and port of the Client.  # noqa: E501

        :return: The client_address of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._client_address

    @client_address.setter
    def client_address(self, client_address):
        """Sets the client_address of this MsgVpnClient.

        The IP address and port of the Client.  # noqa: E501

        :param client_address: The client_address of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._client_address = client_address

    @property
    def client_id(self):
        """Gets the client_id of this MsgVpnClient.  # noqa: E501

        The identifier (ID) of the Client.  # noqa: E501

        :return: The client_id of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this MsgVpnClient.

        The identifier (ID) of the Client.  # noqa: E501

        :param client_id: The client_id of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._client_id = client_id

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnClient.  # noqa: E501

        The name of the Client.  # noqa: E501

        :return: The client_name of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnClient.

        The name of the Client.  # noqa: E501

        :param client_name: The client_name of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def client_profile_name(self):
        """Gets the client_profile_name of this MsgVpnClient.  # noqa: E501

        The name of the client profile of the Client.  # noqa: E501

        :return: The client_profile_name of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._client_profile_name

    @client_profile_name.setter
    def client_profile_name(self, client_profile_name):
        """Sets the client_profile_name of this MsgVpnClient.

        The name of the client profile of the Client.  # noqa: E501

        :param client_profile_name: The client_profile_name of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._client_profile_name = client_profile_name

    @property
    def client_username(self):
        """Gets the client_username of this MsgVpnClient.  # noqa: E501

        The client username of the Client used for authorization.  # noqa: E501

        :return: The client_username of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._client_username

    @client_username.setter
    def client_username(self, client_username):
        """Sets the client_username of this MsgVpnClient.

        The client username of the Client used for authorization.  # noqa: E501

        :param client_username: The client_username of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._client_username = client_username

    @property
    def control_rx_byte_count(self):
        """Gets the control_rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of client control messages received from the Client, in bytes (B).  # noqa: E501

        :return: The control_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._control_rx_byte_count

    @control_rx_byte_count.setter
    def control_rx_byte_count(self, control_rx_byte_count):
        """Sets the control_rx_byte_count of this MsgVpnClient.

        The amount of client control messages received from the Client, in bytes (B).  # noqa: E501

        :param control_rx_byte_count: The control_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._control_rx_byte_count = control_rx_byte_count

    @property
    def control_rx_msg_count(self):
        """Gets the control_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of client control messages received from the Client.  # noqa: E501

        :return: The control_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._control_rx_msg_count

    @control_rx_msg_count.setter
    def control_rx_msg_count(self, control_rx_msg_count):
        """Sets the control_rx_msg_count of this MsgVpnClient.

        The number of client control messages received from the Client.  # noqa: E501

        :param control_rx_msg_count: The control_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._control_rx_msg_count = control_rx_msg_count

    @property
    def control_tx_byte_count(self):
        """Gets the control_tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of client control messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The control_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._control_tx_byte_count

    @control_tx_byte_count.setter
    def control_tx_byte_count(self, control_tx_byte_count):
        """Sets the control_tx_byte_count of this MsgVpnClient.

        The amount of client control messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param control_tx_byte_count: The control_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._control_tx_byte_count = control_tx_byte_count

    @property
    def control_tx_msg_count(self):
        """Gets the control_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of client control messages transmitted to the Client.  # noqa: E501

        :return: The control_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._control_tx_msg_count

    @control_tx_msg_count.setter
    def control_tx_msg_count(self, control_tx_msg_count):
        """Sets the control_tx_msg_count of this MsgVpnClient.

        The number of client control messages transmitted to the Client.  # noqa: E501

        :param control_tx_msg_count: The control_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._control_tx_msg_count = control_tx_msg_count

    @property
    def cut_through_denied_bind_failure_count(self):
        """Gets the cut_through_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to being denied cut-through forwarding.  # noqa: E501

        :return: The cut_through_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._cut_through_denied_bind_failure_count

    @cut_through_denied_bind_failure_count.setter
    def cut_through_denied_bind_failure_count(self, cut_through_denied_bind_failure_count):
        """Sets the cut_through_denied_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to being denied cut-through forwarding.  # noqa: E501

        :param cut_through_denied_bind_failure_count: The cut_through_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._cut_through_denied_bind_failure_count = cut_through_denied_bind_failure_count

    @property
    def data_rx_byte_count(self):
        """Gets the data_rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of client data messages received from the Client, in bytes (B).  # noqa: E501

        :return: The data_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_byte_count

    @data_rx_byte_count.setter
    def data_rx_byte_count(self, data_rx_byte_count):
        """Sets the data_rx_byte_count of this MsgVpnClient.

        The amount of client data messages received from the Client, in bytes (B).  # noqa: E501

        :param data_rx_byte_count: The data_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._data_rx_byte_count = data_rx_byte_count

    @property
    def data_rx_msg_count(self):
        """Gets the data_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of client data messages received from the Client.  # noqa: E501

        :return: The data_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_msg_count

    @data_rx_msg_count.setter
    def data_rx_msg_count(self, data_rx_msg_count):
        """Sets the data_rx_msg_count of this MsgVpnClient.

        The number of client data messages received from the Client.  # noqa: E501

        :param data_rx_msg_count: The data_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._data_rx_msg_count = data_rx_msg_count

    @property
    def data_tx_byte_count(self):
        """Gets the data_tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of client data messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The data_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_byte_count

    @data_tx_byte_count.setter
    def data_tx_byte_count(self, data_tx_byte_count):
        """Sets the data_tx_byte_count of this MsgVpnClient.

        The amount of client data messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param data_tx_byte_count: The data_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._data_tx_byte_count = data_tx_byte_count

    @property
    def data_tx_msg_count(self):
        """Gets the data_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of client data messages transmitted to the Client.  # noqa: E501

        :return: The data_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_msg_count

    @data_tx_msg_count.setter
    def data_tx_msg_count(self, data_tx_msg_count):
        """Sets the data_tx_msg_count of this MsgVpnClient.

        The number of client data messages transmitted to the Client.  # noqa: E501

        :param data_tx_msg_count: The data_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._data_tx_msg_count = data_tx_msg_count

    @property
    def description(self):
        """Gets the description of this MsgVpnClient.  # noqa: E501

        The description text of the Client.  # noqa: E501

        :return: The description of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this MsgVpnClient.

        The description text of the Client.  # noqa: E501

        :param description: The description of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def disabled_bind_failure_count(self):
        """Gets the disabled_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to endpoint being disabled.  # noqa: E501

        :return: The disabled_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._disabled_bind_failure_count

    @disabled_bind_failure_count.setter
    def disabled_bind_failure_count(self, disabled_bind_failure_count):
        """Sets the disabled_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to endpoint being disabled.  # noqa: E501

        :param disabled_bind_failure_count: The disabled_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._disabled_bind_failure_count = disabled_bind_failure_count

    @property
    def dto_local_priority(self):
        """Gets the dto_local_priority of this MsgVpnClient.  # noqa: E501

        The priority of the Client's subscriptions for receiving deliver-to-one (DTO) messages published on the local broker.  # noqa: E501

        :return: The dto_local_priority of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._dto_local_priority

    @dto_local_priority.setter
    def dto_local_priority(self, dto_local_priority):
        """Sets the dto_local_priority of this MsgVpnClient.

        The priority of the Client's subscriptions for receiving deliver-to-one (DTO) messages published on the local broker.  # noqa: E501

        :param dto_local_priority: The dto_local_priority of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._dto_local_priority = dto_local_priority

    @property
    def dto_network_priority(self):
        """Gets the dto_network_priority of this MsgVpnClient.  # noqa: E501

        The priority of the Client's subscriptions for receiving deliver-to-one (DTO) messages published on a remote broker.  # noqa: E501

        :return: The dto_network_priority of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._dto_network_priority

    @dto_network_priority.setter
    def dto_network_priority(self, dto_network_priority):
        """Sets the dto_network_priority of this MsgVpnClient.

        The priority of the Client's subscriptions for receiving deliver-to-one (DTO) messages published on a remote broker.  # noqa: E501

        :param dto_network_priority: The dto_network_priority of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._dto_network_priority = dto_network_priority

    @property
    def eliding(self):
        """Gets the eliding of this MsgVpnClient.  # noqa: E501

        Indicates whether message eliding is enabled for the Client.  # noqa: E501

        :return: The eliding of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._eliding

    @eliding.setter
    def eliding(self, eliding):
        """Sets the eliding of this MsgVpnClient.

        Indicates whether message eliding is enabled for the Client.  # noqa: E501

        :param eliding: The eliding of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._eliding = eliding

    @property
    def eliding_topic_count(self):
        """Gets the eliding_topic_count of this MsgVpnClient.  # noqa: E501

        The number of topics requiring message eliding for the Client.  # noqa: E501

        :return: The eliding_topic_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._eliding_topic_count

    @eliding_topic_count.setter
    def eliding_topic_count(self, eliding_topic_count):
        """Sets the eliding_topic_count of this MsgVpnClient.

        The number of topics requiring message eliding for the Client.  # noqa: E501

        :param eliding_topic_count: The eliding_topic_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._eliding_topic_count = eliding_topic_count

    @property
    def eliding_topic_peak_count(self):
        """Gets the eliding_topic_peak_count of this MsgVpnClient.  # noqa: E501

        The peak number of topics requiring message eliding for the Client.  # noqa: E501

        :return: The eliding_topic_peak_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._eliding_topic_peak_count

    @eliding_topic_peak_count.setter
    def eliding_topic_peak_count(self, eliding_topic_peak_count):
        """Sets the eliding_topic_peak_count of this MsgVpnClient.

        The peak number of topics requiring message eliding for the Client.  # noqa: E501

        :param eliding_topic_peak_count: The eliding_topic_peak_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._eliding_topic_peak_count = eliding_topic_peak_count

    @property
    def guaranteed_denied_bind_failure_count(self):
        """Gets the guaranteed_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to being denied guaranteed messaging.  # noqa: E501

        :return: The guaranteed_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_denied_bind_failure_count

    @guaranteed_denied_bind_failure_count.setter
    def guaranteed_denied_bind_failure_count(self, guaranteed_denied_bind_failure_count):
        """Sets the guaranteed_denied_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to being denied guaranteed messaging.  # noqa: E501

        :param guaranteed_denied_bind_failure_count: The guaranteed_denied_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._guaranteed_denied_bind_failure_count = guaranteed_denied_bind_failure_count

    @property
    def invalid_selector_bind_failure_count(self):
        """Gets the invalid_selector_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to an invalid selector.  # noqa: E501

        :return: The invalid_selector_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._invalid_selector_bind_failure_count

    @invalid_selector_bind_failure_count.setter
    def invalid_selector_bind_failure_count(self, invalid_selector_bind_failure_count):
        """Sets the invalid_selector_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to an invalid selector.  # noqa: E501

        :param invalid_selector_bind_failure_count: The invalid_selector_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._invalid_selector_bind_failure_count = invalid_selector_bind_failure_count

    @property
    def large_msg_event_raised(self):
        """Gets the large_msg_event_raised of this MsgVpnClient.  # noqa: E501

        Indicates whether the large-message event has been raised for the Client.  # noqa: E501

        :return: The large_msg_event_raised of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._large_msg_event_raised

    @large_msg_event_raised.setter
    def large_msg_event_raised(self, large_msg_event_raised):
        """Sets the large_msg_event_raised of this MsgVpnClient.

        Indicates whether the large-message event has been raised for the Client.  # noqa: E501

        :param large_msg_event_raised: The large_msg_event_raised of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._large_msg_event_raised = large_msg_event_raised

    @property
    def login_rx_msg_count(self):
        """Gets the login_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of login request messages received from the Client.  # noqa: E501

        :return: The login_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._login_rx_msg_count

    @login_rx_msg_count.setter
    def login_rx_msg_count(self, login_rx_msg_count):
        """Sets the login_rx_msg_count of this MsgVpnClient.

        The number of login request messages received from the Client.  # noqa: E501

        :param login_rx_msg_count: The login_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._login_rx_msg_count = login_rx_msg_count

    @property
    def login_tx_msg_count(self):
        """Gets the login_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of login response messages transmitted to the Client.  # noqa: E501

        :return: The login_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._login_tx_msg_count

    @login_tx_msg_count.setter
    def login_tx_msg_count(self, login_tx_msg_count):
        """Sets the login_tx_msg_count of this MsgVpnClient.

        The number of login response messages transmitted to the Client.  # noqa: E501

        :param login_tx_msg_count: The login_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._login_tx_msg_count = login_tx_msg_count

    @property
    def max_bind_count_exceeded_bind_failure_count(self):
        """Gets the max_bind_count_exceeded_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to the endpoint maximum bind count being exceeded.  # noqa: E501

        :return: The max_bind_count_exceeded_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._max_bind_count_exceeded_bind_failure_count

    @max_bind_count_exceeded_bind_failure_count.setter
    def max_bind_count_exceeded_bind_failure_count(self, max_bind_count_exceeded_bind_failure_count):
        """Sets the max_bind_count_exceeded_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to the endpoint maximum bind count being exceeded.  # noqa: E501

        :param max_bind_count_exceeded_bind_failure_count: The max_bind_count_exceeded_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._max_bind_count_exceeded_bind_failure_count = max_bind_count_exceeded_bind_failure_count

    @property
    def max_eliding_topic_count_event_raised(self):
        """Gets the max_eliding_topic_count_event_raised of this MsgVpnClient.  # noqa: E501

        Indicates whether the max-eliding-topic-count event has been raised for the Client.  # noqa: E501

        :return: The max_eliding_topic_count_event_raised of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._max_eliding_topic_count_event_raised

    @max_eliding_topic_count_event_raised.setter
    def max_eliding_topic_count_event_raised(self, max_eliding_topic_count_event_raised):
        """Sets the max_eliding_topic_count_event_raised of this MsgVpnClient.

        Indicates whether the max-eliding-topic-count event has been raised for the Client.  # noqa: E501

        :param max_eliding_topic_count_event_raised: The max_eliding_topic_count_event_raised of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._max_eliding_topic_count_event_raised = max_eliding_topic_count_event_raised

    @property
    def mqtt_connack_error_tx_count(self):
        """Gets the mqtt_connack_error_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT connect acknowledgment (CONNACK) refused response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_connack_error_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_connack_error_tx_count

    @mqtt_connack_error_tx_count.setter
    def mqtt_connack_error_tx_count(self, mqtt_connack_error_tx_count):
        """Sets the mqtt_connack_error_tx_count of this MsgVpnClient.

        The number of MQTT connect acknowledgment (CONNACK) refused response packets transmitted to the Client.  # noqa: E501

        :param mqtt_connack_error_tx_count: The mqtt_connack_error_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_connack_error_tx_count = mqtt_connack_error_tx_count

    @property
    def mqtt_connack_tx_count(self):
        """Gets the mqtt_connack_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT connect acknowledgment (CONNACK) accepted response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_connack_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_connack_tx_count

    @mqtt_connack_tx_count.setter
    def mqtt_connack_tx_count(self, mqtt_connack_tx_count):
        """Sets the mqtt_connack_tx_count of this MsgVpnClient.

        The number of MQTT connect acknowledgment (CONNACK) accepted response packets transmitted to the Client.  # noqa: E501

        :param mqtt_connack_tx_count: The mqtt_connack_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_connack_tx_count = mqtt_connack_tx_count

    @property
    def mqtt_connect_rx_count(self):
        """Gets the mqtt_connect_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT connect (CONNECT) request packets received from the Client.  # noqa: E501

        :return: The mqtt_connect_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_connect_rx_count

    @mqtt_connect_rx_count.setter
    def mqtt_connect_rx_count(self, mqtt_connect_rx_count):
        """Sets the mqtt_connect_rx_count of this MsgVpnClient.

        The number of MQTT connect (CONNECT) request packets received from the Client.  # noqa: E501

        :param mqtt_connect_rx_count: The mqtt_connect_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_connect_rx_count = mqtt_connect_rx_count

    @property
    def mqtt_disconnect_rx_count(self):
        """Gets the mqtt_disconnect_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT disconnect (DISCONNECT) request packets received from the Client.  # noqa: E501

        :return: The mqtt_disconnect_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_disconnect_rx_count

    @mqtt_disconnect_rx_count.setter
    def mqtt_disconnect_rx_count(self, mqtt_disconnect_rx_count):
        """Sets the mqtt_disconnect_rx_count of this MsgVpnClient.

        The number of MQTT disconnect (DISCONNECT) request packets received from the Client.  # noqa: E501

        :param mqtt_disconnect_rx_count: The mqtt_disconnect_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_disconnect_rx_count = mqtt_disconnect_rx_count

    @property
    def mqtt_pingreq_rx_count(self):
        """Gets the mqtt_pingreq_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT ping request (PINGREQ) packets received from the Client.  # noqa: E501

        :return: The mqtt_pingreq_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_pingreq_rx_count

    @mqtt_pingreq_rx_count.setter
    def mqtt_pingreq_rx_count(self, mqtt_pingreq_rx_count):
        """Sets the mqtt_pingreq_rx_count of this MsgVpnClient.

        The number of MQTT ping request (PINGREQ) packets received from the Client.  # noqa: E501

        :param mqtt_pingreq_rx_count: The mqtt_pingreq_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_pingreq_rx_count = mqtt_pingreq_rx_count

    @property
    def mqtt_pingresp_tx_count(self):
        """Gets the mqtt_pingresp_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT ping response (PINGRESP) packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_pingresp_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_pingresp_tx_count

    @mqtt_pingresp_tx_count.setter
    def mqtt_pingresp_tx_count(self, mqtt_pingresp_tx_count):
        """Sets the mqtt_pingresp_tx_count of this MsgVpnClient.

        The number of MQTT ping response (PINGRESP) packets transmitted to the Client.  # noqa: E501

        :param mqtt_pingresp_tx_count: The mqtt_pingresp_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_pingresp_tx_count = mqtt_pingresp_tx_count

    @property
    def mqtt_puback_rx_count(self):
        """Gets the mqtt_puback_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish acknowledgement (PUBACK) response packets received from the Client.  # noqa: E501

        :return: The mqtt_puback_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_puback_rx_count

    @mqtt_puback_rx_count.setter
    def mqtt_puback_rx_count(self, mqtt_puback_rx_count):
        """Sets the mqtt_puback_rx_count of this MsgVpnClient.

        The number of MQTT publish acknowledgement (PUBACK) response packets received from the Client.  # noqa: E501

        :param mqtt_puback_rx_count: The mqtt_puback_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_puback_rx_count = mqtt_puback_rx_count

    @property
    def mqtt_puback_tx_count(self):
        """Gets the mqtt_puback_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish acknowledgement (PUBACK) response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_puback_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_puback_tx_count

    @mqtt_puback_tx_count.setter
    def mqtt_puback_tx_count(self, mqtt_puback_tx_count):
        """Sets the mqtt_puback_tx_count of this MsgVpnClient.

        The number of MQTT publish acknowledgement (PUBACK) response packets transmitted to the Client.  # noqa: E501

        :param mqtt_puback_tx_count: The mqtt_puback_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_puback_tx_count = mqtt_puback_tx_count

    @property
    def mqtt_pubcomp_tx_count(self):
        """Gets the mqtt_pubcomp_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish complete (PUBCOMP) packets transmitted to the Client in response to a PUBREL packet. These packets are the fourth and final packet of a QoS 2 protocol exchange.  # noqa: E501

        :return: The mqtt_pubcomp_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_pubcomp_tx_count

    @mqtt_pubcomp_tx_count.setter
    def mqtt_pubcomp_tx_count(self, mqtt_pubcomp_tx_count):
        """Sets the mqtt_pubcomp_tx_count of this MsgVpnClient.

        The number of MQTT publish complete (PUBCOMP) packets transmitted to the Client in response to a PUBREL packet. These packets are the fourth and final packet of a QoS 2 protocol exchange.  # noqa: E501

        :param mqtt_pubcomp_tx_count: The mqtt_pubcomp_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_pubcomp_tx_count = mqtt_pubcomp_tx_count

    @property
    def mqtt_publish_qos0_rx_count(self):
        """Gets the mqtt_publish_qos0_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 0 message delivery.  # noqa: E501

        :return: The mqtt_publish_qos0_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_publish_qos0_rx_count

    @mqtt_publish_qos0_rx_count.setter
    def mqtt_publish_qos0_rx_count(self, mqtt_publish_qos0_rx_count):
        """Sets the mqtt_publish_qos0_rx_count of this MsgVpnClient.

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 0 message delivery.  # noqa: E501

        :param mqtt_publish_qos0_rx_count: The mqtt_publish_qos0_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_publish_qos0_rx_count = mqtt_publish_qos0_rx_count

    @property
    def mqtt_publish_qos0_tx_count(self):
        """Gets the mqtt_publish_qos0_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish message (PUBLISH) request packets transmitted to the Client for QoS 0 message delivery.  # noqa: E501

        :return: The mqtt_publish_qos0_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_publish_qos0_tx_count

    @mqtt_publish_qos0_tx_count.setter
    def mqtt_publish_qos0_tx_count(self, mqtt_publish_qos0_tx_count):
        """Sets the mqtt_publish_qos0_tx_count of this MsgVpnClient.

        The number of MQTT publish message (PUBLISH) request packets transmitted to the Client for QoS 0 message delivery.  # noqa: E501

        :param mqtt_publish_qos0_tx_count: The mqtt_publish_qos0_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_publish_qos0_tx_count = mqtt_publish_qos0_tx_count

    @property
    def mqtt_publish_qos1_rx_count(self):
        """Gets the mqtt_publish_qos1_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 1 message delivery.  # noqa: E501

        :return: The mqtt_publish_qos1_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_publish_qos1_rx_count

    @mqtt_publish_qos1_rx_count.setter
    def mqtt_publish_qos1_rx_count(self, mqtt_publish_qos1_rx_count):
        """Sets the mqtt_publish_qos1_rx_count of this MsgVpnClient.

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 1 message delivery.  # noqa: E501

        :param mqtt_publish_qos1_rx_count: The mqtt_publish_qos1_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_publish_qos1_rx_count = mqtt_publish_qos1_rx_count

    @property
    def mqtt_publish_qos1_tx_count(self):
        """Gets the mqtt_publish_qos1_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish message (PUBLISH) request packets transmitted to the Client for QoS 1 message delivery.  # noqa: E501

        :return: The mqtt_publish_qos1_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_publish_qos1_tx_count

    @mqtt_publish_qos1_tx_count.setter
    def mqtt_publish_qos1_tx_count(self, mqtt_publish_qos1_tx_count):
        """Sets the mqtt_publish_qos1_tx_count of this MsgVpnClient.

        The number of MQTT publish message (PUBLISH) request packets transmitted to the Client for QoS 1 message delivery.  # noqa: E501

        :param mqtt_publish_qos1_tx_count: The mqtt_publish_qos1_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_publish_qos1_tx_count = mqtt_publish_qos1_tx_count

    @property
    def mqtt_publish_qos2_rx_count(self):
        """Gets the mqtt_publish_qos2_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 2 message delivery.  # noqa: E501

        :return: The mqtt_publish_qos2_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_publish_qos2_rx_count

    @mqtt_publish_qos2_rx_count.setter
    def mqtt_publish_qos2_rx_count(self, mqtt_publish_qos2_rx_count):
        """Sets the mqtt_publish_qos2_rx_count of this MsgVpnClient.

        The number of MQTT publish message (PUBLISH) request packets received from the Client for QoS 2 message delivery.  # noqa: E501

        :param mqtt_publish_qos2_rx_count: The mqtt_publish_qos2_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_publish_qos2_rx_count = mqtt_publish_qos2_rx_count

    @property
    def mqtt_pubrec_tx_count(self):
        """Gets the mqtt_pubrec_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish received (PUBREC) packets transmitted to the Client in response to a PUBLISH packet with QoS 2. These packets are the second packet of a QoS 2 protocol exchange.  # noqa: E501

        :return: The mqtt_pubrec_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_pubrec_tx_count

    @mqtt_pubrec_tx_count.setter
    def mqtt_pubrec_tx_count(self, mqtt_pubrec_tx_count):
        """Sets the mqtt_pubrec_tx_count of this MsgVpnClient.

        The number of MQTT publish received (PUBREC) packets transmitted to the Client in response to a PUBLISH packet with QoS 2. These packets are the second packet of a QoS 2 protocol exchange.  # noqa: E501

        :param mqtt_pubrec_tx_count: The mqtt_pubrec_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_pubrec_tx_count = mqtt_pubrec_tx_count

    @property
    def mqtt_pubrel_rx_count(self):
        """Gets the mqtt_pubrel_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT publish release (PUBREL) packets received from the Client in response to a PUBREC packet. These packets are the third packet of a QoS 2 protocol exchange.  # noqa: E501

        :return: The mqtt_pubrel_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_pubrel_rx_count

    @mqtt_pubrel_rx_count.setter
    def mqtt_pubrel_rx_count(self, mqtt_pubrel_rx_count):
        """Sets the mqtt_pubrel_rx_count of this MsgVpnClient.

        The number of MQTT publish release (PUBREL) packets received from the Client in response to a PUBREC packet. These packets are the third packet of a QoS 2 protocol exchange.  # noqa: E501

        :param mqtt_pubrel_rx_count: The mqtt_pubrel_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_pubrel_rx_count = mqtt_pubrel_rx_count

    @property
    def mqtt_suback_error_tx_count(self):
        """Gets the mqtt_suback_error_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT subscribe acknowledgement (SUBACK) failure response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_suback_error_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_suback_error_tx_count

    @mqtt_suback_error_tx_count.setter
    def mqtt_suback_error_tx_count(self, mqtt_suback_error_tx_count):
        """Sets the mqtt_suback_error_tx_count of this MsgVpnClient.

        The number of MQTT subscribe acknowledgement (SUBACK) failure response packets transmitted to the Client.  # noqa: E501

        :param mqtt_suback_error_tx_count: The mqtt_suback_error_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_suback_error_tx_count = mqtt_suback_error_tx_count

    @property
    def mqtt_suback_tx_count(self):
        """Gets the mqtt_suback_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT subscribe acknowledgement (SUBACK) response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_suback_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_suback_tx_count

    @mqtt_suback_tx_count.setter
    def mqtt_suback_tx_count(self, mqtt_suback_tx_count):
        """Sets the mqtt_suback_tx_count of this MsgVpnClient.

        The number of MQTT subscribe acknowledgement (SUBACK) response packets transmitted to the Client.  # noqa: E501

        :param mqtt_suback_tx_count: The mqtt_suback_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_suback_tx_count = mqtt_suback_tx_count

    @property
    def mqtt_subscribe_rx_count(self):
        """Gets the mqtt_subscribe_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT subscribe (SUBSCRIBE) request packets received from the Client to create one or more topic subscriptions.  # noqa: E501

        :return: The mqtt_subscribe_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_subscribe_rx_count

    @mqtt_subscribe_rx_count.setter
    def mqtt_subscribe_rx_count(self, mqtt_subscribe_rx_count):
        """Sets the mqtt_subscribe_rx_count of this MsgVpnClient.

        The number of MQTT subscribe (SUBSCRIBE) request packets received from the Client to create one or more topic subscriptions.  # noqa: E501

        :param mqtt_subscribe_rx_count: The mqtt_subscribe_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_subscribe_rx_count = mqtt_subscribe_rx_count

    @property
    def mqtt_unsuback_tx_count(self):
        """Gets the mqtt_unsuback_tx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT unsubscribe acknowledgement (UNSUBACK) response packets transmitted to the Client.  # noqa: E501

        :return: The mqtt_unsuback_tx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_unsuback_tx_count

    @mqtt_unsuback_tx_count.setter
    def mqtt_unsuback_tx_count(self, mqtt_unsuback_tx_count):
        """Sets the mqtt_unsuback_tx_count of this MsgVpnClient.

        The number of MQTT unsubscribe acknowledgement (UNSUBACK) response packets transmitted to the Client.  # noqa: E501

        :param mqtt_unsuback_tx_count: The mqtt_unsuback_tx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_unsuback_tx_count = mqtt_unsuback_tx_count

    @property
    def mqtt_unsubscribe_rx_count(self):
        """Gets the mqtt_unsubscribe_rx_count of this MsgVpnClient.  # noqa: E501

        The number of MQTT unsubscribe (UNSUBSCRIBE) request packets received from the Client to remove one or more topic subscriptions.  # noqa: E501

        :return: The mqtt_unsubscribe_rx_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_unsubscribe_rx_count

    @mqtt_unsubscribe_rx_count.setter
    def mqtt_unsubscribe_rx_count(self, mqtt_unsubscribe_rx_count):
        """Sets the mqtt_unsubscribe_rx_count of this MsgVpnClient.

        The number of MQTT unsubscribe (UNSUBSCRIBE) request packets received from the Client to remove one or more topic subscriptions.  # noqa: E501

        :param mqtt_unsubscribe_rx_count: The mqtt_unsubscribe_rx_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._mqtt_unsubscribe_rx_count = mqtt_unsubscribe_rx_count

    @property
    def msg_spool_congestion_rx_discarded_msg_count(self):
        """Gets the msg_spool_congestion_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded due to message spool congestion primarily caused by message promotion.  # noqa: E501

        :return: The msg_spool_congestion_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_congestion_rx_discarded_msg_count

    @msg_spool_congestion_rx_discarded_msg_count.setter
    def msg_spool_congestion_rx_discarded_msg_count(self, msg_spool_congestion_rx_discarded_msg_count):
        """Sets the msg_spool_congestion_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded due to message spool congestion primarily caused by message promotion.  # noqa: E501

        :param msg_spool_congestion_rx_discarded_msg_count: The msg_spool_congestion_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._msg_spool_congestion_rx_discarded_msg_count = msg_spool_congestion_rx_discarded_msg_count

    @property
    def msg_spool_rx_discarded_msg_count(self):
        """Gets the msg_spool_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded by the message spool.  # noqa: E501

        :return: The msg_spool_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_rx_discarded_msg_count

    @msg_spool_rx_discarded_msg_count.setter
    def msg_spool_rx_discarded_msg_count(self, msg_spool_rx_discarded_msg_count):
        """Sets the msg_spool_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded by the message spool.  # noqa: E501

        :param msg_spool_rx_discarded_msg_count: The msg_spool_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._msg_spool_rx_discarded_msg_count = msg_spool_rx_discarded_msg_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnClient.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnClient.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def no_local_delivery(self):
        """Gets the no_local_delivery of this MsgVpnClient.  # noqa: E501

        Indicates whether not to deliver messages to the Client if it published them.  # noqa: E501

        :return: The no_local_delivery of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._no_local_delivery

    @no_local_delivery.setter
    def no_local_delivery(self, no_local_delivery):
        """Sets the no_local_delivery of this MsgVpnClient.

        Indicates whether not to deliver messages to the Client if it published them.  # noqa: E501

        :param no_local_delivery: The no_local_delivery of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._no_local_delivery = no_local_delivery

    @property
    def no_subscription_match_rx_discarded_msg_count(self):
        """Gets the no_subscription_match_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded due to no matching subscription found.  # noqa: E501

        :return: The no_subscription_match_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._no_subscription_match_rx_discarded_msg_count

    @no_subscription_match_rx_discarded_msg_count.setter
    def no_subscription_match_rx_discarded_msg_count(self, no_subscription_match_rx_discarded_msg_count):
        """Sets the no_subscription_match_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded due to no matching subscription found.  # noqa: E501

        :param no_subscription_match_rx_discarded_msg_count: The no_subscription_match_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._no_subscription_match_rx_discarded_msg_count = no_subscription_match_rx_discarded_msg_count

    @property
    def original_client_username(self):
        """Gets the original_client_username of this MsgVpnClient.  # noqa: E501

        The original value of the client username used for Client authentication.  # noqa: E501

        :return: The original_client_username of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._original_client_username

    @original_client_username.setter
    def original_client_username(self, original_client_username):
        """Sets the original_client_username of this MsgVpnClient.

        The original value of the client username used for Client authentication.  # noqa: E501

        :param original_client_username: The original_client_username of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._original_client_username = original_client_username

    @property
    def other_bind_failure_count(self):
        """Gets the other_bind_failure_count of this MsgVpnClient.  # noqa: E501

        The number of Client bind failures due to other reasons.  # noqa: E501

        :return: The other_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._other_bind_failure_count

    @other_bind_failure_count.setter
    def other_bind_failure_count(self, other_bind_failure_count):
        """Sets the other_bind_failure_count of this MsgVpnClient.

        The number of Client bind failures due to other reasons.  # noqa: E501

        :param other_bind_failure_count: The other_bind_failure_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._other_bind_failure_count = other_bind_failure_count

    @property
    def platform(self):
        """Gets the platform of this MsgVpnClient.  # noqa: E501

        The platform the Client application software was built for, which may include the OS and API type.  # noqa: E501

        :return: The platform of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this MsgVpnClient.

        The platform the Client application software was built for, which may include the OS and API type.  # noqa: E501

        :param platform: The platform of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._platform = platform

    @property
    def publish_topic_acl_rx_discarded_msg_count(self):
        """Gets the publish_topic_acl_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded due to the publish topic being denied by the Access Control List (ACL) profile.  # noqa: E501

        :return: The publish_topic_acl_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._publish_topic_acl_rx_discarded_msg_count

    @publish_topic_acl_rx_discarded_msg_count.setter
    def publish_topic_acl_rx_discarded_msg_count(self, publish_topic_acl_rx_discarded_msg_count):
        """Sets the publish_topic_acl_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded due to the publish topic being denied by the Access Control List (ACL) profile.  # noqa: E501

        :param publish_topic_acl_rx_discarded_msg_count: The publish_topic_acl_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._publish_topic_acl_rx_discarded_msg_count = publish_topic_acl_rx_discarded_msg_count

    @property
    def rest_http_request_rx_byte_count(self):
        """Gets the rest_http_request_rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of HTTP request messages received from the Client, in bytes (B).  # noqa: E501

        :return: The rest_http_request_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_request_rx_byte_count

    @rest_http_request_rx_byte_count.setter
    def rest_http_request_rx_byte_count(self, rest_http_request_rx_byte_count):
        """Sets the rest_http_request_rx_byte_count of this MsgVpnClient.

        The amount of HTTP request messages received from the Client, in bytes (B).  # noqa: E501

        :param rest_http_request_rx_byte_count: The rest_http_request_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_request_rx_byte_count = rest_http_request_rx_byte_count

    @property
    def rest_http_request_rx_msg_count(self):
        """Gets the rest_http_request_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP request messages received from the Client.  # noqa: E501

        :return: The rest_http_request_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_request_rx_msg_count

    @rest_http_request_rx_msg_count.setter
    def rest_http_request_rx_msg_count(self, rest_http_request_rx_msg_count):
        """Sets the rest_http_request_rx_msg_count of this MsgVpnClient.

        The number of HTTP request messages received from the Client.  # noqa: E501

        :param rest_http_request_rx_msg_count: The rest_http_request_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_request_rx_msg_count = rest_http_request_rx_msg_count

    @property
    def rest_http_request_tx_byte_count(self):
        """Gets the rest_http_request_tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of HTTP request messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The rest_http_request_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_request_tx_byte_count

    @rest_http_request_tx_byte_count.setter
    def rest_http_request_tx_byte_count(self, rest_http_request_tx_byte_count):
        """Sets the rest_http_request_tx_byte_count of this MsgVpnClient.

        The amount of HTTP request messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param rest_http_request_tx_byte_count: The rest_http_request_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_request_tx_byte_count = rest_http_request_tx_byte_count

    @property
    def rest_http_request_tx_msg_count(self):
        """Gets the rest_http_request_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP request messages transmitted to the Client.  # noqa: E501

        :return: The rest_http_request_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_request_tx_msg_count

    @rest_http_request_tx_msg_count.setter
    def rest_http_request_tx_msg_count(self, rest_http_request_tx_msg_count):
        """Sets the rest_http_request_tx_msg_count of this MsgVpnClient.

        The number of HTTP request messages transmitted to the Client.  # noqa: E501

        :param rest_http_request_tx_msg_count: The rest_http_request_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_request_tx_msg_count = rest_http_request_tx_msg_count

    @property
    def rest_http_response_error_rx_msg_count(self):
        """Gets the rest_http_response_error_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP client/server error response messages received from the Client.  # noqa: E501

        :return: The rest_http_response_error_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_error_rx_msg_count

    @rest_http_response_error_rx_msg_count.setter
    def rest_http_response_error_rx_msg_count(self, rest_http_response_error_rx_msg_count):
        """Sets the rest_http_response_error_rx_msg_count of this MsgVpnClient.

        The number of HTTP client/server error response messages received from the Client.  # noqa: E501

        :param rest_http_response_error_rx_msg_count: The rest_http_response_error_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_error_rx_msg_count = rest_http_response_error_rx_msg_count

    @property
    def rest_http_response_error_tx_msg_count(self):
        """Gets the rest_http_response_error_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP client/server error response messages transmitted to the Client.  # noqa: E501

        :return: The rest_http_response_error_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_error_tx_msg_count

    @rest_http_response_error_tx_msg_count.setter
    def rest_http_response_error_tx_msg_count(self, rest_http_response_error_tx_msg_count):
        """Sets the rest_http_response_error_tx_msg_count of this MsgVpnClient.

        The number of HTTP client/server error response messages transmitted to the Client.  # noqa: E501

        :param rest_http_response_error_tx_msg_count: The rest_http_response_error_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_error_tx_msg_count = rest_http_response_error_tx_msg_count

    @property
    def rest_http_response_rx_byte_count(self):
        """Gets the rest_http_response_rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of HTTP response messages received from the Client, in bytes (B).  # noqa: E501

        :return: The rest_http_response_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_rx_byte_count

    @rest_http_response_rx_byte_count.setter
    def rest_http_response_rx_byte_count(self, rest_http_response_rx_byte_count):
        """Sets the rest_http_response_rx_byte_count of this MsgVpnClient.

        The amount of HTTP response messages received from the Client, in bytes (B).  # noqa: E501

        :param rest_http_response_rx_byte_count: The rest_http_response_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_rx_byte_count = rest_http_response_rx_byte_count

    @property
    def rest_http_response_rx_msg_count(self):
        """Gets the rest_http_response_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP response messages received from the Client.  # noqa: E501

        :return: The rest_http_response_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_rx_msg_count

    @rest_http_response_rx_msg_count.setter
    def rest_http_response_rx_msg_count(self, rest_http_response_rx_msg_count):
        """Sets the rest_http_response_rx_msg_count of this MsgVpnClient.

        The number of HTTP response messages received from the Client.  # noqa: E501

        :param rest_http_response_rx_msg_count: The rest_http_response_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_rx_msg_count = rest_http_response_rx_msg_count

    @property
    def rest_http_response_success_rx_msg_count(self):
        """Gets the rest_http_response_success_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP successful response messages received from the Client.  # noqa: E501

        :return: The rest_http_response_success_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_success_rx_msg_count

    @rest_http_response_success_rx_msg_count.setter
    def rest_http_response_success_rx_msg_count(self, rest_http_response_success_rx_msg_count):
        """Sets the rest_http_response_success_rx_msg_count of this MsgVpnClient.

        The number of HTTP successful response messages received from the Client.  # noqa: E501

        :param rest_http_response_success_rx_msg_count: The rest_http_response_success_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_success_rx_msg_count = rest_http_response_success_rx_msg_count

    @property
    def rest_http_response_success_tx_msg_count(self):
        """Gets the rest_http_response_success_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP successful response messages transmitted to the Client.  # noqa: E501

        :return: The rest_http_response_success_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_success_tx_msg_count

    @rest_http_response_success_tx_msg_count.setter
    def rest_http_response_success_tx_msg_count(self, rest_http_response_success_tx_msg_count):
        """Sets the rest_http_response_success_tx_msg_count of this MsgVpnClient.

        The number of HTTP successful response messages transmitted to the Client.  # noqa: E501

        :param rest_http_response_success_tx_msg_count: The rest_http_response_success_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_success_tx_msg_count = rest_http_response_success_tx_msg_count

    @property
    def rest_http_response_timeout_rx_msg_count(self):
        """Gets the rest_http_response_timeout_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP wait for reply timeout response messages received from the Client.  # noqa: E501

        :return: The rest_http_response_timeout_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_timeout_rx_msg_count

    @rest_http_response_timeout_rx_msg_count.setter
    def rest_http_response_timeout_rx_msg_count(self, rest_http_response_timeout_rx_msg_count):
        """Sets the rest_http_response_timeout_rx_msg_count of this MsgVpnClient.

        The number of HTTP wait for reply timeout response messages received from the Client.  # noqa: E501

        :param rest_http_response_timeout_rx_msg_count: The rest_http_response_timeout_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_timeout_rx_msg_count = rest_http_response_timeout_rx_msg_count

    @property
    def rest_http_response_timeout_tx_msg_count(self):
        """Gets the rest_http_response_timeout_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP wait for reply timeout response messages transmitted to the Client.  # noqa: E501

        :return: The rest_http_response_timeout_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_timeout_tx_msg_count

    @rest_http_response_timeout_tx_msg_count.setter
    def rest_http_response_timeout_tx_msg_count(self, rest_http_response_timeout_tx_msg_count):
        """Sets the rest_http_response_timeout_tx_msg_count of this MsgVpnClient.

        The number of HTTP wait for reply timeout response messages transmitted to the Client.  # noqa: E501

        :param rest_http_response_timeout_tx_msg_count: The rest_http_response_timeout_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_timeout_tx_msg_count = rest_http_response_timeout_tx_msg_count

    @property
    def rest_http_response_tx_byte_count(self):
        """Gets the rest_http_response_tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of HTTP response messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The rest_http_response_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_tx_byte_count

    @rest_http_response_tx_byte_count.setter
    def rest_http_response_tx_byte_count(self, rest_http_response_tx_byte_count):
        """Sets the rest_http_response_tx_byte_count of this MsgVpnClient.

        The amount of HTTP response messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param rest_http_response_tx_byte_count: The rest_http_response_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_tx_byte_count = rest_http_response_tx_byte_count

    @property
    def rest_http_response_tx_msg_count(self):
        """Gets the rest_http_response_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of HTTP response messages transmitted to the Client.  # noqa: E501

        :return: The rest_http_response_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rest_http_response_tx_msg_count

    @rest_http_response_tx_msg_count.setter
    def rest_http_response_tx_msg_count(self, rest_http_response_tx_msg_count):
        """Sets the rest_http_response_tx_msg_count of this MsgVpnClient.

        The number of HTTP response messages transmitted to the Client.  # noqa: E501

        :param rest_http_response_tx_msg_count: The rest_http_response_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rest_http_response_tx_msg_count = rest_http_response_tx_msg_count

    @property
    def rx_byte_count(self):
        """Gets the rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of messages received from the Client, in bytes (B).  # noqa: E501

        :return: The rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_count

    @rx_byte_count.setter
    def rx_byte_count(self, rx_byte_count):
        """Sets the rx_byte_count of this MsgVpnClient.

        The amount of messages received from the Client, in bytes (B).  # noqa: E501

        :param rx_byte_count: The rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rx_byte_count = rx_byte_count

    @property
    def rx_byte_rate(self):
        """Gets the rx_byte_rate of this MsgVpnClient.  # noqa: E501

        The current message rate received from the Client, in bytes per second (B/sec).  # noqa: E501

        :return: The rx_byte_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_rate

    @rx_byte_rate.setter
    def rx_byte_rate(self, rx_byte_rate):
        """Sets the rx_byte_rate of this MsgVpnClient.

        The current message rate received from the Client, in bytes per second (B/sec).  # noqa: E501

        :param rx_byte_rate: The rx_byte_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rx_byte_rate = rx_byte_rate

    @property
    def rx_discarded_msg_count(self):
        """Gets the rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages discarded during reception from the Client.  # noqa: E501

        :return: The rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rx_discarded_msg_count

    @rx_discarded_msg_count.setter
    def rx_discarded_msg_count(self, rx_discarded_msg_count):
        """Sets the rx_discarded_msg_count of this MsgVpnClient.

        The number of messages discarded during reception from the Client.  # noqa: E501

        :param rx_discarded_msg_count: The rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rx_discarded_msg_count = rx_discarded_msg_count

    @property
    def rx_msg_count(self):
        """Gets the rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages received from the Client.  # noqa: E501

        :return: The rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_count

    @rx_msg_count.setter
    def rx_msg_count(self, rx_msg_count):
        """Sets the rx_msg_count of this MsgVpnClient.

        The number of messages received from the Client.  # noqa: E501

        :param rx_msg_count: The rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rx_msg_count = rx_msg_count

    @property
    def rx_msg_rate(self):
        """Gets the rx_msg_rate of this MsgVpnClient.  # noqa: E501

        The current message rate received from the Client, in messages per second (msg/sec).  # noqa: E501

        :return: The rx_msg_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_rate

    @rx_msg_rate.setter
    def rx_msg_rate(self, rx_msg_rate):
        """Sets the rx_msg_rate of this MsgVpnClient.

        The current message rate received from the Client, in messages per second (msg/sec).  # noqa: E501

        :param rx_msg_rate: The rx_msg_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._rx_msg_rate = rx_msg_rate

    @property
    def slow_subscriber(self):
        """Gets the slow_subscriber of this MsgVpnClient.  # noqa: E501

        Indicates whether the Client is a slow subscriber and blocks for a few seconds when receiving messages.  # noqa: E501

        :return: The slow_subscriber of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._slow_subscriber

    @slow_subscriber.setter
    def slow_subscriber(self, slow_subscriber):
        """Sets the slow_subscriber of this MsgVpnClient.

        Indicates whether the Client is a slow subscriber and blocks for a few seconds when receiving messages.  # noqa: E501

        :param slow_subscriber: The slow_subscriber of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._slow_subscriber = slow_subscriber

    @property
    def software_date(self):
        """Gets the software_date of this MsgVpnClient.  # noqa: E501

        The date the Client application software was built.  # noqa: E501

        :return: The software_date of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._software_date

    @software_date.setter
    def software_date(self, software_date):
        """Sets the software_date of this MsgVpnClient.

        The date the Client application software was built.  # noqa: E501

        :param software_date: The software_date of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._software_date = software_date

    @property
    def software_version(self):
        """Gets the software_version of this MsgVpnClient.  # noqa: E501

        The version of the Client application software.  # noqa: E501

        :return: The software_version of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._software_version

    @software_version.setter
    def software_version(self, software_version):
        """Sets the software_version of this MsgVpnClient.

        The version of the Client application software.  # noqa: E501

        :param software_version: The software_version of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._software_version = software_version

    @property
    def tls_cipher_description(self):
        """Gets the tls_cipher_description of this MsgVpnClient.  # noqa: E501

        The description of the TLS cipher used by the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :return: The tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_description

    @tls_cipher_description.setter
    def tls_cipher_description(self, tls_cipher_description):
        """Sets the tls_cipher_description of this MsgVpnClient.

        The description of the TLS cipher used by the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :param tls_cipher_description: The tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._tls_cipher_description = tls_cipher_description

    @property
    def tls_downgraded_to_plain_text(self):
        """Gets the tls_downgraded_to_plain_text of this MsgVpnClient.  # noqa: E501

        Indicates whether the Client TLS connection was downgraded to plain-text to increase performance.  # noqa: E501

        :return: The tls_downgraded_to_plain_text of this MsgVpnClient.  # noqa: E501
        :rtype: bool
        """
        return self._tls_downgraded_to_plain_text

    @tls_downgraded_to_plain_text.setter
    def tls_downgraded_to_plain_text(self, tls_downgraded_to_plain_text):
        """Sets the tls_downgraded_to_plain_text of this MsgVpnClient.

        Indicates whether the Client TLS connection was downgraded to plain-text to increase performance.  # noqa: E501

        :param tls_downgraded_to_plain_text: The tls_downgraded_to_plain_text of this MsgVpnClient.  # noqa: E501
        :type: bool
        """

        self._tls_downgraded_to_plain_text = tls_downgraded_to_plain_text

    @property
    def tls_version(self):
        """Gets the tls_version of this MsgVpnClient.  # noqa: E501

        The version of TLS used by the Client.  # noqa: E501

        :return: The tls_version of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._tls_version

    @tls_version.setter
    def tls_version(self, tls_version):
        """Sets the tls_version of this MsgVpnClient.

        The version of TLS used by the Client.  # noqa: E501

        :param tls_version: The tls_version of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._tls_version = tls_version

    @property
    def topic_parse_error_rx_discarded_msg_count(self):
        """Gets the topic_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded due to an error while parsing the publish topic.  # noqa: E501

        :return: The topic_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._topic_parse_error_rx_discarded_msg_count

    @topic_parse_error_rx_discarded_msg_count.setter
    def topic_parse_error_rx_discarded_msg_count(self, topic_parse_error_rx_discarded_msg_count):
        """Sets the topic_parse_error_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded due to an error while parsing the publish topic.  # noqa: E501

        :param topic_parse_error_rx_discarded_msg_count: The topic_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._topic_parse_error_rx_discarded_msg_count = topic_parse_error_rx_discarded_msg_count

    @property
    def tx_byte_count(self):
        """Gets the tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_count

    @tx_byte_count.setter
    def tx_byte_count(self, tx_byte_count):
        """Sets the tx_byte_count of this MsgVpnClient.

        The amount of messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param tx_byte_count: The tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._tx_byte_count = tx_byte_count

    @property
    def tx_byte_rate(self):
        """Gets the tx_byte_rate of this MsgVpnClient.  # noqa: E501

        The current message rate transmitted to the Client, in bytes per second (B/sec).  # noqa: E501

        :return: The tx_byte_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_rate

    @tx_byte_rate.setter
    def tx_byte_rate(self, tx_byte_rate):
        """Sets the tx_byte_rate of this MsgVpnClient.

        The current message rate transmitted to the Client, in bytes per second (B/sec).  # noqa: E501

        :param tx_byte_rate: The tx_byte_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._tx_byte_rate = tx_byte_rate

    @property
    def tx_discarded_msg_count(self):
        """Gets the tx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages discarded during transmission to the Client.  # noqa: E501

        :return: The tx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._tx_discarded_msg_count

    @tx_discarded_msg_count.setter
    def tx_discarded_msg_count(self, tx_discarded_msg_count):
        """Sets the tx_discarded_msg_count of this MsgVpnClient.

        The number of messages discarded during transmission to the Client.  # noqa: E501

        :param tx_discarded_msg_count: The tx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._tx_discarded_msg_count = tx_discarded_msg_count

    @property
    def tx_msg_count(self):
        """Gets the tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages transmitted to the Client.  # noqa: E501

        :return: The tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_count

    @tx_msg_count.setter
    def tx_msg_count(self, tx_msg_count):
        """Sets the tx_msg_count of this MsgVpnClient.

        The number of messages transmitted to the Client.  # noqa: E501

        :param tx_msg_count: The tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._tx_msg_count = tx_msg_count

    @property
    def tx_msg_rate(self):
        """Gets the tx_msg_rate of this MsgVpnClient.  # noqa: E501

        The current message rate transmitted to the Client, in messages per second (msg/sec).  # noqa: E501

        :return: The tx_msg_rate of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_rate

    @tx_msg_rate.setter
    def tx_msg_rate(self, tx_msg_rate):
        """Sets the tx_msg_rate of this MsgVpnClient.

        The current message rate transmitted to the Client, in messages per second (msg/sec).  # noqa: E501

        :param tx_msg_rate: The tx_msg_rate of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._tx_msg_rate = tx_msg_rate

    @property
    def uptime(self):
        """Gets the uptime of this MsgVpnClient.  # noqa: E501

        The amount of time in seconds since the Client connected.  # noqa: E501

        :return: The uptime of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """Sets the uptime of this MsgVpnClient.

        The amount of time in seconds since the Client connected.  # noqa: E501

        :param uptime: The uptime of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._uptime = uptime

    @property
    def user(self):
        """Gets the user of this MsgVpnClient.  # noqa: E501

        The user description for the Client, which may include computer name and process ID.  # noqa: E501

        :return: The user of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this MsgVpnClient.

        The user description for the Client, which may include computer name and process ID.  # noqa: E501

        :param user: The user of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._user = user

    @property
    def virtual_router(self):
        """Gets the virtual_router of this MsgVpnClient.  # noqa: E501

        The virtual router used by the Client. The allowed values and their meaning are:  <pre> \"primary\" - The Client is using the primary virtual router. \"backup\" - The Client is using the backup virtual router. \"internal\" - The Client is using the internal virtual router. \"unknown\" - The Client virtual router is unknown. </pre>   # noqa: E501

        :return: The virtual_router of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._virtual_router

    @virtual_router.setter
    def virtual_router(self, virtual_router):
        """Sets the virtual_router of this MsgVpnClient.

        The virtual router used by the Client. The allowed values and their meaning are:  <pre> \"primary\" - The Client is using the primary virtual router. \"backup\" - The Client is using the backup virtual router. \"internal\" - The Client is using the internal virtual router. \"unknown\" - The Client virtual router is unknown. </pre>   # noqa: E501

        :param virtual_router: The virtual_router of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._virtual_router = virtual_router

    @property
    def web_inactive_timeout(self):
        """Gets the web_inactive_timeout of this MsgVpnClient.  # noqa: E501

        The maximum web transport timeout for the Client being inactive, in seconds.  # noqa: E501

        :return: The web_inactive_timeout of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_inactive_timeout

    @web_inactive_timeout.setter
    def web_inactive_timeout(self, web_inactive_timeout):
        """Sets the web_inactive_timeout of this MsgVpnClient.

        The maximum web transport timeout for the Client being inactive, in seconds.  # noqa: E501

        :param web_inactive_timeout: The web_inactive_timeout of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_inactive_timeout = web_inactive_timeout

    @property
    def web_max_payload(self):
        """Gets the web_max_payload of this MsgVpnClient.  # noqa: E501

        The maximum web transport message payload size which excludes the size of the message header, in bytes.  # noqa: E501

        :return: The web_max_payload of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_max_payload

    @web_max_payload.setter
    def web_max_payload(self, web_max_payload):
        """Sets the web_max_payload of this MsgVpnClient.

        The maximum web transport message payload size which excludes the size of the message header, in bytes.  # noqa: E501

        :param web_max_payload: The web_max_payload of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_max_payload = web_max_payload

    @property
    def web_parse_error_rx_discarded_msg_count(self):
        """Gets the web_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501

        The number of messages from the Client discarded due to an error while parsing the web message.  # noqa: E501

        :return: The web_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_parse_error_rx_discarded_msg_count

    @web_parse_error_rx_discarded_msg_count.setter
    def web_parse_error_rx_discarded_msg_count(self, web_parse_error_rx_discarded_msg_count):
        """Sets the web_parse_error_rx_discarded_msg_count of this MsgVpnClient.

        The number of messages from the Client discarded due to an error while parsing the web message.  # noqa: E501

        :param web_parse_error_rx_discarded_msg_count: The web_parse_error_rx_discarded_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_parse_error_rx_discarded_msg_count = web_parse_error_rx_discarded_msg_count

    @property
    def web_remaining_timeout(self):
        """Gets the web_remaining_timeout of this MsgVpnClient.  # noqa: E501

        The remaining web transport timeout for the Client being inactive, in seconds.  # noqa: E501

        :return: The web_remaining_timeout of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_remaining_timeout

    @web_remaining_timeout.setter
    def web_remaining_timeout(self, web_remaining_timeout):
        """Sets the web_remaining_timeout of this MsgVpnClient.

        The remaining web transport timeout for the Client being inactive, in seconds.  # noqa: E501

        :param web_remaining_timeout: The web_remaining_timeout of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_remaining_timeout = web_remaining_timeout

    @property
    def web_rx_byte_count(self):
        """Gets the web_rx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of web transport messages received from the Client, in bytes (B).  # noqa: E501

        :return: The web_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_rx_byte_count

    @web_rx_byte_count.setter
    def web_rx_byte_count(self, web_rx_byte_count):
        """Sets the web_rx_byte_count of this MsgVpnClient.

        The amount of web transport messages received from the Client, in bytes (B).  # noqa: E501

        :param web_rx_byte_count: The web_rx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_rx_byte_count = web_rx_byte_count

    @property
    def web_rx_encoding(self):
        """Gets the web_rx_encoding of this MsgVpnClient.  # noqa: E501

        The type of encoding used during reception from the Client. The allowed values and their meaning are:  <pre> \"binary\" - The Client is using binary encoding. \"base64\" - The Client is using base64 encoding. \"illegal\" - The Client is using an illegal encoding type. </pre>   # noqa: E501

        :return: The web_rx_encoding of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_rx_encoding

    @web_rx_encoding.setter
    def web_rx_encoding(self, web_rx_encoding):
        """Sets the web_rx_encoding of this MsgVpnClient.

        The type of encoding used during reception from the Client. The allowed values and their meaning are:  <pre> \"binary\" - The Client is using binary encoding. \"base64\" - The Client is using base64 encoding. \"illegal\" - The Client is using an illegal encoding type. </pre>   # noqa: E501

        :param web_rx_encoding: The web_rx_encoding of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_rx_encoding = web_rx_encoding

    @property
    def web_rx_msg_count(self):
        """Gets the web_rx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of web transport messages received from the Client.  # noqa: E501

        :return: The web_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_rx_msg_count

    @web_rx_msg_count.setter
    def web_rx_msg_count(self, web_rx_msg_count):
        """Sets the web_rx_msg_count of this MsgVpnClient.

        The number of web transport messages received from the Client.  # noqa: E501

        :param web_rx_msg_count: The web_rx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_rx_msg_count = web_rx_msg_count

    @property
    def web_rx_protocol(self):
        """Gets the web_rx_protocol of this MsgVpnClient.  # noqa: E501

        The type of web transport used during reception from the Client. The allowed values and their meaning are:  <pre> \"ws-binary\" - The Client is using WebSocket binary transport. \"http-binary-streaming\" - The Client is using HTTP binary streaming transport. \"http-binary\" - The Client is using HTTP binary transport. \"http-base64\" - The Client is using HTTP base64 transport. </pre>   # noqa: E501

        :return: The web_rx_protocol of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_rx_protocol

    @web_rx_protocol.setter
    def web_rx_protocol(self, web_rx_protocol):
        """Sets the web_rx_protocol of this MsgVpnClient.

        The type of web transport used during reception from the Client. The allowed values and their meaning are:  <pre> \"ws-binary\" - The Client is using WebSocket binary transport. \"http-binary-streaming\" - The Client is using HTTP binary streaming transport. \"http-binary\" - The Client is using HTTP binary transport. \"http-base64\" - The Client is using HTTP base64 transport. </pre>   # noqa: E501

        :param web_rx_protocol: The web_rx_protocol of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_rx_protocol = web_rx_protocol

    @property
    def web_rx_request_count(self):
        """Gets the web_rx_request_count of this MsgVpnClient.  # noqa: E501

        The number of web transport requests received from the Client (HTTP only). Not available for WebSockets.  # noqa: E501

        :return: The web_rx_request_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_rx_request_count

    @web_rx_request_count.setter
    def web_rx_request_count(self, web_rx_request_count):
        """Sets the web_rx_request_count of this MsgVpnClient.

        The number of web transport requests received from the Client (HTTP only). Not available for WebSockets.  # noqa: E501

        :param web_rx_request_count: The web_rx_request_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_rx_request_count = web_rx_request_count

    @property
    def web_rx_response_count(self):
        """Gets the web_rx_response_count of this MsgVpnClient.  # noqa: E501

        The number of web transport responses transmitted to the Client on the receive connection (HTTP only). Not available for WebSockets.  # noqa: E501

        :return: The web_rx_response_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_rx_response_count

    @web_rx_response_count.setter
    def web_rx_response_count(self, web_rx_response_count):
        """Sets the web_rx_response_count of this MsgVpnClient.

        The number of web transport responses transmitted to the Client on the receive connection (HTTP only). Not available for WebSockets.  # noqa: E501

        :param web_rx_response_count: The web_rx_response_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_rx_response_count = web_rx_response_count

    @property
    def web_rx_tcp_state(self):
        """Gets the web_rx_tcp_state of this MsgVpnClient.  # noqa: E501

        The TCP state of the receive connection from the Client. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :return: The web_rx_tcp_state of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_rx_tcp_state

    @web_rx_tcp_state.setter
    def web_rx_tcp_state(self, web_rx_tcp_state):
        """Sets the web_rx_tcp_state of this MsgVpnClient.

        The TCP state of the receive connection from the Client. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :param web_rx_tcp_state: The web_rx_tcp_state of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_rx_tcp_state = web_rx_tcp_state

    @property
    def web_rx_tls_cipher_description(self):
        """Gets the web_rx_tls_cipher_description of this MsgVpnClient.  # noqa: E501

        The description of the TLS cipher received from the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :return: The web_rx_tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_rx_tls_cipher_description

    @web_rx_tls_cipher_description.setter
    def web_rx_tls_cipher_description(self, web_rx_tls_cipher_description):
        """Sets the web_rx_tls_cipher_description of this MsgVpnClient.

        The description of the TLS cipher received from the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :param web_rx_tls_cipher_description: The web_rx_tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_rx_tls_cipher_description = web_rx_tls_cipher_description

    @property
    def web_rx_tls_version(self):
        """Gets the web_rx_tls_version of this MsgVpnClient.  # noqa: E501

        The version of TLS used during reception from the Client.  # noqa: E501

        :return: The web_rx_tls_version of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_rx_tls_version

    @web_rx_tls_version.setter
    def web_rx_tls_version(self, web_rx_tls_version):
        """Sets the web_rx_tls_version of this MsgVpnClient.

        The version of TLS used during reception from the Client.  # noqa: E501

        :param web_rx_tls_version: The web_rx_tls_version of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_rx_tls_version = web_rx_tls_version

    @property
    def web_session_id(self):
        """Gets the web_session_id of this MsgVpnClient.  # noqa: E501

        The identifier (ID) of the web transport session for the Client.  # noqa: E501

        :return: The web_session_id of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_session_id

    @web_session_id.setter
    def web_session_id(self, web_session_id):
        """Sets the web_session_id of this MsgVpnClient.

        The identifier (ID) of the web transport session for the Client.  # noqa: E501

        :param web_session_id: The web_session_id of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_session_id = web_session_id

    @property
    def web_tx_byte_count(self):
        """Gets the web_tx_byte_count of this MsgVpnClient.  # noqa: E501

        The amount of web transport messages transmitted to the Client, in bytes (B).  # noqa: E501

        :return: The web_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_tx_byte_count

    @web_tx_byte_count.setter
    def web_tx_byte_count(self, web_tx_byte_count):
        """Sets the web_tx_byte_count of this MsgVpnClient.

        The amount of web transport messages transmitted to the Client, in bytes (B).  # noqa: E501

        :param web_tx_byte_count: The web_tx_byte_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_tx_byte_count = web_tx_byte_count

    @property
    def web_tx_encoding(self):
        """Gets the web_tx_encoding of this MsgVpnClient.  # noqa: E501

        The type of encoding used during transmission to the Client. The allowed values and their meaning are:  <pre> \"binary\" - The Client is using binary encoding. \"base64\" - The Client is using base64 encoding. \"illegal\" - The Client is using an illegal encoding type. </pre>   # noqa: E501

        :return: The web_tx_encoding of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_tx_encoding

    @web_tx_encoding.setter
    def web_tx_encoding(self, web_tx_encoding):
        """Sets the web_tx_encoding of this MsgVpnClient.

        The type of encoding used during transmission to the Client. The allowed values and their meaning are:  <pre> \"binary\" - The Client is using binary encoding. \"base64\" - The Client is using base64 encoding. \"illegal\" - The Client is using an illegal encoding type. </pre>   # noqa: E501

        :param web_tx_encoding: The web_tx_encoding of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_tx_encoding = web_tx_encoding

    @property
    def web_tx_msg_count(self):
        """Gets the web_tx_msg_count of this MsgVpnClient.  # noqa: E501

        The number of web transport messages transmitted to the Client.  # noqa: E501

        :return: The web_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_tx_msg_count

    @web_tx_msg_count.setter
    def web_tx_msg_count(self, web_tx_msg_count):
        """Sets the web_tx_msg_count of this MsgVpnClient.

        The number of web transport messages transmitted to the Client.  # noqa: E501

        :param web_tx_msg_count: The web_tx_msg_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_tx_msg_count = web_tx_msg_count

    @property
    def web_tx_protocol(self):
        """Gets the web_tx_protocol of this MsgVpnClient.  # noqa: E501

        The type of web transport used during transmission to the Client. The allowed values and their meaning are:  <pre> \"ws-binary\" - The Client is using WebSocket binary transport. \"http-binary-streaming\" - The Client is using HTTP binary streaming transport. \"http-binary\" - The Client is using HTTP binary transport. \"http-base64\" - The Client is using HTTP base64 transport. </pre>   # noqa: E501

        :return: The web_tx_protocol of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_tx_protocol

    @web_tx_protocol.setter
    def web_tx_protocol(self, web_tx_protocol):
        """Sets the web_tx_protocol of this MsgVpnClient.

        The type of web transport used during transmission to the Client. The allowed values and their meaning are:  <pre> \"ws-binary\" - The Client is using WebSocket binary transport. \"http-binary-streaming\" - The Client is using HTTP binary streaming transport. \"http-binary\" - The Client is using HTTP binary transport. \"http-base64\" - The Client is using HTTP base64 transport. </pre>   # noqa: E501

        :param web_tx_protocol: The web_tx_protocol of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_tx_protocol = web_tx_protocol

    @property
    def web_tx_request_count(self):
        """Gets the web_tx_request_count of this MsgVpnClient.  # noqa: E501

        The number of web transport requests transmitted to the Client (HTTP only). Not available for WebSockets.  # noqa: E501

        :return: The web_tx_request_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_tx_request_count

    @web_tx_request_count.setter
    def web_tx_request_count(self, web_tx_request_count):
        """Sets the web_tx_request_count of this MsgVpnClient.

        The number of web transport requests transmitted to the Client (HTTP only). Not available for WebSockets.  # noqa: E501

        :param web_tx_request_count: The web_tx_request_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_tx_request_count = web_tx_request_count

    @property
    def web_tx_response_count(self):
        """Gets the web_tx_response_count of this MsgVpnClient.  # noqa: E501

        The number of web transport responses received from the Client on the transmit connection (HTTP only). Not available for WebSockets.  # noqa: E501

        :return: The web_tx_response_count of this MsgVpnClient.  # noqa: E501
        :rtype: int
        """
        return self._web_tx_response_count

    @web_tx_response_count.setter
    def web_tx_response_count(self, web_tx_response_count):
        """Sets the web_tx_response_count of this MsgVpnClient.

        The number of web transport responses received from the Client on the transmit connection (HTTP only). Not available for WebSockets.  # noqa: E501

        :param web_tx_response_count: The web_tx_response_count of this MsgVpnClient.  # noqa: E501
        :type: int
        """

        self._web_tx_response_count = web_tx_response_count

    @property
    def web_tx_tcp_state(self):
        """Gets the web_tx_tcp_state of this MsgVpnClient.  # noqa: E501

        The TCP state of the transmit connection to the Client. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :return: The web_tx_tcp_state of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_tx_tcp_state

    @web_tx_tcp_state.setter
    def web_tx_tcp_state(self, web_tx_tcp_state):
        """Sets the web_tx_tcp_state of this MsgVpnClient.

        The TCP state of the transmit connection to the Client. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :param web_tx_tcp_state: The web_tx_tcp_state of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_tx_tcp_state = web_tx_tcp_state

    @property
    def web_tx_tls_cipher_description(self):
        """Gets the web_tx_tls_cipher_description of this MsgVpnClient.  # noqa: E501

        The description of the TLS cipher transmitted to the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :return: The web_tx_tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_tx_tls_cipher_description

    @web_tx_tls_cipher_description.setter
    def web_tx_tls_cipher_description(self, web_tx_tls_cipher_description):
        """Sets the web_tx_tls_cipher_description of this MsgVpnClient.

        The description of the TLS cipher transmitted to the Client, which may include cipher name, key exchange and encryption algorithms.  # noqa: E501

        :param web_tx_tls_cipher_description: The web_tx_tls_cipher_description of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_tx_tls_cipher_description = web_tx_tls_cipher_description

    @property
    def web_tx_tls_version(self):
        """Gets the web_tx_tls_version of this MsgVpnClient.  # noqa: E501

        The version of TLS used during transmission to the Client.  # noqa: E501

        :return: The web_tx_tls_version of this MsgVpnClient.  # noqa: E501
        :rtype: str
        """
        return self._web_tx_tls_version

    @web_tx_tls_version.setter
    def web_tx_tls_version(self, web_tx_tls_version):
        """Sets the web_tx_tls_version of this MsgVpnClient.

        The version of TLS used during transmission to the Client.  # noqa: E501

        :param web_tx_tls_version: The web_tx_tls_version of this MsgVpnClient.  # noqa: E501
        :type: str
        """

        self._web_tx_tls_version = web_tx_tls_version

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
        if issubclass(MsgVpnClient, dict):
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
        if not isinstance(other, MsgVpnClient):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
