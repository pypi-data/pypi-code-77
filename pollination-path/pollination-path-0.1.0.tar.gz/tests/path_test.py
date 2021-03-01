from pollination.path.copy import Copy
from queenbee.plugin.function import Function


def test_copy():
    function = Copy().queenbee
    assert function.name == 'copy'
    assert isinstance(function, Function)
