import numpy as np
from src.synthetic_calibration import generate,run

def test_reproducible_and_finite():
    a=generate(7,.25,0)
    np.testing.assert_array_equal(a,generate(7,.25,0))
    assert a.shape==(64,240) and np.isfinite(a).all()

def test_independent_conditions():
    assert not np.array_equal(generate(7,.25,0),generate(7,0,.5))

def test_all_scenarios_reported():
    r=run()
    assert set(r['scenarios'])=={'null','coupling','shared_drive'}
    assert all(len(v['heldout'])==8 for v in r['scenarios'].values())
