"""Frozen exploratory bot-holdout benchmark; not an independent biological test.

Do not run as a claim of Xenobot intelligence or causal cell-cell signaling.
This same-study dataset was already published and used to design the pivot.
"""
import json
import sys
from pathlib import Path
import numpy as np
from src.cross_bot import evaluate

SOURCE='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12520083/supplementaryFiles'

def run(folder):
    folder=Path(folder)
    files={p.stem.removeprefix('xenobot_series_'):p for p in folder.glob('xenobot_series_*.npz')}
    if len(files)!=28:raise ValueError('Expect 28 distinct bots')
    mats={i:np.load(p,allow_pickle=False)['arr_0'] for i,p in sorted(files.items())}
    # Numeric IDs <=20 for method development; >20 for once-only same-study checkpoint. Missing IDs 15, 23, 25, 28 are absent in source; never renumber bots.
    dev={i:m for i,m in mats.items() if int(i)<=20}
    holdout={i:m for i,m in mats.items() if int(i)>20}
    if len(dev)!=19 or len(holdout)!=9:raise ValueError('Unexpected ID partition')
    rows=[]
    for i,m in holdout.items():
        score=evaluate(dev,i,m)
        rows.append(vars(score))
    return dict(status='EXPLORATORY SAME-STUDY CHECKPOINT; NOT independent replication or discovery',
                source=SOURCE,development_bots=len(dev),heldout_bots=len(holdout),
                comparison='population_ridge vs strongest own-history/persistence baseline',
                rows=rows,
                mean_persistence_rmse=float(np.mean([r['persistence_rmse'] for r in rows])),
                mean_self_rmse=float(np.mean([r['self_ridge_rmse'] for r in rows])),
                mean_population_rmse=float(np.mean([r['population_ridge_rmse'] for r in rows])))

if __name__=='__main__':print(json.dumps(run(sys.argv[1]),indent=2))
