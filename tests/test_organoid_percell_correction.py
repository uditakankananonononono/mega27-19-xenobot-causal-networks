import numpy as np
from src.organoid_percell_correction import cell_rmse,run

def test_cell_aggregation_differs_from_pooled():
    a=np.array([[0.,1.,3.,7.],[1.,1.,1.,1.]])
    coef=np.array([0.,0.])
    per=cell_rmse(a,coef,False)
    assert per.shape==(2,)
    assert not np.isclose(per.mean(),np.sqrt((per**2).mean()))

def test_six_independent_pairs():
    rng=np.random.default_rng(4)
    pairs={i:{c:rng.normal(size=(22,24)) for c in ('before','after')} for i in range(1,7)}
    result=run(pairs)
    assert len(result['rows'])==6
    assert all(r['before']['n_cells']==22 for r in result['rows'])
