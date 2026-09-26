"""Post-outcome oracle common-driver covariate sensitivity, synthetic only."""
import json
import numpy as np
from src.synthetic_calibration import SCENARIOS,generate

def generate_with_driver(seed,g,h,cells=64,frames=240,burnin=40):
    rng=np.random.default_rng(seed)
    a=np.zeros((cells,frames+burnin));u=np.zeros(frames+burnin)
    for t in range(frames+burnin-1):
        u[t+1]=.75*u[t]+rng.normal()
        mean_other=(a[:,t].sum()-a[:,t])/(cells-1)
        a[:,t+1]=.6*a[:,t]+g*mean_other+h*u[t]+rng.normal(size=cells)
    return a[:,burnin:],u[burnin:]

def features(a,u,pop):
    a=np.asarray(a)
    own=a[:,:-1];other=(a.sum(axis=0,keepdims=True)-a)/(len(a)-1)
    cols=[np.ones_like(own),own,np.broadcast_to(u[:-1],own.shape)]
    if pop:cols.append(other[:,:-1])
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),a[:,1:].ravel()

def fit(series,pop):
    xy=[features(a,u,pop) for a,u in series]
    x=np.concatenate([z[0] for z in xy]);y=np.concatenate([z[1] for z in xy])
    penalty=np.eye(x.shape[1]);penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(a,u,coef,pop):
    x,y=features(a,u,pop)
    return float(np.sqrt(np.mean((y-x@coef)**2)))

def run(seed=20260926):
    out={'status':'POST-OUTCOME ORACLE COMMON-DRIVER SENSITIVITY; NOT BIOLOGY OR PUBLISHED BENCHMARK',
         'protocol':'docs/SYNTHETIC_OBSERVED_DRIVER_SENSITIVITY_PROTOCOL.md',
         'seed':seed,'scenarios':{}}
    for idx,(name,(g,h)) in enumerate(SCENARIOS.items()):
        series=[generate_with_driver(seed+10000*idx+i,g,h) for i in range(24)]
        # The generator's X sequence must not change when exposing U.
        for i,(a,u) in enumerate(series):
            np.testing.assert_array_equal(a,generate(seed+10000*idx+i,g,h))
        own=fit(series[:16],False);pop=fit(series[:16],True)
        rows=[]
        for i in range(16,24):
            a,u=series[i]
            s=score(a,u,own,False);p=score(a,u,pop,True)
            rows.append({'replicate':i,'own_driver_rmse':s,'population_driver_rmse':p,'relative_gain':(s-p)/s})
        out['scenarios'][name]={'g':g,'h':h,'own_driver_coef':own.tolist(),
                                 'population_driver_coef':pop.tolist(),
                                 'heldout':rows,'mean_gain':float(np.mean([r['relative_gain'] for r in rows]))}
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
