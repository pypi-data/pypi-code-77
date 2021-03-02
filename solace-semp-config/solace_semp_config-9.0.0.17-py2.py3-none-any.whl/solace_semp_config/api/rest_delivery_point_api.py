# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see [note 1](#notes)) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+  broker. Resources are either individual **objects**, or **collections** of  objects. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Configuration|/SEMP/v2/config|Reading and writing config state|See [note 2](#notes)    Resources are always nouns, with individual objects being singular and  collections being plural. Objects within a collection are identified by an  `obj-id`, which follows the collection name with the form  `collection-name/obj-id`. Some examples:  <pre> /SEMP/v2/config/msgVpns                       ; MsgVpn collection /SEMP/v2/config/msgVpns/finance               ; MsgVpn object named \"finance\" /SEMP/v2/config/msgVpns/finance/queues        ; Queue collection within MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ ; Queue object named \"orderQ\" within MsgVpn \"finance\" </pre>  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and  are described by JSON arrays. Each item in the array represents an object in  the same manner as the individual object would normally be represented. The creation of a new object is done through its collection  resource.   ## Object Resources  Objects are composed of attributes and collections, and are described by JSON  content as name/value pairs. The collections of an object are not contained  directly in the object's JSON content, rather the content includes a URI  attribute which points to the collection. This contained collection resource  must be managed as a separate resource through this URI.  At a minimum, every object has 1 or more identifying attributes, and its own  `uri` attribute which contains the URI to itself. Attributes may have any  (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See [note 3](#notes) Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in  certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request     ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these  general principles:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see [note 4](#notes)) PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many  method/URI combinations. Individual URIs may document additional parameters.  Note that multiple query parameters can be used together in a single URI,  separated by the ampersand character. For example:  <pre> ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/config/msgVpns?q1=val1&q2=val2 </pre>  ### select  Include in the response only selected attributes of the object, or exclude  from the response selected attributes of the object. Use this query parameter  to limit the size of the returned data for each returned object, return only  those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the  list contains attribute names that are not prefaced by `-`, only those  attributes are included in the response. If the list contains attribute names  that are prefaced by `-`, those attributes are excluded from the response. If  the list contains both types, then the difference of the first set of  attributes and the second set of attributes is returned. If the list is  empty (i.e. `select=`), no attributes are returned  All attributes that are prefaced by `-` must follow all attributes that are  not prefaced by `-`. In addition, each attribute name in the list must match  at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute  names are supported using periods (e.g. `parentName.childName`).  Some examples:  <pre> ; List of all MsgVpn names /SEMP/v2/config/msgVpns?select=msgVpnName  ; List of all MsgVpn and their attributes except for their names /SEMP/v2/config/msgVpns?select=-msgVpnName  ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance?select=authentication*  ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/config/msgVpns/finance?select=-authentication*  ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/config/msgVpns/finance/queues/orderQ?select=owner,permission </pre>  ### where  Include in the response only objects where certain conditions are true. Use  this query parameter to limit which objects are returned to those whose  attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions  must be true for the object to be included in the response. Each expression  takes the form:  <pre> expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' </pre>  `value` may be a number, string, `true`, or `false`, as appropriate for the  type of `attribute-name`. Greater-than and less-than comparisons only work for  numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more  characters). Some examples:  <pre> ; Only enabled MsgVpns /SEMP/v2/config/msgVpns?where=enabled==true  ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/config/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap  ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/config/msgVpns?where=maxConnectionCount>100  ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/config/msgVpns?where=msgVpnName==B* </pre>  ### count  Limit the count of objects in the response. This can be useful to limit the  size of the response for large collections. The minimum value for `count` is  `1` and the default is `10`. There is a hidden maximum  as to prevent overloading the system. For example:  <pre> ; Up to 25 MsgVpns /SEMP/v2/config/msgVpns?count=25 </pre>  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data  that should not be created or interpreted by SEMP clients, and should only be  used as described below.  When a request is made for a collection and there may be additional objects  available for retrieval that are not included in the initial response, the  response will include a `cursorQuery` field containing a cursor. The value  of this field can be specified in the `cursor` query parameter of a  subsequent request to retrieve the next page of objects. For convenience,  an appropriate URI is constructed automatically by the broker and included  in the `nextPageUri` field of the response. This URI can be used directly  to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first. 5|For DELETE, the body of the request currently serves no purpose and will cause an error if not empty.      # noqa: E501

    OpenAPI spec version: 2.10
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from solace_semp_config.api_client import ApiClient


class RestDeliveryPointApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_msg_vpn_rest_delivery_point(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Creates a REST Delivery Point object.  # noqa: E501

        Creates a REST Delivery Point object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_rest_delivery_point_with_http_info(self, msg_vpn_name, body, **kwargs):  # noqa: E501
        """Creates a REST Delivery Point object.  # noqa: E501

        Creates a REST Delivery Point object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
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
                    " to method create_msg_vpn_rest_delivery_point" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_rest_delivery_point`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints', 'POST',
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

    def create_msg_vpn_rest_delivery_point_queue_binding(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Creates a Queue Binding object.  # noqa: E501

        Creates a Queue Binding object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| queueBindingName|x|x||| restDeliveryPointName|x||x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_rest_delivery_point_queue_binding_with_http_info(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Creates a Queue Binding object.  # noqa: E501

        Creates a Queue Binding object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| queueBindingName|x|x||| restDeliveryPointName|x||x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_rest_delivery_point_queue_binding" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `create_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings', 'POST',
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

    def create_msg_vpn_rest_delivery_point_rest_consumer(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Creates a REST Consumer object.  # noqa: E501

        Creates a REST Consumer object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent||||x| authenticationClientCertPassword||||x| authenticationHttpBasicPassword||||x| msgVpnName|x||x|| restConsumerName|x|x||| restDeliveryPointName|x||x||    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Creates a REST Consumer object.  # noqa: E501

        Creates a REST Consumer object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent||||x| authenticationClientCertPassword||||x| authenticationHttpBasicPassword||||x| msgVpnName|x||x|| restConsumerName|x|x||| restDeliveryPointName|x||x||    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_rest_delivery_point_rest_consumer" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `create_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers', 'POST',
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

    def create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Creates a Trusted Common Name object.  # noqa: E501

        Creates a Trusted Common Name object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| restConsumerName|x||x|| restDeliveryPointName|x||x|| tlsTrustedCommonName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonName body: The Trusted Common Name object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
            return data

    def create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Creates a Trusted Common Name object.  # noqa: E501

        Creates a Trusted Common Name object. Any attribute missing from the request will be set to its default value.   Attribute|Identifying|Required|Read-Only|Write-Only|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x||x|| restConsumerName|x||x|| restDeliveryPointName|x||x|| tlsTrustedCommonName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonName body: The Trusted Common Name object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerTlsTrustedCommonNameResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}/tlsTrustedCommonNames', 'POST',
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

    def delete_msg_vpn_rest_delivery_point(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Deletes a REST Delivery Point object.  # noqa: E501

        Deletes a REST Delivery Point object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_rest_delivery_point_with_http_info(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Deletes a REST Delivery Point object.  # noqa: E501

        Deletes a REST Delivery Point object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_rest_delivery_point" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `delete_msg_vpn_rest_delivery_point`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}', 'DELETE',
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

    def delete_msg_vpn_rest_delivery_point_queue_binding(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs):  # noqa: E501
        """Deletes a Queue Binding object.  # noqa: E501

        Deletes a Queue Binding object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_rest_delivery_point_queue_binding_with_http_info(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, **kwargs):  # noqa: E501
        """Deletes a Queue Binding object.  # noqa: E501

        Deletes a Queue Binding object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'queue_binding_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_rest_delivery_point_queue_binding" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `delete_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'queue_binding_name' is set
        if ('queue_binding_name' not in params or
                params['queue_binding_name'] is None):
            raise ValueError("Missing the required parameter `queue_binding_name` when calling `delete_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'msg_vpn_name' in params:
            path_params['msgVpnName'] = params['msg_vpn_name']  # noqa: E501
        if 'rest_delivery_point_name' in params:
            path_params['restDeliveryPointName'] = params['rest_delivery_point_name']  # noqa: E501
        if 'queue_binding_name' in params:
            path_params['queueBindingName'] = params['queue_binding_name']  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings/{queueBindingName}', 'DELETE',
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

    def delete_msg_vpn_rest_delivery_point_rest_consumer(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Deletes a REST Consumer object.  # noqa: E501

        Deletes a REST Consumer object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, **kwargs):  # noqa: E501
        """Deletes a REST Consumer object.  # noqa: E501

        Deletes a REST Consumer object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_rest_delivery_point_rest_consumer" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501

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
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}', 'DELETE',
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

    def delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Deletes a Trusted Common Name object.  # noqa: E501

        Deletes a Trusted Common Name object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs)  # noqa: E501
            return data

    def delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, **kwargs):  # noqa: E501
        """Deletes a Trusted Common Name object.  # noqa: E501

        Deletes a Trusted Common Name object.  A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :return: SempMetaOnlyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'tls_trusted_common_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501
        # verify the required parameter 'tls_trusted_common_name' is set
        if ('tls_trusted_common_name' not in params or
                params['tls_trusted_common_name'] is None):
            raise ValueError("Missing the required parameter `tls_trusted_common_name` when calling `delete_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}/tlsTrustedCommonNames/{tlsTrustedCommonName}', 'DELETE',
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

    def get_msg_vpn_rest_delivery_point(self, msg_vpn_name, rest_delivery_point_name, **kwargs):  # noqa: E501
        """Gets a REST Delivery Point object.  # noqa: E501

        Gets a REST Delivery Point object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a REST Delivery Point object.  # noqa: E501

        Gets a REST Delivery Point object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a Queue Binding object.  # noqa: E501

        Gets a Queue Binding object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| queueBindingName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a Queue Binding object.  # noqa: E501

        Gets a Queue Binding object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| queueBindingName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of Queue Binding objects.  # noqa: E501

        Gets a list of Queue Binding objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| queueBindingName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_bindings(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of Queue Binding objects.  # noqa: E501

        Gets a list of Queue Binding objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| queueBindingName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_queue_bindings_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a REST Consumer object.  # noqa: E501

        Gets a REST Consumer object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: authenticationClientCertContent||x| authenticationClientCertPassword||x| authenticationHttpBasicPassword||x| msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a REST Consumer object.  # noqa: E501

        Gets a REST Consumer object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: authenticationClientCertContent||x| authenticationClientCertPassword||x| authenticationHttpBasicPassword||x| msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a Trusted Common Name object.  # noqa: E501

        Gets a Trusted Common Name object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a Trusted Common Name object.  # noqa: E501

        Gets a Trusted Common Name object.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_name_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, tls_trusted_common_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param str tls_trusted_common_name: The tlsTrustedCommonName of the Trusted Common Name. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of Trusted Common Name objects.  # noqa: E501

        Gets a list of Trusted Common Name objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of Trusted Common Name objects.  # noqa: E501

        Gets a list of Trusted Common Name objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x|| tlsTrustedCommonName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumer_tls_trusted_common_names_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of REST Consumer objects.  # noqa: E501

        Gets a list of REST Consumer objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: authenticationClientCertContent||x| authenticationClientCertPassword||x| authenticationHttpBasicPassword||x| msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumers(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of REST Consumer objects.  # noqa: E501

        Gets a list of REST Consumer objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: authenticationClientCertContent||x| authenticationClientCertPassword||x| authenticationHttpBasicPassword||x| msgVpnName|x|| restConsumerName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_point_rest_consumers_with_http_info(msg_vpn_name, rest_delivery_point_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of REST Delivery Point objects.  # noqa: E501

        Gets a list of REST Delivery Point objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_points(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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
        """Gets a list of REST Delivery Point objects.  # noqa: E501

        Gets a list of REST Delivery Point objects.   Attribute|Identifying|Write-Only|Deprecated :---|:---:|:---:|:---: msgVpnName|x|| restDeliveryPointName|x||    A SEMP client authorized with a minimum access scope/level of \"vpn/readonly\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_msg_vpn_rest_delivery_points_with_http_info(msg_vpn_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param int count: Limit the count of objects in the response. See [Count](#count \"Description of the syntax of the `count` parameter\").
        :param str cursor: The cursor, or position, for the next page of objects. See [Cursor](#cursor \"Description of the syntax of the `cursor` parameter\").
        :param list[str] where: Include in the response only objects where certain conditions are true. See [Where](#where \"Description of the syntax of the `where` parameter\").
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
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

    def replace_msg_vpn_rest_delivery_point(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Replaces a REST Delivery Point object.  # noqa: E501

        Replaces a REST Delivery Point object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: clientProfileName||||x| msgVpnName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
            return data

    def replace_msg_vpn_rest_delivery_point_with_http_info(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Replaces a REST Delivery Point object.  # noqa: E501

        Replaces a REST Delivery Point object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: clientProfileName||||x| msgVpnName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_msg_vpn_rest_delivery_point" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `replace_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `replace_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_msg_vpn_rest_delivery_point`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}', 'PUT',
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

    def replace_msg_vpn_rest_delivery_point_queue_binding(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs):  # noqa: E501
        """Replaces a Queue Binding object.  # noqa: E501

        Replaces a Queue Binding object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x|x||| queueBindingName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs)  # noqa: E501
            return data

    def replace_msg_vpn_rest_delivery_point_queue_binding_with_http_info(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs):  # noqa: E501
        """Replaces a Queue Binding object.  # noqa: E501

        Replaces a Queue Binding object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x|x||| queueBindingName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'queue_binding_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_msg_vpn_rest_delivery_point_queue_binding" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `replace_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `replace_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'queue_binding_name' is set
        if ('queue_binding_name' not in params or
                params['queue_binding_name'] is None):
            raise ValueError("Missing the required parameter `queue_binding_name` when calling `replace_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings/{queueBindingName}', 'PUT',
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

    def replace_msg_vpn_rest_delivery_point_rest_consumer(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Replaces a REST Consumer object.  # noqa: E501

        Replaces a REST Consumer object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent|||x|x| authenticationClientCertPassword|||x|x| authenticationHttpBasicPassword|||x|x| authenticationHttpBasicUsername||||x| authenticationScheme||||x| msgVpnName|x|x||| outgoingConnectionCount||||x| remoteHost||||x| remotePort||||x| restConsumerName|x|x||| restDeliveryPointName|x|x||| tlsCipherSuiteList||||x| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.replace_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.replace_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
            return data

    def replace_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Replaces a REST Consumer object.  # noqa: E501

        Replaces a REST Consumer object. Any attribute missing from the request will be set to its default value, unless the user is not authorized to change its value in which case the missing attribute will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent|||x|x| authenticationClientCertPassword|||x|x| authenticationHttpBasicPassword|||x|x| authenticationHttpBasicUsername||||x| authenticationScheme||||x| msgVpnName|x|x||| outgoingConnectionCount||||x| remoteHost||||x| remotePort||||x| restConsumerName|x|x||| restDeliveryPointName|x|x||| tlsCipherSuiteList||||x| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.replace_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method replace_msg_vpn_rest_delivery_point_rest_consumer" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `replace_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `replace_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `replace_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `replace_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}', 'PUT',
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

    def update_msg_vpn_rest_delivery_point(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Updates a REST Delivery Point object.  # noqa: E501

        Updates a REST Delivery Point object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: clientProfileName||||x| msgVpnName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, **kwargs)  # noqa: E501
            return data

    def update_msg_vpn_rest_delivery_point_with_http_info(self, msg_vpn_name, rest_delivery_point_name, body, **kwargs):  # noqa: E501
        """Updates a REST Delivery Point object.  # noqa: E501

        Updates a REST Delivery Point object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: clientProfileName||||x| msgVpnName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point_with_http_info(msg_vpn_name, rest_delivery_point_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param MsgVpnRestDeliveryPoint body: The REST Delivery Point object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_msg_vpn_rest_delivery_point" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `update_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `update_msg_vpn_rest_delivery_point`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_msg_vpn_rest_delivery_point`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}', 'PATCH',
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

    def update_msg_vpn_rest_delivery_point_queue_binding(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs):  # noqa: E501
        """Updates a Queue Binding object.  # noqa: E501

        Updates a Queue Binding object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x|x||| queueBindingName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point_queue_binding(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs)  # noqa: E501
            return data

    def update_msg_vpn_rest_delivery_point_queue_binding_with_http_info(self, msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, **kwargs):  # noqa: E501
        """Updates a Queue Binding object.  # noqa: E501

        Updates a Queue Binding object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: msgVpnName|x|x||| queueBindingName|x|x||| restDeliveryPointName|x|x|||    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point_queue_binding_with_http_info(msg_vpn_name, rest_delivery_point_name, queue_binding_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str queue_binding_name: The queueBindingName of the Queue Binding. (required)
        :param MsgVpnRestDeliveryPointQueueBinding body: The Queue Binding object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointQueueBindingResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'queue_binding_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_msg_vpn_rest_delivery_point_queue_binding" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `update_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `update_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'queue_binding_name' is set
        if ('queue_binding_name' not in params or
                params['queue_binding_name'] is None):
            raise ValueError("Missing the required parameter `queue_binding_name` when calling `update_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_msg_vpn_rest_delivery_point_queue_binding`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings/{queueBindingName}', 'PATCH',
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

    def update_msg_vpn_rest_delivery_point_rest_consumer(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Updates a REST Consumer object.  # noqa: E501

        Updates a REST Consumer object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent|||x|x| authenticationClientCertPassword|||x|x| authenticationHttpBasicPassword|||x|x| authenticationHttpBasicUsername||||x| authenticationScheme||||x| msgVpnName|x|x||| outgoingConnectionCount||||x| remoteHost||||x| remotePort||||x| restConsumerName|x|x||| restDeliveryPointName|x|x||| tlsCipherSuiteList||||x| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point_rest_consumer(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs)  # noqa: E501
            return data

    def update_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(self, msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, **kwargs):  # noqa: E501
        """Updates a REST Consumer object.  # noqa: E501

        Updates a REST Consumer object. Any attribute missing from the request will be left unchanged.   Attribute|Identifying|Read-Only|Write-Only|Requires-Disable|Deprecated :---|:---:|:---:|:---:|:---:|:---: authenticationClientCertContent|||x|x| authenticationClientCertPassword|||x|x| authenticationHttpBasicPassword|||x|x| authenticationHttpBasicUsername||||x| authenticationScheme||||x| msgVpnName|x|x||| outgoingConnectionCount||||x| remoteHost||||x| remotePort||||x| restConsumerName|x|x||| restDeliveryPointName|x|x||| tlsCipherSuiteList||||x| tlsEnabled||||x|    The following attributes in the request may only be provided in certain combinations with other attributes:   Class|Attribute|Requires|Conflicts :---|:---|:---|:--- MsgVpnRestDeliveryPointRestConsumer|authenticationClientCertPassword|authenticationClientCertContent| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicPassword|authenticationHttpBasicUsername| MsgVpnRestDeliveryPointRestConsumer|authenticationHttpBasicUsername|authenticationHttpBasicPassword| MsgVpnRestDeliveryPointRestConsumer|remotePort|tlsEnabled| MsgVpnRestDeliveryPointRestConsumer|tlsEnabled|remotePort|    A SEMP client authorized with a minimum access scope/level of \"vpn/readwrite\" is required to perform this operation.  This has been available since 2.0.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_msg_vpn_rest_delivery_point_rest_consumer_with_http_info(msg_vpn_name, rest_delivery_point_name, rest_consumer_name, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str msg_vpn_name: The msgVpnName of the Message VPN. (required)
        :param str rest_delivery_point_name: The restDeliveryPointName of the REST Delivery Point. (required)
        :param str rest_consumer_name: The restConsumerName of the REST Consumer. (required)
        :param MsgVpnRestDeliveryPointRestConsumer body: The REST Consumer object's attributes. (required)
        :param list[str] select: Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. See [Select](#select \"Description of the syntax of the `select` parameter\").
        :return: MsgVpnRestDeliveryPointRestConsumerResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['msg_vpn_name', 'rest_delivery_point_name', 'rest_consumer_name', 'body', 'select']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_msg_vpn_rest_delivery_point_rest_consumer" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'msg_vpn_name' is set
        if ('msg_vpn_name' not in params or
                params['msg_vpn_name'] is None):
            raise ValueError("Missing the required parameter `msg_vpn_name` when calling `update_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_delivery_point_name' is set
        if ('rest_delivery_point_name' not in params or
                params['rest_delivery_point_name'] is None):
            raise ValueError("Missing the required parameter `rest_delivery_point_name` when calling `update_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'rest_consumer_name' is set
        if ('rest_consumer_name' not in params or
                params['rest_consumer_name'] is None):
            raise ValueError("Missing the required parameter `rest_consumer_name` when calling `update_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_msg_vpn_rest_delivery_point_rest_consumer`")  # noqa: E501

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
            '/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers/{restConsumerName}', 'PATCH',
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
