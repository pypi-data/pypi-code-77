# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : schema.py
    @desc :
"""
import logging
from datavita.core.typesystem import abstract
from datavita.core.exc import ValidationException
from datavita.core.utils import compat

logger = logging.getLogger(__name__)


class Schema(abstract.Schema):
    fields = {}

    def dumps(self, d: dict, name=None, **kwargs) -> dict:
        result = {}
        errors = []

        for k, field in self.fields.items():
            v = d.get(k)

            # 解决空值
            if v is None:
                if field.required:
                    errors.append(
                        ValidationException(
                            "the field {k} is required".format(k=k)
                        )
                    )
                    continue

                if field.default is None:
                    continue

                if isinstance(field.default, compat.Callable):
                    v = field.default()
                else:
                    v = field.default

            try:
                serialized = field.dumps(v, name=k)
            except ValidationException as e:
                errors.extend(e.errors)
                continue

            result[field.dump_to or k] = serialized

        if len(errors) > 0:
            raise ValidationException(errors)

        return result

    def loads(self, d: dict, name=None, **kwargs) -> dict:
        result = {}
        errors = []

        if not self.case_sensitive:
            d = {k.lower(): v for k, v in d.items()}

        for k, field in self.fields.items():
            load_key = field.load_from or k
            v = d.get(load_key if self.case_sensitive else load_key.lower())
            if v is None:
                if field.default is None:
                    continue

                if isinstance(field.default, compat.Callable):
                    v = field.default()
                else:
                    v = field.default

            try:
                serialized = field.loads(v, name=k)
            except ValidationException as e:
                errors.extend(e.errors)
                continue

            result[k] = serialized

        if len(errors) > 0:
            raise ValidationException(errors)

        return result


class RequestSchema(Schema):
    fields = {}

    def dumps(self, d: dict, name=None, **kwargs) -> dict:
        if not isinstance(d, dict):
            raise ValidationException(
                "invalid field {}, expect dict, got {}".format(name, type(d))
            )
        result = super(RequestSchema, self).dumps(d, name=name, **kwargs)
        return result


class ResponseSchema(Schema):
    pass
