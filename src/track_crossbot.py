"""Cross-bot short-horizon motion predictability in shared arenas.

Locked protocol: docs/TRACK_CROSSBOT_PROTOCOL.md (SHA-256 in .sha256).
Methods/dynamical artifact only; no biological claim under any outcome.
"""
import csv, io, json, zipfile
from collections import defaultdict

import numpy as np

H = 10          # target horizon in frames (seconds)
W = 10          # own-history window in frames
PENALTY = 1.0
N_NULL = 100
SEED = 20260927


def load_replicate(zip_path, inner_name):
    """Return {track_id: (frames int array, xy float array)} with ignore rows dropped."""
    with zipfile.ZipFile(zip_path) as zf:
        raw = zf.read(inner_name).decode('utf-8', 'replace')
    rows = defaultdict(list)
    for row in csv.DictReader(io.StringIO(raw)):
        if row['ignore'].strip().upper() == 'TRUE':
            continue
        rows[row['track_fixed']].append(
            (int(float(row['frame'])), float(row['x']), float(row['y'])))
    out = {}
    for tid, rec in rows.items():
        rec.sort()
        frames = np.array([r[0] for r in rec], dtype=np.int64)
        xy = np.array([[r[1], r[2]] for r in rec], dtype=float)
        out[tid] = (frames, xy)
    return out


def velocity_series(frames, xy):
    """Velocity at frame f = pos(f)-pos(f-1) where both exist and are consecutive.

    Returns dict frame -> velocity vector."""
    vel = {}
    idx = {f: i for i, f in enumerate(frames)}
    for i in range(1, len(frames)):
        f, fp = frames[i], frames[i - 1]
        if f - fp == 1:
            vel[f] = xy[i] - xy[i - 1]
    return vel


def build_rows(tracks):
    """Build per-bot (t, own features, target) and the population table.

    Returns list per bot: (t_array, own_feat [n,2W], target [n,2]),
    and pop table: dict t -> (mean_vel[2], mean_speed, ) computed per focal later.
    To keep it exact per focal, we store per-frame per-bot velocities."""
    vels = {tid: velocity_series(f, xy) for tid, (f, xy) in tracks.items()}
    poss = {tid: {f: xy[i] for i, f in enumerate(fr)} for tid, (fr, xy) in tracks.items()}
    per_bot = {}
    for tid, vel in vels.items():
        ts = sorted(vel)
        tset = set(vel)
        rows_t, rows_x, rows_y = [], [], []
        for t in ts:
            if all((t - k) in tset for k in range(1, W + 1)) and (t + H) in tset and (t + H - 1) in tset:
                rows_t.append(t)
                rows_x.append(np.concatenate([vel[t - k] for k in range(1, W + 1)]))
                rows_y.append(vel[t + H])
        per_bot[tid] = (np.array(rows_t, dtype=np.int64),
                        np.array(rows_x) if rows_t else np.zeros((0, 2 * W)),
                        np.array(rows_y) if rows_t else np.zeros((0, 2)))
    return vels, poss, per_bot


def pop_features(vels, poss, focal_id, t):
    """Population features at frame t-1: others' mean velocity vector, others' mean
    speed, focal distance to centroid of others (protocol's 4 scalars)."""
    tm1 = t - 1
    others = [v[tm1] for tid, v in vels.items() if tid != focal_id and tm1 in v]
    opos = [p[tm1] for tid, p in poss.items() if tid != focal_id and tm1 in p]
    if not others or not opos or tm1 not in poss[focal_id]:
        return None
    m = np.mean(others, axis=0)
    speeds = [np.hypot(*o) for o in others]
    centroid = np.mean(opos, axis=0)
    dist = float(np.hypot(*(poss[focal_id][tm1] - centroid)))
    return np.array([m[0], m[1], np.mean(speeds), dist])


