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


class MsgVpnClientConnection(object):
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
        'client_address': 'str',
        'client_name': 'str',
        'compression': 'bool',
        'encryption': 'bool',
        'fast_retransmit_count': 'int',
        'msg_vpn_name': 'str',
        'rx_queue_byte_count': 'int',
        'segment_received_out_of_order_count': 'int',
        'smoothed_round_trip_time': 'int',
        'tcp_state': 'str',
        'timed_retransmit_count': 'int',
        'tx_queue_byte_count': 'int',
        'uptime': 'int'
    }

    attribute_map = {
        'client_address': 'clientAddress',
        'client_name': 'clientName',
        'compression': 'compression',
        'encryption': 'encryption',
        'fast_retransmit_count': 'fastRetransmitCount',
        'msg_vpn_name': 'msgVpnName',
        'rx_queue_byte_count': 'rxQueueByteCount',
        'segment_received_out_of_order_count': 'segmentReceivedOutOfOrderCount',
        'smoothed_round_trip_time': 'smoothedRoundTripTime',
        'tcp_state': 'tcpState',
        'timed_retransmit_count': 'timedRetransmitCount',
        'tx_queue_byte_count': 'txQueueByteCount',
        'uptime': 'uptime'
    }

    def __init__(self, client_address=None, client_name=None, compression=None, encryption=None, fast_retransmit_count=None, msg_vpn_name=None, rx_queue_byte_count=None, segment_received_out_of_order_count=None, smoothed_round_trip_time=None, tcp_state=None, timed_retransmit_count=None, tx_queue_byte_count=None, uptime=None):  # noqa: E501
        """MsgVpnClientConnection - a model defined in Swagger"""  # noqa: E501

        self._client_address = None
        self._client_name = None
        self._compression = None
        self._encryption = None
        self._fast_retransmit_count = None
        self._msg_vpn_name = None
        self._rx_queue_byte_count = None
        self._segment_received_out_of_order_count = None
        self._smoothed_round_trip_time = None
        self._tcp_state = None
        self._timed_retransmit_count = None
        self._tx_queue_byte_count = None
        self._uptime = None
        self.discriminator = None

        if client_address is not None:
            self.client_address = client_address
        if client_name is not None:
            self.client_name = client_name
        if compression is not None:
            self.compression = compression
        if encryption is not None:
            self.encryption = encryption
        if fast_retransmit_count is not None:
            self.fast_retransmit_count = fast_retransmit_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if rx_queue_byte_count is not None:
            self.rx_queue_byte_count = rx_queue_byte_count
        if segment_received_out_of_order_count is not None:
            self.segment_received_out_of_order_count = segment_received_out_of_order_count
        if smoothed_round_trip_time is not None:
            self.smoothed_round_trip_time = smoothed_round_trip_time
        if tcp_state is not None:
            self.tcp_state = tcp_state
        if timed_retransmit_count is not None:
            self.timed_retransmit_count = timed_retransmit_count
        if tx_queue_byte_count is not None:
            self.tx_queue_byte_count = tx_queue_byte_count
        if uptime is not None:
            self.uptime = uptime

    @property
    def client_address(self):
        """Gets the client_address of this MsgVpnClientConnection.  # noqa: E501

        The IP address and TCP port on the Client side of the Client Connection.  # noqa: E501

        :return: The client_address of this MsgVpnClientConnection.  # noqa: E501
        :rtype: str
        """
        return self._client_address

    @client_address.setter
    def client_address(self, client_address):
        """Sets the client_address of this MsgVpnClientConnection.

        The IP address and TCP port on the Client side of the Client Connection.  # noqa: E501

        :param client_address: The client_address of this MsgVpnClientConnection.  # noqa: E501
        :type: str
        """

        self._client_address = client_address

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnClientConnection.  # noqa: E501

        The name of the Client.  # noqa: E501

        :return: The client_name of this MsgVpnClientConnection.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnClientConnection.

        The name of the Client.  # noqa: E501

        :param client_name: The client_name of this MsgVpnClientConnection.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def compression(self):
        """Gets the compression of this MsgVpnClientConnection.  # noqa: E501

        Indicates whether compression is enabled for the Client Connection.  # noqa: E501

        :return: The compression of this MsgVpnClientConnection.  # noqa: E501
        :rtype: bool
        """
        return self._compression

    @compression.setter
    def compression(self, compression):
        """Sets the compression of this MsgVpnClientConnection.

        Indicates whether compression is enabled for the Client Connection.  # noqa: E501

        :param compression: The compression of this MsgVpnClientConnection.  # noqa: E501
        :type: bool
        """

        self._compression = compression

    @property
    def encryption(self):
        """Gets the encryption of this MsgVpnClientConnection.  # noqa: E501

        Indicates whether TLS encryption is enabled for the Client Connection.  # noqa: E501

        :return: The encryption of this MsgVpnClientConnection.  # noqa: E501
        :rtype: bool
        """
        return self._encryption

    @encryption.setter
    def encryption(self, encryption):
        """Sets the encryption of this MsgVpnClientConnection.

        Indicates whether TLS encryption is enabled for the Client Connection.  # noqa: E501

        :param encryption: The encryption of this MsgVpnClientConnection.  # noqa: E501
        :type: bool
        """

        self._encryption = encryption

    @property
    def fast_retransmit_count(self):
        """Gets the fast_retransmit_count of this MsgVpnClientConnection.  # noqa: E501

        The number of TCP fast retransmits due to duplicate acknowledgments (ACKs). See RFC 5681 for further details.  # noqa: E501

        :return: The fast_retransmit_count of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._fast_retransmit_count

    @fast_retransmit_count.setter
    def fast_retransmit_count(self, fast_retransmit_count):
        """Sets the fast_retransmit_count of this MsgVpnClientConnection.

        The number of TCP fast retransmits due to duplicate acknowledgments (ACKs). See RFC 5681 for further details.  # noqa: E501

        :param fast_retransmit_count: The fast_retransmit_count of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._fast_retransmit_count = fast_retransmit_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnClientConnection.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnClientConnection.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnClientConnection.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnClientConnection.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def rx_queue_byte_count(self):
        """Gets the rx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501

        The number of bytes currently in the receive queue for the Client Connection.  # noqa: E501

        :return: The rx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._rx_queue_byte_count

    @rx_queue_byte_count.setter
    def rx_queue_byte_count(self, rx_queue_byte_count):
        """Sets the rx_queue_byte_count of this MsgVpnClientConnection.

        The number of bytes currently in the receive queue for the Client Connection.  # noqa: E501

        :param rx_queue_byte_count: The rx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._rx_queue_byte_count = rx_queue_byte_count

    @property
    def segment_received_out_of_order_count(self):
        """Gets the segment_received_out_of_order_count of this MsgVpnClientConnection.  # noqa: E501

        The number of TCP segments received from the Client Connection out of order.  # noqa: E501

        :return: The segment_received_out_of_order_count of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._segment_received_out_of_order_count

    @segment_received_out_of_order_count.setter
    def segment_received_out_of_order_count(self, segment_received_out_of_order_count):
        """Sets the segment_received_out_of_order_count of this MsgVpnClientConnection.

        The number of TCP segments received from the Client Connection out of order.  # noqa: E501

        :param segment_received_out_of_order_count: The segment_received_out_of_order_count of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._segment_received_out_of_order_count = segment_received_out_of_order_count

    @property
    def smoothed_round_trip_time(self):
        """Gets the smoothed_round_trip_time of this MsgVpnClientConnection.  # noqa: E501

        The TCP smoothed round-trip time (SRTT) for the Client Connection, in nanoseconds. See RFC 2988 for further details.  # noqa: E501

        :return: The smoothed_round_trip_time of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._smoothed_round_trip_time

    @smoothed_round_trip_time.setter
    def smoothed_round_trip_time(self, smoothed_round_trip_time):
        """Sets the smoothed_round_trip_time of this MsgVpnClientConnection.

        The TCP smoothed round-trip time (SRTT) for the Client Connection, in nanoseconds. See RFC 2988 for further details.  # noqa: E501

        :param smoothed_round_trip_time: The smoothed_round_trip_time of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._smoothed_round_trip_time = smoothed_round_trip_time

    @property
    def tcp_state(self):
        """Gets the tcp_state of this MsgVpnClientConnection.  # noqa: E501

        The TCP state of the Client Connection. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :return: The tcp_state of this MsgVpnClientConnection.  # noqa: E501
        :rtype: str
        """
        return self._tcp_state

    @tcp_state.setter
    def tcp_state(self, tcp_state):
        """Sets the tcp_state of this MsgVpnClientConnection.

        The TCP state of the Client Connection. When fully operational, should be: established. See RFC 793 for further details. The allowed values and their meaning are:  <pre> \"closed\" - No connection state at all. \"listen\" - Waiting for a connection request from any remote TCP and port. \"syn-sent\" - Waiting for a matching connection request after having sent a connection request. \"syn-received\" - Waiting for a confirming connection request acknowledgment after having both received and sent a connection request. \"established\" - An open connection, data received can be delivered to the user. \"close-wait\" - Waiting for a connection termination request from the local user. \"fin-wait-1\" - Waiting for a connection termination request from the remote TCP, or an acknowledgment of the connection termination request previously sent. \"closing\" - Waiting for a connection termination request acknowledgment from the remote TCP. \"last-ack\" - Waiting for an acknowledgment of the connection termination request previously sent to the remote TCP. \"fin-wait-2\" - Waiting for a connection termination request from the remote TCP. \"time-wait\" - Waiting for enough time to pass to be sure the remote TCP received the acknowledgment of its connection termination request. </pre>   # noqa: E501

        :param tcp_state: The tcp_state of this MsgVpnClientConnection.  # noqa: E501
        :type: str
        """

        self._tcp_state = tcp_state

    @property
    def timed_retransmit_count(self):
        """Gets the timed_retransmit_count of this MsgVpnClientConnection.  # noqa: E501

        The number of TCP segments retransmitted due to timeout awaiting an acknowledgement (ACK). See RFC 793 for further details.  # noqa: E501

        :return: The timed_retransmit_count of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._timed_retransmit_count

    @timed_retransmit_count.setter
    def timed_retransmit_count(self, timed_retransmit_count):
        """Sets the timed_retransmit_count of this MsgVpnClientConnection.

        The number of TCP segments retransmitted due to timeout awaiting an acknowledgement (ACK). See RFC 793 for further details.  # noqa: E501

        :param timed_retransmit_count: The timed_retransmit_count of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._timed_retransmit_count = timed_retransmit_count

    @property
    def tx_queue_byte_count(self):
        """Gets the tx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501

        The number of bytes currently in the transmit queue for the Client Connection.  # noqa: E501

        :return: The tx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._tx_queue_byte_count

    @tx_queue_byte_count.setter
    def tx_queue_byte_count(self, tx_queue_byte_count):
        """Sets the tx_queue_byte_count of this MsgVpnClientConnection.

        The number of bytes currently in the transmit queue for the Client Connection.  # noqa: E501

        :param tx_queue_byte_count: The tx_queue_byte_count of this MsgVpnClientConnection.  # noqa: E501
        :type: int
        """

        self._tx_queue_byte_count = tx_queue_byte_count

    @property
    def uptime(self):
        """Gets the uptime of this MsgVpnClientConnection.  # noqa: E501

        The amount of time in seconds since the Client Connection was established.  # noqa: E501

        :return: The uptime of this MsgVpnClientConnection.  # noqa: E501
        :rtype: int
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """Sets the uptime of this MsgVpnClientConnection.

        The amount of time in seconds since the Client Connection was established.  # noqa: E501

        :param uptime: The uptime of this MsgVpnClientConnection.  # noqa: E501
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
        if issubclass(MsgVpnClientConnection, dict):
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
        if not isinstance(other, MsgVpnClientConnection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
