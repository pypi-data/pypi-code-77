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


class MsgVpnRestDeliveryPointRestConsumer(object):
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
        'authentication_http_basic_username': 'str',
        'authentication_scheme': 'str',
        'counter': 'MsgVpnRestDeliveryPointRestConsumerCounter',
        'enabled': 'bool',
        'last_connection_failure_local_endpoint': 'str',
        'last_connection_failure_reason': 'str',
        'last_connection_failure_remote_endpoint': 'str',
        'last_connection_failure_time': 'int',
        'last_failure_reason': 'str',
        'last_failure_time': 'int',
        'local_interface': 'str',
        'max_post_wait_time': 'int',
        'msg_vpn_name': 'str',
        'outgoing_connection_count': 'int',
        'remote_host': 'str',
        'remote_outgoing_connection_up_count': 'int',
        'remote_port': 'int',
        'rest_consumer_name': 'str',
        'rest_delivery_point_name': 'str',
        'retry_delay': 'int',
        'tls_cipher_suite_list': 'str',
        'tls_enabled': 'bool',
        'up': 'bool'
    }

    attribute_map = {
        'authentication_http_basic_username': 'authenticationHttpBasicUsername',
        'authentication_scheme': 'authenticationScheme',
        'counter': 'counter',
        'enabled': 'enabled',
        'last_connection_failure_local_endpoint': 'lastConnectionFailureLocalEndpoint',
        'last_connection_failure_reason': 'lastConnectionFailureReason',
        'last_connection_failure_remote_endpoint': 'lastConnectionFailureRemoteEndpoint',
        'last_connection_failure_time': 'lastConnectionFailureTime',
        'last_failure_reason': 'lastFailureReason',
        'last_failure_time': 'lastFailureTime',
        'local_interface': 'localInterface',
        'max_post_wait_time': 'maxPostWaitTime',
        'msg_vpn_name': 'msgVpnName',
        'outgoing_connection_count': 'outgoingConnectionCount',
        'remote_host': 'remoteHost',
        'remote_outgoing_connection_up_count': 'remoteOutgoingConnectionUpCount',
        'remote_port': 'remotePort',
        'rest_consumer_name': 'restConsumerName',
        'rest_delivery_point_name': 'restDeliveryPointName',
        'retry_delay': 'retryDelay',
        'tls_cipher_suite_list': 'tlsCipherSuiteList',
        'tls_enabled': 'tlsEnabled',
        'up': 'up'
    }

    def __init__(self, authentication_http_basic_username=None, authentication_scheme=None, counter=None, enabled=None, last_connection_failure_local_endpoint=None, last_connection_failure_reason=None, last_connection_failure_remote_endpoint=None, last_connection_failure_time=None, last_failure_reason=None, last_failure_time=None, local_interface=None, max_post_wait_time=None, msg_vpn_name=None, outgoing_connection_count=None, remote_host=None, remote_outgoing_connection_up_count=None, remote_port=None, rest_consumer_name=None, rest_delivery_point_name=None, retry_delay=None, tls_cipher_suite_list=None, tls_enabled=None, up=None):  # noqa: E501
        """MsgVpnRestDeliveryPointRestConsumer - a model defined in Swagger"""  # noqa: E501

        self._authentication_http_basic_username = None
        self._authentication_scheme = None
        self._counter = None
        self._enabled = None
        self._last_connection_failure_local_endpoint = None
        self._last_connection_failure_reason = None
        self._last_connection_failure_remote_endpoint = None
        self._last_connection_failure_time = None
        self._last_failure_reason = None
        self._last_failure_time = None
        self._local_interface = None
        self._max_post_wait_time = None
        self._msg_vpn_name = None
        self._outgoing_connection_count = None
        self._remote_host = None
        self._remote_outgoing_connection_up_count = None
        self._remote_port = None
        self._rest_consumer_name = None
        self._rest_delivery_point_name = None
        self._retry_delay = None
        self._tls_cipher_suite_list = None
        self._tls_enabled = None
        self._up = None
        self.discriminator = None

        if authentication_http_basic_username is not None:
            self.authentication_http_basic_username = authentication_http_basic_username
        if authentication_scheme is not None:
            self.authentication_scheme = authentication_scheme
        if counter is not None:
            self.counter = counter
        if enabled is not None:
            self.enabled = enabled
        if last_connection_failure_local_endpoint is not None:
            self.last_connection_failure_local_endpoint = last_connection_failure_local_endpoint
        if last_connection_failure_reason is not None:
            self.last_connection_failure_reason = last_connection_failure_reason
        if last_connection_failure_remote_endpoint is not None:
            self.last_connection_failure_remote_endpoint = last_connection_failure_remote_endpoint
        if last_connection_failure_time is not None:
            self.last_connection_failure_time = last_connection_failure_time
        if last_failure_reason is not None:
            self.last_failure_reason = last_failure_reason
        if last_failure_time is not None:
            self.last_failure_time = last_failure_time
        if local_interface is not None:
            self.local_interface = local_interface
        if max_post_wait_time is not None:
            self.max_post_wait_time = max_post_wait_time
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if outgoing_connection_count is not None:
            self.outgoing_connection_count = outgoing_connection_count
        if remote_host is not None:
            self.remote_host = remote_host
        if remote_outgoing_connection_up_count is not None:
            self.remote_outgoing_connection_up_count = remote_outgoing_connection_up_count
        if remote_port is not None:
            self.remote_port = remote_port
        if rest_consumer_name is not None:
            self.rest_consumer_name = rest_consumer_name
        if rest_delivery_point_name is not None:
            self.rest_delivery_point_name = rest_delivery_point_name
        if retry_delay is not None:
            self.retry_delay = retry_delay
        if tls_cipher_suite_list is not None:
            self.tls_cipher_suite_list = tls_cipher_suite_list
        if tls_enabled is not None:
            self.tls_enabled = tls_enabled
        if up is not None:
            self.up = up

    @property
    def authentication_http_basic_username(self):
        """Gets the authentication_http_basic_username of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The username that the REST Consumer will use to login to the REST host.  # noqa: E501

        :return: The authentication_http_basic_username of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._authentication_http_basic_username

    @authentication_http_basic_username.setter
    def authentication_http_basic_username(self, authentication_http_basic_username):
        """Sets the authentication_http_basic_username of this MsgVpnRestDeliveryPointRestConsumer.

        The username that the REST Consumer will use to login to the REST host.  # noqa: E501

        :param authentication_http_basic_username: The authentication_http_basic_username of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._authentication_http_basic_username = authentication_http_basic_username

    @property
    def authentication_scheme(self):
        """Gets the authentication_scheme of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The authentication scheme used by the REST Consumer to login to the REST host. The allowed values and their meaning are:  <pre> \"none\" - Login with no authentication. This may be useful for anonymous connections or when a REST Consumer does not require authentication. \"http-basic\" - Login with a username and optional password according to HTTP Basic authentication as per RFC2616. \"client-certificate\" - Login with a client TLS certificate as per RFC5246. Client certificate authentication is only available on TLS connections. </pre>   # noqa: E501

        :return: The authentication_scheme of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._authentication_scheme

    @authentication_scheme.setter
    def authentication_scheme(self, authentication_scheme):
        """Sets the authentication_scheme of this MsgVpnRestDeliveryPointRestConsumer.

        The authentication scheme used by the REST Consumer to login to the REST host. The allowed values and their meaning are:  <pre> \"none\" - Login with no authentication. This may be useful for anonymous connections or when a REST Consumer does not require authentication. \"http-basic\" - Login with a username and optional password according to HTTP Basic authentication as per RFC2616. \"client-certificate\" - Login with a client TLS certificate as per RFC5246. Client certificate authentication is only available on TLS connections. </pre>   # noqa: E501

        :param authentication_scheme: The authentication_scheme of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """
        allowed_values = ["none", "http-basic", "client-certificate"]  # noqa: E501
        if authentication_scheme not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_scheme` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_scheme, allowed_values)
            )

        self._authentication_scheme = authentication_scheme

    @property
    def counter(self):
        """Gets the counter of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501


        :return: The counter of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: MsgVpnRestDeliveryPointRestConsumerCounter
        """
        return self._counter

    @counter.setter
    def counter(self, counter):
        """Sets the counter of this MsgVpnRestDeliveryPointRestConsumer.


        :param counter: The counter of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: MsgVpnRestDeliveryPointRestConsumerCounter
        """

        self._counter = counter

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        Indicates whether the REST Consumer is enabled.  # noqa: E501

        :return: The enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnRestDeliveryPointRestConsumer.

        Indicates whether the REST Consumer is enabled.  # noqa: E501

        :param enabled: The enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def last_connection_failure_local_endpoint(self):
        """Gets the last_connection_failure_local_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The local endpoint at the time of the last connection failure.  # noqa: E501

        :return: The last_connection_failure_local_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._last_connection_failure_local_endpoint

    @last_connection_failure_local_endpoint.setter
    def last_connection_failure_local_endpoint(self, last_connection_failure_local_endpoint):
        """Sets the last_connection_failure_local_endpoint of this MsgVpnRestDeliveryPointRestConsumer.

        The local endpoint at the time of the last connection failure.  # noqa: E501

        :param last_connection_failure_local_endpoint: The last_connection_failure_local_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._last_connection_failure_local_endpoint = last_connection_failure_local_endpoint

    @property
    def last_connection_failure_reason(self):
        """Gets the last_connection_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The reason for the last connection failure between local and remote endpoints.  # noqa: E501

        :return: The last_connection_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._last_connection_failure_reason

    @last_connection_failure_reason.setter
    def last_connection_failure_reason(self, last_connection_failure_reason):
        """Sets the last_connection_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.

        The reason for the last connection failure between local and remote endpoints.  # noqa: E501

        :param last_connection_failure_reason: The last_connection_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._last_connection_failure_reason = last_connection_failure_reason

    @property
    def last_connection_failure_remote_endpoint(self):
        """Gets the last_connection_failure_remote_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The remote endpoint at the time of the last connection failure.  # noqa: E501

        :return: The last_connection_failure_remote_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._last_connection_failure_remote_endpoint

    @last_connection_failure_remote_endpoint.setter
    def last_connection_failure_remote_endpoint(self, last_connection_failure_remote_endpoint):
        """Sets the last_connection_failure_remote_endpoint of this MsgVpnRestDeliveryPointRestConsumer.

        The remote endpoint at the time of the last connection failure.  # noqa: E501

        :param last_connection_failure_remote_endpoint: The last_connection_failure_remote_endpoint of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._last_connection_failure_remote_endpoint = last_connection_failure_remote_endpoint

    @property
    def last_connection_failure_time(self):
        """Gets the last_connection_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The timestamp of the last connection failure between local and remote endpoints. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_connection_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._last_connection_failure_time

    @last_connection_failure_time.setter
    def last_connection_failure_time(self, last_connection_failure_time):
        """Sets the last_connection_failure_time of this MsgVpnRestDeliveryPointRestConsumer.

        The timestamp of the last connection failure between local and remote endpoints. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_connection_failure_time: The last_connection_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._last_connection_failure_time = last_connection_failure_time

    @property
    def last_failure_reason(self):
        """Gets the last_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The reason for the last REST Consumer failure.  # noqa: E501

        :return: The last_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._last_failure_reason

    @last_failure_reason.setter
    def last_failure_reason(self, last_failure_reason):
        """Sets the last_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.

        The reason for the last REST Consumer failure.  # noqa: E501

        :param last_failure_reason: The last_failure_reason of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._last_failure_reason = last_failure_reason

    @property
    def last_failure_time(self):
        """Gets the last_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The timestamp of the last REST Consumer failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The last_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._last_failure_time

    @last_failure_time.setter
    def last_failure_time(self, last_failure_time):
        """Sets the last_failure_time of this MsgVpnRestDeliveryPointRestConsumer.

        The timestamp of the last REST Consumer failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param last_failure_time: The last_failure_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._last_failure_time = last_failure_time

    @property
    def local_interface(self):
        """Gets the local_interface of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The interface that will be used for all outgoing connections associated with the REST Consumer. When unspecified, an interface is automatically chosen.  # noqa: E501

        :return: The local_interface of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._local_interface

    @local_interface.setter
    def local_interface(self, local_interface):
        """Sets the local_interface of this MsgVpnRestDeliveryPointRestConsumer.

        The interface that will be used for all outgoing connections associated with the REST Consumer. When unspecified, an interface is automatically chosen.  # noqa: E501

        :param local_interface: The local_interface of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._local_interface = local_interface

    @property
    def max_post_wait_time(self):
        """Gets the max_post_wait_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The maximum amount of time (in seconds) to wait for an HTTP POST response from the REST Consumer. Once this time is exceeded, the TCP connection is reset.  # noqa: E501

        :return: The max_post_wait_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._max_post_wait_time

    @max_post_wait_time.setter
    def max_post_wait_time(self, max_post_wait_time):
        """Sets the max_post_wait_time of this MsgVpnRestDeliveryPointRestConsumer.

        The maximum amount of time (in seconds) to wait for an HTTP POST response from the REST Consumer. Once this time is exceeded, the TCP connection is reset.  # noqa: E501

        :param max_post_wait_time: The max_post_wait_time of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._max_post_wait_time = max_post_wait_time

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnRestDeliveryPointRestConsumer.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def outgoing_connection_count(self):
        """Gets the outgoing_connection_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The number of concurrent TCP connections open to the REST Consumer.  # noqa: E501

        :return: The outgoing_connection_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._outgoing_connection_count

    @outgoing_connection_count.setter
    def outgoing_connection_count(self, outgoing_connection_count):
        """Sets the outgoing_connection_count of this MsgVpnRestDeliveryPointRestConsumer.

        The number of concurrent TCP connections open to the REST Consumer.  # noqa: E501

        :param outgoing_connection_count: The outgoing_connection_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._outgoing_connection_count = outgoing_connection_count

    @property
    def remote_host(self):
        """Gets the remote_host of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The IP address or DNS name for the REST Consumer.  # noqa: E501

        :return: The remote_host of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._remote_host

    @remote_host.setter
    def remote_host(self, remote_host):
        """Sets the remote_host of this MsgVpnRestDeliveryPointRestConsumer.

        The IP address or DNS name for the REST Consumer.  # noqa: E501

        :param remote_host: The remote_host of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._remote_host = remote_host

    @property
    def remote_outgoing_connection_up_count(self):
        """Gets the remote_outgoing_connection_up_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The number of outgoing connections for the REST Consumer that are up.  # noqa: E501

        :return: The remote_outgoing_connection_up_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._remote_outgoing_connection_up_count

    @remote_outgoing_connection_up_count.setter
    def remote_outgoing_connection_up_count(self, remote_outgoing_connection_up_count):
        """Sets the remote_outgoing_connection_up_count of this MsgVpnRestDeliveryPointRestConsumer.

        The number of outgoing connections for the REST Consumer that are up.  # noqa: E501

        :param remote_outgoing_connection_up_count: The remote_outgoing_connection_up_count of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._remote_outgoing_connection_up_count = remote_outgoing_connection_up_count

    @property
    def remote_port(self):
        """Gets the remote_port of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The port associated with the host of the REST Consumer.  # noqa: E501

        :return: The remote_port of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._remote_port

    @remote_port.setter
    def remote_port(self, remote_port):
        """Sets the remote_port of this MsgVpnRestDeliveryPointRestConsumer.

        The port associated with the host of the REST Consumer.  # noqa: E501

        :param remote_port: The remote_port of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._remote_port = remote_port

    @property
    def rest_consumer_name(self):
        """Gets the rest_consumer_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The name of the REST Consumer.  # noqa: E501

        :return: The rest_consumer_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._rest_consumer_name

    @rest_consumer_name.setter
    def rest_consumer_name(self, rest_consumer_name):
        """Sets the rest_consumer_name of this MsgVpnRestDeliveryPointRestConsumer.

        The name of the REST Consumer.  # noqa: E501

        :param rest_consumer_name: The rest_consumer_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._rest_consumer_name = rest_consumer_name

    @property
    def rest_delivery_point_name(self):
        """Gets the rest_delivery_point_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The name of the REST Delivery Point.  # noqa: E501

        :return: The rest_delivery_point_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._rest_delivery_point_name

    @rest_delivery_point_name.setter
    def rest_delivery_point_name(self, rest_delivery_point_name):
        """Sets the rest_delivery_point_name of this MsgVpnRestDeliveryPointRestConsumer.

        The name of the REST Delivery Point.  # noqa: E501

        :param rest_delivery_point_name: The rest_delivery_point_name of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._rest_delivery_point_name = rest_delivery_point_name

    @property
    def retry_delay(self):
        """Gets the retry_delay of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The number of seconds that must pass before retrying the remote REST Consumer connection.  # noqa: E501

        :return: The retry_delay of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: int
        """
        return self._retry_delay

    @retry_delay.setter
    def retry_delay(self, retry_delay):
        """Sets the retry_delay of this MsgVpnRestDeliveryPointRestConsumer.

        The number of seconds that must pass before retrying the remote REST Consumer connection.  # noqa: E501

        :param retry_delay: The retry_delay of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: int
        """

        self._retry_delay = retry_delay

    @property
    def tls_cipher_suite_list(self):
        """Gets the tls_cipher_suite_list of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        The colon-separated list of cipher-suites the REST Consumer uses in its encrypted connection. All supported suites are included by default, from most-secure to least-secure. The REST Consumer should choose the first suite from this list that it supports.  # noqa: E501

        :return: The tls_cipher_suite_list of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: str
        """
        return self._tls_cipher_suite_list

    @tls_cipher_suite_list.setter
    def tls_cipher_suite_list(self, tls_cipher_suite_list):
        """Sets the tls_cipher_suite_list of this MsgVpnRestDeliveryPointRestConsumer.

        The colon-separated list of cipher-suites the REST Consumer uses in its encrypted connection. All supported suites are included by default, from most-secure to least-secure. The REST Consumer should choose the first suite from this list that it supports.  # noqa: E501

        :param tls_cipher_suite_list: The tls_cipher_suite_list of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: str
        """

        self._tls_cipher_suite_list = tls_cipher_suite_list

    @property
    def tls_enabled(self):
        """Gets the tls_enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        Indicates whether TLS for the REST Consumer is enabled.  # noqa: E501

        :return: The tls_enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: bool
        """
        return self._tls_enabled

    @tls_enabled.setter
    def tls_enabled(self, tls_enabled):
        """Sets the tls_enabled of this MsgVpnRestDeliveryPointRestConsumer.

        Indicates whether TLS for the REST Consumer is enabled.  # noqa: E501

        :param tls_enabled: The tls_enabled of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :type: bool
        """

        self._tls_enabled = tls_enabled

    @property
    def up(self):
        """Gets the up of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501

        Indicates whether the operational state of the REST Consumer is up.  # noqa: E501

        :return: The up of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
        :rtype: bool
        """
        return self._up

    @up.setter
    def up(self, up):
        """Sets the up of this MsgVpnRestDeliveryPointRestConsumer.

        Indicates whether the operational state of the REST Consumer is up.  # noqa: E501

        :param up: The up of this MsgVpnRestDeliveryPointRestConsumer.  # noqa: E501
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
        if issubclass(MsgVpnRestDeliveryPointRestConsumer, dict):
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
        if not isinstance(other, MsgVpnRestDeliveryPointRestConsumer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
