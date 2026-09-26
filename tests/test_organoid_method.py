import numpy as np
import pytest
from src.organoid_method import features,train,score,run

def test_no_future_leakage():
    a=np.array([[1.,2,3,4,5],[4.,3,2,1,0],[0.,1,0,1,0]])
    x,y=features(a)
    a[:,4]=200
    xx,yy=features(a)
    np.testing.assert_array_equal(x,xx)
    assert not np.array_equal(y,yy)

def test_holdout_organoid_never_trains():
    rng=np.random.default_rng(3)
    pairs={i:{'before':rng.normal(size=(22,25)), 'after':rng.normal(size=(23,25))} for i in range(1,7)}
    result=run(pairs)
    assert len(result['rows'])==6
    assert 0<=result['two_sided_exact_signflip_p']<=1
    assert result['rows'][0]['cell_counts']=={'before':22,'after':23}

def test_dimensions():
    a=np.arange(75,dtype=float).reshape(3,25)
    x,y=features(a)
    assert x.shape==(72,3) and y.shape==(72,)
    assert np.isfinite(score(a,train([a,a+1],True),True))
