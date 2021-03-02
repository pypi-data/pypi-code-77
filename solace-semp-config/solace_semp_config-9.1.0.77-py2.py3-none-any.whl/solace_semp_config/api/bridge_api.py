# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the  action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is a hidden maximum as to prevent overloading the system. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.11.00901000077
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from solace_semp_config.api_client import ApiClient


class BridgeApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_msg_vpn_bridge(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Create a Bridge object.  # noqa: E501

        Create a Bridge object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| msgVpnName|x||x|| remoteAuthenticationBasicPassword||||x| remoteAuthenticationClientCertContent||||x| remoteAuthenticationClientCertPassword||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_bridge_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_bridge_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_bridge_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Create a Bridge object.  # noqa: E501

        Create a Bridge object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| msgVpnName|x||x|| remoteAuthenticationBasicPassword||||x| remoteAuthenticationClientCertContent||||x| remoteAuthenticationClientCertPassword||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Remote Message VPN object.  # noqa: E501

        Create a Remote Message VPN object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| msgVpnName|x||x|| password||||x| remoteMsgVpnInterface|x|||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x|||    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_bridge_remote_msg_vpn_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Remote Message VPN object.  # noqa: E501

        Create a Remote Message VPN object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| msgVpnName|x||x|| password||||x| remoteMsgVpnInterface|x|||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x|||    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_bridge_remote_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `create_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `create_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteMsgVpnResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_msg_vpn_bridge_remote_subscription(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Remote Subscription object.  # noqa: E501

        Create a Remote Subscription object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| deliverAlwaysEnabled||x||| msgVpnName|x||x|| remoteSubscriptionTopic|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_remote_subscription(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeRemoteSubscription body: The Remote Subscription object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_bridge_remote_subscription_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Remote Subscription object.  # noqa: E501

        Create a Remote Subscription object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| deliverAlwaysEnabled||x||| msgVpnName|x||x|| remoteSubscriptionTopic|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeRemoteSubscription body: The Remote Subscription object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_bridge_remote_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `create_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `create_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_bridge_remote_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteSubscriptions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_msg_vpn_bridge_tls_trusted_common_name(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Trusted Common Name object.  # noqa: E501

        Create a Trusted Common Name object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| msgVpnName|x||x|| tlsTrustedCommonName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_tls_trusted_common_name(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeTlsTrustedCommonName body: The Trusted Common Name object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_bridge_tls_trusted_common_name_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Create a Trusted Common Name object.  # noqa: E501

        Create a Trusted Common Name object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x||x|| bridgeVirtualRouter|x||x|| msgVpnName|x||x|| tlsTrustedCommonName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridgeTlsTrustedCommonName body: The Trusted Common Name object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_bridge_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `create_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `create_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/tlsTrustedCommonNames', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeTlsTrustedCommonNameResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_msg_vpn_bridge(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Delete a Bridge object.  # noqa: E501

        Delete a Bridge object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_bridge_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Delete a Bridge object.  # noqa: E501

        Delete a Bridge object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `delete_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `delete_msg_vpn_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SempMetaOnlyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs):  # noqa: E501
        """Delete a Remote Message VPN object.  # noqa: E501

        Delete a Remote Message VPN object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_bridge_remote_msg_vpn_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs):  # noqa: E501
        """Delete a Remote Message VPN object.  # noqa: E501

        Delete a Remote Message VPN object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_msg_vpn_name', 'remote_msg_vpn_location', 'remote_msg_vpn_interface']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_bridge_remote_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_name' is set
        if ('remote_msg_vpn_name' not in params or
                params['remote_msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_name` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_location' is set
        if ('remote_msg_vpn_location' not in params or
                params['remote_msg_vpn_location'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_location` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_interface' is set
        if ('remote_msg_vpn_interface' not in params or
                params['remote_msg_vpn_interface'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_interface` when calling `delete_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_msg_vpn_name' in params:
            path_params['remoteMsgVpnName'] = params['remote_msg_vpn_name']  # noqa: E501
        if 'remote_msg_vpn_location' in params:
            path_params['remoteMsgVpnLocation'] = params['remote_msg_vpn_location']  # noqa: E501
        if 'remote_msg_vpn_interface' in params:
            path_params['remoteMsgVpnInterface'] = params['remote_msg_vpn_interface']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns/{remoteMsgVpnName},{remoteMsgVpnLocation},{remoteMsgVpnInterface}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SempMetaOnlyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_msg_vpn_bridge_remote_subscription(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs):  # noqa: E501
        """Delete a Remote Subscription object.  # noqa: E501

        Delete a Remote Subscription object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_remote_subscription(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_subscription_topic: The remoteSubscriptionTopic of the Remote Subscription. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_bridge_remote_subscription_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs):  # noqa: E501
        """Delete a Remote Subscription object.  # noqa: E501

        Delete a Remote Subscription object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_subscription_topic: The remoteSubscriptionTopic of the Remote Subscription. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_subscription_topic']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_bridge_remote_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `delete_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `delete_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'remote_subscription_topic' is set
        if ('remote_subscription_topic' not in params or
                params['remote_subscription_topic'] is None):
            raise ValueError("Missing the required parameter `remote_subscription_topic` when calling `delete_msg_vpn_bridge_remote_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_subscription_topic' in params:
            path_params['remoteSubscriptionTopic'] = params['remote_subscription_topic']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteSubscriptions/{remoteSubscriptionTopic}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SempMetaOnlyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_msg_vpn_bridge_tls_trusted_common_name(self, msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Delete a Trusted Common Name object.  # noqa: E501

        Delete a Trusted Common Name object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_tls_trusted_common_name(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_bridge_tls_trusted_common_name_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Delete a Trusted Common Name object.  # noqa: E501

        Delete a Trusted Common Name object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'tls_trusted_common_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_bridge_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `delete_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `delete_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'tls_trusted_common_name' is set
        if ('tls_trusted_common_name' not in params or
                params['tls_trusted_common_name'] is None):
            raise ValueError("Missing the required parameter `tls_trusted_common_name` when calling `delete_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'tls_trusted_common_name' in params:
            path_params['tlsTrustedCommonName'] = params['tls_trusted_common_name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/tlsTrustedCommonNames/{tlsTrustedCommonName}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SempMetaOnlyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a Bridge object.  # noqa: E501

        Get a Bridge object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteAuthenticationBasicPassword||x| remoteAuthenticationClientCertContent||x| remoteAuthenticationClientCertPassword||x|    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a Bridge object.  # noqa: E501

        Get a Bridge object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteAuthenticationBasicPassword||x| remoteAuthenticationClientCertContent||x| remoteAuthenticationClientCertPassword||x|    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs):  # noqa: E501
        """Get a Remote Message VPN object.  # noqa: E501

        Get a Remote Message VPN object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| password||x| remoteMsgVpnInterface|x|| remoteMsgVpnLocation|x|| remoteMsgVpnName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_remote_msg_vpn_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs):  # noqa: E501
        """Get a Remote Message VPN object.  # noqa: E501

        Get a Remote Message VPN object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| password||x| remoteMsgVpnInterface|x|| remoteMsgVpnLocation|x|| remoteMsgVpnName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_msg_vpn_name', 'remote_msg_vpn_location', 'remote_msg_vpn_interface', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_remote_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_name' is set
        if ('remote_msg_vpn_name' not in params or
                params['remote_msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_name` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_location' is set
        if ('remote_msg_vpn_location' not in params or
                params['remote_msg_vpn_location'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_location` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_interface' is set
        if ('remote_msg_vpn_interface' not in params or
                params['remote_msg_vpn_interface'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_interface` when calling `get_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_msg_vpn_name' in params:
            path_params['remoteMsgVpnName'] = params['remote_msg_vpn_name']  # noqa: E501
        if 'remote_msg_vpn_location' in params:
            path_params['remoteMsgVpnLocation'] = params['remote_msg_vpn_location']  # noqa: E501
        if 'remote_msg_vpn_interface' in params:
            path_params['remoteMsgVpnInterface'] = params['remote_msg_vpn_interface']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns/{remoteMsgVpnName},{remoteMsgVpnLocation},{remoteMsgVpnInterface}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteMsgVpnResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_remote_msg_vpns(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Remote Message VPN objects.  # noqa: E501

        Get a list of Remote Message VPN objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| password||x| remoteMsgVpnInterface|x|| remoteMsgVpnLocation|x|| remoteMsgVpnName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpns(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_remote_msg_vpns_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_remote_msg_vpns_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_remote_msg_vpns_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Remote Message VPN objects.  # noqa: E501

        Get a list of Remote Message VPN objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| password||x| remoteMsgVpnInterface|x|| remoteMsgVpnLocation|x|| remoteMsgVpnName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpns_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_remote_msg_vpns" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_remote_msg_vpns`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_remote_msg_vpns`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_remote_msg_vpns`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'where' in params:
            query_params.append(('where', params['where']))  # noqa: E501
            collection_formats['where'] = 'csv'  # noqa: E501
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteMsgVpnsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_remote_subscription(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs):  # noqa: E501
        """Get a Remote Subscription object.  # noqa: E501

        Get a Remote Subscription object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteSubscriptionTopic|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscription(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_subscription_topic: The remoteSubscriptionTopic of the Remote Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_remote_subscription_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, **kwargs):  # noqa: E501
        """Get a Remote Subscription object.  # noqa: E501

        Get a Remote Subscription object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteSubscriptionTopic|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_subscription_topic: The remoteSubscriptionTopic of the Remote Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_subscription_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_remote_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_remote_subscription`")  # noqa: E501
        # verify the required parameter 'remote_subscription_topic' is set
        if ('remote_subscription_topic' not in params or
                params['remote_subscription_topic'] is None):
            raise ValueError("Missing the required parameter `remote_subscription_topic` when calling `get_msg_vpn_bridge_remote_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_subscription_topic' in params:
            path_params['remoteSubscriptionTopic'] = params['remote_subscription_topic']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteSubscriptions/{remoteSubscriptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_remote_subscriptions(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Remote Subscription objects.  # noqa: E501

        Get a list of Remote Subscription objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteSubscriptionTopic|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscriptions(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_remote_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_remote_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_remote_subscriptions_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Remote Subscription objects.  # noqa: E501

        Get a list of Remote Subscription objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteSubscriptionTopic|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_remote_subscriptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_remote_subscriptions`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_remote_subscriptions`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_remote_subscriptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_bridge_remote_subscriptions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'cursor' in params:
            query_params.append(('cursor', params['cursor']))  # noqa: E501
        if 'where' in params:
            query_params.append(('where', params['where']))  # noqa: E501
            collection_formats['where'] = 'csv'  # noqa: E501
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteSubscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteSubscriptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_tls_trusted_common_name(self, msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Get a Trusted Common Name object.  # noqa: E501

        Get a Trusted Common Name object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_name(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_tls_trusted_common_name_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Get a Trusted Common Name object.  # noqa: E501

        Get a Trusted Common Name object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'tls_trusted_common_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'tls_trusted_common_name' is set
        if ('tls_trusted_common_name' not in params or
                params['tls_trusted_common_name'] is None):
            raise ValueError("Missing the required parameter `tls_trusted_common_name` when calling `get_msg_vpn_bridge_tls_trusted_common_name`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'tls_trusted_common_name' in params:
            path_params['tlsTrustedCommonName'] = params['tls_trusted_common_name']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/tlsTrustedCommonNames/{tlsTrustedCommonName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeTlsTrustedCommonNameResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_tls_trusted_common_names(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Trusted Common Name objects.  # noqa: E501

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_names(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNamesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_tls_trusted_common_names_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_tls_trusted_common_names_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_tls_trusted_common_names_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Trusted Common Name objects.  # noqa: E501

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_names_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeTlsTrustedCommonNamesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_tls_trusted_common_names" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_tls_trusted_common_names`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_tls_trusted_common_names`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_tls_trusted_common_names`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'where' in params:
            query_params.append(('where', params['where']))  # noqa: E501
            collection_formats['where'] = 'csv'  # noqa: E501
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/tlsTrustedCommonNames', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeTlsTrustedCommonNamesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridges(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Bridge objects.  # noqa: E501

        Get a list of Bridge objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteAuthenticationBasicPassword||x| remoteAuthenticationClientCertContent||x| remoteAuthenticationClientCertPassword||x|    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridges(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridges_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridges_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridges_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Bridge objects.  # noqa: E501

        Get a list of Bridge objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: bridgeName|x|| bridgeVirtualRouter|x|| msgVpnName|x|| remoteAuthenticationBasicPassword||x| remoteAuthenticationClientCertContent||x| remoteAuthenticationClientCertPassword||x|    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridges_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridges" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridges`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_bridges`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'cursor' in params:
            query_params.append(('cursor', params['cursor']))  # noqa: E501
        if 'where' in params:
            query_params.append(('where', params['where']))  # noqa: E501
            collection_formats['where'] = 'csv'  # noqa: E501
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def replace_msg_vpn_bridge(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Replace a Bridge object.  # noqa: E501

        Replace a Bridge object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| maxTtl||||x| msgVpnName|x|x||| remoteAuthenticationBasicClientUsername||||x| remoteAuthenticationBasicPassword|||x|x| remoteAuthenticationClientCertContent|||x|x| remoteAuthenticationClientCertPassword|||x|x| remoteAuthenticationScheme||||x| remoteDeliverToOnePriority||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_bridge(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def replace_msg_vpn_bridge_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Replace a Bridge object.  # noqa: E501

        Replace a Bridge object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| maxTtl||||x| msgVpnName|x|x||| remoteAuthenticationBasicClientUsername||||x| remoteAuthenticationBasicPassword|||x|x| remoteAuthenticationClientCertContent|||x|x| remoteAuthenticationClientCertPassword|||x|x| remoteAuthenticationScheme||||x| remoteDeliverToOnePriority||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_msg_vpn_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `replace_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `replace_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `replace_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_msg_vpn_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def replace_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs):  # noqa: E501
        """Replace a Remote Message VPN object.  # noqa: E501

        Replace a Remote Message VPN object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| clientUsername||||x| compressedDataEnabled||||x| egressFlowWindowSize||||x| msgVpnName|x|x||| password|||x|x| remoteMsgVpnInterface|x|x||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x||| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs)  # noqa: E501
            return data

    def replace_msg_vpn_bridge_remote_msg_vpn_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs):  # noqa: E501
        """Replace a Remote Message VPN object.  # noqa: E501

        Replace a Remote Message VPN object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| clientUsername||||x| compressedDataEnabled||||x| egressFlowWindowSize||||x| msgVpnName|x|x||| password|||x|x| remoteMsgVpnInterface|x|x||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x||| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_msg_vpn_name', 'remote_msg_vpn_location', 'remote_msg_vpn_interface', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_msg_vpn_bridge_remote_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_name' is set
        if ('remote_msg_vpn_name' not in params or
                params['remote_msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_name` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_location' is set
        if ('remote_msg_vpn_location' not in params or
                params['remote_msg_vpn_location'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_location` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_interface' is set
        if ('remote_msg_vpn_interface' not in params or
                params['remote_msg_vpn_interface'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_interface` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_msg_vpn_name' in params:
            path_params['remoteMsgVpnName'] = params['remote_msg_vpn_name']  # noqa: E501
        if 'remote_msg_vpn_location' in params:
            path_params['remoteMsgVpnLocation'] = params['remote_msg_vpn_location']  # noqa: E501
        if 'remote_msg_vpn_interface' in params:
            path_params['remoteMsgVpnInterface'] = params['remote_msg_vpn_interface']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns/{remoteMsgVpnName},{remoteMsgVpnLocation},{remoteMsgVpnInterface}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteMsgVpnResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_msg_vpn_bridge(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Update a Bridge object.  # noqa: E501

        Update a Bridge object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| maxTtl||||x| msgVpnName|x|x||| remoteAuthenticationBasicClientUsername||||x| remoteAuthenticationBasicPassword|||x|x| remoteAuthenticationClientCertContent|||x|x| remoteAuthenticationClientCertPassword|||x|x| remoteAuthenticationScheme||||x| remoteDeliverToOnePriority||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_bridge(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def update_msg_vpn_bridge_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Update a Bridge object.  # noqa: E501

        Update a Bridge object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| maxTtl||||x| msgVpnName|x|x||| remoteAuthenticationBasicClientUsername||||x| remoteAuthenticationBasicPassword|||x|x| remoteAuthenticationClientCertContent|||x|x| remoteAuthenticationClientCertPassword|||x|x| remoteAuthenticationScheme||||x| remoteDeliverToOnePriority||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridge|remoteAuthenticationBasicClientUsername|remoteAuthenticationBasicPassword| MsgVpnBridge|remoteAuthenticationBasicPassword|remoteAuthenticationBasicClientUsername| MsgVpnBridge|remoteAuthenticationClientCertPassword|remoteAuthenticationClientCertContent|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param MsgVpnBridge body: The Bridge object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_msg_vpn_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `update_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `update_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `update_msg_vpn_bridge`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_msg_vpn_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs):  # noqa: E501
        """Update a Remote Message VPN object.  # noqa: E501

        Update a Remote Message VPN object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| clientUsername||||x| compressedDataEnabled||||x| egressFlowWindowSize||||x| msgVpnName|x|x||| password|||x|x| remoteMsgVpnInterface|x|x||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x||| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs)  # noqa: E501
            return data

    def update_msg_vpn_bridge_remote_msg_vpn_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, **kwargs):  # noqa: E501
        """Update a Remote Message VPN object.  # noqa: E501

        Update a Remote Message VPN object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: bridgeName|x|x||| bridgeVirtualRouter|x|x||| clientUsername||||x| compressedDataEnabled||||x| egressFlowWindowSize||||x| msgVpnName|x|x||| password|||x|x| remoteMsgVpnInterface|x|x||| remoteMsgVpnLocation|x|x||| remoteMsgVpnName|x|x||| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnBridgeRemoteMsgVpn|clientUsername|password| MsgVpnBridgeRemoteMsgVpn|password|clientUsername|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str bridge_name: The bridgeName of the Bridge. (required)
        :param str bridge_virtual_router: The bridgeVirtualRouter of the Bridge. (required)
        :param str remote_msg_vpn_name: The remoteMsgVpnName of the Remote Message VPN. (required)
        :param str remote_msg_vpn_location: The remoteMsgVpnLocation of the Remote Message VPN. (required)
        :param str remote_msg_vpn_interface: The remoteMsgVpnInterface of the Remote Message VPN. (required)
        :param MsgVpnBridgeRemoteMsgVpn body: The Remote Message VPN object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeRemoteMsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'remote_msg_vpn_name', 'remote_msg_vpn_location', 'remote_msg_vpn_interface', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_msg_vpn_bridge_remote_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_name' is set
        if ('remote_msg_vpn_name' not in params or
                params['remote_msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_name` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_location' is set
        if ('remote_msg_vpn_location' not in params or
                params['remote_msg_vpn_location'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_location` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'remote_msg_vpn_interface' is set
        if ('remote_msg_vpn_interface' not in params or
                params['remote_msg_vpn_interface'] is None):
            raise ValueError("Missing the required parameter `remote_msg_vpn_interface` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_msg_vpn_bridge_remote_msg_vpn`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'remote_msg_vpn_name' in params:
            path_params['remoteMsgVpnName'] = params['remote_msg_vpn_name']  # noqa: E501
        if 'remote_msg_vpn_location' in params:
            path_params['remoteMsgVpnLocation'] = params['remote_msg_vpn_location']  # noqa: E501
        if 'remote_msg_vpn_interface' in params:
            path_params['remoteMsgVpnInterface'] = params['remote_msg_vpn_interface']  # noqa: E501

        query_params = []
        if 'select' in params:
            query_params.append(('select', params['select']))  # noqa: E501
            collection_formats['select'] = 'csv'  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/remoteMsgVpns/{remoteMsgVpnName},{remoteMsgVpnLocation},{remoteMsgVpnInterface}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeRemoteMsgVpnResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
