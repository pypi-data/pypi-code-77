from os.path import join, isfile

from stram.utils.json_processing import (
    dict2json,
    dict2namespace,
    json2dict,
    json2namespace,
)


def test_all_json_processing_functions(tmpdir):
    test_dict = dict(a=1, b=2, c=3)
    test_json_path = join(tmpdir, 'test.json')

    test_namespace = dict2namespace(test_dict)
    assert test_namespace.a == 1
    assert test_namespace.b == 2
    assert test_namespace.c == 3

    dict2json(test_dict, test_json_path)
    assert isfile(test_json_path)

    test_dict_2 = json2dict(test_json_path)
    assert test_dict == test_dict_2

    test_namespace_2 = json2namespace(test_json_path)
    assert test_namespace == test_namespace_2
