"""Permutation-invariant cross-bot calcium predictor, for exploratory testing only."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class CrossBotScore:
    heldout_id: str
    n_cells: int
    n_test_frames: int
    persistence_rmse: float
    self_ridge_rmse: float
    population_ridge_rmse: float


def _features(a, with_population):
    # row = cell, column = time; all predictors at t or earlier.
    x=a[:,:-1]
    y=a[:,1:]
    cols=[np.ones_like(x),x]
    if with_population:
        other=(x.sum(axis=0,keepdims=True)-x)/(len(x)-1)
        cols.append(other)
    return np.stack(cols,axis=-1),y


def evaluate(train_bots, heldout_id, test_bot, ridge=1.0, min_frames=20):
    """Fit common cell-level coefficients on *other* bots; score unseen bot.

    Training normalization is not re-estimated on heldout bot. Input arrays
    are already preprocessed/z-scored by published source. Whole unseen bot
    remains untouched until final scoring; no within-bot adaptation.
    """
    if heldout_id in train_bots:raise ValueError('Heldout bot appears in training')
    if len(train_bots)<2:raise ValueError('Need multiple training bots')
    mats=list(train_bots.values())+[test_bot]
    if any(np.asarray(m).ndim!=2 or min(m.shape)<min_frames or not np.isfinite(m).all() for m in mats):
        raise ValueError('Invalid bot matrix')
    def fit_predict(pop):
        fs=[];ys=[]
        for arr in train_bots.values():
            x,y=_features(np.asarray(arr,dtype=float),pop)
            fs.append(x.reshape(-1,x.shape[-1]));ys.append(y.ravel())
        xx=np.concatenate(fs); yy=np.concatenate(ys)
        penalty=np.eye(xx.shape[1])*ridge;penalty[0,0]=0
        coef=np.linalg.solve(xx.T@xx+penalty,xx.T@yy)
        target,test_y=_features(np.asarray(test_bot,dtype=float),pop)
        return np.sqrt(np.mean((test_y-np.einsum('itd,d->it',target,coef))**2))
    held=np.asarray(test_bot,dtype=float)
    persistence=np.sqrt(np.mean((held[:,1:]-held[:,:-1])**2))
    return CrossBotScore(str(heldout_id),int(held.shape[0]),int(held.shape[1]-1),
                         float(persistence),float(fit_predict(False)),float(fit_predict(True)))
