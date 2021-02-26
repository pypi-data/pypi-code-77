# Copyright (C) 2021 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Task definition for creating plugin for the specified tool."""
import os
import shutil
from pathlib import Path
from typing import Dict

from ayx_plugin_cli.ayx_workspace.constants import (
    AYX_CLI_WORKSPACE_FILES_PATH,
    AYX_WORKSPACE_JSON_PATH,
    BackendLanguage,
    TEMPLATE_ICON_PATH,
    TEMPLATE_TOOL_CONFIG_DIR,
    TEMPLATE_TOOL_ICON_PATH,
    TEMPLATE_TOOL_UI_DIR,
    TemplateToolTypes,
    UI_TEMPLATE_CACHE_DIR,
)
from ayx_plugin_cli.ayx_workspace.models.v1 import AyxWorkspaceV1
from ayx_plugin_cli.node_js_helpers import run_npm

from doit.tools import run_once


def task__download_ui_tool_template() -> Dict:
    """Task to download the UI tool template."""
    return {
        "actions": [(download_ui_tool_template, [UI_TEMPLATE_CACHE_DIR])],
        "targets": [UI_TEMPLATE_CACHE_DIR],
        "uptodate": [run_once],
    }


def task_create_plugin() -> Dict:
    """Create a plugin for the specified tool."""
    tool_type_choices = tuple((tool_type, "") for tool_type in TemplateToolTypes)

    return {
        "title": lambda task: "Create plugin",
        "actions": [
            copy_ui_tool_template,
            ui_npm_install,
            build_backend_action(AyxWorkspaceV1.load().backend_language),
            generate_tool_configuration,
        ],
        "file_dep": [AYX_WORKSPACE_JSON_PATH],
        "task_dep": ["_download_ui_tool_template"],
        "params": [
            {
                "name": "tool_name",
                "long": "tool_name",
                "type": str,
                "default": "PlaceholderToolName",
            },
            {
                "name": "tool_type",
                "long": "tool_type",
                "type": str,
                "default": tool_type_choices[0][0],
                "choices": tool_type_choices,
            },
        ],
        "uptodate": [False],
    }


def build_backend_action(language: BackendLanguage) -> str:
    """Build action to create a plugin."""
    try:
        return {
            BackendLanguage.Python: " ".join(
                [
                    "ayx_python_sdk",
                    "create-ayx-plugin",
                    "--name",
                    "%(tool_name)s",
                    "--tool-type",
                    "%(tool_type)s",
                    "--workspace-directory",
                    '"' + os.getcwd() + '"',
                ]
            )
        }[language]
    except KeyError:
        raise NotImplementedError(f"{language} is not supported as a backend language.")


def generate_tool_configuration(tool_name: str) -> None:
    """Generate default icons for each tool."""
    tool_config_dir = Path(".") / (TEMPLATE_TOOL_CONFIG_DIR % {"tool_name": tool_name})
    tool_config_dir.mkdir()

    shutil.copy(
        TEMPLATE_ICON_PATH,
        Path(".") / (TEMPLATE_TOOL_ICON_PATH % {"tool_name": tool_name}),
    )


def copy_ui_tool_template(tool_name: str) -> None:
    """Copy the UI tool template to the new tool location."""
    shutil.copytree(
        UI_TEMPLATE_CACHE_DIR,
        Path(".") / (TEMPLATE_TOOL_UI_DIR % {"tool_name": tool_name}),
    )


def ui_npm_install(tool_name: str) -> None:
    """Copy the UI tool template to the new tool location."""
    run_npm(
        ["install"], cwd=Path(".") / (TEMPLATE_TOOL_UI_DIR % {"tool_name": tool_name})
    )


def download_ui_tool_template(path: Path = UI_TEMPLATE_CACHE_DIR) -> None:
    """Download the UI template to the specified location."""
    # TODO BEFORE RELEASE: Change this to pull the UI tool template from
    # github instead of a local asset
    zip_cache = path.parent / f"{path.name}.zip"
    if zip_cache.is_file():
        zip_cache.unlink()

    if zip_cache.is_dir():
        shutil.rmtree(zip_cache)

    if path.exists():
        raise FileExistsError("UI Tool template path specified already exists.")

    zip_cache.parent.mkdir(exist_ok=True, parents=True)

    shutil.copy(
        AYX_CLI_WORKSPACE_FILES_PATH / f"{UI_TEMPLATE_CACHE_DIR.name}.zip", zip_cache
    )

    shutil.unpack_archive(zip_cache, path)

    zip_cache.unlink()
