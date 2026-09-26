import numpy as np
from src.organoid_prospective import calibrated,feature,run

def test_scaler_no_future_leak():
    a=np.arange(120,dtype=float).reshape(3,40)
    z,cut=calibrated(a)
    b=a.copy();b[:,cut:]+=1000
    zz,cc=calibrated(b)
    assert cut==cc
    np.testing.assert_array_equal(z[:,:cut],zz[:,:cut])
    x,y=feature(z,cut,True);xx,yy=feature(zz,cut,True)
    # The first scored label changed, but its input at cut-1 did not.
    np.testing.assert_array_equal(x[0],xx[0])
    assert y[0]!=yy[0]

def test_six_organism_units():
    rng=np.random.default_rng(3)
    pairs={i:{c:rng.normal(size=(25,48)) for c in ('before','after')} for i in range(1,7)}
    r=run(pairs)
    assert len(r['rows'])==6
    assert all(x['before']['calibration_frames']==20 for x in r['rows'])
