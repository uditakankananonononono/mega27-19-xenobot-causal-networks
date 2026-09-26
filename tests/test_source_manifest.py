import tempfile
import unittest
from pathlib import Path
from src.source_manifest import manifest

class ManifestTests(unittest.TestCase):
    def test_missing_archives_fail(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):manifest(Path(d))

if __name__=='__main__':unittest.main()
