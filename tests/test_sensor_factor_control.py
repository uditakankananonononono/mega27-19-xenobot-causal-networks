import numpy as np
from src.sensor_factor_control import make,xy,run

def test_targets_identical_all_models():
    r=make(123,0,.5)
    ys=[xy(r,m)[1] for m in ('own','mean','pc1','both')]
    assert len(ys[0])==32*180
    for y in ys[1:]:np.testing.assert_array_equal(y,ys[0])

def test_round12_summary():
    r=run()
    assert len(r['scenarios'])==3
    for c in r['scenarios'].values():
        assert len(c['heldout'])==8
        for k,v in c['means'].items():
            assert abs(v-np.mean([row[k] for row in c['heldout']]))<1e-12
