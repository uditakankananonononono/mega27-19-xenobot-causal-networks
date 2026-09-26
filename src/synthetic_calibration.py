"""Known-ground-truth calibration; synthetic outcomes never biological discovery."""
import json
import numpy as np
from src.organoid_method import train,score
SCENARIOS={'null':(0.0,0.0),'coupling':(0.25,0.0),'shared_drive':(0.0,0.5)}

def generate(seed, g, h, cells=64, frames=240, burnin=40):
    rng=np.random.default_rng(seed)
    a=np.zeros((cells,frames+burnin));u=np.zeros(frames+burnin)
    for t in range(frames+burnin-1):
        u[t+1]=.75*u[t]+rng.normal()
        mean_other=(a[:,t].sum()-a[:,t])/(cells-1)
        a[:,t+1]=.6*a[:,t]+g*mean_other+h*u[t]+rng.normal(size=cells)
    return a[:,burnin:]

def run(seed=20260926):
    # One RNG stream per scenario, fixed in advance. Replicate IDs 0-15 train,
    # 16-23 test, equal allocation in every scenario.
    out={'protocol':'docs/PIVOT_03_SYNTHETIC_CALIBRATION.md','status':'SYNTHETIC METHOD CALIBRATION; NOT A BIOLOGICAL FINDING','seed':seed,'scenarios':{}}
    for name,(g,h) in SCENARIOS.items():
        series=[generate(seed+10000*list(SCENARIOS).index(name)+i,g,h) for i in range(24)]
        own=train(series[:16],False);pop=train(series[:16],True)
        rows=[]
        for i in range(16,24):
            s=score(series[i],own,False);p=score(series[i],pop,True)
            rows.append({'replicate':i,'own_rmse':s,'population_rmse':p,'relative_gain':(s-p)/s})
        out['scenarios'][name]={'g':g,'h':h,'heldout':rows,'mean_gain':float(np.mean([r['relative_gain'] for r in rows]))}
    c=out['scenarios']['coupling']['mean_gain'];n=out['scenarios']['null']['mean_gain'];d=out['scenarios']['shared_drive']['mean_gain']
    out['coupling_beats_null']=bool(c>n)
    out['coupling_beats_shared_drive']=bool(c>d)
    return out

if __name__=='__main__':print(json.dumps(run(),indent=2))
