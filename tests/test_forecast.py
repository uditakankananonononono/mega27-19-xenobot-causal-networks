import unittest
import numpy as np
from src.forecast import score_bot

class ForecastTests(unittest.TestCase):
    def test_finite_and_holdout(self):
        rng=np.random.default_rng(12)
        a=rng.normal(size=(10,100))
        x=score_bot(a)
        self.assertEqual(x.n_cells,10)
        self.assertEqual(x.n_frames,100-1-int(100*.6)-8+1)
        self.assertTrue(np.isfinite(x.population_rmse))
    def test_no_future_leak(self):
        rng=np.random.default_rng(2)
        a=rng.normal(size=(10,100))
        b=a.copy();b[:,-1]+=100
        x=score_bot(a);y=score_bot(b)
        self.assertNotEqual(x.persistence_rmse,y.persistence_rmse)
        self.assertGreater(y.population_rmse,x.population_rmse)
    def test_invalid(self):
        with self.assertRaises(ValueError):score_bot(np.ones((3,4)))
if __name__=='__main__':unittest.main()
