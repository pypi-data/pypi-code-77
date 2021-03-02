# coding: utf-8

"""
    SEMP (Solace Element Management Protocol)

    SEMP (starting in `v2`, see note 1) is a RESTful API for configuring, monitoring, and administering a Solace PubSub+ broker.  SEMP uses URIs to address manageable **resources** of the Solace PubSub+ broker. Resources are individual **objects**, **collections** of objects, or (exclusively in the action API) **actions**. This document applies to the following API:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Monitoring|/SEMP/v2/monitor|Querying operational parameters|See note 2    The following APIs are also available:   API|Base Path|Purpose|Comments :---|:---|:---|:--- Action|/SEMP/v2/action|Performing actions|See note 2 Configuration|/SEMP/v2/config|Reading and writing config state|See note 2    Resources are always nouns, with individual objects being singular and collections being plural.  Objects within a collection are identified by an `obj-id`, which follows the collection name with the form `collection-name/obj-id`.  Actions within an object are identified by an `action-id`, which follows the object name with the form `obj-id/action-id`.  Some examples:  ``` /SEMP/v2/config/msgVpns                        ; MsgVpn collection /SEMP/v2/config/msgVpns/a                      ; MsgVpn object named \"a\" /SEMP/v2/config/msgVpns/a/queues               ; Queue collection in MsgVpn \"a\" /SEMP/v2/config/msgVpns/a/queues/b             ; Queue object named \"b\" in MsgVpn \"a\" /SEMP/v2/action/msgVpns/a/queues/b/startReplay ; Action that starts a replay on Queue \"b\" in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients             ; Client collection in MsgVpn \"a\" /SEMP/v2/monitor/msgVpns/a/clients/c           ; Client object named \"c\" in MsgVpn \"a\" ```  ## Collection Resources  Collections are unordered lists of objects (unless described as otherwise), and are described by JSON arrays. Each item in the array represents an object in the same manner as the individual object would normally be represented. In the configuration API, the creation of a new object is done through its collection resource.  ## Object and Action Resources  Objects are composed of attributes, actions, collections, and other objects. They are described by JSON objects as name/value pairs. The collections and actions of an object are not contained directly in the object's JSON content; rather the content includes an attribute containing a URI which points to the collections and actions. These contained resources must be managed through this URI. At a minimum, every object has one or more identifying attributes, and its own `uri` attribute which contains the URI pointing to itself.  Actions are also composed of attributes, and are described by JSON objects as name/value pairs. Unlike objects, however, they are not members of a collection and cannot be retrieved, only performed. Actions only exist in the action API.  Attributes in an object or action may have any (non-exclusively) of the following properties:   Property|Meaning|Comments :---|:---|:--- Identifying|Attribute is involved in unique identification of the object, and appears in its URI| Required|Attribute must be provided in the request| Read-Only|Attribute can only be read, not written|See note 3 Write-Only|Attribute can only be written, not read| Requires-Disable|Attribute can only be changed when object is disabled| Deprecated|Attribute is deprecated, and will disappear in the next SEMP version|    In some requests, certain attributes may only be provided in certain combinations with other attributes:   Relationship|Meaning :---|:--- Requires|Attribute may only be changed by a request if a particular attribute or combination of attributes is also provided in the request Conflicts|Attribute may only be provided in a request if a particular attribute or combination of attributes is not also provided in the request    ## HTTP Methods  The following HTTP methods manipulate resources in accordance with these general principles. Note that some methods are only used in certain APIs:   Method|Resource|Meaning|Request Body|Response Body|Missing Request Attributes :---|:---|:---|:---|:---|:--- POST|Collection|Create object|Initial attribute values|Object attributes and metadata|Set to default PUT|Object|Create or replace object|New attribute values|Object attributes and metadata|Set to default (but see note 4) PUT|Action|Performs action|Action arguments|Action metadata|N/A PATCH|Object|Update object|New attribute values|Object attributes and metadata|unchanged DELETE|Object|Delete object|Empty|Object metadata|N/A GET|Object|Get object|Empty|Object attributes and metadata|N/A GET|Collection|Get collection|Empty|Object attributes and collection metadata|N/A    ## Common Query Parameters  The following are some common query parameters that are supported by many method/URI combinations. Individual URIs may document additional parameters. Note that multiple query parameters can be used together in a single URI, separated by the ampersand character. For example:  ``` ; Request for the MsgVpns collection using two hypothetical query parameters ; \"q1\" and \"q2\" with values \"val1\" and \"val2\" respectively /SEMP/v2/monitor/msgVpns?q1=val1&q2=val2 ```  ### select  Include in the response only selected attributes of the object, or exclude from the response selected attributes of the object. Use this query parameter to limit the size of the returned data for each returned object, return only those fields that are desired, or exclude fields that are not desired.  The value of `select` is a comma-separated list of attribute names. If the list contains attribute names that are not prefaced by `-`, only those attributes are included in the response. If the list contains attribute names that are prefaced by `-`, those attributes are excluded from the response. If the list contains both types, then the difference of the first set of attributes and the second set of attributes is returned. If the list is empty (i.e. `select=`), no attributes are returned.  All attributes that are prefaced by `-` must follow all attributes that are not prefaced by `-`. In addition, each attribute name in the list must match at least one attribute in the object.  Names may include the `*` wildcard (zero or more characters). Nested attribute names are supported using periods (e.g. `parentName.childName`).  Some examples:  ``` ; List of all MsgVpn names /SEMP/v2/monitor/msgVpns?select=msgVpnName ; List of all MsgVpn and their attributes except for their names /SEMP/v2/monitor/msgVpns?select=-msgVpnName ; Authentication attributes of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance?select=authentication* ; All attributes of MsgVpn \"finance\" except for authentication attributes /SEMP/v2/monitor/msgVpns/finance?select=-authentication* ; Access related attributes of Queue \"orderQ\" of MsgVpn \"finance\" /SEMP/v2/monitor/msgVpns/finance/queues/orderQ?select=owner,permission ```  ### where  Include in the response only objects where certain conditions are true. Use this query parameter to limit which objects are returned to those whose attribute values meet the given conditions.  The value of `where` is a comma-separated list of expressions. All expressions must be true for the object to be included in the response. Each expression takes the form:  ``` expression  = attribute-name OP value OP          = '==' | '!=' | '&lt;' | '&gt;' | '&lt;=' | '&gt;=' ```  `value` may be a number, string, `true`, or `false`, as appropriate for the type of `attribute-name`. Greater-than and less-than comparisons only work for numbers. A `*` in a string `value` is interpreted as a wildcard (zero or more characters). Some examples:  ``` ; Only enabled MsgVpns /SEMP/v2/monitor/msgVpns?where=enabled==true ; Only MsgVpns using basic non-LDAP authentication /SEMP/v2/monitor/msgVpns?where=authenticationBasicEnabled==true,authenticationBasicType!=ldap ; Only MsgVpns that allow more than 100 client connections /SEMP/v2/monitor/msgVpns?where=maxConnectionCount>100 ; Only MsgVpns with msgVpnName starting with \"B\": /SEMP/v2/monitor/msgVpns?where=msgVpnName==B* ```  ### count  Limit the count of objects in the response. This can be useful to limit the size of the response for large collections. The minimum value for `count` is `1` and the default is `10`. There is also a per-collection maximum value to limit request handling time. For example:  ``` ; Up to 25 MsgVpns /SEMP/v2/monitor/msgVpns?count=25 ```  ### cursor  The cursor, or position, for the next page of objects. Cursors are opaque data that should not be created or interpreted by SEMP clients, and should only be used as described below.  When a request is made for a collection and there may be additional objects available for retrieval that are not included in the initial response, the response will include a `cursorQuery` field containing a cursor. The value of this field can be specified in the `cursor` query parameter of a subsequent request to retrieve the next page of objects. For convenience, an appropriate URI is constructed automatically by the broker and included in the `nextPageUri` field of the response. This URI can be used directly to retrieve the next page of objects.  ## Notes  Note|Description :---:|:--- 1|This specification defines SEMP starting in \"v2\", and not the original SEMP \"v1\" interface. Request and response formats between \"v1\" and \"v2\" are entirely incompatible, although both protocols share a common port configuration on the Solace PubSub+ broker. They are differentiated by the initial portion of the URI path, one of either \"/SEMP/\" or \"/SEMP/v2/\" 2|This API is partially implemented. Only a subset of all objects are available. 3|Read-only attributes may appear in POST and PUT/PATCH requests. However, if a read-only attribute is not marked as identifying, it will be ignored during a PUT/PATCH. 4|For PUT, if the SEMP user is not authorized to modify the attribute, its value is left unchanged rather than set to default. In addition, the values of write-only attributes are not set to their defaults on a PUT. If the object does not exist, it is created first.    # noqa: E501

    OpenAPI spec version: 2.16
    Contact: support@solace.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class CertAuthority(object):
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
        'cert_authority_name': 'str',
        'crl_day_list': 'str',
        'crl_last_download_time': 'int',
        'crl_last_failure_reason': 'str',
        'crl_last_failure_time': 'int',
        'crl_next_download_time': 'int',
        'crl_time_list': 'str',
        'crl_up': 'bool',
        'crl_url': 'str',
        'ocsp_last_failure_reason': 'str',
        'ocsp_last_failure_time': 'int',
        'ocsp_last_failure_url': 'str',
        'ocsp_non_responder_cert_enabled': 'bool',
        'ocsp_override_url': 'str',
        'ocsp_timeout': 'int',
        'revocation_check_enabled': 'bool'
    }

    attribute_map = {
        'cert_authority_name': 'certAuthorityName',
        'crl_day_list': 'crlDayList',
        'crl_last_download_time': 'crlLastDownloadTime',
        'crl_last_failure_reason': 'crlLastFailureReason',
        'crl_last_failure_time': 'crlLastFailureTime',
        'crl_next_download_time': 'crlNextDownloadTime',
        'crl_time_list': 'crlTimeList',
        'crl_up': 'crlUp',
        'crl_url': 'crlUrl',
        'ocsp_last_failure_reason': 'ocspLastFailureReason',
        'ocsp_last_failure_time': 'ocspLastFailureTime',
        'ocsp_last_failure_url': 'ocspLastFailureUrl',
        'ocsp_non_responder_cert_enabled': 'ocspNonResponderCertEnabled',
        'ocsp_override_url': 'ocspOverrideUrl',
        'ocsp_timeout': 'ocspTimeout',
        'revocation_check_enabled': 'revocationCheckEnabled'
    }

    def __init__(self, cert_authority_name=None, crl_day_list=None, crl_last_download_time=None, crl_last_failure_reason=None, crl_last_failure_time=None, crl_next_download_time=None, crl_time_list=None, crl_up=None, crl_url=None, ocsp_last_failure_reason=None, ocsp_last_failure_time=None, ocsp_last_failure_url=None, ocsp_non_responder_cert_enabled=None, ocsp_override_url=None, ocsp_timeout=None, revocation_check_enabled=None):  # noqa: E501
        """CertAuthority - a model defined in Swagger"""  # noqa: E501

        self._cert_authority_name = None
        self._crl_day_list = None
        self._crl_last_download_time = None
        self._crl_last_failure_reason = None
        self._crl_last_failure_time = None
        self._crl_next_download_time = None
        self._crl_time_list = None
        self._crl_up = None
        self._crl_url = None
        self._ocsp_last_failure_reason = None
        self._ocsp_last_failure_time = None
        self._ocsp_last_failure_url = None
        self._ocsp_non_responder_cert_enabled = None
        self._ocsp_override_url = None
        self._ocsp_timeout = None
        self._revocation_check_enabled = None
        self.discriminator = None

        if cert_authority_name is not None:
            self.cert_authority_name = cert_authority_name
        if crl_day_list is not None:
            self.crl_day_list = crl_day_list
        if crl_last_download_time is not None:
            self.crl_last_download_time = crl_last_download_time
        if crl_last_failure_reason is not None:
            self.crl_last_failure_reason = crl_last_failure_reason
        if crl_last_failure_time is not None:
            self.crl_last_failure_time = crl_last_failure_time
        if crl_next_download_time is not None:
            self.crl_next_download_time = crl_next_download_time
        if crl_time_list is not None:
            self.crl_time_list = crl_time_list
        if crl_up is not None:
            self.crl_up = crl_up
        if crl_url is not None:
            self.crl_url = crl_url
        if ocsp_last_failure_reason is not None:
            self.ocsp_last_failure_reason = ocsp_last_failure_reason
        if ocsp_last_failure_time is not None:
            self.ocsp_last_failure_time = ocsp_last_failure_time
        if ocsp_last_failure_url is not None:
            self.ocsp_last_failure_url = ocsp_last_failure_url
        if ocsp_non_responder_cert_enabled is not None:
            self.ocsp_non_responder_cert_enabled = ocsp_non_responder_cert_enabled
        if ocsp_override_url is not None:
            self.ocsp_override_url = ocsp_override_url
        if ocsp_timeout is not None:
            self.ocsp_timeout = ocsp_timeout
        if revocation_check_enabled is not None:
            self.revocation_check_enabled = revocation_check_enabled

    @property
    def cert_authority_name(self):
        """Gets the cert_authority_name of this CertAuthority.  # noqa: E501

        The name of the Certificate Authority.  # noqa: E501

        :return: The cert_authority_name of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._cert_authority_name

    @cert_authority_name.setter
    def cert_authority_name(self, cert_authority_name):
        """Sets the cert_authority_name of this CertAuthority.

        The name of the Certificate Authority.  # noqa: E501

        :param cert_authority_name: The cert_authority_name of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._cert_authority_name = cert_authority_name

    @property
    def crl_day_list(self):
        """Gets the crl_day_list of this CertAuthority.  # noqa: E501

        The scheduled CRL refresh day(s), specified as \"daily\" or a comma-separated list of days. Days must be specified as \"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", or \"Sat\", with no spaces, and in sorted order from Sunday to Saturday.  # noqa: E501

        :return: The crl_day_list of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._crl_day_list

    @crl_day_list.setter
    def crl_day_list(self, crl_day_list):
        """Sets the crl_day_list of this CertAuthority.

        The scheduled CRL refresh day(s), specified as \"daily\" or a comma-separated list of days. Days must be specified as \"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", or \"Sat\", with no spaces, and in sorted order from Sunday to Saturday.  # noqa: E501

        :param crl_day_list: The crl_day_list of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._crl_day_list = crl_day_list

    @property
    def crl_last_download_time(self):
        """Gets the crl_last_download_time of this CertAuthority.  # noqa: E501

        The timestamp of the last successful CRL download. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The crl_last_download_time of this CertAuthority.  # noqa: E501
        :rtype: int
        """
        return self._crl_last_download_time

    @crl_last_download_time.setter
    def crl_last_download_time(self, crl_last_download_time):
        """Sets the crl_last_download_time of this CertAuthority.

        The timestamp of the last successful CRL download. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param crl_last_download_time: The crl_last_download_time of this CertAuthority.  # noqa: E501
        :type: int
        """

        self._crl_last_download_time = crl_last_download_time

    @property
    def crl_last_failure_reason(self):
        """Gets the crl_last_failure_reason of this CertAuthority.  # noqa: E501

        The reason for the last CRL failure.  # noqa: E501

        :return: The crl_last_failure_reason of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._crl_last_failure_reason

    @crl_last_failure_reason.setter
    def crl_last_failure_reason(self, crl_last_failure_reason):
        """Sets the crl_last_failure_reason of this CertAuthority.

        The reason for the last CRL failure.  # noqa: E501

        :param crl_last_failure_reason: The crl_last_failure_reason of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._crl_last_failure_reason = crl_last_failure_reason

    @property
    def crl_last_failure_time(self):
        """Gets the crl_last_failure_time of this CertAuthority.  # noqa: E501

        The timestamp of the last CRL failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The crl_last_failure_time of this CertAuthority.  # noqa: E501
        :rtype: int
        """
        return self._crl_last_failure_time

    @crl_last_failure_time.setter
    def crl_last_failure_time(self, crl_last_failure_time):
        """Sets the crl_last_failure_time of this CertAuthority.

        The timestamp of the last CRL failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param crl_last_failure_time: The crl_last_failure_time of this CertAuthority.  # noqa: E501
        :type: int
        """

        self._crl_last_failure_time = crl_last_failure_time

    @property
    def crl_next_download_time(self):
        """Gets the crl_next_download_time of this CertAuthority.  # noqa: E501

        The scheduled time of the next CRL download. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The crl_next_download_time of this CertAuthority.  # noqa: E501
        :rtype: int
        """
        return self._crl_next_download_time

    @crl_next_download_time.setter
    def crl_next_download_time(self, crl_next_download_time):
        """Sets the crl_next_download_time of this CertAuthority.

        The scheduled time of the next CRL download. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param crl_next_download_time: The crl_next_download_time of this CertAuthority.  # noqa: E501
        :type: int
        """

        self._crl_next_download_time = crl_next_download_time

    @property
    def crl_time_list(self):
        """Gets the crl_time_list of this CertAuthority.  # noqa: E501

        The scheduled CRL refresh time(s), specified as \"hourly\" or a comma-separated list of 24-hour times in the form hh:mm, or h:mm. There must be no spaces, and times must be in sorted order from 0:00 to 23:59.  # noqa: E501

        :return: The crl_time_list of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._crl_time_list

    @crl_time_list.setter
    def crl_time_list(self, crl_time_list):
        """Sets the crl_time_list of this CertAuthority.

        The scheduled CRL refresh time(s), specified as \"hourly\" or a comma-separated list of 24-hour times in the form hh:mm, or h:mm. There must be no spaces, and times must be in sorted order from 0:00 to 23:59.  # noqa: E501

        :param crl_time_list: The crl_time_list of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._crl_time_list = crl_time_list

    @property
    def crl_up(self):
        """Gets the crl_up of this CertAuthority.  # noqa: E501

        Indicates whether CRL revocation checking is operationally up.  # noqa: E501

        :return: The crl_up of this CertAuthority.  # noqa: E501
        :rtype: bool
        """
        return self._crl_up

    @crl_up.setter
    def crl_up(self, crl_up):
        """Sets the crl_up of this CertAuthority.

        Indicates whether CRL revocation checking is operationally up.  # noqa: E501

        :param crl_up: The crl_up of this CertAuthority.  # noqa: E501
        :type: bool
        """

        self._crl_up = crl_up

    @property
    def crl_url(self):
        """Gets the crl_url of this CertAuthority.  # noqa: E501

        The URL for the CRL source. This is a required attribute for CRL to be operational and the URL must be complete with http:// included.  # noqa: E501

        :return: The crl_url of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._crl_url

    @crl_url.setter
    def crl_url(self, crl_url):
        """Sets the crl_url of this CertAuthority.

        The URL for the CRL source. This is a required attribute for CRL to be operational and the URL must be complete with http:// included.  # noqa: E501

        :param crl_url: The crl_url of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._crl_url = crl_url

    @property
    def ocsp_last_failure_reason(self):
        """Gets the ocsp_last_failure_reason of this CertAuthority.  # noqa: E501

        The reason for the last OCSP failure.  # noqa: E501

        :return: The ocsp_last_failure_reason of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._ocsp_last_failure_reason

    @ocsp_last_failure_reason.setter
    def ocsp_last_failure_reason(self, ocsp_last_failure_reason):
        """Sets the ocsp_last_failure_reason of this CertAuthority.

        The reason for the last OCSP failure.  # noqa: E501

        :param ocsp_last_failure_reason: The ocsp_last_failure_reason of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._ocsp_last_failure_reason = ocsp_last_failure_reason

    @property
    def ocsp_last_failure_time(self):
        """Gets the ocsp_last_failure_time of this CertAuthority.  # noqa: E501

        The timestamp of the last OCSP failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :return: The ocsp_last_failure_time of this CertAuthority.  # noqa: E501
        :rtype: int
        """
        return self._ocsp_last_failure_time

    @ocsp_last_failure_time.setter
    def ocsp_last_failure_time(self, ocsp_last_failure_time):
        """Sets the ocsp_last_failure_time of this CertAuthority.

        The timestamp of the last OCSP failure. This value represents the number of seconds since 1970-01-01 00:00:00 UTC (Unix time).  # noqa: E501

        :param ocsp_last_failure_time: The ocsp_last_failure_time of this CertAuthority.  # noqa: E501
        :type: int
        """

        self._ocsp_last_failure_time = ocsp_last_failure_time

    @property
    def ocsp_last_failure_url(self):
        """Gets the ocsp_last_failure_url of this CertAuthority.  # noqa: E501

        The URL involved in the last OCSP failure.  # noqa: E501

        :return: The ocsp_last_failure_url of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._ocsp_last_failure_url

    @ocsp_last_failure_url.setter
    def ocsp_last_failure_url(self, ocsp_last_failure_url):
        """Sets the ocsp_last_failure_url of this CertAuthority.

        The URL involved in the last OCSP failure.  # noqa: E501

        :param ocsp_last_failure_url: The ocsp_last_failure_url of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._ocsp_last_failure_url = ocsp_last_failure_url

    @property
    def ocsp_non_responder_cert_enabled(self):
        """Gets the ocsp_non_responder_cert_enabled of this CertAuthority.  # noqa: E501

        Indicates whether a non-responder certificate is allowed to sign an OCSP response. Typically used with an OCSP override URL in cases where a single certificate is used to sign client certificates and OCSP responses.  # noqa: E501

        :return: The ocsp_non_responder_cert_enabled of this CertAuthority.  # noqa: E501
        :rtype: bool
        """
        return self._ocsp_non_responder_cert_enabled

    @ocsp_non_responder_cert_enabled.setter
    def ocsp_non_responder_cert_enabled(self, ocsp_non_responder_cert_enabled):
        """Sets the ocsp_non_responder_cert_enabled of this CertAuthority.

        Indicates whether a non-responder certificate is allowed to sign an OCSP response. Typically used with an OCSP override URL in cases where a single certificate is used to sign client certificates and OCSP responses.  # noqa: E501

        :param ocsp_non_responder_cert_enabled: The ocsp_non_responder_cert_enabled of this CertAuthority.  # noqa: E501
        :type: bool
        """

        self._ocsp_non_responder_cert_enabled = ocsp_non_responder_cert_enabled

    @property
    def ocsp_override_url(self):
        """Gets the ocsp_override_url of this CertAuthority.  # noqa: E501

        The OCSP responder URL to use for overriding the one supplied in the client certificate. The URL must be complete with http:// included.  # noqa: E501

        :return: The ocsp_override_url of this CertAuthority.  # noqa: E501
        :rtype: str
        """
        return self._ocsp_override_url

    @ocsp_override_url.setter
    def ocsp_override_url(self, ocsp_override_url):
        """Sets the ocsp_override_url of this CertAuthority.

        The OCSP responder URL to use for overriding the one supplied in the client certificate. The URL must be complete with http:// included.  # noqa: E501

        :param ocsp_override_url: The ocsp_override_url of this CertAuthority.  # noqa: E501
        :type: str
        """

        self._ocsp_override_url = ocsp_override_url

    @property
    def ocsp_timeout(self):
        """Gets the ocsp_timeout of this CertAuthority.  # noqa: E501

        The timeout in seconds to receive a response from the OCSP responder after sending a request or making the initial connection attempt.  # noqa: E501

        :return: The ocsp_timeout of this CertAuthority.  # noqa: E501
        :rtype: int
        """
        return self._ocsp_timeout

    @ocsp_timeout.setter
    def ocsp_timeout(self, ocsp_timeout):
        """Sets the ocsp_timeout of this CertAuthority.

        The timeout in seconds to receive a response from the OCSP responder after sending a request or making the initial connection attempt.  # noqa: E501

        :param ocsp_timeout: The ocsp_timeout of this CertAuthority.  # noqa: E501
        :type: int
        """

        self._ocsp_timeout = ocsp_timeout

    @property
    def revocation_check_enabled(self):
        """Gets the revocation_check_enabled of this CertAuthority.  # noqa: E501

        Indicates whether Certificate Authority revocation checking is enabled.  # noqa: E501

        :return: The revocation_check_enabled of this CertAuthority.  # noqa: E501
        :rtype: bool
        """
        return self._revocation_check_enabled

    @revocation_check_enabled.setter
    def revocation_check_enabled(self, revocation_check_enabled):
        """Sets the revocation_check_enabled of this CertAuthority.

        Indicates whether Certificate Authority revocation checking is enabled.  # noqa: E501

        :param revocation_check_enabled: The revocation_check_enabled of this CertAuthority.  # noqa: E501
        :type: bool
        """

        self._revocation_check_enabled = revocation_check_enabled

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
        if issubclass(CertAuthority, dict):
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
        if not isinstance(other, CertAuthority):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
