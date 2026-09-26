"""Exploratory leave-one-organoid-out method transfer on non-Xenobot tissue.

Protocol: docs/PIVOT_02_ORGANOID_METHOD.md; not a causal mechanism test.
"""
import itertools
import json
from pathlib import Path
import numpy as np

SOURCE = 'https://github.com/caitlingrasso/bio-connectivity/tree/0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700/data/series_raw'

def load(folder):
    folder=Path(folder)
    pairs={}
    for i in range(1,7):
        pairs[i]={}
        for condition in ('before','after'):
            p=folder/f'bot_{i:02d}_{condition}_series.csv'
            a=np.loadtxt(p,delimiter=',')
            if a.ndim!=2 or min(a.shape)<20 or not np.isfinite(a).all():
                raise ValueError(f'Invalid cells x time: {p}')
            pairs[i][condition]=a
    return pairs

def features(a, population=True, seed=None):
    a=np.asarray(a,dtype=float)
    own=a[:,:-1]
    oth=(a.sum(axis=0,keepdims=True)-a)/(len(a)-1)
    if seed is not None:
        # Each cell's source trace retains ordering/autocorrelation but loses
        # the original alignment with the focal cell. No wraparound forecasts.
        rng=np.random.default_rng(seed)
        shifts=rng.integers(max(2,a.shape[1]//5),max(3,a.shape[1]*4//5),size=len(a))
        shifted=np.stack([np.roll(x,int(s)) for x,s in zip(a,shifts)])
        oth=(shifted.sum(axis=0,keepdims=True)-shifted)/(len(a)-1)
        # np.roll WRAPS boundaries; these are surrogates, not causal forecasts.
        # A shifted population signal is only a deliberately broken control;
        # original focal series and target remain untouched.
    cols=[np.ones_like(own),own]
    if population:cols.append(oth[:,:-1])
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),a[:,1:].ravel()

def train(matrices,population,seed=None,ridge=1.0):
    xx,yy=zip(*(features(a,population,seed=seed) for a in matrices))
    x=np.concatenate(xx); y=np.concatenate(yy)
    penalty=np.eye(x.shape[1])*ridge;penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(a,coef,population,seed=None):
    x,y=features(a,population,seed=seed)
    return float(np.sqrt(np.mean((y-x@coef)**2)))

def run(pairs):
    rows=[]
    for held in sorted(pairs):
        trainset=[pairs[i]['before'] for i in sorted(pairs) if i!=held]
        selfcoef=train(trainset,False)
        popcoef=train(trainset,True)
        controlcoef=train(trainset,True,seed=1985)
        row={'organoid':held,'cell_counts':{c:int(a.shape[0]) for c,a in pairs[held].items()},'frames':{c:int(a.shape[1]) for c,a in pairs[held].items()}}
        for c in ('before','after'):
            a=pairs[held][c]
            own=score(a,selfcoef,False)
            pop=score(a,popcoef,True)
            control=score(a,controlcoef,True,seed=1985)
            persistence=float(np.sqrt(np.mean(np.diff(a,axis=1)**2)))
            row[c]={'self_rmse':own,'population_rmse':pop,'shifted_population_rmse':control,'persistence_rmse':persistence,'relative_gain':(own-pop)/own,'relative_gain_shift_control':(own-control)/own}
        row['paired_gain_delta']=row['after']['relative_gain']-row['before']['relative_gain']
        rows.append(row)
    deltas=np.array([r['paired_gain_delta'] for r in rows]); mean=float(np.mean(deltas))
    null=np.array([np.mean(deltas*np.array(signs)) for signs in itertools.product((-1,1),repeat=len(rows))])
    p=float(np.mean(np.abs(null)>=abs(mean)-1e-14))
    return {'status':'EXPLORATORY CROSS-SYSTEM METHOD TEST; NOT A XENOBOT DISCOVERY', 'source':SOURCE,'upstream_commit':'0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700','protocol':'docs/PIVOT_02_ORGANOID_METHOD.md','rows':rows,'mean_paired_relative_gain_delta':mean,'median_paired_relative_gain_delta':float(np.median(deltas)),'positive_paired_deltas':int(np.sum(deltas>0)),'two_sided_exact_signflip_p':p}

if __name__=='__main__':
    import sys
    print(json.dumps(run(load(sys.argv[1])),indent=2))
