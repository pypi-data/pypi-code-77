# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.13
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnJndiConnectionFactory(object):
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
        'allow_duplicate_client_id_enabled': 'bool',
        'client_description': 'str',
        'client_id': 'str',
        'connection_factory_name': 'str',
        'dto_receive_override_enabled': 'bool',
        'dto_receive_subscriber_local_priority': 'int',
        'dto_receive_subscriber_network_priority': 'int',
        'dto_send_enabled': 'bool',
        'dynamic_endpoint_create_durable_enabled': 'bool',
        'dynamic_endpoint_respect_ttl_enabled': 'bool',
        'guaranteed_receive_ack_timeout': 'int',
        'guaranteed_receive_window_size': 'int',
        'guaranteed_receive_window_size_ack_threshold': 'int',
        'guaranteed_send_ack_timeout': 'int',
        'guaranteed_send_window_size': 'int',
        'messaging_default_delivery_mode': 'str',
        'messaging_default_dmq_eligible_enabled': 'bool',
        'messaging_default_eliding_eligible_enabled': 'bool',
        'messaging_jmsx_user_id_enabled': 'bool',
        'messaging_text_in_xml_payload_enabled': 'bool',
        'msg_vpn_name': 'str',
        'transport_compression_level': 'int',
        'transport_connect_retry_count': 'int',
        'transport_connect_retry_per_host_count': 'int',
        'transport_connect_timeout': 'int',
        'transport_direct_transport_enabled': 'bool',
        'transport_keepalive_count': 'int',
        'transport_keepalive_enabled': 'bool',
        'transport_keepalive_interval': 'int',
        'transport_msg_callback_on_io_thread_enabled': 'bool',
        'transport_optimize_direct_enabled': 'bool',
        'transport_port': 'int',
        'transport_read_timeout': 'int',
        'transport_receive_buffer_size': 'int',
        'transport_reconnect_retry_count': 'int',
        'transport_reconnect_retry_wait': 'int',
        'transport_send_buffer_size': 'int',
        'transport_tcp_no_delay_enabled': 'bool',
        'xa_enabled': 'bool'
    }

    attribute_map = {
        'allow_duplicate_client_id_enabled': 'allowDuplicateClientIdEnabled',
        'client_description': 'clientDescription',
        'client_id': 'clientId',
        'connection_factory_name': 'connectionFactoryName',
        'dto_receive_override_enabled': 'dtoReceiveOverrideEnabled',
        'dto_receive_subscriber_local_priority': 'dtoReceiveSubscriberLocalPriority',
        'dto_receive_subscriber_network_priority': 'dtoReceiveSubscriberNetworkPriority',
        'dto_send_enabled': 'dtoSendEnabled',
        'dynamic_endpoint_create_durable_enabled': 'dynamicEndpointCreateDurableEnabled',
        'dynamic_endpoint_respect_ttl_enabled': 'dynamicEndpointRespectTtlEnabled',
        'guaranteed_receive_ack_timeout': 'guaranteedReceiveAckTimeout',
        'guaranteed_receive_window_size': 'guaranteedReceiveWindowSize',
        'guaranteed_receive_window_size_ack_threshold': 'guaranteedReceiveWindowSizeAckThreshold',
        'guaranteed_send_ack_timeout': 'guaranteedSendAckTimeout',
        'guaranteed_send_window_size': 'guaranteedSendWindowSize',
        'messaging_default_delivery_mode': 'messagingDefaultDeliveryMode',
        'messaging_default_dmq_eligible_enabled': 'messagingDefaultDmqEligibleEnabled',
        'messaging_default_eliding_eligible_enabled': 'messagingDefaultElidingEligibleEnabled',
        'messaging_jmsx_user_id_enabled': 'messagingJmsxUserIdEnabled',
        'messaging_text_in_xml_payload_enabled': 'messagingTextInXmlPayloadEnabled',
        'msg_vpn_name': 'msgVpnName',
        'transport_compression_level': 'transportCompressionLevel',
        'transport_connect_retry_count': 'transportConnectRetryCount',
        'transport_connect_retry_per_host_count': 'transportConnectRetryPerHostCount',
        'transport_connect_timeout': 'transportConnectTimeout',
        'transport_direct_transport_enabled': 'transportDirectTransportEnabled',
        'transport_keepalive_count': 'transportKeepaliveCount',
        'transport_keepalive_enabled': 'transportKeepaliveEnabled',
        'transport_keepalive_interval': 'transportKeepaliveInterval',
        'transport_msg_callback_on_io_thread_enabled': 'transportMsgCallbackOnIoThreadEnabled',
        'transport_optimize_direct_enabled': 'transportOptimizeDirectEnabled',
        'transport_port': 'transportPort',
        'transport_read_timeout': 'transportReadTimeout',
        'transport_receive_buffer_size': 'transportReceiveBufferSize',
        'transport_reconnect_retry_count': 'transportReconnectRetryCount',
        'transport_reconnect_retry_wait': 'transportReconnectRetryWait',
        'transport_send_buffer_size': 'transportSendBufferSize',
        'transport_tcp_no_delay_enabled': 'transportTcpNoDelayEnabled',
        'xa_enabled': 'xaEnabled'
    }

    def __init__(self, allow_duplicate_client_id_enabled=None, client_description=None, client_id=None, connection_factory_name=None, dto_receive_override_enabled=None, dto_receive_subscriber_local_priority=None, dto_receive_subscriber_network_priority=None, dto_send_enabled=None, dynamic_endpoint_create_durable_enabled=None, dynamic_endpoint_respect_ttl_enabled=None, guaranteed_receive_ack_timeout=None, guaranteed_receive_window_size=None, guaranteed_receive_window_size_ack_threshold=None, guaranteed_send_ack_timeout=None, guaranteed_send_window_size=None, messaging_default_delivery_mode=None, messaging_default_dmq_eligible_enabled=None, messaging_default_eliding_eligible_enabled=None, messaging_jmsx_user_id_enabled=None, messaging_text_in_xml_payload_enabled=None, msg_vpn_name=None, transport_compression_level=None, transport_connect_retry_count=None, transport_connect_retry_per_host_count=None, transport_connect_timeout=None, transport_direct_transport_enabled=None, transport_keepalive_count=None, transport_keepalive_enabled=None, transport_keepalive_interval=None, transport_msg_callback_on_io_thread_enabled=None, transport_optimize_direct_enabled=None, transport_port=None, transport_read_timeout=None, transport_receive_buffer_size=None, transport_reconnect_retry_count=None, transport_reconnect_retry_wait=None, transport_send_buffer_size=None, transport_tcp_no_delay_enabled=None, xa_enabled=None):  # noqa: E501
        """MsgVpnJndiConnectionFactory - a model defined in Swagger"""  # noqa: E501

        self._allow_duplicate_client_id_enabled = None
        self._client_description = None
        self._client_id = None
        self._connection_factory_name = None
        self._dto_receive_override_enabled = None
        self._dto_receive_subscriber_local_priority = None
        self._dto_receive_subscriber_network_priority = None
        self._dto_send_enabled = None
        self._dynamic_endpoint_create_durable_enabled = None
        self._dynamic_endpoint_respect_ttl_enabled = None
        self._guaranteed_receive_ack_timeout = None
        self._guaranteed_receive_window_size = None
        self._guaranteed_receive_window_size_ack_threshold = None
        self._guaranteed_send_ack_timeout = None
        self._guaranteed_send_window_size = None
        self._messaging_default_delivery_mode = None
        self._messaging_default_dmq_eligible_enabled = None
        self._messaging_default_eliding_eligible_enabled = None
        self._messaging_jmsx_user_id_enabled = None
        self._messaging_text_in_xml_payload_enabled = None
        self._msg_vpn_name = None
        self._transport_compression_level = None
        self._transport_connect_retry_count = None
        self._transport_connect_retry_per_host_count = None
        self._transport_connect_timeout = None
        self._transport_direct_transport_enabled = None
        self._transport_keepalive_count = None
        self._transport_keepalive_enabled = None
        self._transport_keepalive_interval = None
        self._transport_msg_callback_on_io_thread_enabled = None
        self._transport_optimize_direct_enabled = None
        self._transport_port = None
        self._transport_read_timeout = None
        self._transport_receive_buffer_size = None
        self._transport_reconnect_retry_count = None
        self._transport_reconnect_retry_wait = None
        self._transport_send_buffer_size = None
        self._transport_tcp_no_delay_enabled = None
        self._xa_enabled = None
        self.discriminator = None

        if allow_duplicate_client_id_enabled is not None:
            self.allow_duplicate_client_id_enabled = allow_duplicate_client_id_enabled
        if client_description is not None:
            self.client_description = client_description
        if client_id is not None:
            self.client_id = client_id
        if connection_factory_name is not None:
            self.connection_factory_name = connection_factory_name
        if dto_receive_override_enabled is not None:
            self.dto_receive_override_enabled = dto_receive_override_enabled
        if dto_receive_subscriber_local_priority is not None:
            self.dto_receive_subscriber_local_priority = dto_receive_subscriber_local_priority
        if dto_receive_subscriber_network_priority is not None:
            self.dto_receive_subscriber_network_priority = dto_receive_subscriber_network_priority
        if dto_send_enabled is not None:
            self.dto_send_enabled = dto_send_enabled
        if dynamic_endpoint_create_durable_enabled is not None:
            self.dynamic_endpoint_create_durable_enabled = dynamic_endpoint_create_durable_enabled
        if dynamic_endpoint_respect_ttl_enabled is not None:
            self.dynamic_endpoint_respect_ttl_enabled = dynamic_endpoint_respect_ttl_enabled
        if guaranteed_receive_ack_timeout is not None:
            self.guaranteed_receive_ack_timeout = guaranteed_receive_ack_timeout
        if guaranteed_receive_window_size is not None:
            self.guaranteed_receive_window_size = guaranteed_receive_window_size
        if guaranteed_receive_window_size_ack_threshold is not None:
            self.guaranteed_receive_window_size_ack_threshold = guaranteed_receive_window_size_ack_threshold
        if guaranteed_send_ack_timeout is not None:
            self.guaranteed_send_ack_timeout = guaranteed_send_ack_timeout
        if guaranteed_send_window_size is not None:
            self.guaranteed_send_window_size = guaranteed_send_window_size
        if messaging_default_delivery_mode is not None:
            self.messaging_default_delivery_mode = messaging_default_delivery_mode
        if messaging_default_dmq_eligible_enabled is not None:
            self.messaging_default_dmq_eligible_enabled = messaging_default_dmq_eligible_enabled
        if messaging_default_eliding_eligible_enabled is not None:
            self.messaging_default_eliding_eligible_enabled = messaging_default_eliding_eligible_enabled
        if messaging_jmsx_user_id_enabled is not None:
            self.messaging_jmsx_user_id_enabled = messaging_jmsx_user_id_enabled
        if messaging_text_in_xml_payload_enabled is not None:
            self.messaging_text_in_xml_payload_enabled = messaging_text_in_xml_payload_enabled
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if transport_compression_level is not None:
            self.transport_compression_level = transport_compression_level
        if transport_connect_retry_count is not None:
            self.transport_connect_retry_count = transport_connect_retry_count
        if transport_connect_retry_per_host_count is not None:
            self.transport_connect_retry_per_host_count = transport_connect_retry_per_host_count
        if transport_connect_timeout is not None:
            self.transport_connect_timeout = transport_connect_timeout
        if transport_direct_transport_enabled is not None:
            self.transport_direct_transport_enabled = transport_direct_transport_enabled
        if transport_keepalive_count is not None:
            self.transport_keepalive_count = transport_keepalive_count
        if transport_keepalive_enabled is not None:
            self.transport_keepalive_enabled = transport_keepalive_enabled
        if transport_keepalive_interval is not None:
            self.transport_keepalive_interval = transport_keepalive_interval
        if transport_msg_callback_on_io_thread_enabled is not None:
            self.transport_msg_callback_on_io_thread_enabled = transport_msg_callback_on_io_thread_enabled
        if transport_optimize_direct_enabled is not None:
            self.transport_optimize_direct_enabled = transport_optimize_direct_enabled
        if transport_port is not None:
            self.transport_port = transport_port
        if transport_read_timeout is not None:
            self.transport_read_timeout = transport_read_timeout
        if transport_receive_buffer_size is not None:
            self.transport_receive_buffer_size = transport_receive_buffer_size
        if transport_reconnect_retry_count is not None:
            self.transport_reconnect_retry_count = transport_reconnect_retry_count
        if transport_reconnect_retry_wait is not None:
            self.transport_reconnect_retry_wait = transport_reconnect_retry_wait
        if transport_send_buffer_size is not None:
            self.transport_send_buffer_size = transport_send_buffer_size
        if transport_tcp_no_delay_enabled is not None:
            self.transport_tcp_no_delay_enabled = transport_tcp_no_delay_enabled
        if xa_enabled is not None:
            self.xa_enabled = xa_enabled

    @property
    def allow_duplicate_client_id_enabled(self):
        """Gets the allow_duplicate_client_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable whether new JMS connections can use the same Client identifier (ID) as an existing connection. The default value is `false`. Available since 2.3.  # noqa: E501

        :return: The allow_duplicate_client_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._allow_duplicate_client_id_enabled

    @allow_duplicate_client_id_enabled.setter
    def allow_duplicate_client_id_enabled(self, allow_duplicate_client_id_enabled):
        """Sets the allow_duplicate_client_id_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable whether new JMS connections can use the same Client identifier (ID) as an existing connection. The default value is `false`. Available since 2.3.  # noqa: E501

        :param allow_duplicate_client_id_enabled: The allow_duplicate_client_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._allow_duplicate_client_id_enabled = allow_duplicate_client_id_enabled

    @property
    def client_description(self):
        """Gets the client_description of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The description of the Client. The default value is `\"\"`.  # noqa: E501

        :return: The client_description of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: str
        """
        return self._client_description

    @client_description.setter
    def client_description(self, client_description):
        """Sets the client_description of this MsgVpnJndiConnectionFactory.

        The description of the Client. The default value is `\"\"`.  # noqa: E501

        :param client_description: The client_description of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: str
        """

        self._client_description = client_description

    @property
    def client_id(self):
        """Gets the client_id of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The Client identifier (ID). If not specified, a unique value for it will be generated. The default value is `\"\"`.  # noqa: E501

        :return: The client_id of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this MsgVpnJndiConnectionFactory.

        The Client identifier (ID). If not specified, a unique value for it will be generated. The default value is `\"\"`.  # noqa: E501

        :param client_id: The client_id of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: str
        """

        self._client_id = client_id

    @property
    def connection_factory_name(self):
        """Gets the connection_factory_name of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The name of the JMS Connection Factory.  # noqa: E501

        :return: The connection_factory_name of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: str
        """
        return self._connection_factory_name

    @connection_factory_name.setter
    def connection_factory_name(self, connection_factory_name):
        """Sets the connection_factory_name of this MsgVpnJndiConnectionFactory.

        The name of the JMS Connection Factory.  # noqa: E501

        :param connection_factory_name: The connection_factory_name of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: str
        """

        self._connection_factory_name = connection_factory_name

    @property
    def dto_receive_override_enabled(self):
        """Gets the dto_receive_override_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable overriding by the Subscriber (Consumer) of the deliver-to-one (DTO) property on messages. When enabled, the Subscriber can receive all DTO tagged messages. The default value is `true`.  # noqa: E501

        :return: The dto_receive_override_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._dto_receive_override_enabled

    @dto_receive_override_enabled.setter
    def dto_receive_override_enabled(self, dto_receive_override_enabled):
        """Sets the dto_receive_override_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable overriding by the Subscriber (Consumer) of the deliver-to-one (DTO) property on messages. When enabled, the Subscriber can receive all DTO tagged messages. The default value is `true`.  # noqa: E501

        :param dto_receive_override_enabled: The dto_receive_override_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._dto_receive_override_enabled = dto_receive_override_enabled

    @property
    def dto_receive_subscriber_local_priority(self):
        """Gets the dto_receive_subscriber_local_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The priority for receiving deliver-to-one (DTO) messages by the Subscriber (Consumer) if the messages are published on the local broker that the Subscriber is directly connected to. The default value is `1`.  # noqa: E501

        :return: The dto_receive_subscriber_local_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._dto_receive_subscriber_local_priority

    @dto_receive_subscriber_local_priority.setter
    def dto_receive_subscriber_local_priority(self, dto_receive_subscriber_local_priority):
        """Sets the dto_receive_subscriber_local_priority of this MsgVpnJndiConnectionFactory.

        The priority for receiving deliver-to-one (DTO) messages by the Subscriber (Consumer) if the messages are published on the local broker that the Subscriber is directly connected to. The default value is `1`.  # noqa: E501

        :param dto_receive_subscriber_local_priority: The dto_receive_subscriber_local_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._dto_receive_subscriber_local_priority = dto_receive_subscriber_local_priority

    @property
    def dto_receive_subscriber_network_priority(self):
        """Gets the dto_receive_subscriber_network_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The priority for receiving deliver-to-one (DTO) messages by the Subscriber (Consumer) if the messages are published on a remote broker. The default value is `1`.  # noqa: E501

        :return: The dto_receive_subscriber_network_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._dto_receive_subscriber_network_priority

    @dto_receive_subscriber_network_priority.setter
    def dto_receive_subscriber_network_priority(self, dto_receive_subscriber_network_priority):
        """Sets the dto_receive_subscriber_network_priority of this MsgVpnJndiConnectionFactory.

        The priority for receiving deliver-to-one (DTO) messages by the Subscriber (Consumer) if the messages are published on a remote broker. The default value is `1`.  # noqa: E501

        :param dto_receive_subscriber_network_priority: The dto_receive_subscriber_network_priority of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._dto_receive_subscriber_network_priority = dto_receive_subscriber_network_priority

    @property
    def dto_send_enabled(self):
        """Gets the dto_send_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable the deliver-to-one (DTO) property on messages sent by the Publisher (Producer). The default value is `false`.  # noqa: E501

        :return: The dto_send_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._dto_send_enabled

    @dto_send_enabled.setter
    def dto_send_enabled(self, dto_send_enabled):
        """Sets the dto_send_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable the deliver-to-one (DTO) property on messages sent by the Publisher (Producer). The default value is `false`.  # noqa: E501

        :param dto_send_enabled: The dto_send_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._dto_send_enabled = dto_send_enabled

    @property
    def dynamic_endpoint_create_durable_enabled(self):
        """Gets the dynamic_endpoint_create_durable_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable whether a durable endpoint will be dynamically created on the broker when the client calls \"Session.createDurableSubscriber()\" or \"Session.createQueue()\". The created endpoint respects the message time-to-live (TTL) according to the \"dynamicEndpointRespectTtlEnabled\" property. The default value is `false`.  # noqa: E501

        :return: The dynamic_endpoint_create_durable_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._dynamic_endpoint_create_durable_enabled

    @dynamic_endpoint_create_durable_enabled.setter
    def dynamic_endpoint_create_durable_enabled(self, dynamic_endpoint_create_durable_enabled):
        """Sets the dynamic_endpoint_create_durable_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable whether a durable endpoint will be dynamically created on the broker when the client calls \"Session.createDurableSubscriber()\" or \"Session.createQueue()\". The created endpoint respects the message time-to-live (TTL) according to the \"dynamicEndpointRespectTtlEnabled\" property. The default value is `false`.  # noqa: E501

        :param dynamic_endpoint_create_durable_enabled: The dynamic_endpoint_create_durable_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._dynamic_endpoint_create_durable_enabled = dynamic_endpoint_create_durable_enabled

    @property
    def dynamic_endpoint_respect_ttl_enabled(self):
        """Gets the dynamic_endpoint_respect_ttl_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable whether dynamically created durable and non-durable endpoints respect the message time-to-live (TTL) property. The default value is `true`.  # noqa: E501

        :return: The dynamic_endpoint_respect_ttl_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._dynamic_endpoint_respect_ttl_enabled

    @dynamic_endpoint_respect_ttl_enabled.setter
    def dynamic_endpoint_respect_ttl_enabled(self, dynamic_endpoint_respect_ttl_enabled):
        """Sets the dynamic_endpoint_respect_ttl_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable whether dynamically created durable and non-durable endpoints respect the message time-to-live (TTL) property. The default value is `true`.  # noqa: E501

        :param dynamic_endpoint_respect_ttl_enabled: The dynamic_endpoint_respect_ttl_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._dynamic_endpoint_respect_ttl_enabled = dynamic_endpoint_respect_ttl_enabled

    @property
    def guaranteed_receive_ack_timeout(self):
        """Gets the guaranteed_receive_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The timeout for sending the acknowledgement (ACK) for guaranteed messages received by the Subscriber (Consumer), in milliseconds. The default value is `1000`.  # noqa: E501

        :return: The guaranteed_receive_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_receive_ack_timeout

    @guaranteed_receive_ack_timeout.setter
    def guaranteed_receive_ack_timeout(self, guaranteed_receive_ack_timeout):
        """Sets the guaranteed_receive_ack_timeout of this MsgVpnJndiConnectionFactory.

        The timeout for sending the acknowledgement (ACK) for guaranteed messages received by the Subscriber (Consumer), in milliseconds. The default value is `1000`.  # noqa: E501

        :param guaranteed_receive_ack_timeout: The guaranteed_receive_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._guaranteed_receive_ack_timeout = guaranteed_receive_ack_timeout

    @property
    def guaranteed_receive_window_size(self):
        """Gets the guaranteed_receive_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The size of the window for guaranteed messages received by the Subscriber (Consumer), in messages. The default value is `18`.  # noqa: E501

        :return: The guaranteed_receive_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_receive_window_size

    @guaranteed_receive_window_size.setter
    def guaranteed_receive_window_size(self, guaranteed_receive_window_size):
        """Sets the guaranteed_receive_window_size of this MsgVpnJndiConnectionFactory.

        The size of the window for guaranteed messages received by the Subscriber (Consumer), in messages. The default value is `18`.  # noqa: E501

        :param guaranteed_receive_window_size: The guaranteed_receive_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._guaranteed_receive_window_size = guaranteed_receive_window_size

    @property
    def guaranteed_receive_window_size_ack_threshold(self):
        """Gets the guaranteed_receive_window_size_ack_threshold of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The threshold for sending the acknowledgement (ACK) for guaranteed messages received by the Subscriber (Consumer) as a percentage of `guaranteedReceiveWindowSize`. The default value is `60`.  # noqa: E501

        :return: The guaranteed_receive_window_size_ack_threshold of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_receive_window_size_ack_threshold

    @guaranteed_receive_window_size_ack_threshold.setter
    def guaranteed_receive_window_size_ack_threshold(self, guaranteed_receive_window_size_ack_threshold):
        """Sets the guaranteed_receive_window_size_ack_threshold of this MsgVpnJndiConnectionFactory.

        The threshold for sending the acknowledgement (ACK) for guaranteed messages received by the Subscriber (Consumer) as a percentage of `guaranteedReceiveWindowSize`. The default value is `60`.  # noqa: E501

        :param guaranteed_receive_window_size_ack_threshold: The guaranteed_receive_window_size_ack_threshold of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._guaranteed_receive_window_size_ack_threshold = guaranteed_receive_window_size_ack_threshold

    @property
    def guaranteed_send_ack_timeout(self):
        """Gets the guaranteed_send_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The timeout for receiving the acknowledgement (ACK) for guaranteed messages sent by the Publisher (Producer), in milliseconds. The default value is `2000`.  # noqa: E501

        :return: The guaranteed_send_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_send_ack_timeout

    @guaranteed_send_ack_timeout.setter
    def guaranteed_send_ack_timeout(self, guaranteed_send_ack_timeout):
        """Sets the guaranteed_send_ack_timeout of this MsgVpnJndiConnectionFactory.

        The timeout for receiving the acknowledgement (ACK) for guaranteed messages sent by the Publisher (Producer), in milliseconds. The default value is `2000`.  # noqa: E501

        :param guaranteed_send_ack_timeout: The guaranteed_send_ack_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._guaranteed_send_ack_timeout = guaranteed_send_ack_timeout

    @property
    def guaranteed_send_window_size(self):
        """Gets the guaranteed_send_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The size of the window for non-persistent guaranteed messages sent by the Publisher (Producer), in messages. For persistent messages the window size is fixed at 1. The default value is `255`.  # noqa: E501

        :return: The guaranteed_send_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_send_window_size

    @guaranteed_send_window_size.setter
    def guaranteed_send_window_size(self, guaranteed_send_window_size):
        """Sets the guaranteed_send_window_size of this MsgVpnJndiConnectionFactory.

        The size of the window for non-persistent guaranteed messages sent by the Publisher (Producer), in messages. For persistent messages the window size is fixed at 1. The default value is `255`.  # noqa: E501

        :param guaranteed_send_window_size: The guaranteed_send_window_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._guaranteed_send_window_size = guaranteed_send_window_size

    @property
    def messaging_default_delivery_mode(self):
        """Gets the messaging_default_delivery_mode of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The default delivery mode for messages sent by the Publisher (Producer). The default value is `\"persistent\"`. The allowed values and their meaning are:  <pre> \"persistent\" - The broker spools messages (persists in the Message Spool) as part of the send operation. \"non-persistent\" - The broker does not spool messages (does not persist in the Message Spool) as part of the send operation. </pre>   # noqa: E501

        :return: The messaging_default_delivery_mode of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: str
        """
        return self._messaging_default_delivery_mode

    @messaging_default_delivery_mode.setter
    def messaging_default_delivery_mode(self, messaging_default_delivery_mode):
        """Sets the messaging_default_delivery_mode of this MsgVpnJndiConnectionFactory.

        The default delivery mode for messages sent by the Publisher (Producer). The default value is `\"persistent\"`. The allowed values and their meaning are:  <pre> \"persistent\" - The broker spools messages (persists in the Message Spool) as part of the send operation. \"non-persistent\" - The broker does not spool messages (does not persist in the Message Spool) as part of the send operation. </pre>   # noqa: E501

        :param messaging_default_delivery_mode: The messaging_default_delivery_mode of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: str
        """
        allowed_values = ["persistent", "non-persistent"]  # noqa: E501
        if messaging_default_delivery_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `messaging_default_delivery_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(messaging_default_delivery_mode, allowed_values)
            )

        self._messaging_default_delivery_mode = messaging_default_delivery_mode

    @property
    def messaging_default_dmq_eligible_enabled(self):
        """Gets the messaging_default_dmq_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable whether messages sent by the Publisher (Producer) are Dead Message Queue (DMQ) eligible by default. The default value is `false`.  # noqa: E501

        :return: The messaging_default_dmq_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._messaging_default_dmq_eligible_enabled

    @messaging_default_dmq_eligible_enabled.setter
    def messaging_default_dmq_eligible_enabled(self, messaging_default_dmq_eligible_enabled):
        """Sets the messaging_default_dmq_eligible_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable whether messages sent by the Publisher (Producer) are Dead Message Queue (DMQ) eligible by default. The default value is `false`.  # noqa: E501

        :param messaging_default_dmq_eligible_enabled: The messaging_default_dmq_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._messaging_default_dmq_eligible_enabled = messaging_default_dmq_eligible_enabled

    @property
    def messaging_default_eliding_eligible_enabled(self):
        """Gets the messaging_default_eliding_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable whether messages sent by the Publisher (Producer) are Eliding eligible by default. The default value is `false`.  # noqa: E501

        :return: The messaging_default_eliding_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._messaging_default_eliding_eligible_enabled

    @messaging_default_eliding_eligible_enabled.setter
    def messaging_default_eliding_eligible_enabled(self, messaging_default_eliding_eligible_enabled):
        """Sets the messaging_default_eliding_eligible_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable whether messages sent by the Publisher (Producer) are Eliding eligible by default. The default value is `false`.  # noqa: E501

        :param messaging_default_eliding_eligible_enabled: The messaging_default_eliding_eligible_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._messaging_default_eliding_eligible_enabled = messaging_default_eliding_eligible_enabled

    @property
    def messaging_jmsx_user_id_enabled(self):
        """Gets the messaging_jmsx_user_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable inclusion (adding or replacing) of the JMSXUserID property in messages sent by the Publisher (Producer). The default value is `false`.  # noqa: E501

        :return: The messaging_jmsx_user_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._messaging_jmsx_user_id_enabled

    @messaging_jmsx_user_id_enabled.setter
    def messaging_jmsx_user_id_enabled(self, messaging_jmsx_user_id_enabled):
        """Sets the messaging_jmsx_user_id_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable inclusion (adding or replacing) of the JMSXUserID property in messages sent by the Publisher (Producer). The default value is `false`.  # noqa: E501

        :param messaging_jmsx_user_id_enabled: The messaging_jmsx_user_id_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._messaging_jmsx_user_id_enabled = messaging_jmsx_user_id_enabled

    @property
    def messaging_text_in_xml_payload_enabled(self):
        """Gets the messaging_text_in_xml_payload_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable encoding of JMS text messages in Publisher (Producer) messages as XML payload. When disabled, JMS text messages are encoded as a binary attachment. The default value is `true`.  # noqa: E501

        :return: The messaging_text_in_xml_payload_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._messaging_text_in_xml_payload_enabled

    @messaging_text_in_xml_payload_enabled.setter
    def messaging_text_in_xml_payload_enabled(self, messaging_text_in_xml_payload_enabled):
        """Sets the messaging_text_in_xml_payload_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable encoding of JMS text messages in Publisher (Producer) messages as XML payload. When disabled, JMS text messages are encoded as a binary attachment. The default value is `true`.  # noqa: E501

        :param messaging_text_in_xml_payload_enabled: The messaging_text_in_xml_payload_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._messaging_text_in_xml_payload_enabled = messaging_text_in_xml_payload_enabled

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnJndiConnectionFactory.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def transport_compression_level(self):
        """Gets the transport_compression_level of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The ZLIB compression level for the connection to the broker. The value \"0\" means no compression, and the value \"-1\" means the compression level is specified in the JNDI Properties file. The default value is `-1`.  # noqa: E501

        :return: The transport_compression_level of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_compression_level

    @transport_compression_level.setter
    def transport_compression_level(self, transport_compression_level):
        """Sets the transport_compression_level of this MsgVpnJndiConnectionFactory.

        The ZLIB compression level for the connection to the broker. The value \"0\" means no compression, and the value \"-1\" means the compression level is specified in the JNDI Properties file. The default value is `-1`.  # noqa: E501

        :param transport_compression_level: The transport_compression_level of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_compression_level = transport_compression_level

    @property
    def transport_connect_retry_count(self):
        """Gets the transport_connect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The maximum number of retry attempts to establish an initial connection to the host or list of hosts. The value \"0\" means a single attempt (no retries), and the value \"-1\" means to retry forever. The default value is `0`.  # noqa: E501

        :return: The transport_connect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_connect_retry_count

    @transport_connect_retry_count.setter
    def transport_connect_retry_count(self, transport_connect_retry_count):
        """Sets the transport_connect_retry_count of this MsgVpnJndiConnectionFactory.

        The maximum number of retry attempts to establish an initial connection to the host or list of hosts. The value \"0\" means a single attempt (no retries), and the value \"-1\" means to retry forever. The default value is `0`.  # noqa: E501

        :param transport_connect_retry_count: The transport_connect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_connect_retry_count = transport_connect_retry_count

    @property
    def transport_connect_retry_per_host_count(self):
        """Gets the transport_connect_retry_per_host_count of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The maximum number of retry attempts to establish an initial connection to each host on the list of hosts. The value \"0\" means a single attempt (no retries), and the value \"-1\" means to retry forever. The default value is `0`.  # noqa: E501

        :return: The transport_connect_retry_per_host_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_connect_retry_per_host_count

    @transport_connect_retry_per_host_count.setter
    def transport_connect_retry_per_host_count(self, transport_connect_retry_per_host_count):
        """Sets the transport_connect_retry_per_host_count of this MsgVpnJndiConnectionFactory.

        The maximum number of retry attempts to establish an initial connection to each host on the list of hosts. The value \"0\" means a single attempt (no retries), and the value \"-1\" means to retry forever. The default value is `0`.  # noqa: E501

        :param transport_connect_retry_per_host_count: The transport_connect_retry_per_host_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_connect_retry_per_host_count = transport_connect_retry_per_host_count

    @property
    def transport_connect_timeout(self):
        """Gets the transport_connect_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The timeout for establishing an initial connection to the broker, in milliseconds. The default value is `30000`.  # noqa: E501

        :return: The transport_connect_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_connect_timeout

    @transport_connect_timeout.setter
    def transport_connect_timeout(self, transport_connect_timeout):
        """Sets the transport_connect_timeout of this MsgVpnJndiConnectionFactory.

        The timeout for establishing an initial connection to the broker, in milliseconds. The default value is `30000`.  # noqa: E501

        :param transport_connect_timeout: The transport_connect_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_connect_timeout = transport_connect_timeout

    @property
    def transport_direct_transport_enabled(self):
        """Gets the transport_direct_transport_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable usage of the Direct Transport mode for sending non-persistent messages. When disabled, the Guaranteed Transport mode is used. The default value is `true`.  # noqa: E501

        :return: The transport_direct_transport_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._transport_direct_transport_enabled

    @transport_direct_transport_enabled.setter
    def transport_direct_transport_enabled(self, transport_direct_transport_enabled):
        """Sets the transport_direct_transport_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable usage of the Direct Transport mode for sending non-persistent messages. When disabled, the Guaranteed Transport mode is used. The default value is `true`.  # noqa: E501

        :param transport_direct_transport_enabled: The transport_direct_transport_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._transport_direct_transport_enabled = transport_direct_transport_enabled

    @property
    def transport_keepalive_count(self):
        """Gets the transport_keepalive_count of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The maximum number of consecutive application-level keepalive messages sent without the broker response before the connection to the broker is closed. The default value is `3`.  # noqa: E501

        :return: The transport_keepalive_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_keepalive_count

    @transport_keepalive_count.setter
    def transport_keepalive_count(self, transport_keepalive_count):
        """Sets the transport_keepalive_count of this MsgVpnJndiConnectionFactory.

        The maximum number of consecutive application-level keepalive messages sent without the broker response before the connection to the broker is closed. The default value is `3`.  # noqa: E501

        :param transport_keepalive_count: The transport_keepalive_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_keepalive_count = transport_keepalive_count

    @property
    def transport_keepalive_enabled(self):
        """Gets the transport_keepalive_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable usage of application-level keepalive messages to maintain a connection with the broker. The default value is `true`.  # noqa: E501

        :return: The transport_keepalive_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._transport_keepalive_enabled

    @transport_keepalive_enabled.setter
    def transport_keepalive_enabled(self, transport_keepalive_enabled):
        """Sets the transport_keepalive_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable usage of application-level keepalive messages to maintain a connection with the broker. The default value is `true`.  # noqa: E501

        :param transport_keepalive_enabled: The transport_keepalive_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._transport_keepalive_enabled = transport_keepalive_enabled

    @property
    def transport_keepalive_interval(self):
        """Gets the transport_keepalive_interval of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The interval between application-level keepalive messages, in milliseconds. The default value is `3000`.  # noqa: E501

        :return: The transport_keepalive_interval of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_keepalive_interval

    @transport_keepalive_interval.setter
    def transport_keepalive_interval(self, transport_keepalive_interval):
        """Sets the transport_keepalive_interval of this MsgVpnJndiConnectionFactory.

        The interval between application-level keepalive messages, in milliseconds. The default value is `3000`.  # noqa: E501

        :param transport_keepalive_interval: The transport_keepalive_interval of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_keepalive_interval = transport_keepalive_interval

    @property
    def transport_msg_callback_on_io_thread_enabled(self):
        """Gets the transport_msg_callback_on_io_thread_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable delivery of asynchronous messages directly from the I/O thread. Contact Solace Support before enabling this property. The default value is `false`.  # noqa: E501

        :return: The transport_msg_callback_on_io_thread_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._transport_msg_callback_on_io_thread_enabled

    @transport_msg_callback_on_io_thread_enabled.setter
    def transport_msg_callback_on_io_thread_enabled(self, transport_msg_callback_on_io_thread_enabled):
        """Sets the transport_msg_callback_on_io_thread_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable delivery of asynchronous messages directly from the I/O thread. Contact Solace Support before enabling this property. The default value is `false`.  # noqa: E501

        :param transport_msg_callback_on_io_thread_enabled: The transport_msg_callback_on_io_thread_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._transport_msg_callback_on_io_thread_enabled = transport_msg_callback_on_io_thread_enabled

    @property
    def transport_optimize_direct_enabled(self):
        """Gets the transport_optimize_direct_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable optimization for the Direct Transport delivery mode. If enabled, the client application is limited to one Publisher (Producer) and one non-durable Subscriber (Consumer). The default value is `false`.  # noqa: E501

        :return: The transport_optimize_direct_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._transport_optimize_direct_enabled

    @transport_optimize_direct_enabled.setter
    def transport_optimize_direct_enabled(self, transport_optimize_direct_enabled):
        """Sets the transport_optimize_direct_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable optimization for the Direct Transport delivery mode. If enabled, the client application is limited to one Publisher (Producer) and one non-durable Subscriber (Consumer). The default value is `false`.  # noqa: E501

        :param transport_optimize_direct_enabled: The transport_optimize_direct_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._transport_optimize_direct_enabled = transport_optimize_direct_enabled

    @property
    def transport_port(self):
        """Gets the transport_port of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The connection port number on the broker for SMF clients. The value \"-1\" means the port is specified in the JNDI Properties file. The default value is `-1`.  # noqa: E501

        :return: The transport_port of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_port

    @transport_port.setter
    def transport_port(self, transport_port):
        """Sets the transport_port of this MsgVpnJndiConnectionFactory.

        The connection port number on the broker for SMF clients. The value \"-1\" means the port is specified in the JNDI Properties file. The default value is `-1`.  # noqa: E501

        :param transport_port: The transport_port of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_port = transport_port

    @property
    def transport_read_timeout(self):
        """Gets the transport_read_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The timeout for reading a reply from the broker, in milliseconds. The default value is `10000`.  # noqa: E501

        :return: The transport_read_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_read_timeout

    @transport_read_timeout.setter
    def transport_read_timeout(self, transport_read_timeout):
        """Sets the transport_read_timeout of this MsgVpnJndiConnectionFactory.

        The timeout for reading a reply from the broker, in milliseconds. The default value is `10000`.  # noqa: E501

        :param transport_read_timeout: The transport_read_timeout of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_read_timeout = transport_read_timeout

    @property
    def transport_receive_buffer_size(self):
        """Gets the transport_receive_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The size of the receive socket buffer, in bytes. It corresponds to the SO_RCVBUF socket option. The default value is `65536`.  # noqa: E501

        :return: The transport_receive_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_receive_buffer_size

    @transport_receive_buffer_size.setter
    def transport_receive_buffer_size(self, transport_receive_buffer_size):
        """Sets the transport_receive_buffer_size of this MsgVpnJndiConnectionFactory.

        The size of the receive socket buffer, in bytes. It corresponds to the SO_RCVBUF socket option. The default value is `65536`.  # noqa: E501

        :param transport_receive_buffer_size: The transport_receive_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_receive_buffer_size = transport_receive_buffer_size

    @property
    def transport_reconnect_retry_count(self):
        """Gets the transport_reconnect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The maximum number of attempts to reconnect to the host or list of hosts after the connection has been lost. The value \"-1\" means to retry forever. The default value is `3`.  # noqa: E501

        :return: The transport_reconnect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_reconnect_retry_count

    @transport_reconnect_retry_count.setter
    def transport_reconnect_retry_count(self, transport_reconnect_retry_count):
        """Sets the transport_reconnect_retry_count of this MsgVpnJndiConnectionFactory.

        The maximum number of attempts to reconnect to the host or list of hosts after the connection has been lost. The value \"-1\" means to retry forever. The default value is `3`.  # noqa: E501

        :param transport_reconnect_retry_count: The transport_reconnect_retry_count of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_reconnect_retry_count = transport_reconnect_retry_count

    @property
    def transport_reconnect_retry_wait(self):
        """Gets the transport_reconnect_retry_wait of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The amount of time before making another attempt to connect or reconnect to the host after the connection has been lost, in milliseconds. The default value is `3000`.  # noqa: E501

        :return: The transport_reconnect_retry_wait of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_reconnect_retry_wait

    @transport_reconnect_retry_wait.setter
    def transport_reconnect_retry_wait(self, transport_reconnect_retry_wait):
        """Sets the transport_reconnect_retry_wait of this MsgVpnJndiConnectionFactory.

        The amount of time before making another attempt to connect or reconnect to the host after the connection has been lost, in milliseconds. The default value is `3000`.  # noqa: E501

        :param transport_reconnect_retry_wait: The transport_reconnect_retry_wait of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_reconnect_retry_wait = transport_reconnect_retry_wait

    @property
    def transport_send_buffer_size(self):
        """Gets the transport_send_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501

        The size of the send socket buffer, in bytes. It corresponds to the SO_SNDBUF socket option. The default value is `65536`.  # noqa: E501

        :return: The transport_send_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: int
        """
        return self._transport_send_buffer_size

    @transport_send_buffer_size.setter
    def transport_send_buffer_size(self, transport_send_buffer_size):
        """Sets the transport_send_buffer_size of this MsgVpnJndiConnectionFactory.

        The size of the send socket buffer, in bytes. It corresponds to the SO_SNDBUF socket option. The default value is `65536`.  # noqa: E501

        :param transport_send_buffer_size: The transport_send_buffer_size of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: int
        """

        self._transport_send_buffer_size = transport_send_buffer_size

    @property
    def transport_tcp_no_delay_enabled(self):
        """Gets the transport_tcp_no_delay_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable the TCP_NODELAY option. When enabled, Nagle's algorithm for TCP/IP congestion control (RFC 896) is disabled. The default value is `true`.  # noqa: E501

        :return: The transport_tcp_no_delay_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._transport_tcp_no_delay_enabled

    @transport_tcp_no_delay_enabled.setter
    def transport_tcp_no_delay_enabled(self, transport_tcp_no_delay_enabled):
        """Sets the transport_tcp_no_delay_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable the TCP_NODELAY option. When enabled, Nagle's algorithm for TCP/IP congestion control (RFC 896) is disabled. The default value is `true`.  # noqa: E501

        :param transport_tcp_no_delay_enabled: The transport_tcp_no_delay_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._transport_tcp_no_delay_enabled = transport_tcp_no_delay_enabled

    @property
    def xa_enabled(self):
        """Gets the xa_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501

        Enable or disable this as an XA Connection Factory. When enabled, the Connection Factory can be cast to \"XAConnectionFactory\", \"XAQueueConnectionFactory\" or \"XATopicConnectionFactory\". The default value is `false`.  # noqa: E501

        :return: The xa_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :rtype: bool
        """
        return self._xa_enabled

    @xa_enabled.setter
    def xa_enabled(self, xa_enabled):
        """Sets the xa_enabled of this MsgVpnJndiConnectionFactory.

        Enable or disable this as an XA Connection Factory. When enabled, the Connection Factory can be cast to \"XAConnectionFactory\", \"XAQueueConnectionFactory\" or \"XATopicConnectionFactory\". The default value is `false`.  # noqa: E501

        :param xa_enabled: The xa_enabled of this MsgVpnJndiConnectionFactory.  # noqa: E501
        :type: bool
        """

        self._xa_enabled = xa_enabled

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
        if issubclass(MsgVpnJndiConnectionFactory, dict):
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
        if not isinstance(other, MsgVpnJndiConnectionFactory):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
