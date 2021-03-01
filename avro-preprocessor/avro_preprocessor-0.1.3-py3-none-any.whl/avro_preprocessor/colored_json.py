"""
A module to pretty print colored JSON
"""
import json
import yaml
import yamlloader
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, cast, Optional, Union, Any

from pygments import highlight
from pygments.formatters.terminal256 import TerminalTrueColorFormatter
from pygments.lexers.data import JsonLexer, YamlLexer

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2018, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"


@dataclass
class ColoredJson:
    """
    Pretty prints JSON on the terminal
    """
    json_lexer = JsonLexer()
    yaml_lexer = YamlLexer()
    formatter = TerminalTrueColorFormatter(style='monokai')

    json_indent = 4
    yaml_indent = 4
    yaml_indent_sequence_value = True

    # To force yamlloader to return OrderedDicts even in Python 3.7
    # https://github.com/Phynix/yamlloader/issues/17
    yamlloader.settings.PY_LE_36 = True

    @classmethod
    def highlight_json(cls, data: Union[Dict, OrderedDict],
                       indent: Optional[int] = json_indent) -> str:
        """
        Get a colored, highlighted version of a JSON string.
        :param data: The json to highlight
        :param indent: How much to indent fields in the JSON
        """
        json_text = json.dumps(data, indent=indent)
        return cast(str, highlight(json_text, cls.json_lexer, cls.formatter))

    @classmethod
    def highlight_yaml(cls, data: Union[Dict, OrderedDict],
                       indent: Optional[int] = yaml_indent) -> str:
        """
        Get a colored, highlighted version of a YAML string.
        :param data: The yaml to highlight
        :param indent: How much to indent fields in the YAML
        """
        dumper = IndentSequenceValueDumper if ColoredJson.yaml_indent_sequence_value \
            else yamlloader.ordereddict.CDumper

        yaml_text = yaml.dump(data, Dumper=dumper,
                              indent=ColoredJson.yaml_indent, default_flow_style=False)
        return cast(str, highlight(yaml_text, cls.yaml_lexer, cls.formatter))


class IndentSequenceValueDumper(yamlloader.ordereddict.Dumper):  # type: ignore
    def increase_indent(self, flow: bool = False, indentless: bool = False) \
            -> yamlloader.ordereddict.Dumper:
        return super(IndentSequenceValueDumper, self).increase_indent(flow, False)
