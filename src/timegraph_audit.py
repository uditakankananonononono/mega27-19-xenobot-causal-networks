"""TimeGraph external diagnostic: lagged edge task differs from author Table 2.

Upstream CSVs are read locally and never shipped. This is not biological inference.
"""
import csv, itertools, json
from pathlib import Path
import numpy as np
from scipy import stats

SOURCE='https://github.com/hferdous/TimeGraph/tree/4d93403b002664fa55607f308ad0e80623472ded'
# Directly extracted from Codes/a1.py / Codes/a1c.py n_vars=4,max_lag=2;
# contemporaneous X4->X3 and X3->X2 are intentionally excluded.
TRUTH={(0,3,2),(2,1,1)}  # (source,target,positive lag)
SLOTS={(source,target,lag) for source in range(4) for target in range(4) for lag in (1,2)}

def read_csv(path):
    with open(path,newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=500:raise ValueError('Expected 500 rows')
    required={f'X{i}' for i in range(1,5)}
    if not required.issubset(rows[0]):raise ValueError('Missing observed variables')
    return np.array([[float(row[f'X{i}']) for i in range(1,5)] for row in rows])

def design(a,lag=2):
    if a.shape!=(500,4):raise ValueError('Expected 500x4 observed only')
    n=len(a)-lag
    x=np.stack([a[lag-k:len(a)-k,j] for k in (1,2) for j in range(4)],axis=1)
    return np.column_stack((np.ones(n),x)),a[lag:]

def fit_tvals(x,y):
    coef,residuals,rank,_=np.linalg.lstsq(x,y,rcond=None)
    if rank!=x.shape[1]:raise ValueError('Singular design')
    resid=y-x@coef
    variance=(resid**2).sum(axis=0)/(len(x)-x.shape[1])
    inv=np.linalg.inv(x.T@x)
    se=np.sqrt(inv.diagonal()[:,None]*variance[None,:])
    return coef/se

def var_edges(a):
    x,y=design(a)
    tvals=fit_tvals(x,y)
    threshold=stats.t.isf(.05/(2*len(SLOTS)),df=len(x)-x.shape[1])
    return {(s,t,lag) for s,t,lag in SLOTS if abs(tvals[1+(lag-1)*4+s,t])>threshold}

def pairwise_edges(a):
    x,y=design(a)
    # Each target residual is first stripped of its own two past values.
    # Candidate other-lag predictor is partialled against own history too,
    # but not against other cells: pairwise conditional baseline.
    threshold=stats.t.isf(.05/(2*len(SLOTS)),df=len(x)-3)
    edges=set()
    for target in range(4):
        own=x[:,[0,1+target,5+target]]
        r_y=y[:,target]-own@np.linalg.lstsq(own,y[:,target],rcond=None)[0]
        for source,_,lag in (e for e in SLOTS if e[1]==target):
            cand=x[:,1+(lag-1)*4+source]
            r_x=cand-own@np.linalg.lstsq(own,cand,rcond=None)[0]
            if np.linalg.norm(r_x)<1e-12 or np.linalg.norm(r_y)<1e-12:continue
            r=np.corrcoef(r_x,r_y)[0,1]
            tval=abs(r)*np.sqrt((len(x)-3)/max(1e-15,1-r*r))
            if tval>threshold:edges.add((source,target,lag))
    return edges

def metrics(pred):
    tp=len(pred&TRUTH);fp=len(pred-TRUTH);fn=len(TRUTH-pred)
    return {'predicted_edges':sorted([list(x) for x in pred]),'tp':tp,'fp':fp,'fn':fn,'tpr':tp/len(TRUTH),'fdr':fp/len(pred) if pred else 0.0,'slot_hamming':fp+fn}

def run(a1,a1c):
    r={}
    for name,path in [('A1',a1),('A1C_U_hidden',a1c)]:
        a=read_csv(path)
        r[name]={'shape':list(a.shape),'visible_lag_truth':sorted([list(x) for x in TRUTH]),
                 'var2':metrics(var_edges(a)),'pairwise_own':metrics(pairwise_edges(a)),
                 'zero_edge':metrics(set())}
    return {'status':'EXTERNAL DIAGNOSTIC, NOT PUBLISHED TABLE 2 BENCHMARK COMPARISON OR BIOLOGY',
            'source':SOURCE,'task':'4 visible nodes, positive lags 1/2, 32 possible directed edge slots; U withheld; lag-zero edges excluded',
            'conditions':r}
if __name__=='__main__':
    import sys
    print(json.dumps(run(Path(sys.argv[1]),Path(sys.argv[2])),indent=2))
