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


class MsgVpnClientTransactedSession(object):
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
        'client_name': 'str',
        'commit_count': 'int',
        'commit_failure_count': 'int',
        'commit_success_count': 'int',
        'consumed_msg_count': 'int',
        'end_fail_failure_count': 'int',
        'end_fail_success_count': 'int',
        'end_failure_count': 'int',
        'end_rollback_failure_count': 'int',
        'end_rollback_success_count': 'int',
        'end_success_count': 'int',
        'failure_count': 'int',
        'forget_failure_count': 'int',
        'forget_success_count': 'int',
        'msg_vpn_name': 'str',
        'one_phase_commit_failure_count': 'int',
        'one_phase_commit_success_count': 'int',
        'pending_consumed_msg_count': 'int',
        'pending_published_msg_count': 'int',
        'prepare_failure_count': 'int',
        'prepare_success_count': 'int',
        'previous_transaction_state': 'str',
        'published_msg_count': 'int',
        'resume_failure_count': 'int',
        'resume_success_count': 'int',
        'retrieved_msg_count': 'int',
        'rollback_count': 'int',
        'rollback_failure_count': 'int',
        'rollback_success_count': 'int',
        'session_name': 'str',
        'spooled_msg_count': 'int',
        'start_failure_count': 'int',
        'start_success_count': 'int',
        'success_count': 'int',
        'suspend_failure_count': 'int',
        'suspend_success_count': 'int',
        'transaction_id': 'int',
        'transaction_state': 'str',
        'two_phase_commit_failure_count': 'int',
        'two_phase_commit_success_count': 'int'
    }

    attribute_map = {
        'client_name': 'clientName',
        'commit_count': 'commitCount',
        'commit_failure_count': 'commitFailureCount',
        'commit_success_count': 'commitSuccessCount',
        'consumed_msg_count': 'consumedMsgCount',
        'end_fail_failure_count': 'endFailFailureCount',
        'end_fail_success_count': 'endFailSuccessCount',
        'end_failure_count': 'endFailureCount',
        'end_rollback_failure_count': 'endRollbackFailureCount',
        'end_rollback_success_count': 'endRollbackSuccessCount',
        'end_success_count': 'endSuccessCount',
        'failure_count': 'failureCount',
        'forget_failure_count': 'forgetFailureCount',
        'forget_success_count': 'forgetSuccessCount',
        'msg_vpn_name': 'msgVpnName',
        'one_phase_commit_failure_count': 'onePhaseCommitFailureCount',
        'one_phase_commit_success_count': 'onePhaseCommitSuccessCount',
        'pending_consumed_msg_count': 'pendingConsumedMsgCount',
        'pending_published_msg_count': 'pendingPublishedMsgCount',
        'prepare_failure_count': 'prepareFailureCount',
        'prepare_success_count': 'prepareSuccessCount',
        'previous_transaction_state': 'previousTransactionState',
        'published_msg_count': 'publishedMsgCount',
        'resume_failure_count': 'resumeFailureCount',
        'resume_success_count': 'resumeSuccessCount',
        'retrieved_msg_count': 'retrievedMsgCount',
        'rollback_count': 'rollbackCount',
        'rollback_failure_count': 'rollbackFailureCount',
        'rollback_success_count': 'rollbackSuccessCount',
        'session_name': 'sessionName',
        'spooled_msg_count': 'spooledMsgCount',
        'start_failure_count': 'startFailureCount',
        'start_success_count': 'startSuccessCount',
        'success_count': 'successCount',
        'suspend_failure_count': 'suspendFailureCount',
        'suspend_success_count': 'suspendSuccessCount',
        'transaction_id': 'transactionId',
        'transaction_state': 'transactionState',
        'two_phase_commit_failure_count': 'twoPhaseCommitFailureCount',
        'two_phase_commit_success_count': 'twoPhaseCommitSuccessCount'
    }

    def __init__(self, client_name=None, commit_count=None, commit_failure_count=None, commit_success_count=None, consumed_msg_count=None, end_fail_failure_count=None, end_fail_success_count=None, end_failure_count=None, end_rollback_failure_count=None, end_rollback_success_count=None, end_success_count=None, failure_count=None, forget_failure_count=None, forget_success_count=None, msg_vpn_name=None, one_phase_commit_failure_count=None, one_phase_commit_success_count=None, pending_consumed_msg_count=None, pending_published_msg_count=None, prepare_failure_count=None, prepare_success_count=None, previous_transaction_state=None, published_msg_count=None, resume_failure_count=None, resume_success_count=None, retrieved_msg_count=None, rollback_count=None, rollback_failure_count=None, rollback_success_count=None, session_name=None, spooled_msg_count=None, start_failure_count=None, start_success_count=None, success_count=None, suspend_failure_count=None, suspend_success_count=None, transaction_id=None, transaction_state=None, two_phase_commit_failure_count=None, two_phase_commit_success_count=None):  # noqa: E501
        """MsgVpnClientTransactedSession - a model defined in Swagger"""  # noqa: E501

        self._client_name = None
        self._commit_count = None
        self._commit_failure_count = None
        self._commit_success_count = None
        self._consumed_msg_count = None
        self._end_fail_failure_count = None
        self._end_fail_success_count = None
        self._end_failure_count = None
        self._end_rollback_failure_count = None
        self._end_rollback_success_count = None
        self._end_success_count = None
        self._failure_count = None
        self._forget_failure_count = None
        self._forget_success_count = None
        self._msg_vpn_name = None
        self._one_phase_commit_failure_count = None
        self._one_phase_commit_success_count = None
        self._pending_consumed_msg_count = None
        self._pending_published_msg_count = None
        self._prepare_failure_count = None
        self._prepare_success_count = None
        self._previous_transaction_state = None
        self._published_msg_count = None
        self._resume_failure_count = None
        self._resume_success_count = None
        self._retrieved_msg_count = None
        self._rollback_count = None
        self._rollback_failure_count = None
        self._rollback_success_count = None
        self._session_name = None
        self._spooled_msg_count = None
        self._start_failure_count = None
        self._start_success_count = None
        self._success_count = None
        self._suspend_failure_count = None
        self._suspend_success_count = None
        self._transaction_id = None
        self._transaction_state = None
        self._two_phase_commit_failure_count = None
        self._two_phase_commit_success_count = None
        self.discriminator = None

        if client_name is not None:
            self.client_name = client_name
        if commit_count is not None:
            self.commit_count = commit_count
        if commit_failure_count is not None:
            self.commit_failure_count = commit_failure_count
        if commit_success_count is not None:
            self.commit_success_count = commit_success_count
        if consumed_msg_count is not None:
            self.consumed_msg_count = consumed_msg_count
        if end_fail_failure_count is not None:
            self.end_fail_failure_count = end_fail_failure_count
        if end_fail_success_count is not None:
            self.end_fail_success_count = end_fail_success_count
        if end_failure_count is not None:
            self.end_failure_count = end_failure_count
        if end_rollback_failure_count is not None:
            self.end_rollback_failure_count = end_rollback_failure_count
        if end_rollback_success_count is not None:
            self.end_rollback_success_count = end_rollback_success_count
        if end_success_count is not None:
            self.end_success_count = end_success_count
        if failure_count is not None:
            self.failure_count = failure_count
        if forget_failure_count is not None:
            self.forget_failure_count = forget_failure_count
        if forget_success_count is not None:
            self.forget_success_count = forget_success_count
        if msg_vpn_name is not None:
            self.msg_vpn_name = msg_vpn_name
        if one_phase_commit_failure_count is not None:
            self.one_phase_commit_failure_count = one_phase_commit_failure_count
        if one_phase_commit_success_count is not None:
            self.one_phase_commit_success_count = one_phase_commit_success_count
        if pending_consumed_msg_count is not None:
            self.pending_consumed_msg_count = pending_consumed_msg_count
        if pending_published_msg_count is not None:
            self.pending_published_msg_count = pending_published_msg_count
        if prepare_failure_count is not None:
            self.prepare_failure_count = prepare_failure_count
        if prepare_success_count is not None:
            self.prepare_success_count = prepare_success_count
        if previous_transaction_state is not None:
            self.previous_transaction_state = previous_transaction_state
        if published_msg_count is not None:
            self.published_msg_count = published_msg_count
        if resume_failure_count is not None:
            self.resume_failure_count = resume_failure_count
        if resume_success_count is not None:
            self.resume_success_count = resume_success_count
        if retrieved_msg_count is not None:
            self.retrieved_msg_count = retrieved_msg_count
        if rollback_count is not None:
            self.rollback_count = rollback_count
        if rollback_failure_count is not None:
            self.rollback_failure_count = rollback_failure_count
        if rollback_success_count is not None:
            self.rollback_success_count = rollback_success_count
        if session_name is not None:
            self.session_name = session_name
        if spooled_msg_count is not None:
            self.spooled_msg_count = spooled_msg_count
        if start_failure_count is not None:
            self.start_failure_count = start_failure_count
        if start_success_count is not None:
            self.start_success_count = start_success_count
        if success_count is not None:
            self.success_count = success_count
        if suspend_failure_count is not None:
            self.suspend_failure_count = suspend_failure_count
        if suspend_success_count is not None:
            self.suspend_success_count = suspend_success_count
        if transaction_id is not None:
            self.transaction_id = transaction_id
        if transaction_state is not None:
            self.transaction_state = transaction_state
        if two_phase_commit_failure_count is not None:
            self.two_phase_commit_failure_count = two_phase_commit_failure_count
        if two_phase_commit_success_count is not None:
            self.two_phase_commit_success_count = two_phase_commit_success_count

    @property
    def client_name(self):
        """Gets the client_name of this MsgVpnClientTransactedSession.  # noqa: E501

        The name of the Client.  # noqa: E501

        :return: The client_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this MsgVpnClientTransactedSession.

        The name of the Client.  # noqa: E501

        :param client_name: The client_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def commit_count(self):
        """Gets the commit_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transactions committed within the Transacted Session.  # noqa: E501

        :return: The commit_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._commit_count

    @commit_count.setter
    def commit_count(self, commit_count):
        """Sets the commit_count of this MsgVpnClientTransactedSession.

        The number of transactions committed within the Transacted Session.  # noqa: E501

        :param commit_count: The commit_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._commit_count = commit_count

    @property
    def commit_failure_count(self):
        """Gets the commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction commit operations that failed.  # noqa: E501

        :return: The commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._commit_failure_count

    @commit_failure_count.setter
    def commit_failure_count(self, commit_failure_count):
        """Sets the commit_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction commit operations that failed.  # noqa: E501

        :param commit_failure_count: The commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._commit_failure_count = commit_failure_count

    @property
    def commit_success_count(self):
        """Gets the commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction commit operations that succeeded.  # noqa: E501

        :return: The commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._commit_success_count

    @commit_success_count.setter
    def commit_success_count(self, commit_success_count):
        """Sets the commit_success_count of this MsgVpnClientTransactedSession.

        The number of transaction commit operations that succeeded.  # noqa: E501

        :param commit_success_count: The commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._commit_success_count = commit_success_count

    @property
    def consumed_msg_count(self):
        """Gets the consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages consumed within the Transacted Session.  # noqa: E501

        :return: The consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._consumed_msg_count

    @consumed_msg_count.setter
    def consumed_msg_count(self, consumed_msg_count):
        """Sets the consumed_msg_count of this MsgVpnClientTransactedSession.

        The number of messages consumed within the Transacted Session.  # noqa: E501

        :param consumed_msg_count: The consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._consumed_msg_count = consumed_msg_count

    @property
    def end_fail_failure_count(self):
        """Gets the end_fail_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end fail operations that failed.  # noqa: E501

        :return: The end_fail_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_fail_failure_count

    @end_fail_failure_count.setter
    def end_fail_failure_count(self, end_fail_failure_count):
        """Sets the end_fail_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction end fail operations that failed.  # noqa: E501

        :param end_fail_failure_count: The end_fail_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_fail_failure_count = end_fail_failure_count

    @property
    def end_fail_success_count(self):
        """Gets the end_fail_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end fail operations that succeeded.  # noqa: E501

        :return: The end_fail_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_fail_success_count

    @end_fail_success_count.setter
    def end_fail_success_count(self, end_fail_success_count):
        """Sets the end_fail_success_count of this MsgVpnClientTransactedSession.

        The number of transaction end fail operations that succeeded.  # noqa: E501

        :param end_fail_success_count: The end_fail_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_fail_success_count = end_fail_success_count

    @property
    def end_failure_count(self):
        """Gets the end_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end operations that failed.  # noqa: E501

        :return: The end_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_failure_count

    @end_failure_count.setter
    def end_failure_count(self, end_failure_count):
        """Sets the end_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction end operations that failed.  # noqa: E501

        :param end_failure_count: The end_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_failure_count = end_failure_count

    @property
    def end_rollback_failure_count(self):
        """Gets the end_rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end rollback operations that failed.  # noqa: E501

        :return: The end_rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_rollback_failure_count

    @end_rollback_failure_count.setter
    def end_rollback_failure_count(self, end_rollback_failure_count):
        """Sets the end_rollback_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction end rollback operations that failed.  # noqa: E501

        :param end_rollback_failure_count: The end_rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_rollback_failure_count = end_rollback_failure_count

    @property
    def end_rollback_success_count(self):
        """Gets the end_rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end rollback operations that succeeded.  # noqa: E501

        :return: The end_rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_rollback_success_count

    @end_rollback_success_count.setter
    def end_rollback_success_count(self, end_rollback_success_count):
        """Sets the end_rollback_success_count of this MsgVpnClientTransactedSession.

        The number of transaction end rollback operations that succeeded.  # noqa: E501

        :param end_rollback_success_count: The end_rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_rollback_success_count = end_rollback_success_count

    @property
    def end_success_count(self):
        """Gets the end_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction end operations that succeeded.  # noqa: E501

        :return: The end_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._end_success_count

    @end_success_count.setter
    def end_success_count(self, end_success_count):
        """Sets the end_success_count of this MsgVpnClientTransactedSession.

        The number of transaction end operations that succeeded.  # noqa: E501

        :param end_success_count: The end_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._end_success_count = end_success_count

    @property
    def failure_count(self):
        """Gets the failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transactions that failed within the Transacted Session.  # noqa: E501

        :return: The failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._failure_count

    @failure_count.setter
    def failure_count(self, failure_count):
        """Sets the failure_count of this MsgVpnClientTransactedSession.

        The number of transactions that failed within the Transacted Session.  # noqa: E501

        :param failure_count: The failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._failure_count = failure_count

    @property
    def forget_failure_count(self):
        """Gets the forget_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction forget operations that failed.  # noqa: E501

        :return: The forget_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._forget_failure_count

    @forget_failure_count.setter
    def forget_failure_count(self, forget_failure_count):
        """Sets the forget_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction forget operations that failed.  # noqa: E501

        :param forget_failure_count: The forget_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._forget_failure_count = forget_failure_count

    @property
    def forget_success_count(self):
        """Gets the forget_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction forget operations that succeeded.  # noqa: E501

        :return: The forget_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._forget_success_count

    @forget_success_count.setter
    def forget_success_count(self, forget_success_count):
        """Sets the forget_success_count of this MsgVpnClientTransactedSession.

        The number of transaction forget operations that succeeded.  # noqa: E501

        :param forget_success_count: The forget_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._forget_success_count = forget_success_count

    @property
    def msg_vpn_name(self):
        """Gets the msg_vpn_name of this MsgVpnClientTransactedSession.  # noqa: E501

        The name of the Message VPN.  # noqa: E501

        :return: The msg_vpn_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: str
        """
        return self._msg_vpn_name

    @msg_vpn_name.setter
    def msg_vpn_name(self, msg_vpn_name):
        """Sets the msg_vpn_name of this MsgVpnClientTransactedSession.

        The name of the Message VPN.  # noqa: E501

        :param msg_vpn_name: The msg_vpn_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: str
        """

        self._msg_vpn_name = msg_vpn_name

    @property
    def one_phase_commit_failure_count(self):
        """Gets the one_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction one-phase commit operations that failed.  # noqa: E501

        :return: The one_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._one_phase_commit_failure_count

    @one_phase_commit_failure_count.setter
    def one_phase_commit_failure_count(self, one_phase_commit_failure_count):
        """Sets the one_phase_commit_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction one-phase commit operations that failed.  # noqa: E501

        :param one_phase_commit_failure_count: The one_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._one_phase_commit_failure_count = one_phase_commit_failure_count

    @property
    def one_phase_commit_success_count(self):
        """Gets the one_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction one-phase commit operations that succeeded.  # noqa: E501

        :return: The one_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._one_phase_commit_success_count

    @one_phase_commit_success_count.setter
    def one_phase_commit_success_count(self, one_phase_commit_success_count):
        """Sets the one_phase_commit_success_count of this MsgVpnClientTransactedSession.

        The number of transaction one-phase commit operations that succeeded.  # noqa: E501

        :param one_phase_commit_success_count: The one_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._one_phase_commit_success_count = one_phase_commit_success_count

    @property
    def pending_consumed_msg_count(self):
        """Gets the pending_consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages to be consumed when the transaction is committed.  # noqa: E501

        :return: The pending_consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._pending_consumed_msg_count

    @pending_consumed_msg_count.setter
    def pending_consumed_msg_count(self, pending_consumed_msg_count):
        """Sets the pending_consumed_msg_count of this MsgVpnClientTransactedSession.

        The number of messages to be consumed when the transaction is committed.  # noqa: E501

        :param pending_consumed_msg_count: The pending_consumed_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._pending_consumed_msg_count = pending_consumed_msg_count

    @property
    def pending_published_msg_count(self):
        """Gets the pending_published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages to be published when the transaction is committed.  # noqa: E501

        :return: The pending_published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._pending_published_msg_count

    @pending_published_msg_count.setter
    def pending_published_msg_count(self, pending_published_msg_count):
        """Sets the pending_published_msg_count of this MsgVpnClientTransactedSession.

        The number of messages to be published when the transaction is committed.  # noqa: E501

        :param pending_published_msg_count: The pending_published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._pending_published_msg_count = pending_published_msg_count

    @property
    def prepare_failure_count(self):
        """Gets the prepare_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction prepare operations that failed.  # noqa: E501

        :return: The prepare_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._prepare_failure_count

    @prepare_failure_count.setter
    def prepare_failure_count(self, prepare_failure_count):
        """Sets the prepare_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction prepare operations that failed.  # noqa: E501

        :param prepare_failure_count: The prepare_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._prepare_failure_count = prepare_failure_count

    @property
    def prepare_success_count(self):
        """Gets the prepare_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction prepare operations that succeeded.  # noqa: E501

        :return: The prepare_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._prepare_success_count

    @prepare_success_count.setter
    def prepare_success_count(self, prepare_success_count):
        """Sets the prepare_success_count of this MsgVpnClientTransactedSession.

        The number of transaction prepare operations that succeeded.  # noqa: E501

        :param prepare_success_count: The prepare_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._prepare_success_count = prepare_success_count

    @property
    def previous_transaction_state(self):
        """Gets the previous_transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501

        The state of the previous transaction. The allowed values and their meaning are:  <pre> \"none\" - The previous transaction had no state. \"committed\" - The previous transaction was committed. \"rolled-back\" - The previous transaction was rolled back. \"failed\" - The previous transaction failed. </pre>   # noqa: E501

        :return: The previous_transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: str
        """
        return self._previous_transaction_state

    @previous_transaction_state.setter
    def previous_transaction_state(self, previous_transaction_state):
        """Sets the previous_transaction_state of this MsgVpnClientTransactedSession.

        The state of the previous transaction. The allowed values and their meaning are:  <pre> \"none\" - The previous transaction had no state. \"committed\" - The previous transaction was committed. \"rolled-back\" - The previous transaction was rolled back. \"failed\" - The previous transaction failed. </pre>   # noqa: E501

        :param previous_transaction_state: The previous_transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: str
        """

        self._previous_transaction_state = previous_transaction_state

    @property
    def published_msg_count(self):
        """Gets the published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages published within the Transacted Session.  # noqa: E501

        :return: The published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._published_msg_count

    @published_msg_count.setter
    def published_msg_count(self, published_msg_count):
        """Sets the published_msg_count of this MsgVpnClientTransactedSession.

        The number of messages published within the Transacted Session.  # noqa: E501

        :param published_msg_count: The published_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._published_msg_count = published_msg_count

    @property
    def resume_failure_count(self):
        """Gets the resume_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction resume operations that failed.  # noqa: E501

        :return: The resume_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._resume_failure_count

    @resume_failure_count.setter
    def resume_failure_count(self, resume_failure_count):
        """Sets the resume_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction resume operations that failed.  # noqa: E501

        :param resume_failure_count: The resume_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._resume_failure_count = resume_failure_count

    @property
    def resume_success_count(self):
        """Gets the resume_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction resume operations that succeeded.  # noqa: E501

        :return: The resume_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._resume_success_count

    @resume_success_count.setter
    def resume_success_count(self, resume_success_count):
        """Sets the resume_success_count of this MsgVpnClientTransactedSession.

        The number of transaction resume operations that succeeded.  # noqa: E501

        :param resume_success_count: The resume_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._resume_success_count = resume_success_count

    @property
    def retrieved_msg_count(self):
        """Gets the retrieved_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages retrieved within the Transacted Session.  # noqa: E501

        :return: The retrieved_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._retrieved_msg_count

    @retrieved_msg_count.setter
    def retrieved_msg_count(self, retrieved_msg_count):
        """Sets the retrieved_msg_count of this MsgVpnClientTransactedSession.

        The number of messages retrieved within the Transacted Session.  # noqa: E501

        :param retrieved_msg_count: The retrieved_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._retrieved_msg_count = retrieved_msg_count

    @property
    def rollback_count(self):
        """Gets the rollback_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transactions rolled back within the Transacted Session.  # noqa: E501

        :return: The rollback_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._rollback_count

    @rollback_count.setter
    def rollback_count(self, rollback_count):
        """Sets the rollback_count of this MsgVpnClientTransactedSession.

        The number of transactions rolled back within the Transacted Session.  # noqa: E501

        :param rollback_count: The rollback_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._rollback_count = rollback_count

    @property
    def rollback_failure_count(self):
        """Gets the rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction rollback operations that failed.  # noqa: E501

        :return: The rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._rollback_failure_count

    @rollback_failure_count.setter
    def rollback_failure_count(self, rollback_failure_count):
        """Sets the rollback_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction rollback operations that failed.  # noqa: E501

        :param rollback_failure_count: The rollback_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._rollback_failure_count = rollback_failure_count

    @property
    def rollback_success_count(self):
        """Gets the rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction rollback operations that succeeded.  # noqa: E501

        :return: The rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._rollback_success_count

    @rollback_success_count.setter
    def rollback_success_count(self, rollback_success_count):
        """Sets the rollback_success_count of this MsgVpnClientTransactedSession.

        The number of transaction rollback operations that succeeded.  # noqa: E501

        :param rollback_success_count: The rollback_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._rollback_success_count = rollback_success_count

    @property
    def session_name(self):
        """Gets the session_name of this MsgVpnClientTransactedSession.  # noqa: E501

        The name of the Transacted Session.  # noqa: E501

        :return: The session_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: str
        """
        return self._session_name

    @session_name.setter
    def session_name(self, session_name):
        """Sets the session_name of this MsgVpnClientTransactedSession.

        The name of the Transacted Session.  # noqa: E501

        :param session_name: The session_name of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: str
        """

        self._session_name = session_name

    @property
    def spooled_msg_count(self):
        """Gets the spooled_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of messages spooled within the Transacted Session.  # noqa: E501

        :return: The spooled_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._spooled_msg_count

    @spooled_msg_count.setter
    def spooled_msg_count(self, spooled_msg_count):
        """Sets the spooled_msg_count of this MsgVpnClientTransactedSession.

        The number of messages spooled within the Transacted Session.  # noqa: E501

        :param spooled_msg_count: The spooled_msg_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._spooled_msg_count = spooled_msg_count

    @property
    def start_failure_count(self):
        """Gets the start_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction start operations that failed.  # noqa: E501

        :return: The start_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._start_failure_count

    @start_failure_count.setter
    def start_failure_count(self, start_failure_count):
        """Sets the start_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction start operations that failed.  # noqa: E501

        :param start_failure_count: The start_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._start_failure_count = start_failure_count

    @property
    def start_success_count(self):
        """Gets the start_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction start operations that succeeded.  # noqa: E501

        :return: The start_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._start_success_count

    @start_success_count.setter
    def start_success_count(self, start_success_count):
        """Sets the start_success_count of this MsgVpnClientTransactedSession.

        The number of transaction start operations that succeeded.  # noqa: E501

        :param start_success_count: The start_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._start_success_count = start_success_count

    @property
    def success_count(self):
        """Gets the success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transactions that succeeded within the Transacted Session.  # noqa: E501

        :return: The success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._success_count

    @success_count.setter
    def success_count(self, success_count):
        """Sets the success_count of this MsgVpnClientTransactedSession.

        The number of transactions that succeeded within the Transacted Session.  # noqa: E501

        :param success_count: The success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._success_count = success_count

    @property
    def suspend_failure_count(self):
        """Gets the suspend_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction suspend operations that failed.  # noqa: E501

        :return: The suspend_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._suspend_failure_count

    @suspend_failure_count.setter
    def suspend_failure_count(self, suspend_failure_count):
        """Sets the suspend_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction suspend operations that failed.  # noqa: E501

        :param suspend_failure_count: The suspend_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._suspend_failure_count = suspend_failure_count

    @property
    def suspend_success_count(self):
        """Gets the suspend_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction suspend operations that succeeded.  # noqa: E501

        :return: The suspend_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._suspend_success_count

    @suspend_success_count.setter
    def suspend_success_count(self, suspend_success_count):
        """Sets the suspend_success_count of this MsgVpnClientTransactedSession.

        The number of transaction suspend operations that succeeded.  # noqa: E501

        :param suspend_success_count: The suspend_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._suspend_success_count = suspend_success_count

    @property
    def transaction_id(self):
        """Gets the transaction_id of this MsgVpnClientTransactedSession.  # noqa: E501

        The identifier (ID) of the transaction in the Transacted Session.  # noqa: E501

        :return: The transaction_id of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this MsgVpnClientTransactedSession.

        The identifier (ID) of the transaction in the Transacted Session.  # noqa: E501

        :param transaction_id: The transaction_id of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._transaction_id = transaction_id

    @property
    def transaction_state(self):
        """Gets the transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501

        The state of the current transaction. The allowed values and their meaning are:  <pre> \"in-progress\" - The current transaction is in progress. \"committing\" - The current transaction is committing. \"rolling-back\" - The current transaction is rolling back. \"failing\" - The current transaction is failing. </pre>   # noqa: E501

        :return: The transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: str
        """
        return self._transaction_state

    @transaction_state.setter
    def transaction_state(self, transaction_state):
        """Sets the transaction_state of this MsgVpnClientTransactedSession.

        The state of the current transaction. The allowed values and their meaning are:  <pre> \"in-progress\" - The current transaction is in progress. \"committing\" - The current transaction is committing. \"rolling-back\" - The current transaction is rolling back. \"failing\" - The current transaction is failing. </pre>   # noqa: E501

        :param transaction_state: The transaction_state of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: str
        """

        self._transaction_state = transaction_state

    @property
    def two_phase_commit_failure_count(self):
        """Gets the two_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction two-phase commit operations that failed.  # noqa: E501

        :return: The two_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._two_phase_commit_failure_count

    @two_phase_commit_failure_count.setter
    def two_phase_commit_failure_count(self, two_phase_commit_failure_count):
        """Sets the two_phase_commit_failure_count of this MsgVpnClientTransactedSession.

        The number of transaction two-phase commit operations that failed.  # noqa: E501

        :param two_phase_commit_failure_count: The two_phase_commit_failure_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._two_phase_commit_failure_count = two_phase_commit_failure_count

    @property
    def two_phase_commit_success_count(self):
        """Gets the two_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501

        The number of transaction two-phase commit operations that succeeded.  # noqa: E501

        :return: The two_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :rtype: int
        """
        return self._two_phase_commit_success_count

    @two_phase_commit_success_count.setter
    def two_phase_commit_success_count(self, two_phase_commit_success_count):
        """Sets the two_phase_commit_success_count of this MsgVpnClientTransactedSession.

        The number of transaction two-phase commit operations that succeeded.  # noqa: E501

        :param two_phase_commit_success_count: The two_phase_commit_success_count of this MsgVpnClientTransactedSession.  # noqa: E501
        :type: int
        """

        self._two_phase_commit_success_count = two_phase_commit_success_count

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
        if issubclass(MsgVpnClientTransactedSession, dict):
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
        if not isinstance(other, MsgVpnClientTransactedSession):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
