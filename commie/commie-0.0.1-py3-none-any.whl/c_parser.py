# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

"""This module provides methods for parsing comments from C family languages.

Works with:
  C99+
  C++
  Objective-C
  Java

"""

# AG: Hmm... Is it really different from JS parser?..

import re
from typing import Iterable

from commie import common
from commie.common import Comment


def extract_comments(code:str) -> Iterable[Comment]:
  """Extracts a list of comments from the given C family source code.

  Comments are represented with the Comment class found in the common module.
  C family comments come in two forms, single and multi-line comments.
    - Single-line comments begin with '//' and continue to the end of line.
    - Multi-line comments begin with '/*' and end with '*/' and can span
      multiple lines of code. If a multi-line comment does not terminate
      before EOF is reached, then an exception is raised.

  Note that this doesn't take language-specific preprocessor directives into
  consideration.

  Args:
    code: String containing code to extract comments from.
  Returns:
    Python list of common.Comment in the order that they appear in the code.
  Raises:
    common.UnterminatedCommentError: Encountered an unterminated multi-line
      comment.
  """
  pattern = r"""
    (?P<literal> (\"([^\"\n])*\")+) |
    (?P<single> //(?P<single_content>.*)?$) |
    (?P<multi> /\*(?P<multi_content>(.|\n)*?)?\*/) |
    (?P<error> /\*(.*)?)
  """

  compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

  for match in compiled.finditer(code):

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
        multiline=True)
    elif kind == "error":
      raise common.UnterminatedCommentError()
  #
  #   start_character = match.start()
  #   line_no = bisect_left(lines_indexes, start_character)
  #
  #   if kind == "single":
  #     comment_content = match.group("single_content")
  #     comment = common.Comment(comment_content, line_no + 1)
  #     comments.append(comment)
  #   elif kind == "multi":
  #     comment_content = match.group("multi_content")
  #     comment = common.Comment(comment_content, line_no + 1, multiline=True)
  #     comments.append(comment)
  #   elif kind == "error":
  #     raise common.UnterminatedCommentError()
  #
  # return comments
