# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : abstract.py
    @desc :
"""
import typing

from datavita.core import exc


class Field(object):
    """
        字段
    """
    def __init__(
        self,
        required: bool = False,
        default: typing.Any = None,
        dump_to: str = None,
        load_from: str = None,
        strict: bool = None,
        **kwargs
    ):
        self.required = required
        self.default = default
        self.dump_to = dump_to
        self.load_from = load_from
        self.options = kwargs
        self.strict = bool(strict)  # None as False

    def dumps(self, value, **kwargs):
        raise NotImplementedError

    def loads(self, value, **kwargs):
        raise NotImplementedError

    @staticmethod
    def fail(name, expected, got):
        msg = "invalid field {}, expect {}, got {}".format(name, expected, got)
        raise exc.ValidationException(msg)


class Schema(object):
    """
        模式
    """
    fields = {}

    def __init__(
        self,
        required: bool = False,
        default: typing.Union[typing.Callable, typing.Any] = dict,
        dump_to: str = None,
        load_from: str = None,
        strict: bool = False,
        case_sensitive: bool = False,
        **kwargs
    ):
        self.required = required
        self.default = default
        self.dump_to = dump_to
        self.load_from = load_from
        self.options = kwargs
        self.strict = strict
        self.case_sensitive = case_sensitive

    def dumps(self, d: dict) -> dict:
        raise NotImplementedError

    def loads(self, d: dict) -> dict:
        raise NotImplementedError
