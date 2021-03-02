# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.18
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Broker(object):
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
        'auth_client_cert_revocation_check_mode': 'str',
        'average_rx_byte_rate': 'int',
        'average_rx_compressed_byte_rate': 'int',
        'average_rx_msg_rate': 'int',
        'average_rx_uncompressed_byte_rate': 'int',
        'average_tx_byte_rate': 'int',
        'average_tx_compressed_byte_rate': 'int',
        'average_tx_msg_rate': 'int',
        'average_tx_uncompressed_byte_rate': 'int',
        'cspf_version': 'int',
        'guaranteed_msging_defragmentation_estimated_fragmentation': 'int',
        'guaranteed_msging_defragmentation_estimated_recoverable_space': 'int',
        'guaranteed_msging_defragmentation_last_completed_on': 'int',
        'guaranteed_msging_defragmentation_last_completion_percentage': 'int',
        'guaranteed_msging_defragmentation_last_exit_condition': 'str',
        'guaranteed_msging_defragmentation_last_exit_condition_information': 'str',
        'guaranteed_msging_defragmentation_status': 'str',
        'guaranteed_msging_defragmentation_status_active_completion_percentage': 'int',
        'guaranteed_msging_enabled': 'bool',
        'guaranteed_msging_event_cache_usage_threshold': 'EventThreshold',
        'guaranteed_msging_event_delivered_unacked_threshold': 'EventThresholdByPercent',
        'guaranteed_msging_event_disk_usage_threshold': 'EventThresholdByPercent',
        'guaranteed_msging_event_egress_flow_count_threshold': 'EventThreshold',
        'guaranteed_msging_event_endpoint_count_threshold': 'EventThreshold',
        'guaranteed_msging_event_ingress_flow_count_threshold': 'EventThreshold',
        'guaranteed_msging_event_msg_count_threshold': 'EventThresholdByPercent',
        'guaranteed_msging_event_msg_spool_file_count_threshold': 'EventThresholdByPercent',
        'guaranteed_msging_event_msg_spool_usage_threshold': 'EventThreshold',
        'guaranteed_msging_event_transacted_session_count_threshold': 'EventThreshold',
        'guaranteed_msging_event_transacted_session_resource_count_threshold': 'EventThresholdByPercent',
        'guaranteed_msging_event_transaction_count_threshold': 'EventThreshold',
        'guaranteed_msging_max_cache_usage': 'int',
        'guaranteed_msging_max_msg_spool_usage': 'int',
        'guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout': 'int',
        'guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout': 'int',
        'guaranteed_msging_operational_status': 'str',
        'guaranteed_msging_transaction_replication_compatibility_mode': 'str',
        'rx_byte_count': 'int',
        'rx_byte_rate': 'int',
        'rx_compressed_byte_count': 'int',
        'rx_compressed_byte_rate': 'int',
        'rx_compression_ratio': 'str',
        'rx_msg_count': 'int',
        'rx_msg_rate': 'int',
        'rx_uncompressed_byte_count': 'int',
        'rx_uncompressed_byte_rate': 'int',
        'service_amqp_enabled': 'bool',
        'service_amqp_tls_listen_port': 'int',
        'service_event_connection_count_threshold': 'EventThreshold',
        'service_health_check_enabled': 'bool',
        'service_health_check_listen_port': 'int',
        'service_mate_link_enabled': 'bool',
        'service_mate_link_listen_port': 'int',
        'service_mqtt_enabled': 'bool',
        'service_msg_backbone_enabled': 'bool',
        'service_redundancy_enabled': 'bool',
        'service_redundancy_first_listen_port': 'int',
        'service_rest_event_outgoing_connection_count_threshold': 'EventThreshold',
        'service_rest_incoming_enabled': 'bool',
        'service_rest_outgoing_enabled': 'bool',
        'service_semp_legacy_timeout_enabled': 'bool',
        'service_semp_plain_text_enabled': 'bool',
        'service_semp_plain_text_listen_port': 'int',
        'service_semp_tls_enabled': 'bool',
        'service_semp_tls_listen_port': 'int',
        'service_smf_compression_listen_port': 'int',
        'service_smf_enabled': 'bool',
        'service_smf_event_connection_count_threshold': 'EventThreshold',
        'service_smf_plain_text_listen_port': 'int',
        'service_smf_routing_control_listen_port': 'int',
        'service_smf_tls_listen_port': 'int',
        'service_tls_event_connection_count_threshold': 'EventThreshold',
        'service_web_transport_enabled': 'bool',
        'service_web_transport_plain_text_listen_port': 'int',
        'service_web_transport_tls_listen_port': 'int',
        'service_web_transport_web_url_suffix': 'str',
        'tls_block_version11_enabled': 'bool',
        'tls_cipher_suite_management_default_list': 'str',
        'tls_cipher_suite_management_list': 'str',
        'tls_cipher_suite_management_supported_list': 'str',
        'tls_cipher_suite_msg_backbone_default_list': 'str',
        'tls_cipher_suite_msg_backbone_list': 'str',
        'tls_cipher_suite_msg_backbone_supported_list': 'str',
        'tls_cipher_suite_secure_shell_default_list': 'str',
        'tls_cipher_suite_secure_shell_list': 'str',
        'tls_cipher_suite_secure_shell_supported_list': 'str',
        'tls_crime_exploit_protection_enabled': 'bool',
        'tls_ticket_lifetime': 'int',
        'tls_version_supported_list': 'str',
        'tx_byte_count': 'int',
        'tx_byte_rate': 'int',
        'tx_compressed_byte_count': 'int',
        'tx_compressed_byte_rate': 'int',
        'tx_compression_ratio': 'str',
        'tx_msg_count': 'int',
        'tx_msg_rate': 'int',
        'tx_uncompressed_byte_count': 'int',
        'tx_uncompressed_byte_rate': 'int'
    }

    attribute_map = {
        'auth_client_cert_revocation_check_mode': 'authClientCertRevocationCheckMode',
        'average_rx_byte_rate': 'averageRxByteRate',
        'average_rx_compressed_byte_rate': 'averageRxCompressedByteRate',
        'average_rx_msg_rate': 'averageRxMsgRate',
        'average_rx_uncompressed_byte_rate': 'averageRxUncompressedByteRate',
        'average_tx_byte_rate': 'averageTxByteRate',
        'average_tx_compressed_byte_rate': 'averageTxCompressedByteRate',
        'average_tx_msg_rate': 'averageTxMsgRate',
        'average_tx_uncompressed_byte_rate': 'averageTxUncompressedByteRate',
        'cspf_version': 'cspfVersion',
        'guaranteed_msging_defragmentation_estimated_fragmentation': 'guaranteedMsgingDefragmentationEstimatedFragmentation',
        'guaranteed_msging_defragmentation_estimated_recoverable_space': 'guaranteedMsgingDefragmentationEstimatedRecoverableSpace',
        'guaranteed_msging_defragmentation_last_completed_on': 'guaranteedMsgingDefragmentationLastCompletedOn',
        'guaranteed_msging_defragmentation_last_completion_percentage': 'guaranteedMsgingDefragmentationLastCompletionPercentage',
        'guaranteed_msging_defragmentation_last_exit_condition': 'guaranteedMsgingDefragmentationLastExitCondition',
        'guaranteed_msging_defragmentation_last_exit_condition_information': 'guaranteedMsgingDefragmentationLastExitConditionInformation',
        'guaranteed_msging_defragmentation_status': 'guaranteedMsgingDefragmentationStatus',
        'guaranteed_msging_defragmentation_status_active_completion_percentage': 'guaranteedMsgingDefragmentationStatusActiveCompletionPercentage',
        'guaranteed_msging_enabled': 'guaranteedMsgingEnabled',
        'guaranteed_msging_event_cache_usage_threshold': 'guaranteedMsgingEventCacheUsageThreshold',
        'guaranteed_msging_event_delivered_unacked_threshold': 'guaranteedMsgingEventDeliveredUnackedThreshold',
        'guaranteed_msging_event_disk_usage_threshold': 'guaranteedMsgingEventDiskUsageThreshold',
        'guaranteed_msging_event_egress_flow_count_threshold': 'guaranteedMsgingEventEgressFlowCountThreshold',
        'guaranteed_msging_event_endpoint_count_threshold': 'guaranteedMsgingEventEndpointCountThreshold',
        'guaranteed_msging_event_ingress_flow_count_threshold': 'guaranteedMsgingEventIngressFlowCountThreshold',
        'guaranteed_msging_event_msg_count_threshold': 'guaranteedMsgingEventMsgCountThreshold',
        'guaranteed_msging_event_msg_spool_file_count_threshold': 'guaranteedMsgingEventMsgSpoolFileCountThreshold',
        'guaranteed_msging_event_msg_spool_usage_threshold': 'guaranteedMsgingEventMsgSpoolUsageThreshold',
        'guaranteed_msging_event_transacted_session_count_threshold': 'guaranteedMsgingEventTransactedSessionCountThreshold',
        'guaranteed_msging_event_transacted_session_resource_count_threshold': 'guaranteedMsgingEventTransactedSessionResourceCountThreshold',
        'guaranteed_msging_event_transaction_count_threshold': 'guaranteedMsgingEventTransactionCountThreshold',
        'guaranteed_msging_max_cache_usage': 'guaranteedMsgingMaxCacheUsage',
        'guaranteed_msging_max_msg_spool_usage': 'guaranteedMsgingMaxMsgSpoolUsage',
        'guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout': 'guaranteedMsgingMsgSpoolSyncMirroredMsgAckTimeout',
        'guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout': 'guaranteedMsgingMsgSpoolSyncMirroredSpoolFileAckTimeout',
        'guaranteed_msging_operational_status': 'guaranteedMsgingOperationalStatus',
        'guaranteed_msging_transaction_replication_compatibility_mode': 'guaranteedMsgingTransactionReplicationCompatibilityMode',
        'rx_byte_count': 'rxByteCount',
        'rx_byte_rate': 'rxByteRate',
        'rx_compressed_byte_count': 'rxCompressedByteCount',
        'rx_compressed_byte_rate': 'rxCompressedByteRate',
        'rx_compression_ratio': 'rxCompressionRatio',
        'rx_msg_count': 'rxMsgCount',
        'rx_msg_rate': 'rxMsgRate',
        'rx_uncompressed_byte_count': 'rxUncompressedByteCount',
        'rx_uncompressed_byte_rate': 'rxUncompressedByteRate',
        'service_amqp_enabled': 'serviceAmqpEnabled',
        'service_amqp_tls_listen_port': 'serviceAmqpTlsListenPort',
        'service_event_connection_count_threshold': 'serviceEventConnectionCountThreshold',
        'service_health_check_enabled': 'serviceHealthCheckEnabled',
        'service_health_check_listen_port': 'serviceHealthCheckListenPort',
        'service_mate_link_enabled': 'serviceMateLinkEnabled',
        'service_mate_link_listen_port': 'serviceMateLinkListenPort',
        'service_mqtt_enabled': 'serviceMqttEnabled',
        'service_msg_backbone_enabled': 'serviceMsgBackboneEnabled',
        'service_redundancy_enabled': 'serviceRedundancyEnabled',
        'service_redundancy_first_listen_port': 'serviceRedundancyFirstListenPort',
        'service_rest_event_outgoing_connection_count_threshold': 'serviceRestEventOutgoingConnectionCountThreshold',
        'service_rest_incoming_enabled': 'serviceRestIncomingEnabled',
        'service_rest_outgoing_enabled': 'serviceRestOutgoingEnabled',
        'service_semp_legacy_timeout_enabled': 'serviceSempLegacyTimeoutEnabled',
        'service_semp_plain_text_enabled': 'serviceSempPlainTextEnabled',
        'service_semp_plain_text_listen_port': 'serviceSempPlainTextListenPort',
        'service_semp_tls_enabled': 'serviceSempTlsEnabled',
        'service_semp_tls_listen_port': 'serviceSempTlsListenPort',
        'service_smf_compression_listen_port': 'serviceSmfCompressionListenPort',
        'service_smf_enabled': 'serviceSmfEnabled',
        'service_smf_event_connection_count_threshold': 'serviceSmfEventConnectionCountThreshold',
        'service_smf_plain_text_listen_port': 'serviceSmfPlainTextListenPort',
        'service_smf_routing_control_listen_port': 'serviceSmfRoutingControlListenPort',
        'service_smf_tls_listen_port': 'serviceSmfTlsListenPort',
        'service_tls_event_connection_count_threshold': 'serviceTlsEventConnectionCountThreshold',
        'service_web_transport_enabled': 'serviceWebTransportEnabled',
        'service_web_transport_plain_text_listen_port': 'serviceWebTransportPlainTextListenPort',
        'service_web_transport_tls_listen_port': 'serviceWebTransportTlsListenPort',
        'service_web_transport_web_url_suffix': 'serviceWebTransportWebUrlSuffix',
        'tls_block_version11_enabled': 'tlsBlockVersion11Enabled',
        'tls_cipher_suite_management_default_list': 'tlsCipherSuiteManagementDefaultList',
        'tls_cipher_suite_management_list': 'tlsCipherSuiteManagementList',
        'tls_cipher_suite_management_supported_list': 'tlsCipherSuiteManagementSupportedList',
        'tls_cipher_suite_msg_backbone_default_list': 'tlsCipherSuiteMsgBackboneDefaultList',
        'tls_cipher_suite_msg_backbone_list': 'tlsCipherSuiteMsgBackboneList',
        'tls_cipher_suite_msg_backbone_supported_list': 'tlsCipherSuiteMsgBackboneSupportedList',
        'tls_cipher_suite_secure_shell_default_list': 'tlsCipherSuiteSecureShellDefaultList',
        'tls_cipher_suite_secure_shell_list': 'tlsCipherSuiteSecureShellList',
        'tls_cipher_suite_secure_shell_supported_list': 'tlsCipherSuiteSecureShellSupportedList',
        'tls_crime_exploit_protection_enabled': 'tlsCrimeExploitProtectionEnabled',
        'tls_ticket_lifetime': 'tlsTicketLifetime',
        'tls_version_supported_list': 'tlsVersionSupportedList',
        'tx_byte_count': 'txByteCount',
        'tx_byte_rate': 'txByteRate',
        'tx_compressed_byte_count': 'txCompressedByteCount',
        'tx_compressed_byte_rate': 'txCompressedByteRate',
        'tx_compression_ratio': 'txCompressionRatio',
        'tx_msg_count': 'txMsgCount',
        'tx_msg_rate': 'txMsgRate',
        'tx_uncompressed_byte_count': 'txUncompressedByteCount',
        'tx_uncompressed_byte_rate': 'txUncompressedByteRate'
    }

    def __init__(self, auth_client_cert_revocation_check_mode=None, average_rx_byte_rate=None, average_rx_compressed_byte_rate=None, average_rx_msg_rate=None, average_rx_uncompressed_byte_rate=None, average_tx_byte_rate=None, average_tx_compressed_byte_rate=None, average_tx_msg_rate=None, average_tx_uncompressed_byte_rate=None, cspf_version=None, guaranteed_msging_defragmentation_estimated_fragmentation=None, guaranteed_msging_defragmentation_estimated_recoverable_space=None, guaranteed_msging_defragmentation_last_completed_on=None, guaranteed_msging_defragmentation_last_completion_percentage=None, guaranteed_msging_defragmentation_last_exit_condition=None, guaranteed_msging_defragmentation_last_exit_condition_information=None, guaranteed_msging_defragmentation_status=None, guaranteed_msging_defragmentation_status_active_completion_percentage=None, guaranteed_msging_enabled=None, guaranteed_msging_event_cache_usage_threshold=None, guaranteed_msging_event_delivered_unacked_threshold=None, guaranteed_msging_event_disk_usage_threshold=None, guaranteed_msging_event_egress_flow_count_threshold=None, guaranteed_msging_event_endpoint_count_threshold=None, guaranteed_msging_event_ingress_flow_count_threshold=None, guaranteed_msging_event_msg_count_threshold=None, guaranteed_msging_event_msg_spool_file_count_threshold=None, guaranteed_msging_event_msg_spool_usage_threshold=None, guaranteed_msging_event_transacted_session_count_threshold=None, guaranteed_msging_event_transacted_session_resource_count_threshold=None, guaranteed_msging_event_transaction_count_threshold=None, guaranteed_msging_max_cache_usage=None, guaranteed_msging_max_msg_spool_usage=None, guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout=None, guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout=None, guaranteed_msging_operational_status=None, guaranteed_msging_transaction_replication_compatibility_mode=None, rx_byte_count=None, rx_byte_rate=None, rx_compressed_byte_count=None, rx_compressed_byte_rate=None, rx_compression_ratio=None, rx_msg_count=None, rx_msg_rate=None, rx_uncompressed_byte_count=None, rx_uncompressed_byte_rate=None, service_amqp_enabled=None, service_amqp_tls_listen_port=None, service_event_connection_count_threshold=None, service_health_check_enabled=None, service_health_check_listen_port=None, service_mate_link_enabled=None, service_mate_link_listen_port=None, service_mqtt_enabled=None, service_msg_backbone_enabled=None, service_redundancy_enabled=None, service_redundancy_first_listen_port=None, service_rest_event_outgoing_connection_count_threshold=None, service_rest_incoming_enabled=None, service_rest_outgoing_enabled=None, service_semp_legacy_timeout_enabled=None, service_semp_plain_text_enabled=None, service_semp_plain_text_listen_port=None, service_semp_tls_enabled=None, service_semp_tls_listen_port=None, service_smf_compression_listen_port=None, service_smf_enabled=None, service_smf_event_connection_count_threshold=None, service_smf_plain_text_listen_port=None, service_smf_routing_control_listen_port=None, service_smf_tls_listen_port=None, service_tls_event_connection_count_threshold=None, service_web_transport_enabled=None, service_web_transport_plain_text_listen_port=None, service_web_transport_tls_listen_port=None, service_web_transport_web_url_suffix=None, tls_block_version11_enabled=None, tls_cipher_suite_management_default_list=None, tls_cipher_suite_management_list=None, tls_cipher_suite_management_supported_list=None, tls_cipher_suite_msg_backbone_default_list=None, tls_cipher_suite_msg_backbone_list=None, tls_cipher_suite_msg_backbone_supported_list=None, tls_cipher_suite_secure_shell_default_list=None, tls_cipher_suite_secure_shell_list=None, tls_cipher_suite_secure_shell_supported_list=None, tls_crime_exploit_protection_enabled=None, tls_ticket_lifetime=None, tls_version_supported_list=None, tx_byte_count=None, tx_byte_rate=None, tx_compressed_byte_count=None, tx_compressed_byte_rate=None, tx_compression_ratio=None, tx_msg_count=None, tx_msg_rate=None, tx_uncompressed_byte_count=None, tx_uncompressed_byte_rate=None):  # noqa: E501
        """Broker - a model defined in Swagger"""  # noqa: E501

        self._auth_client_cert_revocation_check_mode = None
        self._average_rx_byte_rate = None
        self._average_rx_compressed_byte_rate = None
        self._average_rx_msg_rate = None
        self._average_rx_uncompressed_byte_rate = None
        self._average_tx_byte_rate = None
        self._average_tx_compressed_byte_rate = None
        self._average_tx_msg_rate = None
        self._average_tx_uncompressed_byte_rate = None
        self._cspf_version = None
        self._guaranteed_msging_defragmentation_estimated_fragmentation = None
        self._guaranteed_msging_defragmentation_estimated_recoverable_space = None
        self._guaranteed_msging_defragmentation_last_completed_on = None
        self._guaranteed_msging_defragmentation_last_completion_percentage = None
        self._guaranteed_msging_defragmentation_last_exit_condition = None
        self._guaranteed_msging_defragmentation_last_exit_condition_information = None
        self._guaranteed_msging_defragmentation_status = None
        self._guaranteed_msging_defragmentation_status_active_completion_percentage = None
        self._guaranteed_msging_enabled = None
        self._guaranteed_msging_event_cache_usage_threshold = None
        self._guaranteed_msging_event_delivered_unacked_threshold = None
        self._guaranteed_msging_event_disk_usage_threshold = None
        self._guaranteed_msging_event_egress_flow_count_threshold = None
        self._guaranteed_msging_event_endpoint_count_threshold = None
        self._guaranteed_msging_event_ingress_flow_count_threshold = None
        self._guaranteed_msging_event_msg_count_threshold = None
        self._guaranteed_msging_event_msg_spool_file_count_threshold = None
        self._guaranteed_msging_event_msg_spool_usage_threshold = None
        self._guaranteed_msging_event_transacted_session_count_threshold = None
        self._guaranteed_msging_event_transacted_session_resource_count_threshold = None
        self._guaranteed_msging_event_transaction_count_threshold = None
        self._guaranteed_msging_max_cache_usage = None
        self._guaranteed_msging_max_msg_spool_usage = None
        self._guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout = None
        self._guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout = None
        self._guaranteed_msging_operational_status = None
        self._guaranteed_msging_transaction_replication_compatibility_mode = None
        self._rx_byte_count = None
        self._rx_byte_rate = None
        self._rx_compressed_byte_count = None
        self._rx_compressed_byte_rate = None
        self._rx_compression_ratio = None
        self._rx_msg_count = None
        self._rx_msg_rate = None
        self._rx_uncompressed_byte_count = None
        self._rx_uncompressed_byte_rate = None
        self._service_amqp_enabled = None
        self._service_amqp_tls_listen_port = None
        self._service_event_connection_count_threshold = None
        self._service_health_check_enabled = None
        self._service_health_check_listen_port = None
        self._service_mate_link_enabled = None
        self._service_mate_link_listen_port = None
        self._service_mqtt_enabled = None
        self._service_msg_backbone_enabled = None
        self._service_redundancy_enabled = None
        self._service_redundancy_first_listen_port = None
        self._service_rest_event_outgoing_connection_count_threshold = None
        self._service_rest_incoming_enabled = None
        self._service_rest_outgoing_enabled = None
        self._service_semp_legacy_timeout_enabled = None
        self._service_semp_plain_text_enabled = None
        self._service_semp_plain_text_listen_port = None
        self._service_semp_tls_enabled = None
        self._service_semp_tls_listen_port = None
        self._service_smf_compression_listen_port = None
        self._service_smf_enabled = None
        self._service_smf_event_connection_count_threshold = None
        self._service_smf_plain_text_listen_port = None
        self._service_smf_routing_control_listen_port = None
        self._service_smf_tls_listen_port = None
        self._service_tls_event_connection_count_threshold = None
        self._service_web_transport_enabled = None
        self._service_web_transport_plain_text_listen_port = None
        self._service_web_transport_tls_listen_port = None
        self._service_web_transport_web_url_suffix = None
        self._tls_block_version11_enabled = None
        self._tls_cipher_suite_management_default_list = None
        self._tls_cipher_suite_management_list = None
        self._tls_cipher_suite_management_supported_list = None
        self._tls_cipher_suite_msg_backbone_default_list = None
        self._tls_cipher_suite_msg_backbone_list = None
        self._tls_cipher_suite_msg_backbone_supported_list = None
        self._tls_cipher_suite_secure_shell_default_list = None
        self._tls_cipher_suite_secure_shell_list = None
        self._tls_cipher_suite_secure_shell_supported_list = None
        self._tls_crime_exploit_protection_enabled = None
        self._tls_ticket_lifetime = None
        self._tls_version_supported_list = None
        self._tx_byte_count = None
        self._tx_byte_rate = None
        self._tx_compressed_byte_count = None
        self._tx_compressed_byte_rate = None
        self._tx_compression_ratio = None
        self._tx_msg_count = None
        self._tx_msg_rate = None
        self._tx_uncompressed_byte_count = None
        self._tx_uncompressed_byte_rate = None
        self.discriminator = None

        if auth_client_cert_revocation_check_mode is not None:
            self.auth_client_cert_revocation_check_mode = auth_client_cert_revocation_check_mode
        if average_rx_byte_rate is not None:
            self.average_rx_byte_rate = average_rx_byte_rate
        if average_rx_compressed_byte_rate is not None:
            self.average_rx_compressed_byte_rate = average_rx_compressed_byte_rate
        if average_rx_msg_rate is not None:
            self.average_rx_msg_rate = average_rx_msg_rate
        if average_rx_uncompressed_byte_rate is not None:
            self.average_rx_uncompressed_byte_rate = average_rx_uncompressed_byte_rate
        if average_tx_byte_rate is not None:
            self.average_tx_byte_rate = average_tx_byte_rate
        if average_tx_compressed_byte_rate is not None:
            self.average_tx_compressed_byte_rate = average_tx_compressed_byte_rate
        if average_tx_msg_rate is not None:
            self.average_tx_msg_rate = average_tx_msg_rate
        if average_tx_uncompressed_byte_rate is not None:
            self.average_tx_uncompressed_byte_rate = average_tx_uncompressed_byte_rate
        if cspf_version is not None:
            self.cspf_version = cspf_version
        if guaranteed_msging_defragmentation_estimated_fragmentation is not None:
            self.guaranteed_msging_defragmentation_estimated_fragmentation = guaranteed_msging_defragmentation_estimated_fragmentation
        if guaranteed_msging_defragmentation_estimated_recoverable_space is not None:
            self.guaranteed_msging_defragmentation_estimated_recoverable_space = guaranteed_msging_defragmentation_estimated_recoverable_space
        if guaranteed_msging_defragmentation_last_completed_on is not None:
            self.guaranteed_msging_defragmentation_last_completed_on = guaranteed_msging_defragmentation_last_completed_on
        if guaranteed_msging_defragmentation_last_completion_percentage is not None:
            self.guaranteed_msging_defragmentation_last_completion_percentage = guaranteed_msging_defragmentation_last_completion_percentage
        if guaranteed_msging_defragmentation_last_exit_condition is not None:
            self.guaranteed_msging_defragmentation_last_exit_condition = guaranteed_msging_defragmentation_last_exit_condition
        if guaranteed_msging_defragmentation_last_exit_condition_information is not None:
            self.guaranteed_msging_defragmentation_last_exit_condition_information = guaranteed_msging_defragmentation_last_exit_condition_information
        if guaranteed_msging_defragmentation_status is not None:
            self.guaranteed_msging_defragmentation_status = guaranteed_msging_defragmentation_status
        if guaranteed_msging_defragmentation_status_active_completion_percentage is not None:
            self.guaranteed_msging_defragmentation_status_active_completion_percentage = guaranteed_msging_defragmentation_status_active_completion_percentage
        if guaranteed_msging_enabled is not None:
            self.guaranteed_msging_enabled = guaranteed_msging_enabled
        if guaranteed_msging_event_cache_usage_threshold is not None:
            self.guaranteed_msging_event_cache_usage_threshold = guaranteed_msging_event_cache_usage_threshold
        if guaranteed_msging_event_delivered_unacked_threshold is not None:
            self.guaranteed_msging_event_delivered_unacked_threshold = guaranteed_msging_event_delivered_unacked_threshold
        if guaranteed_msging_event_disk_usage_threshold is not None:
            self.guaranteed_msging_event_disk_usage_threshold = guaranteed_msging_event_disk_usage_threshold
        if guaranteed_msging_event_egress_flow_count_threshold is not None:
            self.guaranteed_msging_event_egress_flow_count_threshold = guaranteed_msging_event_egress_flow_count_threshold
        if guaranteed_msging_event_endpoint_count_threshold is not None:
            self.guaranteed_msging_event_endpoint_count_threshold = guaranteed_msging_event_endpoint_count_threshold
        if guaranteed_msging_event_ingress_flow_count_threshold is not None:
            self.guaranteed_msging_event_ingress_flow_count_threshold = guaranteed_msging_event_ingress_flow_count_threshold
        if guaranteed_msging_event_msg_count_threshold is not None:
            self.guaranteed_msging_event_msg_count_threshold = guaranteed_msging_event_msg_count_threshold
        if guaranteed_msging_event_msg_spool_file_count_threshold is not None:
            self.guaranteed_msging_event_msg_spool_file_count_threshold = guaranteed_msging_event_msg_spool_file_count_threshold
        if guaranteed_msging_event_msg_spool_usage_threshold is not None:
            self.guaranteed_msging_event_msg_spool_usage_threshold = guaranteed_msging_event_msg_spool_usage_threshold
        if guaranteed_msging_event_transacted_session_count_threshold is not None:
            self.guaranteed_msging_event_transacted_session_count_threshold = guaranteed_msging_event_transacted_session_count_threshold
        if guaranteed_msging_event_transacted_session_resource_count_threshold is not None:
            self.guaranteed_msging_event_transacted_session_resource_count_threshold = guaranteed_msging_event_transacted_session_resource_count_threshold
        if guaranteed_msging_event_transaction_count_threshold is not None:
            self.guaranteed_msging_event_transaction_count_threshold = guaranteed_msging_event_transaction_count_threshold
        if guaranteed_msging_max_cache_usage is not None:
            self.guaranteed_msging_max_cache_usage = guaranteed_msging_max_cache_usage
        if guaranteed_msging_max_msg_spool_usage is not None:
            self.guaranteed_msging_max_msg_spool_usage = guaranteed_msging_max_msg_spool_usage
        if guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout is not None:
            self.guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout = guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout
        if guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout is not None:
            self.guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout = guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout
        if guaranteed_msging_operational_status is not None:
            self.guaranteed_msging_operational_status = guaranteed_msging_operational_status
        if guaranteed_msging_transaction_replication_compatibility_mode is not None:
            self.guaranteed_msging_transaction_replication_compatibility_mode = guaranteed_msging_transaction_replication_compatibility_mode
        if rx_byte_count is not None:
            self.rx_byte_count = rx_byte_count
        if rx_byte_rate is not None:
            self.rx_byte_rate = rx_byte_rate
        if rx_compressed_byte_count is not None:
            self.rx_compressed_byte_count = rx_compressed_byte_count
        if rx_compressed_byte_rate is not None:
            self.rx_compressed_byte_rate = rx_compressed_byte_rate
        if rx_compression_ratio is not None:
            self.rx_compression_ratio = rx_compression_ratio
        if rx_msg_count is not None:
            self.rx_msg_count = rx_msg_count
        if rx_msg_rate is not None:
            self.rx_msg_rate = rx_msg_rate
        if rx_uncompressed_byte_count is not None:
            self.rx_uncompressed_byte_count = rx_uncompressed_byte_count
        if rx_uncompressed_byte_rate is not None:
            self.rx_uncompressed_byte_rate = rx_uncompressed_byte_rate
        if service_amqp_enabled is not None:
            self.service_amqp_enabled = service_amqp_enabled
        if service_amqp_tls_listen_port is not None:
            self.service_amqp_tls_listen_port = service_amqp_tls_listen_port
        if service_event_connection_count_threshold is not None:
            self.service_event_connection_count_threshold = service_event_connection_count_threshold
        if service_health_check_enabled is not None:
            self.service_health_check_enabled = service_health_check_enabled
        if service_health_check_listen_port is not None:
            self.service_health_check_listen_port = service_health_check_listen_port
        if service_mate_link_enabled is not None:
            self.service_mate_link_enabled = service_mate_link_enabled
        if service_mate_link_listen_port is not None:
            self.service_mate_link_listen_port = service_mate_link_listen_port
        if service_mqtt_enabled is not None:
            self.service_mqtt_enabled = service_mqtt_enabled
        if service_msg_backbone_enabled is not None:
            self.service_msg_backbone_enabled = service_msg_backbone_enabled
        if service_redundancy_enabled is not None:
            self.service_redundancy_enabled = service_redundancy_enabled
        if service_redundancy_first_listen_port is not None:
            self.service_redundancy_first_listen_port = service_redundancy_first_listen_port
        if service_rest_event_outgoing_connection_count_threshold is not None:
            self.service_rest_event_outgoing_connection_count_threshold = service_rest_event_outgoing_connection_count_threshold
        if service_rest_incoming_enabled is not None:
            self.service_rest_incoming_enabled = service_rest_incoming_enabled
        if service_rest_outgoing_enabled is not None:
            self.service_rest_outgoing_enabled = service_rest_outgoing_enabled
        if service_semp_legacy_timeout_enabled is not None:
            self.service_semp_legacy_timeout_enabled = service_semp_legacy_timeout_enabled
        if service_semp_plain_text_enabled is not None:
            self.service_semp_plain_text_enabled = service_semp_plain_text_enabled
        if service_semp_plain_text_listen_port is not None:
            self.service_semp_plain_text_listen_port = service_semp_plain_text_listen_port
        if service_semp_tls_enabled is not None:
            self.service_semp_tls_enabled = service_semp_tls_enabled
        if service_semp_tls_listen_port is not None:
            self.service_semp_tls_listen_port = service_semp_tls_listen_port
        if service_smf_compression_listen_port is not None:
            self.service_smf_compression_listen_port = service_smf_compression_listen_port
        if service_smf_enabled is not None:
            self.service_smf_enabled = service_smf_enabled
        if service_smf_event_connection_count_threshold is not None:
            self.service_smf_event_connection_count_threshold = service_smf_event_connection_count_threshold
        if service_smf_plain_text_listen_port is not None:
            self.service_smf_plain_text_listen_port = service_smf_plain_text_listen_port
        if service_smf_routing_control_listen_port is not None:
            self.service_smf_routing_control_listen_port = service_smf_routing_control_listen_port
        if service_smf_tls_listen_port is not None:
            self.service_smf_tls_listen_port = service_smf_tls_listen_port
        if service_tls_event_connection_count_threshold is not None:
            self.service_tls_event_connection_count_threshold = service_tls_event_connection_count_threshold
        if service_web_transport_enabled is not None:
            self.service_web_transport_enabled = service_web_transport_enabled
        if service_web_transport_plain_text_listen_port is not None:
            self.service_web_transport_plain_text_listen_port = service_web_transport_plain_text_listen_port
        if service_web_transport_tls_listen_port is not None:
            self.service_web_transport_tls_listen_port = service_web_transport_tls_listen_port
        if service_web_transport_web_url_suffix is not None:
            self.service_web_transport_web_url_suffix = service_web_transport_web_url_suffix
        if tls_block_version11_enabled is not None:
            self.tls_block_version11_enabled = tls_block_version11_enabled
        if tls_cipher_suite_management_default_list is not None:
            self.tls_cipher_suite_management_default_list = tls_cipher_suite_management_default_list
        if tls_cipher_suite_management_list is not None:
            self.tls_cipher_suite_management_list = tls_cipher_suite_management_list
        if tls_cipher_suite_management_supported_list is not None:
            self.tls_cipher_suite_management_supported_list = tls_cipher_suite_management_supported_list
        if tls_cipher_suite_msg_backbone_default_list is not None:
            self.tls_cipher_suite_msg_backbone_default_list = tls_cipher_suite_msg_backbone_default_list
        if tls_cipher_suite_msg_backbone_list is not None:
            self.tls_cipher_suite_msg_backbone_list = tls_cipher_suite_msg_backbone_list
        if tls_cipher_suite_msg_backbone_supported_list is not None:
            self.tls_cipher_suite_msg_backbone_supported_list = tls_cipher_suite_msg_backbone_supported_list
        if tls_cipher_suite_secure_shell_default_list is not None:
            self.tls_cipher_suite_secure_shell_default_list = tls_cipher_suite_secure_shell_default_list
        if tls_cipher_suite_secure_shell_list is not None:
            self.tls_cipher_suite_secure_shell_list = tls_cipher_suite_secure_shell_list
        if tls_cipher_suite_secure_shell_supported_list is not None:
            self.tls_cipher_suite_secure_shell_supported_list = tls_cipher_suite_secure_shell_supported_list
        if tls_crime_exploit_protection_enabled is not None:
            self.tls_crime_exploit_protection_enabled = tls_crime_exploit_protection_enabled
        if tls_ticket_lifetime is not None:
            self.tls_ticket_lifetime = tls_ticket_lifetime
        if tls_version_supported_list is not None:
            self.tls_version_supported_list = tls_version_supported_list
        if tx_byte_count is not None:
            self.tx_byte_count = tx_byte_count
        if tx_byte_rate is not None:
            self.tx_byte_rate = tx_byte_rate
        if tx_compressed_byte_count is not None:
            self.tx_compressed_byte_count = tx_compressed_byte_count
        if tx_compressed_byte_rate is not None:
            self.tx_compressed_byte_rate = tx_compressed_byte_rate
        if tx_compression_ratio is not None:
            self.tx_compression_ratio = tx_compression_ratio
        if tx_msg_count is not None:
            self.tx_msg_count = tx_msg_count
        if tx_msg_rate is not None:
            self.tx_msg_rate = tx_msg_rate
        if tx_uncompressed_byte_count is not None:
            self.tx_uncompressed_byte_count = tx_uncompressed_byte_count
        if tx_uncompressed_byte_rate is not None:
            self.tx_uncompressed_byte_rate = tx_uncompressed_byte_rate

    @property
    def auth_client_cert_revocation_check_mode(self):
        """Gets the auth_client_cert_revocation_check_mode of this Broker.  # noqa: E501

        The client certificate revocation checking mode used when a client authenticates with a client certificate. The allowed values and their meaning are:  <pre> \"none\" - Do not perform any certificate revocation checking. \"ocsp\" - Use the Open Certificate Status Protcol (OCSP) for certificate revocation checking. \"crl\" - Use Certificate Revocation Lists (CRL) for certificate revocation checking. \"ocsp-crl\" - Use OCSP first, but if OCSP fails to return an unambiguous result, then check via CRL. </pre>   # noqa: E501

        :return: The auth_client_cert_revocation_check_mode of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._auth_client_cert_revocation_check_mode

    @auth_client_cert_revocation_check_mode.setter
    def auth_client_cert_revocation_check_mode(self, auth_client_cert_revocation_check_mode):
        """Sets the auth_client_cert_revocation_check_mode of this Broker.

        The client certificate revocation checking mode used when a client authenticates with a client certificate. The allowed values and their meaning are:  <pre> \"none\" - Do not perform any certificate revocation checking. \"ocsp\" - Use the Open Certificate Status Protcol (OCSP) for certificate revocation checking. \"crl\" - Use Certificate Revocation Lists (CRL) for certificate revocation checking. \"ocsp-crl\" - Use OCSP first, but if OCSP fails to return an unambiguous result, then check via CRL. </pre>   # noqa: E501

        :param auth_client_cert_revocation_check_mode: The auth_client_cert_revocation_check_mode of this Broker.  # noqa: E501
        :type: str
        """
        allowed_values = ["none", "ocsp", "crl", "ocsp-crl"]  # noqa: E501
        if auth_client_cert_revocation_check_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `auth_client_cert_revocation_check_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(auth_client_cert_revocation_check_mode, allowed_values)
            )

        self._auth_client_cert_revocation_check_mode = auth_client_cert_revocation_check_mode

    @property
    def average_rx_byte_rate(self):
        """Gets the average_rx_byte_rate of this Broker.  # noqa: E501

        The one minute average of the message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_rx_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_byte_rate

    @average_rx_byte_rate.setter
    def average_rx_byte_rate(self, average_rx_byte_rate):
        """Sets the average_rx_byte_rate of this Broker.

        The one minute average of the message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_rx_byte_rate: The average_rx_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_rx_byte_rate = average_rx_byte_rate

    @property
    def average_rx_compressed_byte_rate(self):
        """Gets the average_rx_compressed_byte_rate of this Broker.  # noqa: E501

        The one minute average of the compressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_rx_compressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_compressed_byte_rate

    @average_rx_compressed_byte_rate.setter
    def average_rx_compressed_byte_rate(self, average_rx_compressed_byte_rate):
        """Sets the average_rx_compressed_byte_rate of this Broker.

        The one minute average of the compressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_rx_compressed_byte_rate: The average_rx_compressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_rx_compressed_byte_rate = average_rx_compressed_byte_rate

    @property
    def average_rx_msg_rate(self):
        """Gets the average_rx_msg_rate of this Broker.  # noqa: E501

        The one minute average of the message rate received by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :return: The average_rx_msg_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_msg_rate

    @average_rx_msg_rate.setter
    def average_rx_msg_rate(self, average_rx_msg_rate):
        """Sets the average_rx_msg_rate of this Broker.

        The one minute average of the message rate received by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :param average_rx_msg_rate: The average_rx_msg_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_rx_msg_rate = average_rx_msg_rate

    @property
    def average_rx_uncompressed_byte_rate(self):
        """Gets the average_rx_uncompressed_byte_rate of this Broker.  # noqa: E501

        The one minute average of the uncompressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_rx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_uncompressed_byte_rate

    @average_rx_uncompressed_byte_rate.setter
    def average_rx_uncompressed_byte_rate(self, average_rx_uncompressed_byte_rate):
        """Sets the average_rx_uncompressed_byte_rate of this Broker.

        The one minute average of the uncompressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_rx_uncompressed_byte_rate: The average_rx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_rx_uncompressed_byte_rate = average_rx_uncompressed_byte_rate

    @property
    def average_tx_byte_rate(self):
        """Gets the average_tx_byte_rate of this Broker.  # noqa: E501

        The one minute average of the message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_tx_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_byte_rate

    @average_tx_byte_rate.setter
    def average_tx_byte_rate(self, average_tx_byte_rate):
        """Sets the average_tx_byte_rate of this Broker.

        The one minute average of the message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_tx_byte_rate: The average_tx_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_tx_byte_rate = average_tx_byte_rate

    @property
    def average_tx_compressed_byte_rate(self):
        """Gets the average_tx_compressed_byte_rate of this Broker.  # noqa: E501

        The one minute average of the compressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_tx_compressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_compressed_byte_rate

    @average_tx_compressed_byte_rate.setter
    def average_tx_compressed_byte_rate(self, average_tx_compressed_byte_rate):
        """Sets the average_tx_compressed_byte_rate of this Broker.

        The one minute average of the compressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_tx_compressed_byte_rate: The average_tx_compressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_tx_compressed_byte_rate = average_tx_compressed_byte_rate

    @property
    def average_tx_msg_rate(self):
        """Gets the average_tx_msg_rate of this Broker.  # noqa: E501

        The one minute average of the message rate transmitted by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :return: The average_tx_msg_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_msg_rate

    @average_tx_msg_rate.setter
    def average_tx_msg_rate(self, average_tx_msg_rate):
        """Sets the average_tx_msg_rate of this Broker.

        The one minute average of the message rate transmitted by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :param average_tx_msg_rate: The average_tx_msg_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_tx_msg_rate = average_tx_msg_rate

    @property
    def average_tx_uncompressed_byte_rate(self):
        """Gets the average_tx_uncompressed_byte_rate of this Broker.  # noqa: E501

        The one minute average of the uncompressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The average_tx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_uncompressed_byte_rate

    @average_tx_uncompressed_byte_rate.setter
    def average_tx_uncompressed_byte_rate(self, average_tx_uncompressed_byte_rate):
        """Sets the average_tx_uncompressed_byte_rate of this Broker.

        The one minute average of the uncompressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param average_tx_uncompressed_byte_rate: The average_tx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._average_tx_uncompressed_byte_rate = average_tx_uncompressed_byte_rate

    @property
    def cspf_version(self):
        """Gets the cspf_version of this Broker.  # noqa: E501

        The current CSPF version. Available since 2.17.  # noqa: E501

        :return: The cspf_version of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._cspf_version

    @cspf_version.setter
    def cspf_version(self, cspf_version):
        """Sets the cspf_version of this Broker.

        The current CSPF version. Available since 2.17.  # noqa: E501

        :param cspf_version: The cspf_version of this Broker.  # noqa: E501
        :type: int
        """

        self._cspf_version = cspf_version

    @property
    def guaranteed_msging_defragmentation_estimated_fragmentation(self):
        """Gets the guaranteed_msging_defragmentation_estimated_fragmentation of this Broker.  # noqa: E501

        An approximation of the amount of disk space consumed, but not used, by the persisted data. Calculated as a percentage of total space. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_estimated_fragmentation of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_defragmentation_estimated_fragmentation

    @guaranteed_msging_defragmentation_estimated_fragmentation.setter
    def guaranteed_msging_defragmentation_estimated_fragmentation(self, guaranteed_msging_defragmentation_estimated_fragmentation):
        """Sets the guaranteed_msging_defragmentation_estimated_fragmentation of this Broker.

        An approximation of the amount of disk space consumed, but not used, by the persisted data. Calculated as a percentage of total space. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_estimated_fragmentation: The guaranteed_msging_defragmentation_estimated_fragmentation of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_defragmentation_estimated_fragmentation = guaranteed_msging_defragmentation_estimated_fragmentation

    @property
    def guaranteed_msging_defragmentation_estimated_recoverable_space(self):
        """Gets the guaranteed_msging_defragmentation_estimated_recoverable_space of this Broker.  # noqa: E501

        An approximation of the amount of disk space recovered upon a successfully completed execution of a defragmentation operation. Expressed in MB. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_estimated_recoverable_space of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_defragmentation_estimated_recoverable_space

    @guaranteed_msging_defragmentation_estimated_recoverable_space.setter
    def guaranteed_msging_defragmentation_estimated_recoverable_space(self, guaranteed_msging_defragmentation_estimated_recoverable_space):
        """Sets the guaranteed_msging_defragmentation_estimated_recoverable_space of this Broker.

        An approximation of the amount of disk space recovered upon a successfully completed execution of a defragmentation operation. Expressed in MB. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_estimated_recoverable_space: The guaranteed_msging_defragmentation_estimated_recoverable_space of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_defragmentation_estimated_recoverable_space = guaranteed_msging_defragmentation_estimated_recoverable_space

    @property
    def guaranteed_msging_defragmentation_last_completed_on(self):
        """Gets the guaranteed_msging_defragmentation_last_completed_on of this Broker.  # noqa: E501

        A timestamp reflecting when the last defragmentation completed. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time). Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_last_completed_on of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_defragmentation_last_completed_on

    @guaranteed_msging_defragmentation_last_completed_on.setter
    def guaranteed_msging_defragmentation_last_completed_on(self, guaranteed_msging_defragmentation_last_completed_on):
        """Sets the guaranteed_msging_defragmentation_last_completed_on of this Broker.

        A timestamp reflecting when the last defragmentation completed. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time). Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_last_completed_on: The guaranteed_msging_defragmentation_last_completed_on of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_defragmentation_last_completed_on = guaranteed_msging_defragmentation_last_completed_on

    @property
    def guaranteed_msging_defragmentation_last_completion_percentage(self):
        """Gets the guaranteed_msging_defragmentation_last_completion_percentage of this Broker.  # noqa: E501

        How much of the message spool was visited during the last defragmentation operation. This number reflects the percentage of the message spool visited in terms of disk space (as opposed to, for example, spool files). Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_last_completion_percentage of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_defragmentation_last_completion_percentage

    @guaranteed_msging_defragmentation_last_completion_percentage.setter
    def guaranteed_msging_defragmentation_last_completion_percentage(self, guaranteed_msging_defragmentation_last_completion_percentage):
        """Sets the guaranteed_msging_defragmentation_last_completion_percentage of this Broker.

        How much of the message spool was visited during the last defragmentation operation. This number reflects the percentage of the message spool visited in terms of disk space (as opposed to, for example, spool files). Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_last_completion_percentage: The guaranteed_msging_defragmentation_last_completion_percentage of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_defragmentation_last_completion_percentage = guaranteed_msging_defragmentation_last_completion_percentage

    @property
    def guaranteed_msging_defragmentation_last_exit_condition(self):
        """Gets the guaranteed_msging_defragmentation_last_exit_condition of this Broker.  # noqa: E501

        Reflects how the last defragmentation operation completed. The allowed values and their meaning are:  <pre> \"success\" - Defragmentation completed successfully. \"unmovable-local-transaction\" - Defragmentation stopped after encountering an unmovable local transaction. \"unmovable-xa-transaction\" - Defragmentation stopped after encountering an unmovable XA transaction. \"incomplete\" - Defragmentation stopped prematurely. \"stopped-by-administrator\" - Defragmentation stopped by administrator. </pre>  Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_last_exit_condition of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._guaranteed_msging_defragmentation_last_exit_condition

    @guaranteed_msging_defragmentation_last_exit_condition.setter
    def guaranteed_msging_defragmentation_last_exit_condition(self, guaranteed_msging_defragmentation_last_exit_condition):
        """Sets the guaranteed_msging_defragmentation_last_exit_condition of this Broker.

        Reflects how the last defragmentation operation completed. The allowed values and their meaning are:  <pre> \"success\" - Defragmentation completed successfully. \"unmovable-local-transaction\" - Defragmentation stopped after encountering an unmovable local transaction. \"unmovable-xa-transaction\" - Defragmentation stopped after encountering an unmovable XA transaction. \"incomplete\" - Defragmentation stopped prematurely. \"stopped-by-administrator\" - Defragmentation stopped by administrator. </pre>  Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_last_exit_condition: The guaranteed_msging_defragmentation_last_exit_condition of this Broker.  # noqa: E501
        :type: str
        """

        self._guaranteed_msging_defragmentation_last_exit_condition = guaranteed_msging_defragmentation_last_exit_condition

    @property
    def guaranteed_msging_defragmentation_last_exit_condition_information(self):
        """Gets the guaranteed_msging_defragmentation_last_exit_condition_information of this Broker.  # noqa: E501

        Optional additional information regarding the exit condition of the last defragmentation operation. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_last_exit_condition_information of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._guaranteed_msging_defragmentation_last_exit_condition_information

    @guaranteed_msging_defragmentation_last_exit_condition_information.setter
    def guaranteed_msging_defragmentation_last_exit_condition_information(self, guaranteed_msging_defragmentation_last_exit_condition_information):
        """Sets the guaranteed_msging_defragmentation_last_exit_condition_information of this Broker.

        Optional additional information regarding the exit condition of the last defragmentation operation. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_last_exit_condition_information: The guaranteed_msging_defragmentation_last_exit_condition_information of this Broker.  # noqa: E501
        :type: str
        """

        self._guaranteed_msging_defragmentation_last_exit_condition_information = guaranteed_msging_defragmentation_last_exit_condition_information

    @property
    def guaranteed_msging_defragmentation_status(self):
        """Gets the guaranteed_msging_defragmentation_status of this Broker.  # noqa: E501

        Defragmentation status of guaranteed messaging. The allowed values and their meaning are:  <pre> \"idle\" - Defragmentation is not currently running. \"pending\" - Degfragmentation is preparing to run. \"active\" - Defragmentation is in progress. </pre>  Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_status of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._guaranteed_msging_defragmentation_status

    @guaranteed_msging_defragmentation_status.setter
    def guaranteed_msging_defragmentation_status(self, guaranteed_msging_defragmentation_status):
        """Sets the guaranteed_msging_defragmentation_status of this Broker.

        Defragmentation status of guaranteed messaging. The allowed values and their meaning are:  <pre> \"idle\" - Defragmentation is not currently running. \"pending\" - Degfragmentation is preparing to run. \"active\" - Defragmentation is in progress. </pre>  Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_status: The guaranteed_msging_defragmentation_status of this Broker.  # noqa: E501
        :type: str
        """

        self._guaranteed_msging_defragmentation_status = guaranteed_msging_defragmentation_status

    @property
    def guaranteed_msging_defragmentation_status_active_completion_percentage(self):
        """Gets the guaranteed_msging_defragmentation_status_active_completion_percentage of this Broker.  # noqa: E501

        The estimated completion percentage of a defragmentation operation currently in progress. Only valid if the defragmentation status is \"Active\". Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_defragmentation_status_active_completion_percentage of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_defragmentation_status_active_completion_percentage

    @guaranteed_msging_defragmentation_status_active_completion_percentage.setter
    def guaranteed_msging_defragmentation_status_active_completion_percentage(self, guaranteed_msging_defragmentation_status_active_completion_percentage):
        """Sets the guaranteed_msging_defragmentation_status_active_completion_percentage of this Broker.

        The estimated completion percentage of a defragmentation operation currently in progress. Only valid if the defragmentation status is \"Active\". Available since 2.18.  # noqa: E501

        :param guaranteed_msging_defragmentation_status_active_completion_percentage: The guaranteed_msging_defragmentation_status_active_completion_percentage of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_defragmentation_status_active_completion_percentage = guaranteed_msging_defragmentation_status_active_completion_percentage

    @property
    def guaranteed_msging_enabled(self):
        """Gets the guaranteed_msging_enabled of this Broker.  # noqa: E501

        Enable or disable Guaranteed Messaging. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._guaranteed_msging_enabled

    @guaranteed_msging_enabled.setter
    def guaranteed_msging_enabled(self, guaranteed_msging_enabled):
        """Sets the guaranteed_msging_enabled of this Broker.

        Enable or disable Guaranteed Messaging. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_enabled: The guaranteed_msging_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._guaranteed_msging_enabled = guaranteed_msging_enabled

    @property
    def guaranteed_msging_event_cache_usage_threshold(self):
        """Gets the guaranteed_msging_event_cache_usage_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_cache_usage_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_cache_usage_threshold

    @guaranteed_msging_event_cache_usage_threshold.setter
    def guaranteed_msging_event_cache_usage_threshold(self, guaranteed_msging_event_cache_usage_threshold):
        """Sets the guaranteed_msging_event_cache_usage_threshold of this Broker.


        :param guaranteed_msging_event_cache_usage_threshold: The guaranteed_msging_event_cache_usage_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_cache_usage_threshold = guaranteed_msging_event_cache_usage_threshold

    @property
    def guaranteed_msging_event_delivered_unacked_threshold(self):
        """Gets the guaranteed_msging_event_delivered_unacked_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_delivered_unacked_threshold of this Broker.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._guaranteed_msging_event_delivered_unacked_threshold

    @guaranteed_msging_event_delivered_unacked_threshold.setter
    def guaranteed_msging_event_delivered_unacked_threshold(self, guaranteed_msging_event_delivered_unacked_threshold):
        """Sets the guaranteed_msging_event_delivered_unacked_threshold of this Broker.


        :param guaranteed_msging_event_delivered_unacked_threshold: The guaranteed_msging_event_delivered_unacked_threshold of this Broker.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._guaranteed_msging_event_delivered_unacked_threshold = guaranteed_msging_event_delivered_unacked_threshold

    @property
    def guaranteed_msging_event_disk_usage_threshold(self):
        """Gets the guaranteed_msging_event_disk_usage_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_disk_usage_threshold of this Broker.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._guaranteed_msging_event_disk_usage_threshold

    @guaranteed_msging_event_disk_usage_threshold.setter
    def guaranteed_msging_event_disk_usage_threshold(self, guaranteed_msging_event_disk_usage_threshold):
        """Sets the guaranteed_msging_event_disk_usage_threshold of this Broker.


        :param guaranteed_msging_event_disk_usage_threshold: The guaranteed_msging_event_disk_usage_threshold of this Broker.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._guaranteed_msging_event_disk_usage_threshold = guaranteed_msging_event_disk_usage_threshold

    @property
    def guaranteed_msging_event_egress_flow_count_threshold(self):
        """Gets the guaranteed_msging_event_egress_flow_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_egress_flow_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_egress_flow_count_threshold

    @guaranteed_msging_event_egress_flow_count_threshold.setter
    def guaranteed_msging_event_egress_flow_count_threshold(self, guaranteed_msging_event_egress_flow_count_threshold):
        """Sets the guaranteed_msging_event_egress_flow_count_threshold of this Broker.


        :param guaranteed_msging_event_egress_flow_count_threshold: The guaranteed_msging_event_egress_flow_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_egress_flow_count_threshold = guaranteed_msging_event_egress_flow_count_threshold

    @property
    def guaranteed_msging_event_endpoint_count_threshold(self):
        """Gets the guaranteed_msging_event_endpoint_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_endpoint_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_endpoint_count_threshold

    @guaranteed_msging_event_endpoint_count_threshold.setter
    def guaranteed_msging_event_endpoint_count_threshold(self, guaranteed_msging_event_endpoint_count_threshold):
        """Sets the guaranteed_msging_event_endpoint_count_threshold of this Broker.


        :param guaranteed_msging_event_endpoint_count_threshold: The guaranteed_msging_event_endpoint_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_endpoint_count_threshold = guaranteed_msging_event_endpoint_count_threshold

    @property
    def guaranteed_msging_event_ingress_flow_count_threshold(self):
        """Gets the guaranteed_msging_event_ingress_flow_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_ingress_flow_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_ingress_flow_count_threshold

    @guaranteed_msging_event_ingress_flow_count_threshold.setter
    def guaranteed_msging_event_ingress_flow_count_threshold(self, guaranteed_msging_event_ingress_flow_count_threshold):
        """Sets the guaranteed_msging_event_ingress_flow_count_threshold of this Broker.


        :param guaranteed_msging_event_ingress_flow_count_threshold: The guaranteed_msging_event_ingress_flow_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_ingress_flow_count_threshold = guaranteed_msging_event_ingress_flow_count_threshold

    @property
    def guaranteed_msging_event_msg_count_threshold(self):
        """Gets the guaranteed_msging_event_msg_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_msg_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._guaranteed_msging_event_msg_count_threshold

    @guaranteed_msging_event_msg_count_threshold.setter
    def guaranteed_msging_event_msg_count_threshold(self, guaranteed_msging_event_msg_count_threshold):
        """Sets the guaranteed_msging_event_msg_count_threshold of this Broker.


        :param guaranteed_msging_event_msg_count_threshold: The guaranteed_msging_event_msg_count_threshold of this Broker.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._guaranteed_msging_event_msg_count_threshold = guaranteed_msging_event_msg_count_threshold

    @property
    def guaranteed_msging_event_msg_spool_file_count_threshold(self):
        """Gets the guaranteed_msging_event_msg_spool_file_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_msg_spool_file_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._guaranteed_msging_event_msg_spool_file_count_threshold

    @guaranteed_msging_event_msg_spool_file_count_threshold.setter
    def guaranteed_msging_event_msg_spool_file_count_threshold(self, guaranteed_msging_event_msg_spool_file_count_threshold):
        """Sets the guaranteed_msging_event_msg_spool_file_count_threshold of this Broker.


        :param guaranteed_msging_event_msg_spool_file_count_threshold: The guaranteed_msging_event_msg_spool_file_count_threshold of this Broker.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._guaranteed_msging_event_msg_spool_file_count_threshold = guaranteed_msging_event_msg_spool_file_count_threshold

    @property
    def guaranteed_msging_event_msg_spool_usage_threshold(self):
        """Gets the guaranteed_msging_event_msg_spool_usage_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_msg_spool_usage_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_msg_spool_usage_threshold

    @guaranteed_msging_event_msg_spool_usage_threshold.setter
    def guaranteed_msging_event_msg_spool_usage_threshold(self, guaranteed_msging_event_msg_spool_usage_threshold):
        """Sets the guaranteed_msging_event_msg_spool_usage_threshold of this Broker.


        :param guaranteed_msging_event_msg_spool_usage_threshold: The guaranteed_msging_event_msg_spool_usage_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_msg_spool_usage_threshold = guaranteed_msging_event_msg_spool_usage_threshold

    @property
    def guaranteed_msging_event_transacted_session_count_threshold(self):
        """Gets the guaranteed_msging_event_transacted_session_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_transacted_session_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_transacted_session_count_threshold

    @guaranteed_msging_event_transacted_session_count_threshold.setter
    def guaranteed_msging_event_transacted_session_count_threshold(self, guaranteed_msging_event_transacted_session_count_threshold):
        """Sets the guaranteed_msging_event_transacted_session_count_threshold of this Broker.


        :param guaranteed_msging_event_transacted_session_count_threshold: The guaranteed_msging_event_transacted_session_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_transacted_session_count_threshold = guaranteed_msging_event_transacted_session_count_threshold

    @property
    def guaranteed_msging_event_transacted_session_resource_count_threshold(self):
        """Gets the guaranteed_msging_event_transacted_session_resource_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_transacted_session_resource_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._guaranteed_msging_event_transacted_session_resource_count_threshold

    @guaranteed_msging_event_transacted_session_resource_count_threshold.setter
    def guaranteed_msging_event_transacted_session_resource_count_threshold(self, guaranteed_msging_event_transacted_session_resource_count_threshold):
        """Sets the guaranteed_msging_event_transacted_session_resource_count_threshold of this Broker.


        :param guaranteed_msging_event_transacted_session_resource_count_threshold: The guaranteed_msging_event_transacted_session_resource_count_threshold of this Broker.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._guaranteed_msging_event_transacted_session_resource_count_threshold = guaranteed_msging_event_transacted_session_resource_count_threshold

    @property
    def guaranteed_msging_event_transaction_count_threshold(self):
        """Gets the guaranteed_msging_event_transaction_count_threshold of this Broker.  # noqa: E501


        :return: The guaranteed_msging_event_transaction_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._guaranteed_msging_event_transaction_count_threshold

    @guaranteed_msging_event_transaction_count_threshold.setter
    def guaranteed_msging_event_transaction_count_threshold(self, guaranteed_msging_event_transaction_count_threshold):
        """Sets the guaranteed_msging_event_transaction_count_threshold of this Broker.


        :param guaranteed_msging_event_transaction_count_threshold: The guaranteed_msging_event_transaction_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._guaranteed_msging_event_transaction_count_threshold = guaranteed_msging_event_transaction_count_threshold

    @property
    def guaranteed_msging_max_cache_usage(self):
        """Gets the guaranteed_msging_max_cache_usage of this Broker.  # noqa: E501

        Guaranteed messaging cache usage limit. Expressed as a maximum percentage of the NAB's egress queueing. resources that the guaranteed message cache is allowed to use. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_max_cache_usage of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_max_cache_usage

    @guaranteed_msging_max_cache_usage.setter
    def guaranteed_msging_max_cache_usage(self, guaranteed_msging_max_cache_usage):
        """Sets the guaranteed_msging_max_cache_usage of this Broker.

        Guaranteed messaging cache usage limit. Expressed as a maximum percentage of the NAB's egress queueing. resources that the guaranteed message cache is allowed to use. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_max_cache_usage: The guaranteed_msging_max_cache_usage of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_max_cache_usage = guaranteed_msging_max_cache_usage

    @property
    def guaranteed_msging_max_msg_spool_usage(self):
        """Gets the guaranteed_msging_max_msg_spool_usage of this Broker.  # noqa: E501

        The maximum total message spool usage allowed across all VPNs on this broker, in megabytes. Recommendation: the maximum value should be less than 90% of the disk space allocated for the guaranteed message spool. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_max_msg_spool_usage of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_max_msg_spool_usage

    @guaranteed_msging_max_msg_spool_usage.setter
    def guaranteed_msging_max_msg_spool_usage(self, guaranteed_msging_max_msg_spool_usage):
        """Sets the guaranteed_msging_max_msg_spool_usage of this Broker.

        The maximum total message spool usage allowed across all VPNs on this broker, in megabytes. Recommendation: the maximum value should be less than 90% of the disk space allocated for the guaranteed message spool. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_max_msg_spool_usage: The guaranteed_msging_max_msg_spool_usage of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_max_msg_spool_usage = guaranteed_msging_max_msg_spool_usage

    @property
    def guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout(self):
        """Gets the guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout of this Broker.  # noqa: E501

        The maximum time, in milliseconds, that can be tolerated for remote acknowledgement of synchronization messages before which the remote system will be considered out of sync. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout

    @guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout.setter
    def guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout(self, guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout):
        """Sets the guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout of this Broker.

        The maximum time, in milliseconds, that can be tolerated for remote acknowledgement of synchronization messages before which the remote system will be considered out of sync. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout: The guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout = guaranteed_msging_msg_spool_sync_mirrored_msg_ack_timeout

    @property
    def guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout(self):
        """Gets the guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout of this Broker.  # noqa: E501

        The maximum time, in milliseconds, that can be tolerated for remote disk writes before which the remote system will be considered out of sync. Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout

    @guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout.setter
    def guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout(self, guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout):
        """Sets the guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout of this Broker.

        The maximum time, in milliseconds, that can be tolerated for remote disk writes before which the remote system will be considered out of sync. Available since 2.18.  # noqa: E501

        :param guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout: The guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout of this Broker.  # noqa: E501
        :type: int
        """

        self._guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout = guaranteed_msging_msg_spool_sync_mirrored_spool_file_ack_timeout

    @property
    def guaranteed_msging_operational_status(self):
        """Gets the guaranteed_msging_operational_status of this Broker.  # noqa: E501

        Operational status of guaranteed messaging. The allowed values and their meaning are:  <pre> \"disabled\" - The operational status of guaranteed messaging is Disabled. \"not-ready\" - The operational status of guaranteed messaging is NotReady. \"standby\" - The operational status of guaranteed messaging is Standby. \"activating\" - The operational status of guaranteed messaging is Activating. \"active\" - The operational status of guaranteed messaging is Active. </pre>  Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_operational_status of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._guaranteed_msging_operational_status

    @guaranteed_msging_operational_status.setter
    def guaranteed_msging_operational_status(self, guaranteed_msging_operational_status):
        """Sets the guaranteed_msging_operational_status of this Broker.

        Operational status of guaranteed messaging. The allowed values and their meaning are:  <pre> \"disabled\" - The operational status of guaranteed messaging is Disabled. \"not-ready\" - The operational status of guaranteed messaging is NotReady. \"standby\" - The operational status of guaranteed messaging is Standby. \"activating\" - The operational status of guaranteed messaging is Activating. \"active\" - The operational status of guaranteed messaging is Active. </pre>  Available since 2.18.  # noqa: E501

        :param guaranteed_msging_operational_status: The guaranteed_msging_operational_status of this Broker.  # noqa: E501
        :type: str
        """

        self._guaranteed_msging_operational_status = guaranteed_msging_operational_status

    @property
    def guaranteed_msging_transaction_replication_compatibility_mode(self):
        """Gets the guaranteed_msging_transaction_replication_compatibility_mode of this Broker.  # noqa: E501

        The replication compatibility mode for the router. The default value is `\"legacy\"`. The allowed values and their meaning are:\"legacy\" - All transactions originated by clients are replicated to the standby site without using transactions.\"transacted\" - All transactions originated by clients are replicated to the standby site using transactions. The allowed values and their meaning are:  <pre> \"legacy\" - All transactions originated by clients are replicated to the standby site without using transactions. \"transacted\" - All transactions originated by clients are replicated to the standby site using transactions. </pre>  Available since 2.18.  # noqa: E501

        :return: The guaranteed_msging_transaction_replication_compatibility_mode of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._guaranteed_msging_transaction_replication_compatibility_mode

    @guaranteed_msging_transaction_replication_compatibility_mode.setter
    def guaranteed_msging_transaction_replication_compatibility_mode(self, guaranteed_msging_transaction_replication_compatibility_mode):
        """Sets the guaranteed_msging_transaction_replication_compatibility_mode of this Broker.

        The replication compatibility mode for the router. The default value is `\"legacy\"`. The allowed values and their meaning are:\"legacy\" - All transactions originated by clients are replicated to the standby site without using transactions.\"transacted\" - All transactions originated by clients are replicated to the standby site using transactions. The allowed values and their meaning are:  <pre> \"legacy\" - All transactions originated by clients are replicated to the standby site without using transactions. \"transacted\" - All transactions originated by clients are replicated to the standby site using transactions. </pre>  Available since 2.18.  # noqa: E501

        :param guaranteed_msging_transaction_replication_compatibility_mode: The guaranteed_msging_transaction_replication_compatibility_mode of this Broker.  # noqa: E501
        :type: str
        """
        allowed_values = ["legacy", "transacted"]  # noqa: E501
        if guaranteed_msging_transaction_replication_compatibility_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `guaranteed_msging_transaction_replication_compatibility_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(guaranteed_msging_transaction_replication_compatibility_mode, allowed_values)
            )

        self._guaranteed_msging_transaction_replication_compatibility_mode = guaranteed_msging_transaction_replication_compatibility_mode

    @property
    def rx_byte_count(self):
        """Gets the rx_byte_count of this Broker.  # noqa: E501

        The amount of messages received from clients by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The rx_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_count

    @rx_byte_count.setter
    def rx_byte_count(self, rx_byte_count):
        """Sets the rx_byte_count of this Broker.

        The amount of messages received from clients by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param rx_byte_count: The rx_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_byte_count = rx_byte_count

    @property
    def rx_byte_rate(self):
        """Gets the rx_byte_rate of this Broker.  # noqa: E501

        The current message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The rx_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_rate

    @rx_byte_rate.setter
    def rx_byte_rate(self, rx_byte_rate):
        """Sets the rx_byte_rate of this Broker.

        The current message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param rx_byte_rate: The rx_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_byte_rate = rx_byte_rate

    @property
    def rx_compressed_byte_count(self):
        """Gets the rx_compressed_byte_count of this Broker.  # noqa: E501

        The amount of compressed messages received by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The rx_compressed_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_compressed_byte_count

    @rx_compressed_byte_count.setter
    def rx_compressed_byte_count(self, rx_compressed_byte_count):
        """Sets the rx_compressed_byte_count of this Broker.

        The amount of compressed messages received by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param rx_compressed_byte_count: The rx_compressed_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_compressed_byte_count = rx_compressed_byte_count

    @property
    def rx_compressed_byte_rate(self):
        """Gets the rx_compressed_byte_rate of this Broker.  # noqa: E501

        The current compressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The rx_compressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_compressed_byte_rate

    @rx_compressed_byte_rate.setter
    def rx_compressed_byte_rate(self, rx_compressed_byte_rate):
        """Sets the rx_compressed_byte_rate of this Broker.

        The current compressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param rx_compressed_byte_rate: The rx_compressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_compressed_byte_rate = rx_compressed_byte_rate

    @property
    def rx_compression_ratio(self):
        """Gets the rx_compression_ratio of this Broker.  # noqa: E501

        The compression ratio for messages received by the Broker. Available since 2.14.  # noqa: E501

        :return: The rx_compression_ratio of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._rx_compression_ratio

    @rx_compression_ratio.setter
    def rx_compression_ratio(self, rx_compression_ratio):
        """Sets the rx_compression_ratio of this Broker.

        The compression ratio for messages received by the Broker. Available since 2.14.  # noqa: E501

        :param rx_compression_ratio: The rx_compression_ratio of this Broker.  # noqa: E501
        :type: str
        """

        self._rx_compression_ratio = rx_compression_ratio

    @property
    def rx_msg_count(self):
        """Gets the rx_msg_count of this Broker.  # noqa: E501

        The number of messages received from clients by the Broker. Available since 2.14.  # noqa: E501

        :return: The rx_msg_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_count

    @rx_msg_count.setter
    def rx_msg_count(self, rx_msg_count):
        """Sets the rx_msg_count of this Broker.

        The number of messages received from clients by the Broker. Available since 2.14.  # noqa: E501

        :param rx_msg_count: The rx_msg_count of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_msg_count = rx_msg_count

    @property
    def rx_msg_rate(self):
        """Gets the rx_msg_rate of this Broker.  # noqa: E501

        The current message rate received by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :return: The rx_msg_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_rate

    @rx_msg_rate.setter
    def rx_msg_rate(self, rx_msg_rate):
        """Sets the rx_msg_rate of this Broker.

        The current message rate received by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :param rx_msg_rate: The rx_msg_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_msg_rate = rx_msg_rate

    @property
    def rx_uncompressed_byte_count(self):
        """Gets the rx_uncompressed_byte_count of this Broker.  # noqa: E501

        The amount of uncompressed messages received by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The rx_uncompressed_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_uncompressed_byte_count

    @rx_uncompressed_byte_count.setter
    def rx_uncompressed_byte_count(self, rx_uncompressed_byte_count):
        """Sets the rx_uncompressed_byte_count of this Broker.

        The amount of uncompressed messages received by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param rx_uncompressed_byte_count: The rx_uncompressed_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_uncompressed_byte_count = rx_uncompressed_byte_count

    @property
    def rx_uncompressed_byte_rate(self):
        """Gets the rx_uncompressed_byte_rate of this Broker.  # noqa: E501

        The current uncompressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The rx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._rx_uncompressed_byte_rate

    @rx_uncompressed_byte_rate.setter
    def rx_uncompressed_byte_rate(self, rx_uncompressed_byte_rate):
        """Sets the rx_uncompressed_byte_rate of this Broker.

        The current uncompressed message rate received by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param rx_uncompressed_byte_rate: The rx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._rx_uncompressed_byte_rate = rx_uncompressed_byte_rate

    @property
    def service_amqp_enabled(self):
        """Gets the service_amqp_enabled of this Broker.  # noqa: E501

        Enable or disable the AMQP service. When disabled new AMQP Clients may not connect through the global or per-VPN AMQP listen-ports, and all currently connected AMQP Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :return: The service_amqp_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_enabled

    @service_amqp_enabled.setter
    def service_amqp_enabled(self, service_amqp_enabled):
        """Sets the service_amqp_enabled of this Broker.

        Enable or disable the AMQP service. When disabled new AMQP Clients may not connect through the global or per-VPN AMQP listen-ports, and all currently connected AMQP Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :param service_amqp_enabled: The service_amqp_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_amqp_enabled = service_amqp_enabled

    @property
    def service_amqp_tls_listen_port(self):
        """Gets the service_amqp_tls_listen_port of this Broker.  # noqa: E501

        TCP port number that AMQP clients can use to connect to the broker using raw TCP over TLS. Available since 2.17.  # noqa: E501

        :return: The service_amqp_tls_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_amqp_tls_listen_port

    @service_amqp_tls_listen_port.setter
    def service_amqp_tls_listen_port(self, service_amqp_tls_listen_port):
        """Sets the service_amqp_tls_listen_port of this Broker.

        TCP port number that AMQP clients can use to connect to the broker using raw TCP over TLS. Available since 2.17.  # noqa: E501

        :param service_amqp_tls_listen_port: The service_amqp_tls_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_amqp_tls_listen_port = service_amqp_tls_listen_port

    @property
    def service_event_connection_count_threshold(self):
        """Gets the service_event_connection_count_threshold of this Broker.  # noqa: E501


        :return: The service_event_connection_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._service_event_connection_count_threshold

    @service_event_connection_count_threshold.setter
    def service_event_connection_count_threshold(self, service_event_connection_count_threshold):
        """Sets the service_event_connection_count_threshold of this Broker.


        :param service_event_connection_count_threshold: The service_event_connection_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._service_event_connection_count_threshold = service_event_connection_count_threshold

    @property
    def service_health_check_enabled(self):
        """Gets the service_health_check_enabled of this Broker.  # noqa: E501

        Enable or disable the health-check service. Available since 2.17.  # noqa: E501

        :return: The service_health_check_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_health_check_enabled

    @service_health_check_enabled.setter
    def service_health_check_enabled(self, service_health_check_enabled):
        """Sets the service_health_check_enabled of this Broker.

        Enable or disable the health-check service. Available since 2.17.  # noqa: E501

        :param service_health_check_enabled: The service_health_check_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_health_check_enabled = service_health_check_enabled

    @property
    def service_health_check_listen_port(self):
        """Gets the service_health_check_listen_port of this Broker.  # noqa: E501

        The port number for the health-check service. The port must be unique across the message backbone. The health-check service must be disabled to change the port. Available since 2.17.  # noqa: E501

        :return: The service_health_check_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_health_check_listen_port

    @service_health_check_listen_port.setter
    def service_health_check_listen_port(self, service_health_check_listen_port):
        """Sets the service_health_check_listen_port of this Broker.

        The port number for the health-check service. The port must be unique across the message backbone. The health-check service must be disabled to change the port. Available since 2.17.  # noqa: E501

        :param service_health_check_listen_port: The service_health_check_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_health_check_listen_port = service_health_check_listen_port

    @property
    def service_mate_link_enabled(self):
        """Gets the service_mate_link_enabled of this Broker.  # noqa: E501

        Enable or disable the mate-link service. Available since 2.17.  # noqa: E501

        :return: The service_mate_link_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_mate_link_enabled

    @service_mate_link_enabled.setter
    def service_mate_link_enabled(self, service_mate_link_enabled):
        """Sets the service_mate_link_enabled of this Broker.

        Enable or disable the mate-link service. Available since 2.17.  # noqa: E501

        :param service_mate_link_enabled: The service_mate_link_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_mate_link_enabled = service_mate_link_enabled

    @property
    def service_mate_link_listen_port(self):
        """Gets the service_mate_link_listen_port of this Broker.  # noqa: E501

        The port number for the mate-link service. The port must be unique across the message backbone. The mate-link service must be disabled to change the port. Available since 2.17.  # noqa: E501

        :return: The service_mate_link_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_mate_link_listen_port

    @service_mate_link_listen_port.setter
    def service_mate_link_listen_port(self, service_mate_link_listen_port):
        """Sets the service_mate_link_listen_port of this Broker.

        The port number for the mate-link service. The port must be unique across the message backbone. The mate-link service must be disabled to change the port. Available since 2.17.  # noqa: E501

        :param service_mate_link_listen_port: The service_mate_link_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_mate_link_listen_port = service_mate_link_listen_port

    @property
    def service_mqtt_enabled(self):
        """Gets the service_mqtt_enabled of this Broker.  # noqa: E501

        Enable or disable the MQTT service. When disabled new MQTT Clients may not connect through the per-VPN MQTT listen-ports, and all currently connected MQTT Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :return: The service_mqtt_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_enabled

    @service_mqtt_enabled.setter
    def service_mqtt_enabled(self, service_mqtt_enabled):
        """Sets the service_mqtt_enabled of this Broker.

        Enable or disable the MQTT service. When disabled new MQTT Clients may not connect through the per-VPN MQTT listen-ports, and all currently connected MQTT Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :param service_mqtt_enabled: The service_mqtt_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_enabled = service_mqtt_enabled

    @property
    def service_msg_backbone_enabled(self):
        """Gets the service_msg_backbone_enabled of this Broker.  # noqa: E501

        Enable or disable the msg-backbone service. When disabled new Clients may not connect through global or per-VPN listen-ports, and all currently connected Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :return: The service_msg_backbone_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_msg_backbone_enabled

    @service_msg_backbone_enabled.setter
    def service_msg_backbone_enabled(self, service_msg_backbone_enabled):
        """Sets the service_msg_backbone_enabled of this Broker.

        Enable or disable the msg-backbone service. When disabled new Clients may not connect through global or per-VPN listen-ports, and all currently connected Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :param service_msg_backbone_enabled: The service_msg_backbone_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_msg_backbone_enabled = service_msg_backbone_enabled

    @property
    def service_redundancy_enabled(self):
        """Gets the service_redundancy_enabled of this Broker.  # noqa: E501

        Enable or disable the redundancy service. Available since 2.17.  # noqa: E501

        :return: The service_redundancy_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_redundancy_enabled

    @service_redundancy_enabled.setter
    def service_redundancy_enabled(self, service_redundancy_enabled):
        """Sets the service_redundancy_enabled of this Broker.

        Enable or disable the redundancy service. Available since 2.17.  # noqa: E501

        :param service_redundancy_enabled: The service_redundancy_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_redundancy_enabled = service_redundancy_enabled

    @property
    def service_redundancy_first_listen_port(self):
        """Gets the service_redundancy_first_listen_port of this Broker.  # noqa: E501

        The first listen-port used for the redundancy service. Redundancy uses this port and the subsequent 2 ports. These port must be unique across the message backbone. The redundancy service must be disabled to change this port. Available since 2.17.  # noqa: E501

        :return: The service_redundancy_first_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_redundancy_first_listen_port

    @service_redundancy_first_listen_port.setter
    def service_redundancy_first_listen_port(self, service_redundancy_first_listen_port):
        """Sets the service_redundancy_first_listen_port of this Broker.

        The first listen-port used for the redundancy service. Redundancy uses this port and the subsequent 2 ports. These port must be unique across the message backbone. The redundancy service must be disabled to change this port. Available since 2.17.  # noqa: E501

        :param service_redundancy_first_listen_port: The service_redundancy_first_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_redundancy_first_listen_port = service_redundancy_first_listen_port

    @property
    def service_rest_event_outgoing_connection_count_threshold(self):
        """Gets the service_rest_event_outgoing_connection_count_threshold of this Broker.  # noqa: E501


        :return: The service_rest_event_outgoing_connection_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._service_rest_event_outgoing_connection_count_threshold

    @service_rest_event_outgoing_connection_count_threshold.setter
    def service_rest_event_outgoing_connection_count_threshold(self, service_rest_event_outgoing_connection_count_threshold):
        """Sets the service_rest_event_outgoing_connection_count_threshold of this Broker.


        :param service_rest_event_outgoing_connection_count_threshold: The service_rest_event_outgoing_connection_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._service_rest_event_outgoing_connection_count_threshold = service_rest_event_outgoing_connection_count_threshold

    @property
    def service_rest_incoming_enabled(self):
        """Gets the service_rest_incoming_enabled of this Broker.  # noqa: E501

        Enable or disable the REST service incoming connections on the router. Available since 2.17.  # noqa: E501

        :return: The service_rest_incoming_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_enabled

    @service_rest_incoming_enabled.setter
    def service_rest_incoming_enabled(self, service_rest_incoming_enabled):
        """Sets the service_rest_incoming_enabled of this Broker.

        Enable or disable the REST service incoming connections on the router. Available since 2.17.  # noqa: E501

        :param service_rest_incoming_enabled: The service_rest_incoming_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_enabled = service_rest_incoming_enabled

    @property
    def service_rest_outgoing_enabled(self):
        """Gets the service_rest_outgoing_enabled of this Broker.  # noqa: E501

        Enable or disable the REST service outgoing connections on the router. Available since 2.17.  # noqa: E501

        :return: The service_rest_outgoing_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_outgoing_enabled

    @service_rest_outgoing_enabled.setter
    def service_rest_outgoing_enabled(self, service_rest_outgoing_enabled):
        """Sets the service_rest_outgoing_enabled of this Broker.

        Enable or disable the REST service outgoing connections on the router. Available since 2.17.  # noqa: E501

        :param service_rest_outgoing_enabled: The service_rest_outgoing_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_rest_outgoing_enabled = service_rest_outgoing_enabled

    @property
    def service_semp_legacy_timeout_enabled(self):
        """Gets the service_semp_legacy_timeout_enabled of this Broker.  # noqa: E501

        Enable or disable extended SEMP timeouts for paged GETs. When a request times out, it returns the current page of content, even if the page is not full.  When enabled, the timeout is 60 seconds. When disabled, the timeout is 5 seconds.  The recommended setting is disabled (no legacy-timeout).  This parameter is intended as a temporary workaround to be used until SEMP clients can handle short pages.  This setting will be removed in a future release. Available since 2.18.  # noqa: E501

        :return: The service_semp_legacy_timeout_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_semp_legacy_timeout_enabled

    @service_semp_legacy_timeout_enabled.setter
    def service_semp_legacy_timeout_enabled(self, service_semp_legacy_timeout_enabled):
        """Sets the service_semp_legacy_timeout_enabled of this Broker.

        Enable or disable extended SEMP timeouts for paged GETs. When a request times out, it returns the current page of content, even if the page is not full.  When enabled, the timeout is 60 seconds. When disabled, the timeout is 5 seconds.  The recommended setting is disabled (no legacy-timeout).  This parameter is intended as a temporary workaround to be used until SEMP clients can handle short pages.  This setting will be removed in a future release. Available since 2.18.  # noqa: E501

        :param service_semp_legacy_timeout_enabled: The service_semp_legacy_timeout_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_semp_legacy_timeout_enabled = service_semp_legacy_timeout_enabled

    @property
    def service_semp_plain_text_enabled(self):
        """Gets the service_semp_plain_text_enabled of this Broker.  # noqa: E501

        Enable or disable plain-text SEMP service. Available since 2.17.  # noqa: E501

        :return: The service_semp_plain_text_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_semp_plain_text_enabled

    @service_semp_plain_text_enabled.setter
    def service_semp_plain_text_enabled(self, service_semp_plain_text_enabled):
        """Sets the service_semp_plain_text_enabled of this Broker.

        Enable or disable plain-text SEMP service. Available since 2.17.  # noqa: E501

        :param service_semp_plain_text_enabled: The service_semp_plain_text_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_semp_plain_text_enabled = service_semp_plain_text_enabled

    @property
    def service_semp_plain_text_listen_port(self):
        """Gets the service_semp_plain_text_listen_port of this Broker.  # noqa: E501

        The TCP port for plain-text SEMP client connections. Available since 2.17.  # noqa: E501

        :return: The service_semp_plain_text_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_semp_plain_text_listen_port

    @service_semp_plain_text_listen_port.setter
    def service_semp_plain_text_listen_port(self, service_semp_plain_text_listen_port):
        """Sets the service_semp_plain_text_listen_port of this Broker.

        The TCP port for plain-text SEMP client connections. Available since 2.17.  # noqa: E501

        :param service_semp_plain_text_listen_port: The service_semp_plain_text_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_semp_plain_text_listen_port = service_semp_plain_text_listen_port

    @property
    def service_semp_tls_enabled(self):
        """Gets the service_semp_tls_enabled of this Broker.  # noqa: E501

        Enable or disable TLS SEMP service. Available since 2.17.  # noqa: E501

        :return: The service_semp_tls_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_semp_tls_enabled

    @service_semp_tls_enabled.setter
    def service_semp_tls_enabled(self, service_semp_tls_enabled):
        """Sets the service_semp_tls_enabled of this Broker.

        Enable or disable TLS SEMP service. Available since 2.17.  # noqa: E501

        :param service_semp_tls_enabled: The service_semp_tls_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_semp_tls_enabled = service_semp_tls_enabled

    @property
    def service_semp_tls_listen_port(self):
        """Gets the service_semp_tls_listen_port of this Broker.  # noqa: E501

        The TCP port for TLS SEMP client connections. Available since 2.17.  # noqa: E501

        :return: The service_semp_tls_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_semp_tls_listen_port

    @service_semp_tls_listen_port.setter
    def service_semp_tls_listen_port(self, service_semp_tls_listen_port):
        """Sets the service_semp_tls_listen_port of this Broker.

        The TCP port for TLS SEMP client connections. Available since 2.17.  # noqa: E501

        :param service_semp_tls_listen_port: The service_semp_tls_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_semp_tls_listen_port = service_semp_tls_listen_port

    @property
    def service_smf_compression_listen_port(self):
        """Gets the service_smf_compression_listen_port of this Broker.  # noqa: E501

        TCP port number that SMF clients can use to connect to the broker using raw compression TCP. Available since 2.17.  # noqa: E501

        :return: The service_smf_compression_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_compression_listen_port

    @service_smf_compression_listen_port.setter
    def service_smf_compression_listen_port(self, service_smf_compression_listen_port):
        """Sets the service_smf_compression_listen_port of this Broker.

        TCP port number that SMF clients can use to connect to the broker using raw compression TCP. Available since 2.17.  # noqa: E501

        :param service_smf_compression_listen_port: The service_smf_compression_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_smf_compression_listen_port = service_smf_compression_listen_port

    @property
    def service_smf_enabled(self):
        """Gets the service_smf_enabled of this Broker.  # noqa: E501

        Enable or disable the SMF service. When disabled new SMF Clients may not connect through the global listen-ports, and all currently connected SMF Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :return: The service_smf_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_smf_enabled

    @service_smf_enabled.setter
    def service_smf_enabled(self, service_smf_enabled):
        """Sets the service_smf_enabled of this Broker.

        Enable or disable the SMF service. When disabled new SMF Clients may not connect through the global listen-ports, and all currently connected SMF Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :param service_smf_enabled: The service_smf_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_smf_enabled = service_smf_enabled

    @property
    def service_smf_event_connection_count_threshold(self):
        """Gets the service_smf_event_connection_count_threshold of this Broker.  # noqa: E501


        :return: The service_smf_event_connection_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._service_smf_event_connection_count_threshold

    @service_smf_event_connection_count_threshold.setter
    def service_smf_event_connection_count_threshold(self, service_smf_event_connection_count_threshold):
        """Sets the service_smf_event_connection_count_threshold of this Broker.


        :param service_smf_event_connection_count_threshold: The service_smf_event_connection_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._service_smf_event_connection_count_threshold = service_smf_event_connection_count_threshold

    @property
    def service_smf_plain_text_listen_port(self):
        """Gets the service_smf_plain_text_listen_port of this Broker.  # noqa: E501

        TCP port number that SMF clients can use to connect to the broker using raw TCP. Available since 2.17.  # noqa: E501

        :return: The service_smf_plain_text_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_plain_text_listen_port

    @service_smf_plain_text_listen_port.setter
    def service_smf_plain_text_listen_port(self, service_smf_plain_text_listen_port):
        """Sets the service_smf_plain_text_listen_port of this Broker.

        TCP port number that SMF clients can use to connect to the broker using raw TCP. Available since 2.17.  # noqa: E501

        :param service_smf_plain_text_listen_port: The service_smf_plain_text_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_smf_plain_text_listen_port = service_smf_plain_text_listen_port

    @property
    def service_smf_routing_control_listen_port(self):
        """Gets the service_smf_routing_control_listen_port of this Broker.  # noqa: E501

        TCP port number that SMF clients can use to connect to the broker using raw routing control TCP. Available since 2.17.  # noqa: E501

        :return: The service_smf_routing_control_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_routing_control_listen_port

    @service_smf_routing_control_listen_port.setter
    def service_smf_routing_control_listen_port(self, service_smf_routing_control_listen_port):
        """Sets the service_smf_routing_control_listen_port of this Broker.

        TCP port number that SMF clients can use to connect to the broker using raw routing control TCP. Available since 2.17.  # noqa: E501

        :param service_smf_routing_control_listen_port: The service_smf_routing_control_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_smf_routing_control_listen_port = service_smf_routing_control_listen_port

    @property
    def service_smf_tls_listen_port(self):
        """Gets the service_smf_tls_listen_port of this Broker.  # noqa: E501

        TCP port number that SMF clients can use to connect to the broker using raw TCP over TLS. Available since 2.17.  # noqa: E501

        :return: The service_smf_tls_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_tls_listen_port

    @service_smf_tls_listen_port.setter
    def service_smf_tls_listen_port(self, service_smf_tls_listen_port):
        """Sets the service_smf_tls_listen_port of this Broker.

        TCP port number that SMF clients can use to connect to the broker using raw TCP over TLS. Available since 2.17.  # noqa: E501

        :param service_smf_tls_listen_port: The service_smf_tls_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_smf_tls_listen_port = service_smf_tls_listen_port

    @property
    def service_tls_event_connection_count_threshold(self):
        """Gets the service_tls_event_connection_count_threshold of this Broker.  # noqa: E501


        :return: The service_tls_event_connection_count_threshold of this Broker.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._service_tls_event_connection_count_threshold

    @service_tls_event_connection_count_threshold.setter
    def service_tls_event_connection_count_threshold(self, service_tls_event_connection_count_threshold):
        """Sets the service_tls_event_connection_count_threshold of this Broker.


        :param service_tls_event_connection_count_threshold: The service_tls_event_connection_count_threshold of this Broker.  # noqa: E501
        :type: EventThreshold
        """

        self._service_tls_event_connection_count_threshold = service_tls_event_connection_count_threshold

    @property
    def service_web_transport_enabled(self):
        """Gets the service_web_transport_enabled of this Broker.  # noqa: E501

        Enable or disable the web-transport service. When disabled new web-transport Clients may not connect through the global listen-ports, and all currently connected web-transport Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :return: The service_web_transport_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._service_web_transport_enabled

    @service_web_transport_enabled.setter
    def service_web_transport_enabled(self, service_web_transport_enabled):
        """Sets the service_web_transport_enabled of this Broker.

        Enable or disable the web-transport service. When disabled new web-transport Clients may not connect through the global listen-ports, and all currently connected web-transport Clients are immediately disconnected. Available since 2.17.  # noqa: E501

        :param service_web_transport_enabled: The service_web_transport_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._service_web_transport_enabled = service_web_transport_enabled

    @property
    def service_web_transport_plain_text_listen_port(self):
        """Gets the service_web_transport_plain_text_listen_port of this Broker.  # noqa: E501

        The TCP port for plain-text WEB client connections. Available since 2.17.  # noqa: E501

        :return: The service_web_transport_plain_text_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_web_transport_plain_text_listen_port

    @service_web_transport_plain_text_listen_port.setter
    def service_web_transport_plain_text_listen_port(self, service_web_transport_plain_text_listen_port):
        """Sets the service_web_transport_plain_text_listen_port of this Broker.

        The TCP port for plain-text WEB client connections. Available since 2.17.  # noqa: E501

        :param service_web_transport_plain_text_listen_port: The service_web_transport_plain_text_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_web_transport_plain_text_listen_port = service_web_transport_plain_text_listen_port

    @property
    def service_web_transport_tls_listen_port(self):
        """Gets the service_web_transport_tls_listen_port of this Broker.  # noqa: E501

        The TCP port for TLS WEB client connections. Available since 2.17.  # noqa: E501

        :return: The service_web_transport_tls_listen_port of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._service_web_transport_tls_listen_port

    @service_web_transport_tls_listen_port.setter
    def service_web_transport_tls_listen_port(self, service_web_transport_tls_listen_port):
        """Sets the service_web_transport_tls_listen_port of this Broker.

        The TCP port for TLS WEB client connections. Available since 2.17.  # noqa: E501

        :param service_web_transport_tls_listen_port: The service_web_transport_tls_listen_port of this Broker.  # noqa: E501
        :type: int
        """

        self._service_web_transport_tls_listen_port = service_web_transport_tls_listen_port

    @property
    def service_web_transport_web_url_suffix(self):
        """Gets the service_web_transport_web_url_suffix of this Broker.  # noqa: E501

        Used to specify the Web URL suffix that will be used by Web clients when communicating with the broker. Available since 2.17.  # noqa: E501

        :return: The service_web_transport_web_url_suffix of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._service_web_transport_web_url_suffix

    @service_web_transport_web_url_suffix.setter
    def service_web_transport_web_url_suffix(self, service_web_transport_web_url_suffix):
        """Sets the service_web_transport_web_url_suffix of this Broker.

        Used to specify the Web URL suffix that will be used by Web clients when communicating with the broker. Available since 2.17.  # noqa: E501

        :param service_web_transport_web_url_suffix: The service_web_transport_web_url_suffix of this Broker.  # noqa: E501
        :type: str
        """

        self._service_web_transport_web_url_suffix = service_web_transport_web_url_suffix

    @property
    def tls_block_version11_enabled(self):
        """Gets the tls_block_version11_enabled of this Broker.  # noqa: E501

        Indicates whether TLS version 1.1 connections are blocked. When blocked, all existing incoming and outgoing TLS 1.1 connections with Clients, SEMP users, and LDAP servers remain connected while new connections are blocked. Note that support for TLS 1.1 will eventually be discontinued, at which time TLS 1.1 connections will be blocked regardless of this setting.  # noqa: E501

        :return: The tls_block_version11_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._tls_block_version11_enabled

    @tls_block_version11_enabled.setter
    def tls_block_version11_enabled(self, tls_block_version11_enabled):
        """Sets the tls_block_version11_enabled of this Broker.

        Indicates whether TLS version 1.1 connections are blocked. When blocked, all existing incoming and outgoing TLS 1.1 connections with Clients, SEMP users, and LDAP servers remain connected while new connections are blocked. Note that support for TLS 1.1 will eventually be discontinued, at which time TLS 1.1 connections will be blocked regardless of this setting.  # noqa: E501

        :param tls_block_version11_enabled: The tls_block_version11_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._tls_block_version11_enabled = tls_block_version11_enabled

    @property
    def tls_cipher_suite_management_default_list(self):
        """Gets the tls_cipher_suite_management_default_list of this Broker.  # noqa: E501

        The colon-separated list of default cipher suites for TLS management connections.  # noqa: E501

        :return: The tls_cipher_suite_management_default_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_management_default_list

    @tls_cipher_suite_management_default_list.setter
    def tls_cipher_suite_management_default_list(self, tls_cipher_suite_management_default_list):
        """Sets the tls_cipher_suite_management_default_list of this Broker.

        The colon-separated list of default cipher suites for TLS management connections.  # noqa: E501

        :param tls_cipher_suite_management_default_list: The tls_cipher_suite_management_default_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_management_default_list = tls_cipher_suite_management_default_list

    @property
    def tls_cipher_suite_management_list(self):
        """Gets the tls_cipher_suite_management_list of this Broker.  # noqa: E501

        The colon-separated list of cipher suites used for TLS management connections (e.g. SEMP, LDAP). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :return: The tls_cipher_suite_management_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_management_list

    @tls_cipher_suite_management_list.setter
    def tls_cipher_suite_management_list(self, tls_cipher_suite_management_list):
        """Sets the tls_cipher_suite_management_list of this Broker.

        The colon-separated list of cipher suites used for TLS management connections (e.g. SEMP, LDAP). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :param tls_cipher_suite_management_list: The tls_cipher_suite_management_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_management_list = tls_cipher_suite_management_list

    @property
    def tls_cipher_suite_management_supported_list(self):
        """Gets the tls_cipher_suite_management_supported_list of this Broker.  # noqa: E501

        The colon-separated list of supported cipher suites for TLS management connections.  # noqa: E501

        :return: The tls_cipher_suite_management_supported_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_management_supported_list

    @tls_cipher_suite_management_supported_list.setter
    def tls_cipher_suite_management_supported_list(self, tls_cipher_suite_management_supported_list):
        """Sets the tls_cipher_suite_management_supported_list of this Broker.

        The colon-separated list of supported cipher suites for TLS management connections.  # noqa: E501

        :param tls_cipher_suite_management_supported_list: The tls_cipher_suite_management_supported_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_management_supported_list = tls_cipher_suite_management_supported_list

    @property
    def tls_cipher_suite_msg_backbone_default_list(self):
        """Gets the tls_cipher_suite_msg_backbone_default_list of this Broker.  # noqa: E501

        The colon-separated list of default cipher suites for TLS data connections.  # noqa: E501

        :return: The tls_cipher_suite_msg_backbone_default_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_msg_backbone_default_list

    @tls_cipher_suite_msg_backbone_default_list.setter
    def tls_cipher_suite_msg_backbone_default_list(self, tls_cipher_suite_msg_backbone_default_list):
        """Sets the tls_cipher_suite_msg_backbone_default_list of this Broker.

        The colon-separated list of default cipher suites for TLS data connections.  # noqa: E501

        :param tls_cipher_suite_msg_backbone_default_list: The tls_cipher_suite_msg_backbone_default_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_msg_backbone_default_list = tls_cipher_suite_msg_backbone_default_list

    @property
    def tls_cipher_suite_msg_backbone_list(self):
        """Gets the tls_cipher_suite_msg_backbone_list of this Broker.  # noqa: E501

        The colon-separated list of cipher suites used for TLS data connections (e.g. client pub/sub). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :return: The tls_cipher_suite_msg_backbone_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_msg_backbone_list

    @tls_cipher_suite_msg_backbone_list.setter
    def tls_cipher_suite_msg_backbone_list(self, tls_cipher_suite_msg_backbone_list):
        """Sets the tls_cipher_suite_msg_backbone_list of this Broker.

        The colon-separated list of cipher suites used for TLS data connections (e.g. client pub/sub). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :param tls_cipher_suite_msg_backbone_list: The tls_cipher_suite_msg_backbone_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_msg_backbone_list = tls_cipher_suite_msg_backbone_list

    @property
    def tls_cipher_suite_msg_backbone_supported_list(self):
        """Gets the tls_cipher_suite_msg_backbone_supported_list of this Broker.  # noqa: E501

        The colon-separated list of supported cipher suites for TLS data connections.  # noqa: E501

        :return: The tls_cipher_suite_msg_backbone_supported_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_msg_backbone_supported_list

    @tls_cipher_suite_msg_backbone_supported_list.setter
    def tls_cipher_suite_msg_backbone_supported_list(self, tls_cipher_suite_msg_backbone_supported_list):
        """Sets the tls_cipher_suite_msg_backbone_supported_list of this Broker.

        The colon-separated list of supported cipher suites for TLS data connections.  # noqa: E501

        :param tls_cipher_suite_msg_backbone_supported_list: The tls_cipher_suite_msg_backbone_supported_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_msg_backbone_supported_list = tls_cipher_suite_msg_backbone_supported_list

    @property
    def tls_cipher_suite_secure_shell_default_list(self):
        """Gets the tls_cipher_suite_secure_shell_default_list of this Broker.  # noqa: E501

        The colon-separated list of default cipher suites for TLS secure shell connections.  # noqa: E501

        :return: The tls_cipher_suite_secure_shell_default_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_secure_shell_default_list

    @tls_cipher_suite_secure_shell_default_list.setter
    def tls_cipher_suite_secure_shell_default_list(self, tls_cipher_suite_secure_shell_default_list):
        """Sets the tls_cipher_suite_secure_shell_default_list of this Broker.

        The colon-separated list of default cipher suites for TLS secure shell connections.  # noqa: E501

        :param tls_cipher_suite_secure_shell_default_list: The tls_cipher_suite_secure_shell_default_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_secure_shell_default_list = tls_cipher_suite_secure_shell_default_list

    @property
    def tls_cipher_suite_secure_shell_list(self):
        """Gets the tls_cipher_suite_secure_shell_list of this Broker.  # noqa: E501

        The colon-separated list of cipher suites used for TLS secure shell connections (e.g. SSH, SFTP, SCP). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :return: The tls_cipher_suite_secure_shell_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_secure_shell_list

    @tls_cipher_suite_secure_shell_list.setter
    def tls_cipher_suite_secure_shell_list(self, tls_cipher_suite_secure_shell_list):
        """Sets the tls_cipher_suite_secure_shell_list of this Broker.

        The colon-separated list of cipher suites used for TLS secure shell connections (e.g. SSH, SFTP, SCP). The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :param tls_cipher_suite_secure_shell_list: The tls_cipher_suite_secure_shell_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_secure_shell_list = tls_cipher_suite_secure_shell_list

    @property
    def tls_cipher_suite_secure_shell_supported_list(self):
        """Gets the tls_cipher_suite_secure_shell_supported_list of this Broker.  # noqa: E501

        The colon-separated list of supported cipher suites for TLS secure shell connections.  # noqa: E501

        :return: The tls_cipher_suite_secure_shell_supported_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_secure_shell_supported_list

    @tls_cipher_suite_secure_shell_supported_list.setter
    def tls_cipher_suite_secure_shell_supported_list(self, tls_cipher_suite_secure_shell_supported_list):
        """Sets the tls_cipher_suite_secure_shell_supported_list of this Broker.

        The colon-separated list of supported cipher suites for TLS secure shell connections.  # noqa: E501

        :param tls_cipher_suite_secure_shell_supported_list: The tls_cipher_suite_secure_shell_supported_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_secure_shell_supported_list = tls_cipher_suite_secure_shell_supported_list

    @property
    def tls_crime_exploit_protection_enabled(self):
        """Gets the tls_crime_exploit_protection_enabled of this Broker.  # noqa: E501

        Indicates whether protection against the CRIME exploit is enabled. When enabled, TLS+compressed messaging performance is degraded. This protection should only be disabled if sufficient ACL and authentication features are being employed such that a potential attacker does not have sufficient access to trigger the exploit.  # noqa: E501

        :return: The tls_crime_exploit_protection_enabled of this Broker.  # noqa: E501
        :rtype: bool
        """
        return self._tls_crime_exploit_protection_enabled

    @tls_crime_exploit_protection_enabled.setter
    def tls_crime_exploit_protection_enabled(self, tls_crime_exploit_protection_enabled):
        """Sets the tls_crime_exploit_protection_enabled of this Broker.

        Indicates whether protection against the CRIME exploit is enabled. When enabled, TLS+compressed messaging performance is degraded. This protection should only be disabled if sufficient ACL and authentication features are being employed such that a potential attacker does not have sufficient access to trigger the exploit.  # noqa: E501

        :param tls_crime_exploit_protection_enabled: The tls_crime_exploit_protection_enabled of this Broker.  # noqa: E501
        :type: bool
        """

        self._tls_crime_exploit_protection_enabled = tls_crime_exploit_protection_enabled

    @property
    def tls_ticket_lifetime(self):
        """Gets the tls_ticket_lifetime of this Broker.  # noqa: E501

        The TLS ticket lifetime in seconds. When a client connects with TLS, a session with a session ticket is created using the TLS ticket lifetime which determines how long the client has to resume the session.  # noqa: E501

        :return: The tls_ticket_lifetime of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tls_ticket_lifetime

    @tls_ticket_lifetime.setter
    def tls_ticket_lifetime(self, tls_ticket_lifetime):
        """Sets the tls_ticket_lifetime of this Broker.

        The TLS ticket lifetime in seconds. When a client connects with TLS, a session with a session ticket is created using the TLS ticket lifetime which determines how long the client has to resume the session.  # noqa: E501

        :param tls_ticket_lifetime: The tls_ticket_lifetime of this Broker.  # noqa: E501
        :type: int
        """

        self._tls_ticket_lifetime = tls_ticket_lifetime

    @property
    def tls_version_supported_list(self):
        """Gets the tls_version_supported_list of this Broker.  # noqa: E501

        The comma-separated list of supported TLS versions.  # noqa: E501

        :return: The tls_version_supported_list of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tls_version_supported_list

    @tls_version_supported_list.setter
    def tls_version_supported_list(self, tls_version_supported_list):
        """Sets the tls_version_supported_list of this Broker.

        The comma-separated list of supported TLS versions.  # noqa: E501

        :param tls_version_supported_list: The tls_version_supported_list of this Broker.  # noqa: E501
        :type: str
        """

        self._tls_version_supported_list = tls_version_supported_list

    @property
    def tx_byte_count(self):
        """Gets the tx_byte_count of this Broker.  # noqa: E501

        The amount of messages transmitted to clients by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The tx_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_count

    @tx_byte_count.setter
    def tx_byte_count(self, tx_byte_count):
        """Sets the tx_byte_count of this Broker.

        The amount of messages transmitted to clients by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param tx_byte_count: The tx_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_byte_count = tx_byte_count

    @property
    def tx_byte_rate(self):
        """Gets the tx_byte_rate of this Broker.  # noqa: E501

        The current message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The tx_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_rate

    @tx_byte_rate.setter
    def tx_byte_rate(self, tx_byte_rate):
        """Sets the tx_byte_rate of this Broker.

        The current message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param tx_byte_rate: The tx_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_byte_rate = tx_byte_rate

    @property
    def tx_compressed_byte_count(self):
        """Gets the tx_compressed_byte_count of this Broker.  # noqa: E501

        The amount of compressed messages transmitted by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The tx_compressed_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_compressed_byte_count

    @tx_compressed_byte_count.setter
    def tx_compressed_byte_count(self, tx_compressed_byte_count):
        """Sets the tx_compressed_byte_count of this Broker.

        The amount of compressed messages transmitted by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param tx_compressed_byte_count: The tx_compressed_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_compressed_byte_count = tx_compressed_byte_count

    @property
    def tx_compressed_byte_rate(self):
        """Gets the tx_compressed_byte_rate of this Broker.  # noqa: E501

        The current compressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The tx_compressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_compressed_byte_rate

    @tx_compressed_byte_rate.setter
    def tx_compressed_byte_rate(self, tx_compressed_byte_rate):
        """Sets the tx_compressed_byte_rate of this Broker.

        The current compressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param tx_compressed_byte_rate: The tx_compressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_compressed_byte_rate = tx_compressed_byte_rate

    @property
    def tx_compression_ratio(self):
        """Gets the tx_compression_ratio of this Broker.  # noqa: E501

        The compression ratio for messages transmitted by the Broker. Available since 2.14.  # noqa: E501

        :return: The tx_compression_ratio of this Broker.  # noqa: E501
        :rtype: str
        """
        return self._tx_compression_ratio

    @tx_compression_ratio.setter
    def tx_compression_ratio(self, tx_compression_ratio):
        """Sets the tx_compression_ratio of this Broker.

        The compression ratio for messages transmitted by the Broker. Available since 2.14.  # noqa: E501

        :param tx_compression_ratio: The tx_compression_ratio of this Broker.  # noqa: E501
        :type: str
        """

        self._tx_compression_ratio = tx_compression_ratio

    @property
    def tx_msg_count(self):
        """Gets the tx_msg_count of this Broker.  # noqa: E501

        The number of messages transmitted to clients by the Broker. Available since 2.14.  # noqa: E501

        :return: The tx_msg_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_count

    @tx_msg_count.setter
    def tx_msg_count(self, tx_msg_count):
        """Sets the tx_msg_count of this Broker.

        The number of messages transmitted to clients by the Broker. Available since 2.14.  # noqa: E501

        :param tx_msg_count: The tx_msg_count of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_msg_count = tx_msg_count

    @property
    def tx_msg_rate(self):
        """Gets the tx_msg_rate of this Broker.  # noqa: E501

        The current message rate transmitted by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :return: The tx_msg_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_rate

    @tx_msg_rate.setter
    def tx_msg_rate(self, tx_msg_rate):
        """Sets the tx_msg_rate of this Broker.

        The current message rate transmitted by the Broker, in messages per second (msg/sec). Available since 2.14.  # noqa: E501

        :param tx_msg_rate: The tx_msg_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_msg_rate = tx_msg_rate

    @property
    def tx_uncompressed_byte_count(self):
        """Gets the tx_uncompressed_byte_count of this Broker.  # noqa: E501

        The amount of uncompressed messages transmitted by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :return: The tx_uncompressed_byte_count of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_uncompressed_byte_count

    @tx_uncompressed_byte_count.setter
    def tx_uncompressed_byte_count(self, tx_uncompressed_byte_count):
        """Sets the tx_uncompressed_byte_count of this Broker.

        The amount of uncompressed messages transmitted by the Broker, in bytes (B). Available since 2.14.  # noqa: E501

        :param tx_uncompressed_byte_count: The tx_uncompressed_byte_count of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_uncompressed_byte_count = tx_uncompressed_byte_count

    @property
    def tx_uncompressed_byte_rate(self):
        """Gets the tx_uncompressed_byte_rate of this Broker.  # noqa: E501

        The current uncompressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :return: The tx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :rtype: int
        """
        return self._tx_uncompressed_byte_rate

    @tx_uncompressed_byte_rate.setter
    def tx_uncompressed_byte_rate(self, tx_uncompressed_byte_rate):
        """Sets the tx_uncompressed_byte_rate of this Broker.

        The current uncompressed message rate transmitted by the Broker, in bytes per second (B/sec). Available since 2.14.  # noqa: E501

        :param tx_uncompressed_byte_rate: The tx_uncompressed_byte_rate of this Broker.  # noqa: E501
        :type: int
        """

        self._tx_uncompressed_byte_rate = tx_uncompressed_byte_rate

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
        if issubclass(Broker, dict):
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
        if not isinstance(other, Broker):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
