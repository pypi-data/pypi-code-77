# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.17
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnBridgeRemoteMsgVpn(object):
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
        'client_username': 'str',
        'compressed_data_enabled': 'bool',
        'connect_order': 'int',
        'egress_flow_window_size': 'int',
        'enabled': 'bool',
        'last_connection_failure_reason': 'str',
        'last_queue_bind_failure_reason': 'str',
        'msg_vpn_name': 'str',
        'queue_binding': 'str',
        'queue_bound_uptime': 'int',
        'remote_msg_vpn_interface': 'str',
        'remote_msg_vpn_location': 'str',
        'remote_msg_vpn_name': 'str',
        'tls_enabled': 'bool',
        'unidirectional_client_profile': 'str',
        'up': 'bool'
    }

    attribute_map = {
        'bound_to_queue': 'boundToQueue',
        'bridge_name': 'bridgeName',
        'bridge_virtual_router': 'bridgeVirtualRouter',
        'client_username': 'clientUsername',
        'compressed_data_enabled': 'compressedDataEnabled',
        'connect_order': 'connectOrder',
        'egress_flow_window_size': 'egressFlowWindowSize',
        'enabled': 'enabled',
        'last_connection_failure_reason': 'lastConnectionFailureReason',
        'last_queue_bind_failure_reason': 'lastQueueBindFailureReason',
        'msg_vpn_name': 'msgVpnName',
        'queue_binding': 'queueBinding',
        'queue_bound_uptime': 'queueBoundUptime',
        'remote_msg_vpn_interface': 'remoteMsgVpnInterface',
        'remote_msg_vpn_location': 'remoteMsgVpnLocation',
        'remote_msg_vpn_name': 'remoteMsgVpnName',
        'tls_enabled': 'tlsEnabled',
        'unidirectional_client_profile': 'unidirectionalClientProfile',
        'up': 'up'
    }

    def __init__(self, bound_to_queue=None, bridge_name=None, bridge_virtual_router=None, client_username=None, compressed_data_enabled=None, connect_order=None, egress_flow_window_size=None, enabled=None, last_connection_failure_reason=None, last_queue_bind_failure_reason=None, msg_vpn_name=None, queue_binding=None, queue_bound_uptime=None, remote_msg_vpn_interface=None, remote_msg_vpn_location=None, remote_msg_vpn_name=None, tls_enabled=None, unidirectional_client_profile=None, up=None):  # noqa: E501
        """MsgVpnBridgeRemoteMsgVpn - a model defined in Swagger"""  # noqa: E501

        self._bound_to_queue = None
        self._bridge_name = None
        self._bridge_virtual_router = None
        self._client_username = None
        self._compressed_data_enabled = None
        self._connect_order = None
        self._egress_flow_window_size = None
        self._enabled = None
        self._last_connection_failure_reason = None
        self._last_queue_bind_failure_reason = None
        self._msg_vpn_name = None
        self._queue_binding = None
        self._queue_bound_uptime = None
        self._remote_msg_vpn_interface = None
        self._remote_msg_vpn_location = None
        self._remote_msg_vpn_name = None
        self._tls_enabled = None
        self._unidirectional_client_profile = None
        self._up = None
        self.discriminator = None

        if bound_to_queue is not None:
            self.bound_to_queue = bound_to_queue
        if bridge_name is not None:
            self.bridge_name = bridge_name
        if bridge_virtual_router is not None:
            self.bridge_virtual_router = bridge_virtual_router
        if client_username is not None:
            self.client_username = client_username
        if compressed_data_enabled is not None:
            self.compressed_data_enabled = compressed_data_enabled
        if connect_order is not None:
            self.connect_order = connect_order
        if egress_flow_window_size is not None:
            self.egress_flow_window_size = egress_flow_window_size
        if enabled is not None:
            self.enabled = enabled
        if last_connection_failure_reason is not None:
            self.last_connection_failure_reason = last_connection_failure_reason
        if last_queue_bind_failure_reason is not None:
            self.last_queue_bind_failure_reason = last_queue_bind_failure_reason
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if queue_binding is not None:
            self.queue_binding = queue_binding
        if queue_bound_uptime is not None:
            self.queue_bound_uptime = queue_bound_uptime
        if remote_msg_vpn_interface is not None:
            self.remote_msg_vpn_interface = remote_msg_vpn_interface
        if remote_msg_vpn_location is not None:
            self.remote_msg_vpn_location = remote_msg_vpn_location
        if remote_msg_vpn_name is not None:
            self.remote_msg_vpn_name = remote_msg_vpn_name
        if tls_enabled is not None:
            self.tls_enabled = tls_enabled
        if unidirectional_client_profile is not None:
            self.unidirectional_client_profile = unidirectional_client_profile
        if up is not None:
            self.up = up

    @property
    def bound_to_queue(self):
        """Gets the bound_to_queue of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        Indicates whether the Bridge is bound to the queue in the remote Message VPN.  # noqa: E501

        :return: The bound_to_queue of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._bound_to_queue

    @bound_to_queue.setter
    def bound_to_queue(self, bound_to_queue):
        """Sets the bound_to_queue of this MsgVpnBridgeRemoteMsgVpn.

        Indicates whether the Bridge is bound to the queue in the remote Message VPN.  # noqa: E501

        :param bound_to_queue: The bound_to_queue of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: bool
        """

        self._bound_to_queue = bound_to_queue

    @property
    def bridge_name(self):
        """Gets the bridge_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The name of the Bridge.  # noqa: E501

        :return: The bridge_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._bridge_name

    @bridge_name.setter
    def bridge_name(self, bridge_name):
        """Sets the bridge_name of this MsgVpnBridgeRemoteMsgVpn.

        The name of the Bridge.  # noqa: E501

        :param bridge_name: The bridge_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._bridge_name = bridge_name

    @property
    def bridge_virtual_router(self):
        """Gets the bridge_virtual_router of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The virtual router of the Bridge. The allowed values and their meaning are:  <pre> \"primary\" - The Bridge is used for the primary virtual router. \"backup\" - The Bridge is used for the backup virtual router. \"auto\" - The Bridge is automatically assigned a virtual router at creation, depending on the broker's active-standby role. </pre>   # noqa: E501

        :return: The bridge_virtual_router of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._bridge_virtual_router

    @bridge_virtual_router.setter
    def bridge_virtual_router(self, bridge_virtual_router):
        """Sets the bridge_virtual_router of this MsgVpnBridgeRemoteMsgVpn.

        The virtual router of the Bridge. The allowed values and their meaning are:  <pre> \"primary\" - The Bridge is used for the primary virtual router. \"backup\" - The Bridge is used for the backup virtual router. \"auto\" - The Bridge is automatically assigned a virtual router at creation, depending on the broker's active-standby role. </pre>   # noqa: E501

        :param bridge_virtual_router: The bridge_virtual_router of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
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
    def client_username(self):
        """Gets the client_username of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The Client Username the Bridge uses to login to the remote Message VPN. This per remote Message VPN value overrides the value provided for the Bridge overall.  # noqa: E501

        :return: The client_username of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._client_username

    @client_username.setter
    def client_username(self, client_username):
        """Sets the client_username of this MsgVpnBridgeRemoteMsgVpn.

        The Client Username the Bridge uses to login to the remote Message VPN. This per remote Message VPN value overrides the value provided for the Bridge overall.  # noqa: E501

        :param client_username: The client_username of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._client_username = client_username

    @property
    def compressed_data_enabled(self):
        """Gets the compressed_data_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        Indicates whether data compression is enabled for the remote Message VPN connection.  # noqa: E501

        :return: The compressed_data_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._compressed_data_enabled

    @compressed_data_enabled.setter
    def compressed_data_enabled(self, compressed_data_enabled):
        """Sets the compressed_data_enabled of this MsgVpnBridgeRemoteMsgVpn.

        Indicates whether data compression is enabled for the remote Message VPN connection.  # noqa: E501

        :param compressed_data_enabled: The compressed_data_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: bool
        """

        self._compressed_data_enabled = compressed_data_enabled

    @property
    def connect_order(self):
        """Gets the connect_order of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The preference given to incoming connections from remote Message VPN hosts, from 1 (highest priority) to 4 (lowest priority).  # noqa: E501

        :return: The connect_order of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._connect_order

    @connect_order.setter
    def connect_order(self, connect_order):
        """Sets the connect_order of this MsgVpnBridgeRemoteMsgVpn.

        The preference given to incoming connections from remote Message VPN hosts, from 1 (highest priority) to 4 (lowest priority).  # noqa: E501

        :param connect_order: The connect_order of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: int
        """

        self._connect_order = connect_order

    @property
    def egress_flow_window_size(self):
        """Gets the egress_flow_window_size of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The number of outstanding guaranteed messages that can be transmitted over the remote Message VPN connection before an acknowledgement is received.  # noqa: E501

        :return: The egress_flow_window_size of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._egress_flow_window_size

    @egress_flow_window_size.setter
    def egress_flow_window_size(self, egress_flow_window_size):
        """Sets the egress_flow_window_size of this MsgVpnBridgeRemoteMsgVpn.

        The number of outstanding guaranteed messages that can be transmitted over the remote Message VPN connection before an acknowledgement is received.  # noqa: E501

        :param egress_flow_window_size: The egress_flow_window_size of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: int
        """

        self._egress_flow_window_size = egress_flow_window_size

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        Indicates whether the remote Message VPN is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnBridgeRemoteMsgVpn.

        Indicates whether the remote Message VPN is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def last_connection_failure_reason(self):
        """Gets the last_connection_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The reason for the last connection failure to the remote Message VPN.  # noqa: E501

        :return: The last_connection_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._last_connection_failure_reason

    @last_connection_failure_reason.setter
    def last_connection_failure_reason(self, last_connection_failure_reason):
        """Sets the last_connection_failure_reason of this MsgVpnBridgeRemoteMsgVpn.

        The reason for the last connection failure to the remote Message VPN.  # noqa: E501

        :param last_connection_failure_reason: The last_connection_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._last_connection_failure_reason = last_connection_failure_reason

    @property
    def last_queue_bind_failure_reason(self):
        """Gets the last_queue_bind_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The reason for the last queue bind failure in the remote Message VPN.  # noqa: E501

        :return: The last_queue_bind_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._last_queue_bind_failure_reason

    @last_queue_bind_failure_reason.setter
    def last_queue_bind_failure_reason(self, last_queue_bind_failure_reason):
        """Sets the last_queue_bind_failure_reason of this MsgVpnBridgeRemoteMsgVpn.

        The reason for the last queue bind failure in the remote Message VPN.  # noqa: E501

        :param last_queue_bind_failure_reason: The last_queue_bind_failure_reason of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._last_queue_bind_failure_reason = last_queue_bind_failure_reason

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def queue_binding(self):
        """Gets the queue_binding of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The queue binding of the Bridge in the remote Message VPN.  # noqa: E501

        :return: The queue_binding of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._queue_binding

    @queue_binding.setter
    def queue_binding(self, queue_binding):
        """Sets the queue_binding of this MsgVpnBridgeRemoteMsgVpn.

        The queue binding of the Bridge in the remote Message VPN.  # noqa: E501

        :param queue_binding: The queue_binding of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._queue_binding = queue_binding

    @property
    def queue_bound_uptime(self):
        """Gets the queue_bound_uptime of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The amount of time in seconds since the queue was bound in the remote Message VPN.  # noqa: E501

        :return: The queue_bound_uptime of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: int
        """
        return self._queue_bound_uptime

    @queue_bound_uptime.setter
    def queue_bound_uptime(self, queue_bound_uptime):
        """Sets the queue_bound_uptime of this MsgVpnBridgeRemoteMsgVpn.

        The amount of time in seconds since the queue was bound in the remote Message VPN.  # noqa: E501

        :param queue_bound_uptime: The queue_bound_uptime of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: int
        """

        self._queue_bound_uptime = queue_bound_uptime

    @property
    def remote_msg_vpn_interface(self):
        """Gets the remote_msg_vpn_interface of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The physical interface on the local Message VPN host for connecting to the remote Message VPN. By default, an interface is chosen automatically (recommended), but if specified, `remoteMsgVpnLocation` must not be a virtual router name.  # noqa: E501

        :return: The remote_msg_vpn_interface of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._remote_msg_vpn_interface

    @remote_msg_vpn_interface.setter
    def remote_msg_vpn_interface(self, remote_msg_vpn_interface):
        """Sets the remote_msg_vpn_interface of this MsgVpnBridgeRemoteMsgVpn.

        The physical interface on the local Message VPN host for connecting to the remote Message VPN. By default, an interface is chosen automatically (recommended), but if specified, `remoteMsgVpnLocation` must not be a virtual router name.  # noqa: E501

        :param remote_msg_vpn_interface: The remote_msg_vpn_interface of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._remote_msg_vpn_interface = remote_msg_vpn_interface

    @property
    def remote_msg_vpn_location(self):
        """Gets the remote_msg_vpn_location of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The location of the remote Message VPN as either an FQDN with port, IP address with port, or virtual router name (starting with \"v:\").  # noqa: E501

        :return: The remote_msg_vpn_location of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._remote_msg_vpn_location

    @remote_msg_vpn_location.setter
    def remote_msg_vpn_location(self, remote_msg_vpn_location):
        """Sets the remote_msg_vpn_location of this MsgVpnBridgeRemoteMsgVpn.

        The location of the remote Message VPN as either an FQDN with port, IP address with port, or virtual router name (starting with \"v:\").  # noqa: E501

        :param remote_msg_vpn_location: The remote_msg_vpn_location of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._remote_msg_vpn_location = remote_msg_vpn_location

    @property
    def remote_msg_vpn_name(self):
        """Gets the remote_msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The name of the remote Message VPN.  # noqa: E501

        :return: The remote_msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._remote_msg_vpn_name

    @remote_msg_vpn_name.setter
    def remote_msg_vpn_name(self, remote_msg_vpn_name):
        """Sets the remote_msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.

        The name of the remote Message VPN.  # noqa: E501

        :param remote_msg_vpn_name: The remote_msg_vpn_name of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._remote_msg_vpn_name = remote_msg_vpn_name

    @property
    def tls_enabled(self):
        """Gets the tls_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        Indicates whether encryption (TLS) is enabled for the remote Message VPN connection.  # noqa: E501

        :return: The tls_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._tls_enabled

    @tls_enabled.setter
    def tls_enabled(self, tls_enabled):
        """Sets the tls_enabled of this MsgVpnBridgeRemoteMsgVpn.

        Indicates whether encryption (TLS) is enabled for the remote Message VPN connection.  # noqa: E501

        :param tls_enabled: The tls_enabled of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: bool
        """

        self._tls_enabled = tls_enabled

    @property
    def unidirectional_client_profile(self):
        """Gets the unidirectional_client_profile of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        The Client Profile for the unidirectional Bridge of the remote Message VPN. The Client Profile must exist in the local Message VPN, and it is used only for the TCP parameters. Note that the default client profile has a TCP maximum window size of 2MB.  # noqa: E501

        :return: The unidirectional_client_profile of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: str
        """
        return self._unidirectional_client_profile

    @unidirectional_client_profile.setter
    def unidirectional_client_profile(self, unidirectional_client_profile):
        """Sets the unidirectional_client_profile of this MsgVpnBridgeRemoteMsgVpn.

        The Client Profile for the unidirectional Bridge of the remote Message VPN. The Client Profile must exist in the local Message VPN, and it is used only for the TCP parameters. Note that the default client profile has a TCP maximum window size of 2MB.  # noqa: E501

        :param unidirectional_client_profile: The unidirectional_client_profile of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: str
        """

        self._unidirectional_client_profile = unidirectional_client_profile

    @property
    def up(self):
        """Gets the up of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501

        Indicates whether the connection to the remote Message VPN is up.  # noqa: E501

        :return: The up of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :rtype: bool
        """
        return self._up

    @up.setter
    def up(self, up):
        """Sets the up of this MsgVpnBridgeRemoteMsgVpn.

        Indicates whether the connection to the remote Message VPN is up.  # noqa: E501

        :param up: The up of this MsgVpnBridgeRemoteMsgVpn.  # noqa: E501
        :type: bool
        """

        self._up = up

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
        if issubclass(MsgVpnBridgeRemoteMsgVpn, dict):
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
        if not isinstance(other, MsgVpnBridgeRemoteMsgVpn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