def ridge_fit(X, y):
    Xd = np.concatenate([np.ones((len(X), 1)), X], axis=1)
    pen = np.eye(Xd.shape[1]) * PENALTY
    pen[0, 0] = 0.0
    return np.linalg.solve(Xd.T @ Xd + pen, Xd.T @ y)


def predict(coef, X):
    Xd = np.concatenate([np.ones((len(X), 1)), X], axis=1)
    return Xd @ coef


def rel_gain(rmse_own, rmse_full):
    return (rmse_own - rmse_full) / rmse_own if rmse_own > 0 else 0.0


def score_replicate(tracks, null_shifts=N_NULL, seed=SEED):
    ids = sorted(tracks)
    test_ids = set(ids[::3])
    train_ids = [t for t in ids if t not in test_ids]
    vels, poss, per_bot = build_rows(tracks)

    def rows_for(tid_list, shifted=None):
        Xo, Xf, Y = [], [], []
        for tid in tid_list:
            ts, own, tgt = per_bot[tid]
            for i, t in enumerate(ts):
                pf = pop_features(vels, poss, tid, t)
                if pf is None:
                    continue
                Xo.append(own[i])
                Xf.append(np.concatenate([own[i], pf]))
                Y.append(tgt[i])
        if not Xo:
            return None
        return np.array(Xo), np.array(Xf), np.array(Y)

    train = rows_for(train_ids)
    test = rows_for(sorted(test_ids))
    if train is None or test is None or len(test[0]) < 10:
        return None
    coef_o = ridge_fit(train[0], train[2])
    coef_f = ridge_fit(train[1], train[2])
    rmse = lambda a, b: float(np.sqrt(np.mean((a - b) ** 2)))
    r_own = rmse(predict(coef_o, test[0]), test[2])
    r_full = rmse(predict(coef_f, test[1]), test[2])
    gain = rel_gain(r_own, r_full)

    # Alignment null: circularly shift each test focal's target series relative to
    # features is wrong; the protocol shifts the POPULATION series. Implement by
    # shifting population features across time within the test design matrix.
    rng = np.random.default_rng(seed)
    nulls = []
    n = len(test[1])
    for _ in range(null_shifts):
        k = int(rng.integers(1, n))
        Xf_shift = test[1].copy()
        Xf_shift[:, 2 * W:] = np.roll(Xf_shift[:, 2 * W:], k, axis=0)
        nulls.append(rel_gain(r_own, rmse(predict(coef_f, Xf_shift), test[2])))
    pct = float(np.mean([g >= gain for g in nulls]))
    return {'n_bots': len(ids), 'n_test_bots': len(test_ids),
            'n_train_rows': len(train[0]), 'n_test_rows': n,
            'rmse_own': r_own, 'rmse_full': r_full, 'rel_gain': gain,
            'null_mean': float(np.mean(nulls)), 'null_p95': float(np.percentile(nulls, 95)),
            'null_frac_ge_real': pct}


def exact_signflip_p(gains):
    n = len(gains)
    k = sum(1 for g in gains if g > 0)
    from math import comb
    tail = sum(comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


if __name__ == '__main__':
    import sys, os
    raw = sys.argv[1]
    out = {}
    for rep in ['3','4','5','6','7','8','9','10','11','12','13','14']:
        tracks = load_replicate(os.path.join(raw, f'{rep}.csv.zip'), f'{rep}.csv')
        res = score_replicate(tracks)
        if res:
            out[rep] = res
            print(rep, json.dumps(res))
    gains = [v['rel_gain'] for v in out.values()]
    summary = {'replicates': len(out),
               'median_rel_gain': float(np.median(gains)),
               'mean_rel_gain': float(np.mean(gains)),
               'n_positive': sum(1 for g in gains if g > 0),
               'signflip_p_two_sided': exact_signflip_p(gains),
               'n_real_above_null95': sum(1 for v in out.values() if v['rel_gain'] > v['null_p95'])}
    print('SUMMARY', json.dumps(summary))
    json.dump({'per_replicate': out, 'summary': summary},
              open('results/track-crossbot.json', 'w'), indent=1)
