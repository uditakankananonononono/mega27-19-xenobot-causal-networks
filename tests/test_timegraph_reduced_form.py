import json
from src.timegraph_reduced_form import rescore,REDUCED_FORM,DIRECT

def test_target_paths_and_scores():
    assert DIRECT < REDUCED_FORM
    with open('results/timegraph-grid-02.json') as f:r=rescore(json.load(f))
    assert len(r['conditions']['A1']['var2']['rows'])==30
    for c in r['conditions'].values():
        for m in ('var2','pairwise_own'):
            assert all(x['tp']+x['fn']==4 and x['fp']+x['fn']==x['hamming'] for x in c[m]['rows'])
