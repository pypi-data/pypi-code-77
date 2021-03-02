# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

from typing import NamedTuple


class Error(Exception):
  """Base Error class for all comment parsers."""


class FileError(Error):
  """Raised if there is an issue reading a file."""


class UnterminatedCommentError(Error):
  """Raised if an Unterminated multi-line comment is encountered."""


class Span(NamedTuple):
  start: int
  end: int

  def extract(self, text: str):
    return text[self.start:self.end]


class Comment:
  """Represents comments found in a source code string."""

  def __init__(self, markup_span: Span, text_span: Span, multiline: bool):

    self.markup_span: Span = markup_span
    self.text_span: Span = text_span

    self.multiline = multiline

  def __repr__(self):
    return f"Comment({self.markup_span}, {self.text_span}, {self.multiline})"

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if self.__dict__ == other.__dict__:
        return True
    return False
