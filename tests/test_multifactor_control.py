import numpy as np
from src.multifactor_control import generate,prepare,feature,run

def test_shapes_and_target_equality():
    r=prepare(generate(20270000,0,.5,.5))
    assert len(r)==5 and r[0].shape==(32,240)
    ys=[feature(r,m)[1] for m in ('own','mean','pc1','pc2','pc2_mean')]
    assert len(ys[0])==32*180
    for y in ys[1:]:np.testing.assert_array_equal(y,ys[0])

def test_reproducible_and_means():
    np.testing.assert_array_equal(generate(20270000,0,.5,.5),generate(20270000,0,.5,.5))
    r=run();assert len(r['scenarios'])==5
    for c in r['scenarios'].values():
        assert len(c['heldout'])==8
        for k,v in c['mean_gains'].items():
            assert abs(v-np.mean([row[k] for row in c['heldout']]))<1e-12
