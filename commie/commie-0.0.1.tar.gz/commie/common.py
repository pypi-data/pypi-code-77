# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT


class Error(Exception):
  """Base Error class for all comment parsers."""


class FileError(Error):
  """Raised if there is an issue reading a given file."""


class UnterminatedCommentError(Error):
  """Raised if an Unterminated multi-line comment is encountered."""


class Comment:
  """Represents comments found in a source code string."""

  def __init__(self, text: str, start: int, end: int, multiline: bool):

    self.text = text
    self.start = start
    self.end = end
    self.multiline = multiline

  def __str__(self):
    return self.text

  def __repr__(self):
    return f"Comment(\"{self.text}\", {self.start}, {self.end}, {self.multiline})"

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if self.__dict__ == other.__dict__:
        return True
    return False