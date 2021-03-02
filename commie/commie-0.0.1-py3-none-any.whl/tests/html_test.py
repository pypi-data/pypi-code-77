# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest
from commie import html_parser, common
from commie.common import Comment


class ShellParserTest(unittest.TestCase):

  def testComment(self):
    code = '<!--comment-->'
    comments = list(html_parser.extract_comments(code))
    expected = [Comment("comment", 0, 14, False)]
    self.assertEqual(comments, expected)

    c = comments[0]
    self.assertEqual(code[c.start:c.end + 1], code)

  def testMultilineComment(self):
    code = '<!--multi-line\ncomment-->'
    comments = list(html_parser.extract_comments(code))

    expected = [Comment("multi-line\ncomment", 0, 25, False)]
    self.assertEqual(comments, expected)

  def testTwoSeparateSingleComment(self):
    code = '<!--comment1-->\n<!--comment2-->'
    comments = list(html_parser.extract_comments(code))
    expected = [
      Comment("comment1", 0, 15, False),
      Comment("comment2", 16, 31, False)
    ]
    self.assertEqual(comments, expected)

  def testLayeredComment(self):
    code = '<!-- comment<!-- -->'
    comments = list(html_parser.extract_comments(code))
    expected = [Comment(" comment<!-- ", 0, 20, False)]
    self.assertEqual(comments, expected)

  def testNonGreedyComment(self):
    code = '<!--i am a comment--> not a comment -->'
    comments = list(html_parser.extract_comments(code))
    expected = [Comment("i am a comment", 0, 21, False)]
    self.assertEqual(comments, expected)

  def testSideBySideComment(self):
    code = '<!--comment1--> ... <!--comment2-->'
    comments = list(html_parser.extract_comments(code))
    expected = [Comment("comment1", 0, 15, False), Comment("comment2", 20, 35, False)]
    self.assertEqual(comments, expected)

  def testUnterminatedComment(self):
    code = '<!--invalid'
    with self.assertRaises(common.UnterminatedCommentError):
      list(html_parser.extract_comments(code))

  def testLonelyTerminator(self):
    code = 'not a comment-->'
    comments = list(html_parser.extract_comments(code))
    self.assertEqual(comments, [])
