# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.13
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnTopicEndpointTxFlow(object):
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
        'acked_msg_count': 'int',
        'activity_state': 'str',
        'bind_time': 'int',
        'client_name': 'str',
        'consumer_redelivery_request_allowed': 'bool',
        'cut_through_acked_msg_count': 'int',
        'delivery_state': 'str',
        'flow_id': 'int',
        'highest_ack_pending_msg_id': 'int',
        'last_acked_msg_id': 'int',
        'lowest_ack_pending_msg_id': 'int',
        'max_unacked_msgs_exceeded_msg_count': 'int',
        'msg_vpn_name': 'str',
        'no_local_delivery': 'bool',
        'redelivered_msg_count': 'int',
        'redelivery_request_count': 'int',
        'session_name': 'str',
        'store_and_forward_acked_msg_count': 'int',
        'topic_endpoint_name': 'str',
        'unacked_msg_count': 'int',
        'used_window_size': 'int',
        'window_closed_count': 'int',
        'window_size': 'int'
    }

    attribute_map = {
        'acked_msg_count': 'ackedMsgCount',
        'activity_state': 'activityState',
        'bind_time': 'bindTime',
        'client_name': 'clientName',
        'consumer_redelivery_request_allowed': 'consumerRedeliveryRequestAllowed',
        'cut_through_acked_msg_count': 'cutThroughAckedMsgCount',
        'delivery_state': 'deliveryState',
        'flow_id': 'flowId',
        'highest_ack_pending_msg_id': 'highestAckPendingMsgId',
        'last_acked_msg_id': 'lastAckedMsgId',
        'lowest_ack_pending_msg_id': 'lowestAckPendingMsgId',
        'max_unacked_msgs_exceeded_msg_count': 'maxUnackedMsgsExceededMsgCount',
        'msg_vpn_name': 'msgVpnName',
        'no_local_delivery': 'noLocalDelivery',
        'redelivered_msg_count': 'redeliveredMsgCount',
        'redelivery_request_count': 'redeliveryRequestCount',
        'session_name': 'sessionName',
        'store_and_forward_acked_msg_count': 'storeAndForwardAckedMsgCount',
        'topic_endpoint_name': 'topicEndpointName',
        'unacked_msg_count': 'unackedMsgCount',
        'used_window_size': 'usedWindowSize',
        'window_closed_count': 'windowClosedCount',
        'window_size': 'windowSize'
    }

    def __init__(self, acked_msg_count=None, activity_state=None, bind_time=None, client_name=None, consumer_redelivery_request_allowed=None, cut_through_acked_msg_count=None, delivery_state=None, flow_id=None, highest_ack_pending_msg_id=None, last_acked_msg_id=None, lowest_ack_pending_msg_id=None, max_unacked_msgs_exceeded_msg_count=None, msg_vpn_name=None, no_local_delivery=None, redelivered_msg_count=None, redelivery_request_count=None, session_name=None, store_and_forward_acked_msg_count=None, topic_endpoint_name=None, unacked_msg_count=None, used_window_size=None, window_closed_count=None, window_size=None):  # noqa: E501
        """MsgVpnTopicEndpointTxFlow - a model defined in Swagger"""  # noqa: E501

        self._acked_msg_count = None
        self._activity_state = None
        self._bind_time = None
        self._client_name = None
        self._consumer_redelivery_request_allowed = None
        self._cut_through_acked_msg_count = None
        self._delivery_state = None
        self._flow_id = None
        self._highest_ack_pending_msg_id = None
        self._last_acked_msg_id = None
        self._lowest_ack_pending_msg_id = None
        self._max_unacked_msgs_exceeded_msg_count = None
        self._msg_vpn_name = None
        self._no_local_delivery = None
        self._redelivered_msg_count = None
        self._redelivery_request_count = None
        self._session_name = None
        self._store_and_forward_acked_msg_count = None
        self._topic_endpoint_name = None
        self._unacked_msg_count = None
        self._used_window_size = None
        self._window_closed_count = None
        self._window_size = None
        self.discriminator = None

        if acked_msg_count is not None:
            self.acked_msg_count = acked_msg_count
        if activity_state is not None:
            self.activity_state = activity_state
        if bind_time is not None:
            self.bind_time = bind_time
        if client_name is not None:
            self.client_name = client_name
        if consumer_redelivery_request_allowed is not None:
            self.consumer_redelivery_request_allowed = consumer_redelivery_request_allowed
        if cut_through_acked_msg_count is not None:
            self.cut_through_acked_msg_count = cut_through_acked_msg_count
        if delivery_state is not None:
            self.delivery_state = delivery_state
        if flow_id is not None:
            self.flow_id = flow_id
        if highest_ack_pending_msg_id is not None:
            self.highest_ack_pending_msg_id = highest_ack_pending_msg_id
        if last_acked_msg_id is not None:
            self.last_acked_msg_id = last_acked_msg_id
        if lowest_ack_pending_msg_id is not None:
            self.lowest_ack_pending_msg_id = lowest_ack_pending_msg_id
        if max_unacked_msgs_exceeded_msg_count is not None:
            self.max_unacked_msgs_exceeded_msg_count = max_unacked_msgs_exceeded_msg_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if no_local_delivery is not None:
            self.no_local_delivery = no_local_delivery
        if redelivered_msg_count is not None:
            self.redelivered_msg_count = redelivered_msg_count
        if redelivery_request_count is not None:
            self.redelivery_request_count = redelivery_request_count
        if session_name is not None:
            self.session_name = session_name
        if store_and_forward_acked_msg_count is not None:
            self.store_and_forward_acked_msg_count = store_and_forward_acked_msg_count
        if topic_endpoint_name is not None:
            self.topic_endpoint_name = topic_endpoint_name
        if unacked_msg_count is not None:
            self.unacked_msg_count = unacked_msg_count
        if used_window_size is not None:
            self.used_window_size = used_window_size
        if window_closed_count is not None:
            self.window_closed_count = window_closed_count
        if window_size is not None:
            self.window_size = window_size

    @property
    def acked_msg_count(self):
        """Gets the acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages delivered and acknowledged by the consumer.  # noqa: E501

        :return: The acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._acked_msg_count

    @acked_msg_count.setter
    def acked_msg_count(self, acked_msg_count):
        """Sets the acked_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages delivered and acknowledged by the consumer.  # noqa: E501

        :param acked_msg_count: The acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._acked_msg_count = acked_msg_count

    @property
    def activity_state(self):
        """Gets the activity_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The activity state of the Flow. The allowed values and their meaning are:  <pre> \"active-browser\" - The Flow is active as a browser. \"active-consumer\" - The Flow is active as a consumer. \"inactive\" - The Flow is inactive. </pre>   # noqa: E501

        :return: The activity_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._activity_state

    @activity_state.setter
    def activity_state(self, activity_state):
        """Sets the activity_state of this MsgVpnTopicEndpointTxFlow.

        The activity state of the Flow. The allowed values and their meaning are:  <pre> \"active-browser\" - The Flow is active as a browser. \"active-consumer\" - The Flow is active as a consumer. \"inactive\" - The Flow is inactive. </pre>   # noqa: E501

        :param activity_state: The activity_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._activity_state = activity_state

    @property
    def bind_time(self):
        """Gets the bind_time of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The timestamp of when the Flow bound to the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The bind_time of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._bind_time

    @bind_time.setter
    def bind_time(self, bind_time):
        """Sets the bind_time of this MsgVpnTopicEndpointTxFlow.

        The timestamp of when the Flow bound to the Topic Endpoint. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param bind_time: The bind_time of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._bind_time = bind_time

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The name of the Client.  # noqa: E501

        :return: The client_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnTopicEndpointTxFlow.

        The name of the Client.  # noqa: E501

        :param client_name: The client_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def consumer_redelivery_request_allowed(self):
        """Gets the consumer_redelivery_request_allowed of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        Indicates whether redelivery requests can be received as negative acknowledgements (NACKs) from the consumer. Applicable only to REST consumers.  # noqa: E501

        :return: The consumer_redelivery_request_allowed of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: bool
        """
        return self._consumer_redelivery_request_allowed

    @consumer_redelivery_request_allowed.setter
    def consumer_redelivery_request_allowed(self, consumer_redelivery_request_allowed):
        """Sets the consumer_redelivery_request_allowed of this MsgVpnTopicEndpointTxFlow.

        Indicates whether redelivery requests can be received as negative acknowledgements (NACKs) from the consumer. Applicable only to REST consumers.  # noqa: E501

        :param consumer_redelivery_request_allowed: The consumer_redelivery_request_allowed of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: bool
        """

        self._consumer_redelivery_request_allowed = consumer_redelivery_request_allowed

    @property
    def cut_through_acked_msg_count(self):
        """Gets the cut_through_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages that used cut-through delivery and are acknowledged by the consumer.  # noqa: E501

        :return: The cut_through_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._cut_through_acked_msg_count

    @cut_through_acked_msg_count.setter
    def cut_through_acked_msg_count(self, cut_through_acked_msg_count):
        """Sets the cut_through_acked_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages that used cut-through delivery and are acknowledged by the consumer.  # noqa: E501

        :param cut_through_acked_msg_count: The cut_through_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._cut_through_acked_msg_count = cut_through_acked_msg_count

    @property
    def delivery_state(self):
        """Gets the delivery_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The delivery state of the Flow. The allowed values and their meaning are:  <pre> \"closed\" - The Flow is unbound. \"opened\" - The Flow is bound but inactive. \"unbinding\" - The Flow received an unbind request. \"handshaking\" - The Flow is handshaking to become active. \"deliver-cut-through\" - The Flow is streaming messages using direct+guaranteed delivery. \"deliver-from-input-stream\" - The Flow is streaming messages using guaranteed delivery. \"deliver-from-memory\" - The Flow throttled causing message delivery from memory (RAM). \"deliver-from-spool\" - The Flow stalled causing message delivery from spool (ADB or disk). </pre>   # noqa: E501

        :return: The delivery_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._delivery_state

    @delivery_state.setter
    def delivery_state(self, delivery_state):
        """Sets the delivery_state of this MsgVpnTopicEndpointTxFlow.

        The delivery state of the Flow. The allowed values and their meaning are:  <pre> \"closed\" - The Flow is unbound. \"opened\" - The Flow is bound but inactive. \"unbinding\" - The Flow received an unbind request. \"handshaking\" - The Flow is handshaking to become active. \"deliver-cut-through\" - The Flow is streaming messages using direct+guaranteed delivery. \"deliver-from-input-stream\" - The Flow is streaming messages using guaranteed delivery. \"deliver-from-memory\" - The Flow throttled causing message delivery from memory (RAM). \"deliver-from-spool\" - The Flow stalled causing message delivery from spool (ADB or disk). </pre>   # noqa: E501

        :param delivery_state: The delivery_state of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._delivery_state = delivery_state

    @property
    def flow_id(self):
        """Gets the flow_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The identifier (ID) of the Flow.  # noqa: E501

        :return: The flow_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        """Sets the flow_id of this MsgVpnTopicEndpointTxFlow.

        The identifier (ID) of the Flow.  # noqa: E501

        :param flow_id: The flow_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._flow_id = flow_id

    @property
    def highest_ack_pending_msg_id(self):
        """Gets the highest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The highest identifier (ID) of message transmitted and waiting for acknowledgement.  # noqa: E501

        :return: The highest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._highest_ack_pending_msg_id

    @highest_ack_pending_msg_id.setter
    def highest_ack_pending_msg_id(self, highest_ack_pending_msg_id):
        """Sets the highest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.

        The highest identifier (ID) of message transmitted and waiting for acknowledgement.  # noqa: E501

        :param highest_ack_pending_msg_id: The highest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._highest_ack_pending_msg_id = highest_ack_pending_msg_id

    @property
    def last_acked_msg_id(self):
        """Gets the last_acked_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The identifier (ID) of the last message transmitted and acknowledged by the consumer.  # noqa: E501

        :return: The last_acked_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._last_acked_msg_id

    @last_acked_msg_id.setter
    def last_acked_msg_id(self, last_acked_msg_id):
        """Sets the last_acked_msg_id of this MsgVpnTopicEndpointTxFlow.

        The identifier (ID) of the last message transmitted and acknowledged by the consumer.  # noqa: E501

        :param last_acked_msg_id: The last_acked_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._last_acked_msg_id = last_acked_msg_id

    @property
    def lowest_ack_pending_msg_id(self):
        """Gets the lowest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The lowest identifier (ID) of message transmitted and waiting for acknowledgement.  # noqa: E501

        :return: The lowest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._lowest_ack_pending_msg_id

    @lowest_ack_pending_msg_id.setter
    def lowest_ack_pending_msg_id(self, lowest_ack_pending_msg_id):
        """Sets the lowest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.

        The lowest identifier (ID) of message transmitted and waiting for acknowledgement.  # noqa: E501

        :param lowest_ack_pending_msg_id: The lowest_ack_pending_msg_id of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._lowest_ack_pending_msg_id = lowest_ack_pending_msg_id

    @property
    def max_unacked_msgs_exceeded_msg_count(self):
        """Gets the max_unacked_msgs_exceeded_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages that exceeded the maximum number of delivered unacknowledged messages.  # noqa: E501

        :return: The max_unacked_msgs_exceeded_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._max_unacked_msgs_exceeded_msg_count

    @max_unacked_msgs_exceeded_msg_count.setter
    def max_unacked_msgs_exceeded_msg_count(self, max_unacked_msgs_exceeded_msg_count):
        """Sets the max_unacked_msgs_exceeded_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages that exceeded the maximum number of delivered unacknowledged messages.  # noqa: E501

        :param max_unacked_msgs_exceeded_msg_count: The max_unacked_msgs_exceeded_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._max_unacked_msgs_exceeded_msg_count = max_unacked_msgs_exceeded_msg_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnTopicEndpointTxFlow.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def no_local_delivery(self):
        """Gets the no_local_delivery of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        Indicates whether not to deliver messages to a consumer that published them.  # noqa: E501

        :return: The no_local_delivery of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: bool
        """
        return self._no_local_delivery

    @no_local_delivery.setter
    def no_local_delivery(self, no_local_delivery):
        """Sets the no_local_delivery of this MsgVpnTopicEndpointTxFlow.

        Indicates whether not to deliver messages to a consumer that published them.  # noqa: E501

        :param no_local_delivery: The no_local_delivery of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: bool
        """

        self._no_local_delivery = no_local_delivery

    @property
    def redelivered_msg_count(self):
        """Gets the redelivered_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages that were redelivered.  # noqa: E501

        :return: The redelivered_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._redelivered_msg_count

    @redelivered_msg_count.setter
    def redelivered_msg_count(self, redelivered_msg_count):
        """Sets the redelivered_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages that were redelivered.  # noqa: E501

        :param redelivered_msg_count: The redelivered_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._redelivered_msg_count = redelivered_msg_count

    @property
    def redelivery_request_count(self):
        """Gets the redelivery_request_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of consumer requests via negative acknowledgements (NACKs) to redeliver guaranteed messages.  # noqa: E501

        :return: The redelivery_request_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._redelivery_request_count

    @redelivery_request_count.setter
    def redelivery_request_count(self, redelivery_request_count):
        """Sets the redelivery_request_count of this MsgVpnTopicEndpointTxFlow.

        The number of consumer requests via negative acknowledgements (NACKs) to redeliver guaranteed messages.  # noqa: E501

        :param redelivery_request_count: The redelivery_request_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._redelivery_request_count = redelivery_request_count

    @property
    def session_name(self):
        """Gets the session_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The name of the Transacted Session for the Flow.  # noqa: E501

        :return: The session_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._session_name

    @session_name.setter
    def session_name(self, session_name):
        """Sets the session_name of this MsgVpnTopicEndpointTxFlow.

        The name of the Transacted Session for the Flow.  # noqa: E501

        :param session_name: The session_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._session_name = session_name

    @property
    def store_and_forward_acked_msg_count(self):
        """Gets the store_and_forward_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages that used store and forward delivery and are acknowledged by the consumer.  # noqa: E501

        :return: The store_and_forward_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._store_and_forward_acked_msg_count

    @store_and_forward_acked_msg_count.setter
    def store_and_forward_acked_msg_count(self, store_and_forward_acked_msg_count):
        """Sets the store_and_forward_acked_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages that used store and forward delivery and are acknowledged by the consumer.  # noqa: E501

        :param store_and_forward_acked_msg_count: The store_and_forward_acked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._store_and_forward_acked_msg_count = store_and_forward_acked_msg_count

    @property
    def topic_endpoint_name(self):
        """Gets the topic_endpoint_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The name of the Topic Endpoint.  # noqa: E501

        :return: The topic_endpoint_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: str
        """
        return self._topic_endpoint_name

    @topic_endpoint_name.setter
    def topic_endpoint_name(self, topic_endpoint_name):
        """Sets the topic_endpoint_name of this MsgVpnTopicEndpointTxFlow.

        The name of the Topic Endpoint.  # noqa: E501

        :param topic_endpoint_name: The topic_endpoint_name of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: str
        """

        self._topic_endpoint_name = topic_endpoint_name

    @property
    def unacked_msg_count(self):
        """Gets the unacked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages delivered but not yet acknowledged by the consumer.  # noqa: E501

        :return: The unacked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._unacked_msg_count

    @unacked_msg_count.setter
    def unacked_msg_count(self, unacked_msg_count):
        """Sets the unacked_msg_count of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages delivered but not yet acknowledged by the consumer.  # noqa: E501

        :param unacked_msg_count: The unacked_msg_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._unacked_msg_count = unacked_msg_count

    @property
    def used_window_size(self):
        """Gets the used_window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of guaranteed messages using the available window size.  # noqa: E501

        :return: The used_window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._used_window_size

    @used_window_size.setter
    def used_window_size(self, used_window_size):
        """Sets the used_window_size of this MsgVpnTopicEndpointTxFlow.

        The number of guaranteed messages using the available window size.  # noqa: E501

        :param used_window_size: The used_window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._used_window_size = used_window_size

    @property
    def window_closed_count(self):
        """Gets the window_closed_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of times the window for guaranteed messages was filled and closed before an acknowledgement was received.  # noqa: E501

        :return: The window_closed_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._window_closed_count

    @window_closed_count.setter
    def window_closed_count(self, window_closed_count):
        """Sets the window_closed_count of this MsgVpnTopicEndpointTxFlow.

        The number of times the window for guaranteed messages was filled and closed before an acknowledgement was received.  # noqa: E501

        :param window_closed_count: The window_closed_count of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._window_closed_count = window_closed_count

    @property
    def window_size(self):
        """Gets the window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501

        The number of outstanding guaranteed messages that can be transmitted over the Flow before an acknowledgement is received.  # noqa: E501

        :return: The window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :rtype: int
        """
        return self._window_size

    @window_size.setter
    def window_size(self, window_size):
        """Sets the window_size of this MsgVpnTopicEndpointTxFlow.

        The number of outstanding guaranteed messages that can be transmitted over the Flow before an acknowledgement is received.  # noqa: E501

        :param window_size: The window_size of this MsgVpnTopicEndpointTxFlow.  # noqa: E501
        :type: int
        """

        self._window_size = window_size

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
        if issubclass(MsgVpnTopicEndpointTxFlow, dict):
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
        if not isinstance(other, MsgVpnTopicEndpointTxFlow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
