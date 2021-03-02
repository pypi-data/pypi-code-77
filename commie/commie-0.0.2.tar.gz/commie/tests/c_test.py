# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest
from typing import List

from .. import iter_comments_c
from ..parsers.common import Comment, UnterminatedCommentError


def commentsToList(code:str) -> List[Comment]:
  return list(iter_comments_c(code))


class CParserTest(unittest.TestCase):

  def testSimpleMain(self):
    code = "// this is a comment\nint main() {\nreturn 0;\n}\n"
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)

    self.assertEqual(comments[0].markup_span.extract(code), "// this is a comment")
    self.assertEqual(comments[0].text_span.extract(code), " this is a comment")
    self.assertEqual(comments[0].multiline, False)

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)

    self.assertEqual(comments[0].markup_span.extract(code), '// single line comment')
    self.assertEqual(comments[0].text_span.extract(code), " single line comment")
    self.assertEqual(comments[0].multiline, False)

  def testSingleLineCommentInStringLiteral(self):
    code = 'char* msg = "// this is not a comment"'
    comments = commentsToList(code)
    self.assertEqual(comments, [])

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

  def testMultiLineCommentInStringLiteral(self):
    code = 'char* msg = "/* This is not a\\nmultiline comment */"'
    comments = commentsToList(code)
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'int a = 1; /* Unterminated\\n comment'
    with self.assertRaises(UnterminatedCommentError):
      commentsToList(code)

  def testMultipleMultilineComments(self):
    code = '/* abc */ /* 123 */'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 2)

    self.assertEqual(comments[0].markup_span.extract(code), '/* abc */')
    self.assertEqual(comments[0].text_span.extract(code), " abc ")
    self.assertEqual(comments[0].multiline, True)

    self.assertEqual(comments[1].markup_span.extract(code), '/* 123 */')
    self.assertEqual(comments[1].text_span.extract(code), " 123 ")
    self.assertEqual(comments[1].multiline, True)


  def testStringThenComment(self):
    code = r'"" /* "abc */'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)

    self.assertEqual(comments[0].markup_span.extract(code), '/* "abc */')
    self.assertEqual(comments[0].text_span.extract(code), ' "abc ')
    self.assertEqual(comments[0].multiline, True)


  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    # TODO(#27): Re-enable test.
    # code = r'" \" /* \" "'
    # comments = c_parser.extract_comments(code)
    # self.assertEqual(comments, [])
    pass


  def testStringEscapedBackslashCharacter(self):
    code = r'"\\"'
    comments = commentsToList(code)
    self.assertEqual(comments, [])

  def testTwoStringsFollowedByComment(self):
    code = r'"""" // foo'
    comments = commentsToList(code)

    self.assertEqual(len(comments), 1)

    self.assertEqual(comments[0].markup_span.extract(code), '// foo')
    self.assertEqual(comments[0].text_span.extract(code), " foo")
    self.assertEqual(comments[0].multiline, False)

  def testCommentedMultilineComment(self):
    code = '''// What if i start a /* here
    int main(){return 0;}
    // and ended it here */'''

    comments = commentsToList(code)

    self.assertEqual(len(comments), 2)

    self.assertEqual(comments[0].markup_span.extract(code), '// What if i start a /* here')
    self.assertEqual(comments[0].text_span.extract(code), " What if i start a /* here")
    self.assertEqual(comments[0].multiline, False)

    self.assertEqual(comments[1].markup_span.extract(code), '// and ended it here */')
    self.assertEqual(comments[1].text_span.extract(code), " and ended it here */")
    self.assertEqual(comments[1].multiline, False)


  def testMultilineCommentedComment(self):
    code = '''/*// here
    int main(){return 0;}
    */// and ended it here */'''
    comments = commentsToList(code)

    self.assertEqual(len(comments), 2)

    self.assertEqual(comments[0].markup_span.extract(code), "/*// here\n    int main(){return 0;}\n    */")
    self.assertEqual(comments[0].text_span.extract(code), "// here\n    int main(){return 0;}\n    ")
    self.assertEqual(comments[0].multiline, True)

    self.assertEqual(comments[1].markup_span.extract(code), '// and ended it here */')
    self.assertEqual(comments[1].text_span.extract(code), " and ended it here */")
    self.assertEqual(comments[1].multiline, False)
