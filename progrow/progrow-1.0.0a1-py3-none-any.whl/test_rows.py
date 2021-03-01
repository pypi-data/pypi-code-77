from typing import List

from pytest import mark

from progrow.row import Row
from progrow.rows import Rows
from progrow.style import Style


@mark.parametrize(
    "rows, style, expect",
    [
        (
            Rows(
                [
                    Row(name="red", maximum=9, current=1),
                    Row(name="yellow", maximum=9, current=2),
                    Row(name="green", maximum=9, current=3),
                ]
            ),
            Style(color=False, width=40),
            [
                "red    ███▋",
                "yellow ███████▍",
                "green  ██████████▉",
            ],
        ),
        (
            Rows(
                [
                    Row(name="brown", maximum=9, current=4),
                    Row(name="scarlet", maximum=19, current=15),
                    Row(name="black", maximum=119, current=116),
                ]
            ),
            Style(color=False, show_fraction=True, width=40),
            [
                "brown   █████████▊               4 /   9",
                "scarlet █████████████████▍      15 /  19",
                "black   █████████████████████▌ 116 / 119",
            ],
        ),
        (
            Rows(
                [
                    Row(name="ochre", maximum=9, current=7),
                    Row(name="peach", maximum=9, current=8),
                    Row(name="ruby", maximum=9, current=9),
                ]
            ),
            Style(color=False, show_percent=True, width=40),
            [
                "ochre ██████████████████████▌        77%",
                "peach █████████████████████████▊     88%",
                "ruby  █████████████████████████████ 100%",
            ],
        ),
        (
            Rows(
                [
                    Row(name="olive", maximum=9, current=7),
                    Row(name="violet", maximum=9, current=8),
                    Row(name="fawn", maximum=9, current=9),
                ]
            ),
            Style(color=False, show_fraction=True, show_percent=True, width=40),
            [
                "olive  ███████████████▌     7 / 9 •  77%",
                "violet █████████████████▊   8 / 9 •  88%",
                "fawn   ███████████████████▉ 9 / 9 • 100%",
            ],
        ),
    ],
)
def test_to_string(rows: Rows, style: Style, expect: List[str]) -> None:
    assert rows.render(style) == "\n".join(expect) + "\n"
