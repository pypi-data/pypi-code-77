# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.14
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgVpnAuthenticationOauthProvider(object):
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
        'audience_claim_name': 'str',
        'audience_claim_source': 'str',
        'audience_claim_value': 'str',
        'audience_validation_enabled': 'bool',
        'authorization_group_claim_name': 'str',
        'authorization_group_claim_source': 'str',
        'authorization_group_enabled': 'bool',
        'disconnect_on_token_expiration_enabled': 'bool',
        'enabled': 'bool',
        'jwks_refresh_interval': 'int',
        'jwks_uri': 'str',
        'msg_vpn_name': 'str',
        'oauth_provider_name': 'str',
        'token_ignore_time_limits_enabled': 'bool',
        'token_introspection_parameter_name': 'str',
        'token_introspection_password': 'str',
        'token_introspection_timeout': 'int',
        'token_introspection_uri': 'str',
        'token_introspection_username': 'str',
        'username_claim_name': 'str',
        'username_claim_source': 'str',
        'username_validate_enabled': 'bool'
    }

    attribute_map = {
        'audience_claim_name': 'audienceClaimName',
        'audience_claim_source': 'audienceClaimSource',
        'audience_claim_value': 'audienceClaimValue',
        'audience_validation_enabled': 'audienceValidationEnabled',
        'authorization_group_claim_name': 'authorizationGroupClaimName',
        'authorization_group_claim_source': 'authorizationGroupClaimSource',
        'authorization_group_enabled': 'authorizationGroupEnabled',
        'disconnect_on_token_expiration_enabled': 'disconnectOnTokenExpirationEnabled',
        'enabled': 'enabled',
        'jwks_refresh_interval': 'jwksRefreshInterval',
        'jwks_uri': 'jwksUri',
        'msg_vpn_name': 'msgVpnName',
        'oauth_provider_name': 'oauthProviderName',
        'token_ignore_time_limits_enabled': 'tokenIgnoreTimeLimitsEnabled',
        'token_introspection_parameter_name': 'tokenIntrospectionParameterName',
        'token_introspection_password': 'tokenIntrospectionPassword',
        'token_introspection_timeout': 'tokenIntrospectionTimeout',
        'token_introspection_uri': 'tokenIntrospectionUri',
        'token_introspection_username': 'tokenIntrospectionUsername',
        'username_claim_name': 'usernameClaimName',
        'username_claim_source': 'usernameClaimSource',
        'username_validate_enabled': 'usernameValidateEnabled'
    }

    def __init__(self, audience_claim_name=None, audience_claim_source=None, audience_claim_value=None, audience_validation_enabled=None, authorization_group_claim_name=None, authorization_group_claim_source=None, authorization_group_enabled=None, disconnect_on_token_expiration_enabled=None, enabled=None, jwks_refresh_interval=None, jwks_uri=None, msg_vpn_name=None, oauth_provider_name=None, token_ignore_time_limits_enabled=None, token_introspection_parameter_name=None, token_introspection_password=None, token_introspection_timeout=None, token_introspection_uri=None, token_introspection_username=None, username_claim_name=None, username_claim_source=None, username_validate_enabled=None):  # noqa: E501
        """MsgVpnAuthenticationOauthProvider - a model defined in Swagger"""  # noqa: E501

        self._audience_claim_name = None
        self._audience_claim_source = None
        self._audience_claim_value = None
        self._audience_validation_enabled = None
        self._authorization_group_claim_name = None
        self._authorization_group_claim_source = None
        self._authorization_group_enabled = None
        self._disconnect_on_token_expiration_enabled = None
        self._enabled = None
        self._jwks_refresh_interval = None
        self._jwks_uri = None
        self._msg_vpn_name = None
        self._oauth_provider_name = None
        self._token_ignore_time_limits_enabled = None
        self._token_introspection_parameter_name = None
        self._token_introspection_password = None
        self._token_introspection_timeout = None
        self._token_introspection_uri = None
        self._token_introspection_username = None
        self._username_claim_name = None
        self._username_claim_source = None
        self._username_validate_enabled = None
        self.discriminator = None

        if audience_claim_name is not None:
            self.audience_claim_name = audience_claim_name
        if audience_claim_source is not None:
            self.audience_claim_source = audience_claim_source
        if audience_claim_value is not None:
            self.audience_claim_value = audience_claim_value
        if audience_validation_enabled is not None:
            self.audience_validation_enabled = audience_validation_enabled
        if authorization_group_claim_name is not None:
            self.authorization_group_claim_name = authorization_group_claim_name
        if authorization_group_claim_source is not None:
            self.authorization_group_claim_source = authorization_group_claim_source
        if authorization_group_enabled is not None:
            self.authorization_group_enabled = authorization_group_enabled
        if disconnect_on_token_expiration_enabled is not None:
            self.disconnect_on_token_expiration_enabled = disconnect_on_token_expiration_enabled
        if enabled is not None:
            self.enabled = enabled
        if jwks_refresh_interval is not None:
            self.jwks_refresh_interval = jwks_refresh_interval
        if jwks_uri is not None:
            self.jwks_uri = jwks_uri
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if oauth_provider_name is not None:
            self.oauth_provider_name = oauth_provider_name
        if token_ignore_time_limits_enabled is not None:
            self.token_ignore_time_limits_enabled = token_ignore_time_limits_enabled
        if token_introspection_parameter_name is not None:
            self.token_introspection_parameter_name = token_introspection_parameter_name
        if token_introspection_password is not None:
            self.token_introspection_password = token_introspection_password
        if token_introspection_timeout is not None:
            self.token_introspection_timeout = token_introspection_timeout
        if token_introspection_uri is not None:
            self.token_introspection_uri = token_introspection_uri
        if token_introspection_username is not None:
            self.token_introspection_username = token_introspection_username
        if username_claim_name is not None:
            self.username_claim_name = username_claim_name
        if username_claim_source is not None:
            self.username_claim_source = username_claim_source
        if username_validate_enabled is not None:
            self.username_validate_enabled = username_validate_enabled

    @property
    def audience_claim_name(self):
        """Gets the audience_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The audience claim name, indicating which part of the object to use for determining the audience. The default value is `\"aud\"`.  # noqa: E501

        :return: The audience_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._audience_claim_name

    @audience_claim_name.setter
    def audience_claim_name(self, audience_claim_name):
        """Sets the audience_claim_name of this MsgVpnAuthenticationOauthProvider.

        The audience claim name, indicating which part of the object to use for determining the audience. The default value is `\"aud\"`.  # noqa: E501

        :param audience_claim_name: The audience_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._audience_claim_name = audience_claim_name

    @property
    def audience_claim_source(self):
        """Gets the audience_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The audience claim source, indicating where to search for the audience value. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the audience value. \"id-token\" - Search the ID type JWT for the audience value. \"introspection\" - Introspect the access token and search the result for the audience value. </pre>   # noqa: E501

        :return: The audience_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._audience_claim_source

    @audience_claim_source.setter
    def audience_claim_source(self, audience_claim_source):
        """Sets the audience_claim_source of this MsgVpnAuthenticationOauthProvider.

        The audience claim source, indicating where to search for the audience value. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the audience value. \"id-token\" - Search the ID type JWT for the audience value. \"introspection\" - Introspect the access token and search the result for the audience value. </pre>   # noqa: E501

        :param audience_claim_source: The audience_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """
        allowed_values = ["access-token", "id-token", "introspection"]  # noqa: E501
        if audience_claim_source not in allowed_values:
            raise ValueError(
                "Invalid value for `audience_claim_source` ({0}), must be one of {1}"  # noqa: E501
                .format(audience_claim_source, allowed_values)
            )

        self._audience_claim_source = audience_claim_source

    @property
    def audience_claim_value(self):
        """Gets the audience_claim_value of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The required audience value for a token to be considered valid. The default value is `\"\"`.  # noqa: E501

        :return: The audience_claim_value of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._audience_claim_value

    @audience_claim_value.setter
    def audience_claim_value(self, audience_claim_value):
        """Sets the audience_claim_value of this MsgVpnAuthenticationOauthProvider.

        The required audience value for a token to be considered valid. The default value is `\"\"`.  # noqa: E501

        :param audience_claim_value: The audience_claim_value of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._audience_claim_value = audience_claim_value

    @property
    def audience_validation_enabled(self):
        """Gets the audience_validation_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable audience validation. The default value is `false`.  # noqa: E501

        :return: The audience_validation_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._audience_validation_enabled

    @audience_validation_enabled.setter
    def audience_validation_enabled(self, audience_validation_enabled):
        """Sets the audience_validation_enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable audience validation. The default value is `false`.  # noqa: E501

        :param audience_validation_enabled: The audience_validation_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._audience_validation_enabled = audience_validation_enabled

    @property
    def authorization_group_claim_name(self):
        """Gets the authorization_group_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The authorization group claim name, indicating which part of the object to use for determining the authorization group. The default value is `\"scope\"`.  # noqa: E501

        :return: The authorization_group_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._authorization_group_claim_name

    @authorization_group_claim_name.setter
    def authorization_group_claim_name(self, authorization_group_claim_name):
        """Sets the authorization_group_claim_name of this MsgVpnAuthenticationOauthProvider.

        The authorization group claim name, indicating which part of the object to use for determining the authorization group. The default value is `\"scope\"`.  # noqa: E501

        :param authorization_group_claim_name: The authorization_group_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._authorization_group_claim_name = authorization_group_claim_name

    @property
    def authorization_group_claim_source(self):
        """Gets the authorization_group_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The authorization group claim source, indicating where to search for the authorization group name. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the authorization group name. \"id-token\" - Search the ID type JWT for the authorization group name. \"introspection\" - Introspect the access token and search the result for the authorization group name. </pre>   # noqa: E501

        :return: The authorization_group_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._authorization_group_claim_source

    @authorization_group_claim_source.setter
    def authorization_group_claim_source(self, authorization_group_claim_source):
        """Sets the authorization_group_claim_source of this MsgVpnAuthenticationOauthProvider.

        The authorization group claim source, indicating where to search for the authorization group name. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the authorization group name. \"id-token\" - Search the ID type JWT for the authorization group name. \"introspection\" - Introspect the access token and search the result for the authorization group name. </pre>   # noqa: E501

        :param authorization_group_claim_source: The authorization_group_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """
        allowed_values = ["access-token", "id-token", "introspection"]  # noqa: E501
        if authorization_group_claim_source not in allowed_values:
            raise ValueError(
                "Invalid value for `authorization_group_claim_source` ({0}), must be one of {1}"  # noqa: E501
                .format(authorization_group_claim_source, allowed_values)
            )

        self._authorization_group_claim_source = authorization_group_claim_source

    @property
    def authorization_group_enabled(self):
        """Gets the authorization_group_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable OAuth based authorization. When enabled, the configured authorization type for OAuth clients is overridden. The default value is `false`.  # noqa: E501

        :return: The authorization_group_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._authorization_group_enabled

    @authorization_group_enabled.setter
    def authorization_group_enabled(self, authorization_group_enabled):
        """Sets the authorization_group_enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable OAuth based authorization. When enabled, the configured authorization type for OAuth clients is overridden. The default value is `false`.  # noqa: E501

        :param authorization_group_enabled: The authorization_group_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._authorization_group_enabled = authorization_group_enabled

    @property
    def disconnect_on_token_expiration_enabled(self):
        """Gets the disconnect_on_token_expiration_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable the disconnection of clients when their tokens expire. Changing this value does not affect existing clients, only new client connections. The default value is `true`.  # noqa: E501

        :return: The disconnect_on_token_expiration_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._disconnect_on_token_expiration_enabled

    @disconnect_on_token_expiration_enabled.setter
    def disconnect_on_token_expiration_enabled(self, disconnect_on_token_expiration_enabled):
        """Sets the disconnect_on_token_expiration_enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable the disconnection of clients when their tokens expire. Changing this value does not affect existing clients, only new client connections. The default value is `true`.  # noqa: E501

        :param disconnect_on_token_expiration_enabled: The disconnect_on_token_expiration_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._disconnect_on_token_expiration_enabled = disconnect_on_token_expiration_enabled

    @property
    def enabled(self):
        """Gets the enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable OAuth Provider client authentication. The default value is `false`.  # noqa: E501

        :return: The enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable OAuth Provider client authentication. The default value is `false`.  # noqa: E501

        :param enabled: The enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def jwks_refresh_interval(self):
        """Gets the jwks_refresh_interval of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The number of seconds between forced JWKS public key refreshing. The default value is `86400`.  # noqa: E501

        :return: The jwks_refresh_interval of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: int
        """
        return self._jwks_refresh_interval

    @jwks_refresh_interval.setter
    def jwks_refresh_interval(self, jwks_refresh_interval):
        """Sets the jwks_refresh_interval of this MsgVpnAuthenticationOauthProvider.

        The number of seconds between forced JWKS public key refreshing. The default value is `86400`.  # noqa: E501

        :param jwks_refresh_interval: The jwks_refresh_interval of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: int
        """

        self._jwks_refresh_interval = jwks_refresh_interval

    @property
    def jwks_uri(self):
        """Gets the jwks_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The URI where the OAuth provider publishes its JWKS public keys. The default value is `\"\"`.  # noqa: E501

        :return: The jwks_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._jwks_uri

    @jwks_uri.setter
    def jwks_uri(self, jwks_uri):
        """Sets the jwks_uri of this MsgVpnAuthenticationOauthProvider.

        The URI where the OAuth provider publishes its JWKS public keys. The default value is `\"\"`.  # noqa: E501

        :param jwks_uri: The jwks_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._jwks_uri = jwks_uri

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnAuthenticationOauthProvider.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def oauth_provider_name(self):
        """Gets the oauth_provider_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The name of the OAuth Provider.  # noqa: E501

        :return: The oauth_provider_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._oauth_provider_name

    @oauth_provider_name.setter
    def oauth_provider_name(self, oauth_provider_name):
        """Sets the oauth_provider_name of this MsgVpnAuthenticationOauthProvider.

        The name of the OAuth Provider.  # noqa: E501

        :param oauth_provider_name: The oauth_provider_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._oauth_provider_name = oauth_provider_name

    @property
    def token_ignore_time_limits_enabled(self):
        """Gets the token_ignore_time_limits_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable whether to ignore time limits and accept tokens that are not yet valid or are no longer valid. The default value is `false`.  # noqa: E501

        :return: The token_ignore_time_limits_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._token_ignore_time_limits_enabled

    @token_ignore_time_limits_enabled.setter
    def token_ignore_time_limits_enabled(self, token_ignore_time_limits_enabled):
        """Sets the token_ignore_time_limits_enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable whether to ignore time limits and accept tokens that are not yet valid or are no longer valid. The default value is `false`.  # noqa: E501

        :param token_ignore_time_limits_enabled: The token_ignore_time_limits_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._token_ignore_time_limits_enabled = token_ignore_time_limits_enabled

    @property
    def token_introspection_parameter_name(self):
        """Gets the token_introspection_parameter_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The parameter name used to identify the token during access token introspection. A standards compliant OAuth introspection server expects \"token\". The default value is `\"token\"`.  # noqa: E501

        :return: The token_introspection_parameter_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._token_introspection_parameter_name

    @token_introspection_parameter_name.setter
    def token_introspection_parameter_name(self, token_introspection_parameter_name):
        """Sets the token_introspection_parameter_name of this MsgVpnAuthenticationOauthProvider.

        The parameter name used to identify the token during access token introspection. A standards compliant OAuth introspection server expects \"token\". The default value is `\"token\"`.  # noqa: E501

        :param token_introspection_parameter_name: The token_introspection_parameter_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._token_introspection_parameter_name = token_introspection_parameter_name

    @property
    def token_introspection_password(self):
        """Gets the token_introspection_password of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The password to use when logging into the token introspection URI. This attribute is absent from a GET and not updated when absent in a PUT. The default value is `\"\"`.  # noqa: E501

        :return: The token_introspection_password of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._token_introspection_password

    @token_introspection_password.setter
    def token_introspection_password(self, token_introspection_password):
        """Sets the token_introspection_password of this MsgVpnAuthenticationOauthProvider.

        The password to use when logging into the token introspection URI. This attribute is absent from a GET and not updated when absent in a PUT. The default value is `\"\"`.  # noqa: E501

        :param token_introspection_password: The token_introspection_password of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._token_introspection_password = token_introspection_password

    @property
    def token_introspection_timeout(self):
        """Gets the token_introspection_timeout of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The maximum time in seconds a token introspection is allowed to take. The default value is `1`.  # noqa: E501

        :return: The token_introspection_timeout of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: int
        """
        return self._token_introspection_timeout

    @token_introspection_timeout.setter
    def token_introspection_timeout(self, token_introspection_timeout):
        """Sets the token_introspection_timeout of this MsgVpnAuthenticationOauthProvider.

        The maximum time in seconds a token introspection is allowed to take. The default value is `1`.  # noqa: E501

        :param token_introspection_timeout: The token_introspection_timeout of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: int
        """

        self._token_introspection_timeout = token_introspection_timeout

    @property
    def token_introspection_uri(self):
        """Gets the token_introspection_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The token introspection URI of the OAuth authentication server. The default value is `\"\"`.  # noqa: E501

        :return: The token_introspection_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._token_introspection_uri

    @token_introspection_uri.setter
    def token_introspection_uri(self, token_introspection_uri):
        """Sets the token_introspection_uri of this MsgVpnAuthenticationOauthProvider.

        The token introspection URI of the OAuth authentication server. The default value is `\"\"`.  # noqa: E501

        :param token_introspection_uri: The token_introspection_uri of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._token_introspection_uri = token_introspection_uri

    @property
    def token_introspection_username(self):
        """Gets the token_introspection_username of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The username to use when logging into the token introspection URI. The default value is `\"\"`.  # noqa: E501

        :return: The token_introspection_username of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._token_introspection_username

    @token_introspection_username.setter
    def token_introspection_username(self, token_introspection_username):
        """Sets the token_introspection_username of this MsgVpnAuthenticationOauthProvider.

        The username to use when logging into the token introspection URI. The default value is `\"\"`.  # noqa: E501

        :param token_introspection_username: The token_introspection_username of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._token_introspection_username = token_introspection_username

    @property
    def username_claim_name(self):
        """Gets the username_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The username claim name, indicating which part of the object to use for determining the username. The default value is `\"sub\"`.  # noqa: E501

        :return: The username_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._username_claim_name

    @username_claim_name.setter
    def username_claim_name(self, username_claim_name):
        """Sets the username_claim_name of this MsgVpnAuthenticationOauthProvider.

        The username claim name, indicating which part of the object to use for determining the username. The default value is `\"sub\"`.  # noqa: E501

        :param username_claim_name: The username_claim_name of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """

        self._username_claim_name = username_claim_name

    @property
    def username_claim_source(self):
        """Gets the username_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        The username claim source, indicating where to search for the username value. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the username value. \"id-token\" - Search the ID type JWT for the username value. \"introspection\" - Introspect the access token and search the result for the username value. </pre>   # noqa: E501

        :return: The username_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: str
        """
        return self._username_claim_source

    @username_claim_source.setter
    def username_claim_source(self, username_claim_source):
        """Sets the username_claim_source of this MsgVpnAuthenticationOauthProvider.

        The username claim source, indicating where to search for the username value. The default value is `\"id-token\"`. The allowed values and their meaning are:  <pre> \"access-token\" - Search the access type JWT for the username value. \"id-token\" - Search the ID type JWT for the username value. \"introspection\" - Introspect the access token and search the result for the username value. </pre>   # noqa: E501

        :param username_claim_source: The username_claim_source of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: str
        """
        allowed_values = ["access-token", "id-token", "introspection"]  # noqa: E501
        if username_claim_source not in allowed_values:
            raise ValueError(
                "Invalid value for `username_claim_source` ({0}), must be one of {1}"  # noqa: E501
                .format(username_claim_source, allowed_values)
            )

        self._username_claim_source = username_claim_source

    @property
    def username_validate_enabled(self):
        """Gets the username_validate_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501

        Enable or disable whether the API provided username will be validated against the username calculated from the token(s). The default value is `false`.  # noqa: E501

        :return: The username_validate_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :rtype: bool
        """
        return self._username_validate_enabled

    @username_validate_enabled.setter
    def username_validate_enabled(self, username_validate_enabled):
        """Sets the username_validate_enabled of this MsgVpnAuthenticationOauthProvider.

        Enable or disable whether the API provided username will be validated against the username calculated from the token(s). The default value is `false`.  # noqa: E501

        :param username_validate_enabled: The username_validate_enabled of this MsgVpnAuthenticationOauthProvider.  # noqa: E501
        :type: bool
        """

        self._username_validate_enabled = username_validate_enabled

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
        if issubclass(MsgVpnAuthenticationOauthProvider, dict):
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
        if not isinstance(other, MsgVpnAuthenticationOauthProvider):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
