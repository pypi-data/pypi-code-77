# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See note 2 Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/action/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/action/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/action/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/action/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/action/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/action/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/action/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/action/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/action/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/action/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/action/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.12.00902000014
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from solace_semp_action.api_client import ApiClient


class MsgVpnApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def do_msg_vpn_bridge_clear_event(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Clear an event for the Bridge so it can be generated anew.  # noqa: E501

        Clear an event for the Bridge so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"global/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_clear_event(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_bridge_clear_event_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_bridge_clear_event_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_bridge_clear_event_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Clear an event for the Bridge so it can be generated anew.  # noqa: E501

        Clear an event for the Bridge so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"global/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_clear_event_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_bridge_clear_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_bridge_clear_event`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `do_msg_vpn_bridge_clear_event`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `do_msg_vpn_bridge_clear_event`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_bridge_clear_event`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/clearEvent', 'PUT',
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

    def do_msg_vpn_bridge_clear_stats(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Bridge.  # noqa: E501

        Clear the statistics for the Bridge.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_clear_stats(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_bridge_clear_stats_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_bridge_clear_stats_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_bridge_clear_stats_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Bridge.  # noqa: E501

        Clear the statistics for the Bridge.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_clear_stats_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_bridge_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_bridge_clear_stats`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `do_msg_vpn_bridge_clear_stats`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `do_msg_vpn_bridge_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_bridge_clear_stats`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/clearStats', 'PUT',
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

    def do_msg_vpn_bridge_disconnect(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Disconnect the Bridge.  # noqa: E501

        Disconnect the Bridge.    A SEMP client authorized with a minimum access scope/level of \"global/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_disconnect(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeDisconnect body: The Disconnect action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_bridge_disconnect_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_bridge_disconnect_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_bridge_disconnect_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, body, **kwargs):  # noqa: E501
        """Disconnect the Bridge.  # noqa: E501

        Disconnect the Bridge.    A SEMP client authorized with a minimum access scope/level of \"global/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_bridge_disconnect_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param MsgVpnBridgeDisconnect body: The Disconnect action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_bridge_disconnect" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_bridge_disconnect`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `do_msg_vpn_bridge_disconnect`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `do_msg_vpn_bridge_disconnect`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_bridge_disconnect`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/disconnect', 'PUT',
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

    def do_msg_vpn_clear_msg_spool_stats(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the message spool statistics for the Message VPN.  # noqa: E501

        Clear the message spool statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_msg_spool_stats(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearMsgSpoolStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_clear_msg_spool_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_clear_msg_spool_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_clear_msg_spool_stats_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the message spool statistics for the Message VPN.  # noqa: E501

        Clear the message spool statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_msg_spool_stats_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearMsgSpoolStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_clear_msg_spool_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_clear_msg_spool_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_clear_msg_spool_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clearMsgSpoolStats', 'PUT',
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

    def do_msg_vpn_clear_replication_stats(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the replication statistics for the Message VPN.  # noqa: E501

        Clear the replication statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_replication_stats(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearReplicationStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_clear_replication_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_clear_replication_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_clear_replication_stats_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the replication statistics for the Message VPN.  # noqa: E501

        Clear the replication statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_replication_stats_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearReplicationStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_clear_replication_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_clear_replication_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_clear_replication_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clearReplicationStats', 'PUT',
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

    def do_msg_vpn_clear_service_stats(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the service statistics for the Message VPN.  # noqa: E501

        Clear the service statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_service_stats(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearServiceStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_clear_service_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_clear_service_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_clear_service_stats_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the service statistics for the Message VPN.  # noqa: E501

        Clear the service statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_service_stats_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearServiceStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_clear_service_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_clear_service_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_clear_service_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clearServiceStats', 'PUT',
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

    def do_msg_vpn_clear_stats(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the messaging statistics for the Message VPN.  # noqa: E501

        Clear the messaging statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_stats(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_clear_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_clear_stats_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_clear_stats_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Clear the messaging statistics for the Message VPN.  # noqa: E501

        Clear the messaging statistics for the Message VPN.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_clear_stats_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param MsgVpnClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clearStats', 'PUT',
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

    def do_msg_vpn_client_clear_event(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Clear an event for the Client so it can be generated anew.  # noqa: E501

        Clear an event for the Client so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_clear_event(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_client_clear_event_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_client_clear_event_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_client_clear_event_with_http_info(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Clear an event for the Client so it can be generated anew.  # noqa: E501

        Clear an event for the Client so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_clear_event_with_http_info(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_client_clear_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_client_clear_event`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `do_msg_vpn_client_clear_event`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_client_clear_event`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/clearEvent', 'PUT',
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

    def do_msg_vpn_client_clear_stats(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Client.  # noqa: E501

        Clear the statistics for the Client.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_clear_stats(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_client_clear_stats_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_client_clear_stats_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_client_clear_stats_with_http_info(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Client.  # noqa: E501

        Clear the statistics for the Client.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_clear_stats_with_http_info(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_client_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_client_clear_stats`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `do_msg_vpn_client_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_client_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/clearStats', 'PUT',
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

    def do_msg_vpn_client_disconnect(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Disconnect the Client.  # noqa: E501

        Disconnect the Client.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_disconnect(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientDisconnect body: The Disconnect action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_client_disconnect_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_client_disconnect_with_http_info(msg_vpn_name, client_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_client_disconnect_with_http_info(self, msg_vpn_name, client_name, body, **kwargs):  # noqa: E501
        """Disconnect the Client.  # noqa: E501

        Disconnect the Client.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_disconnect_with_http_info(msg_vpn_name, client_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param MsgVpnClientDisconnect body: The Disconnect action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_client_disconnect" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_client_disconnect`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `do_msg_vpn_client_disconnect`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_client_disconnect`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/disconnect', 'PUT',
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

    def do_msg_vpn_client_transacted_session_delete(self, msg_vpn_name, client_name, session_name, body, **kwargs):  # noqa: E501
        """Delete the Transacted Session.  # noqa: E501

        Delete the Transacted Session.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_transacted_session_delete(msg_vpn_name, client_name, session_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str session_name: The name of the Transacted Session. (required)
        :param MsgVpnClientTransactedSessionDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_client_transacted_session_delete_with_http_info(msg_vpn_name, client_name, session_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_client_transacted_session_delete_with_http_info(msg_vpn_name, client_name, session_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_client_transacted_session_delete_with_http_info(self, msg_vpn_name, client_name, session_name, body, **kwargs):  # noqa: E501
        """Delete the Transacted Session.  # noqa: E501

        Delete the Transacted Session.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_client_transacted_session_delete_with_http_info(msg_vpn_name, client_name, session_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str session_name: The name of the Transacted Session. (required)
        :param MsgVpnClientTransactedSessionDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'session_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_client_transacted_session_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_client_transacted_session_delete`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `do_msg_vpn_client_transacted_session_delete`")  # noqa: E501
        # verify the required parameter 'session_name' is set
        if ('session_name' not in params or
                params['session_name'] is None):
            raise ValueError("Missing the required parameter `session_name` when calling `do_msg_vpn_client_transacted_session_delete`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_client_transacted_session_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'session_name' in params:
            path_params['sessionName'] = params['session_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/transactedSessions/{sessionName}/delete', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Backup cached messages of the Cache Instance to disk.  # noqa: E501

        Backup cached messages of the Cache Instance to disk.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceBackupCachedMsgs body: The Backup Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Backup cached messages of the Cache Instance to disk.  # noqa: E501

        Backup cached messages of the Cache Instance to disk.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceBackupCachedMsgs body: The Backup Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_backup_cached_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/backupCachedMsgs', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Cancel the backup of cached messages from the Cache Instance.  # noqa: E501

        Cancel the backup of cached messages from the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceCancelBackupCachedMsgs body: The Cancel Backup Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Cancel the backup of cached messages from the Cache Instance.  # noqa: E501

        Cancel the backup of cached messages from the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceCancelBackupCachedMsgs body: The Cancel Backup Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_backup_cached_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/cancelBackupCachedMsgs', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Cancel the restore of cached messages to the Cache Instance.  # noqa: E501

        Cancel the restore of cached messages to the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceCancelRestoreCachedMsgs body: The Cancel Restore Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Cancel the restore of cached messages to the Cache Instance.  # noqa: E501

        Cancel the restore of cached messages to the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceCancelRestoreCachedMsgs body: The Cancel Restore Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_cancel_restore_cached_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/cancelRestoreCachedMsgs', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_clear_event(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Clear an event for the Cache Instance so it can be generated anew.  # noqa: E501

        Clear an event for the Cache Instance so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_clear_event(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_clear_event_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_clear_event_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_clear_event_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Clear an event for the Cache Instance so it can be generated anew.  # noqa: E501

        Clear an event for the Cache Instance so it can be generated anew.   Attribute|Required|Deprecated :---|:---:|:---: eventName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_clear_event_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceClearEvent body: The Clear Event action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_clear_event" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_event`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_event`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_event`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_event`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_event`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/clearEvent', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_clear_stats(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Cache Instance.  # noqa: E501

        Clear the statistics for the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_clear_stats(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_clear_stats_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_clear_stats_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_clear_stats_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Cache Instance.  # noqa: E501

        Clear the statistics for the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_clear_stats_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_stats`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_stats`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_stats`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/clearStats', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_delete_msgs(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Delete messages covered by the given topic in the Cache Instance.  # noqa: E501

        Delete messages covered by the given topic in the Cache Instance.   Attribute|Required|Deprecated :---|:---:|:---: topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_delete_msgs(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceDeleteMsgs body: The Delete Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_delete_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_delete_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_delete_msgs_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Delete messages covered by the given topic in the Cache Instance.  # noqa: E501

        Delete messages covered by the given topic in the Cache Instance.   Attribute|Required|Deprecated :---|:---:|:---: topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_delete_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceDeleteMsgs body: The Delete Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_delete_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_delete_msgs`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_delete_msgs`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_delete_msgs`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_delete_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_delete_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/deleteMsgs', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Restore cached messages for the Cache Instance from disk.  # noqa: E501

        Restore cached messages for the Cache Instance from disk.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceRestoreCachedMsgs body: The Restore Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Restore cached messages for the Cache Instance from disk.  # noqa: E501

        Restore cached messages for the Cache Instance from disk.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceRestoreCachedMsgs body: The Restore Cached Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_restore_cached_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/restoreCachedMsgs', 'PUT',
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

    def do_msg_vpn_distributed_cache_cluster_instance_start(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Start the Cache Instance.  # noqa: E501

        Start the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_start(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceStart body: The Start Cache Instance action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_distributed_cache_cluster_instance_start_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_distributed_cache_cluster_instance_start_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_distributed_cache_cluster_instance_start_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, body, **kwargs):  # noqa: E501
        """Start the Cache Instance.  # noqa: E501

        Start the Cache Instance.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_distributed_cache_cluster_instance_start_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param MsgVpnDistributedCacheClusterInstanceStart body: The Start Cache Instance action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_distributed_cache_cluster_instance_start" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_start`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_start`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_start`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `do_msg_vpn_distributed_cache_cluster_instance_start`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_distributed_cache_cluster_instance_start`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/start', 'PUT',
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

    def do_msg_vpn_mqtt_session_clear_stats(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, **kwargs):  # noqa: E501
        """Clear the statistics for the MQTT Session.  # noqa: E501

        Clear the statistics for the MQTT Session.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_mqtt_session_clear_stats(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param MsgVpnMqttSessionClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_mqtt_session_clear_stats_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_mqtt_session_clear_stats_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_mqtt_session_clear_stats_with_http_info(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, **kwargs):  # noqa: E501
        """Clear the statistics for the MQTT Session.  # noqa: E501

        Clear the statistics for the MQTT Session.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_mqtt_session_clear_stats_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param MsgVpnMqttSessionClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'mqtt_session_client_id', 'mqtt_session_virtual_router', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_mqtt_session_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_mqtt_session_clear_stats`")  # noqa: E501
        # verify the required parameter 'mqtt_session_client_id' is set
        if ('mqtt_session_client_id' not in params or
                params['mqtt_session_client_id'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_client_id` when calling `do_msg_vpn_mqtt_session_clear_stats`")  # noqa: E501
        # verify the required parameter 'mqtt_session_virtual_router' is set
        if ('mqtt_session_virtual_router' not in params or
                params['mqtt_session_virtual_router'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_virtual_router` when calling `do_msg_vpn_mqtt_session_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_mqtt_session_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'mqtt_session_client_id' in params:
            path_params['mqttSessionClientId'] = params['mqtt_session_client_id']  # noqa: E501
        if 'mqtt_session_virtual_router' in params:
            path_params['mqttSessionVirtualRouter'] = params['mqtt_session_virtual_router']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/mqttSessions/{mqttSessionClientId},{mqttSessionVirtualRouter}/clearStats', 'PUT',
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

    def do_msg_vpn_queue_cancel_replay(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Cancel the replay of messages to the Queue.  # noqa: E501

        Cancel the replay of messages to the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_cancel_replay(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueCancelReplay body: The Cancel Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_queue_cancel_replay_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_queue_cancel_replay_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_queue_cancel_replay_with_http_info(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Cancel the replay of messages to the Queue.  # noqa: E501

        Cancel the replay of messages to the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_cancel_replay_with_http_info(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueCancelReplay body: The Cancel Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_queue_cancel_replay" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_queue_cancel_replay`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `do_msg_vpn_queue_cancel_replay`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_queue_cancel_replay`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/cancelReplay', 'PUT',
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

    def do_msg_vpn_queue_clear_stats(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Queue.  # noqa: E501

        Clear the statistics for the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_clear_stats(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_queue_clear_stats_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_queue_clear_stats_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_queue_clear_stats_with_http_info(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Queue.  # noqa: E501

        Clear the statistics for the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_clear_stats_with_http_info(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_queue_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_queue_clear_stats`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `do_msg_vpn_queue_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_queue_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/clearStats', 'PUT',
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

    def do_msg_vpn_queue_msg_delete(self, msg_vpn_name, queue_name, msg_id, body, **kwargs):  # noqa: E501
        """Delete the Message from the Queue.  # noqa: E501

        Delete the Message from the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_msg_delete(msg_vpn_name, queue_name, msg_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param MsgVpnQueueMsgDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_queue_msg_delete_with_http_info(msg_vpn_name, queue_name, msg_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_queue_msg_delete_with_http_info(msg_vpn_name, queue_name, msg_id, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_queue_msg_delete_with_http_info(self, msg_vpn_name, queue_name, msg_id, body, **kwargs):  # noqa: E501
        """Delete the Message from the Queue.  # noqa: E501

        Delete the Message from the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_msg_delete_with_http_info(msg_vpn_name, queue_name, msg_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param MsgVpnQueueMsgDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'msg_id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_queue_msg_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_queue_msg_delete`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `do_msg_vpn_queue_msg_delete`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `do_msg_vpn_queue_msg_delete`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_queue_msg_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501
        if 'msg_id' in params:
            path_params['msgId'] = params['msg_id']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/msgs/{msgId}/delete', 'PUT',
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

    def do_msg_vpn_queue_start_replay(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Start the replay of messages to the Queue.  # noqa: E501

        Start the replay of messages to the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_start_replay(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueStartReplay body: The Start Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_queue_start_replay_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_queue_start_replay_with_http_info(msg_vpn_name, queue_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_queue_start_replay_with_http_info(self, msg_vpn_name, queue_name, body, **kwargs):  # noqa: E501
        """Start the replay of messages to the Queue.  # noqa: E501

        Start the replay of messages to the Queue.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_queue_start_replay_with_http_info(msg_vpn_name, queue_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param MsgVpnQueueStartReplay body: The Start Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_queue_start_replay" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_queue_start_replay`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `do_msg_vpn_queue_start_replay`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_queue_start_replay`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/startReplay', 'PUT',
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

    def do_msg_vpn_replay_log_trim_logged_msgs(self, msg_vpn_name, replay_log_name, body, **kwargs):  # noqa: E501
        """Trim (delete) messages from the Replay Log.  # noqa: E501

        Trim (delete) messages from the Replay Log.   Attribute|Required|Deprecated :---|:---:|:---: olderThanTime|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_replay_log_trim_logged_msgs(msg_vpn_name, replay_log_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param MsgVpnReplayLogTrimLoggedMsgs body: The Trim Logged Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_replay_log_trim_logged_msgs_with_http_info(msg_vpn_name, replay_log_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_replay_log_trim_logged_msgs_with_http_info(msg_vpn_name, replay_log_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_replay_log_trim_logged_msgs_with_http_info(self, msg_vpn_name, replay_log_name, body, **kwargs):  # noqa: E501
        """Trim (delete) messages from the Replay Log.  # noqa: E501

        Trim (delete) messages from the Replay Log.   Attribute|Required|Deprecated :---|:---:|:---: olderThanTime|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_replay_log_trim_logged_msgs_with_http_info(msg_vpn_name, replay_log_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param MsgVpnReplayLogTrimLoggedMsgs body: The Trim Logged Messages action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'replay_log_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_replay_log_trim_logged_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_replay_log_trim_logged_msgs`")  # noqa: E501
        # verify the required parameter 'replay_log_name' is set
        if ('replay_log_name' not in params or
                params['replay_log_name'] is None):
            raise ValueError("Missing the required parameter `replay_log_name` when calling `do_msg_vpn_replay_log_trim_logged_msgs`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_replay_log_trim_logged_msgs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'replay_log_name' in params:
            path_params['replayLogName'] = params['replay_log_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/replayLogs/{replayLogName}/trimLoggedMsgs', 'PUT',
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

    def do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the REST Consumer.  # noqa: E501

        Clear the statistics for the REST Consumer.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumerClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the REST Consumer.  # noqa: E501

        Clear the statistics for the REST Consumer.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumerClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_rest_delivery_point_rest_consumer_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'rest_consumer_name' in params:
            path_params['restConsumerName'] = params['rest_consumer_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}/clearStats', 'PUT',
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

    def do_msg_vpn_topic_endpoint_cancel_replay(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Cancel the replay of messages to the Topic Endpoint.  # noqa: E501

        Cancel the replay of messages to the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_cancel_replay(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointCancelReplay body: The Cancel Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_topic_endpoint_cancel_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_topic_endpoint_cancel_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_topic_endpoint_cancel_replay_with_http_info(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Cancel the replay of messages to the Topic Endpoint.  # noqa: E501

        Cancel the replay of messages to the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_cancel_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointCancelReplay body: The Cancel Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_topic_endpoint_cancel_replay" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_topic_endpoint_cancel_replay`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `do_msg_vpn_topic_endpoint_cancel_replay`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_topic_endpoint_cancel_replay`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/cancelReplay', 'PUT',
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

    def do_msg_vpn_topic_endpoint_clear_stats(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Topic Endpoint.  # noqa: E501

        Clear the statistics for the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_clear_stats(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_topic_endpoint_clear_stats_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_topic_endpoint_clear_stats_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_topic_endpoint_clear_stats_with_http_info(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Clear the statistics for the Topic Endpoint.  # noqa: E501

        Clear the statistics for the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_clear_stats_with_http_info(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointClearStats body: The Clear Stats action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_topic_endpoint_clear_stats" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_topic_endpoint_clear_stats`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `do_msg_vpn_topic_endpoint_clear_stats`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_topic_endpoint_clear_stats`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/clearStats', 'PUT',
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

    def do_msg_vpn_topic_endpoint_msg_delete(self, msg_vpn_name, topic_endpoint_name, msg_id, body, **kwargs):  # noqa: E501
        """Delete the Message from the Topic Endpoint.  # noqa: E501

        Delete the Message from the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_msg_delete(msg_vpn_name, topic_endpoint_name, msg_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param MsgVpnTopicEndpointMsgDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_topic_endpoint_msg_delete_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_topic_endpoint_msg_delete_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_topic_endpoint_msg_delete_with_http_info(self, msg_vpn_name, topic_endpoint_name, msg_id, body, **kwargs):  # noqa: E501
        """Delete the Message from the Topic Endpoint.  # noqa: E501

        Delete the Message from the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_msg_delete_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param MsgVpnTopicEndpointMsgDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'msg_id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_topic_endpoint_msg_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_topic_endpoint_msg_delete`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `do_msg_vpn_topic_endpoint_msg_delete`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `do_msg_vpn_topic_endpoint_msg_delete`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_topic_endpoint_msg_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501
        if 'msg_id' in params:
            path_params['msgId'] = params['msg_id']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/msgs/{msgId}/delete', 'PUT',
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

    def do_msg_vpn_topic_endpoint_start_replay(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Start the replay of messages to the Topic Endpoint.  # noqa: E501

        Start the replay of messages to the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_start_replay(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointStartReplay body: The Start Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_topic_endpoint_start_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_topic_endpoint_start_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_topic_endpoint_start_replay_with_http_info(self, msg_vpn_name, topic_endpoint_name, body, **kwargs):  # noqa: E501
        """Start the replay of messages to the Topic Endpoint.  # noqa: E501

        Start the replay of messages to the Topic Endpoint.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_topic_endpoint_start_replay_with_http_info(msg_vpn_name, topic_endpoint_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param MsgVpnTopicEndpointStartReplay body: The Start Replay action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_topic_endpoint_start_replay" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_topic_endpoint_start_replay`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `do_msg_vpn_topic_endpoint_start_replay`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_topic_endpoint_start_replay`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/startReplay', 'PUT',
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

    def do_msg_vpn_transaction_commit(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Commit the Transaction.  # noqa: E501

        Commit the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_commit(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionCommit body: The Commit action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_transaction_commit_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_transaction_commit_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_transaction_commit_with_http_info(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Commit the Transaction.  # noqa: E501

        Commit the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_commit_with_http_info(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionCommit body: The Commit action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_transaction_commit" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_transaction_commit`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `do_msg_vpn_transaction_commit`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_transaction_commit`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/transactions/{xid}/commit', 'PUT',
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

    def do_msg_vpn_transaction_delete(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Delete the Transaction.  # noqa: E501

        Delete the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_delete(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_transaction_delete_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_transaction_delete_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_transaction_delete_with_http_info(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Delete the Transaction.  # noqa: E501

        Delete the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_delete_with_http_info(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionDelete body: The Delete action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_transaction_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_transaction_delete`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `do_msg_vpn_transaction_delete`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_transaction_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/transactions/{xid}/delete', 'PUT',
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

    def do_msg_vpn_transaction_rollback(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Rollback the Transaction.  # noqa: E501

        Rollback the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_rollback(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionRollback body: The Rollback action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.do_msg_vpn_transaction_rollback_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
        else:
            (data) = self.do_msg_vpn_transaction_rollback_with_http_info(msg_vpn_name, xid, body, **kwargs)  # noqa: E501
            return data

    def do_msg_vpn_transaction_rollback_with_http_info(self, msg_vpn_name, xid, body, **kwargs):  # noqa: E501
        """Rollback the Transaction.  # noqa: E501

        Rollback the Transaction.    A SEMP client authorized with a minimum access scope/level of \"vpn/read-write\" is required to perform this operation. Available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.do_msg_vpn_transaction_rollback_with_http_info(msg_vpn_name, xid, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param MsgVpnTransactionRollback body: The Rollback action's attributes. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method do_msg_vpn_transaction_rollback" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `do_msg_vpn_transaction_rollback`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `do_msg_vpn_transaction_rollback`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `do_msg_vpn_transaction_rollback`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

        query_params = []

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
            '/msgVpns/{msgVpnName}/transactions/{xid}/rollback', 'PUT',
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

    def get_msg_vpn(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a Message VPN object.  # noqa: E501

        Get a Message VPN object.  Message VPNs (Virtual Private Networks) allow for the segregation of topic space and clients. They also group clients connecting to a network of message brokers, such that messages published within a particular group are only visible to that group's clients.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a Message VPN object.  # noqa: E501

        Get a Message VPN object.  Message VPNs (Virtual Private Networks) allow for the segregation of topic space and clients. They also group clients connecting to a network of message brokers, such that messages published within a particular group are only visible to that group's clients.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn`")  # noqa: E501

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
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a Bridge object.  # noqa: E501

        Get a Bridge object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a Bridge object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

    def get_msg_vpn_bridges(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Bridge objects.  # noqa: E501

        Get a list of Bridge objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridges(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
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

        Get a list of Bridge objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridges_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
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

    def get_msg_vpn_client(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a Client object.  # noqa: E501

        Get a Client object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a Client object.  # noqa: E501

        Get a Client object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_transacted_session(self, msg_vpn_name, client_name, session_name, **kwargs):  # noqa: E501
        """Get a Client Transacted Session object.  # noqa: E501

        Get a Client Transacted Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_transacted_session(msg_vpn_name, client_name, session_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str session_name: The name of the Transacted Session. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTransactedSessionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_transacted_session_with_http_info(msg_vpn_name, client_name, session_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_transacted_session_with_http_info(msg_vpn_name, client_name, session_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_transacted_session_with_http_info(self, msg_vpn_name, client_name, session_name, **kwargs):  # noqa: E501
        """Get a Client Transacted Session object.  # noqa: E501

        Get a Client Transacted Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_transacted_session_with_http_info(msg_vpn_name, client_name, session_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str session_name: The name of the Transacted Session. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTransactedSessionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'session_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_transacted_session" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_transacted_session`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_transacted_session`")  # noqa: E501
        # verify the required parameter 'session_name' is set
        if ('session_name' not in params or
                params['session_name'] is None):
            raise ValueError("Missing the required parameter `session_name` when calling `get_msg_vpn_client_transacted_session`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'session_name' in params:
            path_params['sessionName'] = params['session_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/transactedSessions/{sessionName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientTransactedSessionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_transacted_sessions(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Transacted Session objects.  # noqa: E501

        Get a list of Client Transacted Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_transacted_sessions(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTransactedSessionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_transacted_sessions_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_transacted_sessions_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_transacted_sessions_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Transacted Session objects.  # noqa: E501

        Get a list of Client Transacted Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_transacted_sessions_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTransactedSessionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_transacted_sessions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_transacted_sessions`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_transacted_sessions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_transacted_sessions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/transactedSessions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientTransactedSessionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_clients(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client objects.  # noqa: E501

        Get a list of Client objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_clients(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_clients_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_clients_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_clients_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client objects.  # noqa: E501

        Get a list of Client objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_clients_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientsResponse
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
                    " to method get_msg_vpn_clients" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_clients`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_clients`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clients', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get a Distributed Cache object.  # noqa: E501

        Get a Distributed Cache object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_with_http_info(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get a Distributed Cache object.  # noqa: E501

        Get a Distributed Cache object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_with_http_info(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a Cache Cluster object.  # noqa: E501

        Get a Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_with_http_info(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a Cache Cluster object.  # noqa: E501

        Get a Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_instance(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a Cache Instance object.  # noqa: E501

        Get a Cache Instance object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instance_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instance_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instance_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a Cache Instance object.  # noqa: E501

        Get a Cache Instance object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instance" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instance`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instance`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `get_msg_vpn_distributed_cache_cluster_instance`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'instance_name' in params:
            path_params['instanceName'] = params['instance_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstanceResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_instances(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Cache Instance objects.  # noqa: E501

        Get a list of Cache Instance objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instances(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstancesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instances_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instances_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instances_with_http_info(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Cache Instance objects.  # noqa: E501

        Get a list of Cache Instance objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instances_with_http_info(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstancesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instances" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instances`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instances`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instances`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_instances`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstancesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_clusters(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get a list of Cache Cluster objects.  # noqa: E501

        Get a list of Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_clusters(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClustersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_clusters_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_clusters_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_clusters_with_http_info(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get a list of Cache Cluster objects.  # noqa: E501

        Get a list of Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_clusters_with_http_info(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClustersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_clusters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_clusters`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_clusters`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_clusters`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClustersResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_caches(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Distributed Cache objects.  # noqa: E501

        Get a list of Distributed Cache objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_caches(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCachesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_caches_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_caches_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_caches_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Distributed Cache objects.  # noqa: E501

        Get a list of Distributed Cache objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_caches_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCachesResponse
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
                    " to method get_msg_vpn_distributed_caches" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_caches`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_caches`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/distributedCaches', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCachesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_mqtt_session(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs):  # noqa: E501
        """Get an MQTT Session object.  # noqa: E501

        Get an MQTT Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_session_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_session_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_session_with_http_info(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs):  # noqa: E501
        """Get an MQTT Session object.  # noqa: E501

        Get an MQTT Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'mqtt_session_client_id', 'mqtt_session_virtual_router', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_mqtt_session" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_session`")  # noqa: E501
        # verify the required parameter 'mqtt_session_client_id' is set
        if ('mqtt_session_client_id' not in params or
                params['mqtt_session_client_id'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_client_id` when calling `get_msg_vpn_mqtt_session`")  # noqa: E501
        # verify the required parameter 'mqtt_session_virtual_router' is set
        if ('mqtt_session_virtual_router' not in params or
                params['mqtt_session_virtual_router'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_virtual_router` when calling `get_msg_vpn_mqtt_session`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'mqtt_session_client_id' in params:
            path_params['mqttSessionClientId'] = params['mqtt_session_client_id']  # noqa: E501
        if 'mqtt_session_virtual_router' in params:
            path_params['mqttSessionVirtualRouter'] = params['mqtt_session_virtual_router']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/mqttSessions/{mqttSessionClientId},{mqttSessionVirtualRouter}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttSessionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_mqtt_sessions(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of MQTT Session objects.  # noqa: E501

        Get a list of MQTT Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_sessions(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_sessions_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_sessions_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_sessions_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of MQTT Session objects.  # noqa: E501

        Get a list of MQTT Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_sessions_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionsResponse
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
                    " to method get_msg_vpn_mqtt_sessions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_sessions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_mqtt_sessions`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/mqttSessions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttSessionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a Queue object.  # noqa: E501

        Get a Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a Queue object.  # noqa: E501

        Get a Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_msg(self, msg_vpn_name, queue_name, msg_id, **kwargs):  # noqa: E501
        """Get a Queue Message object.  # noqa: E501

        Get a Queue Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_msg(msg_vpn_name, queue_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_msg_with_http_info(msg_vpn_name, queue_name, msg_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_msg_with_http_info(msg_vpn_name, queue_name, msg_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_msg_with_http_info(self, msg_vpn_name, queue_name, msg_id, **kwargs):  # noqa: E501
        """Get a Queue Message object.  # noqa: E501

        Get a Queue Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_msg_with_http_info(msg_vpn_name, queue_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'msg_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue_msg" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_msg`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_msg`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `get_msg_vpn_queue_msg`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501
        if 'msg_id' in params:
            path_params['msgId'] = params['msg_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/msgs/{msgId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueMsgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_msgs(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Message objects.  # noqa: E501

        Get a list of Queue Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_msgs(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_msgs_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_msgs_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_msgs_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Message objects.  # noqa: E501

        Get a list of Queue Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_msgs_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_msgs`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_msgs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_queue_msgs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/msgs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueMsgsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queues(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Queue objects.  # noqa: E501

        Get a list of Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queues(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queues_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queues_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queues_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Queue objects.  # noqa: E501

        Get a list of Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queues_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuesResponse
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
                    " to method get_msg_vpn_queues" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queues`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_queues`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/queues', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueuesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_replay_log(self, msg_vpn_name, replay_log_name, **kwargs):  # noqa: E501
        """Get a Replay Log object.  # noqa: E501

        Get a Replay Log object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log(msg_vpn_name, replay_log_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replay_log_with_http_info(msg_vpn_name, replay_log_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replay_log_with_http_info(msg_vpn_name, replay_log_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replay_log_with_http_info(self, msg_vpn_name, replay_log_name, **kwargs):  # noqa: E501
        """Get a Replay Log object.  # noqa: E501

        Get a Replay Log object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log_with_http_info(msg_vpn_name, replay_log_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'replay_log_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_replay_log" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replay_log`")  # noqa: E501
        # verify the required parameter 'replay_log_name' is set
        if ('replay_log_name' not in params or
                params['replay_log_name'] is None):
            raise ValueError("Missing the required parameter `replay_log_name` when calling `get_msg_vpn_replay_log`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'replay_log_name' in params:
            path_params['replayLogName'] = params['replay_log_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/replayLogs/{replayLogName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplayLogResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_replay_logs(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replay Log objects.  # noqa: E501

        Get a list of Replay Log objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_logs(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replay_logs_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replay_logs_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replay_logs_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replay Log objects.  # noqa: E501

        Get a list of Replay Log objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_logs_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogsResponse
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
                    " to method get_msg_vpn_replay_logs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replay_logs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_replay_logs`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/replayLogs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplayLogsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_point(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a REST Delivery Point object.  # noqa: E501

        Get a REST Delivery Point object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_with_http_info(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a REST Delivery Point object.  # noqa: E501

        Get a REST Delivery Point object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_point_rest_consumer(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Get a REST Consumer object.  # noqa: E501

        Get a REST Consumer object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Get a REST Consumer object.  # noqa: E501

        Get a REST Consumer object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point_rest_consumer" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'rest_consumer_name' in params:
            path_params['restConsumerName'] = params['rest_consumer_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointRestConsumerResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_point_rest_consumers(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a list of REST Consumer objects.  # noqa: E501

        Get a list of REST Consumer objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumers(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_rest_consumers_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_rest_consumers_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_rest_consumers_with_http_info(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a list of REST Consumer objects.  # noqa: E501

        Get a list of REST Consumer objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumers_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point_rest_consumers" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumers`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumers`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_rest_delivery_point_rest_consumers`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointRestConsumersResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_points(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of REST Delivery Point objects.  # noqa: E501

        Get a list of REST Delivery Point objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_points(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_points_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_points_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_points_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of REST Delivery Point objects.  # noqa: E501

        Get a list of REST Delivery Point objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_points_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointsResponse
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
                    " to method get_msg_vpn_rest_delivery_points" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_points`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_rest_delivery_points`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/restDeliveryPoints', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a Topic Endpoint object.  # noqa: E501

        Get a Topic Endpoint object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_with_http_info(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a Topic Endpoint object.  # noqa: E501

        Get a Topic Endpoint object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_with_http_info(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_topic_endpoint" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint_msg(self, msg_vpn_name, topic_endpoint_name, msg_id, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Message object.  # noqa: E501

        Get a Topic Endpoint Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_msg(msg_vpn_name, topic_endpoint_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_msg_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_msg_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_msg_with_http_info(self, msg_vpn_name, topic_endpoint_name, msg_id, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Message object.  # noqa: E501

        Get a Topic Endpoint Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_msg_with_http_info(msg_vpn_name, topic_endpoint_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'msg_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_topic_endpoint_msg" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_msg`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_msg`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `get_msg_vpn_topic_endpoint_msg`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501
        if 'msg_id' in params:
            path_params['msgId'] = params['msg_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/msgs/{msgId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointMsgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint_msgs(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Message objects.  # noqa: E501

        Get a list of Topic Endpoint Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_msgs(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_msgs_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_msgs_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_msgs_with_http_info(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Message objects.  # noqa: E501

        Get a list of Topic Endpoint Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_msgs_with_http_info(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_topic_endpoint_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_msgs`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_msgs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_topic_endpoint_msgs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/msgs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointMsgsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoints(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint objects.  # noqa: E501

        Get a list of Topic Endpoint objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoints(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoints_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoints_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoints_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint objects.  # noqa: E501

        Get a list of Topic Endpoint objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoints_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointsResponse
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
                    " to method get_msg_vpn_topic_endpoints" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoints`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_topic_endpoints`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/topicEndpoints', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_transaction(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a Replicated Local Transaction or XA Transaction object.  # noqa: E501

        Get a Replicated Local Transaction or XA Transaction object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transaction_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transaction_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transaction_with_http_info(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a Replicated Local Transaction or XA Transaction object.  # noqa: E501

        Get a Replicated Local Transaction or XA Transaction object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_with_http_info(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transaction`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `get_msg_vpn_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/transactions/{xid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_transactions(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replicated Local Transaction or XA Transaction objects.  # noqa: E501

        Get a list of Replicated Local Transaction or XA Transaction objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transactions(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transactions_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transactions_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transactions_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replicated Local Transaction or XA Transaction objects.  # noqa: E501

        Get a list of Replicated Local Transaction or XA Transaction objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transactions_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionsResponse
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
                    " to method get_msg_vpn_transactions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transactions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_transactions`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpns(self, **kwargs):  # noqa: E501
        """Get a list of Message VPN objects.  # noqa: E501

        Get a list of Message VPN objects.  Message VPNs (Virtual Private Networks) allow for the segregation of topic space and clients. They also group clients connecting to a network of message brokers, such that messages published within a particular group are only visible to that group's clients.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpns(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpns_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpns_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_msg_vpns_with_http_info(self, **kwargs):  # noqa: E501
        """Get a list of Message VPN objects.  # noqa: E501

        Get a list of Message VPN objects.  Message VPNs (Virtual Private Networks) allow for the segregation of topic space and clients. They also group clients connecting to a network of message brokers, such that messages published within a particular group are only visible to that group's clients.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpns_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpns" % key
                )
            params[key] = val
        del params['kwargs']

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpns`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

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
            '/msgVpns', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
