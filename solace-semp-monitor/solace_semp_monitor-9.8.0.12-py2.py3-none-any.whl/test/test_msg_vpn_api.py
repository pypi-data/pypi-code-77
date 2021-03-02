# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any combination of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written.|See note 3 Write-Only|Attribute can only be written, not read, unless the attribute is also opaque|See the documentation for the opaque property Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version| Opaque|Attribute can be set or retrieved in opaque form when the `opaquePassword` query parameter is present|See the `opaquePassword` query parameter documentation    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    In the monitoring API, any non-identifying attribute may not be returned in a GET.  ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object (see note 5)|New attribute values|Object attributes and metadata|Set to default, with certain exceptions (see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ### opaquePassword  Attributes with the opaque property are also write-only and so cannot normally be retrieved in a GET. However, when a password is provided in the `opaquePassword` query parameter, attributes with the opaque property are retrieved in a GET in opaque form, encrypted with this password. The query parameter can also be used on a POST, PATCH, or PUT to set opaque attributes using opaque attribute values retrieved in a GET, so long as:  1. the same password that was used to retrieve the opaque attribute values is provided; and  2. the broker to which the request is being sent has the same major and minor SEMP version as the broker that produced the opaque attribute values.  The password provided in the query parameter must be a minimum of 8 characters and a maximum of 128 characters.  The query parameter can only be used in the configuration API, and only over HTTPS.  ## Help  Visit [our website](https://solace.com) to learn more about Solace.  You can also download the SEMP API specifications by clicking [here](https://solace.com/downloads/).  If you need additional support, please contact us at [support@solace.com](mailto:support@solace.com).  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|On a PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT, except in the following two cases: there is a mutual requires relationship with another non-write-only attribute and both attributes are absent from the request; or the attribute is also opaque and the `opaquePassword` query parameter is provided in the request. 5|On a PUT, if the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.19
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import solace_semp_monitor
from solace_semp_monitor.api.msg_vpn_api import MsgVpnApi  # noqa: E501
from solace_semp_monitor.rest import ApiException


