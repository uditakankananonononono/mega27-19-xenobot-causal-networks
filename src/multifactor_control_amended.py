"""Judge-13 two-hidden-factor synthetic failure-map; no causal discovery claims."""
import json
import numpy as np

SCENARIOS={
 'null':(0.,0.,0.),'coupling':(.25,0.,0.),
 'one_driver':(0.,.5,0.),'two_drivers':(0.,.5,.5),
 'coupling_two_drivers':(.25,.5,.5),
}
MODELS=('own','mean','pc1','pc2','pc2_mean')
CUT=60

def generate(seed,g,h1,h2,cells=64,frames=240,burnin=40):
    rng=np.random.default_rng(seed)
    a=np.zeros((cells,frames+burnin))
    u1=np.zeros(frames+burnin);u2=np.zeros(frames+burnin)
    b=np.ones(cells);b[16:32]=-1.;b[48:]=-1.
    for t in range(frames+burnin-1):
        u1[t+1]=.75*u1[t]+rng.normal()
        u2[t+1]=.55*u2[t]+rng.normal()
        other=(a[:,t].sum()-a[:,t])/(cells-1)
        a[:,t+1]=.6*a[:,t]+g*other+h1*u1[t]+h2*b*u2[t]+rng.normal(size=cells)
    return a[:,burnin:]

def prepare(a):
    sensors=a[:32];focal=a[32:]
    mu=sensors[:,:CUT].mean(axis=1)
    centered=(sensors-mu[:,None]).T
    _,_,vh=np.linalg.svd(centered[:CUT],full_matrices=False)
    top=vh[:2].copy()
    for j in range(2):
        if top[j].sum()<0:top[j]*=-1
    pcs=centered@top.T
    mean=sensors.mean(axis=0)
    corr=[float(np.corrcoef(mean[CUT-1:],pcs[CUT-1:,j])[0,1]) for j in range(2)]
    return focal,mean,pcs,corr,top

def feature(record,model):
    focal,mean,pcs,_,_=record
    own=focal[:,CUT-1:-1]
    cols=[np.ones_like(own),own]
    if model in ('mean','pc2_mean'):cols.append(np.broadcast_to(mean[CUT-1:-1],own.shape))
    if model in ('pc1','pc2','pc2_mean'):cols.append(np.broadcast_to(pcs[CUT-1:-1,0],own.shape))
    if model in ('pc2','pc2_mean'):cols.append(np.broadcast_to(pcs[CUT-1:-1,1],own.shape))
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),focal[:,CUT:].ravel()

def fit(train,model):
    matrices=[feature(r,model) for r in train]
    x=np.concatenate([m[0] for m in matrices]);y=np.concatenate([m[1] for m in matrices])
    penalty=np.eye(x.shape[1]);penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(r,model,coef):
    x,y=feature(r,model)
    return float(np.sqrt(np.mean((y-x@coef)**2)))

def run():
    out={'status':'POST-OUTCOME SYNTHETIC TWO-DRIVER METHODS SENSITIVITY, NOT BIOLOGY OR BENCHMARK BEAT',
         'protocol':'docs/JUDGE_13_MULTIFACTOR_AMENDMENT.md','scenarios':{}}
    for index,(name,params) in enumerate(SCENARIOS.items()):
        records=[prepare(generate(20270000+index*10000+i,*params)) for i in range(24)]
        coefs={m:fit(records[:16],m) for m in MODELS}
        rows=[]
        for i in range(16,24):
            r=records[i];rmse={m:score(r,m,c) for m,c in coefs.items()}
            rows.append({'replicate':i,'rmse':rmse,'mean_over_own':(rmse['own']-rmse['mean'])/rmse['own'],
                         'pc1_over_own':(rmse['own']-rmse['pc1'])/rmse['own'],
                         'pc2_over_own':(rmse['own']-rmse['pc2'])/rmse['own'],
                         'mean_added_to_pc2':(rmse['pc2']-rmse['pc2_mean'])/rmse['pc2'],
                         'mean_pc_correlations':r[3]})
        top=np.stack([r[-1] for r in records[:16]])
        # PCA loadings vary across independently generated recordings: dot products to first.
        align=np.abs(np.einsum('rjc,jc->rj',top,top[0]))
        out['scenarios'][name]={'g_h1_h2':params,'coefs':{k:v.tolist() for k,v in coefs.items()},
                                'heldout':rows,
                                'mean_gains':{k:float(np.mean([r[k] for r in rows])) for k in ('mean_over_own','pc1_over_own','pc2_over_own','mean_added_to_pc2')},
                                'train_loading_alignment_to_first':np.mean(align,axis=0).tolist(),
                                'heldout_mean_pc_correlation':np.mean([r['mean_pc_correlations'] for r in rows],axis=0).tolist()}
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
