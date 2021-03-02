# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.16
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnDistributedCacheClusterInstance(object):
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
        'auto_start_enabled': 'bool',
        'average_data_rx_byte_peak_rate': 'int',
        'average_data_rx_byte_rate': 'int',
        'average_data_rx_msg_peak_rate': 'int',
        'average_data_rx_msg_rate': 'int',
        'average_data_tx_msg_peak_rate': 'int',
        'average_data_tx_msg_rate': 'int',
        'average_request_rx_peak_rate': 'int',
        'average_request_rx_rate': 'int',
        'cache_name': 'str',
        'cluster_name': 'str',
        'counter': 'MsgVpnDistributedCacheClusterInstanceCounter',
        'data_rx_byte_peak_rate': 'int',
        'data_rx_byte_rate': 'int',
        'data_rx_msg_peak_rate': 'int',
        'data_rx_msg_rate': 'int',
        'data_tx_msg_peak_rate': 'int',
        'data_tx_msg_rate': 'int',
        'enabled': 'bool',
        'instance_name': 'str',
        'last_registered_time': 'int',
        'last_rx_heartbeat_time': 'int',
        'last_rx_set_lost_msg_time': 'int',
        'last_stopped_reason': 'str',
        'last_stopped_time': 'int',
        'last_tx_clear_lost_msg_time': 'int',
        'memory_usage': 'int',
        'msg_count': 'int',
        'msg_peak_count': 'int',
        'msg_vpn_name': 'str',
        'msgs_lost': 'bool',
        'rate': 'MsgVpnDistributedCacheClusterInstanceRate',
        'request_queue_depth_count': 'int',
        'request_queue_depth_peak_count': 'int',
        'request_rx_peak_rate': 'int',
        'request_rx_rate': 'int',
        'state': 'str',
        'stop_on_lost_msg_enabled': 'bool',
        'topic_count': 'int',
        'topic_peak_count': 'int'
    }

    attribute_map = {
        'auto_start_enabled': 'autoStartEnabled',
        'average_data_rx_byte_peak_rate': 'averageDataRxBytePeakRate',
        'average_data_rx_byte_rate': 'averageDataRxByteRate',
        'average_data_rx_msg_peak_rate': 'averageDataRxMsgPeakRate',
        'average_data_rx_msg_rate': 'averageDataRxMsgRate',
        'average_data_tx_msg_peak_rate': 'averageDataTxMsgPeakRate',
        'average_data_tx_msg_rate': 'averageDataTxMsgRate',
        'average_request_rx_peak_rate': 'averageRequestRxPeakRate',
        'average_request_rx_rate': 'averageRequestRxRate',
        'cache_name': 'cacheName',
        'cluster_name': 'clusterName',
        'counter': 'counter',
        'data_rx_byte_peak_rate': 'dataRxBytePeakRate',
        'data_rx_byte_rate': 'dataRxByteRate',
        'data_rx_msg_peak_rate': 'dataRxMsgPeakRate',
        'data_rx_msg_rate': 'dataRxMsgRate',
        'data_tx_msg_peak_rate': 'dataTxMsgPeakRate',
        'data_tx_msg_rate': 'dataTxMsgRate',
        'enabled': 'enabled',
        'instance_name': 'instanceName',
        'last_registered_time': 'lastRegisteredTime',
        'last_rx_heartbeat_time': 'lastRxHeartbeatTime',
        'last_rx_set_lost_msg_time': 'lastRxSetLostMsgTime',
        'last_stopped_reason': 'lastStoppedReason',
        'last_stopped_time': 'lastStoppedTime',
        'last_tx_clear_lost_msg_time': 'lastTxClearLostMsgTime',
        'memory_usage': 'memoryUsage',
        'msg_count': 'msgCount',
        'msg_peak_count': 'msgPeakCount',
        'msg_vpn_name': 'msgVpnName',
        'msgs_lost': 'msgsLost',
        'rate': 'rate',
        'request_queue_depth_count': 'requestQueueDepthCount',
        'request_queue_depth_peak_count': 'requestQueueDepthPeakCount',
        'request_rx_peak_rate': 'requestRxPeakRate',
        'request_rx_rate': 'requestRxRate',
        'state': 'state',
        'stop_on_lost_msg_enabled': 'stopOnLostMsgEnabled',
        'topic_count': 'topicCount',
        'topic_peak_count': 'topicPeakCount'
    }

    def __init__(self, auto_start_enabled=None, average_data_rx_byte_peak_rate=None, average_data_rx_byte_rate=None, average_data_rx_msg_peak_rate=None, average_data_rx_msg_rate=None, average_data_tx_msg_peak_rate=None, average_data_tx_msg_rate=None, average_request_rx_peak_rate=None, average_request_rx_rate=None, cache_name=None, cluster_name=None, counter=None, data_rx_byte_peak_rate=None, data_rx_byte_rate=None, data_rx_msg_peak_rate=None, data_rx_msg_rate=None, data_tx_msg_peak_rate=None, data_tx_msg_rate=None, enabled=None, instance_name=None, last_registered_time=None, last_rx_heartbeat_time=None, last_rx_set_lost_msg_time=None, last_stopped_reason=None, last_stopped_time=None, last_tx_clear_lost_msg_time=None, memory_usage=None, msg_count=None, msg_peak_count=None, msg_vpn_name=None, msgs_lost=None, rate=None, request_queue_depth_count=None, request_queue_depth_peak_count=None, request_rx_peak_rate=None, request_rx_rate=None, state=None, stop_on_lost_msg_enabled=None, topic_count=None, topic_peak_count=None):  # noqa: E501
        """MsgVpnDistributedCacheClusterInstance - a model defined in Swagger"""  # noqa: E501

        self._auto_start_enabled = None
        self._average_data_rx_byte_peak_rate = None
        self._average_data_rx_byte_rate = None
        self._average_data_rx_msg_peak_rate = None
        self._average_data_rx_msg_rate = None
        self._average_data_tx_msg_peak_rate = None
        self._average_data_tx_msg_rate = None
        self._average_request_rx_peak_rate = None
        self._average_request_rx_rate = None
        self._cache_name = None
        self._cluster_name = None
        self._counter = None
        self._data_rx_byte_peak_rate = None
        self._data_rx_byte_rate = None
        self._data_rx_msg_peak_rate = None
        self._data_rx_msg_rate = None
        self._data_tx_msg_peak_rate = None
        self._data_tx_msg_rate = None
        self._enabled = None
        self._instance_name = None
        self._last_registered_time = None
        self._last_rx_heartbeat_time = None
        self._last_rx_set_lost_msg_time = None
        self._last_stopped_reason = None
        self._last_stopped_time = None
        self._last_tx_clear_lost_msg_time = None
        self._memory_usage = None
        self._msg_count = None
        self._msg_peak_count = None
        self._msg_vpn_name = None
        self._msgs_lost = None
        self._rate = None
        self._request_queue_depth_count = None
        self._request_queue_depth_peak_count = None
        self._request_rx_peak_rate = None
        self._request_rx_rate = None
        self._state = None
        self._stop_on_lost_msg_enabled = None
        self._topic_count = None
        self._topic_peak_count = None
        self.discriminator = None

        if auto_start_enabled is not None:
            self.auto_start_enabled = auto_start_enabled
        if average_data_rx_byte_peak_rate is not None:
            self.average_data_rx_byte_peak_rate = average_data_rx_byte_peak_rate
        if average_data_rx_byte_rate is not None:
            self.average_data_rx_byte_rate = average_data_rx_byte_rate
        if average_data_rx_msg_peak_rate is not None:
            self.average_data_rx_msg_peak_rate = average_data_rx_msg_peak_rate
        if average_data_rx_msg_rate is not None:
            self.average_data_rx_msg_rate = average_data_rx_msg_rate
        if average_data_tx_msg_peak_rate is not None:
            self.average_data_tx_msg_peak_rate = average_data_tx_msg_peak_rate
        if average_data_tx_msg_rate is not None:
            self.average_data_tx_msg_rate = average_data_tx_msg_rate
        if average_request_rx_peak_rate is not None:
            self.average_request_rx_peak_rate = average_request_rx_peak_rate
        if average_request_rx_rate is not None:
            self.average_request_rx_rate = average_request_rx_rate
        if cache_name is not None:
            self.cache_name = cache_name
        if cluster_name is not None:
            self.cluster_name = cluster_name
        if counter is not None:
            self.counter = counter
        if data_rx_byte_peak_rate is not None:
            self.data_rx_byte_peak_rate = data_rx_byte_peak_rate
        if data_rx_byte_rate is not None:
            self.data_rx_byte_rate = data_rx_byte_rate
        if data_rx_msg_peak_rate is not None:
            self.data_rx_msg_peak_rate = data_rx_msg_peak_rate
        if data_rx_msg_rate is not None:
            self.data_rx_msg_rate = data_rx_msg_rate
        if data_tx_msg_peak_rate is not None:
            self.data_tx_msg_peak_rate = data_tx_msg_peak_rate
        if data_tx_msg_rate is not None:
            self.data_tx_msg_rate = data_tx_msg_rate
        if enabled is not None:
            self.enabled = enabled
        if instance_name is not None:
            self.instance_name = instance_name
        if last_registered_time is not None:
            self.last_registered_time = last_registered_time
        if last_rx_heartbeat_time is not None:
            self.last_rx_heartbeat_time = last_rx_heartbeat_time
        if last_rx_set_lost_msg_time is not None:
            self.last_rx_set_lost_msg_time = last_rx_set_lost_msg_time
        if last_stopped_reason is not None:
            self.last_stopped_reason = last_stopped_reason
        if last_stopped_time is not None:
            self.last_stopped_time = last_stopped_time
        if last_tx_clear_lost_msg_time is not None:
            self.last_tx_clear_lost_msg_time = last_tx_clear_lost_msg_time
        if memory_usage is not None:
            self.memory_usage = memory_usage
        if msg_count is not None:
            self.msg_count = msg_count
        if msg_peak_count is not None:
            self.msg_peak_count = msg_peak_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if msgs_lost is not None:
            self.msgs_lost = msgs_lost
        if rate is not None:
            self.rate = rate
        if request_queue_depth_count is not None:
            self.request_queue_depth_count = request_queue_depth_count
        if request_queue_depth_peak_count is not None:
            self.request_queue_depth_peak_count = request_queue_depth_peak_count
        if request_rx_peak_rate is not None:
            self.request_rx_peak_rate = request_rx_peak_rate
        if request_rx_rate is not None:
            self.request_rx_rate = request_rx_rate
        if state is not None:
            self.state = state
        if stop_on_lost_msg_enabled is not None:
            self.stop_on_lost_msg_enabled = stop_on_lost_msg_enabled
        if topic_count is not None:
            self.topic_count = topic_count
        if topic_peak_count is not None:
            self.topic_peak_count = topic_peak_count

    @property
    def auto_start_enabled(self):
        """Gets the auto_start_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        Indicates whether auto-start for the Cache Instance is enabled, and the Cache Instance will automatically attempt to transition from the Stopped operational state to Up whenever it restarts or reconnects to the message broker.  # noqa: E501

        :return: The auto_start_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: bool
        """
        return self._auto_start_enabled

    @auto_start_enabled.setter
    def auto_start_enabled(self, auto_start_enabled):
        """Sets the auto_start_enabled of this MsgVpnDistributedCacheClusterInstance.

        Indicates whether auto-start for the Cache Instance is enabled, and the Cache Instance will automatically attempt to transition from the Stopped operational state to Up whenever it restarts or reconnects to the message broker.  # noqa: E501

        :param auto_start_enabled: The auto_start_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: bool
        """

        self._auto_start_enabled = auto_start_enabled

    @property
    def average_data_rx_byte_peak_rate(self):
        """Gets the average_data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The peak of the one minute average of the data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_rx_byte_peak_rate

    @average_data_rx_byte_peak_rate.setter
    def average_data_rx_byte_peak_rate(self, average_data_rx_byte_peak_rate):
        """Sets the average_data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The peak of the one minute average of the data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param average_data_rx_byte_peak_rate: The average_data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_rx_byte_peak_rate = average_data_rx_byte_peak_rate

    @property
    def average_data_rx_byte_rate(self):
        """Gets the average_data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The one minute average of the data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_rx_byte_rate

    @average_data_rx_byte_rate.setter
    def average_data_rx_byte_rate(self, average_data_rx_byte_rate):
        """Sets the average_data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.

        The one minute average of the data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param average_data_rx_byte_rate: The average_data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_rx_byte_rate = average_data_rx_byte_rate

    @property
    def average_data_rx_msg_peak_rate(self):
        """Gets the average_data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The peak of the one minute average of the data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_rx_msg_peak_rate

    @average_data_rx_msg_peak_rate.setter
    def average_data_rx_msg_peak_rate(self, average_data_rx_msg_peak_rate):
        """Sets the average_data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The peak of the one minute average of the data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_data_rx_msg_peak_rate: The average_data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_rx_msg_peak_rate = average_data_rx_msg_peak_rate

    @property
    def average_data_rx_msg_rate(self):
        """Gets the average_data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The one minute average of the data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_rx_msg_rate

    @average_data_rx_msg_rate.setter
    def average_data_rx_msg_rate(self, average_data_rx_msg_rate):
        """Sets the average_data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.

        The one minute average of the data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_data_rx_msg_rate: The average_data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_rx_msg_rate = average_data_rx_msg_rate

    @property
    def average_data_tx_msg_peak_rate(self):
        """Gets the average_data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The peak of the one minute average of the data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_tx_msg_peak_rate

    @average_data_tx_msg_peak_rate.setter
    def average_data_tx_msg_peak_rate(self, average_data_tx_msg_peak_rate):
        """Sets the average_data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The peak of the one minute average of the data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_data_tx_msg_peak_rate: The average_data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_tx_msg_peak_rate = average_data_tx_msg_peak_rate

    @property
    def average_data_tx_msg_rate(self):
        """Gets the average_data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The one minute average of the data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The average_data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_data_tx_msg_rate

    @average_data_tx_msg_rate.setter
    def average_data_tx_msg_rate(self, average_data_tx_msg_rate):
        """Sets the average_data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.

        The one minute average of the data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param average_data_tx_msg_rate: The average_data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_data_tx_msg_rate = average_data_tx_msg_rate

    @property
    def average_request_rx_peak_rate(self):
        """Gets the average_request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The peak of the one minute average of the request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :return: The average_request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_request_rx_peak_rate

    @average_request_rx_peak_rate.setter
    def average_request_rx_peak_rate(self, average_request_rx_peak_rate):
        """Sets the average_request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The peak of the one minute average of the request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :param average_request_rx_peak_rate: The average_request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_request_rx_peak_rate = average_request_rx_peak_rate

    @property
    def average_request_rx_rate(self):
        """Gets the average_request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The one minute average of the request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :return: The average_request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._average_request_rx_rate

    @average_request_rx_rate.setter
    def average_request_rx_rate(self, average_request_rx_rate):
        """Sets the average_request_rx_rate of this MsgVpnDistributedCacheClusterInstance.

        The one minute average of the request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :param average_request_rx_rate: The average_request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._average_request_rx_rate = average_request_rx_rate

    @property
    def cache_name(self):
        """Gets the cache_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The name of the Distributed Cache.  # noqa: E501

        :return: The cache_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._cache_name

    @cache_name.setter
    def cache_name(self, cache_name):
        """Sets the cache_name of this MsgVpnDistributedCacheClusterInstance.

        The name of the Distributed Cache.  # noqa: E501

        :param cache_name: The cache_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._cache_name = cache_name

    @property
    def cluster_name(self):
        """Gets the cluster_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The name of the Cache Cluster.  # noqa: E501

        :return: The cluster_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name):
        """Sets the cluster_name of this MsgVpnDistributedCacheClusterInstance.

        The name of the Cache Cluster.  # noqa: E501

        :param cluster_name: The cluster_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._cluster_name = cluster_name

    @property
    def counter(self):
        """Gets the counter of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501


        :return: The counter of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: MsgVpnDistributedCacheClusterInstanceCounter
        """
        return self._counter

    @counter.setter
    def counter(self, counter):
        """Sets the counter of this MsgVpnDistributedCacheClusterInstance.


        :param counter: The counter of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: MsgVpnDistributedCacheClusterInstanceCounter
        """

        self._counter = counter

    @property
    def data_rx_byte_peak_rate(self):
        """Gets the data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message peak rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_byte_peak_rate

    @data_rx_byte_peak_rate.setter
    def data_rx_byte_peak_rate(self, data_rx_byte_peak_rate):
        """Sets the data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message peak rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param data_rx_byte_peak_rate: The data_rx_byte_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_rx_byte_peak_rate = data_rx_byte_peak_rate

    @property
    def data_rx_byte_rate(self):
        """Gets the data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :return: The data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_byte_rate

    @data_rx_byte_rate.setter
    def data_rx_byte_rate(self, data_rx_byte_rate):
        """Sets the data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message rate received by the Cache Instance, in bytes per second (B/sec). Available since 2.13.  # noqa: E501

        :param data_rx_byte_rate: The data_rx_byte_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_rx_byte_rate = data_rx_byte_rate

    @property
    def data_rx_msg_peak_rate(self):
        """Gets the data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message peak rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_msg_peak_rate

    @data_rx_msg_peak_rate.setter
    def data_rx_msg_peak_rate(self, data_rx_msg_peak_rate):
        """Sets the data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message peak rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param data_rx_msg_peak_rate: The data_rx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_rx_msg_peak_rate = data_rx_msg_peak_rate

    @property
    def data_rx_msg_rate(self):
        """Gets the data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_rx_msg_rate

    @data_rx_msg_rate.setter
    def data_rx_msg_rate(self, data_rx_msg_rate):
        """Sets the data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message rate received by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param data_rx_msg_rate: The data_rx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_rx_msg_rate = data_rx_msg_rate

    @property
    def data_tx_msg_peak_rate(self):
        """Gets the data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message peak rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_msg_peak_rate

    @data_tx_msg_peak_rate.setter
    def data_tx_msg_peak_rate(self, data_tx_msg_peak_rate):
        """Sets the data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message peak rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param data_tx_msg_peak_rate: The data_tx_msg_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_tx_msg_peak_rate = data_tx_msg_peak_rate

    @property
    def data_tx_msg_rate(self):
        """Gets the data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :return: The data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._data_tx_msg_rate

    @data_tx_msg_rate.setter
    def data_tx_msg_rate(self, data_tx_msg_rate):
        """Sets the data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.

        The data message rate transmitted by the Cache Instance, in messages per second (msg/sec). Available since 2.13.  # noqa: E501

        :param data_tx_msg_rate: The data_tx_msg_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._data_tx_msg_rate = data_tx_msg_rate

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        Indicates whether the Cache Instance is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnDistributedCacheClusterInstance.

        Indicates whether the Cache Instance is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def instance_name(self):
        """Gets the instance_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The name of the Cache Instance.  # noqa: E501

        :return: The instance_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this MsgVpnDistributedCacheClusterInstance.

        The name of the Cache Instance.  # noqa: E501

        :param instance_name: The instance_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._instance_name = instance_name

    @property
    def last_registered_time(self):
        """Gets the last_registered_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The timestamp of when the Cache Instance last registered with the message broker. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_registered_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._last_registered_time

    @last_registered_time.setter
    def last_registered_time(self, last_registered_time):
        """Sets the last_registered_time of this MsgVpnDistributedCacheClusterInstance.

        The timestamp of when the Cache Instance last registered with the message broker. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_registered_time: The last_registered_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._last_registered_time = last_registered_time

    @property
    def last_rx_heartbeat_time(self):
        """Gets the last_rx_heartbeat_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The timestamp of the last heartbeat message received from the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_rx_heartbeat_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._last_rx_heartbeat_time

    @last_rx_heartbeat_time.setter
    def last_rx_heartbeat_time(self, last_rx_heartbeat_time):
        """Sets the last_rx_heartbeat_time of this MsgVpnDistributedCacheClusterInstance.

        The timestamp of the last heartbeat message received from the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_rx_heartbeat_time: The last_rx_heartbeat_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._last_rx_heartbeat_time = last_rx_heartbeat_time

    @property
    def last_rx_set_lost_msg_time(self):
        """Gets the last_rx_set_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The timestamp of the last request for setting the lost message indication received from the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_rx_set_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._last_rx_set_lost_msg_time

    @last_rx_set_lost_msg_time.setter
    def last_rx_set_lost_msg_time(self, last_rx_set_lost_msg_time):
        """Sets the last_rx_set_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.

        The timestamp of the last request for setting the lost message indication received from the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_rx_set_lost_msg_time: The last_rx_set_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._last_rx_set_lost_msg_time = last_rx_set_lost_msg_time

    @property
    def last_stopped_reason(self):
        """Gets the last_stopped_reason of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The reason why the Cache Instance was last stopped.  # noqa: E501

        :return: The last_stopped_reason of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._last_stopped_reason

    @last_stopped_reason.setter
    def last_stopped_reason(self, last_stopped_reason):
        """Sets the last_stopped_reason of this MsgVpnDistributedCacheClusterInstance.

        The reason why the Cache Instance was last stopped.  # noqa: E501

        :param last_stopped_reason: The last_stopped_reason of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._last_stopped_reason = last_stopped_reason

    @property
    def last_stopped_time(self):
        """Gets the last_stopped_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The timestamp of when the Cache Instance was last stopped. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_stopped_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._last_stopped_time

    @last_stopped_time.setter
    def last_stopped_time(self, last_stopped_time):
        """Sets the last_stopped_time of this MsgVpnDistributedCacheClusterInstance.

        The timestamp of when the Cache Instance was last stopped. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_stopped_time: The last_stopped_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._last_stopped_time = last_stopped_time

    @property
    def last_tx_clear_lost_msg_time(self):
        """Gets the last_tx_clear_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The timestamp of the last request for clearing the lost message indication transmitted to the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_tx_clear_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._last_tx_clear_lost_msg_time

    @last_tx_clear_lost_msg_time.setter
    def last_tx_clear_lost_msg_time(self, last_tx_clear_lost_msg_time):
        """Sets the last_tx_clear_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.

        The timestamp of the last request for clearing the lost message indication transmitted to the Cache Instance. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_tx_clear_lost_msg_time: The last_tx_clear_lost_msg_time of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._last_tx_clear_lost_msg_time = last_tx_clear_lost_msg_time

    @property
    def memory_usage(self):
        """Gets the memory_usage of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The memory usage of the Cache Instance, in megabytes (MB).  # noqa: E501

        :return: The memory_usage of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._memory_usage

    @memory_usage.setter
    def memory_usage(self, memory_usage):
        """Sets the memory_usage of this MsgVpnDistributedCacheClusterInstance.

        The memory usage of the Cache Instance, in megabytes (MB).  # noqa: E501

        :param memory_usage: The memory_usage of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._memory_usage = memory_usage

    @property
    def msg_count(self):
        """Gets the msg_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The number of messages cached for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The msg_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._msg_count

    @msg_count.setter
    def msg_count(self, msg_count):
        """Sets the msg_count of this MsgVpnDistributedCacheClusterInstance.

        The number of messages cached for the Cache Instance. Available since 2.13.  # noqa: E501

        :param msg_count: The msg_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._msg_count = msg_count

    @property
    def msg_peak_count(self):
        """Gets the msg_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The number of messages cached peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The msg_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._msg_peak_count

    @msg_peak_count.setter
    def msg_peak_count(self, msg_peak_count):
        """Sets the msg_peak_count of this MsgVpnDistributedCacheClusterInstance.

        The number of messages cached peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :param msg_peak_count: The msg_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._msg_peak_count = msg_peak_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnDistributedCacheClusterInstance.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def msgs_lost(self):
        """Gets the msgs_lost of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        Indicates whether one or more messages were lost by the Cache Instance.  # noqa: E501

        :return: The msgs_lost of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: bool
        """
        return self._msgs_lost

    @msgs_lost.setter
    def msgs_lost(self, msgs_lost):
        """Sets the msgs_lost of this MsgVpnDistributedCacheClusterInstance.

        Indicates whether one or more messages were lost by the Cache Instance.  # noqa: E501

        :param msgs_lost: The msgs_lost of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: bool
        """

        self._msgs_lost = msgs_lost

    @property
    def rate(self):
        """Gets the rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501


        :return: The rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: MsgVpnDistributedCacheClusterInstanceRate
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this MsgVpnDistributedCacheClusterInstance.


        :param rate: The rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: MsgVpnDistributedCacheClusterInstanceRate
        """

        self._rate = rate

    @property
    def request_queue_depth_count(self):
        """Gets the request_queue_depth_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The received request message queue depth for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The request_queue_depth_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._request_queue_depth_count

    @request_queue_depth_count.setter
    def request_queue_depth_count(self, request_queue_depth_count):
        """Sets the request_queue_depth_count of this MsgVpnDistributedCacheClusterInstance.

        The received request message queue depth for the Cache Instance. Available since 2.13.  # noqa: E501

        :param request_queue_depth_count: The request_queue_depth_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._request_queue_depth_count = request_queue_depth_count

    @property
    def request_queue_depth_peak_count(self):
        """Gets the request_queue_depth_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The received request message queue depth peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The request_queue_depth_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._request_queue_depth_peak_count

    @request_queue_depth_peak_count.setter
    def request_queue_depth_peak_count(self, request_queue_depth_peak_count):
        """Sets the request_queue_depth_peak_count of this MsgVpnDistributedCacheClusterInstance.

        The received request message queue depth peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :param request_queue_depth_peak_count: The request_queue_depth_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._request_queue_depth_peak_count = request_queue_depth_peak_count

    @property
    def request_rx_peak_rate(self):
        """Gets the request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The request peak rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :return: The request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._request_rx_peak_rate

    @request_rx_peak_rate.setter
    def request_rx_peak_rate(self, request_rx_peak_rate):
        """Sets the request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.

        The request peak rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :param request_rx_peak_rate: The request_rx_peak_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._request_rx_peak_rate = request_rx_peak_rate

    @property
    def request_rx_rate(self):
        """Gets the request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :return: The request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._request_rx_rate

    @request_rx_rate.setter
    def request_rx_rate(self, request_rx_rate):
        """Sets the request_rx_rate of this MsgVpnDistributedCacheClusterInstance.

        The request rate received by the Cache Instance, in requests per second (req/sec). Available since 2.13.  # noqa: E501

        :param request_rx_rate: The request_rx_rate of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._request_rx_rate = request_rx_rate

    @property
    def state(self):
        """Gets the state of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The operational state of the Cache Instance. The allowed values and their meaning are:  <pre> \"invalid\" - The Cache Instance state is invalid. \"down\" - The Cache Instance is operationally down. \"stopped\" - The Cache Instance has stopped processing cache requests. \"stopped-lost-msg\" - The Cache Instance has stopped due to a lost message. \"register\" - The Cache Instance is registering with the broker. \"config-sync\" - The Cache Instance is synchronizing its configuration with the broker. \"cluster-sync\" - The Cache Instance is synchronizing its messages with the Cache Cluster. \"up\" - The Cache Instance is operationally up. \"backup\" - The Cache Instance is backing up its messages to disk. \"restore\" - The Cache Instance is restoring its messages from disk. \"not-available\" - The Cache Instance state is not available. </pre>   # noqa: E501

        :return: The state of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this MsgVpnDistributedCacheClusterInstance.

        The operational state of the Cache Instance. The allowed values and their meaning are:  <pre> \"invalid\" - The Cache Instance state is invalid. \"down\" - The Cache Instance is operationally down. \"stopped\" - The Cache Instance has stopped processing cache requests. \"stopped-lost-msg\" - The Cache Instance has stopped due to a lost message. \"register\" - The Cache Instance is registering with the broker. \"config-sync\" - The Cache Instance is synchronizing its configuration with the broker. \"cluster-sync\" - The Cache Instance is synchronizing its messages with the Cache Cluster. \"up\" - The Cache Instance is operationally up. \"backup\" - The Cache Instance is backing up its messages to disk. \"restore\" - The Cache Instance is restoring its messages from disk. \"not-available\" - The Cache Instance state is not available. </pre>   # noqa: E501

        :param state: The state of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def stop_on_lost_msg_enabled(self):
        """Gets the stop_on_lost_msg_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        Indicates whether stop-on-lost-message is enabled, and the Cache Instance will transition to the Stopped operational state upon losing a message. When Stopped, it cannot accept or respond to cache requests, but continues to cache messages.  # noqa: E501

        :return: The stop_on_lost_msg_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: bool
        """
        return self._stop_on_lost_msg_enabled

    @stop_on_lost_msg_enabled.setter
    def stop_on_lost_msg_enabled(self, stop_on_lost_msg_enabled):
        """Sets the stop_on_lost_msg_enabled of this MsgVpnDistributedCacheClusterInstance.

        Indicates whether stop-on-lost-message is enabled, and the Cache Instance will transition to the Stopped operational state upon losing a message. When Stopped, it cannot accept or respond to cache requests, but continues to cache messages.  # noqa: E501

        :param stop_on_lost_msg_enabled: The stop_on_lost_msg_enabled of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: bool
        """

        self._stop_on_lost_msg_enabled = stop_on_lost_msg_enabled

    @property
    def topic_count(self):
        """Gets the topic_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The number of topics cached for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The topic_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._topic_count

    @topic_count.setter
    def topic_count(self, topic_count):
        """Sets the topic_count of this MsgVpnDistributedCacheClusterInstance.

        The number of topics cached for the Cache Instance. Available since 2.13.  # noqa: E501

        :param topic_count: The topic_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._topic_count = topic_count

    @property
    def topic_peak_count(self):
        """Gets the topic_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501

        The number of topics cached peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :return: The topic_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :rtype: int
        """
        return self._topic_peak_count

    @topic_peak_count.setter
    def topic_peak_count(self, topic_peak_count):
        """Sets the topic_peak_count of this MsgVpnDistributedCacheClusterInstance.

        The number of topics cached peak for the Cache Instance. Available since 2.13.  # noqa: E501

        :param topic_peak_count: The topic_peak_count of this MsgVpnDistributedCacheClusterInstance.  # noqa: E501
        :type: int
        """

        self._topic_peak_count = topic_peak_count

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
        if issubclass(MsgVpnDistributedCacheClusterInstance, dict):
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
        if not isinstance(other, MsgVpnDistributedCacheClusterInstance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
