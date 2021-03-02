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


class MsgVpnClientRxFlow(object):
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
        'client_name': 'str',
        'connect_time': 'int',
        'destination_group_error_discarded_msg_count': 'int',
        'duplicate_discarded_msg_count': 'int',
        'endpoint_disabled_discarded_msg_count': 'int',
        'endpoint_usage_exceeded_discarded_msg_count': 'int',
        'errored_discarded_msg_count': 'int',
        'flow_id': 'int',
        'flow_name': 'str',
        'guaranteed_msg_count': 'int',
        'last_rx_msg_id': 'int',
        'local_msg_count_exceeded_discarded_msg_count': 'int',
        'low_priority_msg_congestion_discarded_msg_count': 'int',
        'max_msg_size_exceeded_discarded_msg_count': 'int',
        'msg_vpn_name': 'str',
        'no_eligible_destinations_discarded_msg_count': 'int',
        'no_local_delivery_discarded_msg_count': 'int',
        'not_compatible_with_forwarding_mode_discarded_msg_count': 'int',
        'out_of_order_discarded_msg_count': 'int',
        'publish_acl_denied_discarded_msg_count': 'int',
        'publisher_id': 'int',
        'queue_not_found_discarded_msg_count': 'int',
        'replication_standby_discarded_msg_count': 'int',
        'session_name': 'str',
        'smf_ttl_exceeded_discarded_msg_count': 'int',
        'spool_file_limit_exceeded_discarded_msg_count': 'int',
        'spool_not_ready_discarded_msg_count': 'int',
        'spool_to_adb_fail_discarded_msg_count': 'int',
        'spool_to_disk_fail_discarded_msg_count': 'int',
        'spool_usage_exceeded_discarded_msg_count': 'int',
        'sync_replication_ineligible_discarded_msg_count': 'int',
        'user_profile_denied_guaranteed_discarded_msg_count': 'int',
        'window_size': 'int'
    }

    attribute_map = {
        'client_name': 'clientName',
        'connect_time': 'connectTime',
        'destination_group_error_discarded_msg_count': 'destinationGroupErrorDiscardedMsgCount',
        'duplicate_discarded_msg_count': 'duplicateDiscardedMsgCount',
        'endpoint_disabled_discarded_msg_count': 'endpointDisabledDiscardedMsgCount',
        'endpoint_usage_exceeded_discarded_msg_count': 'endpointUsageExceededDiscardedMsgCount',
        'errored_discarded_msg_count': 'erroredDiscardedMsgCount',
        'flow_id': 'flowId',
        'flow_name': 'flowName',
        'guaranteed_msg_count': 'guaranteedMsgCount',
        'last_rx_msg_id': 'lastRxMsgId',
        'local_msg_count_exceeded_discarded_msg_count': 'localMsgCountExceededDiscardedMsgCount',
        'low_priority_msg_congestion_discarded_msg_count': 'lowPriorityMsgCongestionDiscardedMsgCount',
        'max_msg_size_exceeded_discarded_msg_count': 'maxMsgSizeExceededDiscardedMsgCount',
        'msg_vpn_name': 'msgVpnName',
        'no_eligible_destinations_discarded_msg_count': 'noEligibleDestinationsDiscardedMsgCount',
        'no_local_delivery_discarded_msg_count': 'noLocalDeliveryDiscardedMsgCount',
        'not_compatible_with_forwarding_mode_discarded_msg_count': 'notCompatibleWithForwardingModeDiscardedMsgCount',
        'out_of_order_discarded_msg_count': 'outOfOrderDiscardedMsgCount',
        'publish_acl_denied_discarded_msg_count': 'publishAclDeniedDiscardedMsgCount',
        'publisher_id': 'publisherId',
        'queue_not_found_discarded_msg_count': 'queueNotFoundDiscardedMsgCount',
        'replication_standby_discarded_msg_count': 'replicationStandbyDiscardedMsgCount',
        'session_name': 'sessionName',
        'smf_ttl_exceeded_discarded_msg_count': 'smfTtlExceededDiscardedMsgCount',
        'spool_file_limit_exceeded_discarded_msg_count': 'spoolFileLimitExceededDiscardedMsgCount',
        'spool_not_ready_discarded_msg_count': 'spoolNotReadyDiscardedMsgCount',
        'spool_to_adb_fail_discarded_msg_count': 'spoolToAdbFailDiscardedMsgCount',
        'spool_to_disk_fail_discarded_msg_count': 'spoolToDiskFailDiscardedMsgCount',
        'spool_usage_exceeded_discarded_msg_count': 'spoolUsageExceededDiscardedMsgCount',
        'sync_replication_ineligible_discarded_msg_count': 'syncReplicationIneligibleDiscardedMsgCount',
        'user_profile_denied_guaranteed_discarded_msg_count': 'userProfileDeniedGuaranteedDiscardedMsgCount',
        'window_size': 'windowSize'
    }

    def __init__(self, client_name=None, connect_time=None, destination_group_error_discarded_msg_count=None, duplicate_discarded_msg_count=None, endpoint_disabled_discarded_msg_count=None, endpoint_usage_exceeded_discarded_msg_count=None, errored_discarded_msg_count=None, flow_id=None, flow_name=None, guaranteed_msg_count=None, last_rx_msg_id=None, local_msg_count_exceeded_discarded_msg_count=None, low_priority_msg_congestion_discarded_msg_count=None, max_msg_size_exceeded_discarded_msg_count=None, msg_vpn_name=None, no_eligible_destinations_discarded_msg_count=None, no_local_delivery_discarded_msg_count=None, not_compatible_with_forwarding_mode_discarded_msg_count=None, out_of_order_discarded_msg_count=None, publish_acl_denied_discarded_msg_count=None, publisher_id=None, queue_not_found_discarded_msg_count=None, replication_standby_discarded_msg_count=None, session_name=None, smf_ttl_exceeded_discarded_msg_count=None, spool_file_limit_exceeded_discarded_msg_count=None, spool_not_ready_discarded_msg_count=None, spool_to_adb_fail_discarded_msg_count=None, spool_to_disk_fail_discarded_msg_count=None, spool_usage_exceeded_discarded_msg_count=None, sync_replication_ineligible_discarded_msg_count=None, user_profile_denied_guaranteed_discarded_msg_count=None, window_size=None):  # noqa: E501
        """MsgVpnClientRxFlow - a model defined in Swagger"""  # noqa: E501

        self._client_name = None
        self._connect_time = None
        self._destination_group_error_discarded_msg_count = None
        self._duplicate_discarded_msg_count = None
        self._endpoint_disabled_discarded_msg_count = None
        self._endpoint_usage_exceeded_discarded_msg_count = None
        self._errored_discarded_msg_count = None
        self._flow_id = None
        self._flow_name = None
        self._guaranteed_msg_count = None
        self._last_rx_msg_id = None
        self._local_msg_count_exceeded_discarded_msg_count = None
        self._low_priority_msg_congestion_discarded_msg_count = None
        self._max_msg_size_exceeded_discarded_msg_count = None
        self._msg_vpn_name = None
        self._no_eligible_destinations_discarded_msg_count = None
        self._no_local_delivery_discarded_msg_count = None
        self._not_compatible_with_forwarding_mode_discarded_msg_count = None
        self._out_of_order_discarded_msg_count = None
        self._publish_acl_denied_discarded_msg_count = None
        self._publisher_id = None
        self._queue_not_found_discarded_msg_count = None
        self._replication_standby_discarded_msg_count = None
        self._session_name = None
        self._smf_ttl_exceeded_discarded_msg_count = None
        self._spool_file_limit_exceeded_discarded_msg_count = None
        self._spool_not_ready_discarded_msg_count = None
        self._spool_to_adb_fail_discarded_msg_count = None
        self._spool_to_disk_fail_discarded_msg_count = None
        self._spool_usage_exceeded_discarded_msg_count = None
        self._sync_replication_ineligible_discarded_msg_count = None
        self._user_profile_denied_guaranteed_discarded_msg_count = None
        self._window_size = None
        self.discriminator = None

        if client_name is not None:
            self.client_name = client_name
        if connect_time is not None:
            self.connect_time = connect_time
        if destination_group_error_discarded_msg_count is not None:
            self.destination_group_error_discarded_msg_count = destination_group_error_discarded_msg_count
        if duplicate_discarded_msg_count is not None:
            self.duplicate_discarded_msg_count = duplicate_discarded_msg_count
        if endpoint_disabled_discarded_msg_count is not None:
            self.endpoint_disabled_discarded_msg_count = endpoint_disabled_discarded_msg_count
        if endpoint_usage_exceeded_discarded_msg_count is not None:
            self.endpoint_usage_exceeded_discarded_msg_count = endpoint_usage_exceeded_discarded_msg_count
        if errored_discarded_msg_count is not None:
            self.errored_discarded_msg_count = errored_discarded_msg_count
        if flow_id is not None:
            self.flow_id = flow_id
        if flow_name is not None:
            self.flow_name = flow_name
        if guaranteed_msg_count is not None:
            self.guaranteed_msg_count = guaranteed_msg_count
        if last_rx_msg_id is not None:
            self.last_rx_msg_id = last_rx_msg_id
        if local_msg_count_exceeded_discarded_msg_count is not None:
            self.local_msg_count_exceeded_discarded_msg_count = local_msg_count_exceeded_discarded_msg_count
        if low_priority_msg_congestion_discarded_msg_count is not None:
            self.low_priority_msg_congestion_discarded_msg_count = low_priority_msg_congestion_discarded_msg_count
        if max_msg_size_exceeded_discarded_msg_count is not None:
            self.max_msg_size_exceeded_discarded_msg_count = max_msg_size_exceeded_discarded_msg_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if no_eligible_destinations_discarded_msg_count is not None:
            self.no_eligible_destinations_discarded_msg_count = no_eligible_destinations_discarded_msg_count
        if no_local_delivery_discarded_msg_count is not None:
            self.no_local_delivery_discarded_msg_count = no_local_delivery_discarded_msg_count
        if not_compatible_with_forwarding_mode_discarded_msg_count is not None:
            self.not_compatible_with_forwarding_mode_discarded_msg_count = not_compatible_with_forwarding_mode_discarded_msg_count
        if out_of_order_discarded_msg_count is not None:
            self.out_of_order_discarded_msg_count = out_of_order_discarded_msg_count
        if publish_acl_denied_discarded_msg_count is not None:
            self.publish_acl_denied_discarded_msg_count = publish_acl_denied_discarded_msg_count
        if publisher_id is not None:
            self.publisher_id = publisher_id
        if queue_not_found_discarded_msg_count is not None:
            self.queue_not_found_discarded_msg_count = queue_not_found_discarded_msg_count
        if replication_standby_discarded_msg_count is not None:
            self.replication_standby_discarded_msg_count = replication_standby_discarded_msg_count
        if session_name is not None:
            self.session_name = session_name
        if smf_ttl_exceeded_discarded_msg_count is not None:
            self.smf_ttl_exceeded_discarded_msg_count = smf_ttl_exceeded_discarded_msg_count
        if spool_file_limit_exceeded_discarded_msg_count is not None:
            self.spool_file_limit_exceeded_discarded_msg_count = spool_file_limit_exceeded_discarded_msg_count
        if spool_not_ready_discarded_msg_count is not None:
            self.spool_not_ready_discarded_msg_count = spool_not_ready_discarded_msg_count
        if spool_to_adb_fail_discarded_msg_count is not None:
            self.spool_to_adb_fail_discarded_msg_count = spool_to_adb_fail_discarded_msg_count
        if spool_to_disk_fail_discarded_msg_count is not None:
            self.spool_to_disk_fail_discarded_msg_count = spool_to_disk_fail_discarded_msg_count
        if spool_usage_exceeded_discarded_msg_count is not None:
            self.spool_usage_exceeded_discarded_msg_count = spool_usage_exceeded_discarded_msg_count
        if sync_replication_ineligible_discarded_msg_count is not None:
            self.sync_replication_ineligible_discarded_msg_count = sync_replication_ineligible_discarded_msg_count
        if user_profile_denied_guaranteed_discarded_msg_count is not None:
            self.user_profile_denied_guaranteed_discarded_msg_count = user_profile_denied_guaranteed_discarded_msg_count
        if window_size is not None:
            self.window_size = window_size

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnClientRxFlow.  # noqa: E501

        The name of the Client.  # noqa: E501

        :return: The client_name of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnClientRxFlow.

        The name of the Client.  # noqa: E501

        :param client_name: The client_name of this MsgVpnClientRxFlow.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def connect_time(self):
        """Gets the connect_time of this MsgVpnClientRxFlow.  # noqa: E501

        The timestamp of when the Flow from the Client connected.  # noqa: E501

        :return: The connect_time of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._connect_time

    @connect_time.setter
    def connect_time(self, connect_time):
        """Sets the connect_time of this MsgVpnClientRxFlow.

        The timestamp of when the Flow from the Client connected.  # noqa: E501

        :param connect_time: The connect_time of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._connect_time = connect_time

    @property
    def destination_group_error_discarded_msg_count(self):
        """Gets the destination_group_error_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to a destination group error.  # noqa: E501

        :return: The destination_group_error_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._destination_group_error_discarded_msg_count

    @destination_group_error_discarded_msg_count.setter
    def destination_group_error_discarded_msg_count(self, destination_group_error_discarded_msg_count):
        """Sets the destination_group_error_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to a destination group error.  # noqa: E501

        :param destination_group_error_discarded_msg_count: The destination_group_error_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._destination_group_error_discarded_msg_count = destination_group_error_discarded_msg_count

    @property
    def duplicate_discarded_msg_count(self):
        """Gets the duplicate_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to being a duplicate.  # noqa: E501

        :return: The duplicate_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._duplicate_discarded_msg_count

    @duplicate_discarded_msg_count.setter
    def duplicate_discarded_msg_count(self, duplicate_discarded_msg_count):
        """Sets the duplicate_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to being a duplicate.  # noqa: E501

        :param duplicate_discarded_msg_count: The duplicate_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._duplicate_discarded_msg_count = duplicate_discarded_msg_count

    @property
    def endpoint_disabled_discarded_msg_count(self):
        """Gets the endpoint_disabled_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to an eligible endpoint destination being disabled.  # noqa: E501

        :return: The endpoint_disabled_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._endpoint_disabled_discarded_msg_count

    @endpoint_disabled_discarded_msg_count.setter
    def endpoint_disabled_discarded_msg_count(self, endpoint_disabled_discarded_msg_count):
        """Sets the endpoint_disabled_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to an eligible endpoint destination being disabled.  # noqa: E501

        :param endpoint_disabled_discarded_msg_count: The endpoint_disabled_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._endpoint_disabled_discarded_msg_count = endpoint_disabled_discarded_msg_count

    @property
    def endpoint_usage_exceeded_discarded_msg_count(self):
        """Gets the endpoint_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to an eligible endpoint destination having its maximum message spool usage exceeded.  # noqa: E501

        :return: The endpoint_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._endpoint_usage_exceeded_discarded_msg_count

    @endpoint_usage_exceeded_discarded_msg_count.setter
    def endpoint_usage_exceeded_discarded_msg_count(self, endpoint_usage_exceeded_discarded_msg_count):
        """Sets the endpoint_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to an eligible endpoint destination having its maximum message spool usage exceeded.  # noqa: E501

        :param endpoint_usage_exceeded_discarded_msg_count: The endpoint_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._endpoint_usage_exceeded_discarded_msg_count = endpoint_usage_exceeded_discarded_msg_count

    @property
    def errored_discarded_msg_count(self):
        """Gets the errored_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to errors being detected.  # noqa: E501

        :return: The errored_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._errored_discarded_msg_count

    @errored_discarded_msg_count.setter
    def errored_discarded_msg_count(self, errored_discarded_msg_count):
        """Sets the errored_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to errors being detected.  # noqa: E501

        :param errored_discarded_msg_count: The errored_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._errored_discarded_msg_count = errored_discarded_msg_count

    @property
    def flow_id(self):
        """Gets the flow_id of this MsgVpnClientRxFlow.  # noqa: E501

        The identifier (ID) of the flow.  # noqa: E501

        :return: The flow_id of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        """Sets the flow_id of this MsgVpnClientRxFlow.

        The identifier (ID) of the flow.  # noqa: E501

        :param flow_id: The flow_id of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._flow_id = flow_id

    @property
    def flow_name(self):
        """Gets the flow_name of this MsgVpnClientRxFlow.  # noqa: E501

        The name of the Flow.  # noqa: E501

        :return: The flow_name of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: str
        """
        return self._flow_name

    @flow_name.setter
    def flow_name(self, flow_name):
        """Sets the flow_name of this MsgVpnClientRxFlow.

        The name of the Flow.  # noqa: E501

        :param flow_name: The flow_name of this MsgVpnClientRxFlow.  # noqa: E501
        :type: str
        """

        self._flow_name = flow_name

    @property
    def guaranteed_msg_count(self):
        """Gets the guaranteed_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow.  # noqa: E501

        :return: The guaranteed_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._guaranteed_msg_count

    @guaranteed_msg_count.setter
    def guaranteed_msg_count(self, guaranteed_msg_count):
        """Sets the guaranteed_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow.  # noqa: E501

        :param guaranteed_msg_count: The guaranteed_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._guaranteed_msg_count = guaranteed_msg_count

    @property
    def last_rx_msg_id(self):
        """Gets the last_rx_msg_id of this MsgVpnClientRxFlow.  # noqa: E501

        The identifier (ID) of the last message received on the Flow.  # noqa: E501

        :return: The last_rx_msg_id of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._last_rx_msg_id

    @last_rx_msg_id.setter
    def last_rx_msg_id(self, last_rx_msg_id):
        """Sets the last_rx_msg_id of this MsgVpnClientRxFlow.

        The identifier (ID) of the last message received on the Flow.  # noqa: E501

        :param last_rx_msg_id: The last_rx_msg_id of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._last_rx_msg_id = last_rx_msg_id

    @property
    def local_msg_count_exceeded_discarded_msg_count(self):
        """Gets the local_msg_count_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the maximum number of messages allowed on the broker being exceeded.  # noqa: E501

        :return: The local_msg_count_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._local_msg_count_exceeded_discarded_msg_count

    @local_msg_count_exceeded_discarded_msg_count.setter
    def local_msg_count_exceeded_discarded_msg_count(self, local_msg_count_exceeded_discarded_msg_count):
        """Sets the local_msg_count_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the maximum number of messages allowed on the broker being exceeded.  # noqa: E501

        :param local_msg_count_exceeded_discarded_msg_count: The local_msg_count_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._local_msg_count_exceeded_discarded_msg_count = local_msg_count_exceeded_discarded_msg_count

    @property
    def low_priority_msg_congestion_discarded_msg_count(self):
        """Gets the low_priority_msg_congestion_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to congestion of low priority messages.  # noqa: E501

        :return: The low_priority_msg_congestion_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._low_priority_msg_congestion_discarded_msg_count

    @low_priority_msg_congestion_discarded_msg_count.setter
    def low_priority_msg_congestion_discarded_msg_count(self, low_priority_msg_congestion_discarded_msg_count):
        """Sets the low_priority_msg_congestion_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to congestion of low priority messages.  # noqa: E501

        :param low_priority_msg_congestion_discarded_msg_count: The low_priority_msg_congestion_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._low_priority_msg_congestion_discarded_msg_count = low_priority_msg_congestion_discarded_msg_count

    @property
    def max_msg_size_exceeded_discarded_msg_count(self):
        """Gets the max_msg_size_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the maximum allowed message size being exceeded.  # noqa: E501

        :return: The max_msg_size_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._max_msg_size_exceeded_discarded_msg_count

    @max_msg_size_exceeded_discarded_msg_count.setter
    def max_msg_size_exceeded_discarded_msg_count(self, max_msg_size_exceeded_discarded_msg_count):
        """Sets the max_msg_size_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the maximum allowed message size being exceeded.  # noqa: E501

        :param max_msg_size_exceeded_discarded_msg_count: The max_msg_size_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._max_msg_size_exceeded_discarded_msg_count = max_msg_size_exceeded_discarded_msg_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnClientRxFlow.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnClientRxFlow.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnClientRxFlow.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def no_eligible_destinations_discarded_msg_count(self):
        """Gets the no_eligible_destinations_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to there being no eligible endpoint destination.  # noqa: E501

        :return: The no_eligible_destinations_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._no_eligible_destinations_discarded_msg_count

    @no_eligible_destinations_discarded_msg_count.setter
    def no_eligible_destinations_discarded_msg_count(self, no_eligible_destinations_discarded_msg_count):
        """Sets the no_eligible_destinations_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to there being no eligible endpoint destination.  # noqa: E501

        :param no_eligible_destinations_discarded_msg_count: The no_eligible_destinations_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._no_eligible_destinations_discarded_msg_count = no_eligible_destinations_discarded_msg_count

    @property
    def no_local_delivery_discarded_msg_count(self):
        """Gets the no_local_delivery_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to no local delivery being requested.  # noqa: E501

        :return: The no_local_delivery_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._no_local_delivery_discarded_msg_count

    @no_local_delivery_discarded_msg_count.setter
    def no_local_delivery_discarded_msg_count(self, no_local_delivery_discarded_msg_count):
        """Sets the no_local_delivery_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to no local delivery being requested.  # noqa: E501

        :param no_local_delivery_discarded_msg_count: The no_local_delivery_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._no_local_delivery_discarded_msg_count = no_local_delivery_discarded_msg_count

    @property
    def not_compatible_with_forwarding_mode_discarded_msg_count(self):
        """Gets the not_compatible_with_forwarding_mode_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to being incompatible with the forwarding mode of an eligible endpoint destination.  # noqa: E501

        :return: The not_compatible_with_forwarding_mode_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._not_compatible_with_forwarding_mode_discarded_msg_count

    @not_compatible_with_forwarding_mode_discarded_msg_count.setter
    def not_compatible_with_forwarding_mode_discarded_msg_count(self, not_compatible_with_forwarding_mode_discarded_msg_count):
        """Sets the not_compatible_with_forwarding_mode_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to being incompatible with the forwarding mode of an eligible endpoint destination.  # noqa: E501

        :param not_compatible_with_forwarding_mode_discarded_msg_count: The not_compatible_with_forwarding_mode_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._not_compatible_with_forwarding_mode_discarded_msg_count = not_compatible_with_forwarding_mode_discarded_msg_count

    @property
    def out_of_order_discarded_msg_count(self):
        """Gets the out_of_order_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to being received out of order.  # noqa: E501

        :return: The out_of_order_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._out_of_order_discarded_msg_count

    @out_of_order_discarded_msg_count.setter
    def out_of_order_discarded_msg_count(self, out_of_order_discarded_msg_count):
        """Sets the out_of_order_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to being received out of order.  # noqa: E501

        :param out_of_order_discarded_msg_count: The out_of_order_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._out_of_order_discarded_msg_count = out_of_order_discarded_msg_count

    @property
    def publish_acl_denied_discarded_msg_count(self):
        """Gets the publish_acl_denied_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to being denied by the access control list (ACL) profile for the published topic.  # noqa: E501

        :return: The publish_acl_denied_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._publish_acl_denied_discarded_msg_count

    @publish_acl_denied_discarded_msg_count.setter
    def publish_acl_denied_discarded_msg_count(self, publish_acl_denied_discarded_msg_count):
        """Sets the publish_acl_denied_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to being denied by the access control list (ACL) profile for the published topic.  # noqa: E501

        :param publish_acl_denied_discarded_msg_count: The publish_acl_denied_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._publish_acl_denied_discarded_msg_count = publish_acl_denied_discarded_msg_count

    @property
    def publisher_id(self):
        """Gets the publisher_id of this MsgVpnClientRxFlow.  # noqa: E501

        The identifier (ID) of the publisher for the Flow.  # noqa: E501

        :return: The publisher_id of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._publisher_id

    @publisher_id.setter
    def publisher_id(self, publisher_id):
        """Sets the publisher_id of this MsgVpnClientRxFlow.

        The identifier (ID) of the publisher for the Flow.  # noqa: E501

        :param publisher_id: The publisher_id of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._publisher_id = publisher_id

    @property
    def queue_not_found_discarded_msg_count(self):
        """Gets the queue_not_found_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the destination queue not being found.  # noqa: E501

        :return: The queue_not_found_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._queue_not_found_discarded_msg_count

    @queue_not_found_discarded_msg_count.setter
    def queue_not_found_discarded_msg_count(self, queue_not_found_discarded_msg_count):
        """Sets the queue_not_found_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the destination queue not being found.  # noqa: E501

        :param queue_not_found_discarded_msg_count: The queue_not_found_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._queue_not_found_discarded_msg_count = queue_not_found_discarded_msg_count

    @property
    def replication_standby_discarded_msg_count(self):
        """Gets the replication_standby_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the Message VPN being in the replication standby state.  # noqa: E501

        :return: The replication_standby_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._replication_standby_discarded_msg_count

    @replication_standby_discarded_msg_count.setter
    def replication_standby_discarded_msg_count(self, replication_standby_discarded_msg_count):
        """Sets the replication_standby_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the Message VPN being in the replication standby state.  # noqa: E501

        :param replication_standby_discarded_msg_count: The replication_standby_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._replication_standby_discarded_msg_count = replication_standby_discarded_msg_count

    @property
    def session_name(self):
        """Gets the session_name of this MsgVpnClientRxFlow.  # noqa: E501

        The name of the transacted session on the Flow.  # noqa: E501

        :return: The session_name of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: str
        """
        return self._session_name

    @session_name.setter
    def session_name(self, session_name):
        """Sets the session_name of this MsgVpnClientRxFlow.

        The name of the transacted session on the Flow.  # noqa: E501

        :param session_name: The session_name of this MsgVpnClientRxFlow.  # noqa: E501
        :type: str
        """

        self._session_name = session_name

    @property
    def smf_ttl_exceeded_discarded_msg_count(self):
        """Gets the smf_ttl_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the message time-to-live (TTL) count being exceeded. The message TTL count is the maximum number of times the message can cross a bridge between Message VPNs.  # noqa: E501

        :return: The smf_ttl_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._smf_ttl_exceeded_discarded_msg_count

    @smf_ttl_exceeded_discarded_msg_count.setter
    def smf_ttl_exceeded_discarded_msg_count(self, smf_ttl_exceeded_discarded_msg_count):
        """Sets the smf_ttl_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the message time-to-live (TTL) count being exceeded. The message TTL count is the maximum number of times the message can cross a bridge between Message VPNs.  # noqa: E501

        :param smf_ttl_exceeded_discarded_msg_count: The smf_ttl_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._smf_ttl_exceeded_discarded_msg_count = smf_ttl_exceeded_discarded_msg_count

    @property
    def spool_file_limit_exceeded_discarded_msg_count(self):
        """Gets the spool_file_limit_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to all available message spool file resources being used.  # noqa: E501

        :return: The spool_file_limit_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._spool_file_limit_exceeded_discarded_msg_count

    @spool_file_limit_exceeded_discarded_msg_count.setter
    def spool_file_limit_exceeded_discarded_msg_count(self, spool_file_limit_exceeded_discarded_msg_count):
        """Sets the spool_file_limit_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to all available message spool file resources being used.  # noqa: E501

        :param spool_file_limit_exceeded_discarded_msg_count: The spool_file_limit_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._spool_file_limit_exceeded_discarded_msg_count = spool_file_limit_exceeded_discarded_msg_count

    @property
    def spool_not_ready_discarded_msg_count(self):
        """Gets the spool_not_ready_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the message spool being not ready.  # noqa: E501

        :return: The spool_not_ready_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._spool_not_ready_discarded_msg_count

    @spool_not_ready_discarded_msg_count.setter
    def spool_not_ready_discarded_msg_count(self, spool_not_ready_discarded_msg_count):
        """Sets the spool_not_ready_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the message spool being not ready.  # noqa: E501

        :param spool_not_ready_discarded_msg_count: The spool_not_ready_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._spool_not_ready_discarded_msg_count = spool_not_ready_discarded_msg_count

    @property
    def spool_to_adb_fail_discarded_msg_count(self):
        """Gets the spool_to_adb_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to a failure while spooling to the Assured Delivery Blade (ADB).  # noqa: E501

        :return: The spool_to_adb_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._spool_to_adb_fail_discarded_msg_count

    @spool_to_adb_fail_discarded_msg_count.setter
    def spool_to_adb_fail_discarded_msg_count(self, spool_to_adb_fail_discarded_msg_count):
        """Sets the spool_to_adb_fail_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to a failure while spooling to the Assured Delivery Blade (ADB).  # noqa: E501

        :param spool_to_adb_fail_discarded_msg_count: The spool_to_adb_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._spool_to_adb_fail_discarded_msg_count = spool_to_adb_fail_discarded_msg_count

    @property
    def spool_to_disk_fail_discarded_msg_count(self):
        """Gets the spool_to_disk_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to a failure while spooling to the disk.  # noqa: E501

        :return: The spool_to_disk_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._spool_to_disk_fail_discarded_msg_count

    @spool_to_disk_fail_discarded_msg_count.setter
    def spool_to_disk_fail_discarded_msg_count(self, spool_to_disk_fail_discarded_msg_count):
        """Sets the spool_to_disk_fail_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to a failure while spooling to the disk.  # noqa: E501

        :param spool_to_disk_fail_discarded_msg_count: The spool_to_disk_fail_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._spool_to_disk_fail_discarded_msg_count = spool_to_disk_fail_discarded_msg_count

    @property
    def spool_usage_exceeded_discarded_msg_count(self):
        """Gets the spool_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to the maximum message spool usage being exceeded.  # noqa: E501

        :return: The spool_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._spool_usage_exceeded_discarded_msg_count

    @spool_usage_exceeded_discarded_msg_count.setter
    def spool_usage_exceeded_discarded_msg_count(self, spool_usage_exceeded_discarded_msg_count):
        """Sets the spool_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to the maximum message spool usage being exceeded.  # noqa: E501

        :param spool_usage_exceeded_discarded_msg_count: The spool_usage_exceeded_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._spool_usage_exceeded_discarded_msg_count = spool_usage_exceeded_discarded_msg_count

    @property
    def sync_replication_ineligible_discarded_msg_count(self):
        """Gets the sync_replication_ineligible_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to synchronous replication being ineligible.  # noqa: E501

        :return: The sync_replication_ineligible_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._sync_replication_ineligible_discarded_msg_count

    @sync_replication_ineligible_discarded_msg_count.setter
    def sync_replication_ineligible_discarded_msg_count(self, sync_replication_ineligible_discarded_msg_count):
        """Sets the sync_replication_ineligible_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to synchronous replication being ineligible.  # noqa: E501

        :param sync_replication_ineligible_discarded_msg_count: The sync_replication_ineligible_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._sync_replication_ineligible_discarded_msg_count = sync_replication_ineligible_discarded_msg_count

    @property
    def user_profile_denied_guaranteed_discarded_msg_count(self):
        """Gets the user_profile_denied_guaranteed_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501

        The number of guaranteed messages from the Flow discarded due to being denied by the client profile.  # noqa: E501

        :return: The user_profile_denied_guaranteed_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._user_profile_denied_guaranteed_discarded_msg_count

    @user_profile_denied_guaranteed_discarded_msg_count.setter
    def user_profile_denied_guaranteed_discarded_msg_count(self, user_profile_denied_guaranteed_discarded_msg_count):
        """Sets the user_profile_denied_guaranteed_discarded_msg_count of this MsgVpnClientRxFlow.

        The number of guaranteed messages from the Flow discarded due to being denied by the client profile.  # noqa: E501

        :param user_profile_denied_guaranteed_discarded_msg_count: The user_profile_denied_guaranteed_discarded_msg_count of this MsgVpnClientRxFlow.  # noqa: E501
        :type: int
        """

        self._user_profile_denied_guaranteed_discarded_msg_count = user_profile_denied_guaranteed_discarded_msg_count

    @property
    def window_size(self):
        """Gets the window_size of this MsgVpnClientRxFlow.  # noqa: E501

        The size of the window used for guaranteed messages sent on the Flow, in messages.  # noqa: E501

        :return: The window_size of this MsgVpnClientRxFlow.  # noqa: E501
        :rtype: int
        """
        return self._window_size

    @window_size.setter
    def window_size(self, window_size):
        """Sets the window_size of this MsgVpnClientRxFlow.

        The size of the window used for guaranteed messages sent on the Flow, in messages.  # noqa: E501

        :param window_size: The window_size of this MsgVpnClientRxFlow.  # noqa: E501
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
        if issubclass(MsgVpnClientRxFlow, dict):
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
        if not isinstance(other, MsgVpnClientRxFlow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
