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


class MsgVpnBridge(object):
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
        'bound_to_queue': 'bool',
        'bridge_name': 'str',
        'bridge_virtual_router': 'str',
        'client_name': 'str',
        'compressed': 'bool',
        'counter': 'MsgVpnBridgeCounter',
        'enabled': 'bool',
        'encrypted': 'bool',
        'establisher': 'str',
        'inbound_failure_reason': 'str',
        'inbound_state': 'str',
        'last_tx_msg_id': 'int',
        'local_interface': 'str',
        'local_queue_name': 'str',
        'max_ttl': 'int',
        'msg_vpn_name': 'str',
        'outbound_state': 'str',
        'rate': 'MsgVpnBridgeRate',
        'remote_address': 'str',
        'remote_authentication_basic_client_username': 'str',
        'remote_authentication_scheme': 'str',
        'remote_connection_retry_count': 'int',
        'remote_connection_retry_delay': 'int',
        'remote_deliver_to_one_priority': 'str',
        'remote_msg_vpn_name': 'str',
        'remote_router_name': 'str',
        'remote_tx_flow_id': 'int',
        'tls_cipher_suite_list': 'str',
        'tls_default_cipher_suite_list': 'bool',
        'ttl_exceeded_event_raised': 'bool',
        'uptime': 'int'
    }

    attribute_map = {
        'bound_to_queue': 'boundToQueue',
        'bridge_name': 'bridgeName',
        'bridge_virtual_router': 'bridgeVirtualRouter',
        'client_name': 'clientName',
        'compressed': 'compressed',
        'counter': 'counter',
        'enabled': 'enabled',
        'encrypted': 'encrypted',
        'establisher': 'establisher',
        'inbound_failure_reason': 'inboundFailureReason',
        'inbound_state': 'inboundState',
        'last_tx_msg_id': 'lastTxMsgId',
        'local_interface': 'localInterface',
        'local_queue_name': 'localQueueName',
        'max_ttl': 'maxTtl',
        'msg_vpn_name': 'msgVpnName',
        'outbound_state': 'outboundState',
        'rate': 'rate',
        'remote_address': 'remoteAddress',
        'remote_authentication_basic_client_username': 'remoteAuthenticationBasicClientUsername',
        'remote_authentication_scheme': 'remoteAuthenticationScheme',
        'remote_connection_retry_count': 'remoteConnectionRetryCount',
        'remote_connection_retry_delay': 'remoteConnectionRetryDelay',
        'remote_deliver_to_one_priority': 'remoteDeliverToOnePriority',
        'remote_msg_vpn_name': 'remoteMsgVpnName',
        'remote_router_name': 'remoteRouterName',
        'remote_tx_flow_id': 'remoteTxFlowId',
        'tls_cipher_suite_list': 'tlsCipherSuiteList',
        'tls_default_cipher_suite_list': 'tlsDefaultCipherSuiteList',
        'ttl_exceeded_event_raised': 'ttlExceededEventRaised',
        'uptime': 'uptime'
    }

    def __init__(self, bound_to_queue=None, bridge_name=None, bridge_virtual_router=None, client_name=None, compressed=None, counter=None, enabled=None, encrypted=None, establisher=None, inbound_failure_reason=None, inbound_state=None, last_tx_msg_id=None, local_interface=None, local_queue_name=None, max_ttl=None, msg_vpn_name=None, outbound_state=None, rate=None, remote_address=None, remote_authentication_basic_client_username=None, remote_authentication_scheme=None, remote_connection_retry_count=None, remote_connection_retry_delay=None, remote_deliver_to_one_priority=None, remote_msg_vpn_name=None, remote_router_name=None, remote_tx_flow_id=None, tls_cipher_suite_list=None, tls_default_cipher_suite_list=None, ttl_exceeded_event_raised=None, uptime=None):  # noqa: E501
        """MsgVpnBridge - a model defined in Swagger"""  # noqa: E501

        self._bound_to_queue = None
        self._bridge_name = None
        self._bridge_virtual_router = None
        self._client_name = None
        self._compressed = None
        self._counter = None
        self._enabled = None
        self._encrypted = None
        self._establisher = None
        self._inbound_failure_reason = None
        self._inbound_state = None
        self._last_tx_msg_id = None
        self._local_interface = None
        self._local_queue_name = None
        self._max_ttl = None
        self._msg_vpn_name = None
        self._outbound_state = None
        self._rate = None
        self._remote_address = None
        self._remote_authentication_basic_client_username = None
        self._remote_authentication_scheme = None
        self._remote_connection_retry_count = None
        self._remote_connection_retry_delay = None
        self._remote_deliver_to_one_priority = None
        self._remote_msg_vpn_name = None
        self._remote_router_name = None
        self._remote_tx_flow_id = None
        self._tls_cipher_suite_list = None
        self._tls_default_cipher_suite_list = None
        self._ttl_exceeded_event_raised = None
        self._uptime = None
        self.discriminator = None

        if bound_to_queue is not None:
            self.bound_to_queue = bound_to_queue
        if bridge_name is not None:
            self.bridge_name = bridge_name
        if bridge_virtual_router is not None:
            self.bridge_virtual_router = bridge_virtual_router
        if client_name is not None:
            self.client_name = client_name
        if compressed is not None:
            self.compressed = compressed
        if counter is not None:
            self.counter = counter
        if enabled is not None:
            self.enabled = enabled
        if encrypted is not None:
            self.encrypted = encrypted
        if establisher is not None:
            self.establisher = establisher
        if inbound_failure_reason is not None:
            self.inbound_failure_reason = inbound_failure_reason
        if inbound_state is not None:
            self.inbound_state = inbound_state
        if last_tx_msg_id is not None:
            self.last_tx_msg_id = last_tx_msg_id
        if local_interface is not None:
            self.local_interface = local_interface
        if local_queue_name is not None:
            self.local_queue_name = local_queue_name
        if max_ttl is not None:
            self.max_ttl = max_ttl
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if outbound_state is not None:
            self.outbound_state = outbound_state
        if rate is not None:
            self.rate = rate
        if remote_address is not None:
            self.remote_address = remote_address
        if remote_authentication_basic_client_username is not None:
            self.remote_authentication_basic_client_username = remote_authentication_basic_client_username
        if remote_authentication_scheme is not None:
            self.remote_authentication_scheme = remote_authentication_scheme
        if remote_connection_retry_count is not None:
            self.remote_connection_retry_count = remote_connection_retry_count
        if remote_connection_retry_delay is not None:
            self.remote_connection_retry_delay = remote_connection_retry_delay
        if remote_deliver_to_one_priority is not None:
            self.remote_deliver_to_one_priority = remote_deliver_to_one_priority
        if remote_msg_vpn_name is not None:
            self.remote_msg_vpn_name = remote_msg_vpn_name
        if remote_router_name is not None:
            self.remote_router_name = remote_router_name
        if remote_tx_flow_id is not None:
            self.remote_tx_flow_id = remote_tx_flow_id
        if tls_cipher_suite_list is not None:
            self.tls_cipher_suite_list = tls_cipher_suite_list
        if tls_default_cipher_suite_list is not None:
            self.tls_default_cipher_suite_list = tls_default_cipher_suite_list
        if ttl_exceeded_event_raised is not None:
            self.ttl_exceeded_event_raised = ttl_exceeded_event_raised
        if uptime is not None:
            self.uptime = uptime

    @property
    def bound_to_queue(self):
        """Gets the bound_to_queue of this MsgVpnBridge.  # noqa: E501

        Indicates whether the Bridge is bound to the queue in the remote Message VPN.  # noqa: E501

        :return: The bound_to_queue of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._bound_to_queue

    @bound_to_queue.setter
    def bound_to_queue(self, bound_to_queue):
        """Sets the bound_to_queue of this MsgVpnBridge.

        Indicates whether the Bridge is bound to the queue in the remote Message VPN.  # noqa: E501

        :param bound_to_queue: The bound_to_queue of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._bound_to_queue = bound_to_queue

    @property
    def bridge_name(self):
        """Gets the bridge_name of this MsgVpnBridge.  # noqa: E501

        The name of the Bridge.  # noqa: E501

        :return: The bridge_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._bridge_name

    @bridge_name.setter
    def bridge_name(self, bridge_name):
        """Sets the bridge_name of this MsgVpnBridge.

        The name of the Bridge.  # noqa: E501

        :param bridge_name: The bridge_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._bridge_name = bridge_name

    @property
    def bridge_virtual_router(self):
        """Gets the bridge_virtual_router of this MsgVpnBridge.  # noqa: E501

        The virtual router of the Bridge. The allowed values and their meaning are:  <pre> \"primary\" - The Bridge is used for the primary virtual router. \"backup\" - The Bridge is used for the backup virtual router. \"auto\" - The Bridge is automatically assigned a router. </pre>   # noqa: E501

        :return: The bridge_virtual_router of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._bridge_virtual_router

    @bridge_virtual_router.setter
    def bridge_virtual_router(self, bridge_virtual_router):
        """Sets the bridge_virtual_router of this MsgVpnBridge.

        The virtual router of the Bridge. The allowed values and their meaning are:  <pre> \"primary\" - The Bridge is used for the primary virtual router. \"backup\" - The Bridge is used for the backup virtual router. \"auto\" - The Bridge is automatically assigned a router. </pre>   # noqa: E501

        :param bridge_virtual_router: The bridge_virtual_router of this MsgVpnBridge.  # noqa: E501
        :type: str
        """
        allowed_values = ["primary", "backup", "auto"]  # noqa: E501
        if bridge_virtual_router not in allowed_values:
            raise ValueError(
                "Invalid value for `bridge_virtual_router` ({0}), must be one of {1}"  # noqa: E501
                .format(bridge_virtual_router, allowed_values)
            )

        self._bridge_virtual_router = bridge_virtual_router

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnBridge.  # noqa: E501

        The name of the Client for the Bridge.  # noqa: E501

        :return: The client_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnBridge.

        The name of the Client for the Bridge.  # noqa: E501

        :param client_name: The client_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def compressed(self):
        """Gets the compressed of this MsgVpnBridge.  # noqa: E501

        Indicates whether messages transmitted over the Bridge are compressed.  # noqa: E501

        :return: The compressed of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._compressed

    @compressed.setter
    def compressed(self, compressed):
        """Sets the compressed of this MsgVpnBridge.

        Indicates whether messages transmitted over the Bridge are compressed.  # noqa: E501

        :param compressed: The compressed of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._compressed = compressed

    @property
    def counter(self):
        """Gets the counter of this MsgVpnBridge.  # noqa: E501


        :return: The counter of this MsgVpnBridge.  # noqa: E501
        :rtype: MsgVpnBridgeCounter
        """
        return self._counter

    @counter.setter
    def counter(self, counter):
        """Sets the counter of this MsgVpnBridge.


        :param counter: The counter of this MsgVpnBridge.  # noqa: E501
        :type: MsgVpnBridgeCounter
        """

        self._counter = counter

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnBridge.  # noqa: E501

        Indicates whether the Bridge is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnBridge.

        Indicates whether the Bridge is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def encrypted(self):
        """Gets the encrypted of this MsgVpnBridge.  # noqa: E501

        Indicates whether messages transmitted over the Bridge are encrypted with TLS.  # noqa: E501

        :return: The encrypted of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._encrypted

    @encrypted.setter
    def encrypted(self, encrypted):
        """Sets the encrypted of this MsgVpnBridge.

        Indicates whether messages transmitted over the Bridge are encrypted with TLS.  # noqa: E501

        :param encrypted: The encrypted of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._encrypted = encrypted

    @property
    def establisher(self):
        """Gets the establisher of this MsgVpnBridge.  # noqa: E501

        The establisher of the Bridge connection. The allowed values and their meaning are:  <pre> \"local\" - The Bridge connection was established by the local Message VPN. \"remote\" - The Bridge connection was established by the remote Message VPN. </pre>   # noqa: E501

        :return: The establisher of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._establisher

    @establisher.setter
    def establisher(self, establisher):
        """Sets the establisher of this MsgVpnBridge.

        The establisher of the Bridge connection. The allowed values and their meaning are:  <pre> \"local\" - The Bridge connection was established by the local Message VPN. \"remote\" - The Bridge connection was established by the remote Message VPN. </pre>   # noqa: E501

        :param establisher: The establisher of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._establisher = establisher

    @property
    def inbound_failure_reason(self):
        """Gets the inbound_failure_reason of this MsgVpnBridge.  # noqa: E501

        The reason for the inbound connection failure from the Bridge.  # noqa: E501

        :return: The inbound_failure_reason of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._inbound_failure_reason

    @inbound_failure_reason.setter
    def inbound_failure_reason(self, inbound_failure_reason):
        """Sets the inbound_failure_reason of this MsgVpnBridge.

        The reason for the inbound connection failure from the Bridge.  # noqa: E501

        :param inbound_failure_reason: The inbound_failure_reason of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._inbound_failure_reason = inbound_failure_reason

    @property
    def inbound_state(self):
        """Gets the inbound_state of this MsgVpnBridge.  # noqa: E501

        The state of the inbound connection from the Bridge. The allowed values and their meaning are:  <pre> \"init\" - The connection is initializing. \"disabled\" - The connection is disabled by configuration. \"enabled\" - The connection is enabled by configuration. \"not-ready\" - The connection is operationally down. \"not-ready-wait-to-connect\" - The connection is down and waiting to connect. \"not-ready-connecting\" - The connection is trying to connect. \"not-ready-handshaking\" - The connection is handshaking. \"not-ready-wait-next\" - The connection failed to connect and is waiting to retry. \"not-ready-wait-reuse\" - The connection is closing in order to reuse an existing connection. \"not-ready-wait-cleanup\" - The connection is closed and cleaning up. \"ready\" - The connection is operationally up. \"ready-subscribing\" - The connection is up and synchronizing subscriptions. \"ready-in-sync\" - The connection is up and subscriptions are synchronized. </pre>   # noqa: E501

        :return: The inbound_state of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._inbound_state

    @inbound_state.setter
    def inbound_state(self, inbound_state):
        """Sets the inbound_state of this MsgVpnBridge.

        The state of the inbound connection from the Bridge. The allowed values and their meaning are:  <pre> \"init\" - The connection is initializing. \"disabled\" - The connection is disabled by configuration. \"enabled\" - The connection is enabled by configuration. \"not-ready\" - The connection is operationally down. \"not-ready-wait-to-connect\" - The connection is down and waiting to connect. \"not-ready-connecting\" - The connection is trying to connect. \"not-ready-handshaking\" - The connection is handshaking. \"not-ready-wait-next\" - The connection failed to connect and is waiting to retry. \"not-ready-wait-reuse\" - The connection is closing in order to reuse an existing connection. \"not-ready-wait-cleanup\" - The connection is closed and cleaning up. \"ready\" - The connection is operationally up. \"ready-subscribing\" - The connection is up and synchronizing subscriptions. \"ready-in-sync\" - The connection is up and subscriptions are synchronized. </pre>   # noqa: E501

        :param inbound_state: The inbound_state of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._inbound_state = inbound_state

    @property
    def last_tx_msg_id(self):
        """Gets the last_tx_msg_id of this MsgVpnBridge.  # noqa: E501

        The ID of the last message transmitted to the Bridge.  # noqa: E501

        :return: The last_tx_msg_id of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._last_tx_msg_id

    @last_tx_msg_id.setter
    def last_tx_msg_id(self, last_tx_msg_id):
        """Sets the last_tx_msg_id of this MsgVpnBridge.

        The ID of the last message transmitted to the Bridge.  # noqa: E501

        :param last_tx_msg_id: The last_tx_msg_id of this MsgVpnBridge.  # noqa: E501
        :type: int
        """

        self._last_tx_msg_id = last_tx_msg_id

    @property
    def local_interface(self):
        """Gets the local_interface of this MsgVpnBridge.  # noqa: E501

        The physical interface on the local Message VPN host for connecting to the remote Message VPN.  # noqa: E501

        :return: The local_interface of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._local_interface

    @local_interface.setter
    def local_interface(self, local_interface):
        """Sets the local_interface of this MsgVpnBridge.

        The physical interface on the local Message VPN host for connecting to the remote Message VPN.  # noqa: E501

        :param local_interface: The local_interface of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._local_interface = local_interface

    @property
    def local_queue_name(self):
        """Gets the local_queue_name of this MsgVpnBridge.  # noqa: E501

        The name of the local queue for the Bridge.  # noqa: E501

        :return: The local_queue_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._local_queue_name

    @local_queue_name.setter
    def local_queue_name(self, local_queue_name):
        """Sets the local_queue_name of this MsgVpnBridge.

        The name of the local queue for the Bridge.  # noqa: E501

        :param local_queue_name: The local_queue_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._local_queue_name = local_queue_name

    @property
    def max_ttl(self):
        """Gets the max_ttl of this MsgVpnBridge.  # noqa: E501

        The maximum time-to-live (TTL) in hops. Messages are discarded if their TTL exceeds this value.  # noqa: E501

        :return: The max_ttl of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._max_ttl

    @max_ttl.setter
    def max_ttl(self, max_ttl):
        """Sets the max_ttl of this MsgVpnBridge.

        The maximum time-to-live (TTL) in hops. Messages are discarded if their TTL exceeds this value.  # noqa: E501

        :param max_ttl: The max_ttl of this MsgVpnBridge.  # noqa: E501
        :type: int
        """

        self._max_ttl = max_ttl

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnBridge.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnBridge.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def outbound_state(self):
        """Gets the outbound_state of this MsgVpnBridge.  # noqa: E501

        The state of the outbound connection to the Bridge. The allowed values and their meaning are:  <pre> \"init\" - The connection is initializing. \"disabled\" - The connection is disabled by configuration. \"enabled\" - The connection is enabled by configuration. \"not-ready\" - The connection is operationally down. \"not-ready-wait-to-connect\" - The connection is down and waiting to connect. \"not-ready-connecting\" - The connection is trying to connect. \"not-ready-handshaking\" - The connection is handshaking. \"not-ready-wait-next\" - The connection failed to connect and is waiting to retry. \"not-ready-wait-reuse\" - The connection is closing in order to reuse an existing connection. \"not-ready-wait-cleanup\" - The connection is closed and cleaning up. \"ready\" - The connection is operationally up. \"ready-subscribing\" - The connection is up and synchronizing subscriptions. \"ready-in-sync\" - The connection is up and subscriptions are synchronized. </pre>   # noqa: E501

        :return: The outbound_state of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._outbound_state

    @outbound_state.setter
    def outbound_state(self, outbound_state):
        """Sets the outbound_state of this MsgVpnBridge.

        The state of the outbound connection to the Bridge. The allowed values and their meaning are:  <pre> \"init\" - The connection is initializing. \"disabled\" - The connection is disabled by configuration. \"enabled\" - The connection is enabled by configuration. \"not-ready\" - The connection is operationally down. \"not-ready-wait-to-connect\" - The connection is down and waiting to connect. \"not-ready-connecting\" - The connection is trying to connect. \"not-ready-handshaking\" - The connection is handshaking. \"not-ready-wait-next\" - The connection failed to connect and is waiting to retry. \"not-ready-wait-reuse\" - The connection is closing in order to reuse an existing connection. \"not-ready-wait-cleanup\" - The connection is closed and cleaning up. \"ready\" - The connection is operationally up. \"ready-subscribing\" - The connection is up and synchronizing subscriptions. \"ready-in-sync\" - The connection is up and subscriptions are synchronized. </pre>   # noqa: E501

        :param outbound_state: The outbound_state of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._outbound_state = outbound_state

    @property
    def rate(self):
        """Gets the rate of this MsgVpnBridge.  # noqa: E501


        :return: The rate of this MsgVpnBridge.  # noqa: E501
        :rtype: MsgVpnBridgeRate
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this MsgVpnBridge.


        :param rate: The rate of this MsgVpnBridge.  # noqa: E501
        :type: MsgVpnBridgeRate
        """

        self._rate = rate

    @property
    def remote_address(self):
        """Gets the remote_address of this MsgVpnBridge.  # noqa: E501

        The FQDN or IP address of the remote Message VPN.  # noqa: E501

        :return: The remote_address of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_address

    @remote_address.setter
    def remote_address(self, remote_address):
        """Sets the remote_address of this MsgVpnBridge.

        The FQDN or IP address of the remote Message VPN.  # noqa: E501

        :param remote_address: The remote_address of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._remote_address = remote_address

    @property
    def remote_authentication_basic_client_username(self):
        """Gets the remote_authentication_basic_client_username of this MsgVpnBridge.  # noqa: E501

        The Client Username the Bridge uses to login to the remote Message VPN.  # noqa: E501

        :return: The remote_authentication_basic_client_username of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_authentication_basic_client_username

    @remote_authentication_basic_client_username.setter
    def remote_authentication_basic_client_username(self, remote_authentication_basic_client_username):
        """Sets the remote_authentication_basic_client_username of this MsgVpnBridge.

        The Client Username the Bridge uses to login to the remote Message VPN.  # noqa: E501

        :param remote_authentication_basic_client_username: The remote_authentication_basic_client_username of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._remote_authentication_basic_client_username = remote_authentication_basic_client_username

    @property
    def remote_authentication_scheme(self):
        """Gets the remote_authentication_scheme of this MsgVpnBridge.  # noqa: E501

        The authentication scheme for the remote Message VPN. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>   # noqa: E501

        :return: The remote_authentication_scheme of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_authentication_scheme

    @remote_authentication_scheme.setter
    def remote_authentication_scheme(self, remote_authentication_scheme):
        """Sets the remote_authentication_scheme of this MsgVpnBridge.

        The authentication scheme for the remote Message VPN. The allowed values and their meaning are:  <pre> \"basic\" - Basic Authentication Scheme (via username and password). \"client-certificate\" - Client Certificate Authentication Scheme (via certificate file or content). </pre>   # noqa: E501

        :param remote_authentication_scheme: The remote_authentication_scheme of this MsgVpnBridge.  # noqa: E501
        :type: str
        """
        allowed_values = ["basic", "client-certificate"]  # noqa: E501
        if remote_authentication_scheme not in allowed_values:
            raise ValueError(
                "Invalid value for `remote_authentication_scheme` ({0}), must be one of {1}"  # noqa: E501
                .format(remote_authentication_scheme, allowed_values)
            )

        self._remote_authentication_scheme = remote_authentication_scheme

    @property
    def remote_connection_retry_count(self):
        """Gets the remote_connection_retry_count of this MsgVpnBridge.  # noqa: E501

        The maximum number of retry attempts to establish a connection to the remote Message VPN. A value of 0 means to retry forever.  # noqa: E501

        :return: The remote_connection_retry_count of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._remote_connection_retry_count

    @remote_connection_retry_count.setter
    def remote_connection_retry_count(self, remote_connection_retry_count):
        """Sets the remote_connection_retry_count of this MsgVpnBridge.

        The maximum number of retry attempts to establish a connection to the remote Message VPN. A value of 0 means to retry forever.  # noqa: E501

        :param remote_connection_retry_count: The remote_connection_retry_count of this MsgVpnBridge.  # noqa: E501
        :type: int
        """

        self._remote_connection_retry_count = remote_connection_retry_count

    @property
    def remote_connection_retry_delay(self):
        """Gets the remote_connection_retry_delay of this MsgVpnBridge.  # noqa: E501

        The number of seconds to delay before retrying to connect to the remote Message VPN.  # noqa: E501

        :return: The remote_connection_retry_delay of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._remote_connection_retry_delay

    @remote_connection_retry_delay.setter
    def remote_connection_retry_delay(self, remote_connection_retry_delay):
        """Sets the remote_connection_retry_delay of this MsgVpnBridge.

        The number of seconds to delay before retrying to connect to the remote Message VPN.  # noqa: E501

        :param remote_connection_retry_delay: The remote_connection_retry_delay of this MsgVpnBridge.  # noqa: E501
        :type: int
        """

        self._remote_connection_retry_delay = remote_connection_retry_delay

    @property
    def remote_deliver_to_one_priority(self):
        """Gets the remote_deliver_to_one_priority of this MsgVpnBridge.  # noqa: E501

        The priority for deliver-to-one (DTO) messages transmitted from the remote Message VPN. The allowed values and their meaning are:  <pre> \"p1\" - The 1st or highest priority. \"p2\" - The 2nd highest priority. \"p3\" - The 3rd highest priority. \"p4\" - The 4th highest priority. \"da\" - Ignore priority and deliver always. </pre>   # noqa: E501

        :return: The remote_deliver_to_one_priority of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_deliver_to_one_priority

    @remote_deliver_to_one_priority.setter
    def remote_deliver_to_one_priority(self, remote_deliver_to_one_priority):
        """Sets the remote_deliver_to_one_priority of this MsgVpnBridge.

        The priority for deliver-to-one (DTO) messages transmitted from the remote Message VPN. The allowed values and their meaning are:  <pre> \"p1\" - The 1st or highest priority. \"p2\" - The 2nd highest priority. \"p3\" - The 3rd highest priority. \"p4\" - The 4th highest priority. \"da\" - Ignore priority and deliver always. </pre>   # noqa: E501

        :param remote_deliver_to_one_priority: The remote_deliver_to_one_priority of this MsgVpnBridge.  # noqa: E501
        :type: str
        """
        allowed_values = ["p1", "p2", "p3", "p4", "da"]  # noqa: E501
        if remote_deliver_to_one_priority not in allowed_values:
            raise ValueError(
                "Invalid value for `remote_deliver_to_one_priority` ({0}), must be one of {1}"  # noqa: E501
                .format(remote_deliver_to_one_priority, allowed_values)
            )

        self._remote_deliver_to_one_priority = remote_deliver_to_one_priority

    @property
    def remote_msg_vpn_name(self):
        """Gets the remote_msg_vpn_name of this MsgVpnBridge.  # noqa: E501

        The name of the remote Message VPN.  # noqa: E501

        :return: The remote_msg_vpn_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_msg_vpn_name

    @remote_msg_vpn_name.setter
    def remote_msg_vpn_name(self, remote_msg_vpn_name):
        """Sets the remote_msg_vpn_name of this MsgVpnBridge.

        The name of the remote Message VPN.  # noqa: E501

        :param remote_msg_vpn_name: The remote_msg_vpn_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._remote_msg_vpn_name = remote_msg_vpn_name

    @property
    def remote_router_name(self):
        """Gets the remote_router_name of this MsgVpnBridge.  # noqa: E501

        The name of the remote router.  # noqa: E501

        :return: The remote_router_name of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._remote_router_name

    @remote_router_name.setter
    def remote_router_name(self, remote_router_name):
        """Sets the remote_router_name of this MsgVpnBridge.

        The name of the remote router.  # noqa: E501

        :param remote_router_name: The remote_router_name of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._remote_router_name = remote_router_name

    @property
    def remote_tx_flow_id(self):
        """Gets the remote_tx_flow_id of this MsgVpnBridge.  # noqa: E501

        The ID of the transmit flow for the connected remote Message VPN.  # noqa: E501

        :return: The remote_tx_flow_id of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._remote_tx_flow_id

    @remote_tx_flow_id.setter
    def remote_tx_flow_id(self, remote_tx_flow_id):
        """Sets the remote_tx_flow_id of this MsgVpnBridge.

        The ID of the transmit flow for the connected remote Message VPN.  # noqa: E501

        :param remote_tx_flow_id: The remote_tx_flow_id of this MsgVpnBridge.  # noqa: E501
        :type: int
        """

        self._remote_tx_flow_id = remote_tx_flow_id

    @property
    def tls_cipher_suite_list(self):
        """Gets the tls_cipher_suite_list of this MsgVpnBridge.  # noqa: E501

        The colon-separated list of cipher-suites supported for TLS connections to the remote Message VPN. The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :return: The tls_cipher_suite_list of this MsgVpnBridge.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_list

    @tls_cipher_suite_list.setter
    def tls_cipher_suite_list(self, tls_cipher_suite_list):
        """Sets the tls_cipher_suite_list of this MsgVpnBridge.

        The colon-separated list of cipher-suites supported for TLS connections to the remote Message VPN. The value \"default\" implies all supported suites ordered from most secure to least secure.  # noqa: E501

        :param tls_cipher_suite_list: The tls_cipher_suite_list of this MsgVpnBridge.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_list = tls_cipher_suite_list

    @property
    def tls_default_cipher_suite_list(self):
        """Gets the tls_default_cipher_suite_list of this MsgVpnBridge.  # noqa: E501

        Indicates whether the Bridge is configured to use the default cipher-suite list.  # noqa: E501

        :return: The tls_default_cipher_suite_list of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._tls_default_cipher_suite_list

    @tls_default_cipher_suite_list.setter
    def tls_default_cipher_suite_list(self, tls_default_cipher_suite_list):
        """Sets the tls_default_cipher_suite_list of this MsgVpnBridge.

        Indicates whether the Bridge is configured to use the default cipher-suite list.  # noqa: E501

        :param tls_default_cipher_suite_list: The tls_default_cipher_suite_list of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._tls_default_cipher_suite_list = tls_default_cipher_suite_list

    @property
    def ttl_exceeded_event_raised(self):
        """Gets the ttl_exceeded_event_raised of this MsgVpnBridge.  # noqa: E501

        Indicates whether the TTL (hops) exceeded event has been raised.  # noqa: E501

        :return: The ttl_exceeded_event_raised of this MsgVpnBridge.  # noqa: E501
        :rtype: bool
        """
        return self._ttl_exceeded_event_raised

    @ttl_exceeded_event_raised.setter
    def ttl_exceeded_event_raised(self, ttl_exceeded_event_raised):
        """Sets the ttl_exceeded_event_raised of this MsgVpnBridge.

        Indicates whether the TTL (hops) exceeded event has been raised.  # noqa: E501

        :param ttl_exceeded_event_raised: The ttl_exceeded_event_raised of this MsgVpnBridge.  # noqa: E501
        :type: bool
        """

        self._ttl_exceeded_event_raised = ttl_exceeded_event_raised

    @property
    def uptime(self):
        """Gets the uptime of this MsgVpnBridge.  # noqa: E501

        The amount of time in seconds since the Bridge connected to the remote Message VPN.  # noqa: E501

        :return: The uptime of this MsgVpnBridge.  # noqa: E501
        :rtype: int
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """Sets the uptime of this MsgVpnBridge.

        The amount of time in seconds since the Bridge connected to the remote Message VPN.  # noqa: E501

        :param uptime: The uptime of this MsgVpnBridge.  # noqa: E501
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
        if issubclass(MsgVpnBridge, dict):
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
        if not isinstance(other, MsgVpnBridge):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
