#!/usr/bin/env python3
#
#  hooks.py
"""
Built in hooks for ``tox-recreate-hook``.

These are exposed via the ``builtin`` pseudo-module.
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
import shutil

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

__all__ = ["rmdir"]


def rmdir(path: PathLike) -> str:
	r"""
	Remove the given directory and its contents.

	:param path:

	:returns: A message in the format :file:`'removing {<path>}'`

	.. attention::

		On Windows-like systems using ``\`` as a path separator
		you may need to use a *raw string* for the path:

		.. code-block:: ini

			recreate_hook = builtin.rmdir(r"{toxinidir}/doc-source/build")

	"""

	path = PathPlus(path)
	if path.is_dir():
		shutil.rmtree(path)

	return f"removing {path!s}"
