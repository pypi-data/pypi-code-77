# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.19
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnLinks(object):
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
        'acl_profiles_uri': 'str',
        'authentication_oauth_providers_uri': 'str',
        'authorization_groups_uri': 'str',
        'bridges_uri': 'str',
        'client_profiles_uri': 'str',
        'client_usernames_uri': 'str',
        'clients_uri': 'str',
        'config_sync_remote_nodes_uri': 'str',
        'distributed_caches_uri': 'str',
        'dmr_bridges_uri': 'str',
        'jndi_connection_factories_uri': 'str',
        'jndi_queues_uri': 'str',
        'jndi_topics_uri': 'str',
        'mqtt_retain_caches_uri': 'str',
        'mqtt_sessions_uri': 'str',
        'queue_templates_uri': 'str',
        'queues_uri': 'str',
        'replay_logs_uri': 'str',
        'replicated_topics_uri': 'str',
        'rest_delivery_points_uri': 'str',
        'topic_endpoint_templates_uri': 'str',
        'topic_endpoints_uri': 'str',
        'transactions_uri': 'str',
        'uri': 'str'
    }

    attribute_map = {
        'acl_profiles_uri': 'aclProfilesUri',
        'authentication_oauth_providers_uri': 'authenticationOauthProvidersUri',
        'authorization_groups_uri': 'authorizationGroupsUri',
        'bridges_uri': 'bridgesUri',
        'client_profiles_uri': 'clientProfilesUri',
        'client_usernames_uri': 'clientUsernamesUri',
        'clients_uri': 'clientsUri',
        'config_sync_remote_nodes_uri': 'configSyncRemoteNodesUri',
        'distributed_caches_uri': 'distributedCachesUri',
        'dmr_bridges_uri': 'dmrBridgesUri',
        'jndi_connection_factories_uri': 'jndiConnectionFactoriesUri',
        'jndi_queues_uri': 'jndiQueuesUri',
        'jndi_topics_uri': 'jndiTopicsUri',
        'mqtt_retain_caches_uri': 'mqttRetainCachesUri',
        'mqtt_sessions_uri': 'mqttSessionsUri',
        'queue_templates_uri': 'queueTemplatesUri',
        'queues_uri': 'queuesUri',
        'replay_logs_uri': 'replayLogsUri',
        'replicated_topics_uri': 'replicatedTopicsUri',
        'rest_delivery_points_uri': 'restDeliveryPointsUri',
        'topic_endpoint_templates_uri': 'topicEndpointTemplatesUri',
        'topic_endpoints_uri': 'topicEndpointsUri',
        'transactions_uri': 'transactionsUri',
        'uri': 'uri'
    }

    def __init__(self, acl_profiles_uri=None, authentication_oauth_providers_uri=None, authorization_groups_uri=None, bridges_uri=None, client_profiles_uri=None, client_usernames_uri=None, clients_uri=None, config_sync_remote_nodes_uri=None, distributed_caches_uri=None, dmr_bridges_uri=None, jndi_connection_factories_uri=None, jndi_queues_uri=None, jndi_topics_uri=None, mqtt_retain_caches_uri=None, mqtt_sessions_uri=None, queue_templates_uri=None, queues_uri=None, replay_logs_uri=None, replicated_topics_uri=None, rest_delivery_points_uri=None, topic_endpoint_templates_uri=None, topic_endpoints_uri=None, transactions_uri=None, uri=None):  # noqa: E501
        """MsgVpnLinks - a model defined in Swagger"""  # noqa: E501

        self._acl_profiles_uri = None
        self._authentication_oauth_providers_uri = None
        self._authorization_groups_uri = None
        self._bridges_uri = None
        self._client_profiles_uri = None
        self._client_usernames_uri = None
        self._clients_uri = None
        self._config_sync_remote_nodes_uri = None
        self._distributed_caches_uri = None
        self._dmr_bridges_uri = None
        self._jndi_connection_factories_uri = None
        self._jndi_queues_uri = None
        self._jndi_topics_uri = None
        self._mqtt_retain_caches_uri = None
        self._mqtt_sessions_uri = None
        self._queue_templates_uri = None
        self._queues_uri = None
        self._replay_logs_uri = None
        self._replicated_topics_uri = None
        self._rest_delivery_points_uri = None
        self._topic_endpoint_templates_uri = None
        self._topic_endpoints_uri = None
        self._transactions_uri = None
        self._uri = None
        self.discriminator = None

        if acl_profiles_uri is not None:
            self.acl_profiles_uri = acl_profiles_uri
        if authentication_oauth_providers_uri is not None:
            self.authentication_oauth_providers_uri = authentication_oauth_providers_uri
        if authorization_groups_uri is not None:
            self.authorization_groups_uri = authorization_groups_uri
        if bridges_uri is not None:
            self.bridges_uri = bridges_uri
        if client_profiles_uri is not None:
            self.client_profiles_uri = client_profiles_uri
        if client_usernames_uri is not None:
            self.client_usernames_uri = client_usernames_uri
        if clients_uri is not None:
            self.clients_uri = clients_uri
        if config_sync_remote_nodes_uri is not None:
            self.config_sync_remote_nodes_uri = config_sync_remote_nodes_uri
        if distributed_caches_uri is not None:
            self.distributed_caches_uri = distributed_caches_uri
        if dmr_bridges_uri is not None:
            self.dmr_bridges_uri = dmr_bridges_uri
        if jndi_connection_factories_uri is not None:
            self.jndi_connection_factories_uri = jndi_connection_factories_uri
        if jndi_queues_uri is not None:
            self.jndi_queues_uri = jndi_queues_uri
        if jndi_topics_uri is not None:
            self.jndi_topics_uri = jndi_topics_uri
        if mqtt_retain_caches_uri is not None:
            self.mqtt_retain_caches_uri = mqtt_retain_caches_uri
        if mqtt_sessions_uri is not None:
            self.mqtt_sessions_uri = mqtt_sessions_uri
        if queue_templates_uri is not None:
            self.queue_templates_uri = queue_templates_uri
        if queues_uri is not None:
            self.queues_uri = queues_uri
        if replay_logs_uri is not None:
            self.replay_logs_uri = replay_logs_uri
        if replicated_topics_uri is not None:
            self.replicated_topics_uri = replicated_topics_uri
        if rest_delivery_points_uri is not None:
            self.rest_delivery_points_uri = rest_delivery_points_uri
        if topic_endpoint_templates_uri is not None:
            self.topic_endpoint_templates_uri = topic_endpoint_templates_uri
        if topic_endpoints_uri is not None:
            self.topic_endpoints_uri = topic_endpoints_uri
        if transactions_uri is not None:
            self.transactions_uri = transactions_uri
        if uri is not None:
            self.uri = uri

    @property
    def acl_profiles_uri(self):
        """Gets the acl_profiles_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of ACL Profile objects.  # noqa: E501

        :return: The acl_profiles_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._acl_profiles_uri

    @acl_profiles_uri.setter
    def acl_profiles_uri(self, acl_profiles_uri):
        """Sets the acl_profiles_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of ACL Profile objects.  # noqa: E501

        :param acl_profiles_uri: The acl_profiles_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._acl_profiles_uri = acl_profiles_uri

    @property
    def authentication_oauth_providers_uri(self):
        """Gets the authentication_oauth_providers_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of OAuth Provider objects. Available since 2.13.  # noqa: E501

        :return: The authentication_oauth_providers_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._authentication_oauth_providers_uri

    @authentication_oauth_providers_uri.setter
    def authentication_oauth_providers_uri(self, authentication_oauth_providers_uri):
        """Sets the authentication_oauth_providers_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of OAuth Provider objects. Available since 2.13.  # noqa: E501

        :param authentication_oauth_providers_uri: The authentication_oauth_providers_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._authentication_oauth_providers_uri = authentication_oauth_providers_uri

    @property
    def authorization_groups_uri(self):
        """Gets the authorization_groups_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of LDAP Authorization Group objects.  # noqa: E501

        :return: The authorization_groups_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._authorization_groups_uri

    @authorization_groups_uri.setter
    def authorization_groups_uri(self, authorization_groups_uri):
        """Sets the authorization_groups_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of LDAP Authorization Group objects.  # noqa: E501

        :param authorization_groups_uri: The authorization_groups_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._authorization_groups_uri = authorization_groups_uri

    @property
    def bridges_uri(self):
        """Gets the bridges_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Bridge objects.  # noqa: E501

        :return: The bridges_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._bridges_uri

    @bridges_uri.setter
    def bridges_uri(self, bridges_uri):
        """Sets the bridges_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Bridge objects.  # noqa: E501

        :param bridges_uri: The bridges_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._bridges_uri = bridges_uri

    @property
    def client_profiles_uri(self):
        """Gets the client_profiles_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Client Profile objects.  # noqa: E501

        :return: The client_profiles_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._client_profiles_uri

    @client_profiles_uri.setter
    def client_profiles_uri(self, client_profiles_uri):
        """Sets the client_profiles_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Client Profile objects.  # noqa: E501

        :param client_profiles_uri: The client_profiles_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._client_profiles_uri = client_profiles_uri

    @property
    def client_usernames_uri(self):
        """Gets the client_usernames_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Client Username objects.  # noqa: E501

        :return: The client_usernames_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._client_usernames_uri

    @client_usernames_uri.setter
    def client_usernames_uri(self, client_usernames_uri):
        """Sets the client_usernames_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Client Username objects.  # noqa: E501

        :param client_usernames_uri: The client_usernames_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._client_usernames_uri = client_usernames_uri

    @property
    def clients_uri(self):
        """Gets the clients_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Client objects. Available since 2.12.  # noqa: E501

        :return: The clients_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._clients_uri

    @clients_uri.setter
    def clients_uri(self, clients_uri):
        """Sets the clients_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Client objects. Available since 2.12.  # noqa: E501

        :param clients_uri: The clients_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._clients_uri = clients_uri

    @property
    def config_sync_remote_nodes_uri(self):
        """Gets the config_sync_remote_nodes_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Config Sync Remote Node objects. Available since 2.12.  # noqa: E501

        :return: The config_sync_remote_nodes_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._config_sync_remote_nodes_uri

    @config_sync_remote_nodes_uri.setter
    def config_sync_remote_nodes_uri(self, config_sync_remote_nodes_uri):
        """Sets the config_sync_remote_nodes_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Config Sync Remote Node objects. Available since 2.12.  # noqa: E501

        :param config_sync_remote_nodes_uri: The config_sync_remote_nodes_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._config_sync_remote_nodes_uri = config_sync_remote_nodes_uri

    @property
    def distributed_caches_uri(self):
        """Gets the distributed_caches_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Distributed Cache objects.  # noqa: E501

        :return: The distributed_caches_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._distributed_caches_uri

    @distributed_caches_uri.setter
    def distributed_caches_uri(self, distributed_caches_uri):
        """Sets the distributed_caches_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Distributed Cache objects.  # noqa: E501

        :param distributed_caches_uri: The distributed_caches_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._distributed_caches_uri = distributed_caches_uri

    @property
    def dmr_bridges_uri(self):
        """Gets the dmr_bridges_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of DMR Bridge objects.  # noqa: E501

        :return: The dmr_bridges_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._dmr_bridges_uri

    @dmr_bridges_uri.setter
    def dmr_bridges_uri(self, dmr_bridges_uri):
        """Sets the dmr_bridges_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of DMR Bridge objects.  # noqa: E501

        :param dmr_bridges_uri: The dmr_bridges_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._dmr_bridges_uri = dmr_bridges_uri

    @property
    def jndi_connection_factories_uri(self):
        """Gets the jndi_connection_factories_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of JNDI Connection Factory objects.  # noqa: E501

        :return: The jndi_connection_factories_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._jndi_connection_factories_uri

    @jndi_connection_factories_uri.setter
    def jndi_connection_factories_uri(self, jndi_connection_factories_uri):
        """Sets the jndi_connection_factories_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of JNDI Connection Factory objects.  # noqa: E501

        :param jndi_connection_factories_uri: The jndi_connection_factories_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._jndi_connection_factories_uri = jndi_connection_factories_uri

    @property
    def jndi_queues_uri(self):
        """Gets the jndi_queues_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of JNDI Queue objects.  # noqa: E501

        :return: The jndi_queues_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._jndi_queues_uri

    @jndi_queues_uri.setter
    def jndi_queues_uri(self, jndi_queues_uri):
        """Sets the jndi_queues_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of JNDI Queue objects.  # noqa: E501

        :param jndi_queues_uri: The jndi_queues_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._jndi_queues_uri = jndi_queues_uri

    @property
    def jndi_topics_uri(self):
        """Gets the jndi_topics_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of JNDI Topic objects.  # noqa: E501

        :return: The jndi_topics_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._jndi_topics_uri

    @jndi_topics_uri.setter
    def jndi_topics_uri(self, jndi_topics_uri):
        """Sets the jndi_topics_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of JNDI Topic objects.  # noqa: E501

        :param jndi_topics_uri: The jndi_topics_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._jndi_topics_uri = jndi_topics_uri

    @property
    def mqtt_retain_caches_uri(self):
        """Gets the mqtt_retain_caches_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of MQTT Retain Cache objects.  # noqa: E501

        :return: The mqtt_retain_caches_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._mqtt_retain_caches_uri

    @mqtt_retain_caches_uri.setter
    def mqtt_retain_caches_uri(self, mqtt_retain_caches_uri):
        """Sets the mqtt_retain_caches_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of MQTT Retain Cache objects.  # noqa: E501

        :param mqtt_retain_caches_uri: The mqtt_retain_caches_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._mqtt_retain_caches_uri = mqtt_retain_caches_uri

    @property
    def mqtt_sessions_uri(self):
        """Gets the mqtt_sessions_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of MQTT Session objects.  # noqa: E501

        :return: The mqtt_sessions_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._mqtt_sessions_uri

    @mqtt_sessions_uri.setter
    def mqtt_sessions_uri(self, mqtt_sessions_uri):
        """Sets the mqtt_sessions_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of MQTT Session objects.  # noqa: E501

        :param mqtt_sessions_uri: The mqtt_sessions_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._mqtt_sessions_uri = mqtt_sessions_uri

    @property
    def queue_templates_uri(self):
        """Gets the queue_templates_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Queue Template objects. Available since 2.14.  # noqa: E501

        :return: The queue_templates_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._queue_templates_uri

    @queue_templates_uri.setter
    def queue_templates_uri(self, queue_templates_uri):
        """Sets the queue_templates_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Queue Template objects. Available since 2.14.  # noqa: E501

        :param queue_templates_uri: The queue_templates_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._queue_templates_uri = queue_templates_uri

    @property
    def queues_uri(self):
        """Gets the queues_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Queue objects. Available since 2.12.  # noqa: E501

        :return: The queues_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._queues_uri

    @queues_uri.setter
    def queues_uri(self, queues_uri):
        """Sets the queues_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Queue objects. Available since 2.12.  # noqa: E501

        :param queues_uri: The queues_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._queues_uri = queues_uri

    @property
    def replay_logs_uri(self):
        """Gets the replay_logs_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Replay Log objects.  # noqa: E501

        :return: The replay_logs_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._replay_logs_uri

    @replay_logs_uri.setter
    def replay_logs_uri(self, replay_logs_uri):
        """Sets the replay_logs_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Replay Log objects.  # noqa: E501

        :param replay_logs_uri: The replay_logs_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._replay_logs_uri = replay_logs_uri

    @property
    def replicated_topics_uri(self):
        """Gets the replicated_topics_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Replicated Topic objects. Available since 2.12.  # noqa: E501

        :return: The replicated_topics_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._replicated_topics_uri

    @replicated_topics_uri.setter
    def replicated_topics_uri(self, replicated_topics_uri):
        """Sets the replicated_topics_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Replicated Topic objects. Available since 2.12.  # noqa: E501

        :param replicated_topics_uri: The replicated_topics_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._replicated_topics_uri = replicated_topics_uri

    @property
    def rest_delivery_points_uri(self):
        """Gets the rest_delivery_points_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of REST Delivery Point objects.  # noqa: E501

        :return: The rest_delivery_points_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._rest_delivery_points_uri

    @rest_delivery_points_uri.setter
    def rest_delivery_points_uri(self, rest_delivery_points_uri):
        """Sets the rest_delivery_points_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of REST Delivery Point objects.  # noqa: E501

        :param rest_delivery_points_uri: The rest_delivery_points_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._rest_delivery_points_uri = rest_delivery_points_uri

    @property
    def topic_endpoint_templates_uri(self):
        """Gets the topic_endpoint_templates_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Topic Endpoint Template objects. Available since 2.14.  # noqa: E501

        :return: The topic_endpoint_templates_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._topic_endpoint_templates_uri

    @topic_endpoint_templates_uri.setter
    def topic_endpoint_templates_uri(self, topic_endpoint_templates_uri):
        """Sets the topic_endpoint_templates_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Topic Endpoint Template objects. Available since 2.14.  # noqa: E501

        :param topic_endpoint_templates_uri: The topic_endpoint_templates_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._topic_endpoint_templates_uri = topic_endpoint_templates_uri

    @property
    def topic_endpoints_uri(self):
        """Gets the topic_endpoints_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Topic Endpoint objects. Available since 2.12.  # noqa: E501

        :return: The topic_endpoints_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._topic_endpoints_uri

    @topic_endpoints_uri.setter
    def topic_endpoints_uri(self, topic_endpoints_uri):
        """Sets the topic_endpoints_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Topic Endpoint objects. Available since 2.12.  # noqa: E501

        :param topic_endpoints_uri: The topic_endpoints_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._topic_endpoints_uri = topic_endpoints_uri

    @property
    def transactions_uri(self):
        """Gets the transactions_uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN's collection of Replicated Local Transaction or XA Transaction objects. Available since 2.12.  # noqa: E501

        :return: The transactions_uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._transactions_uri

    @transactions_uri.setter
    def transactions_uri(self, transactions_uri):
        """Sets the transactions_uri of this MsgVpnLinks.

        The URI of this Message VPN's collection of Replicated Local Transaction or XA Transaction objects. Available since 2.12.  # noqa: E501

        :param transactions_uri: The transactions_uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._transactions_uri = transactions_uri

    @property
    def uri(self):
        """Gets the uri of this MsgVpnLinks.  # noqa: E501

        The URI of this Message VPN object.  # noqa: E501

        :return: The uri of this MsgVpnLinks.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this MsgVpnLinks.

        The URI of this Message VPN object.  # noqa: E501

        :param uri: The uri of this MsgVpnLinks.  # noqa: E501
        :type: str
        """

        self._uri = uri

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
        if issubclass(MsgVpnLinks, dict):
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
        if not isinstance(other, MsgVpnLinks):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
