#!/usr/bin/env python3
#
#  __init__.py
"""
Allows hooks to be defined which are called when recreating a tox testenv.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import os
import sys
from contextlib import contextmanager
from importlib import import_module
from types import CodeType

# 3rd party
import pluggy  # type: ignore
from domdf_python_tools.paths import in_directory
from domdf_python_tools.typing import PathLike
from first import first
from tox import reporter  # type: ignore
from tox.action import Action  # type: ignore
from tox.config import Config, TestenvConfig  # type: ignore
from tox.venv import VirtualEnv  # type: ignore

# this package
import tox_recreate_hook.hooks

__all__ = ["append_to_sys_path", "tox_testenv_create"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

hookimpl = pluggy.HookimplMarker("tox")


@contextmanager
def append_to_sys_path(path: PathLike):
	"""
	Append ``path`` to :py:obj:`sys.path` for the scope of the :keyword:`with` block.

	:param path:
	"""

	path = os.fspath(path)

	if path in sys.path:
		yield
		return

	try:
		sys.path.append(path)
		yield

	finally:
		if path in sys.path:
			sys.path.remove(path)


@hookimpl
def tox_testenv_create(venv: VirtualEnv, action: Action) -> None:  # noqa: D103
	envconfig: TestenvConfig = venv.envconfig
	config: Config = envconfig.config
	toxinidir = config.toxinidir

	if not envconfig.recreate:
		return

	recreate_hook = envconfig._reader.getstring("recreate_hook", '')

	if not recreate_hook.strip():
		return None

	# The whole process should take place within the toxinidir
	with in_directory(toxinidir):
		print(f"output = {recreate_hook}")
		print(config._cfg.path)
		code: CodeType = compile(f"output = {recreate_hook}", config._cfg.path, mode="single")

		hook_globals = {"builtin": tox_recreate_hook.hooks}

		# The first value in co_names will be the name of the module to import, if any
		if code.co_names:
			module_name = first(code.co_names, key=lambda x: x != "output")

			if module_name and module_name != "builtin":
				with append_to_sys_path(toxinidir):
					hook_globals[module_name] = import_module(module_name)

		# Call the hook
		exec(code, hook_globals)  # pylint: disable=exec-used

		# Retrieve the output message from the hook and print it
		output = hook_globals.get("output", None)

		if output is not None:
			reporter.verbosity0(f"{envconfig.envname} recreate hook: {output}", bold=True)
