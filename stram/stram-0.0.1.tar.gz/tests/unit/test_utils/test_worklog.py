import logging

from stram.utils.worklog import Worklog


def test_all_worklog_operations(
    tmpdir, caplog, content_image, style_image, content_image_hash, style_image_hash
):
    worklog = Worklog.new(content_image, style_image)
    work_units = dict(
        unit_hash_1=dict(method='A', strength=0.25),
        unit_hash_2=dict(method='B', strength=0.45),
    )
    for unit_hash, unit_config in work_units.items():
        worklog.add_work_unit(unit_hash, unit_config)

    assert worklog.content_hash == content_image_hash
    assert worklog.style_hash == style_image_hash
    assert worklog.table == work_units

    worklog_filepath = tmpdir.mkdir('test_worklog').join('test_worklog.json')
    worklog.save_to_filepath(worklog_filepath)
    loaded_worklog = Worklog.from_file(worklog_filepath)

    assert loaded_worklog == worklog

    with caplog.at_level(logging.WARNING):
        loaded_worklog.add_work_unit('unit_hash_2', dict(method='C', strength=0))
    assert 'Overwriting unit of work in the worklog' in caplog.text
