# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import collections
import random
import re




class KeyDefaultDict(collections.defaultdict):
    '''
    Default dict that passes missing keys to the factory function, rather than
    calling the factory function with no arguments.
    '''
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            self[key] = self.default_factory(key)
            return self[key]


def random_ascii_lower_alpha(n):
    '''
    Create a random string of length n consisting of lowercase ASCII
    letters.  Useful for creating more robust tempfile names when working in
    `tempfile.TemporaryDirectory()`.
    '''
    return ''.join(chr(num) for num in (random.randrange(97, 122+1) for _ in range(n)))


def splitlines_lf(string):
    r'''
    Like `str.splitlines()`, but only splits on `\n`.  This should be used
    on strings that have had `\r\n?` normalized to `\n`.  It avoids the
    `str.splitlines()` behavior of splitting on additional code points
    like `\v` and `\f`.
    '''
    lines = string.split('\n')
    if string == '' or string[-1] == '\n':
        lines.pop()
    return lines


_short_unescapes = {
    '\\': '\\',
    "'": "'",
    '"': '"',
    'a': '\a',
    'b': '\b',
    'e': '\x1B',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'v': '\v'
}

_unescape_pattern = r'\\(?:{short}|x{x}|u{u}|u{u_brace}|U{U}|{invalid})'.format(
    short=r'(?P<short>[{0}])'.format(''.join(re.escape(k) for k in _short_unescapes)),
    x=r'(?P<x>[0-9a-fA-F]{2})',
    u=r'(?P<u>[0-9a-fA-F]{4})',
    u_brace=r'\{(?P<u_brace>[0-9a-fA-F]{1,8})\}',
    U=r'(?P<U>[0-9a-fA-F]{8})',
    invalid=r'.?'
)

_unescape_re = re.compile(_unescape_pattern)

def _unescape(match,
              short_unescape_dict=_short_unescapes, chr=chr, int=int):
    lastgroup = match.lastgroup
    if lastgroup == 'invalid':
        raise ValueError
    if lastgroup == 'short':
        return short_unescape_dict[match.group(lastgroup)]
    return chr(int(match.group(lastgroup), 16))

def try_string_literal_to_string(string):
    '''
    Take a string that may represent a string literal, and attempt to extract
    the string literal contents by discarding delimiters and interpreting
    backslash escapes.  If the string does not match the pattern for a string
    literal, then simply return the original string unmodified.
    '''
    if len(string) <= 1 or '\r' in string or '\n' in string:
        return string
    if (string[0] == string[-1] == "'") or (string[0] == string[-1] == '"'):
        try:
            return _unescape_re.sub(_unescape, string[1:-1])
        except Exception:
            return string
    return string
