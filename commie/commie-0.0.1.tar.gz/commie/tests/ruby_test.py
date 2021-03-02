# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT


import unittest
from commie import ruby_parser
from commie.common import Comment


class ShellParserTest(unittest.TestCase):

  def testComment(self):
    code = '# comment'
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(" comment", 0, len(code), False)]
    self.assertEqual(comments, expected)
    self.assertEqual(code[comments[0].end-1], 't')

  def testCommentInSingleQuotedString(self):
    code = "'this is # not a comment'"
    comments = list(ruby_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testCommentInDoubleQuotedString(self):
    code = '"this is # not a comment"'
    comments = list(ruby_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testNestedStringSingleOutside(self):
    code = "'this is \"# not a comment\"'"
    comments = list(ruby_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testNestedStringDoubleOutside(self):
    code = '"this is \'# not a comment\'"'
    comments = list(ruby_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testEscapedSingleQuote(self):
    code = "\\'# this is a comment"
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(" this is a comment", 2, 21, False)]
    self.assertEqual(comments, expected)

  def testEscapedDoubleQuote(self):
    code = '\\"# this is a comment'
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(" this is a comment", 2, 21, False)]
    self.assertEqual(comments, expected)

  def testDoubleComment(self):
    code = '# this is not # another comment'
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(" this is not # another comment", 0, 31, False)]
    self.assertEqual(comments, expected)

  def testLiteralsSeparatedByComment(self):
    code = r"'This is' # 'a comment'"
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(" 'a comment'", 10, 23, False)]
    self.assertEqual(comments, expected)

  def testDifferentLiteralsSeparatedByComment(self):
    code = r''''This is' # "a comment"'''
    comments = list(ruby_parser.extract_comments(code))
    expected = [Comment(' "a comment"', 10, 23, False)]
    self.assertEqual(comments, expected)
