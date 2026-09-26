"""Post-outcome sensitivity: distinguish structural lag links from reduced-form lag paths."""
import json
import numpy as np
from src.timegraph_grid import run

# Derived algebraically from upstream four-node structural equations. This
# sensitivity is not predeclared and is not a replacement for locked scores.
REDUCED_FORM={(0,3,2),(0,2,2),(2,1,1),(2,0,1)}
DIRECT={(0,3,2),(2,1,1)}

def rescore(grid=None):
    grid=run() if grid is None else grid
    assert len(grid['rows'])==60
    result={}
    for condition in ('A1','A1C_U_hidden'):
        rows=[r for r in grid['rows'] if r['condition']==condition]
        condition_result={}
        for method in ('var2','pairwise_own'):
            trials=[]
            edge_freq={}
            for r in rows:
                pred={tuple(e) for e in r[method]['predicted_edges']}
                for edge in pred-DIRECT:
                    key=str(edge)
                    edge_freq[key]=edge_freq.get(key,0)+1
                tp=len(pred&REDUCED_FORM)
                fp=len(pred-REDUCED_FORM)
                fn=len(REDUCED_FORM-pred)
                trials.append({'seed':r['seed'],'tp':tp,'fp':fp,'fn':fn,'hamming':fp+fn})
            condition_result[method]={'rows':trials,
                                      'means':{key:float(np.mean([r[key] for r in trials])) for key in ('tp','fp','fn','hamming')},
                                      'apparent_direct_false_edge_frequency':edge_freq}
        condition_result['paired_reduced_hamming_pairwise_minus_var']=float(np.mean([
            b['hamming']-a['hamming'] for a,b in zip(condition_result['var2']['rows'],condition_result['pairwise_own']['rows'])]))
        result[condition]=condition_result
    return {'status':'POST-OUTCOME GRAPH-TARGET SENSITIVITY, NOT PRESPECIFIED CAUSAL BENCHMARK',
            'direct_structural_lag_truth':sorted(map(list,DIRECT)),
            'algebraic_reduced_form_lag_truth':sorted(map(list,REDUCED_FORM)),
            'conditions':result}

if __name__=='__main__':
    with open('results/timegraph-grid-02.json') as f: grid=json.load(f)
    print(json.dumps(rescore(grid),indent=2))
