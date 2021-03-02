# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest
from commie import js_parser, common
from commie.common import Comment


class JsParserTest(unittest.TestCase):

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = list(js_parser.extract_comments(code))

    expected = [Comment(" single line comment", 0, len(code), False)]
    self.assertEqual(comments, expected)

  def testLineCommentInSingleQuotedLiteral(self):
    code = "msg = '// this is not a comment'"
    comments = list(js_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testLineCommentInDoubleQuotedLiteral(self):
    code = 'msg = "// this is not a comment"'
    comments = list(js_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '/* multiline\ncomment */'
    comments = list(js_parser.extract_comments(code))

    expected = [Comment(" multiline\ncomment ", 0, 23, True)]

    first = comments[0]
    self.assertEqual(code[first.start:first.end + 1], code)

    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = "/***************/"
    comments = list(js_parser.extract_comments(code))
    expected = [Comment("*************", 0, 17, True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInSingleLiteral(self):
    code = "msg = '/* This is not a\\nmultiline comment */'"
    comments = list(js_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentInDoubleLiteral(self):
    code = 'msg = "/* This is not a\\nmultiline comment */"'
    comments = list(js_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'a = 1 /* Unterminated\\n comment'
    with self.assertRaises(common.UnterminatedCommentError):
      comments = list(js_parser.extract_comments(code))

  def testMultiple(self):
    code = """

    /* 
     * this is a fancy comment
     * one more line of it
     */

    let forgetIt = prompt("What?");

    // bye!

    """

    comments = list(js_parser.extract_comments(code))

    self.assertEqual(comments[0].start, 6)
    self.assertEqual(comments[0].end, 75)
    self.assertEqual(comments[0].multiline, True)

    c = comments[0]
    txt = code[c.start:c.end]
    self.assertEqual(txt[0],"/")
    self.assertEqual(txt[-1],"/")

    self.assertEqual(comments[1].start, 118)
    self.assertEqual(comments[1].end, 126)
    self.assertEqual(comments[1].multiline, False)
