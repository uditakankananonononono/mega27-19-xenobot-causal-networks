"""Post-outcome, same-study sensor/focal calcium forecasting, no causal claims."""
import itertools,json
from pathlib import Path
import numpy as np
SOURCE='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12520083/supplementaryFiles'

def features(a, sensor_even=True, population=False):
    a=np.asarray(a,dtype=float)
    sensors=a[0::2] if sensor_even else a[1::2]
    focal=a[1::2] if sensor_even else a[0::2]
    own=focal[:,:-1];y=focal[:,1:]
    cols=[np.ones_like(own),own]
    if population:cols.append(np.broadcast_to(sensors[:,:-1].mean(axis=0),own.shape))
    return np.stack(cols,axis=-1).reshape(-1,len(cols)),y

def fit(train,even,pop):
    batches=[features(a,even,pop) for a in train]
    x=np.concatenate([b[0] for b in batches]);y=np.concatenate([b[1].ravel() for b in batches])
    penalty=np.eye(x.shape[1]);penalty[0,0]=0
    return np.linalg.solve(x.T@x+penalty,x.T@y)

def score(a,coef,even,pop):
    x,y=features(a,even,pop)
    err=(y.ravel()-x@coef).reshape(y.shape)
    pooled=float(np.sqrt(np.mean(err**2)))
    percell=float(np.mean(np.sqrt(np.mean(err**2,axis=1))))
    return {'pooled_rmse':pooled,'mean_percell_rmse':percell,'cells':len(y),'frames':y.shape[1]}

def run(folder):
    folder=Path(folder)
    files={int(p.stem.removeprefix('xenobot_series_')):p for p in folder.glob('xenobot_series_*.npz')}
    if len(files)!=28:raise ValueError('Expected 28 raw source matrix files')
    mats={i:np.load(p,allow_pickle=False)['arr_0'] for i,p in files.items()}
    if any(a.ndim!=2 or a.shape[0]<28 or a.shape[1]<100 or not np.isfinite(a).all() for a in mats.values()):
        raise ValueError('Invalid source cells or time')
    dev={k:v for k,v in mats.items() if k<=20};held={k:v for k,v in mats.items() if k>20}
    if len(dev)!=19 or len(held)!=9:raise ValueError('Unexpected original bot ID partition')
    result={}
    for label,even in (('even_sensors',True),('odd_sensors',False)):
        own=fit(list(dev.values()),even,False)
        with_sensor=fit(list(dev.values()),even,True)
        rows=[]
        for i,a in sorted(held.items()):
            x=score(a,own,even,False);y=score(a,with_sensor,even,True)
            rows.append({'bot_id':i,'own':x,'with_sensor':y,
                         'relative_gain_pooled':(x['pooled_rmse']-y['pooled_rmse'])/x['pooled_rmse'],
                         'relative_gain_percell':(x['mean_percell_rmse']-y['mean_percell_rmse'])/x['mean_percell_rmse']})
        d=np.array([r['relative_gain_pooled'] for r in rows]);m=float(np.mean(d))
        signflip=np.array([(d*np.array(s)).mean() for s in itertools.product((-1,1),repeat=9)])
        result[label]={'coefficients':{'own':own.tolist(),'with_sensor':with_sensor.tolist()},'rows':rows,
                       'mean_relative_gain_pooled':m,'positive_bots_pooled':int(np.sum(d>0)),
                       'mean_relative_gain_percell':float(np.mean([r['relative_gain_percell'] for r in rows])),
                       'two_sided_signflip_p_descriptive':float(np.mean(abs(signflip)>=abs(m)-1e-14))}
    return {'status':'POST-OUTCOME SAME-STUDY REAL CALCIUM METHOD ROBUSTNESS; NOT XENOBOT BEHAVIOR OR CAUSAL BIOLOGY',
            'protocol':'docs/REAL_CALCIUM_SENSOR_FOCAL_PROTOCOL.md','source':SOURCE,'dev_bots':len(dev),'heldout_bots':len(held),'conditions':result}
if __name__=='__main__':
 import sys
 print(json.dumps(run(sys.argv[1]),indent=2))
