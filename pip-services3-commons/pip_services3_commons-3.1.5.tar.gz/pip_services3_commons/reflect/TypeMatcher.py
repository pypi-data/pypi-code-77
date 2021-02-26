# -*- coding: utf-8 -*-
"""
    pip_services3_commons.reflect.TypeMatcher
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Type matcher implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime

from pip_services3_commons.convert import TypeCode


class TypeMatcher:
    """
    Helper class matches value types for equality.

    This class has symmetric implementation across all languages supported
    by Pip.Services toolkit and used to support dynamic data processing.
    """
    @staticmethod
    def match_value(expected_type, actual_value):
        """
        Matches expected type to a type of a value.
        The expected type can be specified by a type, type name or :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`.

        :param expected_type: an expected type to match.

        :param actual_value: a value to match its type to the expected one.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_value is None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type(expected_type, type(actual_value))

    @staticmethod
    def match_type(expected_type, actual_type):
        """
        Matches expected type to an actual type.
        The types can be specified as types, type names or :class:`TypeCode <pip_services3_commons.convert.TypeCode.TypeCode>`.

        :param expected_type: an expected type to match.

        :param actual_type: an actual type to match.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_type is None:
            raise Exception("Actual type cannot be null")

        if isinstance(expected_type, type):
            return issubclass(actual_type, expected_type)

        if isinstance(expected_type, str):
            return TypeMatcher.match_type_by_name(expected_type, actual_type)
        if isinstance(expected_type, int):
            if expected_type == actual_type:
                return True
            # Special provisions for dynamic data
            if expected_type == TypeCode.Integer and (actual_type == TypeCode.Long or actual_type == TypeCode.Float or actual_type == TypeCode.Double):
                return True
            if expected_type == TypeCode.Long and (actual_type == TypeCode.Integer or actual_type == TypeCode.Float or actual_type == TypeCode.Double):
                return True
            if expected_type == TypeCode.Float and (actual_type == TypeCode.Integer or actual_type == TypeCode.Long or actual_type == TypeCode.Double):
                return True
            if expected_type == TypeCode.Double and (actual_type == TypeCode.Integer or actual_type == TypeCode.Long or actual_type == TypeCode.Float):
                return True
            # if expected_type == TypeCode.DateTime and (actual_type == TypeCode.String and DateTimeConverter.toNullableDateTime(actualValue) != null):
            #     return True

        return False

    @staticmethod
    def match_value_by_name(expected_type, actual_value):
        """
        Matches expected type to a type of a value.

        :param expected_type: an expected type name to match.

        :param actual_value: a value to match its type to the expected one.

        :return: True if types are matching and False if they don't.
        """
        if expected_type is None:
            return True
        if actual_value is None:
            raise Exception("Actual value cannot be null")

        return TypeMatcher.match_type_by_name(expected_type, type(actual_value))

    @staticmethod
    def match_type_by_name(expected_type, actual_type):
        """
        Matches expected type to an actual type.

        :param expected_type: an expected type name to match.

        :param actual_type: an actual type to match defined by type code.

        :return: true if types are matching and false if they don't.
        """
        if expected_type is None:
            return True
        if actual_type is None:
            raise Exception("Actual type cannot be null")
        
        expected_type = expected_type.lower()

        if actual_type.__name__.lower() == expected_type: 
            return True
        elif expected_type == "object":
            return True
        elif expected_type == "int" or expected_type == "integer":
            return issubclass(actual_type, int) #or issubclass(actual_type, long)
        elif expected_type == "long":
            return issubclass(actual_type, int)
        elif expected_type == "float" or expected_type == "double":
            return issubclass(actual_type, float)
        elif expected_type == "string":
            return issubclass(actual_type, str) #or issubclass(actual_type, unicode)
        elif expected_type == "bool" or expected_type == "boolean":
            return issubclass(actual_type, bool)
        elif expected_type == "date" or expected_type == "datetime":
            return issubclass(actual_type, datetime.datetime) or issubclass(actual_type. datetime.date)
        elif expected_type == "timespan" or expected_type == "duration":
            return issubclass(actual_type, int) or issubclass(actual_type, float)
        elif expected_type == "enum":
            return issubclass(actual_type, str) or issubclass(actual_type, int)
        elif expected_type == "map" or expected_type == "dict" or expected_type == "dictionary":
            return issubclass(actual_type, dict)
        elif expected_type == "array" or expected_type == "list":
            return issubclass(actual_type, list) or issubclass(actual_type, tuple) or issubclass(actual_type, set)
        elif expected_type.endswith("[]"):
            # Todo: Check subtype
            return issubclass(actual_type, list) or issubclass(actual_type, tuple) or issubclass(actual_type, set)
        else:
            return False
