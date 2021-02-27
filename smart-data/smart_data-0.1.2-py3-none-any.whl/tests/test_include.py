from smart_data import include

expected = {
    'foo': 1.1,
    'bar': [42, {'baz': 2}],
    'zoo': None,
    'zar': [[1, 3], [5, 8]],
}


def test_is_equal():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
        'zaz': 2.2,  # additional key will be ignored
    }
    assert include(got, expected) == []


def test_different_types():
    got = {
        'foo': 1.1,
        'bar': {},
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<type diff>']


def test_lack_of_zoo_key():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}],
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/<lack of zoo>']


def test_longer_list():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}, 4],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<list length diff>']


def test_shorter_list():
    got = {
        'foo': 1.1,
        'bar': [42],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<list length diff>']


def test_different_values():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 43}],
        'zoo': None,
        'zar': [[10, 3], [50, 8]],
    }
    assert include(got, expected) == ['/bar/1/baz/<43 vs 2>', '/zar/0/0/<10 vs 1>', '/zar/1/0/<50 vs 5>']


# Try to test structures with objects:
class Foo:
    def __init__(self, bar):
        self.bar = bar

    def __str__(self):
        return str(self.bar)

    def __eq__(self, other):
        if self.bar == other.bar:
            return True
        else:
            return False


def test_equal_objects():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': []
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': []
    }
    assert include(got_with_obj, expected_with_obj) == []


def test_different_objects():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': []
    }

    got_with_obj = {
        'foo': Foo(2),
        'bar': []
    }
    assert include(got_with_obj, expected_with_obj) == ['/foo/<2 vs 1>']


# pytest -vv
# pytest --cov=smart_data tests/ 
