# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.14
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnDistributedCacheCluster(object):
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
        'cache_name': 'str',
        'cluster_name': 'str',
        'deliver_to_one_override_enabled': 'bool',
        'enabled': 'bool',
        'event_data_byte_rate_threshold': 'EventThresholdByValue',
        'event_data_msg_rate_threshold': 'EventThresholdByValue',
        'event_max_memory_threshold': 'EventThresholdByPercent',
        'event_max_topics_threshold': 'EventThresholdByPercent',
        'event_request_queue_depth_threshold': 'EventThresholdByPercent',
        'event_request_rate_threshold': 'EventThresholdByValue',
        'event_response_rate_threshold': 'EventThresholdByValue',
        'global_caching_enabled': 'bool',
        'global_caching_heartbeat': 'int',
        'global_caching_topic_lifetime': 'int',
        'max_memory': 'int',
        'max_msgs_per_topic': 'int',
        'max_request_queue_depth': 'int',
        'max_topic_count': 'int',
        'msg_lifetime': 'int',
        'msg_vpn_name': 'str',
        'msgs_lost': 'bool',
        'new_topic_advertisement_enabled': 'bool'
    }

    attribute_map = {
        'cache_name': 'cacheName',
        'cluster_name': 'clusterName',
        'deliver_to_one_override_enabled': 'deliverToOneOverrideEnabled',
        'enabled': 'enabled',
        'event_data_byte_rate_threshold': 'eventDataByteRateThreshold',
        'event_data_msg_rate_threshold': 'eventDataMsgRateThreshold',
        'event_max_memory_threshold': 'eventMaxMemoryThreshold',
        'event_max_topics_threshold': 'eventMaxTopicsThreshold',
        'event_request_queue_depth_threshold': 'eventRequestQueueDepthThreshold',
        'event_request_rate_threshold': 'eventRequestRateThreshold',
        'event_response_rate_threshold': 'eventResponseRateThreshold',
        'global_caching_enabled': 'globalCachingEnabled',
        'global_caching_heartbeat': 'globalCachingHeartbeat',
        'global_caching_topic_lifetime': 'globalCachingTopicLifetime',
        'max_memory': 'maxMemory',
        'max_msgs_per_topic': 'maxMsgsPerTopic',
        'max_request_queue_depth': 'maxRequestQueueDepth',
        'max_topic_count': 'maxTopicCount',
        'msg_lifetime': 'msgLifetime',
        'msg_vpn_name': 'msgVpnName',
        'msgs_lost': 'msgsLost',
        'new_topic_advertisement_enabled': 'newTopicAdvertisementEnabled'
    }

    def __init__(self, cache_name=None, cluster_name=None, deliver_to_one_override_enabled=None, enabled=None, event_data_byte_rate_threshold=None, event_data_msg_rate_threshold=None, event_max_memory_threshold=None, event_max_topics_threshold=None, event_request_queue_depth_threshold=None, event_request_rate_threshold=None, event_response_rate_threshold=None, global_caching_enabled=None, global_caching_heartbeat=None, global_caching_topic_lifetime=None, max_memory=None, max_msgs_per_topic=None, max_request_queue_depth=None, max_topic_count=None, msg_lifetime=None, msg_vpn_name=None, msgs_lost=None, new_topic_advertisement_enabled=None):  # noqa: E501
        """MsgVpnDistributedCacheCluster - a model defined in Swagger"""  # noqa: E501

        self._cache_name = None
        self._cluster_name = None
        self._deliver_to_one_override_enabled = None
        self._enabled = None
        self._event_data_byte_rate_threshold = None
        self._event_data_msg_rate_threshold = None
        self._event_max_memory_threshold = None
        self._event_max_topics_threshold = None
        self._event_request_queue_depth_threshold = None
        self._event_request_rate_threshold = None
        self._event_response_rate_threshold = None
        self._global_caching_enabled = None
        self._global_caching_heartbeat = None
        self._global_caching_topic_lifetime = None
        self._max_memory = None
        self._max_msgs_per_topic = None
        self._max_request_queue_depth = None
        self._max_topic_count = None
        self._msg_lifetime = None
        self._msg_vpn_name = None
        self._msgs_lost = None
        self._new_topic_advertisement_enabled = None
        self.discriminator = None

        if cache_name is not None:
            self.cache_name = cache_name
        if cluster_name is not None:
            self.cluster_name = cluster_name
        if deliver_to_one_override_enabled is not None:
            self.deliver_to_one_override_enabled = deliver_to_one_override_enabled
        if enabled is not None:
            self.enabled = enabled
        if event_data_byte_rate_threshold is not None:
            self.event_data_byte_rate_threshold = event_data_byte_rate_threshold
        if event_data_msg_rate_threshold is not None:
            self.event_data_msg_rate_threshold = event_data_msg_rate_threshold
        if event_max_memory_threshold is not None:
            self.event_max_memory_threshold = event_max_memory_threshold
        if event_max_topics_threshold is not None:
            self.event_max_topics_threshold = event_max_topics_threshold
        if event_request_queue_depth_threshold is not None:
            self.event_request_queue_depth_threshold = event_request_queue_depth_threshold
        if event_request_rate_threshold is not None:
            self.event_request_rate_threshold = event_request_rate_threshold
        if event_response_rate_threshold is not None:
            self.event_response_rate_threshold = event_response_rate_threshold
        if global_caching_enabled is not None:
            self.global_caching_enabled = global_caching_enabled
        if global_caching_heartbeat is not None:
            self.global_caching_heartbeat = global_caching_heartbeat
        if global_caching_topic_lifetime is not None:
            self.global_caching_topic_lifetime = global_caching_topic_lifetime
        if max_memory is not None:
            self.max_memory = max_memory
        if max_msgs_per_topic is not None:
            self.max_msgs_per_topic = max_msgs_per_topic
        if max_request_queue_depth is not None:
            self.max_request_queue_depth = max_request_queue_depth
        if max_topic_count is not None:
            self.max_topic_count = max_topic_count
        if msg_lifetime is not None:
            self.msg_lifetime = msg_lifetime
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if msgs_lost is not None:
            self.msgs_lost = msgs_lost
        if new_topic_advertisement_enabled is not None:
            self.new_topic_advertisement_enabled = new_topic_advertisement_enabled

    @property
    def cache_name(self):
        """Gets the cache_name of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The name of the Distributed Cache.  # noqa: E501

        :return: The cache_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: str
        """
        return self._cache_name

    @cache_name.setter
    def cache_name(self, cache_name):
        """Sets the cache_name of this MsgVpnDistributedCacheCluster.

        The name of the Distributed Cache.  # noqa: E501

        :param cache_name: The cache_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: str
        """

        self._cache_name = cache_name

    @property
    def cluster_name(self):
        """Gets the cluster_name of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The name of the Cache Cluster.  # noqa: E501

        :return: The cluster_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name):
        """Sets the cluster_name of this MsgVpnDistributedCacheCluster.

        The name of the Cache Cluster.  # noqa: E501

        :param cluster_name: The cluster_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: str
        """

        self._cluster_name = cluster_name

    @property
    def deliver_to_one_override_enabled(self):
        """Gets the deliver_to_one_override_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501

        Indicates whether deliver-to-one override is enabled for the Cache Cluster.  # noqa: E501

        :return: The deliver_to_one_override_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: bool
        """
        return self._deliver_to_one_override_enabled

    @deliver_to_one_override_enabled.setter
    def deliver_to_one_override_enabled(self, deliver_to_one_override_enabled):
        """Sets the deliver_to_one_override_enabled of this MsgVpnDistributedCacheCluster.

        Indicates whether deliver-to-one override is enabled for the Cache Cluster.  # noqa: E501

        :param deliver_to_one_override_enabled: The deliver_to_one_override_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: bool
        """

        self._deliver_to_one_override_enabled = deliver_to_one_override_enabled

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501

        Indicates whether the Cache Cluster is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnDistributedCacheCluster.

        Indicates whether the Cache Cluster is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def event_data_byte_rate_threshold(self):
        """Gets the event_data_byte_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_data_byte_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_data_byte_rate_threshold

    @event_data_byte_rate_threshold.setter
    def event_data_byte_rate_threshold(self, event_data_byte_rate_threshold):
        """Sets the event_data_byte_rate_threshold of this MsgVpnDistributedCacheCluster.


        :param event_data_byte_rate_threshold: The event_data_byte_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_data_byte_rate_threshold = event_data_byte_rate_threshold

    @property
    def event_data_msg_rate_threshold(self):
        """Gets the event_data_msg_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_data_msg_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_data_msg_rate_threshold

    @event_data_msg_rate_threshold.setter
    def event_data_msg_rate_threshold(self, event_data_msg_rate_threshold):
        """Sets the event_data_msg_rate_threshold of this MsgVpnDistributedCacheCluster.


        :param event_data_msg_rate_threshold: The event_data_msg_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_data_msg_rate_threshold = event_data_msg_rate_threshold

    @property
    def event_max_memory_threshold(self):
        """Gets the event_max_memory_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_max_memory_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._event_max_memory_threshold

    @event_max_memory_threshold.setter
    def event_max_memory_threshold(self, event_max_memory_threshold):
        """Sets the event_max_memory_threshold of this MsgVpnDistributedCacheCluster.


        :param event_max_memory_threshold: The event_max_memory_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._event_max_memory_threshold = event_max_memory_threshold

    @property
    def event_max_topics_threshold(self):
        """Gets the event_max_topics_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_max_topics_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._event_max_topics_threshold

    @event_max_topics_threshold.setter
    def event_max_topics_threshold(self, event_max_topics_threshold):
        """Sets the event_max_topics_threshold of this MsgVpnDistributedCacheCluster.


        :param event_max_topics_threshold: The event_max_topics_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._event_max_topics_threshold = event_max_topics_threshold

    @property
    def event_request_queue_depth_threshold(self):
        """Gets the event_request_queue_depth_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_request_queue_depth_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByPercent
        """
        return self._event_request_queue_depth_threshold

    @event_request_queue_depth_threshold.setter
    def event_request_queue_depth_threshold(self, event_request_queue_depth_threshold):
        """Sets the event_request_queue_depth_threshold of this MsgVpnDistributedCacheCluster.


        :param event_request_queue_depth_threshold: The event_request_queue_depth_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByPercent
        """

        self._event_request_queue_depth_threshold = event_request_queue_depth_threshold

    @property
    def event_request_rate_threshold(self):
        """Gets the event_request_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_request_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_request_rate_threshold

    @event_request_rate_threshold.setter
    def event_request_rate_threshold(self, event_request_rate_threshold):
        """Sets the event_request_rate_threshold of this MsgVpnDistributedCacheCluster.


        :param event_request_rate_threshold: The event_request_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_request_rate_threshold = event_request_rate_threshold

    @property
    def event_response_rate_threshold(self):
        """Gets the event_response_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501


        :return: The event_response_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: EventThresholdByValue
        """
        return self._event_response_rate_threshold

    @event_response_rate_threshold.setter
    def event_response_rate_threshold(self, event_response_rate_threshold):
        """Sets the event_response_rate_threshold of this MsgVpnDistributedCacheCluster.


        :param event_response_rate_threshold: The event_response_rate_threshold of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: EventThresholdByValue
        """

        self._event_response_rate_threshold = event_response_rate_threshold

    @property
    def global_caching_enabled(self):
        """Gets the global_caching_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501

        Indicates whether global caching for the Cache Cluster is enabled, and the Cache Instances will fetch topics from remote Home Cache Clusters when requested, and subscribe to those topics to cache them locally.  # noqa: E501

        :return: The global_caching_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: bool
        """
        return self._global_caching_enabled

    @global_caching_enabled.setter
    def global_caching_enabled(self, global_caching_enabled):
        """Sets the global_caching_enabled of this MsgVpnDistributedCacheCluster.

        Indicates whether global caching for the Cache Cluster is enabled, and the Cache Instances will fetch topics from remote Home Cache Clusters when requested, and subscribe to those topics to cache them locally.  # noqa: E501

        :param global_caching_enabled: The global_caching_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: bool
        """

        self._global_caching_enabled = global_caching_enabled

    @property
    def global_caching_heartbeat(self):
        """Gets the global_caching_heartbeat of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The heartbeat interval, in seconds, used by the Cache Instances to monitor connectivity with the remote Home Cache Clusters.  # noqa: E501

        :return: The global_caching_heartbeat of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._global_caching_heartbeat

    @global_caching_heartbeat.setter
    def global_caching_heartbeat(self, global_caching_heartbeat):
        """Sets the global_caching_heartbeat of this MsgVpnDistributedCacheCluster.

        The heartbeat interval, in seconds, used by the Cache Instances to monitor connectivity with the remote Home Cache Clusters.  # noqa: E501

        :param global_caching_heartbeat: The global_caching_heartbeat of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._global_caching_heartbeat = global_caching_heartbeat

    @property
    def global_caching_topic_lifetime(self):
        """Gets the global_caching_topic_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The topic lifetime, in seconds. If no client requests are received for a given global topic over the duration of the topic lifetime, then the Cache Instance will remove the subscription and cached messages for that topic. A value of 0 disables aging.  # noqa: E501

        :return: The global_caching_topic_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._global_caching_topic_lifetime

    @global_caching_topic_lifetime.setter
    def global_caching_topic_lifetime(self, global_caching_topic_lifetime):
        """Sets the global_caching_topic_lifetime of this MsgVpnDistributedCacheCluster.

        The topic lifetime, in seconds. If no client requests are received for a given global topic over the duration of the topic lifetime, then the Cache Instance will remove the subscription and cached messages for that topic. A value of 0 disables aging.  # noqa: E501

        :param global_caching_topic_lifetime: The global_caching_topic_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._global_caching_topic_lifetime = global_caching_topic_lifetime

    @property
    def max_memory(self):
        """Gets the max_memory of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The maximum memory usage, in megabytes (MB), for each Cache Instance in the Cache Cluster.  # noqa: E501

        :return: The max_memory of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._max_memory

    @max_memory.setter
    def max_memory(self, max_memory):
        """Sets the max_memory of this MsgVpnDistributedCacheCluster.

        The maximum memory usage, in megabytes (MB), for each Cache Instance in the Cache Cluster.  # noqa: E501

        :param max_memory: The max_memory of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._max_memory = max_memory

    @property
    def max_msgs_per_topic(self):
        """Gets the max_msgs_per_topic of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The maximum number of messages per topic for each Cache Instance in the Cache Cluster. When at the maximum, old messages are removed as new messages arrive.  # noqa: E501

        :return: The max_msgs_per_topic of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._max_msgs_per_topic

    @max_msgs_per_topic.setter
    def max_msgs_per_topic(self, max_msgs_per_topic):
        """Sets the max_msgs_per_topic of this MsgVpnDistributedCacheCluster.

        The maximum number of messages per topic for each Cache Instance in the Cache Cluster. When at the maximum, old messages are removed as new messages arrive.  # noqa: E501

        :param max_msgs_per_topic: The max_msgs_per_topic of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._max_msgs_per_topic = max_msgs_per_topic

    @property
    def max_request_queue_depth(self):
        """Gets the max_request_queue_depth of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The maximum queue depth for cache requests received by the Cache Cluster.  # noqa: E501

        :return: The max_request_queue_depth of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._max_request_queue_depth

    @max_request_queue_depth.setter
    def max_request_queue_depth(self, max_request_queue_depth):
        """Sets the max_request_queue_depth of this MsgVpnDistributedCacheCluster.

        The maximum queue depth for cache requests received by the Cache Cluster.  # noqa: E501

        :param max_request_queue_depth: The max_request_queue_depth of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._max_request_queue_depth = max_request_queue_depth

    @property
    def max_topic_count(self):
        """Gets the max_topic_count of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The maximum number of topics for each Cache Instance in the Cache Cluster.  # noqa: E501

        :return: The max_topic_count of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._max_topic_count

    @max_topic_count.setter
    def max_topic_count(self, max_topic_count):
        """Sets the max_topic_count of this MsgVpnDistributedCacheCluster.

        The maximum number of topics for each Cache Instance in the Cache Cluster.  # noqa: E501

        :param max_topic_count: The max_topic_count of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._max_topic_count = max_topic_count

    @property
    def msg_lifetime(self):
        """Gets the msg_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The message lifetime, in seconds. If a message remains cached for the duration of its lifetime, the Cache Instance will remove the message. A lifetime of 0 results in the message being retained indefinitely.  # noqa: E501

        :return: The msg_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: int
        """
        return self._msg_lifetime

    @msg_lifetime.setter
    def msg_lifetime(self, msg_lifetime):
        """Sets the msg_lifetime of this MsgVpnDistributedCacheCluster.

        The message lifetime, in seconds. If a message remains cached for the duration of its lifetime, the Cache Instance will remove the message. A lifetime of 0 results in the message being retained indefinitely.  # noqa: E501

        :param msg_lifetime: The msg_lifetime of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: int
        """

        self._msg_lifetime = msg_lifetime

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnDistributedCacheCluster.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnDistributedCacheCluster.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def msgs_lost(self):
        """Gets the msgs_lost of this MsgVpnDistributedCacheCluster.  # noqa: E501

        Indicates whether one or more messages were lost by any Cache Instance in the Cache Cluster.  # noqa: E501

        :return: The msgs_lost of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: bool
        """
        return self._msgs_lost

    @msgs_lost.setter
    def msgs_lost(self, msgs_lost):
        """Sets the msgs_lost of this MsgVpnDistributedCacheCluster.

        Indicates whether one or more messages were lost by any Cache Instance in the Cache Cluster.  # noqa: E501

        :param msgs_lost: The msgs_lost of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: bool
        """

        self._msgs_lost = msgs_lost

    @property
    def new_topic_advertisement_enabled(self):
        """Gets the new_topic_advertisement_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501

        Indicates whether advertising of new topics learned by the Cache Instances in this Cache Cluster is enabled.  # noqa: E501

        :return: The new_topic_advertisement_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :rtype: bool
        """
        return self._new_topic_advertisement_enabled

    @new_topic_advertisement_enabled.setter
    def new_topic_advertisement_enabled(self, new_topic_advertisement_enabled):
        """Sets the new_topic_advertisement_enabled of this MsgVpnDistributedCacheCluster.

        Indicates whether advertising of new topics learned by the Cache Instances in this Cache Cluster is enabled.  # noqa: E501

        :param new_topic_advertisement_enabled: The new_topic_advertisement_enabled of this MsgVpnDistributedCacheCluster.  # noqa: E501
        :type: bool
        """

        self._new_topic_advertisement_enabled = new_topic_advertisement_enabled

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
        if issubclass(MsgVpnDistributedCacheCluster, dict):
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
        if not isinstance(other, MsgVpnDistributedCacheCluster):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
