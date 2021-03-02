# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see [note 1](#notes)) is a RESTful API for configuring, monitoring, and administering a Solace router.  SEMP uses URIs to address manageable **resources** of the Solace router.  Resources are either individual **objects**, or **collections** of objects.  This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See [note 2](#notes)    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See [note 2](#notes)    Resources are always nouns, with individual objects being singular and  collections being plural. Objects within a collection are identified by an  `obj-id`, which follows the collection name with the form  `collection-name/obj-id`. Some examples:  <pre> /SEMP/v2/config/msgVpns                       ; MsgVpn collection /SEMP/v2/config/msgVpns/finance               ; MsgVpn object named \"finance\" /SEMP/v2/config/msgVpns/finance/queues        ; Queue collection within MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ ; Queue object named \"orderQ\" within MsgVpn \"finance\" </pre>  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and  are described by JSON arrays. Each item in the array represents an object in  the same manner as the individual object would normally be represented. The creation of a new object is done through its collection  resource.   ## Object Resources  Objects are composed of attributes and collections, and are described by JSON  content as name/value pairs. The collections of an object are not contained  directly in the object's JSON content, rather the content includes a URI  attribute which points to the collection. This contained collection resource  must be managed as a separate resource through this URI.  At a minimum, every object has 1 or more identifying attributes, and its own  `uri` attribute which contains the URI to itself. Attributes may have any  (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See [note 3](#notes) Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in  certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request     ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these  general principles:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see [note 4](#notes)) PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many  method/URI combinations. Individual URIs may document additional parameters.  Note that multiple query parameters can be used together in a single URI,  separated by the ampersand character. For example:  <pre> ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 </pre>  ### select  Include in the response only selected attributes of the object. Use this query  parameter to limit the size of the returned data for each returned object, or  return only those fields that are desired.  The value of `select` is a comma-separated list of attribute names. Names may  include the `*` wildcard (zero or more characters). Nested attribute names  are supported using periods (e.g. `parentName.childName`). If the list is  empty (i.e. `select=`) no attributes are returned; otherwise the list must  match at least one attribute name of the object. Some examples:  <pre> ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName  ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication*  ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission </pre>  ### where  Include in the response only objects where certain conditions are true. Use  this query parameter to limit which objects are returned to those whose  attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions  must be true for the object to be included in the response. Each expression  takes the form:  <pre> expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' </pre>  `value` may be a number, string, `true`, or `false`, as appropriate for the  type of `attribute-name`. Greater-than and less-than comparisons only work for  numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more  characters). Some examples:  <pre> ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true  ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap  ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100  ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* </pre>  ### count  Limit the count of objects in the response. This can be useful to limit the  size of the response for large collections. The minimum value for `count` is  `1` and the default is `10`. There is a hidden maximum  as to prevent overloading the system. For example:  <pre> ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 </pre>  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data  that should not be created or interpreted by SEMP clients, and should only be  used as described below.  When a request is made for a collection and there may be additional objects  available for retrieval that are not included in the initial response, the  response will include a `cursorQuery` field containing a cursor. The value  of this field can be specified in the `cursor` query parameter of a  subsequent request to retrieve the next page of objects. For convenience,  an appropriate URI is constructed automatically by the router and included  in the `nextPageUri` field of the response. This URI can be used directly  to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace router. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first. 5|For DELETE, the body of the request currently serves no purpose and will cause an error if not empty.      # noqa: E501

    OpenAPI spec version: 2.4.0
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import solace_semp_config
from solace_semp_config.api.msg_vpn_api import MsgVpnApi  # noqa: E501
from solace_semp_config.rest import ApiException


