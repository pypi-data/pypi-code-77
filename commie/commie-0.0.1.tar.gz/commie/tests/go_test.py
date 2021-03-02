# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest

from commie import go_parser, common
from commie.common import Comment


class GoParserTest(unittest.TestCase):

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = list(go_parser.extract_comments(code))
    expected = [Comment(" single line comment", 0, len(code), False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInRuneLiteral(self):
    code = "msg := '// this is not a comment'"
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testSingleLineCommentInBackTickedLiteral(self):
    code = "msg := `// this is not a comment`"
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testSingleLineCommentInQuotedLiteral(self):
    code = 'msg := "// this is not a comment"'
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '/* multiline\ncomment */'
    comments = list(go_parser.extract_comments(code))
    expected = [Comment(" multiline\ncomment ", 0, 23, True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = "/***************/"
    comments = list(go_parser.extract_comments(code))
    expected = [Comment("*************", 0, 17, True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInRuneLiteral(self):
    code = "msg := '/* This is not a\\nmultiline comment */'"
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentInQuotedLiteral(self):
    code = 'msg := "/* This is not a\\nmultiline comment */"'
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentInBackTickedLiteral(self):
    code = 'msg := `/* This is not a\\nmultiline comment */`'
    comments = list(go_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'a := 1 /* Unterminated\\n comment'
    with self.assertRaises(common.UnterminatedCommentError):
      list(go_parser.extract_comments(code))
