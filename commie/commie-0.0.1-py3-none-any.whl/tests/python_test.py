# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest
from commie import python_parser
from commie.common import Comment


class PythonParserTest(unittest.TestCase):

  def testComment(self):
    code = '# comment'
    comments = list(python_parser.extract_comments(code))
    expected = [Comment(" comment", 0, len(code), False)]
    self.assertEqual(comments, expected)

  def testCommentInSingleQuotedString(self):
    code = "'this is # not a comment'"
    comments = list(python_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testCommentInDoubleQuotedString(self):
    code = '"this is # not a comment"'
    comments = list(python_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testNestedStringSingleOutside(self):
    code = "'this is \"# not a comment\"'"
    comments = list(python_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testNestedStringDoubleOutside(self):
    code = '"this is \'# not a comment\'"'
    comments = list(python_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testEscapedSingleQuote(self):
    code = "\\'# this is a comment"
    comments = list(python_parser.extract_comments(code))
    expected = [Comment(" this is a comment", 2, len(code), False)]
    self.assertEqual(comments, expected)

    c = comments[0]
    self.assertEqual(code[c.start:c.end+1], "# this is a comment")

  def testEscapedDoubleQuote(self):
    code = '\\"# this is another comment'
    comments = list(python_parser.extract_comments(code))
    expected = [Comment(" this is another comment", 2, len(code), False)]
    self.assertEqual(comments, expected)
