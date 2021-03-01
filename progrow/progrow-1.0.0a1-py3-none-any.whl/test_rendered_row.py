from pytest import mark

from progrow.layout import Layout
from progrow.rendered_row import RenderedRow
from progrow.row import Row
from progrow.style import Style


@mark.parametrize(
    "row, style, expect",
    [
        (Row(name="foo", maximum=9, current=0), Style(color=False, width=10), "foo"),
        (Row(name="foo", maximum=9, current=1), Style(color=False, width=10), "foo ▋"),
        (Row(name="foo", maximum=9, current=2), Style(color=False, width=10), "foo █▍"),
        (Row(name="foo", maximum=9, current=3), Style(color=False, width=10), "foo ██"),
        (
            Row(name="foo", maximum=9, current=4),
            Style(color=False, width=10),
            "foo ██▋",
        ),
        (
            Row(name="foo", maximum=9, current=5),
            Style(color=False, width=10),
            "foo ███▍",
        ),
        (
            Row(name="foo", maximum=9, current=6),
            Style(color=False, width=10),
            "foo ████▏",
        ),
        (
            Row(name="foo", maximum=9, current=7),
            Style(color=False, width=10),
            "foo ████▋",
        ),
        (
            Row(name="foo", maximum=9, current=8),
            Style(color=False, width=10),
            "foo █████▍",
        ),
        (
            Row(name="foo", maximum=9, current=9),
            Style(color=False, width=10),
            "foo ██████",
        ),
        (
            Row(name="foo", maximum=9, current=3),
            Style(color=False, post_name=": ", width=10),
            "foo: █▋",
        ),
        (
            Row(name="foo", maximum=9, current=3),
            Style(color=False, show_fraction=True, width=30),
            "foo ██████▋              3 / 9",
        ),
        (
            Row(name="foo", maximum=9, current=3),
            Style(color=False, show_percent=True, width=30),
            "foo ███████▍               33%",
        ),
        (
            Row(name="foo", maximum=9, current=3),
            Style(color=False, show_fraction=True, show_percent=True, width=30),
            "foo ████▋          3 / 9 • 33%",
        ),
    ],
)
def test_to_string(row: Row, style: Style, expect: str) -> None:
    layout = Layout([row])
    assert str(RenderedRow(layout, row, style)) == expect
