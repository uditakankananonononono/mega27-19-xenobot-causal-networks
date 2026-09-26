"""Post-outcome estimator correction: per-cell RMSE then mean over cells."""
import itertools,json
import numpy as np
from src.organoid_method import load,train,features

def cell_rmse(a,coef,pop):
    x,y=features(a,pop)
    pred=x@coef
    cell_errors=(y-pred).reshape(a.shape[0],a.shape[1]-1)
    return np.sqrt(np.mean(cell_errors**2,axis=1))

def run(pairs):
    rows=[]
    for held in sorted(pairs):
        tr=[pairs[i]['before'] for i in sorted(pairs) if i!=held]
        own=train(tr,False);pop=train(tr,True)
        row={'organoid':held}
        for c in ('before','after'):
            a=pairs[held][c]
            s=float(cell_rmse(a,own,False).mean())
            p=float(cell_rmse(a,pop,True).mean())
            row[c]={'mean_cell_own_rmse':s,'mean_cell_population_rmse':p,'relative_gain':(s-p)/s,'n_cells':a.shape[0]}
        row['paired_delta']=row['after']['relative_gain']-row['before']['relative_gain'];rows.append(row)
    d=np.array([r['paired_delta'] for r in rows]);mean=float(d.mean())
    null=np.array([(d*np.array(s)).mean() for s in itertools.product((-1,1),repeat=6)])
    return {'status':'POST-OUTCOME CORRECTION OF DEVIATED POOLED RMSE; NOT PREREGISTERED EVIDENCE','protocol':'docs/ORGANOID_RMSE_AMENDMENT.md','rows':rows,'mean_paired_delta':mean,'positive_count':int(np.sum(d>0)),'two_sided_exact_signflip_p':float(np.mean(abs(null)>=abs(mean)-1e-14))}
if __name__=='__main__':
    import sys
    print(json.dumps(run(load(sys.argv[1])),indent=2))
