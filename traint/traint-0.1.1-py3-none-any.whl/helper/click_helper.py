import os
from pathlib import Path
from configparser import ConfigParser, NoSectionError
from enum import Enum
import click
from collections import OrderedDict
from tabulate import tabulate

class ConfigEntry(Enum):
    API_BASE_URL = "base_url"
    API_TOKEN = "token"

class ClickHelper(object):
    CONFIG_FILE_NAME = '.traint'
    CONFIG_FILE_PATH = os.path.join(Path.home(), CONFIG_FILE_NAME)

    @classmethod
    def echo_highlight(cls, msg: str, new_line=True):
        click.echo(click.style(msg, fg='cyan'), nl=new_line)

    @classmethod
    def echo_warning(cls, msg: str, new_line=True):
        click.echo(click.style(msg, fg='yellow'), nl=new_line)

    @classmethod
    def echo_error(cls, msg: str, new_line=True):
        click.echo(click.style(str(msg), fg='red'), nl=new_line)

    @classmethod
    def echo_dual_color_highlight(cls, first: str, second: str):
        cls.echo_highlight(first, new_line=False)
        click.echo(second)

    @classmethod
    def echo_table(cls, objects, ordered_keys = None):
        # sort object attributes
        if ordered_keys:
            objects = [OrderedDict((k, u[k]) for k in ordered_keys) for u in objects]

        click.echo('\n' + tabulate(objects, headers="keys") + '\n')

    @classmethod
    def prompt_config_values(cls):
        api_base_url = click.prompt('Please enter api base url', type=str, default='https://api.traint.ai/v1')
        # validate
        api_token = click.prompt('Please enter api token', type=str)
        # validate
        cls.save_config(api_base_url, api_token)

    @classmethod
    def save_config(cls, api_base_url, api_token):
        config = ConfigParser(strict=False)
        config.read(cls.CONFIG_FILE_PATH)
        if not config.has_section('api'):
            config.add_section('api')
        config.set('api', ConfigEntry.API_BASE_URL.value, api_base_url)
        config.set('api', ConfigEntry.API_TOKEN.value, api_token)

        with open(cls.CONFIG_FILE_PATH, 'w') as f:
            config.write(f)

    @classmethod
    def get_config_value(cls, key: ConfigEntry):
        config = ConfigParser()
        config.read(cls.CONFIG_FILE_PATH)

        try:
            value = config.get('api', key.value)
        except NoSectionError:
            value = None

        return value

    @classmethod
    def config_complete(cls):
        config = ConfigParser()
        config.read(cls.CONFIG_FILE_PATH)

        try:
            base_url = config.get('api', ConfigEntry.API_BASE_URL.value)
            token = config.get('api', ConfigEntry.API_TOKEN.value)        
        except:
            base_url = False
            token = False
        return base_url and token

