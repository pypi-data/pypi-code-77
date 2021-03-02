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


class MsgVpnCollections(object):
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
        'acl_profiles': 'MsgVpnCollectionsAclprofiles',
        'authentication_oauth_providers': 'MsgVpnCollectionsAuthenticationoauthproviders',
        'authorization_groups': 'MsgVpnCollectionsAuthorizationgroups',
        'bridges': 'MsgVpnCollectionsBridges',
        'client_profiles': 'MsgVpnCollectionsClientprofiles',
        'client_usernames': 'MsgVpnCollectionsClientusernames',
        'clients': 'MsgVpnCollectionsClients',
        'config_sync_remote_nodes': 'MsgVpnCollectionsConfigsyncremotenodes',
        'distributed_caches': 'MsgVpnCollectionsDistributedcaches',
        'dmr_bridges': 'MsgVpnCollectionsDmrbridges',
        'jndi_connection_factories': 'MsgVpnCollectionsJndiconnectionfactories',
        'jndi_queues': 'MsgVpnCollectionsJndiqueues',
        'jndi_topics': 'MsgVpnCollectionsJnditopics',
        'mqtt_retain_caches': 'MsgVpnCollectionsMqttretaincaches',
        'mqtt_sessions': 'MsgVpnCollectionsMqttsessions',
        'queue_templates': 'MsgVpnCollectionsQueuetemplates',
        'queues': 'MsgVpnCollectionsQueues',
        'replay_logs': 'MsgVpnCollectionsReplaylogs',
        'replicated_topics': 'MsgVpnCollectionsReplicatedtopics',
        'rest_delivery_points': 'MsgVpnCollectionsRestdeliverypoints',
        'topic_endpoint_templates': 'MsgVpnCollectionsTopicendpointtemplates',
        'topic_endpoints': 'MsgVpnCollectionsTopicendpoints',
        'transactions': 'MsgVpnCollectionsTransactions'
    }

    attribute_map = {
        'acl_profiles': 'aclProfiles',
        'authentication_oauth_providers': 'authenticationOauthProviders',
        'authorization_groups': 'authorizationGroups',
        'bridges': 'bridges',
        'client_profiles': 'clientProfiles',
        'client_usernames': 'clientUsernames',
        'clients': 'clients',
        'config_sync_remote_nodes': 'configSyncRemoteNodes',
        'distributed_caches': 'distributedCaches',
        'dmr_bridges': 'dmrBridges',
        'jndi_connection_factories': 'jndiConnectionFactories',
        'jndi_queues': 'jndiQueues',
        'jndi_topics': 'jndiTopics',
        'mqtt_retain_caches': 'mqttRetainCaches',
        'mqtt_sessions': 'mqttSessions',
        'queue_templates': 'queueTemplates',
        'queues': 'queues',
        'replay_logs': 'replayLogs',
        'replicated_topics': 'replicatedTopics',
        'rest_delivery_points': 'restDeliveryPoints',
        'topic_endpoint_templates': 'topicEndpointTemplates',
        'topic_endpoints': 'topicEndpoints',
        'transactions': 'transactions'
    }

    def __init__(self, acl_profiles=None, authentication_oauth_providers=None, authorization_groups=None, bridges=None, client_profiles=None, client_usernames=None, clients=None, config_sync_remote_nodes=None, distributed_caches=None, dmr_bridges=None, jndi_connection_factories=None, jndi_queues=None, jndi_topics=None, mqtt_retain_caches=None, mqtt_sessions=None, queue_templates=None, queues=None, replay_logs=None, replicated_topics=None, rest_delivery_points=None, topic_endpoint_templates=None, topic_endpoints=None, transactions=None):  # noqa: E501
        """MsgVpnCollections - a model defined in Swagger"""  # noqa: E501

        self._acl_profiles = None
        self._authentication_oauth_providers = None
        self._authorization_groups = None
        self._bridges = None
        self._client_profiles = None
        self._client_usernames = None
        self._clients = None
        self._config_sync_remote_nodes = None
        self._distributed_caches = None
        self._dmr_bridges = None
        self._jndi_connection_factories = None
        self._jndi_queues = None
        self._jndi_topics = None
        self._mqtt_retain_caches = None
        self._mqtt_sessions = None
        self._queue_templates = None
        self._queues = None
        self._replay_logs = None
        self._replicated_topics = None
        self._rest_delivery_points = None
        self._topic_endpoint_templates = None
        self._topic_endpoints = None
        self._transactions = None
        self.discriminator = None

        if acl_profiles is not None:
            self.acl_profiles = acl_profiles
        if authentication_oauth_providers is not None:
            self.authentication_oauth_providers = authentication_oauth_providers
        if authorization_groups is not None:
            self.authorization_groups = authorization_groups
        if bridges is not None:
            self.bridges = bridges
        if client_profiles is not None:
            self.client_profiles = client_profiles
        if client_usernames is not None:
            self.client_usernames = client_usernames
        if clients is not None:
            self.clients = clients
        if config_sync_remote_nodes is not None:
            self.config_sync_remote_nodes = config_sync_remote_nodes
        if distributed_caches is not None:
            self.distributed_caches = distributed_caches
        if dmr_bridges is not None:
            self.dmr_bridges = dmr_bridges
        if jndi_connection_factories is not None:
            self.jndi_connection_factories = jndi_connection_factories
        if jndi_queues is not None:
            self.jndi_queues = jndi_queues
        if jndi_topics is not None:
            self.jndi_topics = jndi_topics
        if mqtt_retain_caches is not None:
            self.mqtt_retain_caches = mqtt_retain_caches
        if mqtt_sessions is not None:
            self.mqtt_sessions = mqtt_sessions
        if queue_templates is not None:
            self.queue_templates = queue_templates
        if queues is not None:
            self.queues = queues
        if replay_logs is not None:
            self.replay_logs = replay_logs
        if replicated_topics is not None:
            self.replicated_topics = replicated_topics
        if rest_delivery_points is not None:
            self.rest_delivery_points = rest_delivery_points
        if topic_endpoint_templates is not None:
            self.topic_endpoint_templates = topic_endpoint_templates
        if topic_endpoints is not None:
            self.topic_endpoints = topic_endpoints
        if transactions is not None:
            self.transactions = transactions

    @property
    def acl_profiles(self):
        """Gets the acl_profiles of this MsgVpnCollections.  # noqa: E501


        :return: The acl_profiles of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsAclprofiles
        """
        return self._acl_profiles

    @acl_profiles.setter
    def acl_profiles(self, acl_profiles):
        """Sets the acl_profiles of this MsgVpnCollections.


        :param acl_profiles: The acl_profiles of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsAclprofiles
        """

        self._acl_profiles = acl_profiles

    @property
    def authentication_oauth_providers(self):
        """Gets the authentication_oauth_providers of this MsgVpnCollections.  # noqa: E501


        :return: The authentication_oauth_providers of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsAuthenticationoauthproviders
        """
        return self._authentication_oauth_providers

    @authentication_oauth_providers.setter
    def authentication_oauth_providers(self, authentication_oauth_providers):
        """Sets the authentication_oauth_providers of this MsgVpnCollections.


        :param authentication_oauth_providers: The authentication_oauth_providers of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsAuthenticationoauthproviders
        """

        self._authentication_oauth_providers = authentication_oauth_providers

    @property
    def authorization_groups(self):
        """Gets the authorization_groups of this MsgVpnCollections.  # noqa: E501


        :return: The authorization_groups of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsAuthorizationgroups
        """
        return self._authorization_groups

    @authorization_groups.setter
    def authorization_groups(self, authorization_groups):
        """Sets the authorization_groups of this MsgVpnCollections.


        :param authorization_groups: The authorization_groups of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsAuthorizationgroups
        """

        self._authorization_groups = authorization_groups

    @property
    def bridges(self):
        """Gets the bridges of this MsgVpnCollections.  # noqa: E501


        :return: The bridges of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsBridges
        """
        return self._bridges

    @bridges.setter
    def bridges(self, bridges):
        """Sets the bridges of this MsgVpnCollections.


        :param bridges: The bridges of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsBridges
        """

        self._bridges = bridges

    @property
    def client_profiles(self):
        """Gets the client_profiles of this MsgVpnCollections.  # noqa: E501


        :return: The client_profiles of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsClientprofiles
        """
        return self._client_profiles

    @client_profiles.setter
    def client_profiles(self, client_profiles):
        """Sets the client_profiles of this MsgVpnCollections.


        :param client_profiles: The client_profiles of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsClientprofiles
        """

        self._client_profiles = client_profiles

    @property
    def client_usernames(self):
        """Gets the client_usernames of this MsgVpnCollections.  # noqa: E501


        :return: The client_usernames of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsClientusernames
        """
        return self._client_usernames

    @client_usernames.setter
    def client_usernames(self, client_usernames):
        """Sets the client_usernames of this MsgVpnCollections.


        :param client_usernames: The client_usernames of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsClientusernames
        """

        self._client_usernames = client_usernames

    @property
    def clients(self):
        """Gets the clients of this MsgVpnCollections.  # noqa: E501


        :return: The clients of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsClients
        """
        return self._clients

    @clients.setter
    def clients(self, clients):
        """Sets the clients of this MsgVpnCollections.


        :param clients: The clients of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsClients
        """

        self._clients = clients

    @property
    def config_sync_remote_nodes(self):
        """Gets the config_sync_remote_nodes of this MsgVpnCollections.  # noqa: E501


        :return: The config_sync_remote_nodes of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsConfigsyncremotenodes
        """
        return self._config_sync_remote_nodes

    @config_sync_remote_nodes.setter
    def config_sync_remote_nodes(self, config_sync_remote_nodes):
        """Sets the config_sync_remote_nodes of this MsgVpnCollections.


        :param config_sync_remote_nodes: The config_sync_remote_nodes of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsConfigsyncremotenodes
        """

        self._config_sync_remote_nodes = config_sync_remote_nodes

    @property
    def distributed_caches(self):
        """Gets the distributed_caches of this MsgVpnCollections.  # noqa: E501


        :return: The distributed_caches of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsDistributedcaches
        """
        return self._distributed_caches

    @distributed_caches.setter
    def distributed_caches(self, distributed_caches):
        """Sets the distributed_caches of this MsgVpnCollections.


        :param distributed_caches: The distributed_caches of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsDistributedcaches
        """

        self._distributed_caches = distributed_caches

    @property
    def dmr_bridges(self):
        """Gets the dmr_bridges of this MsgVpnCollections.  # noqa: E501


        :return: The dmr_bridges of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsDmrbridges
        """
        return self._dmr_bridges

    @dmr_bridges.setter
    def dmr_bridges(self, dmr_bridges):
        """Sets the dmr_bridges of this MsgVpnCollections.


        :param dmr_bridges: The dmr_bridges of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsDmrbridges
        """

        self._dmr_bridges = dmr_bridges

    @property
    def jndi_connection_factories(self):
        """Gets the jndi_connection_factories of this MsgVpnCollections.  # noqa: E501


        :return: The jndi_connection_factories of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsJndiconnectionfactories
        """
        return self._jndi_connection_factories

    @jndi_connection_factories.setter
    def jndi_connection_factories(self, jndi_connection_factories):
        """Sets the jndi_connection_factories of this MsgVpnCollections.


        :param jndi_connection_factories: The jndi_connection_factories of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsJndiconnectionfactories
        """

        self._jndi_connection_factories = jndi_connection_factories

    @property
    def jndi_queues(self):
        """Gets the jndi_queues of this MsgVpnCollections.  # noqa: E501


        :return: The jndi_queues of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsJndiqueues
        """
        return self._jndi_queues

    @jndi_queues.setter
    def jndi_queues(self, jndi_queues):
        """Sets the jndi_queues of this MsgVpnCollections.


        :param jndi_queues: The jndi_queues of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsJndiqueues
        """

        self._jndi_queues = jndi_queues

    @property
    def jndi_topics(self):
        """Gets the jndi_topics of this MsgVpnCollections.  # noqa: E501


        :return: The jndi_topics of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsJnditopics
        """
        return self._jndi_topics

    @jndi_topics.setter
    def jndi_topics(self, jndi_topics):
        """Sets the jndi_topics of this MsgVpnCollections.


        :param jndi_topics: The jndi_topics of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsJnditopics
        """

        self._jndi_topics = jndi_topics

    @property
    def mqtt_retain_caches(self):
        """Gets the mqtt_retain_caches of this MsgVpnCollections.  # noqa: E501


        :return: The mqtt_retain_caches of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsMqttretaincaches
        """
        return self._mqtt_retain_caches

    @mqtt_retain_caches.setter
    def mqtt_retain_caches(self, mqtt_retain_caches):
        """Sets the mqtt_retain_caches of this MsgVpnCollections.


        :param mqtt_retain_caches: The mqtt_retain_caches of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsMqttretaincaches
        """

        self._mqtt_retain_caches = mqtt_retain_caches

    @property
    def mqtt_sessions(self):
        """Gets the mqtt_sessions of this MsgVpnCollections.  # noqa: E501


        :return: The mqtt_sessions of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsMqttsessions
        """
        return self._mqtt_sessions

    @mqtt_sessions.setter
    def mqtt_sessions(self, mqtt_sessions):
        """Sets the mqtt_sessions of this MsgVpnCollections.


        :param mqtt_sessions: The mqtt_sessions of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsMqttsessions
        """

        self._mqtt_sessions = mqtt_sessions

    @property
    def queue_templates(self):
        """Gets the queue_templates of this MsgVpnCollections.  # noqa: E501


        :return: The queue_templates of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsQueuetemplates
        """
        return self._queue_templates

    @queue_templates.setter
    def queue_templates(self, queue_templates):
        """Sets the queue_templates of this MsgVpnCollections.


        :param queue_templates: The queue_templates of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsQueuetemplates
        """

        self._queue_templates = queue_templates

    @property
    def queues(self):
        """Gets the queues of this MsgVpnCollections.  # noqa: E501


        :return: The queues of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsQueues
        """
        return self._queues

    @queues.setter
    def queues(self, queues):
        """Sets the queues of this MsgVpnCollections.


        :param queues: The queues of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsQueues
        """

        self._queues = queues

    @property
    def replay_logs(self):
        """Gets the replay_logs of this MsgVpnCollections.  # noqa: E501


        :return: The replay_logs of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsReplaylogs
        """
        return self._replay_logs

    @replay_logs.setter
    def replay_logs(self, replay_logs):
        """Sets the replay_logs of this MsgVpnCollections.


        :param replay_logs: The replay_logs of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsReplaylogs
        """

        self._replay_logs = replay_logs

    @property
    def replicated_topics(self):
        """Gets the replicated_topics of this MsgVpnCollections.  # noqa: E501


        :return: The replicated_topics of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsReplicatedtopics
        """
        return self._replicated_topics

    @replicated_topics.setter
    def replicated_topics(self, replicated_topics):
        """Sets the replicated_topics of this MsgVpnCollections.


        :param replicated_topics: The replicated_topics of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsReplicatedtopics
        """

        self._replicated_topics = replicated_topics

    @property
    def rest_delivery_points(self):
        """Gets the rest_delivery_points of this MsgVpnCollections.  # noqa: E501


        :return: The rest_delivery_points of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsRestdeliverypoints
        """
        return self._rest_delivery_points

    @rest_delivery_points.setter
    def rest_delivery_points(self, rest_delivery_points):
        """Sets the rest_delivery_points of this MsgVpnCollections.


        :param rest_delivery_points: The rest_delivery_points of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsRestdeliverypoints
        """

        self._rest_delivery_points = rest_delivery_points

    @property
    def topic_endpoint_templates(self):
        """Gets the topic_endpoint_templates of this MsgVpnCollections.  # noqa: E501


        :return: The topic_endpoint_templates of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsTopicendpointtemplates
        """
        return self._topic_endpoint_templates

    @topic_endpoint_templates.setter
    def topic_endpoint_templates(self, topic_endpoint_templates):
        """Sets the topic_endpoint_templates of this MsgVpnCollections.


        :param topic_endpoint_templates: The topic_endpoint_templates of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsTopicendpointtemplates
        """

        self._topic_endpoint_templates = topic_endpoint_templates

    @property
    def topic_endpoints(self):
        """Gets the topic_endpoints of this MsgVpnCollections.  # noqa: E501


        :return: The topic_endpoints of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsTopicendpoints
        """
        return self._topic_endpoints

    @topic_endpoints.setter
    def topic_endpoints(self, topic_endpoints):
        """Sets the topic_endpoints of this MsgVpnCollections.


        :param topic_endpoints: The topic_endpoints of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsTopicendpoints
        """

        self._topic_endpoints = topic_endpoints

    @property
    def transactions(self):
        """Gets the transactions of this MsgVpnCollections.  # noqa: E501


        :return: The transactions of this MsgVpnCollections.  # noqa: E501
        :rtype: MsgVpnCollectionsTransactions
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        """Sets the transactions of this MsgVpnCollections.


        :param transactions: The transactions of this MsgVpnCollections.  # noqa: E501
        :type: MsgVpnCollectionsTransactions
        """

        self._transactions = transactions

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
        if issubclass(MsgVpnCollections, dict):
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
        if not isinstance(other, MsgVpnCollections):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
