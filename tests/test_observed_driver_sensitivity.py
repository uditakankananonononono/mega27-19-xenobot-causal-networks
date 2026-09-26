import numpy as np
from src.observed_driver_sensitivity import generate_with_driver,features,run
from src.synthetic_calibration import generate

def test_generator_x_identity():
    a,u=generate_with_driver(7,0,.5)
    np.testing.assert_array_equal(a,generate(7,0,.5))
    assert u.shape==(240,)

def test_feature_shape_and_target():
    a,u=generate_with_driver(9,.25,0)
    x,y=features(a,u,True)
    assert x.shape==(64*239,4)
    np.testing.assert_array_equal(y,a[:,1:].ravel())
    np.testing.assert_array_equal(x[:,2],np.tile(u[:-1],64))

def test_summary_recomputed():
    r=run()
    for s in r['scenarios'].values():
        assert len(s['heldout'])==8
        assert abs(s['mean_gain']-np.mean([x['relative_gain'] for x in s['heldout']]))<1e-12
