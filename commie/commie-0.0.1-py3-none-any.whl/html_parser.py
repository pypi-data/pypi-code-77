# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

"""This module provides methods for parsing comments from HTML family languages.

Works with:
  HTML
  XML
  SGML
"""

import re
from typing import Iterable

from commie import common
from commie.common import Comment


def extract_comments(htmlCode: str) -> Iterable[Comment]:
  """Extracts a list of comments from the given HTML family source code.

  Comments are represented with the Comment class found in the common module.
  HTML family comments come in one form, comprising all text within '<!--' and
  '-->' markers. Comments cannot be nested.

  Args:
    htmlCode: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code..
  Raises:
    common.UnterminatedCommentError: Encountered an unterminated multi-line
      comment.
  """
  pattern = r"""
    (?P<literal> (\"([^\"\n])*\")+) |
    (?P<single> <!--(?P<single_content>.*?)-->) |
    (?P<multi> <!--(?P<multi_content>(.|\n)*?)?-->) |
    (?P<error> <!--(.*)?)
  """
  compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

  for match in compiled.finditer(htmlCode):

    kind = match.lastgroup
    span = match.span(0)

    if kind == "single":
      yield common.Comment(
        match.group("single_content"),
        span[0], span[1],
        multiline=False)
    elif kind == "multi":
      yield common.Comment(
        match.group("multi_content"),
        span[0], span[1],
        multiline=False)
    elif kind == "error":
      raise common.UnterminatedCommentError()
