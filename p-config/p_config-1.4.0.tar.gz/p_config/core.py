"""
core
"""
from copy import copy
import json
import os
import warnings

import yaml
from .converter import Converter
from .utils import open_file, Dict


class ConfigMeta(type):
    def __new__(cls, name, bases, attrs):
        converter_mapping = {}
        to_be_removed = []
        for key, value in attrs.items():
            if isinstance(value, (type, Converter)):
                converter_mapping[key.upper()] = value
                to_be_removed.append(key)
            elif key.isupper() and callable(value):
                converter_mapping[key.upper()] = value
                to_be_removed.append(key)
        for key in to_be_removed:
            attrs.pop(key)
        attrs['_converter'] = converter_mapping
        return super().__new__(cls, name, bases, attrs)


class Config(metaclass=ConfigMeta):
    def __init__(self, config_file=None, **defaults):
        self._config = Dict()
        self._converter = copy(self._converter)
        self._update(**defaults)
        if config_file:
            self.load_file(config_file)

    def load(self, file_obj):
        """Same as load_file.
        """
        return self.load_file(file_obj)

    def load_file(self, value, format='yaml'):
        """Load config from a json or yaml file.
        """
        if hasattr(value, 'endswith') and value.endswith('.json') \
                or format == 'json':
            self.load_json_file(value)
        else:
            self.load_yaml_file(value)

    def load_yaml_file(self, value):
        """Load config from yaml file.
        """
        with open_file(value) as f:
            data = yaml.safe_load(f)
        self._update(**data)

    def load_json_file(self, value):
        """Load config from json file.
        """
        with open_file(value) as f:
            data = json.load(f)
        self._update(**data)

    def load_env(self):
        self.load_dict(os.environ)

    def load_dict(self, dct):
        self._update(**dct)

    def _update(self, _prefix='', **dct):
        for key, value in dct.items():
            key = key.upper()
            if _prefix:
                key = _prefix + '.' + key
            if isinstance(value, dict):
                self._update(**value, _prefix=key)
            else:
                self._set(key, value)

    def _set(self, key, value):
        key = key.upper()
        nested_key_lst = key.strip('.').split('.')
        config_dct = self._config
        for part_key in nested_key_lst[:-1]:
            config_dct.setdefault(part_key, Dict())
            if not isinstance(config_dct[part_key], Dict):
                config_dct[part_key] = Dict()
            config_dct = config_dct[part_key]
        part_key = nested_key_lst[-1]
        config_dct[part_key] = self._convert(key, value)

    def _convert(self, key, value):
        if key in self._converter:
            return self._converter[key](value)
        return value

    def set_converter(self, key, convert_func):
        self._converter[key.upper()] = convert_func

    def set_cast_func(self, key, cast_func):
        warnings.warn('use set_converter instead of set_cast_func')
        return self.set_converter(key, cast_func)

    def __getitem__(self, key):
        config = self._config
        for part_key in key.upper().split('.'):
            config = config[part_key]
        return config

    def __setitem__(self, key, value):
        return self._set(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getattr__(self, key):
        if not key.isupper():
            raise KeyError('{} does not exist'.format(key))
        return self.__getitem__(key)
