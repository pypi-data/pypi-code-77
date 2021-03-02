# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest
from typing import List

from .. import iter_comments_js
from ..parsers.common import Comment, UnterminatedCommentError


def commentsToList(code:str) -> List[Comment]:
  return list(iter_comments_js(code))


class JsParserTest(unittest.TestCase):

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)

    self.assertEqual(comments[0].markup_span.extract(code), "// single line comment")
    self.assertEqual(comments[0].text_span.extract(code), " single line comment")
    self.assertEqual(comments[0].multiline, False)

  def testLineCommentInSingleQuotedLiteral(self):
    code = "msg = '// this is not a comment'"
    comments = commentsToList(code)
    self.assertEqual(len(comments), 0)

  def testLineCommentInDoubleQuotedLiteral(self):
    code = 'msg = "// this is not a comment"'
    comments = commentsToList(code)
    self.assertEqual(len(comments), 0)

  def testMultiLineComment(self):
    code = '/* multiline\ncomment */'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)
    self.assertEqual(comments[0].markup_span.extract(code), '/* multiline\ncomment */')
    self.assertEqual(comments[0].text_span.extract(code), " multiline\ncomment ")
    self.assertEqual(comments[0].multiline, True)


  def testMultiLineCommentWithStars(self):
    code = "/***************/"
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)
    self.assertEqual(comments[0].markup_span.extract(code), '/***************/')
    self.assertEqual(comments[0].text_span.extract(code), "*************")
    self.assertEqual(comments[0].multiline, True)

  def testMultiLineCommentInSingleLiteral(self):
    code = "msg = '/* This is not a\\nmultiline comment */'"
    comments = commentsToList(code)
    self.assertEqual(len(comments), 0)

  def testMultiLineCommentInDoubleLiteral(self):
    code = 'msg = "/* This is not a\\nmultiline comment */"'
    comments = commentsToList(code)
    self.assertEqual(len(comments), 0)

  def testMultiLineCommentUnterminated(self):
    code = 'a = 1 /* Unterminated\\n comment'
    with self.assertRaises(UnterminatedCommentError):
      commentsToList(code)

  def testMultiple(self):
    code = """

    /*
     * this is a fancy comment
     * one more line of it
     */

    let forgetIt = prompt("What?");

    // bye!

    """

    comments = commentsToList(code)

    self.assertEqual(len(comments), 2)
    self.assertEqual(comments[0].multiline, True)
    self.assertEqual(comments[1].multiline, False)
