import tempfile
import unittest
from pathlib import Path
import numpy as np
from src.audit_calcium import audit_folder

class CalciumTests(unittest.TestCase):
    def test_missing_bots_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):audit_folder(d)
    def test_pickle_not_needed(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(1,29):np.savez(Path(d)/f'xenobot_series_{i:02}.npz',np.ones((3,4)))
            o=audit_folder(d);self.assertEqual(len(o['matrices']),28)
            self.assertEqual(o['matrices'][0]['dimension_0'],3)
            self.assertIn('not direct voltage',o['caveats'][0])
if __name__=='__main__':unittest.main()
