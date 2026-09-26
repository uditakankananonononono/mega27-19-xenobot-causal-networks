"""Manifest primary public trajectory archives, without opening behavior outcomes."""
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20), b''):h.update(b)
    return h.hexdigest()


def manifest(root):
    root=Path(root)
    archives=sorted(root.glob('rawdata/*.csv.zip'),key=lambda p:int(p.name.split('.')[0]))
    expected=set(range(3,15))
    observed={int(p.name.split('.')[0]) for p in archives}
    if observed != expected: raise ValueError(f'Expected archives 3-14; found {sorted(observed)}')
    entries=[]
    for p in archives:
        with ZipFile(p) as z:
            if z.namelist() != [f'{p.name[:-4]}']: raise ValueError(f'Unexpected archive contents: {p.name}')
        entries.append(dict(name=p.name,byte_size=p.stat().st_size,sha256=sha256(p),
                            role='whole-organism movement tracks'))
    info=root/'rawdata/info.xlsx'
    if not info.exists():raise ValueError('Missing condition metadata')
    entries.append(dict(name='info.xlsx',byte_size=info.stat().st_size,
                        sha256=sha256(info),role='replicate condition/age/scale/arena metadata'))
    return dict(source_url='https://github.com/swarm-lab/xenobots',
                upstream_commit='3d8e4c3f460578700039a1c111d14adc6b1ccb52',
                license='GPL-3.0 repository license; verify data reuse terms separately before redistributing raw archives',
                raw_archives_republished=False,entries=entries)

if __name__=='__main__':print(json.dumps(manifest(sys.argv[1]),indent=2))
