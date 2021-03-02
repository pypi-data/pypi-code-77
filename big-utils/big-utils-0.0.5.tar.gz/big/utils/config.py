"""
Configuration utilities
"""
import json
import logging
import logging.config
import os
from pathlib import Path
from big.utils.strutil import ensure_not_blank, trim, string_2_bool, trim_to_lower

# name of the default logging configuration file
DEFAULT_LOGGING_CONFIG_FILE = 'logging.json'

# name of the default application configuration file
DEFAULT_APP_CONFIG_FILE = 'config.json'


def get_namespace_root():
    """
    Returns the *root* of the application namespace - this method relies explicitly
    on being two packages deep ``big/utils``. So, essentially, it returns a parent
    directory of ``big/utils``.
    """
    return Path(__file__).parent.parent.parent


def configure_logging(config_file_path=None):
    """
    Configures the logging subsystem using the JSON configuration provided in the specified file.
    If the file is not provided (``config_file_path=None``), a default file name, specified by
    the ``DEFAULT_LOGGING_CONFIG_FILE`` constant, is used. That file is assumed to exist at the
    root of the application namespace.

    :param config_file_path: a full (absolute) path of the configuration file or ``None`` (default).
    """
    logging.basicConfig(level="INFO")
    logger = logging.getLogger('config')
    logger.info('*** Initializing logging subsystem configuration')

    file_path = config_file_path if config_file_path else get_namespace_root() / DEFAULT_LOGGING_CONFIG_FILE
    logger.info('*** Logging configuration will be read from the [%s] file', file_path)

    with open(file_path) as f:
        json_config = json.load(f)
        logger.info('*** Logging configuration loaded successfully')

    logging.config.dictConfig(json_config['logging'])
    logger.info('*** Logging subsystem configured ***')


def get_configuration(config_name=None, config_file_path=None, upper_case_keys_only=True, envs=None):
    file_path = config_file_path if config_file_path else get_namespace_root() / DEFAULT_APP_CONFIG_FILE
    config_factory = FileConfigFactory(file_path, upper_case_keys_only=upper_case_keys_only, envs=envs)
    return config_factory[config_name if config_name else 'default']


def _require_bool(val, message=None):
    """Ensures that the value is a boolean value"""
    if not isinstance(val, bool):
        raise ValueError(message if message else "Value must a boolean value")
    return val


class ConfigItem:
    """
    Special class used to interpret individual items in the JSON configuration file.
    """
    TYPE_BOOL = 'bool'
    TYPE_STR = 'str'
    TYPE_INT = 'int'

    VALID_TYPES = [TYPE_STR, TYPE_INT, TYPE_BOOL]

    def __init__(self, key, value_dict):
        self.key = ensure_not_blank(key, "Configuration key must not be blank")
        self.required = _require_bool(value_dict.get('required', False))
        self.lower_case = _require_bool(value_dict.get('lower_case', False))
        self.upper_case = _require_bool(value_dict.get('upper_case', False))

        env_name = trim(value_dict.get('env', self.key))
        self.env_name = env_name if env_name else self.key

        val_type = trim(str(value_dict.get('type', self.TYPE_STR)), self.TYPE_STR).lower()
        if val_type not in self.VALID_TYPES:
            raise ValueError(f'<type> must be on of {self.VALID_TYPES}')
        self.value_type = val_type
        self.default_value = self.__extract_value(value_dict.get('value'))

    @property
    def value(self):
        resolved_value = os.getenv(self.env_name)
        if resolved_value:
            resolved_value = self.__extract_value(resolved_value)
        else:
            resolved_value = self.default_value

        if resolved_value is None and self.required:
            raise LookupError(f'Environment variable [{self.env_name}] must be defined')
        return resolved_value

    def __extract_value(self, val):
        if val:
            extract_dispatch = {
                self.TYPE_STR: self.__extract_str,
                self.TYPE_INT: self.__extract_int,
                self.TYPE_BOOL: self.__extract_bool
            }
            val = extract_dispatch[self.value_type](val)
        return val

    @staticmethod
    def __extract_bool(val):
        if isinstance(val, bool):
            return val
        return string_2_bool(str(val))

    def __extract_str(self, val):
        if self.lower_case and self.upper_case:
            raise ValueError('<lower_case> and <upper_case> cannot be true at the same time')
        val = trim(str(val))
        return val.lower() if self.lower_case else val.upper() if self.upper_case else val

    @staticmethod
    def __extract_int(val):
        if isinstance(val, int):
            return val
        return eval(trim(str(val)))


class ConfigFactory:
    """Loads the configuration from the specified dictionary"""
    STANDARD_ENVS = ('development', 'testing', 'production')
    DEFAULT_ENV = 'development'

    def __init__(self, config_dict, upper_case_keys_only=True, envs=None):
        self.env_configs = {}
        self.upper_case_keys_only = upper_case_keys_only

        # get the actual dictionary - it is stored under key 'config'
        config_dict = config_dict['config']
        self.default_env = config_dict.get('default_env', self.DEFAULT_ENV)
        common = self.__load_configuration(config_dict.get('common'))

        # use default environment names, unless specified otherwise
        envs = envs if envs else self.STANDARD_ENVS

        for env_name in envs:
            env_name = ensure_not_blank(env_name, 'Environment name must not be blank')
            env_name_key = env_name.lower()
            self.env_configs[env_name_key] = common.copy()
            env_cfg = self.__load_configuration(config_dict.get(env_name))
            if env_cfg:
                self.env_configs[env_name_key].update(env_cfg)

    def __load_configuration(self, env_dict):
        config = {}
        if env_dict:
            for key in env_dict.keys():
                og_key = key
                key = trim(key)
                if not self.upper_case_keys_only or (self.upper_case_keys_only and key == key.upper()):
                    ci = ConfigItem(key, env_dict[og_key])
                    config[key] = ci.value
        return config

    def __getitem__(self, key):
        key = trim_to_lower(key)
        key = self.default_env if key == 'default' else key
        return self.env_configs[key]


class FileConfigFactory(ConfigFactory):
    """Loads the configuration from the specified file"""
    def __init__(self, config_file, upper_case_keys_only=True, envs=ConfigFactory.STANDARD_ENVS):
        with open(config_file) as f:
            json_config = json.load(f)

        super().__init__(json_config, upper_case_keys_only, envs)
