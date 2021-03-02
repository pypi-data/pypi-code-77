# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters \"q1\" and \"q2\" ; with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.      # noqa: E501

    OpenAPI spec version: 2.12.00902000028
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from solace_semp_monitor.api_client import ApiClient


class MsgVpnApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

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

    def get_msg_vpn_acl_profile(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get an ACL Profile object.  # noqa: E501

        Get an ACL Profile object.  An ACL Profile controls whether an authenticated client is permitted to establish a connection with the message broker or permitted to publish and subscribe to specific topics.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_with_http_info(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get an ACL Profile object.  # noqa: E501

        Get an ACL Profile object.  An ACL Profile controls whether an authenticated client is permitted to establish a connection with the message broker or permitted to publish and subscribe to specific topics.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_with_http_info(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_client_connect_exception(self, msg_vpn_name, acl_profile_name, client_connect_exception_address, **kwargs):  # noqa: E501
        """Get a Client Connect Exception object.  # noqa: E501

        Get a Client Connect Exception object.  A Client Connect Exception is an exception to the default action to take when a client using the ACL Profile connects to the Message VPN. Exceptions must be expressed as an IP address/netmask in CIDR form.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| clientConnectExceptionAddress|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_client_connect_exception(msg_vpn_name, acl_profile_name, client_connect_exception_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str client_connect_exception_address: The IP address/netmask of the client connect exception in CIDR form. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileClientConnectExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_client_connect_exception_with_http_info(msg_vpn_name, acl_profile_name, client_connect_exception_address, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_client_connect_exception_with_http_info(msg_vpn_name, acl_profile_name, client_connect_exception_address, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_client_connect_exception_with_http_info(self, msg_vpn_name, acl_profile_name, client_connect_exception_address, **kwargs):  # noqa: E501
        """Get a Client Connect Exception object.  # noqa: E501

        Get a Client Connect Exception object.  A Client Connect Exception is an exception to the default action to take when a client using the ACL Profile connects to the Message VPN. Exceptions must be expressed as an IP address/netmask in CIDR form.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| clientConnectExceptionAddress|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_client_connect_exception_with_http_info(msg_vpn_name, acl_profile_name, client_connect_exception_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str client_connect_exception_address: The IP address/netmask of the client connect exception in CIDR form. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileClientConnectExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'client_connect_exception_address', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_client_connect_exception" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_client_connect_exception`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_client_connect_exception`")  # noqa: E501
        # verify the required parameter 'client_connect_exception_address' is set
        if ('client_connect_exception_address' not in params or
                params['client_connect_exception_address'] is None):
            raise ValueError("Missing the required parameter `client_connect_exception_address` when calling `get_msg_vpn_acl_profile_client_connect_exception`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501
        if 'client_connect_exception_address' in params:
            path_params['clientConnectExceptionAddress'] = params['client_connect_exception_address']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/clientConnectExceptions/{clientConnectExceptionAddress}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfileClientConnectExceptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_client_connect_exceptions(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Client Connect Exception objects.  # noqa: E501

        Get a list of Client Connect Exception objects.  A Client Connect Exception is an exception to the default action to take when a client using the ACL Profile connects to the Message VPN. Exceptions must be expressed as an IP address/netmask in CIDR form.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| clientConnectExceptionAddress|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_client_connect_exceptions(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileClientConnectExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_client_connect_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_client_connect_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_client_connect_exceptions_with_http_info(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Client Connect Exception objects.  # noqa: E501

        Get a list of Client Connect Exception objects.  A Client Connect Exception is an exception to the default action to take when a client using the ACL Profile connects to the Message VPN. Exceptions must be expressed as an IP address/netmask in CIDR form.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| clientConnectExceptionAddress|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_client_connect_exceptions_with_http_info(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileClientConnectExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_client_connect_exceptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_client_connect_exceptions`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_client_connect_exceptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_acl_profile_client_connect_exceptions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/clientConnectExceptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfileClientConnectExceptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_publish_exception(self, msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, **kwargs):  # noqa: E501
        """Get a Publish Topic Exception object.  # noqa: E501

        Get a Publish Topic Exception object.  A Publish Topic Exception is an exception to the default action to take when a client using the ACL Profile publishes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| publishExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_publish_exception(msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str topic_syntax: The syntax of the topic for the exception to the default action taken. (required)
        :param str publish_exception_topic: The topic for the exception to the default action taken. May include wildcard characters. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilePublishExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_publish_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_publish_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_publish_exception_with_http_info(self, msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, **kwargs):  # noqa: E501
        """Get a Publish Topic Exception object.  # noqa: E501

        Get a Publish Topic Exception object.  A Publish Topic Exception is an exception to the default action to take when a client using the ACL Profile publishes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| publishExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_publish_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, publish_exception_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str topic_syntax: The syntax of the topic for the exception to the default action taken. (required)
        :param str publish_exception_topic: The topic for the exception to the default action taken. May include wildcard characters. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilePublishExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'topic_syntax', 'publish_exception_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_publish_exception" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_publish_exception`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_publish_exception`")  # noqa: E501
        # verify the required parameter 'topic_syntax' is set
        if ('topic_syntax' not in params or
                params['topic_syntax'] is None):
            raise ValueError("Missing the required parameter `topic_syntax` when calling `get_msg_vpn_acl_profile_publish_exception`")  # noqa: E501
        # verify the required parameter 'publish_exception_topic' is set
        if ('publish_exception_topic' not in params or
                params['publish_exception_topic'] is None):
            raise ValueError("Missing the required parameter `publish_exception_topic` when calling `get_msg_vpn_acl_profile_publish_exception`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501
        if 'topic_syntax' in params:
            path_params['topicSyntax'] = params['topic_syntax']  # noqa: E501
        if 'publish_exception_topic' in params:
            path_params['publishExceptionTopic'] = params['publish_exception_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/publishExceptions/{topicSyntax},{publishExceptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfilePublishExceptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_publish_exceptions(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Publish Topic Exception objects.  # noqa: E501

        Get a list of Publish Topic Exception objects.  A Publish Topic Exception is an exception to the default action to take when a client using the ACL Profile publishes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| publishExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_publish_exceptions(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilePublishExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_publish_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_publish_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_publish_exceptions_with_http_info(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Publish Topic Exception objects.  # noqa: E501

        Get a list of Publish Topic Exception objects.  A Publish Topic Exception is an exception to the default action to take when a client using the ACL Profile publishes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| publishExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_publish_exceptions_with_http_info(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilePublishExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_publish_exceptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_publish_exceptions`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_publish_exceptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_acl_profile_publish_exceptions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/publishExceptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfilePublishExceptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_subscribe_exception(self, msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, **kwargs):  # noqa: E501
        """Get a Subscribe Topic Exception object.  # noqa: E501

        Get a Subscribe Topic Exception object.  A Subscribe Topic Exception is an exception to the default action to take when a client using the ACL Profile subscribes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| subscribeExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_subscribe_exception(msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str topic_syntax: The syntax of the topic for the exception to the default action taken. (required)
        :param str subscribe_exception_topic: The topic for the exception to the default action taken. May include wildcard characters. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileSubscribeExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_subscribe_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_subscribe_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_subscribe_exception_with_http_info(self, msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, **kwargs):  # noqa: E501
        """Get a Subscribe Topic Exception object.  # noqa: E501

        Get a Subscribe Topic Exception object.  A Subscribe Topic Exception is an exception to the default action to take when a client using the ACL Profile subscribes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| subscribeExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_subscribe_exception_with_http_info(msg_vpn_name, acl_profile_name, topic_syntax, subscribe_exception_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param str topic_syntax: The syntax of the topic for the exception to the default action taken. (required)
        :param str subscribe_exception_topic: The topic for the exception to the default action taken. May include wildcard characters. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileSubscribeExceptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'topic_syntax', 'subscribe_exception_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_subscribe_exception" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_subscribe_exception`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_subscribe_exception`")  # noqa: E501
        # verify the required parameter 'topic_syntax' is set
        if ('topic_syntax' not in params or
                params['topic_syntax'] is None):
            raise ValueError("Missing the required parameter `topic_syntax` when calling `get_msg_vpn_acl_profile_subscribe_exception`")  # noqa: E501
        # verify the required parameter 'subscribe_exception_topic' is set
        if ('subscribe_exception_topic' not in params or
                params['subscribe_exception_topic'] is None):
            raise ValueError("Missing the required parameter `subscribe_exception_topic` when calling `get_msg_vpn_acl_profile_subscribe_exception`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501
        if 'topic_syntax' in params:
            path_params['topicSyntax'] = params['topic_syntax']  # noqa: E501
        if 'subscribe_exception_topic' in params:
            path_params['subscribeExceptionTopic'] = params['subscribe_exception_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/subscribeExceptions/{topicSyntax},{subscribeExceptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfileSubscribeExceptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profile_subscribe_exceptions(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Subscribe Topic Exception objects.  # noqa: E501

        Get a list of Subscribe Topic Exception objects.  A Subscribe Topic Exception is an exception to the default action to take when a client using the ACL Profile subscribes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| subscribeExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_subscribe_exceptions(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileSubscribeExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profile_subscribe_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profile_subscribe_exceptions_with_http_info(msg_vpn_name, acl_profile_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profile_subscribe_exceptions_with_http_info(self, msg_vpn_name, acl_profile_name, **kwargs):  # noqa: E501
        """Get a list of Subscribe Topic Exception objects.  # noqa: E501

        Get a list of Subscribe Topic Exception objects.  A Subscribe Topic Exception is an exception to the default action to take when a client using the ACL Profile subscribes to a topic in the Message VPN. Exceptions must be expressed as a topic.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x| subscribeExceptionTopic|x| topicSyntax|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profile_subscribe_exceptions_with_http_info(msg_vpn_name, acl_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str acl_profile_name: The name of the ACL Profile. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfileSubscribeExceptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'acl_profile_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_acl_profile_subscribe_exceptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profile_subscribe_exceptions`")  # noqa: E501
        # verify the required parameter 'acl_profile_name' is set
        if ('acl_profile_name' not in params or
                params['acl_profile_name'] is None):
            raise ValueError("Missing the required parameter `acl_profile_name` when calling `get_msg_vpn_acl_profile_subscribe_exceptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_acl_profile_subscribe_exceptions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'acl_profile_name' in params:
            path_params['aclProfileName'] = params['acl_profile_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/aclProfiles/{aclProfileName}/subscribeExceptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfileSubscribeExceptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_acl_profiles(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of ACL Profile objects.  # noqa: E501

        Get a list of ACL Profile objects.  An ACL Profile controls whether an authenticated client is permitted to establish a connection with the message broker or permitted to publish and subscribe to specific topics.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profiles(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_acl_profiles_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_acl_profiles_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_acl_profiles_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of ACL Profile objects.  # noqa: E501

        Get a list of ACL Profile objects.  An ACL Profile controls whether an authenticated client is permitted to establish a connection with the message broker or permitted to publish and subscribe to specific topics.   Attribute|Identifying|Deprecated :---|:---:|:---: aclProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_acl_profiles_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAclProfilesResponse
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
                    " to method get_msg_vpn_acl_profiles" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_acl_profiles`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_acl_profiles`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/aclProfiles', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAclProfilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_authorization_group(self, msg_vpn_name, authorization_group_name, **kwargs):  # noqa: E501
        """Get an LDAP Authorization Group object.  # noqa: E501

        Get an LDAP Authorization Group object.   Attribute|Identifying|Deprecated :---|:---:|:---: authorizationGroupName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_authorization_group(msg_vpn_name, authorization_group_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str authorization_group_name: The name of the LDAP Authorization Group. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAuthorizationGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_authorization_group_with_http_info(msg_vpn_name, authorization_group_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_authorization_group_with_http_info(msg_vpn_name, authorization_group_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_authorization_group_with_http_info(self, msg_vpn_name, authorization_group_name, **kwargs):  # noqa: E501
        """Get an LDAP Authorization Group object.  # noqa: E501

        Get an LDAP Authorization Group object.   Attribute|Identifying|Deprecated :---|:---:|:---: authorizationGroupName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_authorization_group_with_http_info(msg_vpn_name, authorization_group_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str authorization_group_name: The name of the LDAP Authorization Group. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAuthorizationGroupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'authorization_group_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_authorization_group" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_authorization_group`")  # noqa: E501
        # verify the required parameter 'authorization_group_name' is set
        if ('authorization_group_name' not in params or
                params['authorization_group_name'] is None):
            raise ValueError("Missing the required parameter `authorization_group_name` when calling `get_msg_vpn_authorization_group`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'authorization_group_name' in params:
            path_params['authorizationGroupName'] = params['authorization_group_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/authorizationGroups/{authorizationGroupName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAuthorizationGroupResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_authorization_groups(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of LDAP Authorization Group objects.  # noqa: E501

        Get a list of LDAP Authorization Group objects.   Attribute|Identifying|Deprecated :---|:---:|:---: authorizationGroupName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_authorization_groups(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAuthorizationGroupsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_authorization_groups_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_authorization_groups_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_authorization_groups_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of LDAP Authorization Group objects.  # noqa: E501

        Get a list of LDAP Authorization Group objects.   Attribute|Identifying|Deprecated :---|:---:|:---: authorizationGroupName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_authorization_groups_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnAuthorizationGroupsResponse
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
                    " to method get_msg_vpn_authorization_groups" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_authorization_groups`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_authorization_groups`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/authorizationGroups', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnAuthorizationGroupsResponse',  # noqa: E501
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

    def get_msg_vpn_bridge_local_subscription(self, msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, **kwargs):  # noqa: E501
        """Get a Bridge Local Subscriptions object.  # noqa: E501

        Get a Bridge Local Subscriptions object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| localSubscriptionTopic|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_local_subscription(msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str local_subscription_topic: The topic of the Bridge local subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeLocalSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_local_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_local_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_local_subscription_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, **kwargs):  # noqa: E501
        """Get a Bridge Local Subscriptions object.  # noqa: E501

        Get a Bridge Local Subscriptions object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| localSubscriptionTopic|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_local_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, local_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str local_subscription_topic: The topic of the Bridge local subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeLocalSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'bridge_name', 'bridge_virtual_router', 'local_subscription_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_bridge_local_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_local_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_local_subscription`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_local_subscription`")  # noqa: E501
        # verify the required parameter 'local_subscription_topic' is set
        if ('local_subscription_topic' not in params or
                params['local_subscription_topic'] is None):
            raise ValueError("Missing the required parameter `local_subscription_topic` when calling `get_msg_vpn_bridge_local_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'bridge_name' in params:
            path_params['bridgeName'] = params['bridge_name']  # noqa: E501
        if 'bridge_virtual_router' in params:
            path_params['bridgeVirtualRouter'] = params['bridge_virtual_router']  # noqa: E501
        if 'local_subscription_topic' in params:
            path_params['localSubscriptionTopic'] = params['local_subscription_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/localSubscriptions/{localSubscriptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeLocalSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_local_subscriptions(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Bridge Local Subscriptions objects.  # noqa: E501

        Get a list of Bridge Local Subscriptions objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| localSubscriptionTopic|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_local_subscriptions(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeLocalSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_bridge_local_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_bridge_local_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_bridge_local_subscriptions_with_http_info(self, msg_vpn_name, bridge_name, bridge_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Bridge Local Subscriptions objects.  # noqa: E501

        Get a list of Bridge Local Subscriptions objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| localSubscriptionTopic|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_local_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnBridgeLocalSubscriptionsResponse
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
                    " to method get_msg_vpn_bridge_local_subscriptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_bridge_local_subscriptions`")  # noqa: E501
        # verify the required parameter 'bridge_name' is set
        if ('bridge_name' not in params or
                params['bridge_name'] is None):
            raise ValueError("Missing the required parameter `bridge_name` when calling `get_msg_vpn_bridge_local_subscriptions`")  # noqa: E501
        # verify the required parameter 'bridge_virtual_router' is set
        if ('bridge_virtual_router' not in params or
                params['bridge_virtual_router'] is None):
            raise ValueError("Missing the required parameter `bridge_virtual_router` when calling `get_msg_vpn_bridge_local_subscriptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_bridge_local_subscriptions`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/bridges/{bridgeName},{bridgeVirtualRouter}/localSubscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnBridgeLocalSubscriptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_bridge_remote_msg_vpn(self, msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, **kwargs):  # noqa: E501
        """Get a Remote Message VPN object.  # noqa: E501

        Get a Remote Message VPN object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteMsgVpnInterface|x| remoteMsgVpnLocation|x| remoteMsgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpn(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str remote_msg_vpn_name: The name of the remote Message VPN. (required)
        :param str remote_msg_vpn_location: The location of the remote Message VPN as either an FQDN with port, IP address with port, or virtual router name (starting with \"v:\"). (required)
        :param str remote_msg_vpn_interface: The physical interface on the local Message VPN host for connecting to the remote Message VPN. By default, an interface is chosen automatically (recommended), but if specified, `remoteMsgVpnLocation` must not be a virtual router name. (required)
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

        Get a Remote Message VPN object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteMsgVpnInterface|x| remoteMsgVpnLocation|x| remoteMsgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpn_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_msg_vpn_name, remote_msg_vpn_location, remote_msg_vpn_interface, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str remote_msg_vpn_name: The name of the remote Message VPN. (required)
        :param str remote_msg_vpn_location: The location of the remote Message VPN as either an FQDN with port, IP address with port, or virtual router name (starting with \"v:\"). (required)
        :param str remote_msg_vpn_interface: The physical interface on the local Message VPN host for connecting to the remote Message VPN. By default, an interface is chosen automatically (recommended), but if specified, `remoteMsgVpnLocation` must not be a virtual router name. (required)
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

        Get a list of Remote Message VPN objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteMsgVpnInterface|x| remoteMsgVpnLocation|x| remoteMsgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpns(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a list of Remote Message VPN objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteMsgVpnInterface|x| remoteMsgVpnLocation|x| remoteMsgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_msg_vpns_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a Remote Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteSubscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscription(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str remote_subscription_topic: The topic of the Bridge remote subscription. (required)
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

        Get a Remote Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteSubscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscription_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, remote_subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str remote_subscription_topic: The topic of the Bridge remote subscription. (required)
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

        Get a list of Remote Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteSubscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscriptions(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a list of Remote Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| remoteSubscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_remote_subscriptions_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a Trusted Common Name object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_name(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str tls_trusted_common_name: The expected trusted common name of the remote certificate. (required)
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

        Get a Trusted Common Name object.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_name_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
        :param str tls_trusted_common_name: The expected trusted common name of the remote certificate. (required)
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

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_names(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Deprecated :---|:---:|:---: bridgeName|x| bridgeVirtualRouter|x| msgVpnName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_bridge_tls_trusted_common_names_with_http_info(msg_vpn_name, bridge_name, bridge_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str bridge_name: The name of the Bridge. (required)
        :param str bridge_virtual_router: The virtual router of the Bridge. (required)
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

        Get a Client object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Client object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_client_connection(self, msg_vpn_name, client_name, client_address, **kwargs):  # noqa: E501
        """Get a Client Connection object.  # noqa: E501

        Get a Client Connection object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientAddress|x| clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_connection(msg_vpn_name, client_name, client_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str client_address: The IP address and TCP port on the Client side of the Client Connection. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientConnectionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_connection_with_http_info(msg_vpn_name, client_name, client_address, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_connection_with_http_info(msg_vpn_name, client_name, client_address, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_connection_with_http_info(self, msg_vpn_name, client_name, client_address, **kwargs):  # noqa: E501
        """Get a Client Connection object.  # noqa: E501

        Get a Client Connection object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientAddress|x| clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_connection_with_http_info(msg_vpn_name, client_name, client_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str client_address: The IP address and TCP port on the Client side of the Client Connection. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientConnectionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'client_address', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_connection" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_connection`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_connection`")  # noqa: E501
        # verify the required parameter 'client_address' is set
        if ('client_address' not in params or
                params['client_address'] is None):
            raise ValueError("Missing the required parameter `client_address` when calling `get_msg_vpn_client_connection`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'client_address' in params:
            path_params['clientAddress'] = params['client_address']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/connections/{clientAddress}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientConnectionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_connections(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Connection objects.  # noqa: E501

        Get a list of Client Connection objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientAddress|x| clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_connections(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientConnectionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_connections_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_connections_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_connections_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Connection objects.  # noqa: E501

        Get a list of Client Connection objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientAddress|x| clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_connections_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientConnectionsResponse
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
                    " to method get_msg_vpn_client_connections" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_connections`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_connections`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_connections`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clients/{clientName}/connections', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientConnectionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_profile(self, msg_vpn_name, client_profile_name, **kwargs):  # noqa: E501
        """Get a Client Profile object.  # noqa: E501

        Get a Client Profile object.  Client Profiles are used to assign common configuration properties to clients that have been successfully authorized.   Attribute|Identifying|Deprecated :---|:---:|:---: clientProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_profile(msg_vpn_name, client_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_profile_name: The name of the Client Profile. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_profile_with_http_info(msg_vpn_name, client_profile_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_profile_with_http_info(msg_vpn_name, client_profile_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_profile_with_http_info(self, msg_vpn_name, client_profile_name, **kwargs):  # noqa: E501
        """Get a Client Profile object.  # noqa: E501

        Get a Client Profile object.  Client Profiles are used to assign common configuration properties to clients that have been successfully authorized.   Attribute|Identifying|Deprecated :---|:---:|:---: clientProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_profile_with_http_info(msg_vpn_name, client_profile_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_profile_name: The name of the Client Profile. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_profile_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_profile" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_profile`")  # noqa: E501
        # verify the required parameter 'client_profile_name' is set
        if ('client_profile_name' not in params or
                params['client_profile_name'] is None):
            raise ValueError("Missing the required parameter `client_profile_name` when calling `get_msg_vpn_client_profile`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_profile_name' in params:
            path_params['clientProfileName'] = params['client_profile_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientProfileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_profiles(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client Profile objects.  # noqa: E501

        Get a list of Client Profile objects.  Client Profiles are used to assign common configuration properties to clients that have been successfully authorized.   Attribute|Identifying|Deprecated :---|:---:|:---: clientProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_profiles(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientProfilesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_profiles_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_profiles_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_profiles_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client Profile objects.  # noqa: E501

        Get a list of Client Profile objects.  Client Profiles are used to assign common configuration properties to clients that have been successfully authorized.   Attribute|Identifying|Deprecated :---|:---:|:---: clientProfileName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_profiles_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientProfilesResponse
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
                    " to method get_msg_vpn_client_profiles" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_profiles`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_profiles`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clientProfiles', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientProfilesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_rx_flow(self, msg_vpn_name, client_name, flow_id, **kwargs):  # noqa: E501
        """Get a Client Receive Flow object.  # noqa: E501

        Get a Client Receive Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_rx_flow(msg_vpn_name, client_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str flow_id: The identifier (ID) of the flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientRxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_rx_flow_with_http_info(msg_vpn_name, client_name, flow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_rx_flow_with_http_info(msg_vpn_name, client_name, flow_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_rx_flow_with_http_info(self, msg_vpn_name, client_name, flow_id, **kwargs):  # noqa: E501
        """Get a Client Receive Flow object.  # noqa: E501

        Get a Client Receive Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_rx_flow_with_http_info(msg_vpn_name, client_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str flow_id: The identifier (ID) of the flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientRxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'flow_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_rx_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_rx_flow`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_rx_flow`")  # noqa: E501
        # verify the required parameter 'flow_id' is set
        if ('flow_id' not in params or
                params['flow_id'] is None):
            raise ValueError("Missing the required parameter `flow_id` when calling `get_msg_vpn_client_rx_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'flow_id' in params:
            path_params['flowId'] = params['flow_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/rxFlows/{flowId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientRxFlowResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_rx_flows(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Receive Flow objects.  # noqa: E501

        Get a list of Client Receive Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_rx_flows(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientRxFlowsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_rx_flows_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_rx_flows_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_rx_flows_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Receive Flow objects.  # noqa: E501

        Get a list of Client Receive Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_rx_flows_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientRxFlowsResponse
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
                    " to method get_msg_vpn_client_rx_flows" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_rx_flows`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_rx_flows`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_rx_flows`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clients/{clientName}/rxFlows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientRxFlowsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_subscription(self, msg_vpn_name, client_name, subscription_topic, **kwargs):  # noqa: E501
        """Get a Client Subscription object.  # noqa: E501

        Get a Client Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_subscription(msg_vpn_name, client_name, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str subscription_topic: The topic of the Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_subscription_with_http_info(msg_vpn_name, client_name, subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_subscription_with_http_info(msg_vpn_name, client_name, subscription_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_subscription_with_http_info(self, msg_vpn_name, client_name, subscription_topic, **kwargs):  # noqa: E501
        """Get a Client Subscription object.  # noqa: E501

        Get a Client Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_subscription_with_http_info(msg_vpn_name, client_name, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str subscription_topic: The topic of the Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'subscription_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_subscription`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_subscription`")  # noqa: E501
        # verify the required parameter 'subscription_topic' is set
        if ('subscription_topic' not in params or
                params['subscription_topic'] is None):
            raise ValueError("Missing the required parameter `subscription_topic` when calling `get_msg_vpn_client_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'subscription_topic' in params:
            path_params['subscriptionTopic'] = params['subscription_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/subscriptions/{subscriptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_subscriptions(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Subscription objects.  # noqa: E501

        Get a list of Client Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_subscriptions(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_subscriptions_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_subscriptions_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_subscriptions_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Subscription objects.  # noqa: E501

        Get a list of Client Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_subscriptions_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientSubscriptionsResponse
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
                    " to method get_msg_vpn_client_subscriptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_subscriptions`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_subscriptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_subscriptions`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clients/{clientName}/subscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientSubscriptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_transacted_session(self, msg_vpn_name, client_name, session_name, **kwargs):  # noqa: E501
        """Get a Client Transacted Session object.  # noqa: E501

        Get a Client Transacted Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Client Transacted Session object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Client Transacted Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Client Transacted Session objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x| sessionName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_client_tx_flow(self, msg_vpn_name, client_name, flow_id, **kwargs):  # noqa: E501
        """Get a Client Transmit Flow object.  # noqa: E501

        Get a Client Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_tx_flow(msg_vpn_name, client_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str flow_id: The identifier (ID) of the flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_tx_flow_with_http_info(msg_vpn_name, client_name, flow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_tx_flow_with_http_info(msg_vpn_name, client_name, flow_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_tx_flow_with_http_info(self, msg_vpn_name, client_name, flow_id, **kwargs):  # noqa: E501
        """Get a Client Transmit Flow object.  # noqa: E501

        Get a Client Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_tx_flow_with_http_info(msg_vpn_name, client_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param str flow_id: The identifier (ID) of the flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_name', 'flow_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_tx_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_tx_flow`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_tx_flow`")  # noqa: E501
        # verify the required parameter 'flow_id' is set
        if ('flow_id' not in params or
                params['flow_id'] is None):
            raise ValueError("Missing the required parameter `flow_id` when calling `get_msg_vpn_client_tx_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_name' in params:
            path_params['clientName'] = params['client_name']  # noqa: E501
        if 'flow_id' in params:
            path_params['flowId'] = params['flow_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clients/{clientName}/txFlows/{flowId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientTxFlowResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_tx_flows(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Transmit Flow objects.  # noqa: E501

        Get a list of Client Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_tx_flows(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTxFlowsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_tx_flows_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_tx_flows_with_http_info(msg_vpn_name, client_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_tx_flows_with_http_info(self, msg_vpn_name, client_name, **kwargs):  # noqa: E501
        """Get a list of Client Transmit Flow objects.  # noqa: E501

        Get a list of Client Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| flowId|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_tx_flows_with_http_info(msg_vpn_name, client_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_name: The name of the Client. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientTxFlowsResponse
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
                    " to method get_msg_vpn_client_tx_flows" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_tx_flows`")  # noqa: E501
        # verify the required parameter 'client_name' is set
        if ('client_name' not in params or
                params['client_name'] is None):
            raise ValueError("Missing the required parameter `client_name` when calling `get_msg_vpn_client_tx_flows`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_tx_flows`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clients/{clientName}/txFlows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientTxFlowsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_username(self, msg_vpn_name, client_username, **kwargs):  # noqa: E501
        """Get a Client Username object.  # noqa: E501

        Get a Client Username object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientUsername|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_username(msg_vpn_name, client_username, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_username: The value of the Client Username. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientUsernameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_username_with_http_info(msg_vpn_name, client_username, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_username_with_http_info(msg_vpn_name, client_username, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_username_with_http_info(self, msg_vpn_name, client_username, **kwargs):  # noqa: E501
        """Get a Client Username object.  # noqa: E501

        Get a Client Username object.   Attribute|Identifying|Deprecated :---|:---:|:---: clientUsername|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_username_with_http_info(msg_vpn_name, client_username, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str client_username: The value of the Client Username. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientUsernameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'client_username', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_client_username" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_username`")  # noqa: E501
        # verify the required parameter 'client_username' is set
        if ('client_username' not in params or
                params['client_username'] is None):
            raise ValueError("Missing the required parameter `client_username` when calling `get_msg_vpn_client_username`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'client_username' in params:
            path_params['clientUsername'] = params['client_username']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/clientUsernames/{clientUsername}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientUsernameResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_client_usernames(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client Username objects.  # noqa: E501

        Get a list of Client Username objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientUsername|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_usernames(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientUsernamesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_client_usernames_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_client_usernames_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_client_usernames_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client Username objects.  # noqa: E501

        Get a list of Client Username objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientUsername|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_client_usernames_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnClientUsernamesResponse
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
                    " to method get_msg_vpn_client_usernames" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_client_usernames`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_client_usernames`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/clientUsernames', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnClientUsernamesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_clients(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Client objects.  # noqa: E501

        Get a list of Client objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Client objects.   Attribute|Identifying|Deprecated :---|:---:|:---: clientName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_config_sync_remote_node(self, msg_vpn_name, remote_node_name, **kwargs):  # noqa: E501
        """Get a Config Sync Remote Node object.  # noqa: E501

        Get a Config Sync Remote Node object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_config_sync_remote_node(msg_vpn_name, remote_node_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str remote_node_name: The name of the Config Sync Remote Node. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnConfigSyncRemoteNodeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_config_sync_remote_node_with_http_info(msg_vpn_name, remote_node_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_config_sync_remote_node_with_http_info(msg_vpn_name, remote_node_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_config_sync_remote_node_with_http_info(self, msg_vpn_name, remote_node_name, **kwargs):  # noqa: E501
        """Get a Config Sync Remote Node object.  # noqa: E501

        Get a Config Sync Remote Node object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_config_sync_remote_node_with_http_info(msg_vpn_name, remote_node_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str remote_node_name: The name of the Config Sync Remote Node. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnConfigSyncRemoteNodeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'remote_node_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_config_sync_remote_node" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_config_sync_remote_node`")  # noqa: E501
        # verify the required parameter 'remote_node_name' is set
        if ('remote_node_name' not in params or
                params['remote_node_name'] is None):
            raise ValueError("Missing the required parameter `remote_node_name` when calling `get_msg_vpn_config_sync_remote_node`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'remote_node_name' in params:
            path_params['remoteNodeName'] = params['remote_node_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/configSyncRemoteNodes/{remoteNodeName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnConfigSyncRemoteNodeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_config_sync_remote_nodes(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Config Sync Remote Node objects.  # noqa: E501

        Get a list of Config Sync Remote Node objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_config_sync_remote_nodes(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnConfigSyncRemoteNodesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_config_sync_remote_nodes_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_config_sync_remote_nodes_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_config_sync_remote_nodes_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Config Sync Remote Node objects.  # noqa: E501

        Get a list of Config Sync Remote Node objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_config_sync_remote_nodes_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnConfigSyncRemoteNodesResponse
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
                    " to method get_msg_vpn_config_sync_remote_nodes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_config_sync_remote_nodes`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_config_sync_remote_nodes`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/configSyncRemoteNodes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnConfigSyncRemoteNodesResponse',  # noqa: E501
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

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a Home Cache Cluster object.  # noqa: E501

        Get a Home Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster(msg_vpn_name, cache_name, cluster_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_with_http_info(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a Home Cache Cluster object.  # noqa: E501

        Get a Home Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'home_cluster_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'home_cluster_name' is set
        if ('home_cluster_name' not in params or
                params['home_cluster_name'] is None):
            raise ValueError("Missing the required parameter `home_cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'home_cluster_name' in params:
            path_params['homeClusterName'] = params['home_cluster_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/globalCachingHomeClusters/{homeClusterName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterGlobalCachingHomeClusterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, **kwargs):  # noqa: E501
        """Get a Topic Prefix object.  # noqa: E501

        Get a Topic Prefix object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix(msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param str topic_prefix: A topic prefix for global topics available from the remote Home Cache Cluster. A wildcard (/>) is implied at the end of the prefix. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix_with_http_info(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, **kwargs):  # noqa: E501
        """Get a Topic Prefix object.  # noqa: E501

        Get a Topic Prefix object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, topic_prefix, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param str topic_prefix: A topic prefix for global topics available from the remote Home Cache Cluster. A wildcard (/>) is implied at the end of the prefix. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'home_cluster_name', 'topic_prefix', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix`")  # noqa: E501
        # verify the required parameter 'home_cluster_name' is set
        if ('home_cluster_name' not in params or
                params['home_cluster_name'] is None):
            raise ValueError("Missing the required parameter `home_cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix`")  # noqa: E501
        # verify the required parameter 'topic_prefix' is set
        if ('topic_prefix' not in params or
                params['topic_prefix'] is None):
            raise ValueError("Missing the required parameter `topic_prefix` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefix`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'home_cluster_name' in params:
            path_params['homeClusterName'] = params['home_cluster_name']  # noqa: E501
        if 'topic_prefix' in params:
            path_params['topicPrefix'] = params['topic_prefix']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/globalCachingHomeClusters/{homeClusterName}/topicPrefixes/{topicPrefix}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a list of Topic Prefix objects.  # noqa: E501

        Get a list of Topic Prefix objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes(msg_vpn_name, cache_name, cluster_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes_with_http_info(self, msg_vpn_name, cache_name, cluster_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a list of Topic Prefix objects.  # noqa: E501

        Get a list of Topic Prefix objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes_with_http_info(msg_vpn_name, cache_name, cluster_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'home_cluster_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes`")  # noqa: E501
        # verify the required parameter 'home_cluster_name' is set
        if ('home_cluster_name' not in params or
                params['home_cluster_name'] is None):
            raise ValueError("Missing the required parameter `home_cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_cluster_topic_prefixes`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'home_cluster_name' in params:
            path_params['homeClusterName'] = params['home_cluster_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/globalCachingHomeClusters/{homeClusterName}/topicPrefixes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterGlobalCachingHomeClusterTopicPrefixesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Home Cache Cluster objects.  # noqa: E501

        Get a list of Home Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClustersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters_with_http_info(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Home Cache Cluster objects.  # noqa: E501

        Get a list of Home Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterGlobalCachingHomeClustersResponse
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
                    " to method get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_global_caching_home_clusters`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/globalCachingHomeClusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterGlobalCachingHomeClustersResponse',  # noqa: E501
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

    def get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster(self, msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a Remote Home Cache Cluster object.  # noqa: E501

        Get a Remote Home Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster(msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, **kwargs):  # noqa: E501
        """Get a Remote Home Cache Cluster object.  # noqa: E501

        Get a Remote Home Cache Cluster object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, home_cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param str home_cluster_name: The name of the remote Home Cache Cluster. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClusterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'home_cluster_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster`")  # noqa: E501
        # verify the required parameter 'home_cluster_name' is set
        if ('home_cluster_name' not in params or
                params['home_cluster_name'] is None):
            raise ValueError("Missing the required parameter `home_cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_cluster`")  # noqa: E501

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
        if 'home_cluster_name' in params:
            path_params['homeClusterName'] = params['home_cluster_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/remoteGlobalCachingHomeClusters/{homeClusterName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClusterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a list of Remote Home Cache Cluster objects.  # noqa: E501

        Get a list of Remote Home Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClustersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a list of Remote Home Cache Cluster objects.  # noqa: E501

        Get a list of Remote Home Cache Cluster objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClustersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_global_caching_home_clusters`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/remoteGlobalCachingHomeClusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstanceRemoteGlobalCachingHomeClustersResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_instance_remote_topic(self, msg_vpn_name, cache_name, cluster_name, instance_name, topic, **kwargs):  # noqa: E501
        """Get a Remote Topic object.  # noqa: E501

        Get a Remote Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_topic(msg_vpn_name, cache_name, cluster_name, instance_name, topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param str topic: The value of the remote Topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instance_remote_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instance_remote_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instance_remote_topic_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, topic, **kwargs):  # noqa: E501
        """Get a Remote Topic object.  # noqa: E501

        Get a Remote Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param str topic: The value of the remote Topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instance_remote_topic" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topic`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topic`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topic`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topic`")  # noqa: E501
        # verify the required parameter 'topic' is set
        if ('topic' not in params or
                params['topic'] is None):
            raise ValueError("Missing the required parameter `topic` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topic`")  # noqa: E501

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
        if 'topic' in params:
            path_params['topic'] = params['topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/remoteTopics/{topic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstanceRemoteTopicResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_instance_remote_topics(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a list of Remote Topic objects.  # noqa: E501

        Get a list of Remote Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_topics(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteTopicsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_instance_remote_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_instance_remote_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_instance_remote_topics_with_http_info(self, msg_vpn_name, cache_name, cluster_name, instance_name, **kwargs):  # noqa: E501
        """Get a list of Remote Topic objects.  # noqa: E501

        Get a list of Remote Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_instance_remote_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, instance_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str instance_name: The name of the Cache Instance. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterInstanceRemoteTopicsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'instance_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_instance_remote_topics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topics`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topics`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topics`")  # noqa: E501
        # verify the required parameter 'instance_name' is set
        if ('instance_name' not in params or
                params['instance_name'] is None):
            raise ValueError("Missing the required parameter `instance_name` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topics`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_instance_remote_topics`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/instances/{instanceName}/remoteTopics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterInstanceRemoteTopicsResponse',  # noqa: E501
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

    def get_msg_vpn_distributed_cache_cluster_topic(self, msg_vpn_name, cache_name, cluster_name, topic, **kwargs):  # noqa: E501
        """Get a Topic object.  # noqa: E501

        Get a Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_topic(msg_vpn_name, cache_name, cluster_name, topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str topic: The value of the Topic in the form a/b/c. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_topic_with_http_info(self, msg_vpn_name, cache_name, cluster_name, topic, **kwargs):  # noqa: E501
        """Get a Topic object.  # noqa: E501

        Get a Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_topic_with_http_info(msg_vpn_name, cache_name, cluster_name, topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param str topic: The value of the Topic in the form a/b/c. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'cache_name', 'cluster_name', 'topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_distributed_cache_cluster_topic" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_topic`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_topic`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_topic`")  # noqa: E501
        # verify the required parameter 'topic' is set
        if ('topic' not in params or
                params['topic'] is None):
            raise ValueError("Missing the required parameter `topic` when calling `get_msg_vpn_distributed_cache_cluster_topic`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'cache_name' in params:
            path_params['cacheName'] = params['cache_name']  # noqa: E501
        if 'cluster_name' in params:
            path_params['clusterName'] = params['cluster_name']  # noqa: E501
        if 'topic' in params:
            path_params['topic'] = params['topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/topics/{topic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterTopicResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_distributed_cache_cluster_topics(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Topic objects.  # noqa: E501

        Get a list of Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_topics(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterTopicsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_distributed_cache_cluster_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_distributed_cache_cluster_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_distributed_cache_cluster_topics_with_http_info(self, msg_vpn_name, cache_name, cluster_name, **kwargs):  # noqa: E501
        """Get a list of Topic objects.  # noqa: E501

        Get a list of Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_distributed_cache_cluster_topics_with_http_info(msg_vpn_name, cache_name, cluster_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the Distributed Cache. (required)
        :param str cluster_name: The name of the Cache Cluster. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDistributedCacheClusterTopicsResponse
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
                    " to method get_msg_vpn_distributed_cache_cluster_topics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_distributed_cache_cluster_topics`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_distributed_cache_cluster_topics`")  # noqa: E501
        # verify the required parameter 'cluster_name' is set
        if ('cluster_name' not in params or
                params['cluster_name'] is None):
            raise ValueError("Missing the required parameter `cluster_name` when calling `get_msg_vpn_distributed_cache_cluster_topics`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_distributed_cache_cluster_topics`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/distributedCaches/{cacheName}/clusters/{clusterName}/topics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDistributedCacheClusterTopicsResponse',  # noqa: E501
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

    def get_msg_vpn_dmr_bridge(self, msg_vpn_name, remote_node_name, **kwargs):  # noqa: E501
        """Get a DMR Bridge object.  # noqa: E501

        Get a DMR Bridge object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_dmr_bridge(msg_vpn_name, remote_node_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str remote_node_name: The name of the node at the remote end of the DMR Bridge. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDmrBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_dmr_bridge_with_http_info(msg_vpn_name, remote_node_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_dmr_bridge_with_http_info(msg_vpn_name, remote_node_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_dmr_bridge_with_http_info(self, msg_vpn_name, remote_node_name, **kwargs):  # noqa: E501
        """Get a DMR Bridge object.  # noqa: E501

        Get a DMR Bridge object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_dmr_bridge_with_http_info(msg_vpn_name, remote_node_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str remote_node_name: The name of the node at the remote end of the DMR Bridge. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDmrBridgeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'remote_node_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_dmr_bridge" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_dmr_bridge`")  # noqa: E501
        # verify the required parameter 'remote_node_name' is set
        if ('remote_node_name' not in params or
                params['remote_node_name'] is None):
            raise ValueError("Missing the required parameter `remote_node_name` when calling `get_msg_vpn_dmr_bridge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'remote_node_name' in params:
            path_params['remoteNodeName'] = params['remote_node_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/dmrBridges/{remoteNodeName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDmrBridgeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_dmr_bridges(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of DMR Bridge objects.  # noqa: E501

        Get a list of DMR Bridge objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_dmr_bridges(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDmrBridgesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_dmr_bridges_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_dmr_bridges_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_dmr_bridges_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of DMR Bridge objects.  # noqa: E501

        Get a list of DMR Bridge objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| remoteNodeName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_dmr_bridges_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnDmrBridgesResponse
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
                    " to method get_msg_vpn_dmr_bridges" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_dmr_bridges`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_dmr_bridges`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/dmrBridges', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnDmrBridgesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_connection_factories(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Connection Factory objects.  # noqa: E501

        Get a list of JNDI Connection Factory objects.   Attribute|Identifying|Deprecated :---|:---:|:---: connectionFactoryName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_connection_factories(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiConnectionFactoriesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_connection_factories_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_connection_factories_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_connection_factories_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Connection Factory objects.  # noqa: E501

        Get a list of JNDI Connection Factory objects.   Attribute|Identifying|Deprecated :---|:---:|:---: connectionFactoryName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_connection_factories_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiConnectionFactoriesResponse
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
                    " to method get_msg_vpn_jndi_connection_factories" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_connection_factories`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_jndi_connection_factories`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/jndiConnectionFactories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiConnectionFactoriesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_connection_factory(self, msg_vpn_name, connection_factory_name, **kwargs):  # noqa: E501
        """Get a JNDI Connection Factory object.  # noqa: E501

        Get a JNDI Connection Factory object.   Attribute|Identifying|Deprecated :---|:---:|:---: connectionFactoryName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_connection_factory(msg_vpn_name, connection_factory_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str connection_factory_name: The name of the JMS Connection Factory. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiConnectionFactoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_connection_factory_with_http_info(msg_vpn_name, connection_factory_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_connection_factory_with_http_info(msg_vpn_name, connection_factory_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_connection_factory_with_http_info(self, msg_vpn_name, connection_factory_name, **kwargs):  # noqa: E501
        """Get a JNDI Connection Factory object.  # noqa: E501

        Get a JNDI Connection Factory object.   Attribute|Identifying|Deprecated :---|:---:|:---: connectionFactoryName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_connection_factory_with_http_info(msg_vpn_name, connection_factory_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str connection_factory_name: The name of the JMS Connection Factory. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiConnectionFactoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'connection_factory_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_jndi_connection_factory" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_connection_factory`")  # noqa: E501
        # verify the required parameter 'connection_factory_name' is set
        if ('connection_factory_name' not in params or
                params['connection_factory_name'] is None):
            raise ValueError("Missing the required parameter `connection_factory_name` when calling `get_msg_vpn_jndi_connection_factory`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'connection_factory_name' in params:
            path_params['connectionFactoryName'] = params['connection_factory_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/jndiConnectionFactories/{connectionFactoryName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiConnectionFactoryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_queue(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a JNDI Queue object.  # noqa: E501

        Get a JNDI Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_queue(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The JNDI name of the JMS Queue. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiQueueResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_queue_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_queue_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_queue_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a JNDI Queue object.  # noqa: E501

        Get a JNDI Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_queue_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The JNDI name of the JMS Queue. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiQueueResponse
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
                    " to method get_msg_vpn_jndi_queue" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_queue`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_jndi_queue`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/jndiQueues/{queueName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiQueueResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_queues(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Queue objects.  # noqa: E501

        Get a list of JNDI Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_queues(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiQueuesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_queues_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_queues_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_queues_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Queue objects.  # noqa: E501

        Get a list of JNDI Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_queues_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiQueuesResponse
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
                    " to method get_msg_vpn_jndi_queues" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_queues`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_jndi_queues`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/jndiQueues', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiQueuesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_topic(self, msg_vpn_name, topic_name, **kwargs):  # noqa: E501
        """Get a JNDI Topic object.  # noqa: E501

        Get a JNDI Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_topic(msg_vpn_name, topic_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_name: The JNDI name of the JMS Topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_topic_with_http_info(msg_vpn_name, topic_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_topic_with_http_info(msg_vpn_name, topic_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_topic_with_http_info(self, msg_vpn_name, topic_name, **kwargs):  # noqa: E501
        """Get a JNDI Topic object.  # noqa: E501

        Get a JNDI Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_topic_with_http_info(msg_vpn_name, topic_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_name: The JNDI name of the JMS Topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_jndi_topic" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_topic`")  # noqa: E501
        # verify the required parameter 'topic_name' is set
        if ('topic_name' not in params or
                params['topic_name'] is None):
            raise ValueError("Missing the required parameter `topic_name` when calling `get_msg_vpn_jndi_topic`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_name' in params:
            path_params['topicName'] = params['topic_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/jndiTopics/{topicName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiTopicResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_jndi_topics(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Topic objects.  # noqa: E501

        Get a list of JNDI Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_topics(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiTopicsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_jndi_topics_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_jndi_topics_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_jndi_topics_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of JNDI Topic objects.  # noqa: E501

        Get a list of JNDI Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_jndi_topics_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnJndiTopicsResponse
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
                    " to method get_msg_vpn_jndi_topics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_jndi_topics`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_jndi_topics`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/jndiTopics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnJndiTopicsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_mqtt_retain_cache(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get an MQTT Retain Cache object.  # noqa: E501

        Get an MQTT Retain Cache object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_retain_cache(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the MQTT Retain Cache. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttRetainCacheResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_retain_cache_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_retain_cache_with_http_info(msg_vpn_name, cache_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_retain_cache_with_http_info(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get an MQTT Retain Cache object.  # noqa: E501

        Get an MQTT Retain Cache object.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_retain_cache_with_http_info(msg_vpn_name, cache_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str cache_name: The name of the MQTT Retain Cache. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttRetainCacheResponse
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
                    " to method get_msg_vpn_mqtt_retain_cache" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_retain_cache`")  # noqa: E501
        # verify the required parameter 'cache_name' is set
        if ('cache_name' not in params or
                params['cache_name'] is None):
            raise ValueError("Missing the required parameter `cache_name` when calling `get_msg_vpn_mqtt_retain_cache`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/mqttRetainCaches/{cacheName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttRetainCacheResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_mqtt_retain_caches(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of MQTT Retain Cache objects.  # noqa: E501

        Get a list of MQTT Retain Cache objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_retain_caches(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttRetainCachesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_retain_caches_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_retain_caches_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_retain_caches_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of MQTT Retain Cache objects.  # noqa: E501

        Get a list of MQTT Retain Cache objects.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_retain_caches_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttRetainCachesResponse
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
                    " to method get_msg_vpn_mqtt_retain_caches" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_retain_caches`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_mqtt_retain_caches`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/mqttRetainCaches', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttRetainCachesResponse',  # noqa: E501
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

    def get_msg_vpn_mqtt_session_subscription(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, **kwargs):  # noqa: E501
        """Get a Subscription object.  # noqa: E501

        Get a Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session_subscription(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param str subscription_topic: The MQTT subscription topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_session_subscription_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_session_subscription_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_session_subscription_with_http_info(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, **kwargs):  # noqa: E501
        """Get a Subscription object.  # noqa: E501

        Get a Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session_subscription_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param str subscription_topic: The MQTT subscription topic. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'mqtt_session_client_id', 'mqtt_session_virtual_router', 'subscription_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_mqtt_session_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_session_subscription`")  # noqa: E501
        # verify the required parameter 'mqtt_session_client_id' is set
        if ('mqtt_session_client_id' not in params or
                params['mqtt_session_client_id'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_client_id` when calling `get_msg_vpn_mqtt_session_subscription`")  # noqa: E501
        # verify the required parameter 'mqtt_session_virtual_router' is set
        if ('mqtt_session_virtual_router' not in params or
                params['mqtt_session_virtual_router'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_virtual_router` when calling `get_msg_vpn_mqtt_session_subscription`")  # noqa: E501
        # verify the required parameter 'subscription_topic' is set
        if ('subscription_topic' not in params or
                params['subscription_topic'] is None):
            raise ValueError("Missing the required parameter `subscription_topic` when calling `get_msg_vpn_mqtt_session_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'mqtt_session_client_id' in params:
            path_params['mqttSessionClientId'] = params['mqtt_session_client_id']  # noqa: E501
        if 'mqtt_session_virtual_router' in params:
            path_params['mqttSessionVirtualRouter'] = params['mqtt_session_virtual_router']  # noqa: E501
        if 'subscription_topic' in params:
            path_params['subscriptionTopic'] = params['subscription_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/mqttSessions/{mqttSessionClientId},{mqttSessionVirtualRouter}/subscriptions/{subscriptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttSessionSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_mqtt_session_subscriptions(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Subscription objects.  # noqa: E501

        Get a list of Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session_subscriptions(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_mqtt_session_subscriptions_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_mqtt_session_subscriptions_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_mqtt_session_subscriptions_with_http_info(self, msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, **kwargs):  # noqa: E501
        """Get a list of Subscription objects.  # noqa: E501

        Get a list of Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: mqttSessionClientId|x| mqttSessionVirtualRouter|x| msgVpnName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_mqtt_session_subscriptions_with_http_info(msg_vpn_name, mqtt_session_client_id, mqtt_session_virtual_router, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str mqtt_session_client_id: The Client ID of the MQTT Session, which corresponds to the ClientId provided in the MQTT CONNECT packet. (required)
        :param str mqtt_session_virtual_router: The virtual router of the MQTT Session. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnMqttSessionSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'mqtt_session_client_id', 'mqtt_session_virtual_router', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_mqtt_session_subscriptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_mqtt_session_subscriptions`")  # noqa: E501
        # verify the required parameter 'mqtt_session_client_id' is set
        if ('mqtt_session_client_id' not in params or
                params['mqtt_session_client_id'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_client_id` when calling `get_msg_vpn_mqtt_session_subscriptions`")  # noqa: E501
        # verify the required parameter 'mqtt_session_virtual_router' is set
        if ('mqtt_session_virtual_router' not in params or
                params['mqtt_session_virtual_router'] is None):
            raise ValueError("Missing the required parameter `mqtt_session_virtual_router` when calling `get_msg_vpn_mqtt_session_subscriptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_mqtt_session_subscriptions`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'mqtt_session_client_id' in params:
            path_params['mqttSessionClientId'] = params['mqtt_session_client_id']  # noqa: E501
        if 'mqtt_session_virtual_router' in params:
            path_params['mqttSessionVirtualRouter'] = params['mqtt_session_virtual_router']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/mqttSessions/{mqttSessionClientId},{mqttSessionVirtualRouter}/subscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnMqttSessionSubscriptionsResponse',  # noqa: E501
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

        Get a Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Queue object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Queue Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Queue Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Queue Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Queue Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_queue_priorities(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Priority objects.  # noqa: E501

        Get a list of Queue Priority objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_priorities(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuePrioritiesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_priorities_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_priorities_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_priorities_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Priority objects.  # noqa: E501

        Get a list of Queue Priority objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_priorities_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuePrioritiesResponse
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
                    " to method get_msg_vpn_queue_priorities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_priorities`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_priorities`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_queue_priorities`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/queues/{queueName}/priorities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueuePrioritiesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_priority(self, msg_vpn_name, queue_name, priority, **kwargs):  # noqa: E501
        """Get a Queue Priority object.  # noqa: E501

        Get a Queue Priority object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_priority(msg_vpn_name, queue_name, priority, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str priority: The level of the Priority, from 9 (highest) to 0 (lowest). (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuePriorityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_priority_with_http_info(msg_vpn_name, queue_name, priority, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_priority_with_http_info(msg_vpn_name, queue_name, priority, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_priority_with_http_info(self, msg_vpn_name, queue_name, priority, **kwargs):  # noqa: E501
        """Get a Queue Priority object.  # noqa: E501

        Get a Queue Priority object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_priority_with_http_info(msg_vpn_name, queue_name, priority, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str priority: The level of the Priority, from 9 (highest) to 0 (lowest). (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueuePriorityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'priority', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue_priority" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_priority`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_priority`")  # noqa: E501
        # verify the required parameter 'priority' is set
        if ('priority' not in params or
                params['priority'] is None):
            raise ValueError("Missing the required parameter `priority` when calling `get_msg_vpn_queue_priority`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501
        if 'priority' in params:
            path_params['priority'] = params['priority']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/priorities/{priority}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueuePriorityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_subscription(self, msg_vpn_name, queue_name, subscription_topic, **kwargs):  # noqa: E501
        """Get a Queue Subscription object.  # noqa: E501

        Get a Queue Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_subscription(msg_vpn_name, queue_name, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str subscription_topic: The topic of the Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_subscription_with_http_info(msg_vpn_name, queue_name, subscription_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_subscription_with_http_info(msg_vpn_name, queue_name, subscription_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_subscription_with_http_info(self, msg_vpn_name, queue_name, subscription_topic, **kwargs):  # noqa: E501
        """Get a Queue Subscription object.  # noqa: E501

        Get a Queue Subscription object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_subscription_with_http_info(msg_vpn_name, queue_name, subscription_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str subscription_topic: The topic of the Subscription. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueSubscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'subscription_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue_subscription" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_subscription`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_subscription`")  # noqa: E501
        # verify the required parameter 'subscription_topic' is set
        if ('subscription_topic' not in params or
                params['subscription_topic'] is None):
            raise ValueError("Missing the required parameter `subscription_topic` when calling `get_msg_vpn_queue_subscription`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501
        if 'subscription_topic' in params:
            path_params['subscriptionTopic'] = params['subscription_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/subscriptions/{subscriptionTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueSubscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_subscriptions(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Subscription objects.  # noqa: E501

        Get a list of Queue Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_subscriptions(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueSubscriptionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_subscriptions_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_subscriptions_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_subscriptions_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Subscription objects.  # noqa: E501

        Get a list of Queue Subscription objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x| subscriptionTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_subscriptions_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueSubscriptionsResponse
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
                    " to method get_msg_vpn_queue_subscriptions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_subscriptions`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_subscriptions`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_queue_subscriptions`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/queues/{queueName}/subscriptions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueSubscriptionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_tx_flow(self, msg_vpn_name, queue_name, flow_id, **kwargs):  # noqa: E501
        """Get a Queue Transmit Flow object.  # noqa: E501

        Get a Queue Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_tx_flow(msg_vpn_name, queue_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str flow_id: The identifier (ID) of the Flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_tx_flow_with_http_info(msg_vpn_name, queue_name, flow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_tx_flow_with_http_info(msg_vpn_name, queue_name, flow_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_tx_flow_with_http_info(self, msg_vpn_name, queue_name, flow_id, **kwargs):  # noqa: E501
        """Get a Queue Transmit Flow object.  # noqa: E501

        Get a Queue Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_tx_flow_with_http_info(msg_vpn_name, queue_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param str flow_id: The identifier (ID) of the Flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'queue_name', 'flow_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_queue_tx_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_tx_flow`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_tx_flow`")  # noqa: E501
        # verify the required parameter 'flow_id' is set
        if ('flow_id' not in params or
                params['flow_id'] is None):
            raise ValueError("Missing the required parameter `flow_id` when calling `get_msg_vpn_queue_tx_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'queue_name' in params:
            path_params['queueName'] = params['queue_name']  # noqa: E501
        if 'flow_id' in params:
            path_params['flowId'] = params['flow_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/queues/{queueName}/txFlows/{flowId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueTxFlowResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queue_tx_flows(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Transmit Flow objects.  # noqa: E501

        Get a list of Queue Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_tx_flows(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueTxFlowsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_queue_tx_flows_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_queue_tx_flows_with_http_info(msg_vpn_name, queue_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_queue_tx_flows_with_http_info(self, msg_vpn_name, queue_name, **kwargs):  # noqa: E501
        """Get a list of Queue Transmit Flow objects.  # noqa: E501

        Get a list of Queue Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_queue_tx_flows_with_http_info(msg_vpn_name, queue_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str queue_name: The name of the Queue. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnQueueTxFlowsResponse
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
                    " to method get_msg_vpn_queue_tx_flows" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_queue_tx_flows`")  # noqa: E501
        # verify the required parameter 'queue_name' is set
        if ('queue_name' not in params or
                params['queue_name'] is None):
            raise ValueError("Missing the required parameter `queue_name` when calling `get_msg_vpn_queue_tx_flows`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_queue_tx_flows`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/queues/{queueName}/txFlows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnQueueTxFlowsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_queues(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Queue objects.  # noqa: E501

        Get a list of Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Queue objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_replay_log_msg(self, msg_vpn_name, replay_log_name, msg_id, **kwargs):  # noqa: E501
        """Get a Message object.  # noqa: E501

        Get a Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log_msg(msg_vpn_name, replay_log_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param str msg_id: The identifier (ID) of the message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replay_log_msg_with_http_info(msg_vpn_name, replay_log_name, msg_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replay_log_msg_with_http_info(msg_vpn_name, replay_log_name, msg_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replay_log_msg_with_http_info(self, msg_vpn_name, replay_log_name, msg_id, **kwargs):  # noqa: E501
        """Get a Message object.  # noqa: E501

        Get a Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log_msg_with_http_info(msg_vpn_name, replay_log_name, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param str msg_id: The identifier (ID) of the message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'replay_log_name', 'msg_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_replay_log_msg" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replay_log_msg`")  # noqa: E501
        # verify the required parameter 'replay_log_name' is set
        if ('replay_log_name' not in params or
                params['replay_log_name'] is None):
            raise ValueError("Missing the required parameter `replay_log_name` when calling `get_msg_vpn_replay_log_msg`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `get_msg_vpn_replay_log_msg`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'replay_log_name' in params:
            path_params['replayLogName'] = params['replay_log_name']  # noqa: E501
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
            '/msgVpns/{msgVpnName}/replayLogs/{replayLogName}/msgs/{msgId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplayLogMsgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_replay_log_msgs(self, msg_vpn_name, replay_log_name, **kwargs):  # noqa: E501
        """Get a list of Message objects.  # noqa: E501

        Get a list of Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log_msgs(msg_vpn_name, replay_log_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replay_log_msgs_with_http_info(msg_vpn_name, replay_log_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replay_log_msgs_with_http_info(msg_vpn_name, replay_log_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replay_log_msgs_with_http_info(self, msg_vpn_name, replay_log_name, **kwargs):  # noqa: E501
        """Get a list of Message objects.  # noqa: E501

        Get a list of Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| replayLogName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replay_log_msgs_with_http_info(msg_vpn_name, replay_log_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replay_log_name: The name of the Replay Log. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplayLogMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'replay_log_name', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_replay_log_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replay_log_msgs`")  # noqa: E501
        # verify the required parameter 'replay_log_name' is set
        if ('replay_log_name' not in params or
                params['replay_log_name'] is None):
            raise ValueError("Missing the required parameter `replay_log_name` when calling `get_msg_vpn_replay_log_msgs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_replay_log_msgs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'replay_log_name' in params:
            path_params['replayLogName'] = params['replay_log_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/replayLogs/{replayLogName}/msgs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplayLogMsgsResponse',  # noqa: E501
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

    def get_msg_vpn_replicated_topic(self, msg_vpn_name, replicated_topic, **kwargs):  # noqa: E501
        """Get a Replicated Topic object.  # noqa: E501

        Get a Replicated Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replicatedTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replicated_topic(msg_vpn_name, replicated_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replicated_topic: The topic for applying replication. Published messages matching this topic will be replicated to the standby site. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplicatedTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replicated_topic_with_http_info(msg_vpn_name, replicated_topic, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replicated_topic_with_http_info(msg_vpn_name, replicated_topic, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replicated_topic_with_http_info(self, msg_vpn_name, replicated_topic, **kwargs):  # noqa: E501
        """Get a Replicated Topic object.  # noqa: E501

        Get a Replicated Topic object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replicatedTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replicated_topic_with_http_info(msg_vpn_name, replicated_topic, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str replicated_topic: The topic for applying replication. Published messages matching this topic will be replicated to the standby site. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplicatedTopicResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'replicated_topic', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_replicated_topic" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replicated_topic`")  # noqa: E501
        # verify the required parameter 'replicated_topic' is set
        if ('replicated_topic' not in params or
                params['replicated_topic'] is None):
            raise ValueError("Missing the required parameter `replicated_topic` when calling `get_msg_vpn_replicated_topic`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'replicated_topic' in params:
            path_params['replicatedTopic'] = params['replicated_topic']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/replicatedTopics/{replicatedTopic}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplicatedTopicResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_replicated_topics(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replicated Topic objects.  # noqa: E501

        Get a list of Replicated Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replicatedTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replicated_topics(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplicatedTopicsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_replicated_topics_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_replicated_topics_with_http_info(msg_vpn_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_replicated_topics_with_http_info(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Replicated Topic objects.  # noqa: E501

        Get a list of Replicated Topic objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| replicatedTopic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_replicated_topics_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnReplicatedTopicsResponse
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
                    " to method get_msg_vpn_replicated_topics" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_replicated_topics`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_replicated_topics`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/replicatedTopics', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnReplicatedTopicsResponse',  # noqa: E501
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

    def get_msg_vpn_rest_delivery_point_queue_binding(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs):  # noqa: E501
        """Get a Queue Binding object.  # noqa: E501

        Get a Queue Binding object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueBindingName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str queue_binding_name: The name of a queue in the Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_queue_binding_with_http_info(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs):  # noqa: E501
        """Get a Queue Binding object.  # noqa: E501

        Get a Queue Binding object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueBindingName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str queue_binding_name: The name of a queue in the Message VPN. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'queue_binding_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point_queue_binding" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'queue_binding_name' is set
        if ('queue_binding_name' not in params or
                params['queue_binding_name'] is None):
            raise ValueError("Missing the required parameter `queue_binding_name` when calling `get_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'queue_binding_name' in params:
            path_params['queueBindingName'] = params['queue_binding_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings/{queueBindingName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointQueueBindingResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_point_queue_bindings(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a list of Queue Binding objects.  # noqa: E501

        Get a list of Queue Binding objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueBindingName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_bindings(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointQueueBindingsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_queue_bindings_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_queue_bindings_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_queue_bindings_with_http_info(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Get a list of Queue Binding objects.  # noqa: E501

        Get a list of Queue Binding objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| queueBindingName|x| restDeliveryPointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_bindings_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointQueueBindingsResponse
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
                    " to method get_msg_vpn_rest_delivery_point_queue_bindings" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_queue_bindings`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_queue_bindings`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_rest_delivery_point_queue_bindings`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointQueueBindingsResponse',  # noqa: E501
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

    def get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Get a Trusted Common Name object.  # noqa: E501

        Get a Trusted Common Name object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param str tls_trusted_common_name: The expected trusted common name of the remote certificate. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Get a Trusted Common Name object.  # noqa: E501

        Get a Trusted Common Name object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param str tls_trusted_common_name: The expected trusted common name of the remote certificate. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'tls_trusted_common_name', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'tls_trusted_common_name' is set
        if ('tls_trusted_common_name' not in params or
                params['tls_trusted_common_name'] is None):
            raise ValueError("Missing the required parameter `tls_trusted_common_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'rest_consumer_name' in params:
            path_params['restConsumerName'] = params['rest_consumer_name']  # noqa: E501
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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}/tlsTrustedCommonNames/{tlsTrustedCommonName}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNameResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Get a list of Trusted Common Name objects.  # noqa: E501

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNamesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Get a list of Trusted Common Name objects.  # noqa: E501

        Get a list of Trusted Common Name objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| restConsumerName|x| restDeliveryPointName|x| tlsTrustedCommonName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str rest_delivery_point_name: The name of the REST Delivery Point. (required)
        :param str rest_consumer_name: The name of the REST Consumer. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNamesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'rest_consumer_name' in params:
            path_params['restConsumerName'] = params['rest_consumer_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}/tlsTrustedCommonNames', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNamesResponse',  # noqa: E501
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

        Get a Topic Endpoint object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Topic Endpoint object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Topic Endpoint Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a Topic Endpoint Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Topic Endpoint Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Topic Endpoint Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_topic_endpoint_priorities(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Priority objects.  # noqa: E501

        Get a list of Topic Endpoint Priority objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_priorities(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointPrioritiesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_priorities_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_priorities_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_priorities_with_http_info(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Priority objects.  # noqa: E501

        Get a list of Topic Endpoint Priority objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_priorities_with_http_info(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointPrioritiesResponse
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
                    " to method get_msg_vpn_topic_endpoint_priorities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_priorities`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_priorities`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_topic_endpoint_priorities`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/priorities', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointPrioritiesResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint_priority(self, msg_vpn_name, topic_endpoint_name, priority, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Priority object.  # noqa: E501

        Get a Topic Endpoint Priority object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_priority(msg_vpn_name, topic_endpoint_name, priority, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str priority: The level of the Priority, from 9 (highest) to 0 (lowest). (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointPriorityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_priority_with_http_info(msg_vpn_name, topic_endpoint_name, priority, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_priority_with_http_info(msg_vpn_name, topic_endpoint_name, priority, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_priority_with_http_info(self, msg_vpn_name, topic_endpoint_name, priority, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Priority object.  # noqa: E501

        Get a Topic Endpoint Priority object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| priority|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_priority_with_http_info(msg_vpn_name, topic_endpoint_name, priority, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str priority: The level of the Priority, from 9 (highest) to 0 (lowest). (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointPriorityResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'priority', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_topic_endpoint_priority" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_priority`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_priority`")  # noqa: E501
        # verify the required parameter 'priority' is set
        if ('priority' not in params or
                params['priority'] is None):
            raise ValueError("Missing the required parameter `priority` when calling `get_msg_vpn_topic_endpoint_priority`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501
        if 'priority' in params:
            path_params['priority'] = params['priority']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/priorities/{priority}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointPriorityResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint_tx_flow(self, msg_vpn_name, topic_endpoint_name, flow_id, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Transmit Flow object.  # noqa: E501

        Get a Topic Endpoint Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_tx_flow(msg_vpn_name, topic_endpoint_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str flow_id: The identifier (ID) of the Flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_tx_flow_with_http_info(msg_vpn_name, topic_endpoint_name, flow_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_tx_flow_with_http_info(msg_vpn_name, topic_endpoint_name, flow_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_tx_flow_with_http_info(self, msg_vpn_name, topic_endpoint_name, flow_id, **kwargs):  # noqa: E501
        """Get a Topic Endpoint Transmit Flow object.  # noqa: E501

        Get a Topic Endpoint Transmit Flow object.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_tx_flow_with_http_info(msg_vpn_name, topic_endpoint_name, flow_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param str flow_id: The identifier (ID) of the Flow. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointTxFlowResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'topic_endpoint_name', 'flow_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_topic_endpoint_tx_flow" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_tx_flow`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_tx_flow`")  # noqa: E501
        # verify the required parameter 'flow_id' is set
        if ('flow_id' not in params or
                params['flow_id'] is None):
            raise ValueError("Missing the required parameter `flow_id` when calling `get_msg_vpn_topic_endpoint_tx_flow`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'topic_endpoint_name' in params:
            path_params['topicEndpointName'] = params['topic_endpoint_name']  # noqa: E501
        if 'flow_id' in params:
            path_params['flowId'] = params['flow_id']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/txFlows/{flowId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointTxFlowResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoint_tx_flows(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Transmit Flow objects.  # noqa: E501

        Get a list of Topic Endpoint Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_tx_flows(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointTxFlowsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_topic_endpoint_tx_flows_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_topic_endpoint_tx_flows_with_http_info(msg_vpn_name, topic_endpoint_name, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_topic_endpoint_tx_flows_with_http_info(self, msg_vpn_name, topic_endpoint_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint Transmit Flow objects.  # noqa: E501

        Get a list of Topic Endpoint Transmit Flow objects.   Attribute|Identifying|Deprecated :---|:---:|:---: flowId|x| msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_topic_endpoint_tx_flows_with_http_info(msg_vpn_name, topic_endpoint_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str topic_endpoint_name: The name of the Topic Endpoint. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTopicEndpointTxFlowsResponse
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
                    " to method get_msg_vpn_topic_endpoint_tx_flows" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_topic_endpoint_tx_flows`")  # noqa: E501
        # verify the required parameter 'topic_endpoint_name' is set
        if ('topic_endpoint_name' not in params or
                params['topic_endpoint_name'] is None):
            raise ValueError("Missing the required parameter `topic_endpoint_name` when calling `get_msg_vpn_topic_endpoint_tx_flows`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_topic_endpoint_tx_flows`, must be a value greater than or equal to `1`")  # noqa: E501
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
            '/msgVpns/{msgVpnName}/topicEndpoints/{topicEndpointName}/txFlows', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTopicEndpointTxFlowsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_topic_endpoints(self, msg_vpn_name, **kwargs):  # noqa: E501
        """Get a list of Topic Endpoint objects.  # noqa: E501

        Get a list of Topic Endpoint objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

        Get a list of Topic Endpoint objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgVpnName|x| topicEndpointName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
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

    def get_msg_vpn_transaction_consumer_msg(self, msg_vpn_name, xid, msg_id, **kwargs):  # noqa: E501
        """Get a Transaction Consumer Message object.  # noqa: E501

        Get a Transaction Consumer Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_consumer_msg(msg_vpn_name, xid, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionConsumerMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transaction_consumer_msg_with_http_info(msg_vpn_name, xid, msg_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transaction_consumer_msg_with_http_info(msg_vpn_name, xid, msg_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transaction_consumer_msg_with_http_info(self, msg_vpn_name, xid, msg_id, **kwargs):  # noqa: E501
        """Get a Transaction Consumer Message object.  # noqa: E501

        Get a Transaction Consumer Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_consumer_msg_with_http_info(msg_vpn_name, xid, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionConsumerMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'msg_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_transaction_consumer_msg" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transaction_consumer_msg`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `get_msg_vpn_transaction_consumer_msg`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `get_msg_vpn_transaction_consumer_msg`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501
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
            '/msgVpns/{msgVpnName}/transactions/{xid}/consumerMsgs/{msgId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionConsumerMsgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_transaction_consumer_msgs(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a list of Transaction Consumer Message objects.  # noqa: E501

        Get a list of Transaction Consumer Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_consumer_msgs(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionConsumerMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transaction_consumer_msgs_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transaction_consumer_msgs_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transaction_consumer_msgs_with_http_info(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a list of Transaction Consumer Message objects.  # noqa: E501

        Get a list of Transaction Consumer Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_consumer_msgs_with_http_info(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionConsumerMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_transaction_consumer_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transaction_consumer_msgs`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `get_msg_vpn_transaction_consumer_msgs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_transaction_consumer_msgs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/transactions/{xid}/consumerMsgs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionConsumerMsgsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_transaction_publisher_msg(self, msg_vpn_name, xid, msg_id, **kwargs):  # noqa: E501
        """Get a Transaction Publisher Message object.  # noqa: E501

        Get a Transaction Publisher Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_publisher_msg(msg_vpn_name, xid, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionPublisherMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transaction_publisher_msg_with_http_info(msg_vpn_name, xid, msg_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transaction_publisher_msg_with_http_info(msg_vpn_name, xid, msg_id, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transaction_publisher_msg_with_http_info(self, msg_vpn_name, xid, msg_id, **kwargs):  # noqa: E501
        """Get a Transaction Publisher Message object.  # noqa: E501

        Get a Transaction Publisher Message object.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_publisher_msg_with_http_info(msg_vpn_name, xid, msg_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param str msg_id: The identifier (ID) of the Message. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionPublisherMsgResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'msg_id', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_transaction_publisher_msg" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transaction_publisher_msg`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `get_msg_vpn_transaction_publisher_msg`")  # noqa: E501
        # verify the required parameter 'msg_id' is set
        if ('msg_id' not in params or
                params['msg_id'] is None):
            raise ValueError("Missing the required parameter `msg_id` when calling `get_msg_vpn_transaction_publisher_msg`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501
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
            '/msgVpns/{msgVpnName}/transactions/{xid}/publisherMsgs/{msgId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionPublisherMsgResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_msg_vpn_transaction_publisher_msgs(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a list of Transaction Publisher Message objects.  # noqa: E501

        Get a list of Transaction Publisher Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_publisher_msgs(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionPublisherMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_msg_vpn_transaction_publisher_msgs_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_msg_vpn_transaction_publisher_msgs_with_http_info(msg_vpn_name, xid, **kwargs)  # noqa: E501
            return data

    def get_msg_vpn_transaction_publisher_msgs_with_http_info(self, msg_vpn_name, xid, **kwargs):  # noqa: E501
        """Get a list of Transaction Publisher Message objects.  # noqa: E501

        Get a list of Transaction Publisher Message objects.   Attribute|Identifying|Deprecated :---|:---:|:---: msgId|x| msgVpnName|x| xid|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.12.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_transaction_publisher_msgs_with_http_info(msg_vpn_name, xid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The name of the Message VPN. (required)
        :param str xid: The identifier (ID) of the Transaction. (required)
        :param int count: Limit the count of objects in the response. See the documentation for the `count` parameter.
        :param str cursor: The cursor, or position, for the next page of objects. See the documentation for the `cursor` parameter.
        :param list[str] where: Include in the response only objects where certain conditions are true. See the the documentation for the `where` parameter.
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See the documentation for the `select` parameter.
        :return: MsgVpnTransactionPublisherMsgsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'xid', 'count', 'cursor', 'where', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_msg_vpn_transaction_publisher_msgs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `get_msg_vpn_transaction_publisher_msgs`")  # noqa: E501
        # verify the required parameter 'xid' is set
        if ('xid' not in params or
                params['xid'] is None):
            raise ValueError("Missing the required parameter `xid` when calling `get_msg_vpn_transaction_publisher_msgs`")  # noqa: E501

        if 'count' in params and params['count'] < 1:  # noqa: E501
            raise ValueError("Invalid value for parameter `count` when calling `get_msg_vpn_transaction_publisher_msgs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'xid' in params:
            path_params['xid'] = params['xid']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/transactions/{xid}/publisherMsgs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MsgVpnTransactionPublisherMsgsResponse',  # noqa: E501
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