class TestMsgVpnApi(unittest.TestCase):
    """MsgVpnApi unit test stubs"""

    def setUp(self):
        self.api = solace_semp_monitor.api.msg_vpn_api.MsgVpnApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_msg_vpn(self):
        """Test case for get_msg_vpn

        Get a Message VPN object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile(self):
        """Test case for get_msg_vpn_acl_profile

        Get an ACL Profile object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_client_connect_exception(self):
        """Test case for get_msg_vpn_acl_profile_client_connect_exception

        Get a Client Connect Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_client_connect_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_client_connect_exceptions

        Get a list of Client Connect Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_exception(self):
        """Test case for get_msg_vpn_acl_profile_publish_exception

        Get a Publish Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_publish_exceptions

        Get a list of Publish Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_topic_exception(self):
        """Test case for get_msg_vpn_acl_profile_publish_topic_exception

        Get a Publish Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_topic_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_publish_topic_exceptions

        Get a list of Publish Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_exception(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_exception

        Get a Subscribe Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_exceptions

        Get a list of Subscribe Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_share_name_exception(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_share_name_exception

        Get a Subscribe Share Name Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_share_name_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_share_name_exceptions

        Get a list of Subscribe Share Name Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_topic_exception(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_topic_exception

        Get a Subscribe Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_topic_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_topic_exceptions

        Get a list of Subscribe Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profiles(self):
        """Test case for get_msg_vpn_acl_profiles

        Get a list of ACL Profile objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authentication_oauth_provider(self):
        """Test case for get_msg_vpn_authentication_oauth_provider

        Get an OAuth Provider object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authentication_oauth_providers(self):
        """Test case for get_msg_vpn_authentication_oauth_providers

        Get a list of OAuth Provider objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authorization_group(self):
        """Test case for get_msg_vpn_authorization_group

        Get an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authorization_groups(self):
        """Test case for get_msg_vpn_authorization_groups

        Get a list of LDAP Authorization Group objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge(self):
        """Test case for get_msg_vpn_bridge

        Get a Bridge object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_local_subscription(self):
        """Test case for get_msg_vpn_bridge_local_subscription

        Get a Bridge Local Subscriptions object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_local_subscriptions(self):
        """Test case for get_msg_vpn_bridge_local_subscriptions

        Get a list of Bridge Local Subscriptions objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for get_msg_vpn_bridge_remote_msg_vpn

        Get a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_msg_vpns(self):
        """Test case for get_msg_vpn_bridge_remote_msg_vpns

        Get a list of Remote Message VPN objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_subscription(self):
        """Test case for get_msg_vpn_bridge_remote_subscription

        Get a Remote Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_subscriptions(self):
        """Test case for get_msg_vpn_bridge_remote_subscriptions

        Get a list of Remote Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_tls_trusted_common_name(self):
        """Test case for get_msg_vpn_bridge_tls_trusted_common_name

        Get a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_tls_trusted_common_names(self):
        """Test case for get_msg_vpn_bridge_tls_trusted_common_names

        Get a list of Trusted Common Name objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridges(self):
        """Test case for get_msg_vpn_bridges

        Get a list of Bridge objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client(self):
        """Test case for get_msg_vpn_client

        Get a Client object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_connection(self):
        """Test case for get_msg_vpn_client_connection

        Get a Client Connection object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_connections(self):
        """Test case for get_msg_vpn_client_connections

        Get a list of Client Connection objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_profile(self):
        """Test case for get_msg_vpn_client_profile

        Get a Client Profile object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_profiles(self):
        """Test case for get_msg_vpn_client_profiles

        Get a list of Client Profile objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_rx_flow(self):
        """Test case for get_msg_vpn_client_rx_flow

        Get a Client Receive Flow object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_rx_flows(self):
        """Test case for get_msg_vpn_client_rx_flows

        Get a list of Client Receive Flow objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_subscription(self):
        """Test case for get_msg_vpn_client_subscription

        Get a Client Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_subscriptions(self):
        """Test case for get_msg_vpn_client_subscriptions

        Get a list of Client Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_transacted_session(self):
        """Test case for get_msg_vpn_client_transacted_session

        Get a Client Transacted Session object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_transacted_sessions(self):
        """Test case for get_msg_vpn_client_transacted_sessions

        Get a list of Client Transacted Session objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_tx_flow(self):
        """Test case for get_msg_vpn_client_tx_flow

        Get a Client Transmit Flow object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_tx_flows(self):
        """Test case for get_msg_vpn_client_tx_flows

        Get a list of Client Transmit Flow objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_username(self):
        """Test case for get_msg_vpn_client_username

        Get a Client Username object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_usernames(self):
        """Test case for get_msg_vpn_client_usernames

        Get a list of Client Username objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_clients(self):
        """Test case for get_msg_vpn_clients

        Get a list of Client objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_config_sync_remote_node(self):
        """Test case for get_msg_vpn_config_sync_remote_node

        Get a Config Sync Remote Node object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_config_sync_remote_nodes(self):
        """Test case for get_msg_vpn_config_sync_remote_nodes

        Get a list of Config Sync Remote Node objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache(self):
        """Test case for get_msg_vpn_distributed_cache

        Get a Distributed Cache object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster(self):
        """Test case for get_msg_vpn_distributed_cache_cluster

        Get a Cache Cluster object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster

        Get a Home Cache Cluster object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix

        Get a Topic Prefix object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes

        Get a list of Topic Prefix objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters

        Get a list of Home Cache Cluster objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instance(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instance

        Get a Cache Instance object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster

        Get a Remote Home Cache Cluster object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters

        Get a list of Remote Home Cache Cluster objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instance_remote_topic(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instance_remote_topic

        Get a Remote Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instance_remote_topics(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instance_remote_topics

        Get a list of Remote Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_instances(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_instances

        Get a list of Cache Instance objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_topic(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_topic

        Get a Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_cluster_topics(self):
        """Test case for get_msg_vpn_distributed_cache_cluster_topics

        Get a list of Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_cache_clusters(self):
        """Test case for get_msg_vpn_distributed_cache_clusters

        Get a list of Cache Cluster objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_distributed_caches(self):
        """Test case for get_msg_vpn_distributed_caches

        Get a list of Distributed Cache objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_dmr_bridge(self):
        """Test case for get_msg_vpn_dmr_bridge

        Get a DMR Bridge object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_dmr_bridges(self):
        """Test case for get_msg_vpn_dmr_bridges

        Get a list of DMR Bridge objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_connection_factories(self):
        """Test case for get_msg_vpn_jndi_connection_factories

        Get a list of JNDI Connection Factory objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_connection_factory(self):
        """Test case for get_msg_vpn_jndi_connection_factory

        Get a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_queue(self):
        """Test case for get_msg_vpn_jndi_queue

        Get a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_queues(self):
        """Test case for get_msg_vpn_jndi_queues

        Get a list of JNDI Queue objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_topic(self):
        """Test case for get_msg_vpn_jndi_topic

        Get a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_topics(self):
        """Test case for get_msg_vpn_jndi_topics

        Get a list of JNDI Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_retain_cache(self):
        """Test case for get_msg_vpn_mqtt_retain_cache

        Get an MQTT Retain Cache object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_retain_caches(self):
        """Test case for get_msg_vpn_mqtt_retain_caches

        Get a list of MQTT Retain Cache objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session(self):
        """Test case for get_msg_vpn_mqtt_session

        Get an MQTT Session object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session_subscription(self):
        """Test case for get_msg_vpn_mqtt_session_subscription

        Get a Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session_subscriptions(self):
        """Test case for get_msg_vpn_mqtt_session_subscriptions

        Get a list of Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_sessions(self):
        """Test case for get_msg_vpn_mqtt_sessions

        Get a list of MQTT Session objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue(self):
        """Test case for get_msg_vpn_queue

        Get a Queue object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_msg(self):
        """Test case for get_msg_vpn_queue_msg

        Get a Queue Message object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_msgs(self):
        """Test case for get_msg_vpn_queue_msgs

        Get a list of Queue Message objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_priorities(self):
        """Test case for get_msg_vpn_queue_priorities

        Get a list of Queue Priority objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_priority(self):
        """Test case for get_msg_vpn_queue_priority

        Get a Queue Priority object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_subscription(self):
        """Test case for get_msg_vpn_queue_subscription

        Get a Queue Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_subscriptions(self):
        """Test case for get_msg_vpn_queue_subscriptions

        Get a list of Queue Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_template(self):
        """Test case for get_msg_vpn_queue_template

        Get a Queue Template object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_templates(self):
        """Test case for get_msg_vpn_queue_templates

        Get a list of Queue Template objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_tx_flow(self):
        """Test case for get_msg_vpn_queue_tx_flow

        Get a Queue Transmit Flow object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_tx_flows(self):
        """Test case for get_msg_vpn_queue_tx_flows

        Get a list of Queue Transmit Flow objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queues(self):
        """Test case for get_msg_vpn_queues

        Get a list of Queue objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replay_log(self):
        """Test case for get_msg_vpn_replay_log

        Get a Replay Log object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replay_log_msg(self):
        """Test case for get_msg_vpn_replay_log_msg

        Get a Message object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replay_log_msgs(self):
        """Test case for get_msg_vpn_replay_log_msgs

        Get a list of Message objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replay_logs(self):
        """Test case for get_msg_vpn_replay_logs

        Get a list of Replay Log objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replicated_topic(self):
        """Test case for get_msg_vpn_replicated_topic

        Get a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replicated_topics(self):
        """Test case for get_msg_vpn_replicated_topics

        Get a list of Replicated Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point(self):
        """Test case for get_msg_vpn_rest_delivery_point

        Get a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for get_msg_vpn_rest_delivery_point_queue_binding

        Get a Queue Binding object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_queue_bindings(self):
        """Test case for get_msg_vpn_rest_delivery_point_queue_bindings

        Get a list of Queue Binding objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer

        Get a REST Consumer object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name

        Get a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names

        Get a list of Trusted Common Name objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumers(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumers

        Get a list of REST Consumer objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_points(self):
        """Test case for get_msg_vpn_rest_delivery_points

        Get a list of REST Delivery Point objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint(self):
        """Test case for get_msg_vpn_topic_endpoint

        Get a Topic Endpoint object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_msg(self):
        """Test case for get_msg_vpn_topic_endpoint_msg

        Get a Topic Endpoint Message object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_msgs(self):
        """Test case for get_msg_vpn_topic_endpoint_msgs

        Get a list of Topic Endpoint Message objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_priorities(self):
        """Test case for get_msg_vpn_topic_endpoint_priorities

        Get a list of Topic Endpoint Priority objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_priority(self):
        """Test case for get_msg_vpn_topic_endpoint_priority

        Get a Topic Endpoint Priority object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_template(self):
        """Test case for get_msg_vpn_topic_endpoint_template

        Get a Topic Endpoint Template object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_templates(self):
        """Test case for get_msg_vpn_topic_endpoint_templates

        Get a list of Topic Endpoint Template objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_tx_flow(self):
        """Test case for get_msg_vpn_topic_endpoint_tx_flow

        Get a Topic Endpoint Transmit Flow object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint_tx_flows(self):
        """Test case for get_msg_vpn_topic_endpoint_tx_flows

        Get a list of Topic Endpoint Transmit Flow objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoints(self):
        """Test case for get_msg_vpn_topic_endpoints

        Get a list of Topic Endpoint objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transaction(self):
        """Test case for get_msg_vpn_transaction

        Get a Replicated Local Transaction or XA Transaction object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transaction_consumer_msg(self):
        """Test case for get_msg_vpn_transaction_consumer_msg

        Get a Transaction Consumer Message object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transaction_consumer_msgs(self):
        """Test case for get_msg_vpn_transaction_consumer_msgs

        Get a list of Transaction Consumer Message objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transaction_publisher_msg(self):
        """Test case for get_msg_vpn_transaction_publisher_msg

        Get a Transaction Publisher Message object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transaction_publisher_msgs(self):
        """Test case for get_msg_vpn_transaction_publisher_msgs

        Get a list of Transaction Publisher Message objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_transactions(self):
        """Test case for get_msg_vpn_transactions

        Get a list of Replicated Local Transaction or XA Transaction objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpns(self):
        """Test case for get_msg_vpns

        Get a list of Message VPN objects.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
