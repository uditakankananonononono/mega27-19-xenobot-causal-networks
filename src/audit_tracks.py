"""Fail-closed structural audit of published whole-organism Xenobot tracking CSVs.

No trajectory outcomes, behavioral effects, or model metrics are calculated.
"""
import csv
import io
import json
import re
import sys
import zipfile
from pathlib import Path

REQUIRED = {'x', 'y', 'frame', 'track_fixed', 'ignore'}


def audit_archive(path):
    path = Path(path)
    if not re.fullmatch(r'\d+\.csv\.zip', path.name):
        raise ValueError('Expected published numeric replicate CSV zip')
    with zipfile.ZipFile(path) as z:
        members = [n for n in z.namelist() if n.endswith('.csv') and not n.startswith('__MACOSX/')]
        if members != [path.name[:-4]]:
            raise ValueError('Archive must contain one correctly named CSV')
        with z.open(members[0]) as raw:
            text = io.TextIOWrapper(raw, encoding='utf-8-sig', newline='')
            reader = csv.DictReader(text)
            fields = set(reader.fieldnames or [])
            if not REQUIRED.issubset(fields):
                raise ValueError(f'Missing fields: {sorted(REQUIRED-fields)}')
            count = 0
            tracks = set()
            invalid = 0
            for row in reader:
                count += 1
                try:
                    float(row['x']); float(row['y']); int(row['frame'])
                    tracks.add(row['track_fixed'])
                except (ValueError, TypeError):
                    invalid += 1
    return {'replicate': path.name.split('.')[0], 'rows': count,
            'whole_organism_track_ids': len(tracks), 'invalid_coordinates_or_frames': invalid,
            'columns': sorted(fields), 'cell_level': False}


def main(argv):
    base = Path(argv[1])
    files = sorted(base.glob('*.csv.zip'))
    if not files:
        raise ValueError('No published track archives found')
    result = [audit_archive(p) for p in files]
    print(json.dumps({'source': 'swarm-lab/xenobots public tracking repository',
      'scope': 'structure only, no outcome test', 'replicates': result,
      'warnings': ['Tracks are whole-organism positions, not cellular measurements.',
                   'One condition per replicate in info.xlsx: leave-replicate-out cannot estimate unseen-condition effects.',
                   'Independent experiment/batch identity and linked cellular modalities not validated.']}, indent=2))


if __name__ == '__main__':
    main(sys.argv)
