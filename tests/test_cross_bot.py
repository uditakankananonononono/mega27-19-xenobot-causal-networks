import unittest
import numpy as np
from src.cross_bot import evaluate

class CrossBotTests(unittest.TestCase):
    def test_no_heldout_in_training(self):
        train={'01':np.ones((10,30)),'02':np.ones((10,30))}
        with self.assertRaises(ValueError):evaluate(train,'01',np.ones((10,30)))
    def test_permutation_invariance(self):
        rng=np.random.default_rng(8)
        train={'01':rng.normal(size=(22,30)),'02':rng.normal(size=(24,30))}
        bot=rng.normal(size=(23,30));a=evaluate(train,'03',bot)
        bot=bot[::-1];train={k:v[::-1] for k,v in train.items()}
        b=evaluate(train,'03',bot)
        self.assertAlmostEqual(a.population_ridge_rmse,b.population_ridge_rmse)
        self.assertAlmostEqual(a.self_ridge_rmse,b.self_ridge_rmse)
    def test_future_labels_not_in_features(self):
        rng=np.random.default_rng(9)
        train={'01':rng.normal(size=(22,30)),'02':rng.normal(size=(24,30))}
        bot=rng.normal(size=(23,30));a=evaluate(train,'03',bot)
        bbot=bot.copy();bbot[:,-1]+=100;b=evaluate(train,'03',bbot)
        self.assertGreater(b.population_ridge_rmse,a.population_ridge_rmse)
if __name__=='__main__':unittest.main()
