# from pytest import mark
# from progrow.column_calculator import ColumnCalculator
# from progrow.row import Row
# from progrow.style import Style


# @mark.parametrize(
#     "columns, name, expect",
#     [
#         (Columns(), "foo", 3),
#         (Columns(name_width=5), "foo", 5),
#         (Columns(total_width=5), "foo", 3),
#         (Columns(total_width=2), "foo", 2),
#     ],
# )
# def test_name(columns: Columns, name: str, expect: int) -> None:
#     row = Row(name=name, maximum=1.0, current=0.5)
#     column_calculator = ColumnCalculator(columns, row, Style())
#     assert column_calculator.name == expect


# @mark.parametrize(
#     "columns, style, name, expect",
#     [
#         (Columns(total_width=20), Style(), "foo", 16),
#         (Columns(total_width=20), Style(name_post="::"), "foo", 15),
#     ],
# )
# def test_bar(columns: Columns, style: Style, name: str, expect: int) -> None:
#     row = Row(name=name, maximum=1.0, current=0.5)
#     column_calculator = ColumnCalculator(columns, row, style)
#     assert column_calculator.bar == expect


# @mark.parametrize(
#     "columns, row, style, expect",
#     [
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=0), Style(), 0),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=1), Style(), 1),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=2), Style(), 1),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=3), Style(), 2),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=4), Style(), 2),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=5), Style(), 3),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=6), Style(), 4),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=7), Style(), 4),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=8), Style(), 5),
#         (Columns(total_width=10), Row(name="foo", maximum=9, current=9), Style(), 6),
#     ],
# )
# def test_bar_filled(columns: Columns, row: Row, style: Style, expect: int) -> None:
#     column_calculator = ColumnCalculator(columns, row, style)
#     assert column_calculator.bar_filled == expect
