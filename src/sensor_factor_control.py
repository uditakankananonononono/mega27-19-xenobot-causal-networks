"""Judge-12 sensor-only proxy diagnostic, synthetic and noncausal."""
import json
import numpy as np
from src.synthetic_calibration import SCENARIOS,generate
from src.observed_driver_sensitivity import generate_with_driver
CUT=60

def make(seed,g,h):
    a,u=generate_with_driver(seed,g,h)
    np.testing.assert_array_equal(a,generate(seed,g,h))
    sensors=a[:32];focal=a[32:]
    mu=sensors[:,:CUT].mean(axis=1)
    centered=(sensors-mu[:,None]).T
    _,_,vh=np.linalg.svd(centered[:CUT],full_matrices=False)
    loading=vh[0]
    if loading.sum()<0:loading=-loading
    pc=centered@loading
    mean=sensors.mean(axis=0)
    corr=float(np.corrcoef(pc[CUT-1:],mean[CUT-1:])[0,1])
    # same target frames from 60..239 in all models
    return focal,mean,pc,corr

def xy(record,model):
    focal,mean,pc,_=record
    own=focal[:,CUT-1:-1]
    cols=[np.ones_like(own),own]
    if model in ('mean','both'):cols.append(np.broadcast_to(mean[CUT-1:-1],own.shape))
    if model in ('pc1','both'):cols.append(np.broadcast_to(pc[CUT-1:-1],own.shape))
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),focal[:,CUT:].ravel()

def fit(records,model):
    batches=[xy(r,model) for r in records]
    x=np.concatenate([b[0] for b in batches]);y=np.concatenate([b[1] for b in batches])
    penalty=np.eye(x.shape[1]);penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(record,model,coef):
    x,y=xy(record,model)
    return float(np.sqrt(np.mean((y-x@coef)**2)))

def run(seed=20260926):
    output={'status':'POST-OUTCOME JUDGE-12 SENSOR-ONLY FACTOR SENSITIVITY, NOT CAUSAL BIOLOGY',
            'protocol':'docs/JUDGE_12_SENSOR_FACTOR_PROTOCOL.md','seed':seed,'scenarios':{}}
    for idx,(name,(g,h)) in enumerate(SCENARIOS.items()):
        series=[make(seed+idx*10000+i,g,h) for i in range(24)]
        models={m:fit(series[:16],m) for m in ('own','mean','pc1','both')}
        rows=[]
        for i in range(16,24):
            r=series[i];values={m:score(r,m,v) for m,v in models.items()};base=values['own']
            rows.append({'replicate':i,'rmse':values,'pc_mean_correlation':r[-1],
                         'mean_vs_own_gain':(base-values['mean'])/base,
                         'pc_vs_own_gain':(base-values['pc1'])/base,
                         'mean_added_to_pc_gain':(values['pc1']-values['both'])/values['pc1']})
        keys=('mean_vs_own_gain','pc_vs_own_gain','mean_added_to_pc_gain','pc_mean_correlation')
        output['scenarios'][name]={'g':g,'h':h,'coefficients':{m:v.tolist() for m,v in models.items()},'heldout':rows,
                                   'means':{k:float(np.mean([r[k] for r in rows])) for k in keys}}
    return output
if __name__=='__main__':print(json.dumps(run(),indent=2))
