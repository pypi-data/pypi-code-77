from lxml.html.clean import Cleaner

from plainhtml.dom import DOM
from plainhtml.utils import parse_tree

CLEANER = Cleaner(
    scripts=True,
    javascript=True,
    comments=True,
    style=True,
    links=True,
    meta=True,
    page_structure=False,
    processing_instructions=True,
    embedded=True,
    frames=True,
    forms=True,
    annoying_tags=False,
    remove_unknown_tags=False,
    safe_attrs_only=False,
)


def extract_text(html: str) -> str:
    """Extract plain text from HTML

    Almost the same as the `normalize-space` XPath expression, but this function adds also spaces
    between inline elements (like `<span>`) which are often used as block elements in HTML, and
    adds appropriate newlines to make output better formatted.

    Parameters
    ----------
    html : str
        HTML to extract plain text from

    Returns
    -------
    str
        Plain text
    """
    if not html.strip():
        return ""
    tree = parse_tree(html)
    try:
        clean_tree = CLEANER.clean_html(tree)
    except AssertionError:
        # https://bugs.launchpad.net/lxml/+bug/1838497
        clean_tree = tree
    return DOM(clean_tree).extract_text()