class TestMsgVpnApi(unittest.TestCase):
    """MsgVpnApi unit test stubs"""

    def setUp(self):
        self.api = solace_semp_config.api.msg_vpn_api.MsgVpnApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_msg_vpn(self):
        """Test case for create_msg_vpn

        Creates a Message VPN object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_acl_profile(self):
        """Test case for create_msg_vpn_acl_profile

        Creates an ACL Profile object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_acl_profile_client_connect_exception(self):
        """Test case for create_msg_vpn_acl_profile_client_connect_exception

        Creates a Client Connect Exception object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_acl_profile_publish_exception(self):
        """Test case for create_msg_vpn_acl_profile_publish_exception

        Creates a Publish Topic Exception object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_acl_profile_subscribe_exception(self):
        """Test case for create_msg_vpn_acl_profile_subscribe_exception

        Creates a Subscribe Topic Exception object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_authorization_group(self):
        """Test case for create_msg_vpn_authorization_group

        Creates an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_bridge(self):
        """Test case for create_msg_vpn_bridge

        Creates a Bridge object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for create_msg_vpn_bridge_remote_msg_vpn

        Creates a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_bridge_remote_subscription(self):
        """Test case for create_msg_vpn_bridge_remote_subscription

        Creates a Remote Subscription object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_bridge_tls_trusted_common_name(self):
        """Test case for create_msg_vpn_bridge_tls_trusted_common_name

        Creates a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_client_profile(self):
        """Test case for create_msg_vpn_client_profile

        Creates a Client Profile object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_client_username(self):
        """Test case for create_msg_vpn_client_username

        Creates a Client Username object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_jndi_connection_factory(self):
        """Test case for create_msg_vpn_jndi_connection_factory

        Creates a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_jndi_queue(self):
        """Test case for create_msg_vpn_jndi_queue

        Creates a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_jndi_topic(self):
        """Test case for create_msg_vpn_jndi_topic

        Creates a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_mqtt_session(self):
        """Test case for create_msg_vpn_mqtt_session

        Creates an MQTT Session object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_mqtt_session_subscription(self):
        """Test case for create_msg_vpn_mqtt_session_subscription

        Creates an MQTT Session Subscription object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_queue(self):
        """Test case for create_msg_vpn_queue

        Creates a Queue object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_queue_subscription(self):
        """Test case for create_msg_vpn_queue_subscription

        Creates a Queue Subscription object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_replicated_topic(self):
        """Test case for create_msg_vpn_replicated_topic

        Creates a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_rest_delivery_point(self):
        """Test case for create_msg_vpn_rest_delivery_point

        Creates a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for create_msg_vpn_rest_delivery_point_queue_binding

        Creates a Queue Binding object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for create_msg_vpn_rest_delivery_point_rest_consumer

        Creates a REST Consumer object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self):
        """Test case for create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name

        Creates a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_sequenced_topic(self):
        """Test case for create_msg_vpn_sequenced_topic

        Creates a Sequenced Topic object.  # noqa: E501
        """
        pass

    def test_create_msg_vpn_topic_endpoint(self):
        """Test case for create_msg_vpn_topic_endpoint

        Creates a Topic Endpoint object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn(self):
        """Test case for delete_msg_vpn

        Deletes a Message VPN object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_acl_profile(self):
        """Test case for delete_msg_vpn_acl_profile

        Deletes an ACL Profile object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_acl_profile_client_connect_exception(self):
        """Test case for delete_msg_vpn_acl_profile_client_connect_exception

        Deletes a Client Connect Exception object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_acl_profile_publish_exception(self):
        """Test case for delete_msg_vpn_acl_profile_publish_exception

        Deletes a Publish Topic Exception object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_acl_profile_subscribe_exception(self):
        """Test case for delete_msg_vpn_acl_profile_subscribe_exception

        Deletes a Subscribe Topic Exception object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_authorization_group(self):
        """Test case for delete_msg_vpn_authorization_group

        Deletes an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_bridge(self):
        """Test case for delete_msg_vpn_bridge

        Deletes a Bridge object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for delete_msg_vpn_bridge_remote_msg_vpn

        Deletes a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_bridge_remote_subscription(self):
        """Test case for delete_msg_vpn_bridge_remote_subscription

        Deletes a Remote Subscription object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_bridge_tls_trusted_common_name(self):
        """Test case for delete_msg_vpn_bridge_tls_trusted_common_name

        Deletes a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_client_profile(self):
        """Test case for delete_msg_vpn_client_profile

        Deletes a Client Profile object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_client_username(self):
        """Test case for delete_msg_vpn_client_username

        Deletes a Client Username object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_jndi_connection_factory(self):
        """Test case for delete_msg_vpn_jndi_connection_factory

        Deletes a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_jndi_queue(self):
        """Test case for delete_msg_vpn_jndi_queue

        Deletes a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_jndi_topic(self):
        """Test case for delete_msg_vpn_jndi_topic

        Deletes a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_mqtt_session(self):
        """Test case for delete_msg_vpn_mqtt_session

        Deletes an MQTT Session object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_mqtt_session_subscription(self):
        """Test case for delete_msg_vpn_mqtt_session_subscription

        Deletes an MQTT Session Subscription object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_queue(self):
        """Test case for delete_msg_vpn_queue

        Deletes a Queue object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_queue_subscription(self):
        """Test case for delete_msg_vpn_queue_subscription

        Deletes a Queue Subscription object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_replicated_topic(self):
        """Test case for delete_msg_vpn_replicated_topic

        Deletes a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_rest_delivery_point(self):
        """Test case for delete_msg_vpn_rest_delivery_point

        Deletes a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for delete_msg_vpn_rest_delivery_point_queue_binding

        Deletes a Queue Binding object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for delete_msg_vpn_rest_delivery_point_rest_consumer

        Deletes a REST Consumer object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self):
        """Test case for delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name

        Deletes a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_sequenced_topic(self):
        """Test case for delete_msg_vpn_sequenced_topic

        Deletes a Sequenced Topic object.  # noqa: E501
        """
        pass

    def test_delete_msg_vpn_topic_endpoint(self):
        """Test case for delete_msg_vpn_topic_endpoint

        Deletes a Topic Endpoint object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn(self):
        """Test case for get_msg_vpn

        Gets a Message VPN object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile(self):
        """Test case for get_msg_vpn_acl_profile

        Gets an ACL Profile object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_client_connect_exception(self):
        """Test case for get_msg_vpn_acl_profile_client_connect_exception

        Gets a Client Connect Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_client_connect_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_client_connect_exceptions

        Gets a list of Client Connect Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_exception(self):
        """Test case for get_msg_vpn_acl_profile_publish_exception

        Gets a Publish Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_publish_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_publish_exceptions

        Gets a list of Publish Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_exception(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_exception

        Gets a Subscribe Topic Exception object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profile_subscribe_exceptions(self):
        """Test case for get_msg_vpn_acl_profile_subscribe_exceptions

        Gets a list of Subscribe Topic Exception objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_acl_profiles(self):
        """Test case for get_msg_vpn_acl_profiles

        Gets a list of ACL Profile objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authorization_group(self):
        """Test case for get_msg_vpn_authorization_group

        Gets an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_authorization_groups(self):
        """Test case for get_msg_vpn_authorization_groups

        Gets a list of LDAP Authorization Group objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge(self):
        """Test case for get_msg_vpn_bridge

        Gets a Bridge object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for get_msg_vpn_bridge_remote_msg_vpn

        Gets a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_msg_vpns(self):
        """Test case for get_msg_vpn_bridge_remote_msg_vpns

        Gets a list of Remote Message VPN objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_subscription(self):
        """Test case for get_msg_vpn_bridge_remote_subscription

        Gets a Remote Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_remote_subscriptions(self):
        """Test case for get_msg_vpn_bridge_remote_subscriptions

        Gets a list of Remote Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_tls_trusted_common_name(self):
        """Test case for get_msg_vpn_bridge_tls_trusted_common_name

        Gets a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridge_tls_trusted_common_names(self):
        """Test case for get_msg_vpn_bridge_tls_trusted_common_names

        Gets a list of Trusted Common Name objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_bridges(self):
        """Test case for get_msg_vpn_bridges

        Gets a list of Bridge objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_profile(self):
        """Test case for get_msg_vpn_client_profile

        Gets a Client Profile object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_profiles(self):
        """Test case for get_msg_vpn_client_profiles

        Gets a list of Client Profile objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_username(self):
        """Test case for get_msg_vpn_client_username

        Gets a Client Username object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_client_usernames(self):
        """Test case for get_msg_vpn_client_usernames

        Gets a list of Client Username objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_connection_factories(self):
        """Test case for get_msg_vpn_jndi_connection_factories

        Gets a list of JNDI Connection Factory objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_connection_factory(self):
        """Test case for get_msg_vpn_jndi_connection_factory

        Gets a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_queue(self):
        """Test case for get_msg_vpn_jndi_queue

        Gets a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_queues(self):
        """Test case for get_msg_vpn_jndi_queues

        Gets a list of JNDI Queue objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_topic(self):
        """Test case for get_msg_vpn_jndi_topic

        Gets a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_jndi_topics(self):
        """Test case for get_msg_vpn_jndi_topics

        Gets a list of JNDI Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session(self):
        """Test case for get_msg_vpn_mqtt_session

        Gets an MQTT Session object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session_subscription(self):
        """Test case for get_msg_vpn_mqtt_session_subscription

        Gets an MQTT Session Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_session_subscriptions(self):
        """Test case for get_msg_vpn_mqtt_session_subscriptions

        Gets a list of MQTT Session Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_mqtt_sessions(self):
        """Test case for get_msg_vpn_mqtt_sessions

        Gets a list of MQTT Session objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue(self):
        """Test case for get_msg_vpn_queue

        Gets a Queue object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_subscription(self):
        """Test case for get_msg_vpn_queue_subscription

        Gets a Queue Subscription object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queue_subscriptions(self):
        """Test case for get_msg_vpn_queue_subscriptions

        Gets a list of Queue Subscription objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_queues(self):
        """Test case for get_msg_vpn_queues

        Gets a list of Queue objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replicated_topic(self):
        """Test case for get_msg_vpn_replicated_topic

        Gets a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_replicated_topics(self):
        """Test case for get_msg_vpn_replicated_topics

        Gets a list of Replicated Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point(self):
        """Test case for get_msg_vpn_rest_delivery_point

        Gets a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for get_msg_vpn_rest_delivery_point_queue_binding

        Gets a Queue Binding object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_queue_bindings(self):
        """Test case for get_msg_vpn_rest_delivery_point_queue_bindings

        Gets a list of Queue Binding objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer

        Gets a REST Consumer object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name

        Gets a Trusted Common Name object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names

        Gets a list of Trusted Common Name objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_point_rest_consumers(self):
        """Test case for get_msg_vpn_rest_delivery_point_rest_consumers

        Gets a list of REST Consumer objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_rest_delivery_points(self):
        """Test case for get_msg_vpn_rest_delivery_points

        Gets a list of REST Delivery Point objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_sequenced_topic(self):
        """Test case for get_msg_vpn_sequenced_topic

        Gets a Sequenced Topic object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_sequenced_topics(self):
        """Test case for get_msg_vpn_sequenced_topics

        Gets a list of Sequenced Topic objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoint(self):
        """Test case for get_msg_vpn_topic_endpoint

        Gets a Topic Endpoint object.  # noqa: E501
        """
        pass

    def test_get_msg_vpn_topic_endpoints(self):
        """Test case for get_msg_vpn_topic_endpoints

        Gets a list of Topic Endpoint objects.  # noqa: E501
        """
        pass

    def test_get_msg_vpns(self):
        """Test case for get_msg_vpns

        Gets a list of Message VPN objects.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn(self):
        """Test case for replace_msg_vpn

        Replaces a Message VPN object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_acl_profile(self):
        """Test case for replace_msg_vpn_acl_profile

        Replaces an ACL Profile object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_authorization_group(self):
        """Test case for replace_msg_vpn_authorization_group

        Replaces an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_bridge(self):
        """Test case for replace_msg_vpn_bridge

        Replaces a Bridge object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for replace_msg_vpn_bridge_remote_msg_vpn

        Replaces a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_client_profile(self):
        """Test case for replace_msg_vpn_client_profile

        Replaces a Client Profile object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_client_username(self):
        """Test case for replace_msg_vpn_client_username

        Replaces a Client Username object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_jndi_connection_factory(self):
        """Test case for replace_msg_vpn_jndi_connection_factory

        Replaces a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_jndi_queue(self):
        """Test case for replace_msg_vpn_jndi_queue

        Replaces a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_jndi_topic(self):
        """Test case for replace_msg_vpn_jndi_topic

        Replaces a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_mqtt_session(self):
        """Test case for replace_msg_vpn_mqtt_session

        Replaces an MQTT Session object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_mqtt_session_subscription(self):
        """Test case for replace_msg_vpn_mqtt_session_subscription

        Replaces an MQTT Session Subscription object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_queue(self):
        """Test case for replace_msg_vpn_queue

        Replaces a Queue object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_replicated_topic(self):
        """Test case for replace_msg_vpn_replicated_topic

        Replaces a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_rest_delivery_point(self):
        """Test case for replace_msg_vpn_rest_delivery_point

        Replaces a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for replace_msg_vpn_rest_delivery_point_queue_binding

        Replaces a Queue Binding object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for replace_msg_vpn_rest_delivery_point_rest_consumer

        Replaces a REST Consumer object.  # noqa: E501
        """
        pass

    def test_replace_msg_vpn_topic_endpoint(self):
        """Test case for replace_msg_vpn_topic_endpoint

        Replaces a Topic Endpoint object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn(self):
        """Test case for update_msg_vpn

        Updates a Message VPN object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_acl_profile(self):
        """Test case for update_msg_vpn_acl_profile

        Updates an ACL Profile object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_authorization_group(self):
        """Test case for update_msg_vpn_authorization_group

        Updates an LDAP Authorization Group object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_bridge(self):
        """Test case for update_msg_vpn_bridge

        Updates a Bridge object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_bridge_remote_msg_vpn(self):
        """Test case for update_msg_vpn_bridge_remote_msg_vpn

        Updates a Remote Message VPN object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_client_profile(self):
        """Test case for update_msg_vpn_client_profile

        Updates a Client Profile object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_client_username(self):
        """Test case for update_msg_vpn_client_username

        Updates a Client Username object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_jndi_connection_factory(self):
        """Test case for update_msg_vpn_jndi_connection_factory

        Updates a JNDI Connection Factory object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_jndi_queue(self):
        """Test case for update_msg_vpn_jndi_queue

        Updates a JNDI Queue object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_jndi_topic(self):
        """Test case for update_msg_vpn_jndi_topic

        Updates a JNDI Topic object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_mqtt_session(self):
        """Test case for update_msg_vpn_mqtt_session

        Updates an MQTT Session object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_mqtt_session_subscription(self):
        """Test case for update_msg_vpn_mqtt_session_subscription

        Updates an MQTT Session Subscription object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_queue(self):
        """Test case for update_msg_vpn_queue

        Updates a Queue object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_replicated_topic(self):
        """Test case for update_msg_vpn_replicated_topic

        Updates a Replicated Topic object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_rest_delivery_point(self):
        """Test case for update_msg_vpn_rest_delivery_point

        Updates a REST Delivery Point object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_rest_delivery_point_queue_binding(self):
        """Test case for update_msg_vpn_rest_delivery_point_queue_binding

        Updates a Queue Binding object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_rest_delivery_point_rest_consumer(self):
        """Test case for update_msg_vpn_rest_delivery_point_rest_consumer

        Updates a REST Consumer object.  # noqa: E501
        """
        pass

    def test_update_msg_vpn_topic_endpoint(self):
        """Test case for update_msg_vpn_topic_endpoint

        Updates a Topic Endpoint object.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
