"""Conservative calcium forecasting controls; exploratory, not a biological result.

Rows are identified cells, columns are ordered frames. Never split cells/frames
across bot-level train/test. This module only implements no-fit baselines and
bot-wise temporally blocked scoring with no future values in features.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Score:
    n_cells: int
    n_frames: int
    persistence_rmse: float
    ar1_rmse: float
    global_rmse: float
    population_rmse: float


def _rmse(y, pred):
    return float(np.sqrt(np.mean((y-pred)**2)))


def score_bot(a, train_fraction=.6, gap=8, ridge=1e-3):
    a=np.asarray(a,dtype=float)
    if a.ndim!=2 or min(a.shape)<10 or not np.isfinite(a).all():
        raise ValueError('Require finite cells x frames matrix of adequate size')
    if not (0.5<=train_fraction<=.8):raise ValueError('Bad training fraction')
    n,t=a.shape
    split=int(t*train_fraction)
    if split+gap+1>=t:raise ValueError('Gap leaves no holdout frames')
    # Predict y_i(t+1) from x_i(t), and separately a leave-one-out global mean
    # at the same PAST time. The focal cell never leaks into the population input.
    x=a[:,:-1]
    y=a[:,1:]
    loo=(x.sum(axis=0,keepdims=True)-x)/(n-1)
    train=np.arange(split-1)
    test=np.arange(split+gap-1,t-1)
    if not len(test):raise ValueError('No held-out times')
    # Per-bot fitting is a local adaptation experiment, not cross-bot model
    # generalization; temporal gap keeps immediate autocorrelation from touching.
    def fit(features):
        design=np.stack([np.ones_like(x),*features],axis=-1)
        coefs=[]
        for i in range(n):
            z=design[i,train,:]
            coefs.append(np.linalg.solve(z.T@z+ridge*np.eye(z.shape[1]),z.T@y[i,train]))
        return np.einsum('itd,id->it',design[:,test,:],np.asarray(coefs))
    target=y[:,test]
    persistence=x[:,test]
    ar1=fit([x])
    # global-only is a deliberately weak control; population+own is important.
    global_only=fit([loo])
    population=fit([x,loo])
    return Score(n,len(test),_rmse(target,persistence),_rmse(target,ar1),
                 _rmse(target,global_only),_rmse(target,population))
