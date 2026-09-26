import csv
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from src.audit_tracks import audit_archive

class AuditTests(unittest.TestCase):
    def test_no_cell_inference(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'3.csv.zip'
            s=io.StringIO(); writer=csv.DictWriter(s,fieldnames=['x','y','frame','track_fixed','ignore']); writer.writeheader(); writer.writerow(dict(x=1,y=2,frame=1,track_fixed=7,ignore='FALSE'))
            with zipfile.ZipFile(p,'w') as z:z.writestr('3.csv',s.getvalue())
            result=audit_archive(p)
            self.assertFalse(result['cell_level'])
            self.assertEqual(result['whole_organism_track_ids'],1)
            self.assertEqual(result['rows'],1)
    def test_reject_other_names(self):
        with self.assertRaises(ValueError): audit_archive('/tmp/arbitrary.zip')

if __name__=='__main__':unittest.main()
