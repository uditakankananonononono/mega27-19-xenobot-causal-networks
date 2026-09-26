"""Structural-only audit of published Varley 2025 Xenobot calcium matrices.

Public processed GCaMP6s intensities, not raw microscope video or outcomes.
Does not compute correlations, prediction accuracy or claimed discoveries.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
import numpy as np


def audit_folder(folder):
    files=sorted(Path(folder).glob('xenobot_series_*.npz'))
    ids=[re.fullmatch(r'xenobot_series_(\d{2})\.npz',p.name) for p in files]
    if len(files)!=28 or any(x is None for x in ids):
        raise ValueError('Expected 28 exactly named Xenobot series')
    if len({x.group(1) for x in ids}) != len(ids):
        raise ValueError('Duplicate Xenobot ID')
    result=[]
    for p in files:
        with np.load(p, allow_pickle=False) as z:
            if z.files != ['arr_0']:raise ValueError(f'Unexpected keys: {p.name}: {z.files}')
            a=z['arr_0']
            if a.ndim!=2 or min(a.shape)<2 or not np.issubdtype(a.dtype,np.number):
                raise ValueError(f'Invalid matrix: {p.name}')
            finite=bool(np.isfinite(a).all())
        result.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                           dimension_0=int(a.shape[0]),dimension_1=int(a.shape[1]),
                           finite=finite))
    return dict(source='Varley et al. 2025 Europe PMC supplement PMC12520083',
                scope='structural metadata only; dimension orientation and time cadence not yet established',
                matrices=result,
                caveats=['Processed calcium intensity, not direct voltage, gene expression or interventions.',
                         'Per-bot developmental/condition metadata absent in NPZ filenames.',
                         'The paper already analyzed information integration in these same bots.',
                         'Same-dataset bot holdout is not independent experimental replication.'])

if __name__=='__main__':
    print(json.dumps(audit_folder(sys.argv[1]),indent=2))
