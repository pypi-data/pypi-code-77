import os
import sys

from dash_data_table import components
from dash_data_table.components import *

__version__ = "0.0.2"
_current_path = os.path.dirname(os.path.abspath(__file__))
METADATA_PATH = os.path.join(_current_path, "components", "metadata.json")

_js_dist = [
    {
        "relative_package_path": "components/dash_data_table.min.js",
        "external_url": f"https://unpkg.com/dash-data-table@{__version__}/dash_data_table/dash_data_table.min.js",
        "namespace": "dash_data_table",
    },
    {
        "relative_package_path": "components/dash_data_table.min.js.map",
        "external_url": f"https://unpkg.com/dash-data-table@{__version__}/dash_data_table/dash_data_table.min.js.map",
        "namespace": "dash_data_table",
        "dynamic": True,
    },
]
_css_dist = []

for component in components.__all__:
    setattr(locals()[component], "_js_dist", _js_dist)
    setattr(locals()[component], "_css_dist", _css_dist)
