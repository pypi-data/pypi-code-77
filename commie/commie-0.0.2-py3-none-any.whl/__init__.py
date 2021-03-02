from .parsers.c_parser import extract_comments as iter_comments_c
from .parsers.common import Comment, Span, FileError, UnterminatedCommentError
from .parsers.css_parser import extract_comments as iter_comments_css
from .parsers.go_parser import extract_comments as iter_comments_go
from .parsers.html_parser import extract_comments as iter_comments_html
from .parsers.js_parser import extract_comments as iter_comments_js
from .parsers.python_parser import extract_comments as iter_comments_python
from .parsers.ruby_parser import extract_comments as iter_comments_ruby
from .parsers.shell_parser import extract_comments as iter_comments_shell
