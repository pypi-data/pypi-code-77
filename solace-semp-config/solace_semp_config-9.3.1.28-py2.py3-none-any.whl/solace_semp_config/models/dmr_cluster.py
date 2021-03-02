# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.13
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class DmrCluster(object):
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
        'authentication_basic_enabled': 'bool',
        'authentication_basic_password': 'str',
        'authentication_basic_type': 'str',
        'authentication_client_cert_content': 'str',
        'authentication_client_cert_enabled': 'bool',
        'authentication_client_cert_password': 'str',
        'direct_only_enabled': 'bool',
        'dmr_cluster_name': 'str',
        'enabled': 'bool',
        'node_name': 'str',
        'tls_server_cert_enforce_trusted_common_name_enabled': 'bool',
        'tls_server_cert_max_chain_depth': 'int',
        'tls_server_cert_validate_date_enabled': 'bool'
    }

    attribute_map = {
        'authentication_basic_enabled': 'authenticationBasicEnabled',
        'authentication_basic_password': 'authenticationBasicPassword',
        'authentication_basic_type': 'authenticationBasicType',
        'authentication_client_cert_content': 'authenticationClientCertContent',
        'authentication_client_cert_enabled': 'authenticationClientCertEnabled',
        'authentication_client_cert_password': 'authenticationClientCertPassword',
        'direct_only_enabled': 'directOnlyEnabled',
        'dmr_cluster_name': 'dmrClusterName',
        'enabled': 'enabled',
        'node_name': 'nodeName',
        'tls_server_cert_enforce_trusted_common_name_enabled': 'tlsServerCertEnforceTrustedCommonNameEnabled',
        'tls_server_cert_max_chain_depth': 'tlsServerCertMaxChainDepth',
        'tls_server_cert_validate_date_enabled': 'tlsServerCertValidateDateEnabled'
    }

    def __init__(self, authentication_basic_enabled=None, authentication_basic_password=None, authentication_basic_type=None, authentication_client_cert_content=None, authentication_client_cert_enabled=None, authentication_client_cert_password=None, direct_only_enabled=None, dmr_cluster_name=None, enabled=None, node_name=None, tls_server_cert_enforce_trusted_common_name_enabled=None, tls_server_cert_max_chain_depth=None, tls_server_cert_validate_date_enabled=None):  # noqa: E501
        """DmrCluster - a model defined in Swagger"""  # noqa: E501

        self._authentication_basic_enabled = None
        self._authentication_basic_password = None
        self._authentication_basic_type = None
        self._authentication_client_cert_content = None
        self._authentication_client_cert_enabled = None
        self._authentication_client_cert_password = None
        self._direct_only_enabled = None
        self._dmr_cluster_name = None
        self._enabled = None
        self._node_name = None
        self._tls_server_cert_enforce_trusted_common_name_enabled = None
        self._tls_server_cert_max_chain_depth = None
        self._tls_server_cert_validate_date_enabled = None
        self.discriminator = None

        if authentication_basic_enabled is not None:
            self.authentication_basic_enabled = authentication_basic_enabled
        if authentication_basic_password is not None:
            self.authentication_basic_password = authentication_basic_password
        if authentication_basic_type is not None:
            self.authentication_basic_type = authentication_basic_type
        if authentication_client_cert_content is not None:
            self.authentication_client_cert_content = authentication_client_cert_content
        if authentication_client_cert_enabled is not None:
            self.authentication_client_cert_enabled = authentication_client_cert_enabled
        if authentication_client_cert_password is not None:
            self.authentication_client_cert_password = authentication_client_cert_password
        if direct_only_enabled is not None:
            self.direct_only_enabled = direct_only_enabled
        if dmr_cluster_name is not None:
            self.dmr_cluster_name = dmr_cluster_name
        if enabled is not None:
            self.enabled = enabled
        if node_name is not None:
            self.node_name = node_name
        if tls_server_cert_enforce_trusted_common_name_enabled is not None:
            self.tls_server_cert_enforce_trusted_common_name_enabled = tls_server_cert_enforce_trusted_common_name_enabled
        if tls_server_cert_max_chain_depth is not None:
            self.tls_server_cert_max_chain_depth = tls_server_cert_max_chain_depth
        if tls_server_cert_validate_date_enabled is not None:
            self.tls_server_cert_validate_date_enabled = tls_server_cert_validate_date_enabled

    @property
    def authentication_basic_enabled(self):
        """Gets the authentication_basic_enabled of this DmrCluster.  # noqa: E501

        Enable or disable basic authentication for Cluster Links. The default value is `true`.  # noqa: E501

        :return: The authentication_basic_enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_basic_enabled

    @authentication_basic_enabled.setter
    def authentication_basic_enabled(self, authentication_basic_enabled):
        """Sets the authentication_basic_enabled of this DmrCluster.

        Enable or disable basic authentication for Cluster Links. The default value is `true`.  # noqa: E501

        :param authentication_basic_enabled: The authentication_basic_enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._authentication_basic_enabled = authentication_basic_enabled

    @property
    def authentication_basic_password(self):
        """Gets the authentication_basic_password of this DmrCluster.  # noqa: E501

        The password used to authenticate incoming Cluster Links when using basic internal authentication. The same password is also used by outgoing Cluster Links if a per-Link password is not configured. This attribute is absent from a GET and not updated when absent in a PUT. The default is to have no `authenticationBasicPassword`.  # noqa: E501

        :return: The authentication_basic_password of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._authentication_basic_password

    @authentication_basic_password.setter
    def authentication_basic_password(self, authentication_basic_password):
        """Sets the authentication_basic_password of this DmrCluster.

        The password used to authenticate incoming Cluster Links when using basic internal authentication. The same password is also used by outgoing Cluster Links if a per-Link password is not configured. This attribute is absent from a GET and not updated when absent in a PUT. The default is to have no `authenticationBasicPassword`.  # noqa: E501

        :param authentication_basic_password: The authentication_basic_password of this DmrCluster.  # noqa: E501
        :type: str
        """

        self._authentication_basic_password = authentication_basic_password

    @property
    def authentication_basic_type(self):
        """Gets the authentication_basic_type of this DmrCluster.  # noqa: E501

        The type of basic authentication to use for Cluster Links. The default value is `\"internal\"`. The allowed values and their meaning are:  <pre> \"internal\" - Use locally configured password. \"none\" - No authentication. </pre>   # noqa: E501

        :return: The authentication_basic_type of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._authentication_basic_type

    @authentication_basic_type.setter
    def authentication_basic_type(self, authentication_basic_type):
        """Sets the authentication_basic_type of this DmrCluster.

        The type of basic authentication to use for Cluster Links. The default value is `\"internal\"`. The allowed values and their meaning are:  <pre> \"internal\" - Use locally configured password. \"none\" - No authentication. </pre>   # noqa: E501

        :param authentication_basic_type: The authentication_basic_type of this DmrCluster.  # noqa: E501
        :type: str
        """
        allowed_values = ["internal", "none"]  # noqa: E501
        if authentication_basic_type not in allowed_values:
            raise ValueError(
                "Invalid value for `authentication_basic_type` ({0}), must be one of {1}"  # noqa: E501
                .format(authentication_basic_type, allowed_values)
            )

        self._authentication_basic_type = authentication_basic_type

    @property
    def authentication_client_cert_content(self):
        """Gets the authentication_client_cert_content of this DmrCluster.  # noqa: E501

        The PEM formatted content for the client certificate used to login to the remote node. It must consist of a private key and between one and three certificates comprising the certificate trust chain. This attribute is absent from a GET and not updated when absent in a PUT. Changing this attribute requires an HTTPS connection. The default value is `\"\"`.  # noqa: E501

        :return: The authentication_client_cert_content of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._authentication_client_cert_content

    @authentication_client_cert_content.setter
    def authentication_client_cert_content(self, authentication_client_cert_content):
        """Sets the authentication_client_cert_content of this DmrCluster.

        The PEM formatted content for the client certificate used to login to the remote node. It must consist of a private key and between one and three certificates comprising the certificate trust chain. This attribute is absent from a GET and not updated when absent in a PUT. Changing this attribute requires an HTTPS connection. The default value is `\"\"`.  # noqa: E501

        :param authentication_client_cert_content: The authentication_client_cert_content of this DmrCluster.  # noqa: E501
        :type: str
        """

        self._authentication_client_cert_content = authentication_client_cert_content

    @property
    def authentication_client_cert_enabled(self):
        """Gets the authentication_client_cert_enabled of this DmrCluster.  # noqa: E501

        Enable or disable client certificate authentication for Cluster Links. The default value is `true`.  # noqa: E501

        :return: The authentication_client_cert_enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._authentication_client_cert_enabled

    @authentication_client_cert_enabled.setter
    def authentication_client_cert_enabled(self, authentication_client_cert_enabled):
        """Sets the authentication_client_cert_enabled of this DmrCluster.

        Enable or disable client certificate authentication for Cluster Links. The default value is `true`.  # noqa: E501

        :param authentication_client_cert_enabled: The authentication_client_cert_enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._authentication_client_cert_enabled = authentication_client_cert_enabled

    @property
    def authentication_client_cert_password(self):
        """Gets the authentication_client_cert_password of this DmrCluster.  # noqa: E501

        The password for the client certificate. This attribute is absent from a GET and not updated when absent in a PUT. Changing this attribute requires an HTTPS connection. The default value is `\"\"`.  # noqa: E501

        :return: The authentication_client_cert_password of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._authentication_client_cert_password

    @authentication_client_cert_password.setter
    def authentication_client_cert_password(self, authentication_client_cert_password):
        """Sets the authentication_client_cert_password of this DmrCluster.

        The password for the client certificate. This attribute is absent from a GET and not updated when absent in a PUT. Changing this attribute requires an HTTPS connection. The default value is `\"\"`.  # noqa: E501

        :param authentication_client_cert_password: The authentication_client_cert_password of this DmrCluster.  # noqa: E501
        :type: str
        """

        self._authentication_client_cert_password = authentication_client_cert_password

    @property
    def direct_only_enabled(self):
        """Gets the direct_only_enabled of this DmrCluster.  # noqa: E501

        Enable or disable direct messaging only. Guaranteed messages will not be transmitted through the cluster. The default value is `false`.  # noqa: E501

        :return: The direct_only_enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._direct_only_enabled

    @direct_only_enabled.setter
    def direct_only_enabled(self, direct_only_enabled):
        """Sets the direct_only_enabled of this DmrCluster.

        Enable or disable direct messaging only. Guaranteed messages will not be transmitted through the cluster. The default value is `false`.  # noqa: E501

        :param direct_only_enabled: The direct_only_enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._direct_only_enabled = direct_only_enabled

    @property
    def dmr_cluster_name(self):
        """Gets the dmr_cluster_name of this DmrCluster.  # noqa: E501

        The name of the Cluster.  # noqa: E501

        :return: The dmr_cluster_name of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._dmr_cluster_name

    @dmr_cluster_name.setter
    def dmr_cluster_name(self, dmr_cluster_name):
        """Sets the dmr_cluster_name of this DmrCluster.

        The name of the Cluster.  # noqa: E501

        :param dmr_cluster_name: The dmr_cluster_name of this DmrCluster.  # noqa: E501
        :type: str
        """

        self._dmr_cluster_name = dmr_cluster_name

    @property
    def enabled(self):
        """Gets the enabled of this DmrCluster.  # noqa: E501

        Enable or disable the Cluster. The default value is `false`.  # noqa: E501

        :return: The enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this DmrCluster.

        Enable or disable the Cluster. The default value is `false`.  # noqa: E501

        :param enabled: The enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def node_name(self):
        """Gets the node_name of this DmrCluster.  # noqa: E501

        The name of this node in the Cluster. This is the name that this broker (or redundant group of brokers) is know by to other nodes in the Cluster. The name is chosen automatically to be either this broker's Router Name or Mate Router Name, depending on which Active Standby Role (primary or backup) this broker plays in its redundancy group.  # noqa: E501

        :return: The node_name of this DmrCluster.  # noqa: E501
        :rtype: str
        """
        return self._node_name

    @node_name.setter
    def node_name(self, node_name):
        """Sets the node_name of this DmrCluster.

        The name of this node in the Cluster. This is the name that this broker (or redundant group of brokers) is know by to other nodes in the Cluster. The name is chosen automatically to be either this broker's Router Name or Mate Router Name, depending on which Active Standby Role (primary or backup) this broker plays in its redundancy group.  # noqa: E501

        :param node_name: The node_name of this DmrCluster.  # noqa: E501
        :type: str
        """

        self._node_name = node_name

    @property
    def tls_server_cert_enforce_trusted_common_name_enabled(self):
        """Gets the tls_server_cert_enforce_trusted_common_name_enabled of this DmrCluster.  # noqa: E501

        Enable or disable the enforcing of the common name provided by the remote broker against the list of trusted common names configured for the Link. If enabled, the certificate's common name must match one of the trusted common names for the Link to be accepted. The default value is `true`.  # noqa: E501

        :return: The tls_server_cert_enforce_trusted_common_name_enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._tls_server_cert_enforce_trusted_common_name_enabled

    @tls_server_cert_enforce_trusted_common_name_enabled.setter
    def tls_server_cert_enforce_trusted_common_name_enabled(self, tls_server_cert_enforce_trusted_common_name_enabled):
        """Sets the tls_server_cert_enforce_trusted_common_name_enabled of this DmrCluster.

        Enable or disable the enforcing of the common name provided by the remote broker against the list of trusted common names configured for the Link. If enabled, the certificate's common name must match one of the trusted common names for the Link to be accepted. The default value is `true`.  # noqa: E501

        :param tls_server_cert_enforce_trusted_common_name_enabled: The tls_server_cert_enforce_trusted_common_name_enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._tls_server_cert_enforce_trusted_common_name_enabled = tls_server_cert_enforce_trusted_common_name_enabled

    @property
    def tls_server_cert_max_chain_depth(self):
        """Gets the tls_server_cert_max_chain_depth of this DmrCluster.  # noqa: E501

        The maximum allowed depth of a certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate. The default value is `3`.  # noqa: E501

        :return: The tls_server_cert_max_chain_depth of this DmrCluster.  # noqa: E501
        :rtype: int
        """
        return self._tls_server_cert_max_chain_depth

    @tls_server_cert_max_chain_depth.setter
    def tls_server_cert_max_chain_depth(self, tls_server_cert_max_chain_depth):
        """Sets the tls_server_cert_max_chain_depth of this DmrCluster.

        The maximum allowed depth of a certificate chain. The depth of a chain is defined as the number of signing CA certificates that are present in the chain back to a trusted self-signed root CA certificate. The default value is `3`.  # noqa: E501

        :param tls_server_cert_max_chain_depth: The tls_server_cert_max_chain_depth of this DmrCluster.  # noqa: E501
        :type: int
        """

        self._tls_server_cert_max_chain_depth = tls_server_cert_max_chain_depth

    @property
    def tls_server_cert_validate_date_enabled(self):
        """Gets the tls_server_cert_validate_date_enabled of this DmrCluster.  # noqa: E501

        Enable or disable the validation of the \"Not Before\" and \"Not After\" validity dates in the certificate. When disabled, the certificate is accepted even if the certificate is not valid based on these dates. The default value is `true`.  # noqa: E501

        :return: The tls_server_cert_validate_date_enabled of this DmrCluster.  # noqa: E501
        :rtype: bool
        """
        return self._tls_server_cert_validate_date_enabled

    @tls_server_cert_validate_date_enabled.setter
    def tls_server_cert_validate_date_enabled(self, tls_server_cert_validate_date_enabled):
        """Sets the tls_server_cert_validate_date_enabled of this DmrCluster.

        Enable or disable the validation of the \"Not Before\" and \"Not After\" validity dates in the certificate. When disabled, the certificate is accepted even if the certificate is not valid based on these dates. The default value is `true`.  # noqa: E501

        :param tls_server_cert_validate_date_enabled: The tls_server_cert_validate_date_enabled of this DmrCluster.  # noqa: E501
        :type: bool
        """

        self._tls_server_cert_validate_date_enabled = tls_server_cert_validate_date_enabled

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
        if issubclass(DmrCluster, dict):
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
        if not isinstance(other, DmrCluster):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
