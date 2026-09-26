import tempfile
import unittest
from src.cross_bot_benchmark import run
class BenchmarkTests(unittest.TestCase):
    def test_missing_data_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):run(d)
if __name__=='__main__':unittest.main()
