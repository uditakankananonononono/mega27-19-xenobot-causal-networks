"""Within-recording calibration diagnostic, distinct from raw six-organoid test."""
import itertools,json
import numpy as np
from src.organoid_method import load

def calibrated(a):
    a=np.asarray(a,dtype=float)
    cut=max(20,int(np.floor(.25*a.shape[1])))
    if cut>=a.shape[1]-2:raise ValueError('too short')
    mu=a[:,:cut].mean(axis=1,keepdims=True)
    sd=a[:,:cut].std(axis=1,keepdims=True)
    z=(a-mu)/np.maximum(sd,1e-8)
    return z,cut

def feature(a,cut,pop):
    # Predict y at cut ... T-1 from features at cut-1 ... T-2.
    x=a[:,cut-1:-1];y=a[:,cut:]
    cols=[np.ones_like(x),x]
    if pop:
        oth=(a.sum(axis=0,keepdims=True)-a)/(len(a)-1)
        cols.append(oth[:,cut-1:-1])
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),y.ravel()

def fit(train,pop):
    xy=[feature(*calibrated(a),pop) for a in train]
    x=np.concatenate([p[0] for p in xy]);y=np.concatenate([p[1] for p in xy])
    penalty=np.eye(x.shape[1]);penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(a,coef,pop):
    x,y=feature(*calibrated(a),pop)
    return float(np.sqrt(np.mean((y-x@coef)**2)))

def run(pairs):
    rows=[]
    for held in sorted(pairs):
        tr=[pairs[i]['before'] for i in sorted(pairs) if i!=held]
        own=fit(tr,False);population=fit(tr,True)
        row={'organoid':held}
        for c in ('before','after'):
            a=pairs[held][c];s=score(a,own,False);p=score(a,population,True)
            row[c]={'calibration_frames':calibrated(a)[1], 'score_frames':int(a.shape[1]-calibrated(a)[1]),'own_rmse':s,'population_rmse':p,'relative_gain':(s-p)/s}
        row['paired_delta']=row['after']['relative_gain']-row['before']['relative_gain'];rows.append(row)
    d=np.array([r['paired_delta'] for r in rows]);mean=float(d.mean())
    null=np.array([(d*np.array(s)).mean() for s in itertools.product((-1,1),repeat=len(d))])
    return {'status':'POST-OUTCOME PROSPECTIVE CALIBRATION DIAGNOSTIC; NOT DISCOVERY','protocol':'docs/PIVOT_04_CALIBRATED_PROSPECTIVE_TEST.md','rows':rows,'mean_paired_delta':mean,'positive_count':int(np.sum(d>0)),'two_sided_exact_signflip_p':float(np.mean(abs(null)>=abs(mean)-1e-14))}
if __name__=='__main__':
    import sys
    print(json.dumps(run(load(sys.argv[1])),indent=2))
