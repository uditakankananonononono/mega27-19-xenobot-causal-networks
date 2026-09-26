import numpy as np
from src.timegraph_audit import TRUTH,SLOTS,metrics,design,fit_tvals

def test_ground_truth_and_slots():
    assert TRUTH=={(0,3,2),(2,1,1)}
    assert len(SLOTS)==32
    assert metrics(set())['slot_hamming']==2
    assert metrics(TRUTH)['slot_hamming']==0

def test_no_future_in_lag_design():
    a=np.arange(2000.,dtype=float).reshape(500,4)
    x,y=design(a)
    b=a.copy();b[-1,:]=1e6
    xx,yy=design(b)
    np.testing.assert_array_equal(x[-1,:],xx[-1,:])
    assert not np.array_equal(y[-1],yy[-1])

def test_ols_known_coefficient():
    rng=np.random.default_rng(12)
    x=np.column_stack((np.ones(500),rng.normal(size=(500,3))))
    y=x[:,1]*.8+rng.normal(size=500)*.02
    t=fit_tvals(x,y[:,None])
    assert t.shape==(4,1) and abs(t[1,0])>20
