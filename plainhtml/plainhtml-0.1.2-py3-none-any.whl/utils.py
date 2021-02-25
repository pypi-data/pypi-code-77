from lxml.html import HtmlElement, HTMLParser, etree

PARSER = HTMLParser(recover=True, encoding="utf8")


def parse_tree(html: str) -> HtmlElement:
    """Parse HTML tree from a string

    Parameters
    ----------
    html : str
        HTML to parse

    Returns
    -------
    HtmlElement
        HTML element object
    """
    body = html.strip().replace("\x00", "").encode("utf8")
    tree = etree.fromstring(body, parser=PARSER)
    if tree is None:
        tree = etree.fromstring(b"<html/>", parser=PARSER)
    return tree
