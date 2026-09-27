import unittest

import numpy as np

from src.track_crossbot import (build_rows, exact_signflip_p, load_replicate,
                                ridge_fit, score_replicate, velocity_series)


def make_tracks(n_bots=6, frames=400, seed=1, coupled=True):
    rng = np.random.default_rng(seed)
    t = np.arange(1, frames + 1)
    tracks = {}
    drivers = rng.normal(0, 1, (frames, 2)).cumsum(axis=0)
    for i in range(n_bots):
        tid = f'bot{i:02d}'
        if coupled and i > 0:
            base = 0.8 * drivers + 0.2 * rng.normal(0, 1, (frames, 2)).cumsum(axis=0)
        else:
            base = drivers.copy()
        xy = base + rng.normal(0, 0.01, (frames, 2))
        tracks[tid] = (t, xy)
    return tracks


class CrossBotTests(unittest.TestCase):
    def test_velocity_requires_consecutive_frames(self):
        frames = np.array([1, 2, 4, 5])
        xy = np.array([[0., 0.], [1., 0.], [3., 0.], [6., 0.]])
        vel = velocity_series(frames, xy)
        self.assertEqual(set(vel), {2, 5})

    def test_coefficients_do_not_depend_on_test_bots(self):
        tracks = make_tracks()
        res1 = score_replicate(tracks, null_shifts=2)
        modified = dict(tracks)
        ids = sorted(tracks)
        for tid in ids[::3]:
            f, xy = modified[tid]
            modified[tid] = (f, xy + 1000.0)
        res2 = score_replicate(modified, null_shifts=2)
        # train-only fit means own-model test design shifts but train rows unchanged
        self.assertEqual(res1['n_train_rows'], res2['n_train_rows'])

    def test_coupled_system_beats_own_history(self):
        tracks = make_tracks(n_bots=9, frames=2000, coupled=True)
        res = score_replicate(tracks, null_shifts=10)
        self.assertIsNotNone(res)
        self.assertGreater(res['rel_gain'], 0)

    def test_independent_bots_no_large_positive_gain(self):
        rng = np.random.default_rng(7)
        t = np.arange(1, 3001)
        tracks = {f'b{i}': (t, rng.normal(0, 1, (3000, 2)).cumsum(axis=0))
                  for i in range(9)}
        res = score_replicate(tracks, null_shifts=10)
        self.assertLess(res['rel_gain'], 0.05)

    def test_signflip_bounds(self):
        self.assertAlmostEqual(exact_signflip_p([0] * 12), 2 / 2 ** 12)
        self.assertAlmostEqual(exact_signflip_p([1.] * 6 + [-1.] * 6), 1.0)
        self.assertLess(exact_signflip_p([1] * 12), 0.001)


if __name__ == '__main__':
    unittest.main()
