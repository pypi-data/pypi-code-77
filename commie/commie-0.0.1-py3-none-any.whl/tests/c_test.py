# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: MIT

import unittest

from commie import common, c_parser
from commie.common import Comment


class CParserTest(unittest.TestCase):

  def testSimpleMain(self):
    code = "// this is a comment\nint main() {\nreturn 0;\n}\n"
    comments = list(c_parser.extract_comments(code))
    expected = [Comment(" this is a comment", 0, 20, False)]
    self.assertEqual(comments, expected)

  def testSingleLineComment(self):
    code = '// single line comment'
    comments = list(c_parser.extract_comments(code))
    expected = [Comment(" single line comment", 0, 22, False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInStringLiteral(self):
    code = 'char* msg = "// this is not a comment"'
    comments = list(c_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '/* multiline\ncomment */'
    comments = list(c_parser.extract_comments(code))
    expected = [Comment(" multiline\ncomment ", 0, 23, True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = "/***************/"
    comments = list(c_parser.extract_comments(code))
    expected = [Comment("*************", 0, 17, True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInStringLiteral(self):
    code = 'char* msg = "/* This is not a\\nmultiline comment */"'
    comments = list(c_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'int a = 1; /* Unterminated\\n comment'
    with self.assertRaises(common.UnterminatedCommentError):
      list(c_parser.extract_comments(code))

  def testMultipleMultilineComments(self):
    code = '/* abc */ /* 123 */'
    comments = list(c_parser.extract_comments(code))
    expected = [Comment(" abc ", 0, 9, True), Comment(" 123 ", 10, 19, True)]
    self.assertEqual(comments, expected)

  def testStringThenComment(self):
    code = r'"" /* "abc */'
    comments = list(c_parser.extract_comments(code))
    expected = [Comment(' "abc ', 3, 13, True)]
    self.assertEqual(comments, expected)

  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    # TODO(#27): Re-enable test.
    # code = r'" \" /* \" "'
    # comments = c_parser.extract_comments(code)
    # self.assertEqual(comments, [])
    pass

  def testStringEscapedBackslashCharacter(self):
    code = r'"\\"'
    comments = list(c_parser.extract_comments(code))
    self.assertEqual(comments, [])

  def testTwoStringsFollowedByComment(self):
    code = r'"""" // foo'
    comments = list(c_parser.extract_comments(code))
    self.assertEqual(comments, [Comment(" foo", 5, 11, False)])

  def testCommentedMultilineComment(self):
    code = '''// What if i start a /* here
    int main(){return 0;}
    // and ended it here */'''

    comments = list(c_parser.extract_comments(code))
    expected = [Comment(" What if i start a /* here", 0, 28, False),
                Comment(" and ended it here */", 59, 82, False)]
    self.assertEqual(comments, expected)

  def testMultilineCommentedComment(self):
    code = '''/*// here
    int main(){return 0;}
    */// and ended it here */'''
    comments = list(c_parser.extract_comments(code))
    expected = [Comment("// here\n    int main(){return 0;}\n    ", 0, 42, True),
                Comment(" and ended it here */", 42, 65, False)]
    self.assertEqual(comments, expected)
