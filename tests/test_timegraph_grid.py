import numpy as np
from src.timegraph_grid import generate,run

def test_source_equivalent_draw_order():
    a,u=generate(42,False)
    b,v=generate(42,True)
    assert a.shape==b.shape==(500,4)
    np.testing.assert_allclose(a[0],b[0])
    assert not np.allclose(a[1],b[1])
    assert np.allclose(u,0) and np.std(v)>0

def test_generator_reproducible():
    a,u=generate(1000,True)
    aa,uu=generate(1000,True)
    np.testing.assert_array_equal(a,aa);np.testing.assert_array_equal(u,uu)

def test_grid_has_matched_seeds():
    r=run()
    assert len(r['rows'])==60
    assert {x['seed'] for x in r['rows']}==set(range(1000,1030))
    assert all(len([x for x in r['rows'] if x['seed']==seed])==2 for seed in range(1000,1030))
