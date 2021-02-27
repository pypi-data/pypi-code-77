from math import isclose

from stram.domain.toolsets.general_toolset import EarlyStopper


def test_early_stopping():
    delta = 0.03
    patience = 5
    stopper = EarlyStopper(delta, patience)

    assert not stopper(1.00)
    assert not stopper(0.90)
    assert not stopper(0.88)
    assert not stopper(0.87)
    assert not stopper(0.86)
    assert stopper.actual_delta is None

    assert not stopper(0.85)
    assert isclose(stopper.actual_delta, 0.15, abs_tol=1e-4)

    assert not stopper(0.85)
    assert isclose(stopper.actual_delta, 0.05555, abs_tol=1e-4)

    assert not stopper(0.85)
    assert isclose(stopper.actual_delta, 0.03409, abs_tol=1e-4)

    assert stopper(0.85)
    assert 'actual_delta=' in stopper.deltas_info()
    assert 'expected_delta=' in stopper.deltas_info()
