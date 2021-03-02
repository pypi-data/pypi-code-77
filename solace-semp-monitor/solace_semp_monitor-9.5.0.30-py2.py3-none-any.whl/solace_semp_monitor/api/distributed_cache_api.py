# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.16
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from solace_semp_monitor.api_client import ApiClient


class DistributedCacheApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_msg_vpn_distributed_cache(self, msg_vpn_name, cache_name, **kwargs):  # noqa: E501
        """Get a Distributed Cache object.  # noqa: E501

        Get a Distributed Cache object.  A Distributed Cache is a collection of one or more Cache Clusters that belong to the same Message VPN. Each Cache Cluster in a Distributed Cache is configured to subscribe to a different set of topics. This effectively divides up the configured topic space, to provide scaling to very large topic spaces or very high cached message throughput.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Distributed Cache object.  A Distributed Cache is a collection of one or more Cache Clusters that belong to the same Message VPN. Each Cache Cluster in a Distributed Cache is configured to subscribe to a different set of topics. This effectively divides up the configured topic space, to provide scaling to very large topic spaces or very high cached message throughput.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Cache Cluster object.  A Cache Cluster is a collection of one or more Cache Instances that subscribe to exactly the same topics. Cache Instances are grouped together in a Cache Cluster for the purpose of fault tolerance and load balancing. As published messages are received, the message broker message bus sends these live data messages to the Cache Instances in the Cache Cluster. This enables client cache requests to be served by any of Cache Instances in the Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Cache Cluster object.  A Cache Cluster is a collection of one or more Cache Instances that subscribe to exactly the same topics. Cache Instances are grouped together in a Cache Cluster for the purpose of fault tolerance and load balancing. As published messages are received, the message broker message bus sends these live data messages to the Cache Instances in the Cache Cluster. This enables client cache requests to be served by any of Cache Instances in the Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Home Cache Cluster object.  A Home Cache Cluster is a Cache Cluster that is the \"definitive\" Cache Cluster for a given topic in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Home Cache Cluster object.  A Home Cache Cluster is a Cache Cluster that is the \"definitive\" Cache Cluster for a given topic in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Topic Prefix object.  A Topic Prefix is a prefix for a global topic that is available from the containing Home Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Topic Prefix object.  A Topic Prefix is a prefix for a global topic that is available from the containing Home Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Topic Prefix objects.  A Topic Prefix is a prefix for a global topic that is available from the containing Home Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Topic Prefix objects.  A Topic Prefix is a prefix for a global topic that is available from the containing Home Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x| topicPrefix|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Home Cache Cluster objects.  A Home Cache Cluster is a Cache Cluster that is the \"definitive\" Cache Cluster for a given topic in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Home Cache Cluster objects.  A Home Cache Cluster is a Cache Cluster that is the \"definitive\" Cache Cluster for a given topic in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Cache Instance object.  A Cache Instance is a single Cache process that belongs to a single Cache Cluster. A Cache Instance object provisioned on the broker is used to disseminate configuration information to the Cache process. Cache Instances listen for and cache live data messages that match the topic subscriptions configured for their parent Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| counter.msgCount||x counter.msgPeakCount||x counter.requestQueueDepthCount||x counter.requestQueueDepthPeakCount||x counter.topicCount||x counter.topicPeakCount||x instanceName|x| msgVpnName|x| rate.averageDataRxBytePeakRate||x rate.averageDataRxByteRate||x rate.averageDataRxMsgPeakRate||x rate.averageDataRxMsgRate||x rate.averageDataTxMsgPeakRate||x rate.averageDataTxMsgRate||x rate.averageRequestRxPeakRate||x rate.averageRequestRxRate||x rate.dataRxBytePeakRate||x rate.dataRxByteRate||x rate.dataRxMsgPeakRate||x rate.dataRxMsgRate||x rate.dataTxMsgPeakRate||x rate.dataTxMsgRate||x rate.requestRxPeakRate||x rate.requestRxRate||x    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Cache Instance object.  A Cache Instance is a single Cache process that belongs to a single Cache Cluster. A Cache Instance object provisioned on the broker is used to disseminate configuration information to the Cache process. Cache Instances listen for and cache live data messages that match the topic subscriptions configured for their parent Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| counter.msgCount||x counter.msgPeakCount||x counter.requestQueueDepthCount||x counter.requestQueueDepthPeakCount||x counter.topicCount||x counter.topicPeakCount||x instanceName|x| msgVpnName|x| rate.averageDataRxBytePeakRate||x rate.averageDataRxByteRate||x rate.averageDataRxMsgPeakRate||x rate.averageDataRxMsgRate||x rate.averageDataTxMsgPeakRate||x rate.averageDataTxMsgRate||x rate.averageRequestRxPeakRate||x rate.averageRequestRxRate||x rate.dataRxBytePeakRate||x rate.dataRxByteRate||x rate.dataRxMsgPeakRate||x rate.dataRxMsgRate||x rate.dataTxMsgPeakRate||x rate.dataTxMsgRate||x rate.requestRxPeakRate||x rate.requestRxRate||x    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Remote Home Cache Cluster object.  A Remote Home Cache Cluster is a Home Cache Cluster that the Cache Instance is communicating with in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Remote Home Cache Cluster object.  A Remote Home Cache Cluster is a Home Cache Cluster that the Cache Instance is communicating with in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Remote Home Cache Cluster objects.  A Remote Home Cache Cluster is a Home Cache Cluster that the Cache Instance is communicating with in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Remote Home Cache Cluster objects.  A Remote Home Cache Cluster is a Home Cache Cluster that the Cache Instance is communicating with in the context of the Global Caching feature.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| homeClusterName|x| instanceName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Remote Topic object.  A Remote Topic is a topic for which the Cache Instance has cached messages.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Remote Topic object.  A Remote Topic is a topic for which the Cache Instance has cached messages.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Remote Topic objects.  A Remote Topic is a topic for which the Cache Instance has cached messages.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Remote Topic objects.  A Remote Topic is a topic for which the Cache Instance has cached messages.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| instanceName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Cache Instance objects.  A Cache Instance is a single Cache process that belongs to a single Cache Cluster. A Cache Instance object provisioned on the broker is used to disseminate configuration information to the Cache process. Cache Instances listen for and cache live data messages that match the topic subscriptions configured for their parent Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| counter.msgCount||x counter.msgPeakCount||x counter.requestQueueDepthCount||x counter.requestQueueDepthPeakCount||x counter.topicCount||x counter.topicPeakCount||x instanceName|x| msgVpnName|x| rate.averageDataRxBytePeakRate||x rate.averageDataRxByteRate||x rate.averageDataRxMsgPeakRate||x rate.averageDataRxMsgRate||x rate.averageDataTxMsgPeakRate||x rate.averageDataTxMsgRate||x rate.averageRequestRxPeakRate||x rate.averageRequestRxRate||x rate.dataRxBytePeakRate||x rate.dataRxByteRate||x rate.dataRxMsgPeakRate||x rate.dataRxMsgRate||x rate.dataTxMsgPeakRate||x rate.dataTxMsgRate||x rate.requestRxPeakRate||x rate.requestRxRate||x    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Cache Instance objects.  A Cache Instance is a single Cache process that belongs to a single Cache Cluster. A Cache Instance object provisioned on the broker is used to disseminate configuration information to the Cache process. Cache Instances listen for and cache live data messages that match the topic subscriptions configured for their parent Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| counter.msgCount||x counter.msgPeakCount||x counter.requestQueueDepthCount||x counter.requestQueueDepthPeakCount||x counter.topicCount||x counter.topicPeakCount||x instanceName|x| msgVpnName|x| rate.averageDataRxBytePeakRate||x rate.averageDataRxByteRate||x rate.averageDataRxMsgPeakRate||x rate.averageDataRxMsgRate||x rate.averageDataTxMsgPeakRate||x rate.averageDataTxMsgRate||x rate.averageRequestRxPeakRate||x rate.averageRequestRxRate||x rate.dataRxBytePeakRate||x rate.dataRxByteRate||x rate.dataRxMsgPeakRate||x rate.dataRxMsgRate||x rate.dataTxMsgPeakRate||x rate.dataTxMsgRate||x rate.requestRxPeakRate||x rate.requestRxRate||x    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Topic object.  The Cache Instances that belong to the containing Cache Cluster will cache any messages published to topics that match a Topic Subscription.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a Topic object.  The Cache Instances that belong to the containing Cache Cluster will cache any messages published to topics that match a Topic Subscription.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Topic objects.  The Cache Instances that belong to the containing Cache Cluster will cache any messages published to topics that match a Topic Subscription.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Topic objects.  The Cache Instances that belong to the containing Cache Cluster will cache any messages published to topics that match a Topic Subscription.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x| topic|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Cache Cluster objects.  A Cache Cluster is a collection of one or more Cache Instances that subscribe to exactly the same topics. Cache Instances are grouped together in a Cache Cluster for the purpose of fault tolerance and load balancing. As published messages are received, the message broker message bus sends these live data messages to the Cache Instances in the Cache Cluster. This enables client cache requests to be served by any of Cache Instances in the Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Cache Cluster objects.  A Cache Cluster is a collection of one or more Cache Instances that subscribe to exactly the same topics. Cache Instances are grouped together in a Cache Cluster for the purpose of fault tolerance and load balancing. As published messages are received, the message broker message bus sends these live data messages to the Cache Instances in the Cache Cluster. This enables client cache requests to be served by any of Cache Instances in the Cache Cluster.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| clusterName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Distributed Cache objects.  A Distributed Cache is a collection of one or more Cache Clusters that belong to the same Message VPN. Each Cache Cluster in a Distributed Cache is configured to subscribe to a different set of topics. This effectively divides up the configured topic space, to provide scaling to very large topic spaces or very high cached message throughput.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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

        Get a list of Distributed Cache objects.  A Distributed Cache is a collection of one or more Cache Clusters that belong to the same Message VPN. Each Cache Cluster in a Distributed Cache is configured to subscribe to a different set of topics. This effectively divides up the configured topic space, to provide scaling to very large topic spaces or very high cached message throughput.   Attribute|Identifying|Deprecated :---|:---:|:---: cacheName|x| msgVpnName|x|    A SEMP client authorized with a minimum access scope/level of \"vpn/read-only\" is required to perform this operation.  This has been available since 2.11.  # noqa: E501
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
