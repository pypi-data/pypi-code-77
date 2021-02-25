import re
from typing import Optional, Union

from lxml.html import HtmlElement

# pre-compiled regular expressions
WHITESPACE_PATTERN = re.compile(r"\s+")
TRAILING_WHITESPACE_PATTERN = re.compile(r"\s$")
PUNCT_AFTER_PATTERN = re.compile(r'^[,:;.!?")]')
OPEN_BRACKET_BEFORE_PATTERN = re.compile(r"\($")


class _Newline:
    pass


class _DoubleNewline:
    pass


class DOM:
    def __init__(self, tree: HtmlElement):
        self.tree = tree
        self.lines = []
        self._newline = _Newline()
        self._double_newline = _DoubleNewline()
        self._previous_line = self._double_newline
        self._newline_tags = {
            "article",
            "aside",
            "br",
            "dd",
            "details",
            "div",
            "dt",
            "fieldset",
            "figcaption",
            "footer",
            "form",
            "header",
            "hr",
            "legend",
            "li",
            "main",
            "nav",
            "table",
            "tr",
        }
        self._double_newline_tags = {
            "blockquote",
            "dl",
            "figure",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ol",
            "p",
            "pre",
            "title",
            "ul",
        }

    def extract_text(self) -> str:
        """Extract plain text from the DOM

        Returns
        -------
        str
            Plain text
        """
        self._traverse_text_fragments(self.tree, handle_tail=False)
        return "".join(self.lines).replace("\r", "\n").strip()

    def _add_space(self, text: str, previous: Union[_Newline, _DoubleNewline, str]) -> bool:
        """Whether to add whitespace to the text or not

        Parameters
        ----------
        text : str
            Text to add space to (or not)
        previous : Union[_Newline, _DoubleNewline, str]
            Previous element

        Returns
        -------
        bool
            True if add whitespace, False otherwise
        """
        if previous == self._newline or previous == self._double_newline:
            return False
        elif not self._has_trailing_whitespace(previous):
            if self._has_punct_after(text) or self._has_open_bracket_before(previous):
                return False
        return True

    def _get_space_between(self, text: str, previous: Union[_Newline, _DoubleNewline, str]) -> str:
        """Get space between the previous and current element

        Parameters
        ----------
        text : str
            Current element text
        previous : Union[_Newline, _DoubleNewline, str]
            Previous element

        Returns
        -------
        str
            Space between two elements
        """
        if not text:
            return " "
        return " " if self._add_space(text, previous) else ""

    def _add_newlines(self, tag: str):
        """Add newlines to the parsed lines

        Parameters
        ----------
        tag : str
            Current tag
        """
        if self._previous_line != self._double_newline:
            if tag in self._double_newline_tags:
                self._previous_line = self._double_newline
                self.lines.append("\n" if self._previous_line == self._newline else "\n\n")
            elif tag in self._newline_tags:
                if self._previous_line != self._newline:
                    self.lines.append("\n")
                self._previous_line = self._newline

    def _add_text(self, text: Optional[str]):
        """Add text to parsed lines

        Parameters
        ----------
        text : Optional[str]
            Text to add
        """
        text_ = self._normalize_whitespace(text) if text else ""
        if text_:
            if space := self._get_space_between(text_, self._previous_line):
                self.lines[-1] = self.lines[-1] + space + text
            else:
                self.lines.append(text_)
            self._previous_line = text

    def _traverse_text_fragments(self, tree: HtmlElement, handle_tail: bool = True):
        """Traverse all text fragments

        Parameters
        ----------
        tree : HtmlElement
            DOM tree
        handle_tail : bool, optional
            If Ture, add text of the tail, by default True
        """
        self._add_newlines(tree.tag)
        self._add_text(tree.text)
        for child in tree:
            self._traverse_text_fragments(child)
        self._add_newlines(tree.tag)
        if handle_tail:
            self._add_text(tree.tail)

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """Noramlize all whitespaces

        Parameters
        ----------
        text : str
            Text to normalize

        Returns
        -------
        str
            Normalized text
        """
        return WHITESPACE_PATTERN.sub(" ", text.strip())

    @staticmethod
    def _has_trailing_whitespace(text: str) -> bool:
        """Check if text has trailing whitespace

        Parameters
        ----------
        text : str
            Text to check

        Returns
        -------
        bool
            True if text has trailing whitespace, False otherwise
        """
        if TRAILING_WHITESPACE_PATTERN.search(text):
            return True
        else:
            return False

    @staticmethod
    def _has_punct_after(text: str) -> bool:
        """Check if text has punctuation at the end

        Parameters
        ----------
        text : str
            Text to check

        Returns
        -------
        bool
            True if text has punctuation at the end, False otherwise
        """
        if PUNCT_AFTER_PATTERN.search(text):
            return True
        else:
            return False

    @staticmethod
    def _has_open_bracket_before(text: str) -> bool:
        """Check if text has open bracket at the beginning

        Parameters
        ----------
        text : str
            Text to check

        Returns
        -------
        bool
            True if text has open bracket at the beginning, False otherwise
        """
        if OPEN_BRACKET_BEFORE_PATTERN.search(text):
            return True
        else:
            return False
