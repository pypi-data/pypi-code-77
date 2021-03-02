# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

from typing import NamedTuple, Optional


class Error(Exception):
  """Base Error class for all comment parsers."""


class FileError(Error):
  """Raised if there is an issue reading a file."""


class UnterminatedCommentError(Error):
  """Raised if an Unterminated multi-line comment is encountered."""

class FormatUndetectedError(Error):
  """Raised if there is an issue reading a file."""



class Span(NamedTuple):
  start: int
  end: int

  def extract(self, text: str):
    return text[self.start:self.end]


class Comment:
  """Represents comments found in a source code string."""

  def __init__(self, source:str, code_span: Span, text_span: Span, multiline: bool):

    self.source = source
    self.code_span: Span = code_span
    self.text_span: Span = text_span
    self.multiline = multiline

    self._text:Optional[str] = None
    self._markup:Optional[str] = None

  @property
  def text(self) -> str:
    if self._text is None:
      self._text = self.text_span.extract(self.source)
    return self._text

  @property
  def code(self) -> str:
    if self._text is None:
      self._text = self.code_span.extract(self.source)
    return self._text

  def __repr__(self):
    return f"Comment({self.code_span}, {self.text_span}, {self.multiline})"

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if self.__dict__ == other.__dict__:
        return True
    return False

