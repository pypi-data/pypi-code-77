from pytest import mark

from progrow.row import Row


@mark.parametrize(
    "maximum, current, expect",
    [
        (50, 25, "50%"),
        (3, 2, "66%"),
    ],
)
def test_human_percent(maximum: float, current: float, expect: str) -> None:
    assert Row("foo", maximum=maximum, current=current).human_percent == expect


@mark.parametrize(
    "maximum, current, expect",
    [
        (50, 25, 0.5),
        (3, 2, 0.6666666666666666),
    ],
)
def test_percent(maximum: float, current: float, expect: float) -> None:
    assert Row("foo", maximum=maximum, current=current).percent == expect
