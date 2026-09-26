"""Source-equivalent TimeGraph A1/A1C generator diagnostic, 30 matched seeds.

Equations and noise draw order audited against hferdous/TimeGraph SHA
4d93403b002664fa55607f308ad0e80623472ded. No raw upstream data shipped.
"""
import json
import numpy as np
from src.timegraph_audit import var_edges,pairwise_edges,metrics

def generate(seed,hidden=False,n=500):
    # Match upstream use of global MT19937 np.random.seed, draw order:
    # initial two rows X then U per row; later each row draws 4 X noises+U.
    rng=np.random.RandomState(seed)
    x=np.zeros((n,4));u=np.zeros(n)
    for t in range(2):
        x[t]=rng.normal(0,.1,size=4)
        if hidden:u[t]=rng.normal(0,.1,size=1)[0]
    for t in range(2,n):
        eps=rng.normal(0,.1,size=5 if hidden else 4)
        if hidden:u[t]=eps[-1]
        x[t,3]=.25*x[t-2,0]+eps[3]
        x[t,2]=.35*x[t,3]+(.3*u[t] if hidden else 0)+eps[2]
        x[t,1]=.3*x[t-1,2]+eps[1]
        x[t,0]=.4*x[t,1]+(.5*u[t] if hidden else 0)+eps[0]
    return x,u

def run():
    rows=[]
    for seed in range(1000,1030):
        for label,hidden in (('A1',False),('A1C_U_hidden',True)):
            x,_=generate(seed,hidden)
            rows.append({'seed':seed,'condition':label,'var2':metrics(var_edges(x)),'pairwise_own':metrics(pairwise_edges(x)),'zero_edge':metrics(set())})
    summary={}
    for label in ('A1','A1C_U_hidden'):
        rr=[r for r in rows if r['condition']==label]
        summary[label]={}
        for model in ('var2','pairwise_own','zero_edge'):
            summary[label][model]={k:float(np.mean([r[model][k] for r in rr])) for k in ('tp','fp','fn','tpr','fdr','slot_hamming')}
        summary[label]['paired_hamming_pairwise_minus_var']=float(np.mean([r['pairwise_own']['slot_hamming']-r['var2']['slot_hamming'] for r in rr]))
    return {'status':'GENERATOR REPRODUCTION DIAGNOSTIC, NOT PUBLISHED TABLE 2 WIN OR BIOLOGICAL DISCOVERY','source_commit':'4d93403b002664fa55607f308ad0e80623472ded','protocol':'docs/TIMEGRAPH_GRID_02_PROTOCOL.md','rows':rows,'summary':summary}
if __name__=='__main__':print(json.dumps(run(),indent=2))
