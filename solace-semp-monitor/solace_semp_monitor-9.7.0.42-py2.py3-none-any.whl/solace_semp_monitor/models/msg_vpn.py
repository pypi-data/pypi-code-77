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


class MsgVpn(object):
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
        'alias': 'str',
        'authentication_basic_enabled': 'bool',
        'authentication_basic_profile_name': 'str',
        'authentication_basic_radius_domain': 'str',
        'authentication_basic_type': 'str',
        'authentication_client_cert_allow_api_provided_username_enabled': 'bool',
        'authentication_client_cert_enabled': 'bool',
        'authentication_client_cert_max_chain_depth': 'int',
        'authentication_client_cert_revocation_check_mode': 'str',
        'authentication_client_cert_username_source': 'str',
        'authentication_client_cert_validate_date_enabled': 'bool',
        'authentication_kerberos_allow_api_provided_username_enabled': 'bool',
        'authentication_kerberos_enabled': 'bool',
        'authentication_oauth_default_provider_name': 'str',
        'authentication_oauth_enabled': 'bool',
        'authorization_ldap_group_membership_attribute_name': 'str',
        'authorization_ldap_trim_client_username_domain_enabled': 'bool',
        'authorization_profile_name': 'str',
        'authorization_type': 'str',
        'average_rx_byte_rate': 'int',
        'average_rx_compressed_byte_rate': 'int',
        'average_rx_msg_rate': 'int',
        'average_rx_uncompressed_byte_rate': 'int',
        'average_tx_byte_rate': 'int',
        'average_tx_compressed_byte_rate': 'int',
        'average_tx_msg_rate': 'int',
        'average_tx_uncompressed_byte_rate': 'int',
        'bridging_tls_server_cert_enforce_trusted_common_name_enabled': 'bool',
        'bridging_tls_server_cert_max_chain_depth': 'int',
        'bridging_tls_server_cert_validate_date_enabled': 'bool',
        'bridging_tls_server_cert_validate_name_enabled': 'bool',
        'config_sync_local_key': 'str',
        'config_sync_local_last_result': 'str',
        'config_sync_local_role': 'str',
        'config_sync_local_state': 'str',
        'config_sync_local_time_in_state': 'int',
        'control_rx_byte_count': 'int',
        'control_rx_msg_count': 'int',
        'control_tx_byte_count': 'int',
        'control_tx_msg_count': 'int',
        'counter': 'MsgVpnCounter',
        'data_rx_byte_count': 'int',
        'data_rx_msg_count': 'int',
        'data_tx_byte_count': 'int',
        'data_tx_msg_count': 'int',
        'discarded_rx_msg_count': 'int',
        'discarded_tx_msg_count': 'int',
        'distributed_cache_management_enabled': 'bool',
        'dmr_enabled': 'bool',
        'enabled': 'bool',
        'event_connection_count_threshold': 'EventThreshold',
        'event_egress_flow_count_threshold': 'EventThreshold',
        'event_egress_msg_rate_threshold': 'EventThresholdByValue',
        'event_endpoint_count_threshold': 'EventThreshold',
        'event_ingress_flow_count_threshold': 'EventThreshold',
        'event_ingress_msg_rate_threshold': 'EventThresholdByValue',
        'event_large_msg_threshold': 'int',
        'event_log_tag': 'str',
        'event_msg_spool_usage_threshold': 'EventThreshold',
        'event_publish_client_enabled': 'bool',
        'event_publish_msg_vpn_enabled': 'bool',
        'event_publish_subscription_mode': 'str',
        'event_publish_topic_format_mqtt_enabled': 'bool',
        'event_publish_topic_format_smf_enabled': 'bool',
        'event_service_amqp_connection_count_threshold': 'EventThreshold',
        'event_service_mqtt_connection_count_threshold': 'EventThreshold',
        'event_service_rest_incoming_connection_count_threshold': 'EventThreshold',
        'event_service_smf_connection_count_threshold': 'EventThreshold',
        'event_service_web_connection_count_threshold': 'EventThreshold',
        'event_subscription_count_threshold': 'EventThreshold',
        'event_transacted_session_count_threshold': 'EventThreshold',
        'event_transaction_count_threshold': 'EventThreshold',
        'export_subscriptions_enabled': 'bool',
        'failure_reason': 'str',
        'jndi_enabled': 'bool',
        'login_rx_msg_count': 'int',
        'login_tx_msg_count': 'int',
        'max_connection_count': 'int',
        'max_effective_endpoint_count': 'int',
        'max_effective_rx_flow_count': 'int',
        'max_effective_subscription_count': 'int',
        'max_effective_transacted_session_count': 'int',
        'max_effective_transaction_count': 'int',
        'max_effective_tx_flow_count': 'int',
        'max_egress_flow_count': 'int',
        'max_endpoint_count': 'int',
        'max_ingress_flow_count': 'int',
        'max_msg_spool_usage': 'int',
        'max_subscription_count': 'int',
        'max_transacted_session_count': 'int',
        'max_transaction_count': 'int',
        'mqtt_retain_max_memory': 'int',
        'msg_replay_active_count': 'int',
        'msg_replay_failed_count': 'int',
        'msg_replay_initializing_count': 'int',
        'msg_replay_pending_complete_count': 'int',
        'msg_spool_msg_count': 'int',
        'msg_spool_rx_msg_count': 'int',
        'msg_spool_tx_msg_count': 'int',
        'msg_spool_usage': 'int',
        'msg_vpn_name': 'str',
        'rate': 'MsgVpnRate',
        'replication_ack_propagation_interval_msg_count': 'int',
        'replication_active_ack_prop_tx_msg_count': 'int',
        'replication_active_async_queued_msg_count': 'int',
        'replication_active_locally_consumed_msg_count': 'int',
        'replication_active_mate_flow_congested_peak_time': 'int',
        'replication_active_mate_flow_not_congested_peak_time': 'int',
        'replication_active_promoted_queued_msg_count': 'int',
        'replication_active_reconcile_request_rx_msg_count': 'int',
        'replication_active_sync_eligible_peak_time': 'int',
        'replication_active_sync_ineligible_peak_time': 'int',
        'replication_active_sync_queued_as_async_msg_count': 'int',
        'replication_active_sync_queued_msg_count': 'int',
        'replication_active_transition_to_sync_ineligible_count': 'int',
        'replication_bridge_authentication_basic_client_username': 'str',
        'replication_bridge_authentication_scheme': 'str',
        'replication_bridge_bound_to_queue': 'bool',
        'replication_bridge_compressed_data_enabled': 'bool',
        'replication_bridge_egress_flow_window_size': 'int',
        'replication_bridge_name': 'str',
        'replication_bridge_retry_delay': 'int',
        'replication_bridge_tls_enabled': 'bool',
        'replication_bridge_unidirectional_client_profile_name': 'str',
        'replication_bridge_up': 'bool',
        'replication_enabled': 'bool',
        'replication_queue_bound': 'bool',
        'replication_queue_max_msg_spool_usage': 'int',
        'replication_queue_reject_msg_to_sender_on_discard_enabled': 'bool',
        'replication_reject_msg_when_sync_ineligible_enabled': 'bool',
        'replication_remote_bridge_name': 'str',
        'replication_remote_bridge_up': 'bool',
        'replication_role': 'str',
        'replication_standby_ack_prop_out_of_seq_rx_msg_count': 'int',
        'replication_standby_ack_prop_rx_msg_count': 'int',
        'replication_standby_reconcile_request_tx_msg_count': 'int',
        'replication_standby_rx_msg_count': 'int',
        'replication_standby_transaction_request_count': 'int',
        'replication_standby_transaction_request_failure_count': 'int',
        'replication_standby_transaction_request_success_count': 'int',
        'replication_sync_eligible': 'bool',
        'replication_transaction_mode': 'str',
        'rest_tls_server_cert_enforce_trusted_common_name_enabled': 'bool',
        'rest_tls_server_cert_max_chain_depth': 'int',
        'rest_tls_server_cert_validate_date_enabled': 'bool',
        'rest_tls_server_cert_validate_name_enabled': 'bool',
        'rx_byte_count': 'int',
        'rx_byte_rate': 'int',
        'rx_compressed_byte_count': 'int',
        'rx_compressed_byte_rate': 'int',
        'rx_compression_ratio': 'str',
        'rx_msg_count': 'int',
        'rx_msg_rate': 'int',
        'rx_uncompressed_byte_count': 'int',
        'rx_uncompressed_byte_rate': 'int',
        'semp_over_msg_bus_admin_client_enabled': 'bool',
        'semp_over_msg_bus_admin_distributed_cache_enabled': 'bool',
        'semp_over_msg_bus_admin_enabled': 'bool',
        'semp_over_msg_bus_enabled': 'bool',
        'semp_over_msg_bus_show_enabled': 'bool',
        'service_amqp_max_connection_count': 'int',
        'service_amqp_plain_text_compressed': 'bool',
        'service_amqp_plain_text_enabled': 'bool',
        'service_amqp_plain_text_failure_reason': 'str',
        'service_amqp_plain_text_listen_port': 'int',
        'service_amqp_plain_text_up': 'bool',
        'service_amqp_tls_compressed': 'bool',
        'service_amqp_tls_enabled': 'bool',
        'service_amqp_tls_failure_reason': 'str',
        'service_amqp_tls_listen_port': 'int',
        'service_amqp_tls_up': 'bool',
        'service_mqtt_max_connection_count': 'int',
        'service_mqtt_plain_text_compressed': 'bool',
        'service_mqtt_plain_text_enabled': 'bool',
        'service_mqtt_plain_text_failure_reason': 'str',
        'service_mqtt_plain_text_listen_port': 'int',
        'service_mqtt_plain_text_up': 'bool',
        'service_mqtt_tls_compressed': 'bool',
        'service_mqtt_tls_enabled': 'bool',
        'service_mqtt_tls_failure_reason': 'str',
        'service_mqtt_tls_listen_port': 'int',
        'service_mqtt_tls_up': 'bool',
        'service_mqtt_tls_web_socket_compressed': 'bool',
        'service_mqtt_tls_web_socket_enabled': 'bool',
        'service_mqtt_tls_web_socket_failure_reason': 'str',
        'service_mqtt_tls_web_socket_listen_port': 'int',
        'service_mqtt_tls_web_socket_up': 'bool',
        'service_mqtt_web_socket_compressed': 'bool',
        'service_mqtt_web_socket_enabled': 'bool',
        'service_mqtt_web_socket_failure_reason': 'str',
        'service_mqtt_web_socket_listen_port': 'int',
        'service_mqtt_web_socket_up': 'bool',
        'service_rest_incoming_max_connection_count': 'int',
        'service_rest_incoming_plain_text_compressed': 'bool',
        'service_rest_incoming_plain_text_enabled': 'bool',
        'service_rest_incoming_plain_text_failure_reason': 'str',
        'service_rest_incoming_plain_text_listen_port': 'int',
        'service_rest_incoming_plain_text_up': 'bool',
        'service_rest_incoming_tls_compressed': 'bool',
        'service_rest_incoming_tls_enabled': 'bool',
        'service_rest_incoming_tls_failure_reason': 'str',
        'service_rest_incoming_tls_listen_port': 'int',
        'service_rest_incoming_tls_up': 'bool',
        'service_rest_mode': 'str',
        'service_rest_outgoing_max_connection_count': 'int',
        'service_smf_max_connection_count': 'int',
        'service_smf_plain_text_enabled': 'bool',
        'service_smf_plain_text_failure_reason': 'str',
        'service_smf_plain_text_up': 'bool',
        'service_smf_tls_enabled': 'bool',
        'service_smf_tls_failure_reason': 'str',
        'service_smf_tls_up': 'bool',
        'service_web_max_connection_count': 'int',
        'service_web_plain_text_enabled': 'bool',
        'service_web_plain_text_failure_reason': 'str',
        'service_web_plain_text_up': 'bool',
        'service_web_tls_enabled': 'bool',
        'service_web_tls_failure_reason': 'str',
        'service_web_tls_up': 'bool',
        'state': 'str',
        'subscription_export_progress': 'int',
        'system_manager': 'bool',
        'tls_allow_downgrade_to_plain_text_enabled': 'bool',
        'tls_average_rx_byte_rate': 'int',
        'tls_average_tx_byte_rate': 'int',
        'tls_rx_byte_count': 'int',
        'tls_rx_byte_rate': 'int',
        'tls_tx_byte_count': 'int',
        'tls_tx_byte_rate': 'int',
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
        'alias': 'alias',
        'authentication_basic_enabled': 'authenticationBasicEnabled',
        'authentication_basic_profile_name': 'authenticationBasicProfileName',
        'authentication_basic_radius_domain': 'authenticationBasicRadiusDomain',
        'authentication_basic_type': 'authenticationBasicType',
        'authentication_client_cert_allow_api_provided_username_enabled': 'authenticationClientCertAllowApiProvidedUsernameEnabled',
        'authentication_client_cert_enabled': 'authenticationClientCertEnabled',
        'authentication_client_cert_max_chain_depth': 'authenticationClientCertMaxChainDepth',
        'authentication_client_cert_revocation_check_mode': 'authenticationClientCertRevocationCheckMode',
        'authentication_client_cert_username_source': 'authenticationClientCertUsernameSource',
        'authentication_client_cert_validate_date_enabled': 'authenticationClientCertValidateDateEnabled',
        'authentication_kerberos_allow_api_provided_username_enabled': 'authenticationKerberosAllowApiProvidedUsernameEnabled',
        'authentication_kerberos_enabled': 'authenticationKerberosEnabled',
        'authentication_oauth_default_provider_name': 'authenticationOauthDefaultProviderName',
        'authentication_oauth_enabled': 'authenticationOauthEnabled',
        'authorization_ldap_group_membership_attribute_name': 'authorizationLdapGroupMembershipAttributeName',
        'authorization_ldap_trim_client_username_domain_enabled': 'authorizationLdapTrimClientUsernameDomainEnabled',
        'authorization_profile_name': 'authorizationProfileName',
        'authorization_type': 'authorizationType',
        'average_rx_byte_rate': 'averageRxByteRate',
        'average_rx_compressed_byte_rate': 'averageRxCompressedByteRate',
        'average_rx_msg_rate': 'averageRxMsgRate',
        'average_rx_uncompressed_byte_rate': 'averageRxUncompressedByteRate',
        'average_tx_byte_rate': 'averageTxByteRate',
        'average_tx_compressed_byte_rate': 'averageTxCompressedByteRate',
        'average_tx_msg_rate': 'averageTxMsgRate',
        'average_tx_uncompressed_byte_rate': 'averageTxUncompressedByteRate',
        'bridging_tls_server_cert_enforce_trusted_common_name_enabled': 'bridgingTlsServerCertEnforceTrustedCommonNameEnabled',
        'bridging_tls_server_cert_max_chain_depth': 'bridgingTlsServerCertMaxChainDepth',
        'bridging_tls_server_cert_validate_date_enabled': 'bridgingTlsServerCertValidateDateEnabled',
        'bridging_tls_server_cert_validate_name_enabled': 'bridgingTlsServerCertValidateNameEnabled',
        'config_sync_local_key': 'configSyncLocalKey',
        'config_sync_local_last_result': 'configSyncLocalLastResult',
        'config_sync_local_role': 'configSyncLocalRole',
        'config_sync_local_state': 'configSyncLocalState',
        'config_sync_local_time_in_state': 'configSyncLocalTimeInState',
        'control_rx_byte_count': 'controlRxByteCount',
        'control_rx_msg_count': 'controlRxMsgCount',
        'control_tx_byte_count': 'controlTxByteCount',
        'control_tx_msg_count': 'controlTxMsgCount',
        'counter': 'counter',
        'data_rx_byte_count': 'dataRxByteCount',
        'data_rx_msg_count': 'dataRxMsgCount',
        'data_tx_byte_count': 'dataTxByteCount',
        'data_tx_msg_count': 'dataTxMsgCount',
        'discarded_rx_msg_count': 'discardedRxMsgCount',
        'discarded_tx_msg_count': 'discardedTxMsgCount',
        'distributed_cache_management_enabled': 'distributedCacheManagementEnabled',
        'dmr_enabled': 'dmrEnabled',
        'enabled': 'enabled',
        'event_connection_count_threshold': 'eventConnectionCountThreshold',
        'event_egress_flow_count_threshold': 'eventEgressFlowCountThreshold',
        'event_egress_msg_rate_threshold': 'eventEgressMsgRateThreshold',
        'event_endpoint_count_threshold': 'eventEndpointCountThreshold',
        'event_ingress_flow_count_threshold': 'eventIngressFlowCountThreshold',
        'event_ingress_msg_rate_threshold': 'eventIngressMsgRateThreshold',
        'event_large_msg_threshold': 'eventLargeMsgThreshold',
        'event_log_tag': 'eventLogTag',
        'event_msg_spool_usage_threshold': 'eventMsgSpoolUsageThreshold',
        'event_publish_client_enabled': 'eventPublishClientEnabled',
        'event_publish_msg_vpn_enabled': 'eventPublishMsgVpnEnabled',
        'event_publish_subscription_mode': 'eventPublishSubscriptionMode',
        'event_publish_topic_format_mqtt_enabled': 'eventPublishTopicFormatMqttEnabled',
        'event_publish_topic_format_smf_enabled': 'eventPublishTopicFormatSmfEnabled',
        'event_service_amqp_connection_count_threshold': 'eventServiceAmqpConnectionCountThreshold',
        'event_service_mqtt_connection_count_threshold': 'eventServiceMqttConnectionCountThreshold',
        'event_service_rest_incoming_connection_count_threshold': 'eventServiceRestIncomingConnectionCountThreshold',
        'event_service_smf_connection_count_threshold': 'eventServiceSmfConnectionCountThreshold',
        'event_service_web_connection_count_threshold': 'eventServiceWebConnectionCountThreshold',
        'event_subscription_count_threshold': 'eventSubscriptionCountThreshold',
        'event_transacted_session_count_threshold': 'eventTransactedSessionCountThreshold',
        'event_transaction_count_threshold': 'eventTransactionCountThreshold',
        'export_subscriptions_enabled': 'exportSubscriptionsEnabled',
        'failure_reason': 'failureReason',
        'jndi_enabled': 'jndiEnabled',
        'login_rx_msg_count': 'loginRxMsgCount',
        'login_tx_msg_count': 'loginTxMsgCount',
        'max_connection_count': 'maxConnectionCount',
        'max_effective_endpoint_count': 'maxEffectiveEndpointCount',
        'max_effective_rx_flow_count': 'maxEffectiveRxFlowCount',
        'max_effective_subscription_count': 'maxEffectiveSubscriptionCount',
        'max_effective_transacted_session_count': 'maxEffectiveTransactedSessionCount',
        'max_effective_transaction_count': 'maxEffectiveTransactionCount',
        'max_effective_tx_flow_count': 'maxEffectiveTxFlowCount',
        'max_egress_flow_count': 'maxEgressFlowCount',
        'max_endpoint_count': 'maxEndpointCount',
        'max_ingress_flow_count': 'maxIngressFlowCount',
        'max_msg_spool_usage': 'maxMsgSpoolUsage',
        'max_subscription_count': 'maxSubscriptionCount',
        'max_transacted_session_count': 'maxTransactedSessionCount',
        'max_transaction_count': 'maxTransactionCount',
        'mqtt_retain_max_memory': 'mqttRetainMaxMemory',
        'msg_replay_active_count': 'msgReplayActiveCount',
        'msg_replay_failed_count': 'msgReplayFailedCount',
        'msg_replay_initializing_count': 'msgReplayInitializingCount',
        'msg_replay_pending_complete_count': 'msgReplayPendingCompleteCount',
        'msg_spool_msg_count': 'msgSpoolMsgCount',
        'msg_spool_rx_msg_count': 'msgSpoolRxMsgCount',
        'msg_spool_tx_msg_count': 'msgSpoolTxMsgCount',
        'msg_spool_usage': 'msgSpoolUsage',
        'msg_vpn_name': 'msgVpnName',
        'rate': 'rate',
        'replication_ack_propagation_interval_msg_count': 'replicationAckPropagationIntervalMsgCount',
        'replication_active_ack_prop_tx_msg_count': 'replicationActiveAckPropTxMsgCount',
        'replication_active_async_queued_msg_count': 'replicationActiveAsyncQueuedMsgCount',
        'replication_active_locally_consumed_msg_count': 'replicationActiveLocallyConsumedMsgCount',
        'replication_active_mate_flow_congested_peak_time': 'replicationActiveMateFlowCongestedPeakTime',
        'replication_active_mate_flow_not_congested_peak_time': 'replicationActiveMateFlowNotCongestedPeakTime',
        'replication_active_promoted_queued_msg_count': 'replicationActivePromotedQueuedMsgCount',
        'replication_active_reconcile_request_rx_msg_count': 'replicationActiveReconcileRequestRxMsgCount',
        'replication_active_sync_eligible_peak_time': 'replicationActiveSyncEligiblePeakTime',
        'replication_active_sync_ineligible_peak_time': 'replicationActiveSyncIneligiblePeakTime',
        'replication_active_sync_queued_as_async_msg_count': 'replicationActiveSyncQueuedAsAsyncMsgCount',
        'replication_active_sync_queued_msg_count': 'replicationActiveSyncQueuedMsgCount',
        'replication_active_transition_to_sync_ineligible_count': 'replicationActiveTransitionToSyncIneligibleCount',
        'replication_bridge_authentication_basic_client_username': 'replicationBridgeAuthenticationBasicClientUsername',
        'replication_bridge_authentication_scheme': 'replicationBridgeAuthenticationScheme',
        'replication_bridge_bound_to_queue': 'replicationBridgeBoundToQueue',
        'replication_bridge_compressed_data_enabled': 'replicationBridgeCompressedDataEnabled',
        'replication_bridge_egress_flow_window_size': 'replicationBridgeEgressFlowWindowSize',
        'replication_bridge_name': 'replicationBridgeName',
        'replication_bridge_retry_delay': 'replicationBridgeRetryDelay',
        'replication_bridge_tls_enabled': 'replicationBridgeTlsEnabled',
        'replication_bridge_unidirectional_client_profile_name': 'replicationBridgeUnidirectionalClientProfileName',
        'replication_bridge_up': 'replicationBridgeUp',
        'replication_enabled': 'replicationEnabled',
        'replication_queue_bound': 'replicationQueueBound',
        'replication_queue_max_msg_spool_usage': 'replicationQueueMaxMsgSpoolUsage',
        'replication_queue_reject_msg_to_sender_on_discard_enabled': 'replicationQueueRejectMsgToSenderOnDiscardEnabled',
        'replication_reject_msg_when_sync_ineligible_enabled': 'replicationRejectMsgWhenSyncIneligibleEnabled',
        'replication_remote_bridge_name': 'replicationRemoteBridgeName',
        'replication_remote_bridge_up': 'replicationRemoteBridgeUp',
        'replication_role': 'replicationRole',
        'replication_standby_ack_prop_out_of_seq_rx_msg_count': 'replicationStandbyAckPropOutOfSeqRxMsgCount',
        'replication_standby_ack_prop_rx_msg_count': 'replicationStandbyAckPropRxMsgCount',
        'replication_standby_reconcile_request_tx_msg_count': 'replicationStandbyReconcileRequestTxMsgCount',
        'replication_standby_rx_msg_count': 'replicationStandbyRxMsgCount',
        'replication_standby_transaction_request_count': 'replicationStandbyTransactionRequestCount',
        'replication_standby_transaction_request_failure_count': 'replicationStandbyTransactionRequestFailureCount',
        'replication_standby_transaction_request_success_count': 'replicationStandbyTransactionRequestSuccessCount',
        'replication_sync_eligible': 'replicationSyncEligible',
        'replication_transaction_mode': 'replicationTransactionMode',
        'rest_tls_server_cert_enforce_trusted_common_name_enabled': 'restTlsServerCertEnforceTrustedCommonNameEnabled',
        'rest_tls_server_cert_max_chain_depth': 'restTlsServerCertMaxChainDepth',
        'rest_tls_server_cert_validate_date_enabled': 'restTlsServerCertValidateDateEnabled',
        'rest_tls_server_cert_validate_name_enabled': 'restTlsServerCertValidateNameEnabled',
        'rx_byte_count': 'rxByteCount',
        'rx_byte_rate': 'rxByteRate',
        'rx_compressed_byte_count': 'rxCompressedByteCount',
        'rx_compressed_byte_rate': 'rxCompressedByteRate',
        'rx_compression_ratio': 'rxCompressionRatio',
        'rx_msg_count': 'rxMsgCount',
        'rx_msg_rate': 'rxMsgRate',
        'rx_uncompressed_byte_count': 'rxUncompressedByteCount',
        'rx_uncompressed_byte_rate': 'rxUncompressedByteRate',
        'semp_over_msg_bus_admin_client_enabled': 'sempOverMsgBusAdminClientEnabled',
        'semp_over_msg_bus_admin_distributed_cache_enabled': 'sempOverMsgBusAdminDistributedCacheEnabled',
        'semp_over_msg_bus_admin_enabled': 'sempOverMsgBusAdminEnabled',
        'semp_over_msg_bus_enabled': 'sempOverMsgBusEnabled',
        'semp_over_msg_bus_show_enabled': 'sempOverMsgBusShowEnabled',
        'service_amqp_max_connection_count': 'serviceAmqpMaxConnectionCount',
        'service_amqp_plain_text_compressed': 'serviceAmqpPlainTextCompressed',
        'service_amqp_plain_text_enabled': 'serviceAmqpPlainTextEnabled',
        'service_amqp_plain_text_failure_reason': 'serviceAmqpPlainTextFailureReason',
        'service_amqp_plain_text_listen_port': 'serviceAmqpPlainTextListenPort',
        'service_amqp_plain_text_up': 'serviceAmqpPlainTextUp',
        'service_amqp_tls_compressed': 'serviceAmqpTlsCompressed',
        'service_amqp_tls_enabled': 'serviceAmqpTlsEnabled',
        'service_amqp_tls_failure_reason': 'serviceAmqpTlsFailureReason',
        'service_amqp_tls_listen_port': 'serviceAmqpTlsListenPort',
        'service_amqp_tls_up': 'serviceAmqpTlsUp',
        'service_mqtt_max_connection_count': 'serviceMqttMaxConnectionCount',
        'service_mqtt_plain_text_compressed': 'serviceMqttPlainTextCompressed',
        'service_mqtt_plain_text_enabled': 'serviceMqttPlainTextEnabled',
        'service_mqtt_plain_text_failure_reason': 'serviceMqttPlainTextFailureReason',
        'service_mqtt_plain_text_listen_port': 'serviceMqttPlainTextListenPort',
        'service_mqtt_plain_text_up': 'serviceMqttPlainTextUp',
        'service_mqtt_tls_compressed': 'serviceMqttTlsCompressed',
        'service_mqtt_tls_enabled': 'serviceMqttTlsEnabled',
        'service_mqtt_tls_failure_reason': 'serviceMqttTlsFailureReason',
        'service_mqtt_tls_listen_port': 'serviceMqttTlsListenPort',
        'service_mqtt_tls_up': 'serviceMqttTlsUp',
        'service_mqtt_tls_web_socket_compressed': 'serviceMqttTlsWebSocketCompressed',
        'service_mqtt_tls_web_socket_enabled': 'serviceMqttTlsWebSocketEnabled',
        'service_mqtt_tls_web_socket_failure_reason': 'serviceMqttTlsWebSocketFailureReason',
        'service_mqtt_tls_web_socket_listen_port': 'serviceMqttTlsWebSocketListenPort',
        'service_mqtt_tls_web_socket_up': 'serviceMqttTlsWebSocketUp',
        'service_mqtt_web_socket_compressed': 'serviceMqttWebSocketCompressed',
        'service_mqtt_web_socket_enabled': 'serviceMqttWebSocketEnabled',
        'service_mqtt_web_socket_failure_reason': 'serviceMqttWebSocketFailureReason',
        'service_mqtt_web_socket_listen_port': 'serviceMqttWebSocketListenPort',
        'service_mqtt_web_socket_up': 'serviceMqttWebSocketUp',
        'service_rest_incoming_max_connection_count': 'serviceRestIncomingMaxConnectionCount',
        'service_rest_incoming_plain_text_compressed': 'serviceRestIncomingPlainTextCompressed',
        'service_rest_incoming_plain_text_enabled': 'serviceRestIncomingPlainTextEnabled',
        'service_rest_incoming_plain_text_failure_reason': 'serviceRestIncomingPlainTextFailureReason',
        'service_rest_incoming_plain_text_listen_port': 'serviceRestIncomingPlainTextListenPort',
        'service_rest_incoming_plain_text_up': 'serviceRestIncomingPlainTextUp',
        'service_rest_incoming_tls_compressed': 'serviceRestIncomingTlsCompressed',
        'service_rest_incoming_tls_enabled': 'serviceRestIncomingTlsEnabled',
        'service_rest_incoming_tls_failure_reason': 'serviceRestIncomingTlsFailureReason',
        'service_rest_incoming_tls_listen_port': 'serviceRestIncomingTlsListenPort',
        'service_rest_incoming_tls_up': 'serviceRestIncomingTlsUp',
        'service_rest_mode': 'serviceRestMode',
        'service_rest_outgoing_max_connection_count': 'serviceRestOutgoingMaxConnectionCount',
        'service_smf_max_connection_count': 'serviceSmfMaxConnectionCount',
        'service_smf_plain_text_enabled': 'serviceSmfPlainTextEnabled',
        'service_smf_plain_text_failure_reason': 'serviceSmfPlainTextFailureReason',
        'service_smf_plain_text_up': 'serviceSmfPlainTextUp',
        'service_smf_tls_enabled': 'serviceSmfTlsEnabled',
        'service_smf_tls_failure_reason': 'serviceSmfTlsFailureReason',
        'service_smf_tls_up': 'serviceSmfTlsUp',
        'service_web_max_connection_count': 'serviceWebMaxConnectionCount',
        'service_web_plain_text_enabled': 'serviceWebPlainTextEnabled',
        'service_web_plain_text_failure_reason': 'serviceWebPlainTextFailureReason',
        'service_web_plain_text_up': 'serviceWebPlainTextUp',
        'service_web_tls_enabled': 'serviceWebTlsEnabled',
        'service_web_tls_failure_reason': 'serviceWebTlsFailureReason',
        'service_web_tls_up': 'serviceWebTlsUp',
        'state': 'state',
        'subscription_export_progress': 'subscriptionExportProgress',
        'system_manager': 'systemManager',
        'tls_allow_downgrade_to_plain_text_enabled': 'tlsAllowDowngradeToPlainTextEnabled',
        'tls_average_rx_byte_rate': 'tlsAverageRxByteRate',
        'tls_average_tx_byte_rate': 'tlsAverageTxByteRate',
        'tls_rx_byte_count': 'tlsRxByteCount',
        'tls_rx_byte_rate': 'tlsRxByteRate',
        'tls_tx_byte_count': 'tlsTxByteCount',
        'tls_tx_byte_rate': 'tlsTxByteRate',
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

    def __init__(self, alias=None, authentication_basic_enabled=None, authentication_basic_profile_name=None, authentication_basic_radius_domain=None, authentication_basic_type=None, authentication_client_cert_allow_api_provided_username_enabled=None, authentication_client_cert_enabled=None, authentication_client_cert_max_chain_depth=None, authentication_client_cert_revocation_check_mode=None, authentication_client_cert_username_source=None, authentication_client_cert_validate_date_enabled=None, authentication_kerberos_allow_api_provided_username_enabled=None, authentication_kerberos_enabled=None, authentication_oauth_default_provider_name=None, authentication_oauth_enabled=None, authorization_ldap_group_membership_attribute_name=None, authorization_ldap_trim_client_username_domain_enabled=None, authorization_profile_name=None, authorization_type=None, average_rx_byte_rate=None, average_rx_compressed_byte_rate=None, average_rx_msg_rate=None, average_rx_uncompressed_byte_rate=None, average_tx_byte_rate=None, average_tx_compressed_byte_rate=None, average_tx_msg_rate=None, average_tx_uncompressed_byte_rate=None, bridging_tls_server_cert_enforce_trusted_common_name_enabled=None, bridging_tls_server_cert_max_chain_depth=None, bridging_tls_server_cert_validate_date_enabled=None, bridging_tls_server_cert_validate_name_enabled=None, config_sync_local_key=None, config_sync_local_last_result=None, config_sync_local_role=None, config_sync_local_state=None, config_sync_local_time_in_state=None, control_rx_byte_count=None, control_rx_msg_count=None, control_tx_byte_count=None, control_tx_msg_count=None, counter=None, data_rx_byte_count=None, data_rx_msg_count=None, data_tx_byte_count=None, data_tx_msg_count=None, discarded_rx_msg_count=None, discarded_tx_msg_count=None, distributed_cache_management_enabled=None, dmr_enabled=None, enabled=None, event_connection_count_threshold=None, event_egress_flow_count_threshold=None, event_egress_msg_rate_threshold=None, event_endpoint_count_threshold=None, event_ingress_flow_count_threshold=None, event_ingress_msg_rate_threshold=None, event_large_msg_threshold=None, event_log_tag=None, event_msg_spool_usage_threshold=None, event_publish_client_enabled=None, event_publish_msg_vpn_enabled=None, event_publish_subscription_mode=None, event_publish_topic_format_mqtt_enabled=None, event_publish_topic_format_smf_enabled=None, event_service_amqp_connection_count_threshold=None, event_service_mqtt_connection_count_threshold=None, event_service_rest_incoming_connection_count_threshold=None, event_service_smf_connection_count_threshold=None, event_service_web_connection_count_threshold=None, event_subscription_count_threshold=None, event_transacted_session_count_threshold=None, event_transaction_count_threshold=None, export_subscriptions_enabled=None, failure_reason=None, jndi_enabled=None, login_rx_msg_count=None, login_tx_msg_count=None, max_connection_count=None, max_effective_endpoint_count=None, max_effective_rx_flow_count=None, max_effective_subscription_count=None, max_effective_transacted_session_count=None, max_effective_transaction_count=None, max_effective_tx_flow_count=None, max_egress_flow_count=None, max_endpoint_count=None, max_ingress_flow_count=None, max_msg_spool_usage=None, max_subscription_count=None, max_transacted_session_count=None, max_transaction_count=None, mqtt_retain_max_memory=None, msg_replay_active_count=None, msg_replay_failed_count=None, msg_replay_initializing_count=None, msg_replay_pending_complete_count=None, msg_spool_msg_count=None, msg_spool_rx_msg_count=None, msg_spool_tx_msg_count=None, msg_spool_usage=None, msg_vpn_name=None, rate=None, replication_ack_propagation_interval_msg_count=None, replication_active_ack_prop_tx_msg_count=None, replication_active_async_queued_msg_count=None, replication_active_locally_consumed_msg_count=None, replication_active_mate_flow_congested_peak_time=None, replication_active_mate_flow_not_congested_peak_time=None, replication_active_promoted_queued_msg_count=None, replication_active_reconcile_request_rx_msg_count=None, replication_active_sync_eligible_peak_time=None, replication_active_sync_ineligible_peak_time=None, replication_active_sync_queued_as_async_msg_count=None, replication_active_sync_queued_msg_count=None, replication_active_transition_to_sync_ineligible_count=None, replication_bridge_authentication_basic_client_username=None, replication_bridge_authentication_scheme=None, replication_bridge_bound_to_queue=None, replication_bridge_compressed_data_enabled=None, replication_bridge_egress_flow_window_size=None, replication_bridge_name=None, replication_bridge_retry_delay=None, replication_bridge_tls_enabled=None, replication_bridge_unidirectional_client_profile_name=None, replication_bridge_up=None, replication_enabled=None, replication_queue_bound=None, replication_queue_max_msg_spool_usage=None, replication_queue_reject_msg_to_sender_on_discard_enabled=None, replication_reject_msg_when_sync_ineligible_enabled=None, replication_remote_bridge_name=None, replication_remote_bridge_up=None, replication_role=None, replication_standby_ack_prop_out_of_seq_rx_msg_count=None, replication_standby_ack_prop_rx_msg_count=None, replication_standby_reconcile_request_tx_msg_count=None, replication_standby_rx_msg_count=None, replication_standby_transaction_request_count=None, replication_standby_transaction_request_failure_count=None, replication_standby_transaction_request_success_count=None, replication_sync_eligible=None, replication_transaction_mode=None, rest_tls_server_cert_enforce_trusted_common_name_enabled=None, rest_tls_server_cert_max_chain_depth=None, rest_tls_server_cert_validate_date_enabled=None, rest_tls_server_cert_validate_name_enabled=None, rx_byte_count=None, rx_byte_rate=None, rx_compressed_byte_count=None, rx_compressed_byte_rate=None, rx_compression_ratio=None, rx_msg_count=None, rx_msg_rate=None, rx_uncompressed_byte_count=None, rx_uncompressed_byte_rate=None, semp_over_msg_bus_admin_client_enabled=None, semp_over_msg_bus_admin_distributed_cache_enabled=None, semp_over_msg_bus_admin_enabled=None, semp_over_msg_bus_enabled=None, semp_over_msg_bus_show_enabled=None, service_amqp_max_connection_count=None, service_amqp_plain_text_compressed=None, service_amqp_plain_text_enabled=None, service_amqp_plain_text_failure_reason=None, service_amqp_plain_text_listen_port=None, service_amqp_plain_text_up=None, service_amqp_tls_compressed=None, service_amqp_tls_enabled=None, service_amqp_tls_failure_reason=None, service_amqp_tls_listen_port=None, service_amqp_tls_up=None, service_mqtt_max_connection_count=None, service_mqtt_plain_text_compressed=None, service_mqtt_plain_text_enabled=None, service_mqtt_plain_text_failure_reason=None, service_mqtt_plain_text_listen_port=None, service_mqtt_plain_text_up=None, service_mqtt_tls_compressed=None, service_mqtt_tls_enabled=None, service_mqtt_tls_failure_reason=None, service_mqtt_tls_listen_port=None, service_mqtt_tls_up=None, service_mqtt_tls_web_socket_compressed=None, service_mqtt_tls_web_socket_enabled=None, service_mqtt_tls_web_socket_failure_reason=None, service_mqtt_tls_web_socket_listen_port=None, service_mqtt_tls_web_socket_up=None, service_mqtt_web_socket_compressed=None, service_mqtt_web_socket_enabled=None, service_mqtt_web_socket_failure_reason=None, service_mqtt_web_socket_listen_port=None, service_mqtt_web_socket_up=None, service_rest_incoming_max_connection_count=None, service_rest_incoming_plain_text_compressed=None, service_rest_incoming_plain_text_enabled=None, service_rest_incoming_plain_text_failure_reason=None, service_rest_incoming_plain_text_listen_port=None, service_rest_incoming_plain_text_up=None, service_rest_incoming_tls_compressed=None, service_rest_incoming_tls_enabled=None, service_rest_incoming_tls_failure_reason=None, service_rest_incoming_tls_listen_port=None, service_rest_incoming_tls_up=None, service_rest_mode=None, service_rest_outgoing_max_connection_count=None, service_smf_max_connection_count=None, service_smf_plain_text_enabled=None, service_smf_plain_text_failure_reason=None, service_smf_plain_text_up=None, service_smf_tls_enabled=None, service_smf_tls_failure_reason=None, service_smf_tls_up=None, service_web_max_connection_count=None, service_web_plain_text_enabled=None, service_web_plain_text_failure_reason=None, service_web_plain_text_up=None, service_web_tls_enabled=None, service_web_tls_failure_reason=None, service_web_tls_up=None, state=None, subscription_export_progress=None, system_manager=None, tls_allow_downgrade_to_plain_text_enabled=None, tls_average_rx_byte_rate=None, tls_average_tx_byte_rate=None, tls_rx_byte_count=None, tls_rx_byte_rate=None, tls_tx_byte_count=None, tls_tx_byte_rate=None, tx_byte_count=None, tx_byte_rate=None, tx_compressed_byte_count=None, tx_compressed_byte_rate=None, tx_compression_ratio=None, tx_msg_count=None, tx_msg_rate=None, tx_uncompressed_byte_count=None, tx_uncompressed_byte_rate=None):  # noqa: E501
        """MsgVpn - a model defined in Swagger"""  # noqa: E501

        self._alias = None
        self._authentication_basic_enabled = None
        self._authentication_basic_profile_name = None
        self._authentication_basic_radius_domain = None
        self._authentication_basic_type = None
        self._authentication_client_cert_allow_api_provided_username_enabled = None
        self._authentication_client_cert_enabled = None
        self._authentication_client_cert_max_chain_depth = None
        self._authentication_client_cert_revocation_check_mode = None
        self._authentication_client_cert_username_source = None
        self._authentication_client_cert_validate_date_enabled = None
        self._authentication_kerberos_allow_api_provided_username_enabled = None
        self._authentication_kerberos_enabled = None
        self._authentication_oauth_default_provider_name = None
        self._authentication_oauth_enabled = None
        self._authorization_ldap_group_membership_attribute_name = None
        self._authorization_ldap_trim_client_username_domain_enabled = None
        self._authorization_profile_name = None
        self._authorization_type = None
        self._average_rx_byte_rate = None
        self._average_rx_compressed_byte_rate = None
        self._average_rx_msg_rate = None
        self._average_rx_uncompressed_byte_rate = None
        self._average_tx_byte_rate = None
        self._average_tx_compressed_byte_rate = None
        self._average_tx_msg_rate = None
        self._average_tx_uncompressed_byte_rate = None
        self._bridging_tls_server_cert_enforce_trusted_common_name_enabled = None
        self._bridging_tls_server_cert_max_chain_depth = None
        self._bridging_tls_server_cert_validate_date_enabled = None
        self._bridging_tls_server_cert_validate_name_enabled = None
        self._config_sync_local_key = None
        self._config_sync_local_last_result = None
        self._config_sync_local_role = None
        self._config_sync_local_state = None
        self._config_sync_local_time_in_state = None
        self._control_rx_byte_count = None
        self._control_rx_msg_count = None
        self._control_tx_byte_count = None
        self._control_tx_msg_count = None
        self._counter = None
        self._data_rx_byte_count = None
        self._data_rx_msg_count = None
        self._data_tx_byte_count = None
        self._data_tx_msg_count = None
        self._discarded_rx_msg_count = None
        self._discarded_tx_msg_count = None
        self._distributed_cache_management_enabled = None
        self._dmr_enabled = None
        self._enabled = None
        self._event_connection_count_threshold = None
        self._event_egress_flow_count_threshold = None
        self._event_egress_msg_rate_threshold = None
        self._event_endpoint_count_threshold = None
        self._event_ingress_flow_count_threshold = None
        self._event_ingress_msg_rate_threshold = None
        self._event_large_msg_threshold = None
        self._event_log_tag = None
        self._event_msg_spool_usage_threshold = None
        self._event_publish_client_enabled = None
        self._event_publish_msg_vpn_enabled = None
        self._event_publish_subscription_mode = None
        self._event_publish_topic_format_mqtt_enabled = None
        self._event_publish_topic_format_smf_enabled = None
        self._event_service_amqp_connection_count_threshold = None
        self._event_service_mqtt_connection_count_threshold = None
        self._event_service_rest_incoming_connection_count_threshold = None
        self._event_service_smf_connection_count_threshold = None
        self._event_service_web_connection_count_threshold = None
        self._event_subscription_count_threshold = None
        self._event_transacted_session_count_threshold = None
        self._event_transaction_count_threshold = None
        self._export_subscriptions_enabled = None
        self._failure_reason = None
        self._jndi_enabled = None
        self._login_rx_msg_count = None
        self._login_tx_msg_count = None
        self._max_connection_count = None
        self._max_effective_endpoint_count = None
        self._max_effective_rx_flow_count = None
        self._max_effective_subscription_count = None
        self._max_effective_transacted_session_count = None
        self._max_effective_transaction_count = None
        self._max_effective_tx_flow_count = None
        self._max_egress_flow_count = None
        self._max_endpoint_count = None
        self._max_ingress_flow_count = None
        self._max_msg_spool_usage = None
        self._max_subscription_count = None
        self._max_transacted_session_count = None
        self._max_transaction_count = None
        self._mqtt_retain_max_memory = None
        self._msg_replay_active_count = None
        self._msg_replay_failed_count = None
        self._msg_replay_initializing_count = None
        self._msg_replay_pending_complete_count = None
        self._msg_spool_msg_count = None
        self._msg_spool_rx_msg_count = None
        self._msg_spool_tx_msg_count = None
        self._msg_spool_usage = None
        self._msg_vpn_name = None
        self._rate = None
        self._replication_ack_propagation_interval_msg_count = None
        self._replication_active_ack_prop_tx_msg_count = None
        self._replication_active_async_queued_msg_count = None
        self._replication_active_locally_consumed_msg_count = None
        self._replication_active_mate_flow_congested_peak_time = None
        self._replication_active_mate_flow_not_congested_peak_time = None
        self._replication_active_promoted_queued_msg_count = None
        self._replication_active_reconcile_request_rx_msg_count = None
        self._replication_active_sync_eligible_peak_time = None
        self._replication_active_sync_ineligible_peak_time = None
        self._replication_active_sync_queued_as_async_msg_count = None
        self._replication_active_sync_queued_msg_count = None
        self._replication_active_transition_to_sync_ineligible_count = None
        self._replication_bridge_authentication_basic_client_username = None
        self._replication_bridge_authentication_scheme = None
        self._replication_bridge_bound_to_queue = None
        self._replication_bridge_compressed_data_enabled = None
        self._replication_bridge_egress_flow_window_size = None
        self._replication_bridge_name = None
        self._replication_bridge_retry_delay = None
        self._replication_bridge_tls_enabled = None
        self._replication_bridge_unidirectional_client_profile_name = None
        self._replication_bridge_up = None
        self._replication_enabled = None
        self._replication_queue_bound = None
        self._replication_queue_max_msg_spool_usage = None
        self._replication_queue_reject_msg_to_sender_on_discard_enabled = None
        self._replication_reject_msg_when_sync_ineligible_enabled = None
        self._replication_remote_bridge_name = None
        self._replication_remote_bridge_up = None
        self._replication_role = None
        self._replication_standby_ack_prop_out_of_seq_rx_msg_count = None
        self._replication_standby_ack_prop_rx_msg_count = None
        self._replication_standby_reconcile_request_tx_msg_count = None
        self._replication_standby_rx_msg_count = None
        self._replication_standby_transaction_request_count = None
        self._replication_standby_transaction_request_failure_count = None
        self._replication_standby_transaction_request_success_count = None
        self._replication_sync_eligible = None
        self._replication_transaction_mode = None
        self._rest_tls_server_cert_enforce_trusted_common_name_enabled = None
        self._rest_tls_server_cert_max_chain_depth = None
        self._rest_tls_server_cert_validate_date_enabled = None
        self._rest_tls_server_cert_validate_name_enabled = None
        self._rx_byte_count = None
        self._rx_byte_rate = None
        self._rx_compressed_byte_count = None
        self._rx_compressed_byte_rate = None
        self._rx_compression_ratio = None
        self._rx_msg_count = None
        self._rx_msg_rate = None
        self._rx_uncompressed_byte_count = None
        self._rx_uncompressed_byte_rate = None
        self._semp_over_msg_bus_admin_client_enabled = None
        self._semp_over_msg_bus_admin_distributed_cache_enabled = None
        self._semp_over_msg_bus_admin_enabled = None
        self._semp_over_msg_bus_enabled = None
        self._semp_over_msg_bus_show_enabled = None
        self._service_amqp_max_connection_count = None
        self._service_amqp_plain_text_compressed = None
        self._service_amqp_plain_text_enabled = None
        self._service_amqp_plain_text_failure_reason = None
        self._service_amqp_plain_text_listen_port = None
        self._service_amqp_plain_text_up = None
        self._service_amqp_tls_compressed = None
        self._service_amqp_tls_enabled = None
        self._service_amqp_tls_failure_reason = None
        self._service_amqp_tls_listen_port = None
        self._service_amqp_tls_up = None
        self._service_mqtt_max_connection_count = None
        self._service_mqtt_plain_text_compressed = None
        self._service_mqtt_plain_text_enabled = None
        self._service_mqtt_plain_text_failure_reason = None
        self._service_mqtt_plain_text_listen_port = None
        self._service_mqtt_plain_text_up = None
        self._service_mqtt_tls_compressed = None
        self._service_mqtt_tls_enabled = None
        self._service_mqtt_tls_failure_reason = None
        self._service_mqtt_tls_listen_port = None
        self._service_mqtt_tls_up = None
        self._service_mqtt_tls_web_socket_compressed = None
        self._service_mqtt_tls_web_socket_enabled = None
        self._service_mqtt_tls_web_socket_failure_reason = None
        self._service_mqtt_tls_web_socket_listen_port = None
        self._service_mqtt_tls_web_socket_up = None
        self._service_mqtt_web_socket_compressed = None
        self._service_mqtt_web_socket_enabled = None
        self._service_mqtt_web_socket_failure_reason = None
        self._service_mqtt_web_socket_listen_port = None
        self._service_mqtt_web_socket_up = None
        self._service_rest_incoming_max_connection_count = None
        self._service_rest_incoming_plain_text_compressed = None
        self._service_rest_incoming_plain_text_enabled = None
        self._service_rest_incoming_plain_text_failure_reason = None
        self._service_rest_incoming_plain_text_listen_port = None
        self._service_rest_incoming_plain_text_up = None
        self._service_rest_incoming_tls_compressed = None
        self._service_rest_incoming_tls_enabled = None
        self._service_rest_incoming_tls_failure_reason = None
        self._service_rest_incoming_tls_listen_port = None
        self._service_rest_incoming_tls_up = None
        self._service_rest_mode = None
        self._service_rest_outgoing_max_connection_count = None
        self._service_smf_max_connection_count = None
        self._service_smf_plain_text_enabled = None
        self._service_smf_plain_text_failure_reason = None
        self._service_smf_plain_text_up = None
        self._service_smf_tls_enabled = None
        self._service_smf_tls_failure_reason = None
        self._service_smf_tls_up = None
        self._service_web_max_connection_count = None
        self._service_web_plain_text_enabled = None
        self._service_web_plain_text_failure_reason = None
        self._service_web_plain_text_up = None
        self._service_web_tls_enabled = None
        self._service_web_tls_failure_reason = None
        self._service_web_tls_up = None
        self._state = None
        self._subscription_export_progress = None
        self._system_manager = None
        self._tls_allow_downgrade_to_plain_text_enabled = None
        self._tls_average_rx_byte_rate = None
        self._tls_average_tx_byte_rate = None
        self._tls_rx_byte_count = None
        self._tls_rx_byte_rate = None
        self._tls_tx_byte_count = None
        self._tls_tx_byte_rate = None
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

        if alias is not None:
            self.alias = alias
        if authentication_basic_enabled is not None:
            self.authentication_basic_enabled = authentication_basic_enabled
        if authentication_basic_profile_name is not None:
            self.authentication_basic_profile_name = authentication_basic_profile_name
        if authentication_basic_radius_domain is not None:
            self.authentication_basic_radius_domain = authentication_basic_radius_domain
        if authentication_basic_type is not None:
            self.authentication_basic_type = authentication_basic_type
        if authentication_client_cert_allow_api_provided_username_enabled is not None:
            self.authentication_client_cert_allow_api_provided_username_enabled = authentication_client_cert_allow_api_provided_username_enabled
        if authentication_client_cert_enabled is not None:
            self.authentication_client_cert_enabled = authentication_client_cert_enabled
        if authentication_client_cert_max_chain_depth is not None:
            self.authentication_client_cert_max_chain_depth = authentication_client_cert_max_chain_depth
        if authentication_client_cert_revocation_check_mode is not None:
            self.authentication_client_cert_revocation_check_mode = authentication_client_cert_revocation_check_mode
        if authentication_client_cert_username_source is not None:
            self.authentication_client_cert_username_source = authentication_client_cert_username_source
        if authentication_client_cert_validate_date_enabled is not None:
            self.authentication_client_cert_validate_date_enabled = authentication_client_cert_validate_date_enabled
        if authentication_kerberos_allow_api_provided_username_enabled is not None:
            self.authentication_kerberos_allow_api_provided_username_enabled = authentication_kerberos_allow_api_provided_username_enabled
        if authentication_kerberos_enabled is not None:
            self.authentication_kerberos_enabled = authentication_kerberos_enabled
        if authentication_oauth_default_provider_name is not None:
            self.authentication_oauth_default_provider_name = authentication_oauth_default_provider_name
        if authentication_oauth_enabled is not None:
            self.authentication_oauth_enabled = authentication_oauth_enabled
        if authorization_ldap_group_membership_attribute_name is not None:
            self.authorization_ldap_group_membership_attribute_name = authorization_ldap_group_membership_attribute_name
        if authorization_ldap_trim_client_username_domain_enabled is not None:
            self.authorization_ldap_trim_client_username_domain_enabled = authorization_ldap_trim_client_username_domain_enabled
        if authorization_profile_name is not None:
            self.authorization_profile_name = authorization_profile_name
        if authorization_type is not None:
            self.authorization_type = authorization_type
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
        if bridging_tls_server_cert_enforce_trusted_common_name_enabled is not None:
            self.bridging_tls_server_cert_enforce_trusted_common_name_enabled = bridging_tls_server_cert_enforce_trusted_common_name_enabled
        if bridging_tls_server_cert_max_chain_depth is not None:
            self.bridging_tls_server_cert_max_chain_depth = bridging_tls_server_cert_max_chain_depth
        if bridging_tls_server_cert_validate_date_enabled is not None:
            self.bridging_tls_server_cert_validate_date_enabled = bridging_tls_server_cert_validate_date_enabled
        if bridging_tls_server_cert_validate_name_enabled is not None:
            self.bridging_tls_server_cert_validate_name_enabled = bridging_tls_server_cert_validate_name_enabled
        if config_sync_local_key is not None:
            self.config_sync_local_key = config_sync_local_key
        if config_sync_local_last_result is not None:
            self.config_sync_local_last_result = config_sync_local_last_result
        if config_sync_local_role is not None:
            self.config_sync_local_role = config_sync_local_role
        if config_sync_local_state is not None:
            self.config_sync_local_state = config_sync_local_state
        if config_sync_local_time_in_state is not None:
            self.config_sync_local_time_in_state = config_sync_local_time_in_state
        if control_rx_byte_count is not None:
            self.control_rx_byte_count = control_rx_byte_count
        if control_rx_msg_count is not None:
            self.control_rx_msg_count = control_rx_msg_count
        if control_tx_byte_count is not None:
            self.control_tx_byte_count = control_tx_byte_count
        if control_tx_msg_count is not None:
            self.control_tx_msg_count = control_tx_msg_count
        if counter is not None:
            self.counter = counter
        if data_rx_byte_count is not None:
            self.data_rx_byte_count = data_rx_byte_count
        if data_rx_msg_count is not None:
            self.data_rx_msg_count = data_rx_msg_count
        if data_tx_byte_count is not None:
            self.data_tx_byte_count = data_tx_byte_count
        if data_tx_msg_count is not None:
            self.data_tx_msg_count = data_tx_msg_count
        if discarded_rx_msg_count is not None:
            self.discarded_rx_msg_count = discarded_rx_msg_count
        if discarded_tx_msg_count is not None:
            self.discarded_tx_msg_count = discarded_tx_msg_count
        if distributed_cache_management_enabled is not None:
            self.distributed_cache_management_enabled = distributed_cache_management_enabled
        if dmr_enabled is not None:
            self.dmr_enabled = dmr_enabled
        if enabled is not None:
            self.enabled = enabled
        if event_connection_count_threshold is not None:
            self.event_connection_count_threshold = event_connection_count_threshold
        if event_egress_flow_count_threshold is not None:
            self.event_egress_flow_count_threshold = event_egress_flow_count_threshold
        if event_egress_msg_rate_threshold is not None:
            self.event_egress_msg_rate_threshold = event_egress_msg_rate_threshold
        if event_endpoint_count_threshold is not None:
            self.event_endpoint_count_threshold = event_endpoint_count_threshold
        if event_ingress_flow_count_threshold is not None:
            self.event_ingress_flow_count_threshold = event_ingress_flow_count_threshold
        if event_ingress_msg_rate_threshold is not None:
            self.event_ingress_msg_rate_threshold = event_ingress_msg_rate_threshold
        if event_large_msg_threshold is not None:
            self.event_large_msg_threshold = event_large_msg_threshold
        if event_log_tag is not None:
            self.event_log_tag = event_log_tag
        if event_msg_spool_usage_threshold is not None:
            self.event_msg_spool_usage_threshold = event_msg_spool_usage_threshold
        if event_publish_client_enabled is not None:
            self.event_publish_client_enabled = event_publish_client_enabled
        if event_publish_msg_vpn_enabled is not None:
            self.event_publish_msg_vpn_enabled = event_publish_msg_vpn_enabled
        if event_publish_subscription_mode is not None:
            self.event_publish_subscription_mode = event_publish_subscription_mode
        if event_publish_topic_format_mqtt_enabled is not None:
            self.event_publish_topic_format_mqtt_enabled = event_publish_topic_format_mqtt_enabled
        if event_publish_topic_format_smf_enabled is not None:
            self.event_publish_topic_format_smf_enabled = event_publish_topic_format_smf_enabled
        if event_service_amqp_connection_count_threshold is not None:
            self.event_service_amqp_connection_count_threshold = event_service_amqp_connection_count_threshold
        if event_service_mqtt_connection_count_threshold is not None:
            self.event_service_mqtt_connection_count_threshold = event_service_mqtt_connection_count_threshold
        if event_service_rest_incoming_connection_count_threshold is not None:
            self.event_service_rest_incoming_connection_count_threshold = event_service_rest_incoming_connection_count_threshold
        if event_service_smf_connection_count_threshold is not None:
            self.event_service_smf_connection_count_threshold = event_service_smf_connection_count_threshold
        if event_service_web_connection_count_threshold is not None:
            self.event_service_web_connection_count_threshold = event_service_web_connection_count_threshold
        if event_subscription_count_threshold is not None:
            self.event_subscription_count_threshold = event_subscription_count_threshold
        if event_transacted_session_count_threshold is not None:
            self.event_transacted_session_count_threshold = event_transacted_session_count_threshold
        if event_transaction_count_threshold is not None:
            self.event_transaction_count_threshold = event_transaction_count_threshold
        if export_subscriptions_enabled is not None:
            self.export_subscriptions_enabled = export_subscriptions_enabled
        if failure_reason is not None:
            self.failure_reason = failure_reason
        if jndi_enabled is not None:
            self.jndi_enabled = jndi_enabled
        if login_rx_msg_count is not None:
            self.login_rx_msg_count = login_rx_msg_count
        if login_tx_msg_count is not None:
            self.login_tx_msg_count = login_tx_msg_count
        if max_connection_count is not None:
            self.max_connection_count = max_connection_count
        if max_effective_endpoint_count is not None:
            self.max_effective_endpoint_count = max_effective_endpoint_count
        if max_effective_rx_flow_count is not None:
            self.max_effective_rx_flow_count = max_effective_rx_flow_count
        if max_effective_subscription_count is not None:
            self.max_effective_subscription_count = max_effective_subscription_count
        if max_effective_transacted_session_count is not None:
            self.max_effective_transacted_session_count = max_effective_transacted_session_count
        if max_effective_transaction_count is not None:
            self.max_effective_transaction_count = max_effective_transaction_count
        if max_effective_tx_flow_count is not None:
            self.max_effective_tx_flow_count = max_effective_tx_flow_count
        if max_egress_flow_count is not None:
            self.max_egress_flow_count = max_egress_flow_count
        if max_endpoint_count is not None:
            self.max_endpoint_count = max_endpoint_count
        if max_ingress_flow_count is not None:
            self.max_ingress_flow_count = max_ingress_flow_count
        if max_msg_spool_usage is not None:
            self.max_msg_spool_usage = max_msg_spool_usage
        if max_subscription_count is not None:
            self.max_subscription_count = max_subscription_count
        if max_transacted_session_count is not None:
            self.max_transacted_session_count = max_transacted_session_count
        if max_transaction_count is not None:
            self.max_transaction_count = max_transaction_count
        if mqtt_retain_max_memory is not None:
            self.mqtt_retain_max_memory = mqtt_retain_max_memory
        if msg_replay_active_count is not None:
            self.msg_replay_active_count = msg_replay_active_count
        if msg_replay_failed_count is not None:
            self.msg_replay_failed_count = msg_replay_failed_count
        if msg_replay_initializing_count is not None:
            self.msg_replay_initializing_count = msg_replay_initializing_count
        if msg_replay_pending_complete_count is not None:
            self.msg_replay_pending_complete_count = msg_replay_pending_complete_count
        if msg_spool_msg_count is not None:
            self.msg_spool_msg_count = msg_spool_msg_count
        if msg_spool_rx_msg_count is not None:
            self.msg_spool_rx_msg_count = msg_spool_rx_msg_count
        if msg_spool_tx_msg_count is not None:
            self.msg_spool_tx_msg_count = msg_spool_tx_msg_count
        if msg_spool_usage is not None:
            self.msg_spool_usage = msg_spool_usage
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if rate is not None:
            self.rate = rate
        if replication_ack_propagation_interval_msg_count is not None:
            self.replication_ack_propagation_interval_msg_count = replication_ack_propagation_interval_msg_count
        if replication_active_ack_prop_tx_msg_count is not None:
            self.replication_active_ack_prop_tx_msg_count = replication_active_ack_prop_tx_msg_count
        if replication_active_async_queued_msg_count is not None:
            self.replication_active_async_queued_msg_count = replication_active_async_queued_msg_count
        if replication_active_locally_consumed_msg_count is not None:
            self.replication_active_locally_consumed_msg_count = replication_active_locally_consumed_msg_count
        if replication_active_mate_flow_congested_peak_time is not None:
            self.replication_active_mate_flow_congested_peak_time = replication_active_mate_flow_congested_peak_time
        if replication_active_mate_flow_not_congested_peak_time is not None:
            self.replication_active_mate_flow_not_congested_peak_time = replication_active_mate_flow_not_congested_peak_time
        if replication_active_promoted_queued_msg_count is not None:
            self.replication_active_promoted_queued_msg_count = replication_active_promoted_queued_msg_count
        if replication_active_reconcile_request_rx_msg_count is not None:
            self.replication_active_reconcile_request_rx_msg_count = replication_active_reconcile_request_rx_msg_count
        if replication_active_sync_eligible_peak_time is not None:
            self.replication_active_sync_eligible_peak_time = replication_active_sync_eligible_peak_time
        if replication_active_sync_ineligible_peak_time is not None:
            self.replication_active_sync_ineligible_peak_time = replication_active_sync_ineligible_peak_time
        if replication_active_sync_queued_as_async_msg_count is not None:
            self.replication_active_sync_queued_as_async_msg_count = replication_active_sync_queued_as_async_msg_count
        if replication_active_sync_queued_msg_count is not None:
            self.replication_active_sync_queued_msg_count = replication_active_sync_queued_msg_count
        if replication_active_transition_to_sync_ineligible_count is not None:
            self.replication_active_transition_to_sync_ineligible_count = replication_active_transition_to_sync_ineligible_count
        if replication_bridge_authentication_basic_client_username is not None:
            self.replication_bridge_authentication_basic_client_username = replication_bridge_authentication_basic_client_username
        if replication_bridge_authentication_scheme is not None:
            self.replication_bridge_authentication_scheme = replication_bridge_authentication_scheme
        if replication_bridge_bound_to_queue is not None:
            self.replication_bridge_bound_to_queue = replication_bridge_bound_to_queue
        if replication_bridge_compressed_data_enabled is not None:
            self.replication_bridge_compressed_data_enabled = replication_bridge_compressed_data_enabled
        if replication_bridge_egress_flow_window_size is not None:
            self.replication_bridge_egress_flow_window_size = replication_bridge_egress_flow_window_size
        if replication_bridge_name is not None:
            self.replication_bridge_name = replication_bridge_name
        if replication_bridge_retry_delay is not None:
            self.replication_bridge_retry_delay = replication_bridge_retry_delay
        if replication_bridge_tls_enabled is not None:
            self.replication_bridge_tls_enabled = replication_bridge_tls_enabled
        if replication_bridge_unidirectional_client_profile_name is not None:
            self.replication_bridge_unidirectional_client_profile_name = replication_bridge_unidirectional_client_profile_name
        if replication_bridge_up is not None:
            self.replication_bridge_up = replication_bridge_up
        if replication_enabled is not None:
            self.replication_enabled = replication_enabled
        if replication_queue_bound is not None:
            self.replication_queue_bound = replication_queue_bound
        if replication_queue_max_msg_spool_usage is not None:
            self.replication_queue_max_msg_spool_usage = replication_queue_max_msg_spool_usage
        if replication_queue_reject_msg_to_sender_on_discard_enabled is not None:
            self.replication_queue_reject_msg_to_sender_on_discard_enabled = replication_queue_reject_msg_to_sender_on_discard_enabled
        if replication_reject_msg_when_sync_ineligible_enabled is not None:
            self.replication_reject_msg_when_sync_ineligible_enabled = replication_reject_msg_when_sync_ineligible_enabled
        if replication_remote_bridge_name is not None:
            self.replication_remote_bridge_name = replication_remote_bridge_name
        if replication_remote_bridge_up is not None:
            self.replication_remote_bridge_up = replication_remote_bridge_up
        if replication_role is not None:
            self.replication_role = replication_role
        if replication_standby_ack_prop_out_of_seq_rx_msg_count is not None:
            self.replication_standby_ack_prop_out_of_seq_rx_msg_count = replication_standby_ack_prop_out_of_seq_rx_msg_count
        if replication_standby_ack_prop_rx_msg_count is not None:
            self.replication_standby_ack_prop_rx_msg_count = replication_standby_ack_prop_rx_msg_count
        if replication_standby_reconcile_request_tx_msg_count is not None:
            self.replication_standby_reconcile_request_tx_msg_count = replication_standby_reconcile_request_tx_msg_count
        if replication_standby_rx_msg_count is not None:
            self.replication_standby_rx_msg_count = replication_standby_rx_msg_count
        if replication_standby_transaction_request_count is not None:
            self.replication_standby_transaction_request_count = replication_standby_transaction_request_count
        if replication_standby_transaction_request_failure_count is not None:
            self.replication_standby_transaction_request_failure_count = replication_standby_transaction_request_failure_count
        if replication_standby_transaction_request_success_count is not None:
            self.replication_standby_transaction_request_success_count = replication_standby_transaction_request_success_count
        if replication_sync_eligible is not None:
            self.replication_sync_eligible = replication_sync_eligible
        if replication_transaction_mode is not None:
            self.replication_transaction_mode = replication_transaction_mode
        if rest_tls_server_cert_enforce_trusted_common_name_enabled is not None:
            self.rest_tls_server_cert_enforce_trusted_common_name_enabled = rest_tls_server_cert_enforce_trusted_common_name_enabled
        if rest_tls_server_cert_max_chain_depth is not None:
            self.rest_tls_server_cert_max_chain_depth = rest_tls_server_cert_max_chain_depth
        if rest_tls_server_cert_validate_date_enabled is not None:
            self.rest_tls_server_cert_validate_date_enabled = rest_tls_server_cert_validate_date_enabled
        if rest_tls_server_cert_validate_name_enabled is not None:
            self.rest_tls_server_cert_validate_name_enabled = rest_tls_server_cert_validate_name_enabled
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
        if semp_over_msg_bus_admin_client_enabled is not None:
            self.semp_over_msg_bus_admin_client_enabled = semp_over_msg_bus_admin_client_enabled
        if semp_over_msg_bus_admin_distributed_cache_enabled is not None:
            self.semp_over_msg_bus_admin_distributed_cache_enabled = semp_over_msg_bus_admin_distributed_cache_enabled
        if semp_over_msg_bus_admin_enabled is not None:
            self.semp_over_msg_bus_admin_enabled = semp_over_msg_bus_admin_enabled
        if semp_over_msg_bus_enabled is not None:
            self.semp_over_msg_bus_enabled = semp_over_msg_bus_enabled
        if semp_over_msg_bus_show_enabled is not None:
            self.semp_over_msg_bus_show_enabled = semp_over_msg_bus_show_enabled
        if service_amqp_max_connection_count is not None:
            self.service_amqp_max_connection_count = service_amqp_max_connection_count
        if service_amqp_plain_text_compressed is not None:
            self.service_amqp_plain_text_compressed = service_amqp_plain_text_compressed
        if service_amqp_plain_text_enabled is not None:
            self.service_amqp_plain_text_enabled = service_amqp_plain_text_enabled
        if service_amqp_plain_text_failure_reason is not None:
            self.service_amqp_plain_text_failure_reason = service_amqp_plain_text_failure_reason
        if service_amqp_plain_text_listen_port is not None:
            self.service_amqp_plain_text_listen_port = service_amqp_plain_text_listen_port
        if service_amqp_plain_text_up is not None:
            self.service_amqp_plain_text_up = service_amqp_plain_text_up
        if service_amqp_tls_compressed is not None:
            self.service_amqp_tls_compressed = service_amqp_tls_compressed
        if service_amqp_tls_enabled is not None:
            self.service_amqp_tls_enabled = service_amqp_tls_enabled
        if service_amqp_tls_failure_reason is not None:
            self.service_amqp_tls_failure_reason = service_amqp_tls_failure_reason
        if service_amqp_tls_listen_port is not None:
            self.service_amqp_tls_listen_port = service_amqp_tls_listen_port
        if service_amqp_tls_up is not None:
            self.service_amqp_tls_up = service_amqp_tls_up
        if service_mqtt_max_connection_count is not None:
            self.service_mqtt_max_connection_count = service_mqtt_max_connection_count
        if service_mqtt_plain_text_compressed is not None:
            self.service_mqtt_plain_text_compressed = service_mqtt_plain_text_compressed
        if service_mqtt_plain_text_enabled is not None:
            self.service_mqtt_plain_text_enabled = service_mqtt_plain_text_enabled
        if service_mqtt_plain_text_failure_reason is not None:
            self.service_mqtt_plain_text_failure_reason = service_mqtt_plain_text_failure_reason
        if service_mqtt_plain_text_listen_port is not None:
            self.service_mqtt_plain_text_listen_port = service_mqtt_plain_text_listen_port
        if service_mqtt_plain_text_up is not None:
            self.service_mqtt_plain_text_up = service_mqtt_plain_text_up
        if service_mqtt_tls_compressed is not None:
            self.service_mqtt_tls_compressed = service_mqtt_tls_compressed
        if service_mqtt_tls_enabled is not None:
            self.service_mqtt_tls_enabled = service_mqtt_tls_enabled
        if service_mqtt_tls_failure_reason is not None:
            self.service_mqtt_tls_failure_reason = service_mqtt_tls_failure_reason
        if service_mqtt_tls_listen_port is not None:
            self.service_mqtt_tls_listen_port = service_mqtt_tls_listen_port
        if service_mqtt_tls_up is not None:
            self.service_mqtt_tls_up = service_mqtt_tls_up
        if service_mqtt_tls_web_socket_compressed is not None:
            self.service_mqtt_tls_web_socket_compressed = service_mqtt_tls_web_socket_compressed
        if service_mqtt_tls_web_socket_enabled is not None:
            self.service_mqtt_tls_web_socket_enabled = service_mqtt_tls_web_socket_enabled
        if service_mqtt_tls_web_socket_failure_reason is not None:
            self.service_mqtt_tls_web_socket_failure_reason = service_mqtt_tls_web_socket_failure_reason
        if service_mqtt_tls_web_socket_listen_port is not None:
            self.service_mqtt_tls_web_socket_listen_port = service_mqtt_tls_web_socket_listen_port
        if service_mqtt_tls_web_socket_up is not None:
            self.service_mqtt_tls_web_socket_up = service_mqtt_tls_web_socket_up
        if service_mqtt_web_socket_compressed is not None:
            self.service_mqtt_web_socket_compressed = service_mqtt_web_socket_compressed
        if service_mqtt_web_socket_enabled is not None:
            self.service_mqtt_web_socket_enabled = service_mqtt_web_socket_enabled
        if service_mqtt_web_socket_failure_reason is not None:
            self.service_mqtt_web_socket_failure_reason = service_mqtt_web_socket_failure_reason
        if service_mqtt_web_socket_listen_port is not None:
            self.service_mqtt_web_socket_listen_port = service_mqtt_web_socket_listen_port
        if service_mqtt_web_socket_up is not None:
            self.service_mqtt_web_socket_up = service_mqtt_web_socket_up
        if service_rest_incoming_max_connection_count is not None:
            self.service_rest_incoming_max_connection_count = service_rest_incoming_max_connection_count
        if service_rest_incoming_plain_text_compressed is not None:
            self.service_rest_incoming_plain_text_compressed = service_rest_incoming_plain_text_compressed
        if service_rest_incoming_plain_text_enabled is not None:
            self.service_rest_incoming_plain_text_enabled = service_rest_incoming_plain_text_enabled
        if service_rest_incoming_plain_text_failure_reason is not None:
            self.service_rest_incoming_plain_text_failure_reason = service_rest_incoming_plain_text_failure_reason
        if service_rest_incoming_plain_text_listen_port is not None:
            self.service_rest_incoming_plain_text_listen_port = service_rest_incoming_plain_text_listen_port
        if service_rest_incoming_plain_text_up is not None:
            self.service_rest_incoming_plain_text_up = service_rest_incoming_plain_text_up
        if service_rest_incoming_tls_compressed is not None:
            self.service_rest_incoming_tls_compressed = service_rest_incoming_tls_compressed
        if service_rest_incoming_tls_enabled is not None:
            self.service_rest_incoming_tls_enabled = service_rest_incoming_tls_enabled
        if service_rest_incoming_tls_failure_reason is not None:
            self.service_rest_incoming_tls_failure_reason = service_rest_incoming_tls_failure_reason
        if service_rest_incoming_tls_listen_port is not None:
            self.service_rest_incoming_tls_listen_port = service_rest_incoming_tls_listen_port
        if service_rest_incoming_tls_up is not None:
            self.service_rest_incoming_tls_up = service_rest_incoming_tls_up
        if service_rest_mode is not None:
            self.service_rest_mode = service_rest_mode
        if service_rest_outgoing_max_connection_count is not None:
            self.service_rest_outgoing_max_connection_count = service_rest_outgoing_max_connection_count
        if service_smf_max_connection_count is not None:
            self.service_smf_max_connection_count = service_smf_max_connection_count
        if service_smf_plain_text_enabled is not None:
            self.service_smf_plain_text_enabled = service_smf_plain_text_enabled
        if service_smf_plain_text_failure_reason is not None:
            self.service_smf_plain_text_failure_reason = service_smf_plain_text_failure_reason
        if service_smf_plain_text_up is not None:
            self.service_smf_plain_text_up = service_smf_plain_text_up
        if service_smf_tls_enabled is not None:
            self.service_smf_tls_enabled = service_smf_tls_enabled
        if service_smf_tls_failure_reason is not None:
            self.service_smf_tls_failure_reason = service_smf_tls_failure_reason
        if service_smf_tls_up is not None:
            self.service_smf_tls_up = service_smf_tls_up
        if service_web_max_connection_count is not None:
            self.service_web_max_connection_count = service_web_max_connection_count
        if service_web_plain_text_enabled is not None:
            self.service_web_plain_text_enabled = service_web_plain_text_enabled
        if service_web_plain_text_failure_reason is not None:
            self.service_web_plain_text_failure_reason = service_web_plain_text_failure_reason
        if service_web_plain_text_up is not None:
            self.service_web_plain_text_up = service_web_plain_text_up
        if service_web_tls_enabled is not None:
            self.service_web_tls_enabled = service_web_tls_enabled
        if service_web_tls_failure_reason is not None:
            self.service_web_tls_failure_reason = service_web_tls_failure_reason
        if service_web_tls_up is not None:
            self.service_web_tls_up = service_web_tls_up
        if state is not None:
            self.state = state
        if subscription_export_progress is not None:
            self.subscription_export_progress = subscription_export_progress
        if system_manager is not None:
            self.system_manager = system_manager
        if tls_allow_downgrade_to_plain_text_enabled is not None:
            self.tls_allow_downgrade_to_plain_text_enabled = tls_allow_downgrade_to_plain_text_enabled
        if tls_average_rx_byte_rate is not None:
            self.tls_average_rx_byte_rate = tls_average_rx_byte_rate
        if tls_average_tx_byte_rate is not None:
            self.tls_average_tx_byte_rate = tls_average_tx_byte_rate
        if tls_rx_byte_count is not None:
            self.tls_rx_byte_count = tls_rx_byte_count
        if tls_rx_byte_rate is not None:
            self.tls_rx_byte_rate = tls_rx_byte_rate
        if tls_tx_byte_count is not None:
            self.tls_tx_byte_count = tls_tx_byte_count
        if tls_tx_byte_rate is not None:
            self.tls_tx_byte_rate = tls_tx_byte_rate
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
    def alias(self):
        """Gets the alias of this MsgVpn.  # noqa: E501

        The name of another Message VPN which this Message VPN is an alias for. Available since 2.14.  # noqa: E501

        :return: The alias of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this MsgVpn.

        The name of another Message VPN which this Message VPN is an alias for. Available since 2.14.  # noqa: E501

        :param alias: The alias of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._alias = alias

    @property
    def authentication_basic_enabled(self):
        """Gets the authentication_basic_enabled of this MsgVpn.  # noqa: E501

        Indicates whether basic authentication is enabled for clients connecting to the Message VPN.  # noqa: E501

        :return: The authentication_basic_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_basic_enabled

    @authentication_basic_enabled.setter
    def authentication_basic_enabled(self, authentication_basic_enabled):
        """Sets the authentication_basic_enabled of this MsgVpn.

        Indicates whether basic authentication is enabled for clients connecting to the Message VPN.  # noqa: E501

        :param authentication_basic_enabled: The authentication_basic_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_basic_enabled = authentication_basic_enabled

    @property
    def authentication_basic_profile_name(self):
        """Gets the authentication_basic_profile_name of this MsgVpn.  # noqa: E501

        The name of the RADIUS or LDAP Profile to use for basic authentication.  # noqa: E501

        :return: The authentication_basic_profile_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_basic_profile_name

    @authentication_basic_profile_name.setter
    def authentication_basic_profile_name(self, authentication_basic_profile_name):
        """Sets the authentication_basic_profile_name of this MsgVpn.

        The name of the RADIUS or LDAP Profile to use for basic authentication.  # noqa: E501

        :param authentication_basic_profile_name: The authentication_basic_profile_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._authentication_basic_profile_name = authentication_basic_profile_name

    @property
    def authentication_basic_radius_domain(self):
        """Gets the authentication_basic_radius_domain of this MsgVpn.  # noqa: E501

        The RADIUS domain to use for basic authentication.  # noqa: E501

        :return: The authentication_basic_radius_domain of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_basic_radius_domain

    @authentication_basic_radius_domain.setter
    def authentication_basic_radius_domain(self, authentication_basic_radius_domain):
        """Sets the authentication_basic_radius_domain of this MsgVpn.

        The RADIUS domain to use for basic authentication.  # noqa: E501

        :param authentication_basic_radius_domain: The authentication_basic_radius_domain of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._authentication_basic_radius_domain = authentication_basic_radius_domain

    @property
    def authentication_basic_type(self):
        """Gets the authentication_basic_type of this MsgVpn.  # noqa: E501

        The type of basic authentication to use for clients connecting to the Message VPN. The allowed values and their meaning are:  <pre> \"internal\" - Internal database. Authentication is against Client Usernames. \"ldap\" - LDAP authentication. An LDAP profile name must be provided. \"radius\" - RADIUS authentication. A RADIUS profile name must be provided. \"none\" - No authentication. Anonymous login allowed. </pre>   # noqa: E501

        :return: The authentication_basic_type of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_basic_type

    @authentication_basic_type.setter
    def authentication_basic_type(self, authentication_basic_type):
        """Sets the authentication_basic_type of this MsgVpn.

        The type of basic authentication to use for clients connecting to the Message VPN. The allowed values and their meaning are:  <pre> \"internal\" - Internal database. Authentication is against Client Usernames. \"ldap\" - LDAP authentication. An LDAP profile name must be provided. \"radius\" - RADIUS authentication. A RADIUS profile name must be provided. \"none\" - No authentication. Anonymous login allowed. </pre>   # noqa: E501

        :param authentication_basic_type: The authentication_basic_type of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["internal", "ldap", "radius", "none"]  # noqa: E501
        if authentication_basic_type not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_basic_type` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_basic_type, allowed_values)
            )

        self._authentication_basic_type = authentication_basic_type

    @property
    def authentication_client_cert_allow_api_provided_username_enabled(self):
        """Gets the authentication_client_cert_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501

        Indicates whether a client is allowed to specify a Client Username via the API connect method. When disabled, the certificate CN (Common Name) is always used.  # noqa: E501

        :return: The authentication_client_cert_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_client_cert_allow_api_provided_username_enabled

    @authentication_client_cert_allow_api_provided_username_enabled.setter
    def authentication_client_cert_allow_api_provided_username_enabled(self, authentication_client_cert_allow_api_provided_username_enabled):
        """Sets the authentication_client_cert_allow_api_provided_username_enabled of this MsgVpn.

        Indicates whether a client is allowed to specify a Client Username via the API connect method. When disabled, the certificate CN (Common Name) is always used.  # noqa: E501

        :param authentication_client_cert_allow_api_provided_username_enabled: The authentication_client_cert_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_client_cert_allow_api_provided_username_enabled = authentication_client_cert_allow_api_provided_username_enabled

    @property
    def authentication_client_cert_enabled(self):
        """Gets the authentication_client_cert_enabled of this MsgVpn.  # noqa: E501

        Indicates whether client certificate authentication is enabled in the Message VPN.  # noqa: E501

        :return: The authentication_client_cert_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_client_cert_enabled

    @authentication_client_cert_enabled.setter
    def authentication_client_cert_enabled(self, authentication_client_cert_enabled):
        """Sets the authentication_client_cert_enabled of this MsgVpn.

        Indicates whether client certificate authentication is enabled in the Message VPN.  # noqa: E501

        :param authentication_client_cert_enabled: The authentication_client_cert_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_client_cert_enabled = authentication_client_cert_enabled

    @property
    def authentication_client_cert_max_chain_depth(self):
        """Gets the authentication_client_cert_max_chain_depth of this MsgVpn.  # noqa: E501

        The maximum depth for a client certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :return: The authentication_client_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._authentication_client_cert_max_chain_depth

    @authentication_client_cert_max_chain_depth.setter
    def authentication_client_cert_max_chain_depth(self, authentication_client_cert_max_chain_depth):
        """Sets the authentication_client_cert_max_chain_depth of this MsgVpn.

        The maximum depth for a client certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :param authentication_client_cert_max_chain_depth: The authentication_client_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._authentication_client_cert_max_chain_depth = authentication_client_cert_max_chain_depth

    @property
    def authentication_client_cert_revocation_check_mode(self):
        """Gets the authentication_client_cert_revocation_check_mode of this MsgVpn.  # noqa: E501

        The desired behavior for client certificate revocation checking. The allowed values and their meaning are:  <pre> \"allow-all\" - Allow the client to authenticate, the result of client certificate revocation check is ignored. \"allow-unknown\" - Allow the client to authenticate even if the revocation status of his certificate cannot be determined. \"allow-valid\" - Allow the client to authenticate only when the revocation check returned an explicit positive response. </pre>   # noqa: E501

        :return: The authentication_client_cert_revocation_check_mode of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_client_cert_revocation_check_mode

    @authentication_client_cert_revocation_check_mode.setter
    def authentication_client_cert_revocation_check_mode(self, authentication_client_cert_revocation_check_mode):
        """Sets the authentication_client_cert_revocation_check_mode of this MsgVpn.

        The desired behavior for client certificate revocation checking. The allowed values and their meaning are:  <pre> \"allow-all\" - Allow the client to authenticate, the result of client certificate revocation check is ignored. \"allow-unknown\" - Allow the client to authenticate even if the revocation status of his certificate cannot be determined. \"allow-valid\" - Allow the client to authenticate only when the revocation check returned an explicit positive response. </pre>   # noqa: E501

        :param authentication_client_cert_revocation_check_mode: The authentication_client_cert_revocation_check_mode of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["allow-all", "allow-unknown", "allow-valid"]  # noqa: E501
        if authentication_client_cert_revocation_check_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_client_cert_revocation_check_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_client_cert_revocation_check_mode, allowed_values)
            )

        self._authentication_client_cert_revocation_check_mode = authentication_client_cert_revocation_check_mode

    @property
    def authentication_client_cert_username_source(self):
        """Gets the authentication_client_cert_username_source of this MsgVpn.  # noqa: E501

        The field from the client certificate to use as the client username. The allowed values and their meaning are:  <pre> \"common-name\" - The username is extracted from the certificate's Common Name. \"subject-alternate-name-msupn\" - The username is extracted from the certificate's Other Name type of the Subject Alternative Name and must have the msUPN signature. </pre>   # noqa: E501

        :return: The authentication_client_cert_username_source of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_client_cert_username_source

    @authentication_client_cert_username_source.setter
    def authentication_client_cert_username_source(self, authentication_client_cert_username_source):
        """Sets the authentication_client_cert_username_source of this MsgVpn.

        The field from the client certificate to use as the client username. The allowed values and their meaning are:  <pre> \"common-name\" - The username is extracted from the certificate's Common Name. \"subject-alternate-name-msupn\" - The username is extracted from the certificate's Other Name type of the Subject Alternative Name and must have the msUPN signature. </pre>   # noqa: E501

        :param authentication_client_cert_username_source: The authentication_client_cert_username_source of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["common-name", "subject-alternate-name-msupn"]  # noqa: E501
        if authentication_client_cert_username_source not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_client_cert_username_source` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_client_cert_username_source, allowed_values)
            )

        self._authentication_client_cert_username_source = authentication_client_cert_username_source

    @property
    def authentication_client_cert_validate_date_enabled(self):
        """Gets the authentication_client_cert_validate_date_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the client certificate are checked.  # noqa: E501

        :return: The authentication_client_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_client_cert_validate_date_enabled

    @authentication_client_cert_validate_date_enabled.setter
    def authentication_client_cert_validate_date_enabled(self, authentication_client_cert_validate_date_enabled):
        """Sets the authentication_client_cert_validate_date_enabled of this MsgVpn.

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the client certificate are checked.  # noqa: E501

        :param authentication_client_cert_validate_date_enabled: The authentication_client_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_client_cert_validate_date_enabled = authentication_client_cert_validate_date_enabled

    @property
    def authentication_kerberos_allow_api_provided_username_enabled(self):
        """Gets the authentication_kerberos_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501

        Indicates whether a client is allowed to specify a Client Username via the API connect method. When disabled, the Kerberos Principal name is always used.  # noqa: E501

        :return: The authentication_kerberos_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_kerberos_allow_api_provided_username_enabled

    @authentication_kerberos_allow_api_provided_username_enabled.setter
    def authentication_kerberos_allow_api_provided_username_enabled(self, authentication_kerberos_allow_api_provided_username_enabled):
        """Sets the authentication_kerberos_allow_api_provided_username_enabled of this MsgVpn.

        Indicates whether a client is allowed to specify a Client Username via the API connect method. When disabled, the Kerberos Principal name is always used.  # noqa: E501

        :param authentication_kerberos_allow_api_provided_username_enabled: The authentication_kerberos_allow_api_provided_username_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_kerberos_allow_api_provided_username_enabled = authentication_kerberos_allow_api_provided_username_enabled

    @property
    def authentication_kerberos_enabled(self):
        """Gets the authentication_kerberos_enabled of this MsgVpn.  # noqa: E501

        Indicates whether Kerberos authentication is enabled in the Message VPN.  # noqa: E501

        :return: The authentication_kerberos_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_kerberos_enabled

    @authentication_kerberos_enabled.setter
    def authentication_kerberos_enabled(self, authentication_kerberos_enabled):
        """Sets the authentication_kerberos_enabled of this MsgVpn.

        Indicates whether Kerberos authentication is enabled in the Message VPN.  # noqa: E501

        :param authentication_kerberos_enabled: The authentication_kerberos_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_kerberos_enabled = authentication_kerberos_enabled

    @property
    def authentication_oauth_default_provider_name(self):
        """Gets the authentication_oauth_default_provider_name of this MsgVpn.  # noqa: E501

        The name of the provider to use when the client does not supply a provider name. Available since 2.13.  # noqa: E501

        :return: The authentication_oauth_default_provider_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authentication_oauth_default_provider_name

    @authentication_oauth_default_provider_name.setter
    def authentication_oauth_default_provider_name(self, authentication_oauth_default_provider_name):
        """Sets the authentication_oauth_default_provider_name of this MsgVpn.

        The name of the provider to use when the client does not supply a provider name. Available since 2.13.  # noqa: E501

        :param authentication_oauth_default_provider_name: The authentication_oauth_default_provider_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._authentication_oauth_default_provider_name = authentication_oauth_default_provider_name

    @property
    def authentication_oauth_enabled(self):
        """Gets the authentication_oauth_enabled of this MsgVpn.  # noqa: E501

        Indicates whether OAuth authentication is enabled. Available since 2.13.  # noqa: E501

        :return: The authentication_oauth_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_oauth_enabled

    @authentication_oauth_enabled.setter
    def authentication_oauth_enabled(self, authentication_oauth_enabled):
        """Sets the authentication_oauth_enabled of this MsgVpn.

        Indicates whether OAuth authentication is enabled. Available since 2.13.  # noqa: E501

        :param authentication_oauth_enabled: The authentication_oauth_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authentication_oauth_enabled = authentication_oauth_enabled

    @property
    def authorization_ldap_group_membership_attribute_name(self):
        """Gets the authorization_ldap_group_membership_attribute_name of this MsgVpn.  # noqa: E501

        The name of the attribute that is retrieved from the LDAP server as part of the LDAP search when authorizing a client connecting to the Message VPN.  # noqa: E501

        :return: The authorization_ldap_group_membership_attribute_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authorization_ldap_group_membership_attribute_name

    @authorization_ldap_group_membership_attribute_name.setter
    def authorization_ldap_group_membership_attribute_name(self, authorization_ldap_group_membership_attribute_name):
        """Sets the authorization_ldap_group_membership_attribute_name of this MsgVpn.

        The name of the attribute that is retrieved from the LDAP server as part of the LDAP search when authorizing a client connecting to the Message VPN.  # noqa: E501

        :param authorization_ldap_group_membership_attribute_name: The authorization_ldap_group_membership_attribute_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._authorization_ldap_group_membership_attribute_name = authorization_ldap_group_membership_attribute_name

    @property
    def authorization_ldap_trim_client_username_domain_enabled(self):
        """Gets the authorization_ldap_trim_client_username_domain_enabled of this MsgVpn.  # noqa: E501

        Indicates whether client-username domain trimming for LDAP lookups of client connections is enabled. Available since 2.13.  # noqa: E501

        :return: The authorization_ldap_trim_client_username_domain_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._authorization_ldap_trim_client_username_domain_enabled

    @authorization_ldap_trim_client_username_domain_enabled.setter
    def authorization_ldap_trim_client_username_domain_enabled(self, authorization_ldap_trim_client_username_domain_enabled):
        """Sets the authorization_ldap_trim_client_username_domain_enabled of this MsgVpn.

        Indicates whether client-username domain trimming for LDAP lookups of client connections is enabled. Available since 2.13.  # noqa: E501

        :param authorization_ldap_trim_client_username_domain_enabled: The authorization_ldap_trim_client_username_domain_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._authorization_ldap_trim_client_username_domain_enabled = authorization_ldap_trim_client_username_domain_enabled

    @property
    def authorization_profile_name(self):
        """Gets the authorization_profile_name of this MsgVpn.  # noqa: E501

        The name of the LDAP Profile to use for client authorization.  # noqa: E501

        :return: The authorization_profile_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authorization_profile_name

    @authorization_profile_name.setter
    def authorization_profile_name(self, authorization_profile_name):
        """Sets the authorization_profile_name of this MsgVpn.

        The name of the LDAP Profile to use for client authorization.  # noqa: E501

        :param authorization_profile_name: The authorization_profile_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._authorization_profile_name = authorization_profile_name

    @property
    def authorization_type(self):
        """Gets the authorization_type of this MsgVpn.  # noqa: E501

        The type of authorization to use for clients connecting to the Message VPN. The allowed values and their meaning are:  <pre> \"ldap\" - LDAP authorization. \"internal\" - Internal authorization. </pre>   # noqa: E501

        :return: The authorization_type of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._authorization_type

    @authorization_type.setter
    def authorization_type(self, authorization_type):
        """Sets the authorization_type of this MsgVpn.

        The type of authorization to use for clients connecting to the Message VPN. The allowed values and their meaning are:  <pre> \"ldap\" - LDAP authorization. \"internal\" - Internal authorization. </pre>   # noqa: E501

        :param authorization_type: The authorization_type of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["ldap", "internal"]  # noqa: E501
        if authorization_type not in allowed_values:
            raise ValueError(
                "Invalid value for `authorization_type` ({0}), must be one of {1}"  # noqa: E501
                .format(authorization_type, allowed_values)
            )

        self._authorization_type = authorization_type

    @property
    def average_rx_byte_rate(self):
        """Gets the average_rx_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The average_rx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_byte_rate

    @average_rx_byte_rate.setter
    def average_rx_byte_rate(self, average_rx_byte_rate):
        """Sets the average_rx_byte_rate of this MsgVpn.

        The one minute average of the message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param average_rx_byte_rate: The average_rx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_rx_byte_rate = average_rx_byte_rate

    @property
    def average_rx_compressed_byte_rate(self):
        """Gets the average_rx_compressed_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the compressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The average_rx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_compressed_byte_rate

    @average_rx_compressed_byte_rate.setter
    def average_rx_compressed_byte_rate(self, average_rx_compressed_byte_rate):
        """Sets the average_rx_compressed_byte_rate of this MsgVpn.

        The one minute average of the compressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param average_rx_compressed_byte_rate: The average_rx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_rx_compressed_byte_rate = average_rx_compressed_byte_rate

    @property
    def average_rx_msg_rate(self):
        """Gets the average_rx_msg_rate of this MsgVpn.  # noqa: E501

        The one minute average of the message rate received by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_rx_msg_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_msg_rate

    @average_rx_msg_rate.setter
    def average_rx_msg_rate(self, average_rx_msg_rate):
        """Sets the average_rx_msg_rate of this MsgVpn.

        The one minute average of the message rate received by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_rx_msg_rate: The average_rx_msg_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_rx_msg_rate = average_rx_msg_rate

    @property
    def average_rx_uncompressed_byte_rate(self):
        """Gets the average_rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the uncompressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The average_rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_rx_uncompressed_byte_rate

    @average_rx_uncompressed_byte_rate.setter
    def average_rx_uncompressed_byte_rate(self, average_rx_uncompressed_byte_rate):
        """Sets the average_rx_uncompressed_byte_rate of this MsgVpn.

        The one minute average of the uncompressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param average_rx_uncompressed_byte_rate: The average_rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_rx_uncompressed_byte_rate = average_rx_uncompressed_byte_rate

    @property
    def average_tx_byte_rate(self):
        """Gets the average_tx_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The average_tx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_byte_rate

    @average_tx_byte_rate.setter
    def average_tx_byte_rate(self, average_tx_byte_rate):
        """Sets the average_tx_byte_rate of this MsgVpn.

        The one minute average of the message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param average_tx_byte_rate: The average_tx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_tx_byte_rate = average_tx_byte_rate

    @property
    def average_tx_compressed_byte_rate(self):
        """Gets the average_tx_compressed_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the compressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The average_tx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_compressed_byte_rate

    @average_tx_compressed_byte_rate.setter
    def average_tx_compressed_byte_rate(self, average_tx_compressed_byte_rate):
        """Sets the average_tx_compressed_byte_rate of this MsgVpn.

        The one minute average of the compressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param average_tx_compressed_byte_rate: The average_tx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_tx_compressed_byte_rate = average_tx_compressed_byte_rate

    @property
    def average_tx_msg_rate(self):
        """Gets the average_tx_msg_rate of this MsgVpn.  # noqa: E501

        The one minute average of the message rate transmitted by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_tx_msg_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_msg_rate

    @average_tx_msg_rate.setter
    def average_tx_msg_rate(self, average_tx_msg_rate):
        """Sets the average_tx_msg_rate of this MsgVpn.

        The one minute average of the message rate transmitted by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_tx_msg_rate: The average_tx_msg_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_tx_msg_rate = average_tx_msg_rate

    @property
    def average_tx_uncompressed_byte_rate(self):
        """Gets the average_tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the uncompressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The average_tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._average_tx_uncompressed_byte_rate

    @average_tx_uncompressed_byte_rate.setter
    def average_tx_uncompressed_byte_rate(self, average_tx_uncompressed_byte_rate):
        """Sets the average_tx_uncompressed_byte_rate of this MsgVpn.

        The one minute average of the uncompressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param average_tx_uncompressed_byte_rate: The average_tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._average_tx_uncompressed_byte_rate = average_tx_uncompressed_byte_rate

    @property
    def bridging_tls_server_cert_enforce_trusted_common_name_enabled(self):
        """Gets the bridging_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the Common Name (CN) in the server certificate from the remote broker is validated for the Bridge. Deprecated since 2.18. Common Name validation has been replaced by Server Certificate Name validation.  # noqa: E501

        :return: The bridging_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._bridging_tls_server_cert_enforce_trusted_common_name_enabled

    @bridging_tls_server_cert_enforce_trusted_common_name_enabled.setter
    def bridging_tls_server_cert_enforce_trusted_common_name_enabled(self, bridging_tls_server_cert_enforce_trusted_common_name_enabled):
        """Sets the bridging_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.

        Indicates whether the Common Name (CN) in the server certificate from the remote broker is validated for the Bridge. Deprecated since 2.18. Common Name validation has been replaced by Server Certificate Name validation.  # noqa: E501

        :param bridging_tls_server_cert_enforce_trusted_common_name_enabled: The bridging_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._bridging_tls_server_cert_enforce_trusted_common_name_enabled = bridging_tls_server_cert_enforce_trusted_common_name_enabled

    @property
    def bridging_tls_server_cert_max_chain_depth(self):
        """Gets the bridging_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501

        The maximum depth for a server certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :return: The bridging_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._bridging_tls_server_cert_max_chain_depth

    @bridging_tls_server_cert_max_chain_depth.setter
    def bridging_tls_server_cert_max_chain_depth(self, bridging_tls_server_cert_max_chain_depth):
        """Sets the bridging_tls_server_cert_max_chain_depth of this MsgVpn.

        The maximum depth for a server certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :param bridging_tls_server_cert_max_chain_depth: The bridging_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._bridging_tls_server_cert_max_chain_depth = bridging_tls_server_cert_max_chain_depth

    @property
    def bridging_tls_server_cert_validate_date_enabled(self):
        """Gets the bridging_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the server certificate are checked.  # noqa: E501

        :return: The bridging_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._bridging_tls_server_cert_validate_date_enabled

    @bridging_tls_server_cert_validate_date_enabled.setter
    def bridging_tls_server_cert_validate_date_enabled(self, bridging_tls_server_cert_validate_date_enabled):
        """Sets the bridging_tls_server_cert_validate_date_enabled of this MsgVpn.

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the server certificate are checked.  # noqa: E501

        :param bridging_tls_server_cert_validate_date_enabled: The bridging_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._bridging_tls_server_cert_validate_date_enabled = bridging_tls_server_cert_validate_date_enabled

    @property
    def bridging_tls_server_cert_validate_name_enabled(self):
        """Gets the bridging_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501

        Enable or disable the standard TLS authentication mechanism of verifying the name used to connect to the bridge. If enabled, the name used to connect to the bridge is checked against the names specified in the certificate returned by the remote router. Legacy Common Name validation is not performed if Server Certificate Name Validation is enabled, even if Common Name validation is also enabled. Available since 2.18.  # noqa: E501

        :return: The bridging_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._bridging_tls_server_cert_validate_name_enabled

    @bridging_tls_server_cert_validate_name_enabled.setter
    def bridging_tls_server_cert_validate_name_enabled(self, bridging_tls_server_cert_validate_name_enabled):
        """Sets the bridging_tls_server_cert_validate_name_enabled of this MsgVpn.

        Enable or disable the standard TLS authentication mechanism of verifying the name used to connect to the bridge. If enabled, the name used to connect to the bridge is checked against the names specified in the certificate returned by the remote router. Legacy Common Name validation is not performed if Server Certificate Name Validation is enabled, even if Common Name validation is also enabled. Available since 2.18.  # noqa: E501

        :param bridging_tls_server_cert_validate_name_enabled: The bridging_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._bridging_tls_server_cert_validate_name_enabled = bridging_tls_server_cert_validate_name_enabled

    @property
    def config_sync_local_key(self):
        """Gets the config_sync_local_key of this MsgVpn.  # noqa: E501

        The key for the config sync table of the local Message VPN. Available since 2.12.  # noqa: E501

        :return: The config_sync_local_key of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._config_sync_local_key

    @config_sync_local_key.setter
    def config_sync_local_key(self, config_sync_local_key):
        """Sets the config_sync_local_key of this MsgVpn.

        The key for the config sync table of the local Message VPN. Available since 2.12.  # noqa: E501

        :param config_sync_local_key: The config_sync_local_key of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._config_sync_local_key = config_sync_local_key

    @property
    def config_sync_local_last_result(self):
        """Gets the config_sync_local_last_result of this MsgVpn.  # noqa: E501

        The result of the last operation on the config sync table of the local Message VPN. Available since 2.12.  # noqa: E501

        :return: The config_sync_local_last_result of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._config_sync_local_last_result

    @config_sync_local_last_result.setter
    def config_sync_local_last_result(self, config_sync_local_last_result):
        """Sets the config_sync_local_last_result of this MsgVpn.

        The result of the last operation on the config sync table of the local Message VPN. Available since 2.12.  # noqa: E501

        :param config_sync_local_last_result: The config_sync_local_last_result of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._config_sync_local_last_result = config_sync_local_last_result

    @property
    def config_sync_local_role(self):
        """Gets the config_sync_local_role of this MsgVpn.  # noqa: E501

        The role of the config sync table of the local Message VPN. The allowed values and their meaning are:  <pre> \"unknown\" - The role is unknown. \"primary\" - Acts as the primary source of config data. \"replica\" - Acts as a replica of the primary config data. </pre>  Available since 2.12.  # noqa: E501

        :return: The config_sync_local_role of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._config_sync_local_role

    @config_sync_local_role.setter
    def config_sync_local_role(self, config_sync_local_role):
        """Sets the config_sync_local_role of this MsgVpn.

        The role of the config sync table of the local Message VPN. The allowed values and their meaning are:  <pre> \"unknown\" - The role is unknown. \"primary\" - Acts as the primary source of config data. \"replica\" - Acts as a replica of the primary config data. </pre>  Available since 2.12.  # noqa: E501

        :param config_sync_local_role: The config_sync_local_role of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._config_sync_local_role = config_sync_local_role

    @property
    def config_sync_local_state(self):
        """Gets the config_sync_local_state of this MsgVpn.  # noqa: E501

        The state of the config sync table of the local Message VPN. The allowed values and their meaning are:  <pre> \"unknown\" - The state is unknown. \"in-sync\" - The config data is synchronized between Message VPNs. \"reconciling\" - The config data is reconciling between Message VPNs. \"blocked\" - The config data is blocked from reconciling due to an error. \"out-of-sync\" - The config data is out of sync between Message VPNs. \"down\" - The state is down due to configuration. </pre>  Available since 2.12.  # noqa: E501

        :return: The config_sync_local_state of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._config_sync_local_state

    @config_sync_local_state.setter
    def config_sync_local_state(self, config_sync_local_state):
        """Sets the config_sync_local_state of this MsgVpn.

        The state of the config sync table of the local Message VPN. The allowed values and their meaning are:  <pre> \"unknown\" - The state is unknown. \"in-sync\" - The config data is synchronized between Message VPNs. \"reconciling\" - The config data is reconciling between Message VPNs. \"blocked\" - The config data is blocked from reconciling due to an error. \"out-of-sync\" - The config data is out of sync between Message VPNs. \"down\" - The state is down due to configuration. </pre>  Available since 2.12.  # noqa: E501

        :param config_sync_local_state: The config_sync_local_state of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._config_sync_local_state = config_sync_local_state

    @property
    def config_sync_local_time_in_state(self):
        """Gets the config_sync_local_time_in_state of this MsgVpn.  # noqa: E501

        The amount of time in seconds the config sync table of the local Message VPN has been in the current state. Available since 2.12.  # noqa: E501

        :return: The config_sync_local_time_in_state of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._config_sync_local_time_in_state

    @config_sync_local_time_in_state.setter
    def config_sync_local_time_in_state(self, config_sync_local_time_in_state):
        """Sets the config_sync_local_time_in_state of this MsgVpn.

        The amount of time in seconds the config sync table of the local Message VPN has been in the current state. Available since 2.12.  # noqa: E501

        :param config_sync_local_time_in_state: The config_sync_local_time_in_state of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._config_sync_local_time_in_state = config_sync_local_time_in_state

    @property
    def control_rx_byte_count(self):
        """Gets the control_rx_byte_count of this MsgVpn.  # noqa: E501

        The amount of client control messages received from clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The control_rx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._control_rx_byte_count

    @control_rx_byte_count.setter
    def control_rx_byte_count(self, control_rx_byte_count):
        """Sets the control_rx_byte_count of this MsgVpn.

        The amount of client control messages received from clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param control_rx_byte_count: The control_rx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._control_rx_byte_count = control_rx_byte_count

    @property
    def control_rx_msg_count(self):
        """Gets the control_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of client control messages received from clients by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The control_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._control_rx_msg_count

    @control_rx_msg_count.setter
    def control_rx_msg_count(self, control_rx_msg_count):
        """Sets the control_rx_msg_count of this MsgVpn.

        The number of client control messages received from clients by the Message VPN. Available since 2.13.  # noqa: E501

        :param control_rx_msg_count: The control_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._control_rx_msg_count = control_rx_msg_count

    @property
    def control_tx_byte_count(self):
        """Gets the control_tx_byte_count of this MsgVpn.  # noqa: E501

        The amount of client control messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The control_tx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._control_tx_byte_count

    @control_tx_byte_count.setter
    def control_tx_byte_count(self, control_tx_byte_count):
        """Sets the control_tx_byte_count of this MsgVpn.

        The amount of client control messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param control_tx_byte_count: The control_tx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._control_tx_byte_count = control_tx_byte_count

    @property
    def control_tx_msg_count(self):
        """Gets the control_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of client control messages transmitted to clients by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The control_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._control_tx_msg_count

    @control_tx_msg_count.setter
    def control_tx_msg_count(self, control_tx_msg_count):
        """Sets the control_tx_msg_count of this MsgVpn.

        The number of client control messages transmitted to clients by the Message VPN. Available since 2.13.  # noqa: E501

        :param control_tx_msg_count: The control_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._control_tx_msg_count = control_tx_msg_count

    @property
    def counter(self):
        """Gets the counter of this MsgVpn.  # noqa: E501


        :return: The counter of this MsgVpn.  # noqa: E501
        :rtype: MsgVpnCounter
        """
        return self._counter

    @counter.setter
    def counter(self, counter):
        """Sets the counter of this MsgVpn.


        :param counter: The counter of this MsgVpn.  # noqa: E501
        :type: MsgVpnCounter
        """

        self._counter = counter

    @property
    def data_rx_byte_count(self):
        """Gets the data_rx_byte_count of this MsgVpn.  # noqa: E501

        The amount of client data messages received from clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The data_rx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_byte_count

    @data_rx_byte_count.setter
    def data_rx_byte_count(self, data_rx_byte_count):
        """Sets the data_rx_byte_count of this MsgVpn.

        The amount of client data messages received from clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param data_rx_byte_count: The data_rx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._data_rx_byte_count = data_rx_byte_count

    @property
    def data_rx_msg_count(self):
        """Gets the data_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of client data messages received from clients by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The data_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_msg_count

    @data_rx_msg_count.setter
    def data_rx_msg_count(self, data_rx_msg_count):
        """Sets the data_rx_msg_count of this MsgVpn.

        The number of client data messages received from clients by the Message VPN. Available since 2.13.  # noqa: E501

        :param data_rx_msg_count: The data_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._data_rx_msg_count = data_rx_msg_count

    @property
    def data_tx_byte_count(self):
        """Gets the data_tx_byte_count of this MsgVpn.  # noqa: E501

        The amount of client data messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The data_tx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_byte_count

    @data_tx_byte_count.setter
    def data_tx_byte_count(self, data_tx_byte_count):
        """Sets the data_tx_byte_count of this MsgVpn.

        The amount of client data messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param data_tx_byte_count: The data_tx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._data_tx_byte_count = data_tx_byte_count

    @property
    def data_tx_msg_count(self):
        """Gets the data_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of client data messages transmitted to clients by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The data_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_msg_count

    @data_tx_msg_count.setter
    def data_tx_msg_count(self, data_tx_msg_count):
        """Sets the data_tx_msg_count of this MsgVpn.

        The number of client data messages transmitted to clients by the Message VPN. Available since 2.13.  # noqa: E501

        :param data_tx_msg_count: The data_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._data_tx_msg_count = data_tx_msg_count

    @property
    def discarded_rx_msg_count(self):
        """Gets the discarded_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of messages discarded during reception by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The discarded_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._discarded_rx_msg_count

    @discarded_rx_msg_count.setter
    def discarded_rx_msg_count(self, discarded_rx_msg_count):
        """Sets the discarded_rx_msg_count of this MsgVpn.

        The number of messages discarded during reception by the Message VPN. Available since 2.13.  # noqa: E501

        :param discarded_rx_msg_count: The discarded_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._discarded_rx_msg_count = discarded_rx_msg_count

    @property
    def discarded_tx_msg_count(self):
        """Gets the discarded_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of messages discarded during transmission by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The discarded_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._discarded_tx_msg_count

    @discarded_tx_msg_count.setter
    def discarded_tx_msg_count(self, discarded_tx_msg_count):
        """Sets the discarded_tx_msg_count of this MsgVpn.

        The number of messages discarded during transmission by the Message VPN. Available since 2.13.  # noqa: E501

        :param discarded_tx_msg_count: The discarded_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._discarded_tx_msg_count = discarded_tx_msg_count

    @property
    def distributed_cache_management_enabled(self):
        """Gets the distributed_cache_management_enabled of this MsgVpn.  # noqa: E501

        Indicates whether managing of cache instances over the message bus is enabled in the Message VPN.  # noqa: E501

        :return: The distributed_cache_management_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._distributed_cache_management_enabled

    @distributed_cache_management_enabled.setter
    def distributed_cache_management_enabled(self, distributed_cache_management_enabled):
        """Sets the distributed_cache_management_enabled of this MsgVpn.

        Indicates whether managing of cache instances over the message bus is enabled in the Message VPN.  # noqa: E501

        :param distributed_cache_management_enabled: The distributed_cache_management_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._distributed_cache_management_enabled = distributed_cache_management_enabled

    @property
    def dmr_enabled(self):
        """Gets the dmr_enabled of this MsgVpn.  # noqa: E501

        Indicates whether Dynamic Message Routing (DMR) is enabled for the Message VPN.  # noqa: E501

        :return: The dmr_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._dmr_enabled

    @dmr_enabled.setter
    def dmr_enabled(self, dmr_enabled):
        """Sets the dmr_enabled of this MsgVpn.

        Indicates whether Dynamic Message Routing (DMR) is enabled for the Message VPN.  # noqa: E501

        :param dmr_enabled: The dmr_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._dmr_enabled = dmr_enabled

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpn.  # noqa: E501

        Indicates whether the Message VPN is enabled.  # noqa: E501

        :return: The enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpn.

        Indicates whether the Message VPN is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def event_connection_count_threshold(self):
        """Gets the event_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_connection_count_threshold

    @event_connection_count_threshold.setter
    def event_connection_count_threshold(self, event_connection_count_threshold):
        """Sets the event_connection_count_threshold of this MsgVpn.


        :param event_connection_count_threshold: The event_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_connection_count_threshold = event_connection_count_threshold

    @property
    def event_egress_flow_count_threshold(self):
        """Gets the event_egress_flow_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_egress_flow_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_egress_flow_count_threshold

    @event_egress_flow_count_threshold.setter
    def event_egress_flow_count_threshold(self, event_egress_flow_count_threshold):
        """Sets the event_egress_flow_count_threshold of this MsgVpn.


        :param event_egress_flow_count_threshold: The event_egress_flow_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_egress_flow_count_threshold = event_egress_flow_count_threshold

    @property
    def event_egress_msg_rate_threshold(self):
        """Gets the event_egress_msg_rate_threshold of this MsgVpn.  # noqa: E501


        :return: The event_egress_msg_rate_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_egress_msg_rate_threshold

    @event_egress_msg_rate_threshold.setter
    def event_egress_msg_rate_threshold(self, event_egress_msg_rate_threshold):
        """Sets the event_egress_msg_rate_threshold of this MsgVpn.


        :param event_egress_msg_rate_threshold: The event_egress_msg_rate_threshold of this MsgVpn.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_egress_msg_rate_threshold = event_egress_msg_rate_threshold

    @property
    def event_endpoint_count_threshold(self):
        """Gets the event_endpoint_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_endpoint_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_endpoint_count_threshold

    @event_endpoint_count_threshold.setter
    def event_endpoint_count_threshold(self, event_endpoint_count_threshold):
        """Sets the event_endpoint_count_threshold of this MsgVpn.


        :param event_endpoint_count_threshold: The event_endpoint_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_endpoint_count_threshold = event_endpoint_count_threshold

    @property
    def event_ingress_flow_count_threshold(self):
        """Gets the event_ingress_flow_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_ingress_flow_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_ingress_flow_count_threshold

    @event_ingress_flow_count_threshold.setter
    def event_ingress_flow_count_threshold(self, event_ingress_flow_count_threshold):
        """Sets the event_ingress_flow_count_threshold of this MsgVpn.


        :param event_ingress_flow_count_threshold: The event_ingress_flow_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_ingress_flow_count_threshold = event_ingress_flow_count_threshold

    @property
    def event_ingress_msg_rate_threshold(self):
        """Gets the event_ingress_msg_rate_threshold of this MsgVpn.  # noqa: E501


        :return: The event_ingress_msg_rate_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_ingress_msg_rate_threshold

    @event_ingress_msg_rate_threshold.setter
    def event_ingress_msg_rate_threshold(self, event_ingress_msg_rate_threshold):
        """Sets the event_ingress_msg_rate_threshold of this MsgVpn.


        :param event_ingress_msg_rate_threshold: The event_ingress_msg_rate_threshold of this MsgVpn.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_ingress_msg_rate_threshold = event_ingress_msg_rate_threshold

    @property
    def event_large_msg_threshold(self):
        """Gets the event_large_msg_threshold of this MsgVpn.  # noqa: E501

        Exceeding this message size in kilobytes (KB) triggers a corresponding Event in the Message VPN.  # noqa: E501

        :return: The event_large_msg_threshold of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._event_large_msg_threshold

    @event_large_msg_threshold.setter
    def event_large_msg_threshold(self, event_large_msg_threshold):
        """Sets the event_large_msg_threshold of this MsgVpn.

        Exceeding this message size in kilobytes (KB) triggers a corresponding Event in the Message VPN.  # noqa: E501

        :param event_large_msg_threshold: The event_large_msg_threshold of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._event_large_msg_threshold = event_large_msg_threshold

    @property
    def event_log_tag(self):
        """Gets the event_log_tag of this MsgVpn.  # noqa: E501

        The value of the prefix applied to all published Events in the Message VPN.  # noqa: E501

        :return: The event_log_tag of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._event_log_tag

    @event_log_tag.setter
    def event_log_tag(self, event_log_tag):
        """Sets the event_log_tag of this MsgVpn.

        The value of the prefix applied to all published Events in the Message VPN.  # noqa: E501

        :param event_log_tag: The event_log_tag of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._event_log_tag = event_log_tag

    @property
    def event_msg_spool_usage_threshold(self):
        """Gets the event_msg_spool_usage_threshold of this MsgVpn.  # noqa: E501


        :return: The event_msg_spool_usage_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_msg_spool_usage_threshold

    @event_msg_spool_usage_threshold.setter
    def event_msg_spool_usage_threshold(self, event_msg_spool_usage_threshold):
        """Sets the event_msg_spool_usage_threshold of this MsgVpn.


        :param event_msg_spool_usage_threshold: The event_msg_spool_usage_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_msg_spool_usage_threshold = event_msg_spool_usage_threshold

    @property
    def event_publish_client_enabled(self):
        """Gets the event_publish_client_enabled of this MsgVpn.  # noqa: E501

        Indicates whether client Events are published in the Message VPN.  # noqa: E501

        :return: The event_publish_client_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._event_publish_client_enabled

    @event_publish_client_enabled.setter
    def event_publish_client_enabled(self, event_publish_client_enabled):
        """Sets the event_publish_client_enabled of this MsgVpn.

        Indicates whether client Events are published in the Message VPN.  # noqa: E501

        :param event_publish_client_enabled: The event_publish_client_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._event_publish_client_enabled = event_publish_client_enabled

    @property
    def event_publish_msg_vpn_enabled(self):
        """Gets the event_publish_msg_vpn_enabled of this MsgVpn.  # noqa: E501

        Indicates whether Message VPN Events are published in the Message VPN.  # noqa: E501

        :return: The event_publish_msg_vpn_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._event_publish_msg_vpn_enabled

    @event_publish_msg_vpn_enabled.setter
    def event_publish_msg_vpn_enabled(self, event_publish_msg_vpn_enabled):
        """Sets the event_publish_msg_vpn_enabled of this MsgVpn.

        Indicates whether Message VPN Events are published in the Message VPN.  # noqa: E501

        :param event_publish_msg_vpn_enabled: The event_publish_msg_vpn_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._event_publish_msg_vpn_enabled = event_publish_msg_vpn_enabled

    @property
    def event_publish_subscription_mode(self):
        """Gets the event_publish_subscription_mode of this MsgVpn.  # noqa: E501

        The mode of subscription Events published in the Message VPN. The allowed values and their meaning are:  <pre> \"off\" - Disable client level event message publishing. \"on-with-format-v1\" - Enable client level event message publishing with format v1. \"on-with-no-unsubscribe-events-on-disconnect-format-v1\" - As \"on-with-format-v1\", but unsubscribe events are not generated when a client disconnects. Unsubscribe events are still raised when a client explicitly unsubscribes from its subscriptions. \"on-with-format-v2\" - Enable client level event message publishing with format v2. \"on-with-no-unsubscribe-events-on-disconnect-format-v2\" - As \"on-with-format-v2\", but unsubscribe events are not generated when a client disconnects. Unsubscribe events are still raised when a client explicitly unsubscribes from its subscriptions. </pre>   # noqa: E501

        :return: The event_publish_subscription_mode of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._event_publish_subscription_mode

    @event_publish_subscription_mode.setter
    def event_publish_subscription_mode(self, event_publish_subscription_mode):
        """Sets the event_publish_subscription_mode of this MsgVpn.

        The mode of subscription Events published in the Message VPN. The allowed values and their meaning are:  <pre> \"off\" - Disable client level event message publishing. \"on-with-format-v1\" - Enable client level event message publishing with format v1. \"on-with-no-unsubscribe-events-on-disconnect-format-v1\" - As \"on-with-format-v1\", but unsubscribe events are not generated when a client disconnects. Unsubscribe events are still raised when a client explicitly unsubscribes from its subscriptions. \"on-with-format-v2\" - Enable client level event message publishing with format v2. \"on-with-no-unsubscribe-events-on-disconnect-format-v2\" - As \"on-with-format-v2\", but unsubscribe events are not generated when a client disconnects. Unsubscribe events are still raised when a client explicitly unsubscribes from its subscriptions. </pre>   # noqa: E501

        :param event_publish_subscription_mode: The event_publish_subscription_mode of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["off", "on-with-format-v1", "on-with-no-unsubscribe-events-on-disconnect-format-v1", "on-with-format-v2", "on-with-no-unsubscribe-events-on-disconnect-format-v2"]  # noqa: E501
        if event_publish_subscription_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `event_publish_subscription_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(event_publish_subscription_mode, allowed_values)
            )

        self._event_publish_subscription_mode = event_publish_subscription_mode

    @property
    def event_publish_topic_format_mqtt_enabled(self):
        """Gets the event_publish_topic_format_mqtt_enabled of this MsgVpn.  # noqa: E501

        Indicates whether Message VPN Events are published in the MQTT format.  # noqa: E501

        :return: The event_publish_topic_format_mqtt_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._event_publish_topic_format_mqtt_enabled

    @event_publish_topic_format_mqtt_enabled.setter
    def event_publish_topic_format_mqtt_enabled(self, event_publish_topic_format_mqtt_enabled):
        """Sets the event_publish_topic_format_mqtt_enabled of this MsgVpn.

        Indicates whether Message VPN Events are published in the MQTT format.  # noqa: E501

        :param event_publish_topic_format_mqtt_enabled: The event_publish_topic_format_mqtt_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._event_publish_topic_format_mqtt_enabled = event_publish_topic_format_mqtt_enabled

    @property
    def event_publish_topic_format_smf_enabled(self):
        """Gets the event_publish_topic_format_smf_enabled of this MsgVpn.  # noqa: E501

        Indicates whether Message VPN Events are published in the SMF format.  # noqa: E501

        :return: The event_publish_topic_format_smf_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._event_publish_topic_format_smf_enabled

    @event_publish_topic_format_smf_enabled.setter
    def event_publish_topic_format_smf_enabled(self, event_publish_topic_format_smf_enabled):
        """Sets the event_publish_topic_format_smf_enabled of this MsgVpn.

        Indicates whether Message VPN Events are published in the SMF format.  # noqa: E501

        :param event_publish_topic_format_smf_enabled: The event_publish_topic_format_smf_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._event_publish_topic_format_smf_enabled = event_publish_topic_format_smf_enabled

    @property
    def event_service_amqp_connection_count_threshold(self):
        """Gets the event_service_amqp_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_service_amqp_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_amqp_connection_count_threshold

    @event_service_amqp_connection_count_threshold.setter
    def event_service_amqp_connection_count_threshold(self, event_service_amqp_connection_count_threshold):
        """Sets the event_service_amqp_connection_count_threshold of this MsgVpn.


        :param event_service_amqp_connection_count_threshold: The event_service_amqp_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_amqp_connection_count_threshold = event_service_amqp_connection_count_threshold

    @property
    def event_service_mqtt_connection_count_threshold(self):
        """Gets the event_service_mqtt_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_service_mqtt_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_mqtt_connection_count_threshold

    @event_service_mqtt_connection_count_threshold.setter
    def event_service_mqtt_connection_count_threshold(self, event_service_mqtt_connection_count_threshold):
        """Sets the event_service_mqtt_connection_count_threshold of this MsgVpn.


        :param event_service_mqtt_connection_count_threshold: The event_service_mqtt_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_mqtt_connection_count_threshold = event_service_mqtt_connection_count_threshold

    @property
    def event_service_rest_incoming_connection_count_threshold(self):
        """Gets the event_service_rest_incoming_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_service_rest_incoming_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_rest_incoming_connection_count_threshold

    @event_service_rest_incoming_connection_count_threshold.setter
    def event_service_rest_incoming_connection_count_threshold(self, event_service_rest_incoming_connection_count_threshold):
        """Sets the event_service_rest_incoming_connection_count_threshold of this MsgVpn.


        :param event_service_rest_incoming_connection_count_threshold: The event_service_rest_incoming_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_rest_incoming_connection_count_threshold = event_service_rest_incoming_connection_count_threshold

    @property
    def event_service_smf_connection_count_threshold(self):
        """Gets the event_service_smf_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_service_smf_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_smf_connection_count_threshold

    @event_service_smf_connection_count_threshold.setter
    def event_service_smf_connection_count_threshold(self, event_service_smf_connection_count_threshold):
        """Sets the event_service_smf_connection_count_threshold of this MsgVpn.


        :param event_service_smf_connection_count_threshold: The event_service_smf_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_smf_connection_count_threshold = event_service_smf_connection_count_threshold

    @property
    def event_service_web_connection_count_threshold(self):
        """Gets the event_service_web_connection_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_service_web_connection_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_service_web_connection_count_threshold

    @event_service_web_connection_count_threshold.setter
    def event_service_web_connection_count_threshold(self, event_service_web_connection_count_threshold):
        """Sets the event_service_web_connection_count_threshold of this MsgVpn.


        :param event_service_web_connection_count_threshold: The event_service_web_connection_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_service_web_connection_count_threshold = event_service_web_connection_count_threshold

    @property
    def event_subscription_count_threshold(self):
        """Gets the event_subscription_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_subscription_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_subscription_count_threshold

    @event_subscription_count_threshold.setter
    def event_subscription_count_threshold(self, event_subscription_count_threshold):
        """Sets the event_subscription_count_threshold of this MsgVpn.


        :param event_subscription_count_threshold: The event_subscription_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_subscription_count_threshold = event_subscription_count_threshold

    @property
    def event_transacted_session_count_threshold(self):
        """Gets the event_transacted_session_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_transacted_session_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_transacted_session_count_threshold

    @event_transacted_session_count_threshold.setter
    def event_transacted_session_count_threshold(self, event_transacted_session_count_threshold):
        """Sets the event_transacted_session_count_threshold of this MsgVpn.


        :param event_transacted_session_count_threshold: The event_transacted_session_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_transacted_session_count_threshold = event_transacted_session_count_threshold

    @property
    def event_transaction_count_threshold(self):
        """Gets the event_transaction_count_threshold of this MsgVpn.  # noqa: E501


        :return: The event_transaction_count_threshold of this MsgVpn.  # noqa: E501
        :rtype: EventThreshold
        """
        return self._event_transaction_count_threshold

    @event_transaction_count_threshold.setter
    def event_transaction_count_threshold(self, event_transaction_count_threshold):
        """Sets the event_transaction_count_threshold of this MsgVpn.


        :param event_transaction_count_threshold: The event_transaction_count_threshold of this MsgVpn.  # noqa: E501
        :type: EventThreshold
        """

        self._event_transaction_count_threshold = event_transaction_count_threshold

    @property
    def export_subscriptions_enabled(self):
        """Gets the export_subscriptions_enabled of this MsgVpn.  # noqa: E501

        Indicates whether exports of subscriptions to other routers in the network over neighbour links is enabled in the Message VPN.  # noqa: E501

        :return: The export_subscriptions_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._export_subscriptions_enabled

    @export_subscriptions_enabled.setter
    def export_subscriptions_enabled(self, export_subscriptions_enabled):
        """Sets the export_subscriptions_enabled of this MsgVpn.

        Indicates whether exports of subscriptions to other routers in the network over neighbour links is enabled in the Message VPN.  # noqa: E501

        :param export_subscriptions_enabled: The export_subscriptions_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._export_subscriptions_enabled = export_subscriptions_enabled

    @property
    def failure_reason(self):
        """Gets the failure_reason of this MsgVpn.  # noqa: E501

        The reason for the Message VPN failure.  # noqa: E501

        :return: The failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """Sets the failure_reason of this MsgVpn.

        The reason for the Message VPN failure.  # noqa: E501

        :param failure_reason: The failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._failure_reason = failure_reason

    @property
    def jndi_enabled(self):
        """Gets the jndi_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the JNDI access for clients is enabled in the Message VPN.  # noqa: E501

        :return: The jndi_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._jndi_enabled

    @jndi_enabled.setter
    def jndi_enabled(self, jndi_enabled):
        """Sets the jndi_enabled of this MsgVpn.

        Indicates whether the JNDI access for clients is enabled in the Message VPN.  # noqa: E501

        :param jndi_enabled: The jndi_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._jndi_enabled = jndi_enabled

    @property
    def login_rx_msg_count(self):
        """Gets the login_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of login request messages received by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The login_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._login_rx_msg_count

    @login_rx_msg_count.setter
    def login_rx_msg_count(self, login_rx_msg_count):
        """Sets the login_rx_msg_count of this MsgVpn.

        The number of login request messages received by the Message VPN. Available since 2.13.  # noqa: E501

        :param login_rx_msg_count: The login_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._login_rx_msg_count = login_rx_msg_count

    @property
    def login_tx_msg_count(self):
        """Gets the login_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of login response messages transmitted by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The login_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._login_tx_msg_count

    @login_tx_msg_count.setter
    def login_tx_msg_count(self, login_tx_msg_count):
        """Sets the login_tx_msg_count of this MsgVpn.

        The number of login response messages transmitted by the Message VPN. Available since 2.13.  # noqa: E501

        :param login_tx_msg_count: The login_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._login_tx_msg_count = login_tx_msg_count

    @property
    def max_connection_count(self):
        """Gets the max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of client connections to the Message VPN.  # noqa: E501

        :return: The max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_connection_count

    @max_connection_count.setter
    def max_connection_count(self, max_connection_count):
        """Sets the max_connection_count of this MsgVpn.

        The maximum number of client connections to the Message VPN.  # noqa: E501

        :param max_connection_count: The max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_connection_count = max_connection_count

    @property
    def max_effective_endpoint_count(self):
        """Gets the max_effective_endpoint_count of this MsgVpn.  # noqa: E501

        The effective maximum number of Queues and Topic Endpoints allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_endpoint_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_endpoint_count

    @max_effective_endpoint_count.setter
    def max_effective_endpoint_count(self, max_effective_endpoint_count):
        """Sets the max_effective_endpoint_count of this MsgVpn.

        The effective maximum number of Queues and Topic Endpoints allowed in the Message VPN.  # noqa: E501

        :param max_effective_endpoint_count: The max_effective_endpoint_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_endpoint_count = max_effective_endpoint_count

    @property
    def max_effective_rx_flow_count(self):
        """Gets the max_effective_rx_flow_count of this MsgVpn.  # noqa: E501

        The effective maximum number of receive flows allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_rx_flow_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_rx_flow_count

    @max_effective_rx_flow_count.setter
    def max_effective_rx_flow_count(self, max_effective_rx_flow_count):
        """Sets the max_effective_rx_flow_count of this MsgVpn.

        The effective maximum number of receive flows allowed in the Message VPN.  # noqa: E501

        :param max_effective_rx_flow_count: The max_effective_rx_flow_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_rx_flow_count = max_effective_rx_flow_count

    @property
    def max_effective_subscription_count(self):
        """Gets the max_effective_subscription_count of this MsgVpn.  # noqa: E501

        The effective maximum number of subscriptions allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_subscription_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_subscription_count

    @max_effective_subscription_count.setter
    def max_effective_subscription_count(self, max_effective_subscription_count):
        """Sets the max_effective_subscription_count of this MsgVpn.

        The effective maximum number of subscriptions allowed in the Message VPN.  # noqa: E501

        :param max_effective_subscription_count: The max_effective_subscription_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_subscription_count = max_effective_subscription_count

    @property
    def max_effective_transacted_session_count(self):
        """Gets the max_effective_transacted_session_count of this MsgVpn.  # noqa: E501

        The effective maximum number of transacted sessions allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_transacted_session_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_transacted_session_count

    @max_effective_transacted_session_count.setter
    def max_effective_transacted_session_count(self, max_effective_transacted_session_count):
        """Sets the max_effective_transacted_session_count of this MsgVpn.

        The effective maximum number of transacted sessions allowed in the Message VPN.  # noqa: E501

        :param max_effective_transacted_session_count: The max_effective_transacted_session_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_transacted_session_count = max_effective_transacted_session_count

    @property
    def max_effective_transaction_count(self):
        """Gets the max_effective_transaction_count of this MsgVpn.  # noqa: E501

        The effective maximum number of transactions allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_transaction_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_transaction_count

    @max_effective_transaction_count.setter
    def max_effective_transaction_count(self, max_effective_transaction_count):
        """Sets the max_effective_transaction_count of this MsgVpn.

        The effective maximum number of transactions allowed in the Message VPN.  # noqa: E501

        :param max_effective_transaction_count: The max_effective_transaction_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_transaction_count = max_effective_transaction_count

    @property
    def max_effective_tx_flow_count(self):
        """Gets the max_effective_tx_flow_count of this MsgVpn.  # noqa: E501

        The effective maximum number of transmit flows allowed in the Message VPN.  # noqa: E501

        :return: The max_effective_tx_flow_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_effective_tx_flow_count

    @max_effective_tx_flow_count.setter
    def max_effective_tx_flow_count(self, max_effective_tx_flow_count):
        """Sets the max_effective_tx_flow_count of this MsgVpn.

        The effective maximum number of transmit flows allowed in the Message VPN.  # noqa: E501

        :param max_effective_tx_flow_count: The max_effective_tx_flow_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_effective_tx_flow_count = max_effective_tx_flow_count

    @property
    def max_egress_flow_count(self):
        """Gets the max_egress_flow_count of this MsgVpn.  # noqa: E501

        The maximum number of transmit flows that can be created in the Message VPN.  # noqa: E501

        :return: The max_egress_flow_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_egress_flow_count

    @max_egress_flow_count.setter
    def max_egress_flow_count(self, max_egress_flow_count):
        """Sets the max_egress_flow_count of this MsgVpn.

        The maximum number of transmit flows that can be created in the Message VPN.  # noqa: E501

        :param max_egress_flow_count: The max_egress_flow_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_egress_flow_count = max_egress_flow_count

    @property
    def max_endpoint_count(self):
        """Gets the max_endpoint_count of this MsgVpn.  # noqa: E501

        The maximum number of Queues and Topic Endpoints that can be created in the Message VPN.  # noqa: E501

        :return: The max_endpoint_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_endpoint_count

    @max_endpoint_count.setter
    def max_endpoint_count(self, max_endpoint_count):
        """Sets the max_endpoint_count of this MsgVpn.

        The maximum number of Queues and Topic Endpoints that can be created in the Message VPN.  # noqa: E501

        :param max_endpoint_count: The max_endpoint_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_endpoint_count = max_endpoint_count

    @property
    def max_ingress_flow_count(self):
        """Gets the max_ingress_flow_count of this MsgVpn.  # noqa: E501

        The maximum number of receive flows that can be created in the Message VPN.  # noqa: E501

        :return: The max_ingress_flow_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_ingress_flow_count

    @max_ingress_flow_count.setter
    def max_ingress_flow_count(self, max_ingress_flow_count):
        """Sets the max_ingress_flow_count of this MsgVpn.

        The maximum number of receive flows that can be created in the Message VPN.  # noqa: E501

        :param max_ingress_flow_count: The max_ingress_flow_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_ingress_flow_count = max_ingress_flow_count

    @property
    def max_msg_spool_usage(self):
        """Gets the max_msg_spool_usage of this MsgVpn.  # noqa: E501

        The maximum message spool usage by the Message VPN, in megabytes.  # noqa: E501

        :return: The max_msg_spool_usage of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_spool_usage

    @max_msg_spool_usage.setter
    def max_msg_spool_usage(self, max_msg_spool_usage):
        """Sets the max_msg_spool_usage of this MsgVpn.

        The maximum message spool usage by the Message VPN, in megabytes.  # noqa: E501

        :param max_msg_spool_usage: The max_msg_spool_usage of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_msg_spool_usage = max_msg_spool_usage

    @property
    def max_subscription_count(self):
        """Gets the max_subscription_count of this MsgVpn.  # noqa: E501

        The maximum number of local client subscriptions that can be added to the Message VPN. This limit is not enforced when a subscription is added using a management interface, such as CLI or SEMP.  # noqa: E501

        :return: The max_subscription_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_subscription_count

    @max_subscription_count.setter
    def max_subscription_count(self, max_subscription_count):
        """Sets the max_subscription_count of this MsgVpn.

        The maximum number of local client subscriptions that can be added to the Message VPN. This limit is not enforced when a subscription is added using a management interface, such as CLI or SEMP.  # noqa: E501

        :param max_subscription_count: The max_subscription_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_subscription_count = max_subscription_count

    @property
    def max_transacted_session_count(self):
        """Gets the max_transacted_session_count of this MsgVpn.  # noqa: E501

        The maximum number of transacted sessions that can be created in the Message VPN.  # noqa: E501

        :return: The max_transacted_session_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_transacted_session_count

    @max_transacted_session_count.setter
    def max_transacted_session_count(self, max_transacted_session_count):
        """Sets the max_transacted_session_count of this MsgVpn.

        The maximum number of transacted sessions that can be created in the Message VPN.  # noqa: E501

        :param max_transacted_session_count: The max_transacted_session_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_transacted_session_count = max_transacted_session_count

    @property
    def max_transaction_count(self):
        """Gets the max_transaction_count of this MsgVpn.  # noqa: E501

        The maximum number of transactions that can be created in the Message VPN.  # noqa: E501

        :return: The max_transaction_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._max_transaction_count

    @max_transaction_count.setter
    def max_transaction_count(self, max_transaction_count):
        """Sets the max_transaction_count of this MsgVpn.

        The maximum number of transactions that can be created in the Message VPN.  # noqa: E501

        :param max_transaction_count: The max_transaction_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._max_transaction_count = max_transaction_count

    @property
    def mqtt_retain_max_memory(self):
        """Gets the mqtt_retain_max_memory of this MsgVpn.  # noqa: E501

        The maximum total memory usage of the MQTT Retain feature for this Message VPN, in MB. If the maximum memory is reached, any arriving retain messages that require more memory are discarded. A value of -1 indicates that the memory is bounded only by the global max memory limit. A value of 0 prevents MQTT Retain from becoming operational.  # noqa: E501

        :return: The mqtt_retain_max_memory of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._mqtt_retain_max_memory

    @mqtt_retain_max_memory.setter
    def mqtt_retain_max_memory(self, mqtt_retain_max_memory):
        """Sets the mqtt_retain_max_memory of this MsgVpn.

        The maximum total memory usage of the MQTT Retain feature for this Message VPN, in MB. If the maximum memory is reached, any arriving retain messages that require more memory are discarded. A value of -1 indicates that the memory is bounded only by the global max memory limit. A value of 0 prevents MQTT Retain from becoming operational.  # noqa: E501

        :param mqtt_retain_max_memory: The mqtt_retain_max_memory of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._mqtt_retain_max_memory = mqtt_retain_max_memory

    @property
    def msg_replay_active_count(self):
        """Gets the msg_replay_active_count of this MsgVpn.  # noqa: E501

        The number of message replays that are currently active in the Message VPN.  # noqa: E501

        :return: The msg_replay_active_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_replay_active_count

    @msg_replay_active_count.setter
    def msg_replay_active_count(self, msg_replay_active_count):
        """Sets the msg_replay_active_count of this MsgVpn.

        The number of message replays that are currently active in the Message VPN.  # noqa: E501

        :param msg_replay_active_count: The msg_replay_active_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_replay_active_count = msg_replay_active_count

    @property
    def msg_replay_failed_count(self):
        """Gets the msg_replay_failed_count of this MsgVpn.  # noqa: E501

        The number of message replays that are currently failed in the Message VPN.  # noqa: E501

        :return: The msg_replay_failed_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_replay_failed_count

    @msg_replay_failed_count.setter
    def msg_replay_failed_count(self, msg_replay_failed_count):
        """Sets the msg_replay_failed_count of this MsgVpn.

        The number of message replays that are currently failed in the Message VPN.  # noqa: E501

        :param msg_replay_failed_count: The msg_replay_failed_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_replay_failed_count = msg_replay_failed_count

    @property
    def msg_replay_initializing_count(self):
        """Gets the msg_replay_initializing_count of this MsgVpn.  # noqa: E501

        The number of message replays that are currently initializing in the Message VPN.  # noqa: E501

        :return: The msg_replay_initializing_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_replay_initializing_count

    @msg_replay_initializing_count.setter
    def msg_replay_initializing_count(self, msg_replay_initializing_count):
        """Sets the msg_replay_initializing_count of this MsgVpn.

        The number of message replays that are currently initializing in the Message VPN.  # noqa: E501

        :param msg_replay_initializing_count: The msg_replay_initializing_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_replay_initializing_count = msg_replay_initializing_count

    @property
    def msg_replay_pending_complete_count(self):
        """Gets the msg_replay_pending_complete_count of this MsgVpn.  # noqa: E501

        The number of message replays that are pending complete in the Message VPN.  # noqa: E501

        :return: The msg_replay_pending_complete_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_replay_pending_complete_count

    @msg_replay_pending_complete_count.setter
    def msg_replay_pending_complete_count(self, msg_replay_pending_complete_count):
        """Sets the msg_replay_pending_complete_count of this MsgVpn.

        The number of message replays that are pending complete in the Message VPN.  # noqa: E501

        :param msg_replay_pending_complete_count: The msg_replay_pending_complete_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_replay_pending_complete_count = msg_replay_pending_complete_count

    @property
    def msg_spool_msg_count(self):
        """Gets the msg_spool_msg_count of this MsgVpn.  # noqa: E501

        The current number of messages spooled (persisted in the Message Spool) in the Message VPN. Available since 2.14.  # noqa: E501

        :return: The msg_spool_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_msg_count

    @msg_spool_msg_count.setter
    def msg_spool_msg_count(self, msg_spool_msg_count):
        """Sets the msg_spool_msg_count of this MsgVpn.

        The current number of messages spooled (persisted in the Message Spool) in the Message VPN. Available since 2.14.  # noqa: E501

        :param msg_spool_msg_count: The msg_spool_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_spool_msg_count = msg_spool_msg_count

    @property
    def msg_spool_rx_msg_count(self):
        """Gets the msg_spool_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of guaranteed messages received by the Message VPN. Available since 2.13.  # noqa: E501

        :return: The msg_spool_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_rx_msg_count

    @msg_spool_rx_msg_count.setter
    def msg_spool_rx_msg_count(self, msg_spool_rx_msg_count):
        """Sets the msg_spool_rx_msg_count of this MsgVpn.

        The number of guaranteed messages received by the Message VPN. Available since 2.13.  # noqa: E501

        :param msg_spool_rx_msg_count: The msg_spool_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_spool_rx_msg_count = msg_spool_rx_msg_count

    @property
    def msg_spool_tx_msg_count(self):
        """Gets the msg_spool_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of guaranteed messages transmitted by the Message VPN. One message to multiple clients is counted as one message. Available since 2.13.  # noqa: E501

        :return: The msg_spool_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_tx_msg_count

    @msg_spool_tx_msg_count.setter
    def msg_spool_tx_msg_count(self, msg_spool_tx_msg_count):
        """Sets the msg_spool_tx_msg_count of this MsgVpn.

        The number of guaranteed messages transmitted by the Message VPN. One message to multiple clients is counted as one message. Available since 2.13.  # noqa: E501

        :param msg_spool_tx_msg_count: The msg_spool_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_spool_tx_msg_count = msg_spool_tx_msg_count

    @property
    def msg_spool_usage(self):
        """Gets the msg_spool_usage of this MsgVpn.  # noqa: E501

        The current message spool usage by the Message VPN, in bytes (B).  # noqa: E501

        :return: The msg_spool_usage of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._msg_spool_usage

    @msg_spool_usage.setter
    def msg_spool_usage(self, msg_spool_usage):
        """Sets the msg_spool_usage of this MsgVpn.

        The current message spool usage by the Message VPN, in bytes (B).  # noqa: E501

        :param msg_spool_usage: The msg_spool_usage of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._msg_spool_usage = msg_spool_usage

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpn.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpn.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def rate(self):
        """Gets the rate of this MsgVpn.  # noqa: E501


        :return: The rate of this MsgVpn.  # noqa: E501
        :rtype: MsgVpnRate
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this MsgVpn.


        :param rate: The rate of this MsgVpn.  # noqa: E501
        :type: MsgVpnRate
        """

        self._rate = rate

    @property
    def replication_ack_propagation_interval_msg_count(self):
        """Gets the replication_ack_propagation_interval_msg_count of this MsgVpn.  # noqa: E501

        The acknowledgement (ACK) propagation interval for the replication Bridge, in number of replicated messages. Available since 2.12.  # noqa: E501

        :return: The replication_ack_propagation_interval_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_ack_propagation_interval_msg_count

    @replication_ack_propagation_interval_msg_count.setter
    def replication_ack_propagation_interval_msg_count(self, replication_ack_propagation_interval_msg_count):
        """Sets the replication_ack_propagation_interval_msg_count of this MsgVpn.

        The acknowledgement (ACK) propagation interval for the replication Bridge, in number of replicated messages. Available since 2.12.  # noqa: E501

        :param replication_ack_propagation_interval_msg_count: The replication_ack_propagation_interval_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_ack_propagation_interval_msg_count = replication_ack_propagation_interval_msg_count

    @property
    def replication_active_ack_prop_tx_msg_count(self):
        """Gets the replication_active_ack_prop_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of acknowledgement messages propagated to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_ack_prop_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_ack_prop_tx_msg_count

    @replication_active_ack_prop_tx_msg_count.setter
    def replication_active_ack_prop_tx_msg_count(self, replication_active_ack_prop_tx_msg_count):
        """Sets the replication_active_ack_prop_tx_msg_count of this MsgVpn.

        The number of acknowledgement messages propagated to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_ack_prop_tx_msg_count: The replication_active_ack_prop_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_ack_prop_tx_msg_count = replication_active_ack_prop_tx_msg_count

    @property
    def replication_active_async_queued_msg_count(self):
        """Gets the replication_active_async_queued_msg_count of this MsgVpn.  # noqa: E501

        The number of async messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_async_queued_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_async_queued_msg_count

    @replication_active_async_queued_msg_count.setter
    def replication_active_async_queued_msg_count(self, replication_active_async_queued_msg_count):
        """Sets the replication_active_async_queued_msg_count of this MsgVpn.

        The number of async messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_async_queued_msg_count: The replication_active_async_queued_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_async_queued_msg_count = replication_active_async_queued_msg_count

    @property
    def replication_active_locally_consumed_msg_count(self):
        """Gets the replication_active_locally_consumed_msg_count of this MsgVpn.  # noqa: E501

        The number of messages consumed in the replication active local Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_locally_consumed_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_locally_consumed_msg_count

    @replication_active_locally_consumed_msg_count.setter
    def replication_active_locally_consumed_msg_count(self, replication_active_locally_consumed_msg_count):
        """Sets the replication_active_locally_consumed_msg_count of this MsgVpn.

        The number of messages consumed in the replication active local Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_locally_consumed_msg_count: The replication_active_locally_consumed_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_locally_consumed_msg_count = replication_active_locally_consumed_msg_count

    @property
    def replication_active_mate_flow_congested_peak_time(self):
        """Gets the replication_active_mate_flow_congested_peak_time of this MsgVpn.  # noqa: E501

        The peak amount of time in seconds the message flow has been congested to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_mate_flow_congested_peak_time of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_mate_flow_congested_peak_time

    @replication_active_mate_flow_congested_peak_time.setter
    def replication_active_mate_flow_congested_peak_time(self, replication_active_mate_flow_congested_peak_time):
        """Sets the replication_active_mate_flow_congested_peak_time of this MsgVpn.

        The peak amount of time in seconds the message flow has been congested to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_mate_flow_congested_peak_time: The replication_active_mate_flow_congested_peak_time of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_mate_flow_congested_peak_time = replication_active_mate_flow_congested_peak_time

    @property
    def replication_active_mate_flow_not_congested_peak_time(self):
        """Gets the replication_active_mate_flow_not_congested_peak_time of this MsgVpn.  # noqa: E501

        The peak amount of time in seconds the message flow has not been congested to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_mate_flow_not_congested_peak_time of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_mate_flow_not_congested_peak_time

    @replication_active_mate_flow_not_congested_peak_time.setter
    def replication_active_mate_flow_not_congested_peak_time(self, replication_active_mate_flow_not_congested_peak_time):
        """Sets the replication_active_mate_flow_not_congested_peak_time of this MsgVpn.

        The peak amount of time in seconds the message flow has not been congested to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_mate_flow_not_congested_peak_time: The replication_active_mate_flow_not_congested_peak_time of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_mate_flow_not_congested_peak_time = replication_active_mate_flow_not_congested_peak_time

    @property
    def replication_active_promoted_queued_msg_count(self):
        """Gets the replication_active_promoted_queued_msg_count of this MsgVpn.  # noqa: E501

        The number of promoted messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_promoted_queued_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_promoted_queued_msg_count

    @replication_active_promoted_queued_msg_count.setter
    def replication_active_promoted_queued_msg_count(self, replication_active_promoted_queued_msg_count):
        """Sets the replication_active_promoted_queued_msg_count of this MsgVpn.

        The number of promoted messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_promoted_queued_msg_count: The replication_active_promoted_queued_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_promoted_queued_msg_count = replication_active_promoted_queued_msg_count

    @property
    def replication_active_reconcile_request_rx_msg_count(self):
        """Gets the replication_active_reconcile_request_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of reconcile request messages received from the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_reconcile_request_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_reconcile_request_rx_msg_count

    @replication_active_reconcile_request_rx_msg_count.setter
    def replication_active_reconcile_request_rx_msg_count(self, replication_active_reconcile_request_rx_msg_count):
        """Sets the replication_active_reconcile_request_rx_msg_count of this MsgVpn.

        The number of reconcile request messages received from the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_reconcile_request_rx_msg_count: The replication_active_reconcile_request_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_reconcile_request_rx_msg_count = replication_active_reconcile_request_rx_msg_count

    @property
    def replication_active_sync_eligible_peak_time(self):
        """Gets the replication_active_sync_eligible_peak_time of this MsgVpn.  # noqa: E501

        The peak amount of time in seconds sync replication has been eligible to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_sync_eligible_peak_time of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_sync_eligible_peak_time

    @replication_active_sync_eligible_peak_time.setter
    def replication_active_sync_eligible_peak_time(self, replication_active_sync_eligible_peak_time):
        """Sets the replication_active_sync_eligible_peak_time of this MsgVpn.

        The peak amount of time in seconds sync replication has been eligible to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_sync_eligible_peak_time: The replication_active_sync_eligible_peak_time of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_sync_eligible_peak_time = replication_active_sync_eligible_peak_time

    @property
    def replication_active_sync_ineligible_peak_time(self):
        """Gets the replication_active_sync_ineligible_peak_time of this MsgVpn.  # noqa: E501

        The peak amount of time in seconds sync replication has been ineligible to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_sync_ineligible_peak_time of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_sync_ineligible_peak_time

    @replication_active_sync_ineligible_peak_time.setter
    def replication_active_sync_ineligible_peak_time(self, replication_active_sync_ineligible_peak_time):
        """Sets the replication_active_sync_ineligible_peak_time of this MsgVpn.

        The peak amount of time in seconds sync replication has been ineligible to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_sync_ineligible_peak_time: The replication_active_sync_ineligible_peak_time of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_sync_ineligible_peak_time = replication_active_sync_ineligible_peak_time

    @property
    def replication_active_sync_queued_as_async_msg_count(self):
        """Gets the replication_active_sync_queued_as_async_msg_count of this MsgVpn.  # noqa: E501

        The number of sync messages queued as async to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_sync_queued_as_async_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_sync_queued_as_async_msg_count

    @replication_active_sync_queued_as_async_msg_count.setter
    def replication_active_sync_queued_as_async_msg_count(self, replication_active_sync_queued_as_async_msg_count):
        """Sets the replication_active_sync_queued_as_async_msg_count of this MsgVpn.

        The number of sync messages queued as async to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_sync_queued_as_async_msg_count: The replication_active_sync_queued_as_async_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_sync_queued_as_async_msg_count = replication_active_sync_queued_as_async_msg_count

    @property
    def replication_active_sync_queued_msg_count(self):
        """Gets the replication_active_sync_queued_msg_count of this MsgVpn.  # noqa: E501

        The number of sync messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_sync_queued_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_sync_queued_msg_count

    @replication_active_sync_queued_msg_count.setter
    def replication_active_sync_queued_msg_count(self, replication_active_sync_queued_msg_count):
        """Sets the replication_active_sync_queued_msg_count of this MsgVpn.

        The number of sync messages queued to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_sync_queued_msg_count: The replication_active_sync_queued_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_sync_queued_msg_count = replication_active_sync_queued_msg_count

    @property
    def replication_active_transition_to_sync_ineligible_count(self):
        """Gets the replication_active_transition_to_sync_ineligible_count of this MsgVpn.  # noqa: E501

        The number of sync replication ineligible transitions to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_active_transition_to_sync_ineligible_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_active_transition_to_sync_ineligible_count

    @replication_active_transition_to_sync_ineligible_count.setter
    def replication_active_transition_to_sync_ineligible_count(self, replication_active_transition_to_sync_ineligible_count):
        """Sets the replication_active_transition_to_sync_ineligible_count of this MsgVpn.

        The number of sync replication ineligible transitions to the replication standby remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_active_transition_to_sync_ineligible_count: The replication_active_transition_to_sync_ineligible_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_active_transition_to_sync_ineligible_count = replication_active_transition_to_sync_ineligible_count

    @property
    def replication_bridge_authentication_basic_client_username(self):
        """Gets the replication_bridge_authentication_basic_client_username of this MsgVpn.  # noqa: E501

        The Client Username the replication Bridge uses to login to the remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_authentication_basic_client_username of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_bridge_authentication_basic_client_username

    @replication_bridge_authentication_basic_client_username.setter
    def replication_bridge_authentication_basic_client_username(self, replication_bridge_authentication_basic_client_username):
        """Sets the replication_bridge_authentication_basic_client_username of this MsgVpn.

        The Client Username the replication Bridge uses to login to the remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_bridge_authentication_basic_client_username: The replication_bridge_authentication_basic_client_username of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._replication_bridge_authentication_basic_client_username = replication_bridge_authentication_basic_client_username

    @property
    def replication_bridge_authentication_scheme(self):
        """Gets the replication_bridge_authentication_scheme of this MsgVpn.  # noqa: E501

        The authentication scheme for the replication Bridge in the Message VPN. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>  Available since 2.12.  # noqa: E501

        :return: The replication_bridge_authentication_scheme of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_bridge_authentication_scheme

    @replication_bridge_authentication_scheme.setter
    def replication_bridge_authentication_scheme(self, replication_bridge_authentication_scheme):
        """Sets the replication_bridge_authentication_scheme of this MsgVpn.

        The authentication scheme for the replication Bridge in the Message VPN. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>  Available since 2.12.  # noqa: E501

        :param replication_bridge_authentication_scheme: The replication_bridge_authentication_scheme of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["basic", "client-certificate"]  # noqa: E501
        if replication_bridge_authentication_scheme not in allowed_values:
            raise ValueError(
                "Invalid value for `replication_bridge_authentication_scheme` ({0}), must be one of {1}"  # noqa: E501
                .format(replication_bridge_authentication_scheme, allowed_values)
            )

        self._replication_bridge_authentication_scheme = replication_bridge_authentication_scheme

    @property
    def replication_bridge_bound_to_queue(self):
        """Gets the replication_bridge_bound_to_queue of this MsgVpn.  # noqa: E501

        Indicates whether the local replication Bridge is bound to the Queue in the remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_bound_to_queue of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_bridge_bound_to_queue

    @replication_bridge_bound_to_queue.setter
    def replication_bridge_bound_to_queue(self, replication_bridge_bound_to_queue):
        """Sets the replication_bridge_bound_to_queue of this MsgVpn.

        Indicates whether the local replication Bridge is bound to the Queue in the remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_bridge_bound_to_queue: The replication_bridge_bound_to_queue of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_bridge_bound_to_queue = replication_bridge_bound_to_queue

    @property
    def replication_bridge_compressed_data_enabled(self):
        """Gets the replication_bridge_compressed_data_enabled of this MsgVpn.  # noqa: E501

        Indicates whether compression is used for the replication Bridge. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_compressed_data_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_bridge_compressed_data_enabled

    @replication_bridge_compressed_data_enabled.setter
    def replication_bridge_compressed_data_enabled(self, replication_bridge_compressed_data_enabled):
        """Sets the replication_bridge_compressed_data_enabled of this MsgVpn.

        Indicates whether compression is used for the replication Bridge. Available since 2.12.  # noqa: E501

        :param replication_bridge_compressed_data_enabled: The replication_bridge_compressed_data_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_bridge_compressed_data_enabled = replication_bridge_compressed_data_enabled

    @property
    def replication_bridge_egress_flow_window_size(self):
        """Gets the replication_bridge_egress_flow_window_size of this MsgVpn.  # noqa: E501

        The size of the window used for guaranteed messages published to the replication Bridge, in messages. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_egress_flow_window_size of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_bridge_egress_flow_window_size

    @replication_bridge_egress_flow_window_size.setter
    def replication_bridge_egress_flow_window_size(self, replication_bridge_egress_flow_window_size):
        """Sets the replication_bridge_egress_flow_window_size of this MsgVpn.

        The size of the window used for guaranteed messages published to the replication Bridge, in messages. Available since 2.12.  # noqa: E501

        :param replication_bridge_egress_flow_window_size: The replication_bridge_egress_flow_window_size of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_bridge_egress_flow_window_size = replication_bridge_egress_flow_window_size

    @property
    def replication_bridge_name(self):
        """Gets the replication_bridge_name of this MsgVpn.  # noqa: E501

        The name of the local replication Bridge in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_bridge_name

    @replication_bridge_name.setter
    def replication_bridge_name(self, replication_bridge_name):
        """Sets the replication_bridge_name of this MsgVpn.

        The name of the local replication Bridge in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_bridge_name: The replication_bridge_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._replication_bridge_name = replication_bridge_name

    @property
    def replication_bridge_retry_delay(self):
        """Gets the replication_bridge_retry_delay of this MsgVpn.  # noqa: E501

        The number of seconds that must pass before retrying the replication Bridge connection. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_retry_delay of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_bridge_retry_delay

    @replication_bridge_retry_delay.setter
    def replication_bridge_retry_delay(self, replication_bridge_retry_delay):
        """Sets the replication_bridge_retry_delay of this MsgVpn.

        The number of seconds that must pass before retrying the replication Bridge connection. Available since 2.12.  # noqa: E501

        :param replication_bridge_retry_delay: The replication_bridge_retry_delay of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_bridge_retry_delay = replication_bridge_retry_delay

    @property
    def replication_bridge_tls_enabled(self):
        """Gets the replication_bridge_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for the replication Bridge connection. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_bridge_tls_enabled

    @replication_bridge_tls_enabled.setter
    def replication_bridge_tls_enabled(self, replication_bridge_tls_enabled):
        """Sets the replication_bridge_tls_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for the replication Bridge connection. Available since 2.12.  # noqa: E501

        :param replication_bridge_tls_enabled: The replication_bridge_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_bridge_tls_enabled = replication_bridge_tls_enabled

    @property
    def replication_bridge_unidirectional_client_profile_name(self):
        """Gets the replication_bridge_unidirectional_client_profile_name of this MsgVpn.  # noqa: E501

        The Client Profile for the unidirectional replication Bridge in the Message VPN. It is used only for the TCP parameters. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_unidirectional_client_profile_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_bridge_unidirectional_client_profile_name

    @replication_bridge_unidirectional_client_profile_name.setter
    def replication_bridge_unidirectional_client_profile_name(self, replication_bridge_unidirectional_client_profile_name):
        """Sets the replication_bridge_unidirectional_client_profile_name of this MsgVpn.

        The Client Profile for the unidirectional replication Bridge in the Message VPN. It is used only for the TCP parameters. Available since 2.12.  # noqa: E501

        :param replication_bridge_unidirectional_client_profile_name: The replication_bridge_unidirectional_client_profile_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._replication_bridge_unidirectional_client_profile_name = replication_bridge_unidirectional_client_profile_name

    @property
    def replication_bridge_up(self):
        """Gets the replication_bridge_up of this MsgVpn.  # noqa: E501

        Indicates whether the local replication Bridge is operationally up in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_bridge_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_bridge_up

    @replication_bridge_up.setter
    def replication_bridge_up(self, replication_bridge_up):
        """Sets the replication_bridge_up of this MsgVpn.

        Indicates whether the local replication Bridge is operationally up in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_bridge_up: The replication_bridge_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_bridge_up = replication_bridge_up

    @property
    def replication_enabled(self):
        """Gets the replication_enabled of this MsgVpn.  # noqa: E501

        Indicates whether replication is enabled for the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_enabled

    @replication_enabled.setter
    def replication_enabled(self, replication_enabled):
        """Sets the replication_enabled of this MsgVpn.

        Indicates whether replication is enabled for the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_enabled: The replication_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_enabled = replication_enabled

    @property
    def replication_queue_bound(self):
        """Gets the replication_queue_bound of this MsgVpn.  # noqa: E501

        Indicates whether the remote replication Bridge is bound to the Queue in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_queue_bound of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_queue_bound

    @replication_queue_bound.setter
    def replication_queue_bound(self, replication_queue_bound):
        """Sets the replication_queue_bound of this MsgVpn.

        Indicates whether the remote replication Bridge is bound to the Queue in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_queue_bound: The replication_queue_bound of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_queue_bound = replication_queue_bound

    @property
    def replication_queue_max_msg_spool_usage(self):
        """Gets the replication_queue_max_msg_spool_usage of this MsgVpn.  # noqa: E501

        The maximum message spool usage by the replication Bridge local Queue (quota), in megabytes. Available since 2.12.  # noqa: E501

        :return: The replication_queue_max_msg_spool_usage of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_queue_max_msg_spool_usage

    @replication_queue_max_msg_spool_usage.setter
    def replication_queue_max_msg_spool_usage(self, replication_queue_max_msg_spool_usage):
        """Sets the replication_queue_max_msg_spool_usage of this MsgVpn.

        The maximum message spool usage by the replication Bridge local Queue (quota), in megabytes. Available since 2.12.  # noqa: E501

        :param replication_queue_max_msg_spool_usage: The replication_queue_max_msg_spool_usage of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_queue_max_msg_spool_usage = replication_queue_max_msg_spool_usage

    @property
    def replication_queue_reject_msg_to_sender_on_discard_enabled(self):
        """Gets the replication_queue_reject_msg_to_sender_on_discard_enabled of this MsgVpn.  # noqa: E501

        Indicates whether messages discarded on this replication Bridge Queue are rejected back to the sender. Available since 2.12.  # noqa: E501

        :return: The replication_queue_reject_msg_to_sender_on_discard_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_queue_reject_msg_to_sender_on_discard_enabled

    @replication_queue_reject_msg_to_sender_on_discard_enabled.setter
    def replication_queue_reject_msg_to_sender_on_discard_enabled(self, replication_queue_reject_msg_to_sender_on_discard_enabled):
        """Sets the replication_queue_reject_msg_to_sender_on_discard_enabled of this MsgVpn.

        Indicates whether messages discarded on this replication Bridge Queue are rejected back to the sender. Available since 2.12.  # noqa: E501

        :param replication_queue_reject_msg_to_sender_on_discard_enabled: The replication_queue_reject_msg_to_sender_on_discard_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_queue_reject_msg_to_sender_on_discard_enabled = replication_queue_reject_msg_to_sender_on_discard_enabled

    @property
    def replication_reject_msg_when_sync_ineligible_enabled(self):
        """Gets the replication_reject_msg_when_sync_ineligible_enabled of this MsgVpn.  # noqa: E501

        Indicates whether guaranteed messages published to synchronously replicated Topics are rejected back to the sender when synchronous replication becomes ineligible. Available since 2.12.  # noqa: E501

        :return: The replication_reject_msg_when_sync_ineligible_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_reject_msg_when_sync_ineligible_enabled

    @replication_reject_msg_when_sync_ineligible_enabled.setter
    def replication_reject_msg_when_sync_ineligible_enabled(self, replication_reject_msg_when_sync_ineligible_enabled):
        """Sets the replication_reject_msg_when_sync_ineligible_enabled of this MsgVpn.

        Indicates whether guaranteed messages published to synchronously replicated Topics are rejected back to the sender when synchronous replication becomes ineligible. Available since 2.12.  # noqa: E501

        :param replication_reject_msg_when_sync_ineligible_enabled: The replication_reject_msg_when_sync_ineligible_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_reject_msg_when_sync_ineligible_enabled = replication_reject_msg_when_sync_ineligible_enabled

    @property
    def replication_remote_bridge_name(self):
        """Gets the replication_remote_bridge_name of this MsgVpn.  # noqa: E501

        The name of the remote replication Bridge in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_remote_bridge_name of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_remote_bridge_name

    @replication_remote_bridge_name.setter
    def replication_remote_bridge_name(self, replication_remote_bridge_name):
        """Sets the replication_remote_bridge_name of this MsgVpn.

        The name of the remote replication Bridge in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_remote_bridge_name: The replication_remote_bridge_name of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._replication_remote_bridge_name = replication_remote_bridge_name

    @property
    def replication_remote_bridge_up(self):
        """Gets the replication_remote_bridge_up of this MsgVpn.  # noqa: E501

        Indicates whether the remote replication Bridge is operationally up in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_remote_bridge_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_remote_bridge_up

    @replication_remote_bridge_up.setter
    def replication_remote_bridge_up(self, replication_remote_bridge_up):
        """Sets the replication_remote_bridge_up of this MsgVpn.

        Indicates whether the remote replication Bridge is operationally up in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_remote_bridge_up: The replication_remote_bridge_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_remote_bridge_up = replication_remote_bridge_up

    @property
    def replication_role(self):
        """Gets the replication_role of this MsgVpn.  # noqa: E501

        The replication role for the Message VPN. The allowed values and their meaning are:  <pre> \"active\" - Assume the Active role in replication for the Message VPN. \"standby\" - Assume the Standby role in replication for the Message VPN. </pre>  Available since 2.12.  # noqa: E501

        :return: The replication_role of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_role

    @replication_role.setter
    def replication_role(self, replication_role):
        """Sets the replication_role of this MsgVpn.

        The replication role for the Message VPN. The allowed values and their meaning are:  <pre> \"active\" - Assume the Active role in replication for the Message VPN. \"standby\" - Assume the Standby role in replication for the Message VPN. </pre>  Available since 2.12.  # noqa: E501

        :param replication_role: The replication_role of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["active", "standby"]  # noqa: E501
        if replication_role not in allowed_values:
            raise ValueError(
                "Invalid value for `replication_role` ({0}), must be one of {1}"  # noqa: E501
                .format(replication_role, allowed_values)
            )

        self._replication_role = replication_role

    @property
    def replication_standby_ack_prop_out_of_seq_rx_msg_count(self):
        """Gets the replication_standby_ack_prop_out_of_seq_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of acknowledgement messages received out of sequence from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_standby_ack_prop_out_of_seq_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_ack_prop_out_of_seq_rx_msg_count

    @replication_standby_ack_prop_out_of_seq_rx_msg_count.setter
    def replication_standby_ack_prop_out_of_seq_rx_msg_count(self, replication_standby_ack_prop_out_of_seq_rx_msg_count):
        """Sets the replication_standby_ack_prop_out_of_seq_rx_msg_count of this MsgVpn.

        The number of acknowledgement messages received out of sequence from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_standby_ack_prop_out_of_seq_rx_msg_count: The replication_standby_ack_prop_out_of_seq_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_ack_prop_out_of_seq_rx_msg_count = replication_standby_ack_prop_out_of_seq_rx_msg_count

    @property
    def replication_standby_ack_prop_rx_msg_count(self):
        """Gets the replication_standby_ack_prop_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of acknowledgement messages received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_standby_ack_prop_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_ack_prop_rx_msg_count

    @replication_standby_ack_prop_rx_msg_count.setter
    def replication_standby_ack_prop_rx_msg_count(self, replication_standby_ack_prop_rx_msg_count):
        """Sets the replication_standby_ack_prop_rx_msg_count of this MsgVpn.

        The number of acknowledgement messages received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_standby_ack_prop_rx_msg_count: The replication_standby_ack_prop_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_ack_prop_rx_msg_count = replication_standby_ack_prop_rx_msg_count

    @property
    def replication_standby_reconcile_request_tx_msg_count(self):
        """Gets the replication_standby_reconcile_request_tx_msg_count of this MsgVpn.  # noqa: E501

        The number of reconcile request messages transmitted to the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_standby_reconcile_request_tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_reconcile_request_tx_msg_count

    @replication_standby_reconcile_request_tx_msg_count.setter
    def replication_standby_reconcile_request_tx_msg_count(self, replication_standby_reconcile_request_tx_msg_count):
        """Sets the replication_standby_reconcile_request_tx_msg_count of this MsgVpn.

        The number of reconcile request messages transmitted to the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_standby_reconcile_request_tx_msg_count: The replication_standby_reconcile_request_tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_reconcile_request_tx_msg_count = replication_standby_reconcile_request_tx_msg_count

    @property
    def replication_standby_rx_msg_count(self):
        """Gets the replication_standby_rx_msg_count of this MsgVpn.  # noqa: E501

        The number of messages received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_standby_rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_rx_msg_count

    @replication_standby_rx_msg_count.setter
    def replication_standby_rx_msg_count(self, replication_standby_rx_msg_count):
        """Sets the replication_standby_rx_msg_count of this MsgVpn.

        The number of messages received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_standby_rx_msg_count: The replication_standby_rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_rx_msg_count = replication_standby_rx_msg_count

    @property
    def replication_standby_transaction_request_count(self):
        """Gets the replication_standby_transaction_request_count of this MsgVpn.  # noqa: E501

        The number of transaction requests received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_standby_transaction_request_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_transaction_request_count

    @replication_standby_transaction_request_count.setter
    def replication_standby_transaction_request_count(self, replication_standby_transaction_request_count):
        """Sets the replication_standby_transaction_request_count of this MsgVpn.

        The number of transaction requests received from the replication active remote Message VPN. Available since 2.12.  # noqa: E501

        :param replication_standby_transaction_request_count: The replication_standby_transaction_request_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_transaction_request_count = replication_standby_transaction_request_count

    @property
    def replication_standby_transaction_request_failure_count(self):
        """Gets the replication_standby_transaction_request_failure_count of this MsgVpn.  # noqa: E501

        The number of transaction requests received from the replication active remote Message VPN that failed. Available since 2.12.  # noqa: E501

        :return: The replication_standby_transaction_request_failure_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_transaction_request_failure_count

    @replication_standby_transaction_request_failure_count.setter
    def replication_standby_transaction_request_failure_count(self, replication_standby_transaction_request_failure_count):
        """Sets the replication_standby_transaction_request_failure_count of this MsgVpn.

        The number of transaction requests received from the replication active remote Message VPN that failed. Available since 2.12.  # noqa: E501

        :param replication_standby_transaction_request_failure_count: The replication_standby_transaction_request_failure_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_transaction_request_failure_count = replication_standby_transaction_request_failure_count

    @property
    def replication_standby_transaction_request_success_count(self):
        """Gets the replication_standby_transaction_request_success_count of this MsgVpn.  # noqa: E501

        The number of transaction requests received from the replication active remote Message VPN that succeeded. Available since 2.12.  # noqa: E501

        :return: The replication_standby_transaction_request_success_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_transaction_request_success_count

    @replication_standby_transaction_request_success_count.setter
    def replication_standby_transaction_request_success_count(self, replication_standby_transaction_request_success_count):
        """Sets the replication_standby_transaction_request_success_count of this MsgVpn.

        The number of transaction requests received from the replication active remote Message VPN that succeeded. Available since 2.12.  # noqa: E501

        :param replication_standby_transaction_request_success_count: The replication_standby_transaction_request_success_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._replication_standby_transaction_request_success_count = replication_standby_transaction_request_success_count

    @property
    def replication_sync_eligible(self):
        """Gets the replication_sync_eligible of this MsgVpn.  # noqa: E501

        Indicates whether sync replication is eligible in the Message VPN. Available since 2.12.  # noqa: E501

        :return: The replication_sync_eligible of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._replication_sync_eligible

    @replication_sync_eligible.setter
    def replication_sync_eligible(self, replication_sync_eligible):
        """Sets the replication_sync_eligible of this MsgVpn.

        Indicates whether sync replication is eligible in the Message VPN. Available since 2.12.  # noqa: E501

        :param replication_sync_eligible: The replication_sync_eligible of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._replication_sync_eligible = replication_sync_eligible

    @property
    def replication_transaction_mode(self):
        """Gets the replication_transaction_mode of this MsgVpn.  # noqa: E501

        Indicates whether synchronous or asynchronous replication mode is used for all transactions within the Message VPN. The allowed values and their meaning are:  <pre> \"sync\" - Messages are acknowledged when replicated (spooled remotely). \"async\" - Messages are acknowledged when pending replication (spooled locally). </pre>  Available since 2.12.  # noqa: E501

        :return: The replication_transaction_mode of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._replication_transaction_mode

    @replication_transaction_mode.setter
    def replication_transaction_mode(self, replication_transaction_mode):
        """Sets the replication_transaction_mode of this MsgVpn.

        Indicates whether synchronous or asynchronous replication mode is used for all transactions within the Message VPN. The allowed values and their meaning are:  <pre> \"sync\" - Messages are acknowledged when replicated (spooled remotely). \"async\" - Messages are acknowledged when pending replication (spooled locally). </pre>  Available since 2.12.  # noqa: E501

        :param replication_transaction_mode: The replication_transaction_mode of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["sync", "async"]  # noqa: E501
        if replication_transaction_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `replication_transaction_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(replication_transaction_mode, allowed_values)
            )

        self._replication_transaction_mode = replication_transaction_mode

    @property
    def rest_tls_server_cert_enforce_trusted_common_name_enabled(self):
        """Gets the rest_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the Common Name (CN) in the server certificate from the remote REST Consumer is validated. Deprecated since 2.17. Common Name validation has been replaced by Server Certificate Name validation.  # noqa: E501

        :return: The rest_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._rest_tls_server_cert_enforce_trusted_common_name_enabled

    @rest_tls_server_cert_enforce_trusted_common_name_enabled.setter
    def rest_tls_server_cert_enforce_trusted_common_name_enabled(self, rest_tls_server_cert_enforce_trusted_common_name_enabled):
        """Sets the rest_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.

        Indicates whether the Common Name (CN) in the server certificate from the remote REST Consumer is validated. Deprecated since 2.17. Common Name validation has been replaced by Server Certificate Name validation.  # noqa: E501

        :param rest_tls_server_cert_enforce_trusted_common_name_enabled: The rest_tls_server_cert_enforce_trusted_common_name_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._rest_tls_server_cert_enforce_trusted_common_name_enabled = rest_tls_server_cert_enforce_trusted_common_name_enabled

    @property
    def rest_tls_server_cert_max_chain_depth(self):
        """Gets the rest_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501

        The maximum depth for a REST Consumer server certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :return: The rest_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rest_tls_server_cert_max_chain_depth

    @rest_tls_server_cert_max_chain_depth.setter
    def rest_tls_server_cert_max_chain_depth(self, rest_tls_server_cert_max_chain_depth):
        """Sets the rest_tls_server_cert_max_chain_depth of this MsgVpn.

        The maximum depth for a REST Consumer server certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate.  # noqa: E501

        :param rest_tls_server_cert_max_chain_depth: The rest_tls_server_cert_max_chain_depth of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rest_tls_server_cert_max_chain_depth = rest_tls_server_cert_max_chain_depth

    @property
    def rest_tls_server_cert_validate_date_enabled(self):
        """Gets the rest_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the REST Consumer server certificate are checked.  # noqa: E501

        :return: The rest_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._rest_tls_server_cert_validate_date_enabled

    @rest_tls_server_cert_validate_date_enabled.setter
    def rest_tls_server_cert_validate_date_enabled(self, rest_tls_server_cert_validate_date_enabled):
        """Sets the rest_tls_server_cert_validate_date_enabled of this MsgVpn.

        Indicates whether the \"Not Before\" and \"Not After\" validity dates in the REST Consumer server certificate are checked.  # noqa: E501

        :param rest_tls_server_cert_validate_date_enabled: The rest_tls_server_cert_validate_date_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._rest_tls_server_cert_validate_date_enabled = rest_tls_server_cert_validate_date_enabled

    @property
    def rest_tls_server_cert_validate_name_enabled(self):
        """Gets the rest_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501

        Enable or disable the standard TLS authentication mechanism of verifying the name used to connect to the remote REST Consumer. If enabled, the name used to connect to the remote REST Consumer is checked against the names specified in the certificate returned by the remote router. Legacy Common Name validation is not performed if Server Certificate Name Validation is enabled, even if Common Name validation is also enabled. Available since 2.17.  # noqa: E501

        :return: The rest_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._rest_tls_server_cert_validate_name_enabled

    @rest_tls_server_cert_validate_name_enabled.setter
    def rest_tls_server_cert_validate_name_enabled(self, rest_tls_server_cert_validate_name_enabled):
        """Sets the rest_tls_server_cert_validate_name_enabled of this MsgVpn.

        Enable or disable the standard TLS authentication mechanism of verifying the name used to connect to the remote REST Consumer. If enabled, the name used to connect to the remote REST Consumer is checked against the names specified in the certificate returned by the remote router. Legacy Common Name validation is not performed if Server Certificate Name Validation is enabled, even if Common Name validation is also enabled. Available since 2.17.  # noqa: E501

        :param rest_tls_server_cert_validate_name_enabled: The rest_tls_server_cert_validate_name_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._rest_tls_server_cert_validate_name_enabled = rest_tls_server_cert_validate_name_enabled

    @property
    def rx_byte_count(self):
        """Gets the rx_byte_count of this MsgVpn.  # noqa: E501

        The amount of messages received from clients by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The rx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_count

    @rx_byte_count.setter
    def rx_byte_count(self, rx_byte_count):
        """Sets the rx_byte_count of this MsgVpn.

        The amount of messages received from clients by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param rx_byte_count: The rx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_byte_count = rx_byte_count

    @property
    def rx_byte_rate(self):
        """Gets the rx_byte_rate of this MsgVpn.  # noqa: E501

        The current message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The rx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_byte_rate

    @rx_byte_rate.setter
    def rx_byte_rate(self, rx_byte_rate):
        """Sets the rx_byte_rate of this MsgVpn.

        The current message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param rx_byte_rate: The rx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_byte_rate = rx_byte_rate

    @property
    def rx_compressed_byte_count(self):
        """Gets the rx_compressed_byte_count of this MsgVpn.  # noqa: E501

        The amount of compressed messages received by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The rx_compressed_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_compressed_byte_count

    @rx_compressed_byte_count.setter
    def rx_compressed_byte_count(self, rx_compressed_byte_count):
        """Sets the rx_compressed_byte_count of this MsgVpn.

        The amount of compressed messages received by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param rx_compressed_byte_count: The rx_compressed_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_compressed_byte_count = rx_compressed_byte_count

    @property
    def rx_compressed_byte_rate(self):
        """Gets the rx_compressed_byte_rate of this MsgVpn.  # noqa: E501

        The current compressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The rx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_compressed_byte_rate

    @rx_compressed_byte_rate.setter
    def rx_compressed_byte_rate(self, rx_compressed_byte_rate):
        """Sets the rx_compressed_byte_rate of this MsgVpn.

        The current compressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param rx_compressed_byte_rate: The rx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_compressed_byte_rate = rx_compressed_byte_rate

    @property
    def rx_compression_ratio(self):
        """Gets the rx_compression_ratio of this MsgVpn.  # noqa: E501

        The compression ratio for messages received by the message VPN. Available since 2.12.  # noqa: E501

        :return: The rx_compression_ratio of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._rx_compression_ratio

    @rx_compression_ratio.setter
    def rx_compression_ratio(self, rx_compression_ratio):
        """Sets the rx_compression_ratio of this MsgVpn.

        The compression ratio for messages received by the message VPN. Available since 2.12.  # noqa: E501

        :param rx_compression_ratio: The rx_compression_ratio of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._rx_compression_ratio = rx_compression_ratio

    @property
    def rx_msg_count(self):
        """Gets the rx_msg_count of this MsgVpn.  # noqa: E501

        The number of messages received from clients by the Message VPN. Available since 2.12.  # noqa: E501

        :return: The rx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_count

    @rx_msg_count.setter
    def rx_msg_count(self, rx_msg_count):
        """Sets the rx_msg_count of this MsgVpn.

        The number of messages received from clients by the Message VPN. Available since 2.12.  # noqa: E501

        :param rx_msg_count: The rx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_msg_count = rx_msg_count

    @property
    def rx_msg_rate(self):
        """Gets the rx_msg_rate of this MsgVpn.  # noqa: E501

        The current message rate received by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The rx_msg_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_msg_rate

    @rx_msg_rate.setter
    def rx_msg_rate(self, rx_msg_rate):
        """Sets the rx_msg_rate of this MsgVpn.

        The current message rate received by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param rx_msg_rate: The rx_msg_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_msg_rate = rx_msg_rate

    @property
    def rx_uncompressed_byte_count(self):
        """Gets the rx_uncompressed_byte_count of this MsgVpn.  # noqa: E501

        The amount of uncompressed messages received by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The rx_uncompressed_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_uncompressed_byte_count

    @rx_uncompressed_byte_count.setter
    def rx_uncompressed_byte_count(self, rx_uncompressed_byte_count):
        """Sets the rx_uncompressed_byte_count of this MsgVpn.

        The amount of uncompressed messages received by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param rx_uncompressed_byte_count: The rx_uncompressed_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_uncompressed_byte_count = rx_uncompressed_byte_count

    @property
    def rx_uncompressed_byte_rate(self):
        """Gets the rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501

        The current uncompressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._rx_uncompressed_byte_rate

    @rx_uncompressed_byte_rate.setter
    def rx_uncompressed_byte_rate(self, rx_uncompressed_byte_rate):
        """Sets the rx_uncompressed_byte_rate of this MsgVpn.

        The current uncompressed message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param rx_uncompressed_byte_rate: The rx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._rx_uncompressed_byte_rate = rx_uncompressed_byte_rate

    @property
    def semp_over_msg_bus_admin_client_enabled(self):
        """Gets the semp_over_msg_bus_admin_client_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"admin\" level \"client\" commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :return: The semp_over_msg_bus_admin_client_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._semp_over_msg_bus_admin_client_enabled

    @semp_over_msg_bus_admin_client_enabled.setter
    def semp_over_msg_bus_admin_client_enabled(self, semp_over_msg_bus_admin_client_enabled):
        """Sets the semp_over_msg_bus_admin_client_enabled of this MsgVpn.

        Indicates whether the \"admin\" level \"client\" commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :param semp_over_msg_bus_admin_client_enabled: The semp_over_msg_bus_admin_client_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._semp_over_msg_bus_admin_client_enabled = semp_over_msg_bus_admin_client_enabled

    @property
    def semp_over_msg_bus_admin_distributed_cache_enabled(self):
        """Gets the semp_over_msg_bus_admin_distributed_cache_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"admin\" level \"Distributed Cache\" commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :return: The semp_over_msg_bus_admin_distributed_cache_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._semp_over_msg_bus_admin_distributed_cache_enabled

    @semp_over_msg_bus_admin_distributed_cache_enabled.setter
    def semp_over_msg_bus_admin_distributed_cache_enabled(self, semp_over_msg_bus_admin_distributed_cache_enabled):
        """Sets the semp_over_msg_bus_admin_distributed_cache_enabled of this MsgVpn.

        Indicates whether the \"admin\" level \"Distributed Cache\" commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :param semp_over_msg_bus_admin_distributed_cache_enabled: The semp_over_msg_bus_admin_distributed_cache_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._semp_over_msg_bus_admin_distributed_cache_enabled = semp_over_msg_bus_admin_distributed_cache_enabled

    @property
    def semp_over_msg_bus_admin_enabled(self):
        """Gets the semp_over_msg_bus_admin_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"admin\" level commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :return: The semp_over_msg_bus_admin_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._semp_over_msg_bus_admin_enabled

    @semp_over_msg_bus_admin_enabled.setter
    def semp_over_msg_bus_admin_enabled(self, semp_over_msg_bus_admin_enabled):
        """Sets the semp_over_msg_bus_admin_enabled of this MsgVpn.

        Indicates whether the \"admin\" level commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :param semp_over_msg_bus_admin_enabled: The semp_over_msg_bus_admin_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._semp_over_msg_bus_admin_enabled = semp_over_msg_bus_admin_enabled

    @property
    def semp_over_msg_bus_enabled(self):
        """Gets the semp_over_msg_bus_enabled of this MsgVpn.  # noqa: E501

        Indicates whether SEMP over the message bus is enabled in the Message VPN.  # noqa: E501

        :return: The semp_over_msg_bus_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._semp_over_msg_bus_enabled

    @semp_over_msg_bus_enabled.setter
    def semp_over_msg_bus_enabled(self, semp_over_msg_bus_enabled):
        """Sets the semp_over_msg_bus_enabled of this MsgVpn.

        Indicates whether SEMP over the message bus is enabled in the Message VPN.  # noqa: E501

        :param semp_over_msg_bus_enabled: The semp_over_msg_bus_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._semp_over_msg_bus_enabled = semp_over_msg_bus_enabled

    @property
    def semp_over_msg_bus_show_enabled(self):
        """Gets the semp_over_msg_bus_show_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the \"show\" level commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :return: The semp_over_msg_bus_show_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._semp_over_msg_bus_show_enabled

    @semp_over_msg_bus_show_enabled.setter
    def semp_over_msg_bus_show_enabled(self, semp_over_msg_bus_show_enabled):
        """Sets the semp_over_msg_bus_show_enabled of this MsgVpn.

        Indicates whether the \"show\" level commands are enabled for SEMP over the message bus in the Message VPN.  # noqa: E501

        :param semp_over_msg_bus_show_enabled: The semp_over_msg_bus_show_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._semp_over_msg_bus_show_enabled = semp_over_msg_bus_show_enabled

    @property
    def service_amqp_max_connection_count(self):
        """Gets the service_amqp_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of AMQP client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :return: The service_amqp_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_amqp_max_connection_count

    @service_amqp_max_connection_count.setter
    def service_amqp_max_connection_count(self, service_amqp_max_connection_count):
        """Sets the service_amqp_max_connection_count of this MsgVpn.

        The maximum number of AMQP client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :param service_amqp_max_connection_count: The service_amqp_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_amqp_max_connection_count = service_amqp_max_connection_count

    @property
    def service_amqp_plain_text_compressed(self):
        """Gets the service_amqp_plain_text_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the AMQP Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_amqp_plain_text_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_plain_text_compressed

    @service_amqp_plain_text_compressed.setter
    def service_amqp_plain_text_compressed(self, service_amqp_plain_text_compressed):
        """Sets the service_amqp_plain_text_compressed of this MsgVpn.

        Indicates whether the AMQP Service is compressed in the Message VPN.  # noqa: E501

        :param service_amqp_plain_text_compressed: The service_amqp_plain_text_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_plain_text_compressed = service_amqp_plain_text_compressed

    @property
    def service_amqp_plain_text_enabled(self):
        """Gets the service_amqp_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the AMQP Service is enabled in the Message VPN.  # noqa: E501

        :return: The service_amqp_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_plain_text_enabled

    @service_amqp_plain_text_enabled.setter
    def service_amqp_plain_text_enabled(self, service_amqp_plain_text_enabled):
        """Sets the service_amqp_plain_text_enabled of this MsgVpn.

        Indicates whether the AMQP Service is enabled in the Message VPN.  # noqa: E501

        :param service_amqp_plain_text_enabled: The service_amqp_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_plain_text_enabled = service_amqp_plain_text_enabled

    @property
    def service_amqp_plain_text_failure_reason(self):
        """Gets the service_amqp_plain_text_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the AMQP Service failure in the Message VPN.  # noqa: E501

        :return: The service_amqp_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_amqp_plain_text_failure_reason

    @service_amqp_plain_text_failure_reason.setter
    def service_amqp_plain_text_failure_reason(self, service_amqp_plain_text_failure_reason):
        """Sets the service_amqp_plain_text_failure_reason of this MsgVpn.

        The reason for the AMQP Service failure in the Message VPN.  # noqa: E501

        :param service_amqp_plain_text_failure_reason: The service_amqp_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_amqp_plain_text_failure_reason = service_amqp_plain_text_failure_reason

    @property
    def service_amqp_plain_text_listen_port(self):
        """Gets the service_amqp_plain_text_listen_port of this MsgVpn.  # noqa: E501

        The port number for plain-text AMQP clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_amqp_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_amqp_plain_text_listen_port

    @service_amqp_plain_text_listen_port.setter
    def service_amqp_plain_text_listen_port(self, service_amqp_plain_text_listen_port):
        """Sets the service_amqp_plain_text_listen_port of this MsgVpn.

        The port number for plain-text AMQP clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_amqp_plain_text_listen_port: The service_amqp_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_amqp_plain_text_listen_port = service_amqp_plain_text_listen_port

    @property
    def service_amqp_plain_text_up(self):
        """Gets the service_amqp_plain_text_up of this MsgVpn.  # noqa: E501

        Indicates whether the AMQP Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_amqp_plain_text_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_plain_text_up

    @service_amqp_plain_text_up.setter
    def service_amqp_plain_text_up(self, service_amqp_plain_text_up):
        """Sets the service_amqp_plain_text_up of this MsgVpn.

        Indicates whether the AMQP Service is operationally up in the Message VPN.  # noqa: E501

        :param service_amqp_plain_text_up: The service_amqp_plain_text_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_plain_text_up = service_amqp_plain_text_up

    @property
    def service_amqp_tls_compressed(self):
        """Gets the service_amqp_tls_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related AMQP Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_amqp_tls_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_tls_compressed

    @service_amqp_tls_compressed.setter
    def service_amqp_tls_compressed(self, service_amqp_tls_compressed):
        """Sets the service_amqp_tls_compressed of this MsgVpn.

        Indicates whether the TLS related AMQP Service is compressed in the Message VPN.  # noqa: E501

        :param service_amqp_tls_compressed: The service_amqp_tls_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_tls_compressed = service_amqp_tls_compressed

    @property
    def service_amqp_tls_enabled(self):
        """Gets the service_amqp_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for AMQP clients in the Message VPN.  # noqa: E501

        :return: The service_amqp_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_tls_enabled

    @service_amqp_tls_enabled.setter
    def service_amqp_tls_enabled(self, service_amqp_tls_enabled):
        """Sets the service_amqp_tls_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for AMQP clients in the Message VPN.  # noqa: E501

        :param service_amqp_tls_enabled: The service_amqp_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_tls_enabled = service_amqp_tls_enabled

    @property
    def service_amqp_tls_failure_reason(self):
        """Gets the service_amqp_tls_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related AMQP Service failure in the Message VPN.  # noqa: E501

        :return: The service_amqp_tls_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_amqp_tls_failure_reason

    @service_amqp_tls_failure_reason.setter
    def service_amqp_tls_failure_reason(self, service_amqp_tls_failure_reason):
        """Sets the service_amqp_tls_failure_reason of this MsgVpn.

        The reason for the TLS related AMQP Service failure in the Message VPN.  # noqa: E501

        :param service_amqp_tls_failure_reason: The service_amqp_tls_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_amqp_tls_failure_reason = service_amqp_tls_failure_reason

    @property
    def service_amqp_tls_listen_port(self):
        """Gets the service_amqp_tls_listen_port of this MsgVpn.  # noqa: E501

        The port number for AMQP clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_amqp_tls_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_amqp_tls_listen_port

    @service_amqp_tls_listen_port.setter
    def service_amqp_tls_listen_port(self, service_amqp_tls_listen_port):
        """Sets the service_amqp_tls_listen_port of this MsgVpn.

        The port number for AMQP clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_amqp_tls_listen_port: The service_amqp_tls_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_amqp_tls_listen_port = service_amqp_tls_listen_port

    @property
    def service_amqp_tls_up(self):
        """Gets the service_amqp_tls_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related AMQP Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_amqp_tls_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_amqp_tls_up

    @service_amqp_tls_up.setter
    def service_amqp_tls_up(self, service_amqp_tls_up):
        """Sets the service_amqp_tls_up of this MsgVpn.

        Indicates whether the TLS related AMQP Service is operationally up in the Message VPN.  # noqa: E501

        :param service_amqp_tls_up: The service_amqp_tls_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_amqp_tls_up = service_amqp_tls_up

    @property
    def service_mqtt_max_connection_count(self):
        """Gets the service_mqtt_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of MQTT client connections that can be simultaneously connected to the Message VPN.  # noqa: E501

        :return: The service_mqtt_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_mqtt_max_connection_count

    @service_mqtt_max_connection_count.setter
    def service_mqtt_max_connection_count(self, service_mqtt_max_connection_count):
        """Sets the service_mqtt_max_connection_count of this MsgVpn.

        The maximum number of MQTT client connections that can be simultaneously connected to the Message VPN.  # noqa: E501

        :param service_mqtt_max_connection_count: The service_mqtt_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_mqtt_max_connection_count = service_mqtt_max_connection_count

    @property
    def service_mqtt_plain_text_compressed(self):
        """Gets the service_mqtt_plain_text_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the MQTT Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_mqtt_plain_text_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_plain_text_compressed

    @service_mqtt_plain_text_compressed.setter
    def service_mqtt_plain_text_compressed(self, service_mqtt_plain_text_compressed):
        """Sets the service_mqtt_plain_text_compressed of this MsgVpn.

        Indicates whether the MQTT Service is compressed in the Message VPN.  # noqa: E501

        :param service_mqtt_plain_text_compressed: The service_mqtt_plain_text_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_plain_text_compressed = service_mqtt_plain_text_compressed

    @property
    def service_mqtt_plain_text_enabled(self):
        """Gets the service_mqtt_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the MQTT Service is enabled in the Message VPN.  # noqa: E501

        :return: The service_mqtt_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_plain_text_enabled

    @service_mqtt_plain_text_enabled.setter
    def service_mqtt_plain_text_enabled(self, service_mqtt_plain_text_enabled):
        """Sets the service_mqtt_plain_text_enabled of this MsgVpn.

        Indicates whether the MQTT Service is enabled in the Message VPN.  # noqa: E501

        :param service_mqtt_plain_text_enabled: The service_mqtt_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_plain_text_enabled = service_mqtt_plain_text_enabled

    @property
    def service_mqtt_plain_text_failure_reason(self):
        """Gets the service_mqtt_plain_text_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the MQTT Service failure in the Message VPN.  # noqa: E501

        :return: The service_mqtt_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_mqtt_plain_text_failure_reason

    @service_mqtt_plain_text_failure_reason.setter
    def service_mqtt_plain_text_failure_reason(self, service_mqtt_plain_text_failure_reason):
        """Sets the service_mqtt_plain_text_failure_reason of this MsgVpn.

        The reason for the MQTT Service failure in the Message VPN.  # noqa: E501

        :param service_mqtt_plain_text_failure_reason: The service_mqtt_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_mqtt_plain_text_failure_reason = service_mqtt_plain_text_failure_reason

    @property
    def service_mqtt_plain_text_listen_port(self):
        """Gets the service_mqtt_plain_text_listen_port of this MsgVpn.  # noqa: E501

        The port number for plain-text MQTT clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_mqtt_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_mqtt_plain_text_listen_port

    @service_mqtt_plain_text_listen_port.setter
    def service_mqtt_plain_text_listen_port(self, service_mqtt_plain_text_listen_port):
        """Sets the service_mqtt_plain_text_listen_port of this MsgVpn.

        The port number for plain-text MQTT clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_mqtt_plain_text_listen_port: The service_mqtt_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_mqtt_plain_text_listen_port = service_mqtt_plain_text_listen_port

    @property
    def service_mqtt_plain_text_up(self):
        """Gets the service_mqtt_plain_text_up of this MsgVpn.  # noqa: E501

        Indicates whether the MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_mqtt_plain_text_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_plain_text_up

    @service_mqtt_plain_text_up.setter
    def service_mqtt_plain_text_up(self, service_mqtt_plain_text_up):
        """Sets the service_mqtt_plain_text_up of this MsgVpn.

        Indicates whether the MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :param service_mqtt_plain_text_up: The service_mqtt_plain_text_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_plain_text_up = service_mqtt_plain_text_up

    @property
    def service_mqtt_tls_compressed(self):
        """Gets the service_mqtt_tls_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related MQTT Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_compressed

    @service_mqtt_tls_compressed.setter
    def service_mqtt_tls_compressed(self, service_mqtt_tls_compressed):
        """Sets the service_mqtt_tls_compressed of this MsgVpn.

        Indicates whether the TLS related MQTT Service is compressed in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_compressed: The service_mqtt_tls_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_compressed = service_mqtt_tls_compressed

    @property
    def service_mqtt_tls_enabled(self):
        """Gets the service_mqtt_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for MQTT clients in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_enabled

    @service_mqtt_tls_enabled.setter
    def service_mqtt_tls_enabled(self, service_mqtt_tls_enabled):
        """Sets the service_mqtt_tls_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for MQTT clients in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_enabled: The service_mqtt_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_enabled = service_mqtt_tls_enabled

    @property
    def service_mqtt_tls_failure_reason(self):
        """Gets the service_mqtt_tls_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related MQTT Service failure in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_mqtt_tls_failure_reason

    @service_mqtt_tls_failure_reason.setter
    def service_mqtt_tls_failure_reason(self, service_mqtt_tls_failure_reason):
        """Sets the service_mqtt_tls_failure_reason of this MsgVpn.

        The reason for the TLS related MQTT Service failure in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_failure_reason: The service_mqtt_tls_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_mqtt_tls_failure_reason = service_mqtt_tls_failure_reason

    @property
    def service_mqtt_tls_listen_port(self):
        """Gets the service_mqtt_tls_listen_port of this MsgVpn.  # noqa: E501

        The port number for MQTT clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_mqtt_tls_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_mqtt_tls_listen_port

    @service_mqtt_tls_listen_port.setter
    def service_mqtt_tls_listen_port(self, service_mqtt_tls_listen_port):
        """Sets the service_mqtt_tls_listen_port of this MsgVpn.

        The port number for MQTT clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_mqtt_tls_listen_port: The service_mqtt_tls_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_mqtt_tls_listen_port = service_mqtt_tls_listen_port

    @property
    def service_mqtt_tls_up(self):
        """Gets the service_mqtt_tls_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_up

    @service_mqtt_tls_up.setter
    def service_mqtt_tls_up(self, service_mqtt_tls_up):
        """Sets the service_mqtt_tls_up of this MsgVpn.

        Indicates whether the TLS related MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_up: The service_mqtt_tls_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_up = service_mqtt_tls_up

    @property
    def service_mqtt_tls_web_socket_compressed(self):
        """Gets the service_mqtt_tls_web_socket_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related Web transport MQTT Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_web_socket_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_web_socket_compressed

    @service_mqtt_tls_web_socket_compressed.setter
    def service_mqtt_tls_web_socket_compressed(self, service_mqtt_tls_web_socket_compressed):
        """Sets the service_mqtt_tls_web_socket_compressed of this MsgVpn.

        Indicates whether the TLS related Web transport MQTT Service is compressed in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_web_socket_compressed: The service_mqtt_tls_web_socket_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_web_socket_compressed = service_mqtt_tls_web_socket_compressed

    @property
    def service_mqtt_tls_web_socket_enabled(self):
        """Gets the service_mqtt_tls_web_socket_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for MQTT Web clients in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_web_socket_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_web_socket_enabled

    @service_mqtt_tls_web_socket_enabled.setter
    def service_mqtt_tls_web_socket_enabled(self, service_mqtt_tls_web_socket_enabled):
        """Sets the service_mqtt_tls_web_socket_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for MQTT Web clients in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_web_socket_enabled: The service_mqtt_tls_web_socket_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_web_socket_enabled = service_mqtt_tls_web_socket_enabled

    @property
    def service_mqtt_tls_web_socket_failure_reason(self):
        """Gets the service_mqtt_tls_web_socket_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related Web transport MQTT Service failure in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_web_socket_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_mqtt_tls_web_socket_failure_reason

    @service_mqtt_tls_web_socket_failure_reason.setter
    def service_mqtt_tls_web_socket_failure_reason(self, service_mqtt_tls_web_socket_failure_reason):
        """Sets the service_mqtt_tls_web_socket_failure_reason of this MsgVpn.

        The reason for the TLS related Web transport MQTT Service failure in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_web_socket_failure_reason: The service_mqtt_tls_web_socket_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_mqtt_tls_web_socket_failure_reason = service_mqtt_tls_web_socket_failure_reason

    @property
    def service_mqtt_tls_web_socket_listen_port(self):
        """Gets the service_mqtt_tls_web_socket_listen_port of this MsgVpn.  # noqa: E501

        The port number for MQTT clients that connect to the Message VPN using WebSocket over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_mqtt_tls_web_socket_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_mqtt_tls_web_socket_listen_port

    @service_mqtt_tls_web_socket_listen_port.setter
    def service_mqtt_tls_web_socket_listen_port(self, service_mqtt_tls_web_socket_listen_port):
        """Sets the service_mqtt_tls_web_socket_listen_port of this MsgVpn.

        The port number for MQTT clients that connect to the Message VPN using WebSocket over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_mqtt_tls_web_socket_listen_port: The service_mqtt_tls_web_socket_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_mqtt_tls_web_socket_listen_port = service_mqtt_tls_web_socket_listen_port

    @property
    def service_mqtt_tls_web_socket_up(self):
        """Gets the service_mqtt_tls_web_socket_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related Web transport MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_mqtt_tls_web_socket_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_tls_web_socket_up

    @service_mqtt_tls_web_socket_up.setter
    def service_mqtt_tls_web_socket_up(self, service_mqtt_tls_web_socket_up):
        """Sets the service_mqtt_tls_web_socket_up of this MsgVpn.

        Indicates whether the TLS related Web transport MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :param service_mqtt_tls_web_socket_up: The service_mqtt_tls_web_socket_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_tls_web_socket_up = service_mqtt_tls_web_socket_up

    @property
    def service_mqtt_web_socket_compressed(self):
        """Gets the service_mqtt_web_socket_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the Web transport related MQTT Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_mqtt_web_socket_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_web_socket_compressed

    @service_mqtt_web_socket_compressed.setter
    def service_mqtt_web_socket_compressed(self, service_mqtt_web_socket_compressed):
        """Sets the service_mqtt_web_socket_compressed of this MsgVpn.

        Indicates whether the Web transport related MQTT Service is compressed in the Message VPN.  # noqa: E501

        :param service_mqtt_web_socket_compressed: The service_mqtt_web_socket_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_web_socket_compressed = service_mqtt_web_socket_compressed

    @property
    def service_mqtt_web_socket_enabled(self):
        """Gets the service_mqtt_web_socket_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the Web transport for the SMF Service is enabled in the Message VPN.  # noqa: E501

        :return: The service_mqtt_web_socket_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_web_socket_enabled

    @service_mqtt_web_socket_enabled.setter
    def service_mqtt_web_socket_enabled(self, service_mqtt_web_socket_enabled):
        """Sets the service_mqtt_web_socket_enabled of this MsgVpn.

        Indicates whether the Web transport for the SMF Service is enabled in the Message VPN.  # noqa: E501

        :param service_mqtt_web_socket_enabled: The service_mqtt_web_socket_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_web_socket_enabled = service_mqtt_web_socket_enabled

    @property
    def service_mqtt_web_socket_failure_reason(self):
        """Gets the service_mqtt_web_socket_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the Web transport related MQTT Service failure in the Message VPN.  # noqa: E501

        :return: The service_mqtt_web_socket_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_mqtt_web_socket_failure_reason

    @service_mqtt_web_socket_failure_reason.setter
    def service_mqtt_web_socket_failure_reason(self, service_mqtt_web_socket_failure_reason):
        """Sets the service_mqtt_web_socket_failure_reason of this MsgVpn.

        The reason for the Web transport related MQTT Service failure in the Message VPN.  # noqa: E501

        :param service_mqtt_web_socket_failure_reason: The service_mqtt_web_socket_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_mqtt_web_socket_failure_reason = service_mqtt_web_socket_failure_reason

    @property
    def service_mqtt_web_socket_listen_port(self):
        """Gets the service_mqtt_web_socket_listen_port of this MsgVpn.  # noqa: E501

        The port number for plain-text MQTT clients that connect to the Message VPN using WebSocket. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_mqtt_web_socket_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_mqtt_web_socket_listen_port

    @service_mqtt_web_socket_listen_port.setter
    def service_mqtt_web_socket_listen_port(self, service_mqtt_web_socket_listen_port):
        """Sets the service_mqtt_web_socket_listen_port of this MsgVpn.

        The port number for plain-text MQTT clients that connect to the Message VPN using WebSocket. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_mqtt_web_socket_listen_port: The service_mqtt_web_socket_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_mqtt_web_socket_listen_port = service_mqtt_web_socket_listen_port

    @property
    def service_mqtt_web_socket_up(self):
        """Gets the service_mqtt_web_socket_up of this MsgVpn.  # noqa: E501

        Indicates whether the Web transport related MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_mqtt_web_socket_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_mqtt_web_socket_up

    @service_mqtt_web_socket_up.setter
    def service_mqtt_web_socket_up(self, service_mqtt_web_socket_up):
        """Sets the service_mqtt_web_socket_up of this MsgVpn.

        Indicates whether the Web transport related MQTT Service is operationally up in the Message VPN.  # noqa: E501

        :param service_mqtt_web_socket_up: The service_mqtt_web_socket_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_mqtt_web_socket_up = service_mqtt_web_socket_up

    @property
    def service_rest_incoming_max_connection_count(self):
        """Gets the service_rest_incoming_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of REST incoming client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :return: The service_rest_incoming_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_rest_incoming_max_connection_count

    @service_rest_incoming_max_connection_count.setter
    def service_rest_incoming_max_connection_count(self, service_rest_incoming_max_connection_count):
        """Sets the service_rest_incoming_max_connection_count of this MsgVpn.

        The maximum number of REST incoming client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :param service_rest_incoming_max_connection_count: The service_rest_incoming_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_rest_incoming_max_connection_count = service_rest_incoming_max_connection_count

    @property
    def service_rest_incoming_plain_text_compressed(self):
        """Gets the service_rest_incoming_plain_text_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the incoming REST Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_plain_text_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_plain_text_compressed

    @service_rest_incoming_plain_text_compressed.setter
    def service_rest_incoming_plain_text_compressed(self, service_rest_incoming_plain_text_compressed):
        """Sets the service_rest_incoming_plain_text_compressed of this MsgVpn.

        Indicates whether the incoming REST Service is compressed in the Message VPN.  # noqa: E501

        :param service_rest_incoming_plain_text_compressed: The service_rest_incoming_plain_text_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_plain_text_compressed = service_rest_incoming_plain_text_compressed

    @property
    def service_rest_incoming_plain_text_enabled(self):
        """Gets the service_rest_incoming_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the REST Service is enabled in the Message VPN for incoming clients.  # noqa: E501

        :return: The service_rest_incoming_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_plain_text_enabled

    @service_rest_incoming_plain_text_enabled.setter
    def service_rest_incoming_plain_text_enabled(self, service_rest_incoming_plain_text_enabled):
        """Sets the service_rest_incoming_plain_text_enabled of this MsgVpn.

        Indicates whether the REST Service is enabled in the Message VPN for incoming clients.  # noqa: E501

        :param service_rest_incoming_plain_text_enabled: The service_rest_incoming_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_plain_text_enabled = service_rest_incoming_plain_text_enabled

    @property
    def service_rest_incoming_plain_text_failure_reason(self):
        """Gets the service_rest_incoming_plain_text_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the incoming REST Service failure in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_rest_incoming_plain_text_failure_reason

    @service_rest_incoming_plain_text_failure_reason.setter
    def service_rest_incoming_plain_text_failure_reason(self, service_rest_incoming_plain_text_failure_reason):
        """Sets the service_rest_incoming_plain_text_failure_reason of this MsgVpn.

        The reason for the incoming REST Service failure in the Message VPN.  # noqa: E501

        :param service_rest_incoming_plain_text_failure_reason: The service_rest_incoming_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_rest_incoming_plain_text_failure_reason = service_rest_incoming_plain_text_failure_reason

    @property
    def service_rest_incoming_plain_text_listen_port(self):
        """Gets the service_rest_incoming_plain_text_listen_port of this MsgVpn.  # noqa: E501

        The port number for incoming plain-text REST clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_rest_incoming_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_rest_incoming_plain_text_listen_port

    @service_rest_incoming_plain_text_listen_port.setter
    def service_rest_incoming_plain_text_listen_port(self, service_rest_incoming_plain_text_listen_port):
        """Sets the service_rest_incoming_plain_text_listen_port of this MsgVpn.

        The port number for incoming plain-text REST clients that connect to the Message VPN. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_rest_incoming_plain_text_listen_port: The service_rest_incoming_plain_text_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_rest_incoming_plain_text_listen_port = service_rest_incoming_plain_text_listen_port

    @property
    def service_rest_incoming_plain_text_up(self):
        """Gets the service_rest_incoming_plain_text_up of this MsgVpn.  # noqa: E501

        Indicates whether the incoming REST Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_plain_text_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_plain_text_up

    @service_rest_incoming_plain_text_up.setter
    def service_rest_incoming_plain_text_up(self, service_rest_incoming_plain_text_up):
        """Sets the service_rest_incoming_plain_text_up of this MsgVpn.

        Indicates whether the incoming REST Service is operationally up in the Message VPN.  # noqa: E501

        :param service_rest_incoming_plain_text_up: The service_rest_incoming_plain_text_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_plain_text_up = service_rest_incoming_plain_text_up

    @property
    def service_rest_incoming_tls_compressed(self):
        """Gets the service_rest_incoming_tls_compressed of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related incoming REST Service is compressed in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_tls_compressed of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_tls_compressed

    @service_rest_incoming_tls_compressed.setter
    def service_rest_incoming_tls_compressed(self, service_rest_incoming_tls_compressed):
        """Sets the service_rest_incoming_tls_compressed of this MsgVpn.

        Indicates whether the TLS related incoming REST Service is compressed in the Message VPN.  # noqa: E501

        :param service_rest_incoming_tls_compressed: The service_rest_incoming_tls_compressed of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_tls_compressed = service_rest_incoming_tls_compressed

    @property
    def service_rest_incoming_tls_enabled(self):
        """Gets the service_rest_incoming_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for incoming REST clients in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_tls_enabled

    @service_rest_incoming_tls_enabled.setter
    def service_rest_incoming_tls_enabled(self, service_rest_incoming_tls_enabled):
        """Sets the service_rest_incoming_tls_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for incoming REST clients in the Message VPN.  # noqa: E501

        :param service_rest_incoming_tls_enabled: The service_rest_incoming_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_tls_enabled = service_rest_incoming_tls_enabled

    @property
    def service_rest_incoming_tls_failure_reason(self):
        """Gets the service_rest_incoming_tls_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related incoming REST Service failure in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_tls_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_rest_incoming_tls_failure_reason

    @service_rest_incoming_tls_failure_reason.setter
    def service_rest_incoming_tls_failure_reason(self, service_rest_incoming_tls_failure_reason):
        """Sets the service_rest_incoming_tls_failure_reason of this MsgVpn.

        The reason for the TLS related incoming REST Service failure in the Message VPN.  # noqa: E501

        :param service_rest_incoming_tls_failure_reason: The service_rest_incoming_tls_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_rest_incoming_tls_failure_reason = service_rest_incoming_tls_failure_reason

    @property
    def service_rest_incoming_tls_listen_port(self):
        """Gets the service_rest_incoming_tls_listen_port of this MsgVpn.  # noqa: E501

        The port number for incoming REST clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :return: The service_rest_incoming_tls_listen_port of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_rest_incoming_tls_listen_port

    @service_rest_incoming_tls_listen_port.setter
    def service_rest_incoming_tls_listen_port(self, service_rest_incoming_tls_listen_port):
        """Sets the service_rest_incoming_tls_listen_port of this MsgVpn.

        The port number for incoming REST clients that connect to the Message VPN over TLS. The port must be unique across the message backbone. A value of 0 means that the listen-port is unassigned and cannot be enabled.  # noqa: E501

        :param service_rest_incoming_tls_listen_port: The service_rest_incoming_tls_listen_port of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_rest_incoming_tls_listen_port = service_rest_incoming_tls_listen_port

    @property
    def service_rest_incoming_tls_up(self):
        """Gets the service_rest_incoming_tls_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related incoming REST Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_rest_incoming_tls_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_rest_incoming_tls_up

    @service_rest_incoming_tls_up.setter
    def service_rest_incoming_tls_up(self, service_rest_incoming_tls_up):
        """Sets the service_rest_incoming_tls_up of this MsgVpn.

        Indicates whether the TLS related incoming REST Service is operationally up in the Message VPN.  # noqa: E501

        :param service_rest_incoming_tls_up: The service_rest_incoming_tls_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_rest_incoming_tls_up = service_rest_incoming_tls_up

    @property
    def service_rest_mode(self):
        """Gets the service_rest_mode of this MsgVpn.  # noqa: E501

        The REST service mode for incoming REST clients that connect to the Message VPN. The allowed values and their meaning are:  <pre> \"gateway\" - Act as a message gateway through which REST messages are propagated. \"messaging\" - Act as a message broker on which REST messages are queued. </pre>   # noqa: E501

        :return: The service_rest_mode of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_rest_mode

    @service_rest_mode.setter
    def service_rest_mode(self, service_rest_mode):
        """Sets the service_rest_mode of this MsgVpn.

        The REST service mode for incoming REST clients that connect to the Message VPN. The allowed values and their meaning are:  <pre> \"gateway\" - Act as a message gateway through which REST messages are propagated. \"messaging\" - Act as a message broker on which REST messages are queued. </pre>   # noqa: E501

        :param service_rest_mode: The service_rest_mode of this MsgVpn.  # noqa: E501
        :type: str
        """
        allowed_values = ["gateway", "messaging"]  # noqa: E501
        if service_rest_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `service_rest_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(service_rest_mode, allowed_values)
            )

        self._service_rest_mode = service_rest_mode

    @property
    def service_rest_outgoing_max_connection_count(self):
        """Gets the service_rest_outgoing_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of REST Consumer (outgoing) client connections that can be simultaneously connected to the Message VPN.  # noqa: E501

        :return: The service_rest_outgoing_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_rest_outgoing_max_connection_count

    @service_rest_outgoing_max_connection_count.setter
    def service_rest_outgoing_max_connection_count(self, service_rest_outgoing_max_connection_count):
        """Sets the service_rest_outgoing_max_connection_count of this MsgVpn.

        The maximum number of REST Consumer (outgoing) client connections that can be simultaneously connected to the Message VPN.  # noqa: E501

        :param service_rest_outgoing_max_connection_count: The service_rest_outgoing_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_rest_outgoing_max_connection_count = service_rest_outgoing_max_connection_count

    @property
    def service_smf_max_connection_count(self):
        """Gets the service_smf_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of SMF client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :return: The service_smf_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_smf_max_connection_count

    @service_smf_max_connection_count.setter
    def service_smf_max_connection_count(self, service_smf_max_connection_count):
        """Sets the service_smf_max_connection_count of this MsgVpn.

        The maximum number of SMF client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :param service_smf_max_connection_count: The service_smf_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_smf_max_connection_count = service_smf_max_connection_count

    @property
    def service_smf_plain_text_enabled(self):
        """Gets the service_smf_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the SMF Service is enabled in the Message VPN.  # noqa: E501

        :return: The service_smf_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_smf_plain_text_enabled

    @service_smf_plain_text_enabled.setter
    def service_smf_plain_text_enabled(self, service_smf_plain_text_enabled):
        """Sets the service_smf_plain_text_enabled of this MsgVpn.

        Indicates whether the SMF Service is enabled in the Message VPN.  # noqa: E501

        :param service_smf_plain_text_enabled: The service_smf_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_smf_plain_text_enabled = service_smf_plain_text_enabled

    @property
    def service_smf_plain_text_failure_reason(self):
        """Gets the service_smf_plain_text_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the SMF Service failure in the Message VPN.  # noqa: E501

        :return: The service_smf_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_smf_plain_text_failure_reason

    @service_smf_plain_text_failure_reason.setter
    def service_smf_plain_text_failure_reason(self, service_smf_plain_text_failure_reason):
        """Sets the service_smf_plain_text_failure_reason of this MsgVpn.

        The reason for the SMF Service failure in the Message VPN.  # noqa: E501

        :param service_smf_plain_text_failure_reason: The service_smf_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_smf_plain_text_failure_reason = service_smf_plain_text_failure_reason

    @property
    def service_smf_plain_text_up(self):
        """Gets the service_smf_plain_text_up of this MsgVpn.  # noqa: E501

        Indicates whether the SMF Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_smf_plain_text_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_smf_plain_text_up

    @service_smf_plain_text_up.setter
    def service_smf_plain_text_up(self, service_smf_plain_text_up):
        """Sets the service_smf_plain_text_up of this MsgVpn.

        Indicates whether the SMF Service is operationally up in the Message VPN.  # noqa: E501

        :param service_smf_plain_text_up: The service_smf_plain_text_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_smf_plain_text_up = service_smf_plain_text_up

    @property
    def service_smf_tls_enabled(self):
        """Gets the service_smf_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for SMF clients in the Message VPN.  # noqa: E501

        :return: The service_smf_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_smf_tls_enabled

    @service_smf_tls_enabled.setter
    def service_smf_tls_enabled(self, service_smf_tls_enabled):
        """Sets the service_smf_tls_enabled of this MsgVpn.

        Indicates whether encryption (TLS) is enabled for SMF clients in the Message VPN.  # noqa: E501

        :param service_smf_tls_enabled: The service_smf_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_smf_tls_enabled = service_smf_tls_enabled

    @property
    def service_smf_tls_failure_reason(self):
        """Gets the service_smf_tls_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related SMF Service failure in the Message VPN.  # noqa: E501

        :return: The service_smf_tls_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_smf_tls_failure_reason

    @service_smf_tls_failure_reason.setter
    def service_smf_tls_failure_reason(self, service_smf_tls_failure_reason):
        """Sets the service_smf_tls_failure_reason of this MsgVpn.

        The reason for the TLS related SMF Service failure in the Message VPN.  # noqa: E501

        :param service_smf_tls_failure_reason: The service_smf_tls_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_smf_tls_failure_reason = service_smf_tls_failure_reason

    @property
    def service_smf_tls_up(self):
        """Gets the service_smf_tls_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related SMF Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_smf_tls_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_smf_tls_up

    @service_smf_tls_up.setter
    def service_smf_tls_up(self, service_smf_tls_up):
        """Sets the service_smf_tls_up of this MsgVpn.

        Indicates whether the TLS related SMF Service is operationally up in the Message VPN.  # noqa: E501

        :param service_smf_tls_up: The service_smf_tls_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_smf_tls_up = service_smf_tls_up

    @property
    def service_web_max_connection_count(self):
        """Gets the service_web_max_connection_count of this MsgVpn.  # noqa: E501

        The maximum number of Web Transport client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :return: The service_web_max_connection_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._service_web_max_connection_count

    @service_web_max_connection_count.setter
    def service_web_max_connection_count(self, service_web_max_connection_count):
        """Sets the service_web_max_connection_count of this MsgVpn.

        The maximum number of Web Transport client connections that can be simultaneously connected to the Message VPN. This value may be higher than supported by the platform.  # noqa: E501

        :param service_web_max_connection_count: The service_web_max_connection_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._service_web_max_connection_count = service_web_max_connection_count

    @property
    def service_web_plain_text_enabled(self):
        """Gets the service_web_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether the Web transport for the SMF Service is enabled in the Message VPN.  # noqa: E501

        :return: The service_web_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_web_plain_text_enabled

    @service_web_plain_text_enabled.setter
    def service_web_plain_text_enabled(self, service_web_plain_text_enabled):
        """Sets the service_web_plain_text_enabled of this MsgVpn.

        Indicates whether the Web transport for the SMF Service is enabled in the Message VPN.  # noqa: E501

        :param service_web_plain_text_enabled: The service_web_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_web_plain_text_enabled = service_web_plain_text_enabled

    @property
    def service_web_plain_text_failure_reason(self):
        """Gets the service_web_plain_text_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the Web transport related SMF Service failure in the Message VPN.  # noqa: E501

        :return: The service_web_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_web_plain_text_failure_reason

    @service_web_plain_text_failure_reason.setter
    def service_web_plain_text_failure_reason(self, service_web_plain_text_failure_reason):
        """Sets the service_web_plain_text_failure_reason of this MsgVpn.

        The reason for the Web transport related SMF Service failure in the Message VPN.  # noqa: E501

        :param service_web_plain_text_failure_reason: The service_web_plain_text_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_web_plain_text_failure_reason = service_web_plain_text_failure_reason

    @property
    def service_web_plain_text_up(self):
        """Gets the service_web_plain_text_up of this MsgVpn.  # noqa: E501

        Indicates whether the Web transport for the SMF Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_web_plain_text_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_web_plain_text_up

    @service_web_plain_text_up.setter
    def service_web_plain_text_up(self, service_web_plain_text_up):
        """Sets the service_web_plain_text_up of this MsgVpn.

        Indicates whether the Web transport for the SMF Service is operationally up in the Message VPN.  # noqa: E501

        :param service_web_plain_text_up: The service_web_plain_text_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_web_plain_text_up = service_web_plain_text_up

    @property
    def service_web_tls_enabled(self):
        """Gets the service_web_tls_enabled of this MsgVpn.  # noqa: E501

        Indicates whether TLS is enabled for SMF clients in the Message VPN that use the Web transport.  # noqa: E501

        :return: The service_web_tls_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_web_tls_enabled

    @service_web_tls_enabled.setter
    def service_web_tls_enabled(self, service_web_tls_enabled):
        """Sets the service_web_tls_enabled of this MsgVpn.

        Indicates whether TLS is enabled for SMF clients in the Message VPN that use the Web transport.  # noqa: E501

        :param service_web_tls_enabled: The service_web_tls_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_web_tls_enabled = service_web_tls_enabled

    @property
    def service_web_tls_failure_reason(self):
        """Gets the service_web_tls_failure_reason of this MsgVpn.  # noqa: E501

        The reason for the TLS related Web transport SMF Service failure in the Message VPN.  # noqa: E501

        :return: The service_web_tls_failure_reason of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._service_web_tls_failure_reason

    @service_web_tls_failure_reason.setter
    def service_web_tls_failure_reason(self, service_web_tls_failure_reason):
        """Sets the service_web_tls_failure_reason of this MsgVpn.

        The reason for the TLS related Web transport SMF Service failure in the Message VPN.  # noqa: E501

        :param service_web_tls_failure_reason: The service_web_tls_failure_reason of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._service_web_tls_failure_reason = service_web_tls_failure_reason

    @property
    def service_web_tls_up(self):
        """Gets the service_web_tls_up of this MsgVpn.  # noqa: E501

        Indicates whether the TLS related Web transport SMF Service is operationally up in the Message VPN.  # noqa: E501

        :return: The service_web_tls_up of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._service_web_tls_up

    @service_web_tls_up.setter
    def service_web_tls_up(self, service_web_tls_up):
        """Sets the service_web_tls_up of this MsgVpn.

        Indicates whether the TLS related Web transport SMF Service is operationally up in the Message VPN.  # noqa: E501

        :param service_web_tls_up: The service_web_tls_up of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._service_web_tls_up = service_web_tls_up

    @property
    def state(self):
        """Gets the state of this MsgVpn.  # noqa: E501

        The operational state of the local Message VPN. The allowed values and their meaning are:  <pre> \"up\" - The Message VPN is operationally up. \"down\" - The Message VPN is operationally down. \"standby\" - The Message VPN is operationally replication standby. </pre>   # noqa: E501

        :return: The state of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this MsgVpn.

        The operational state of the local Message VPN. The allowed values and their meaning are:  <pre> \"up\" - The Message VPN is operationally up. \"down\" - The Message VPN is operationally down. \"standby\" - The Message VPN is operationally replication standby. </pre>   # noqa: E501

        :param state: The state of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def subscription_export_progress(self):
        """Gets the subscription_export_progress of this MsgVpn.  # noqa: E501

        The progress of the subscription export task, in percent complete.  # noqa: E501

        :return: The subscription_export_progress of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._subscription_export_progress

    @subscription_export_progress.setter
    def subscription_export_progress(self, subscription_export_progress):
        """Sets the subscription_export_progress of this MsgVpn.

        The progress of the subscription export task, in percent complete.  # noqa: E501

        :param subscription_export_progress: The subscription_export_progress of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._subscription_export_progress = subscription_export_progress

    @property
    def system_manager(self):
        """Gets the system_manager of this MsgVpn.  # noqa: E501

        Indicates whether the Message VPN is the system manager for handling system level SEMP get requests and system level event publishing.  # noqa: E501

        :return: The system_manager of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._system_manager

    @system_manager.setter
    def system_manager(self, system_manager):
        """Sets the system_manager of this MsgVpn.

        Indicates whether the Message VPN is the system manager for handling system level SEMP get requests and system level event publishing.  # noqa: E501

        :param system_manager: The system_manager of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._system_manager = system_manager

    @property
    def tls_allow_downgrade_to_plain_text_enabled(self):
        """Gets the tls_allow_downgrade_to_plain_text_enabled of this MsgVpn.  # noqa: E501

        Indicates whether SMF clients connected to the Message VPN are allowed to downgrade their connections from TLS to plain text.  # noqa: E501

        :return: The tls_allow_downgrade_to_plain_text_enabled of this MsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._tls_allow_downgrade_to_plain_text_enabled

    @tls_allow_downgrade_to_plain_text_enabled.setter
    def tls_allow_downgrade_to_plain_text_enabled(self, tls_allow_downgrade_to_plain_text_enabled):
        """Sets the tls_allow_downgrade_to_plain_text_enabled of this MsgVpn.

        Indicates whether SMF clients connected to the Message VPN are allowed to downgrade their connections from TLS to plain text.  # noqa: E501

        :param tls_allow_downgrade_to_plain_text_enabled: The tls_allow_downgrade_to_plain_text_enabled of this MsgVpn.  # noqa: E501
        :type: bool
        """

        self._tls_allow_downgrade_to_plain_text_enabled = tls_allow_downgrade_to_plain_text_enabled

    @property
    def tls_average_rx_byte_rate(self):
        """Gets the tls_average_rx_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the TLS message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The tls_average_rx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_average_rx_byte_rate

    @tls_average_rx_byte_rate.setter
    def tls_average_rx_byte_rate(self, tls_average_rx_byte_rate):
        """Sets the tls_average_rx_byte_rate of this MsgVpn.

        The one minute average of the TLS message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param tls_average_rx_byte_rate: The tls_average_rx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_average_rx_byte_rate = tls_average_rx_byte_rate

    @property
    def tls_average_tx_byte_rate(self):
        """Gets the tls_average_tx_byte_rate of this MsgVpn.  # noqa: E501

        The one minute average of the TLS message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The tls_average_tx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_average_tx_byte_rate

    @tls_average_tx_byte_rate.setter
    def tls_average_tx_byte_rate(self, tls_average_tx_byte_rate):
        """Sets the tls_average_tx_byte_rate of this MsgVpn.

        The one minute average of the TLS message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param tls_average_tx_byte_rate: The tls_average_tx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_average_tx_byte_rate = tls_average_tx_byte_rate

    @property
    def tls_rx_byte_count(self):
        """Gets the tls_rx_byte_count of this MsgVpn.  # noqa: E501

        The amount of TLS messages received by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The tls_rx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_rx_byte_count

    @tls_rx_byte_count.setter
    def tls_rx_byte_count(self, tls_rx_byte_count):
        """Sets the tls_rx_byte_count of this MsgVpn.

        The amount of TLS messages received by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param tls_rx_byte_count: The tls_rx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_rx_byte_count = tls_rx_byte_count

    @property
    def tls_rx_byte_rate(self):
        """Gets the tls_rx_byte_rate of this MsgVpn.  # noqa: E501

        The current TLS message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The tls_rx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_rx_byte_rate

    @tls_rx_byte_rate.setter
    def tls_rx_byte_rate(self, tls_rx_byte_rate):
        """Sets the tls_rx_byte_rate of this MsgVpn.

        The current TLS message rate received by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param tls_rx_byte_rate: The tls_rx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_rx_byte_rate = tls_rx_byte_rate

    @property
    def tls_tx_byte_count(self):
        """Gets the tls_tx_byte_count of this MsgVpn.  # noqa: E501

        The amount of TLS messages transmitted by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :return: The tls_tx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_tx_byte_count

    @tls_tx_byte_count.setter
    def tls_tx_byte_count(self, tls_tx_byte_count):
        """Sets the tls_tx_byte_count of this MsgVpn.

        The amount of TLS messages transmitted by the Message VPN, in bytes (B). Available since 2.13.  # noqa: E501

        :param tls_tx_byte_count: The tls_tx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_tx_byte_count = tls_tx_byte_count

    @property
    def tls_tx_byte_rate(self):
        """Gets the tls_tx_byte_rate of this MsgVpn.  # noqa: E501

        The current TLS message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The tls_tx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tls_tx_byte_rate

    @tls_tx_byte_rate.setter
    def tls_tx_byte_rate(self, tls_tx_byte_rate):
        """Sets the tls_tx_byte_rate of this MsgVpn.

        The current TLS message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param tls_tx_byte_rate: The tls_tx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tls_tx_byte_rate = tls_tx_byte_rate

    @property
    def tx_byte_count(self):
        """Gets the tx_byte_count of this MsgVpn.  # noqa: E501

        The amount of messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The tx_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_count

    @tx_byte_count.setter
    def tx_byte_count(self, tx_byte_count):
        """Sets the tx_byte_count of this MsgVpn.

        The amount of messages transmitted to clients by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param tx_byte_count: The tx_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_byte_count = tx_byte_count

    @property
    def tx_byte_rate(self):
        """Gets the tx_byte_rate of this MsgVpn.  # noqa: E501

        The current message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The tx_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_byte_rate

    @tx_byte_rate.setter
    def tx_byte_rate(self, tx_byte_rate):
        """Sets the tx_byte_rate of this MsgVpn.

        The current message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param tx_byte_rate: The tx_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_byte_rate = tx_byte_rate

    @property
    def tx_compressed_byte_count(self):
        """Gets the tx_compressed_byte_count of this MsgVpn.  # noqa: E501

        The amount of compressed messages transmitted by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The tx_compressed_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_compressed_byte_count

    @tx_compressed_byte_count.setter
    def tx_compressed_byte_count(self, tx_compressed_byte_count):
        """Sets the tx_compressed_byte_count of this MsgVpn.

        The amount of compressed messages transmitted by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param tx_compressed_byte_count: The tx_compressed_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_compressed_byte_count = tx_compressed_byte_count

    @property
    def tx_compressed_byte_rate(self):
        """Gets the tx_compressed_byte_rate of this MsgVpn.  # noqa: E501

        The current compressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The tx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_compressed_byte_rate

    @tx_compressed_byte_rate.setter
    def tx_compressed_byte_rate(self, tx_compressed_byte_rate):
        """Sets the tx_compressed_byte_rate of this MsgVpn.

        The current compressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param tx_compressed_byte_rate: The tx_compressed_byte_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_compressed_byte_rate = tx_compressed_byte_rate

    @property
    def tx_compression_ratio(self):
        """Gets the tx_compression_ratio of this MsgVpn.  # noqa: E501

        The compression ratio for messages transmitted by the message VPN. Available since 2.12.  # noqa: E501

        :return: The tx_compression_ratio of this MsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._tx_compression_ratio

    @tx_compression_ratio.setter
    def tx_compression_ratio(self, tx_compression_ratio):
        """Sets the tx_compression_ratio of this MsgVpn.

        The compression ratio for messages transmitted by the message VPN. Available since 2.12.  # noqa: E501

        :param tx_compression_ratio: The tx_compression_ratio of this MsgVpn.  # noqa: E501
        :type: str
        """

        self._tx_compression_ratio = tx_compression_ratio

    @property
    def tx_msg_count(self):
        """Gets the tx_msg_count of this MsgVpn.  # noqa: E501

        The number of messages transmitted to clients by the Message VPN. Available since 2.12.  # noqa: E501

        :return: The tx_msg_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_count

    @tx_msg_count.setter
    def tx_msg_count(self, tx_msg_count):
        """Sets the tx_msg_count of this MsgVpn.

        The number of messages transmitted to clients by the Message VPN. Available since 2.12.  # noqa: E501

        :param tx_msg_count: The tx_msg_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_msg_count = tx_msg_count

    @property
    def tx_msg_rate(self):
        """Gets the tx_msg_rate of this MsgVpn.  # noqa: E501

        The current message rate transmitted by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The tx_msg_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_msg_rate

    @tx_msg_rate.setter
    def tx_msg_rate(self, tx_msg_rate):
        """Sets the tx_msg_rate of this MsgVpn.

        The current message rate transmitted by the Message VPN, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param tx_msg_rate: The tx_msg_rate of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_msg_rate = tx_msg_rate

    @property
    def tx_uncompressed_byte_count(self):
        """Gets the tx_uncompressed_byte_count of this MsgVpn.  # noqa: E501

        The amount of uncompressed messages transmitted by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :return: The tx_uncompressed_byte_count of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_uncompressed_byte_count

    @tx_uncompressed_byte_count.setter
    def tx_uncompressed_byte_count(self, tx_uncompressed_byte_count):
        """Sets the tx_uncompressed_byte_count of this MsgVpn.

        The amount of uncompressed messages transmitted by the Message VPN, in bytes (B). Available since 2.12.  # noqa: E501

        :param tx_uncompressed_byte_count: The tx_uncompressed_byte_count of this MsgVpn.  # noqa: E501
        :type: int
        """

        self._tx_uncompressed_byte_count = tx_uncompressed_byte_count

    @property
    def tx_uncompressed_byte_rate(self):
        """Gets the tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501

        The current uncompressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :return: The tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._tx_uncompressed_byte_rate

    @tx_uncompressed_byte_rate.setter
    def tx_uncompressed_byte_rate(self, tx_uncompressed_byte_rate):
        """Sets the tx_uncompressed_byte_rate of this MsgVpn.

        The current uncompressed message rate transmitted by the Message VPN, in bytes per second (B/sec). Available since 2.12.  # noqa: E501

        :param tx_uncompressed_byte_rate: The tx_uncompressed_byte_rate of this MsgVpn.  # noqa: E501
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
        if issubclass(MsgVpn, dict):
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
        if not isinstance(other, MsgVpn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
