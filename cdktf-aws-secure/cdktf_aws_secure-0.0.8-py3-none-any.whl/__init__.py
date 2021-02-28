'''
[![NPM version](https://badge.fury.io/js/cdktf-aws-secure.svg)](https://badge.fury.io/js/cdktf-aws-secure)
[![PyPI version](https://badge.fury.io/py/cdktf-aws-secure.svg)](https://badge.fury.io/py/cdktf-aws-secure)
![Release](https://github.com/shazi7804/cdktf-aws-secure-constructs/workflows/Release/badge.svg)

# Terraform CDK - AWS Secure constructs

The Level 2 construct can be used to set up your AWS account with the reasonably secure configuration baseline. Internally it uses the [Terraform CDK](https://cdk.tf/) and the [AWS Provider](https://cdk.tf/provider/aws).

## Install

Just the constructs

```
npm install cdktf-aws-secure
```

## Example

* Enable account password policy by default

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from constructs import Construct
from cdktf import Resource
from cdktf_aws_secure import CreateAccountPasswordPolicy

class AwsSecure(Resource):
    def __init__(self, scope, name):
        super().__init__(scope, name)

        policy = CreateAccountPasswordPolicy(self, "DefaultAccountPwdPolicy")

        policy.add_config_rule()
```

## Docs

See [API Docs](./API.md)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class CreateAccountPasswordPolicy(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.CreateAccountPasswordPolicy",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        allow_users_to_change_password: typing.Optional[builtins.bool] = None,
        max_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        password_reuse_prevention: typing.Optional[jsii.Number] = None,
        require_lowercase_characters: typing.Optional[builtins.bool] = None,
        require_numbers: typing.Optional[builtins.bool] = None,
        require_symbols: typing.Optional[builtins.bool] = None,
        require_uppercase_characters: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param allow_users_to_change_password: 
        :param max_password_age: 
        :param minimum_password_length: 
        :param password_reuse_prevention: 
        :param require_lowercase_characters: 
        :param require_numbers: 
        :param require_symbols: 
        :param require_uppercase_characters: 
        '''
        props = CreateAccountPasswordPolicyProps(
            allow_users_to_change_password=allow_users_to_change_password,
            max_password_age=max_password_age,
            minimum_password_length=minimum_password_length,
            password_reuse_prevention=password_reuse_prevention,
            require_lowercase_characters=require_lowercase_characters,
            require_numbers=require_numbers,
            require_symbols=require_symbols,
            require_uppercase_characters=require_uppercase_characters,
        )

        jsii.create(CreateAccountPasswordPolicy, self, [scope, name, props])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self) -> None:
        '''addConfigRule.'''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="expirePasswords")
    def expire_passwords(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "expirePasswords"))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.CreateAccountPasswordPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_users_to_change_password": "allowUsersToChangePassword",
        "max_password_age": "maxPasswordAge",
        "minimum_password_length": "minimumPasswordLength",
        "password_reuse_prevention": "passwordReusePrevention",
        "require_lowercase_characters": "requireLowercaseCharacters",
        "require_numbers": "requireNumbers",
        "require_symbols": "requireSymbols",
        "require_uppercase_characters": "requireUppercaseCharacters",
    },
)
class CreateAccountPasswordPolicyProps:
    def __init__(
        self,
        *,
        allow_users_to_change_password: typing.Optional[builtins.bool] = None,
        max_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        password_reuse_prevention: typing.Optional[jsii.Number] = None,
        require_lowercase_characters: typing.Optional[builtins.bool] = None,
        require_numbers: typing.Optional[builtins.bool] = None,
        require_symbols: typing.Optional[builtins.bool] = None,
        require_uppercase_characters: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_users_to_change_password: 
        :param max_password_age: 
        :param minimum_password_length: 
        :param password_reuse_prevention: 
        :param require_lowercase_characters: 
        :param require_numbers: 
        :param require_symbols: 
        :param require_uppercase_characters: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_users_to_change_password is not None:
            self._values["allow_users_to_change_password"] = allow_users_to_change_password
        if max_password_age is not None:
            self._values["max_password_age"] = max_password_age
        if minimum_password_length is not None:
            self._values["minimum_password_length"] = minimum_password_length
        if password_reuse_prevention is not None:
            self._values["password_reuse_prevention"] = password_reuse_prevention
        if require_lowercase_characters is not None:
            self._values["require_lowercase_characters"] = require_lowercase_characters
        if require_numbers is not None:
            self._values["require_numbers"] = require_numbers
        if require_symbols is not None:
            self._values["require_symbols"] = require_symbols
        if require_uppercase_characters is not None:
            self._values["require_uppercase_characters"] = require_uppercase_characters

    @builtins.property
    def allow_users_to_change_password(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_users_to_change_password")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_password_age(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_password_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_password_length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("minimum_password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_reuse_prevention(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("password_reuse_prevention")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_lowercase_characters(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_lowercase_characters")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_numbers(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_numbers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_symbols(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_symbols")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_uppercase_characters(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_uppercase_characters")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateAccountPasswordPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CreateVpcFlowLog(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.CreateVpcFlowLog",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        vpc_id: builtins.str,
        log_destination: typing.Optional[builtins.str] = None,
        log_destination_type: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param vpc_id: 
        :param log_destination: 
        :param log_destination_type: 
        :param log_format: 
        :param tags: 
        :param traffic_type: 
        '''
        props = CreateVpcFlowLogProps(
            vpc_id=vpc_id,
            log_destination=log_destination,
            log_destination_type=log_destination_type,
            log_format=log_format,
            tags=tags,
            traffic_type=traffic_type,
        )

        jsii.create(CreateVpcFlowLog, self, [scope, name, props])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self) -> None:
        '''addConfigRule.'''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", []))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.CreateVpcFlowLogProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_id": "vpcId",
        "log_destination": "logDestination",
        "log_destination_type": "logDestinationType",
        "log_format": "logFormat",
        "tags": "tags",
        "traffic_type": "trafficType",
    },
)
class CreateVpcFlowLogProps:
    def __init__(
        self,
        *,
        vpc_id: builtins.str,
        log_destination: typing.Optional[builtins.str] = None,
        log_destination_type: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_id: 
        :param log_destination: 
        :param log_destination_type: 
        :param log_format: 
        :param tags: 
        :param traffic_type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc_id": vpc_id,
        }
        if log_destination is not None:
            self._values["log_destination"] = log_destination
        if log_destination_type is not None:
            self._values["log_destination_type"] = log_destination_type
        if log_format is not None:
            self._values["log_format"] = log_format
        if tags is not None:
            self._values["tags"] = tags
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type

    @builtins.property
    def vpc_id(self) -> builtins.str:
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_destination(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_destination_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def traffic_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateVpcFlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CreateAccountPasswordPolicy",
    "CreateAccountPasswordPolicyProps",
    "CreateVpcFlowLog",
    "CreateVpcFlowLogProps",
]

publication.publish()
