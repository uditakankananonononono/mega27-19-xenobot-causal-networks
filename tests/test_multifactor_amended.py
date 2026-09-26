import numpy as np
from src.multifactor_control_amended import generate,prepare,feature,run

def test_sensor_latent_rank_and_target_equality():
    b=np.ones(64);b[16:32]=-1;b[48:]=-1
    assert np.linalg.matrix_rank(np.stack((np.ones(32),b[:32]),axis=1))==2
    r=prepare(generate(20270000,0,.5,.5))
    ys=[feature(r,m)[1] for m in ('own','mean','pc1','pc2','pc2_mean')]
    for y in ys[1:]:np.testing.assert_array_equal(y,ys[0])

def test_amended_summary():
    r=run()
    for c in r['scenarios'].values():
        assert len(c['heldout'])==8
        for key,val in c['mean_gains'].items():
            assert abs(val-np.mean([row[key] for row in c['heldout']]))<1e-12
