import numpy as np
from src.imperfect_proxy_sensitivity import sample,run
from src.synthetic_calibration import generate

def test_identity_and_proxy_variation():
    x,z=sample(20260926,0,0,0,0)
    np.testing.assert_array_equal(x,generate(20260926,0,0));assert not z.any()
    x1,p1=sample(20260926,0,0,0,2)
    x2,p2=sample(20260926,0,0,0,2)
    np.testing.assert_array_equal(x1,x2);np.testing.assert_array_equal(p1,p2)
    assert not np.array_equal(z,p1)

def test_summary():
    r=run()
    assert len(r['scenarios'])==3
    for case in r['scenarios'].values():
        assert len(case['proxy_levels'])==4
        for level in case['proxy_levels'].values():
            assert len(level['heldout'])==8
            assert abs(level['mean_relative_gain']-np.mean([x['relative_gain'] for x in level['heldout']]))<1e-12
