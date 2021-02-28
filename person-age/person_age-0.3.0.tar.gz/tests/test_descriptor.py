import pytest

from person.descriptor import get_age_description


@pytest.mark.parametrize("test_value,expected_result", [(10, "Dziecko"), (100, "Emeryt")])
def test_should_return_correct_description(test_value, expected_result):
    assert get_age_description(test_value) == expected_result
