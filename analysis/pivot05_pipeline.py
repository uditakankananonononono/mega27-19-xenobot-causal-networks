"""PIVOT 05 locked-prereg pipeline (docs/PIVOT_05_MOVIE_CALCIUM_PROTOCOL.md, SHA e709ca53).
Phase 1: per panel, decode green channel over analysis_frame_range (analysis_box_xy crop),
adaptive dedupe of held/looped frames (collapse runs where consecutive diff <
0.2 * max diff of first 60 frames; blind, structural), bandpass (remove lowest and highest
10% of 0..Nyquist), store filtered (T,P) array, record global max amplitude across panels.
Phase 2: zero samples < 1% of global max amplitude; per-pixel temporal variance; top-10%
and top-50% subsets; median variance; median cosine cross-correlation over 100k random
pairs (seed 20260929); 200 circular-shift nulls (per-pair random lag on j-series);
compression guard (mean abs frame-to-frame diff). Stats JSON checkpointed per panel.
"""
import json, os, subprocess
import numpy as np
import scipy.fft

BASE = "/tmp/movies"
SEG = json.load(open("/tmp/movies/segmentation.json"))
FILT_DIR = "/tmp/movies/filtered"
STATS_DIR = "/tmp/movies/stats"
os.makedirs(FILT_DIR, exist_ok=True)
os.makedirs(STATS_DIR, exist_ok=True)
SEED = 20260929
N_PAIRS = 100_000
N_NULL = 200

def decode_panel(movie, box, frange):
    """Stream green-channel cropped frames in [f0, f1]; yield np arrays one at a time."""
    c0, r0, c1, r1 = box
    f0, f1 = frange
    w, h = c1 - c0, r1 - r0
    nframes = f1 - f0 + 1
    cmd = ["ffmpeg", "-v", "error", "-i", os.path.join(BASE, movie),
           "-vf", f"select='between(n\\,{f0}\\,{f1})',crop={w}:{h}:{c0}:{r0}",
           "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**7)
    fsz = w * h * 3
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        yield np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)[..., 1]
    p.wait()

def panel_diffs(movie, box, frange):
    """Pass 1: consecutive-frame mean abs diffs (float32, gray) over the range."""
    c0, r0, c1, r1 = box
    f0, f1 = frange
    w, h = c1 - c0, r1 - r0
    cmd = ["ffmpeg", "-v", "error", "-i", os.path.join(BASE, movie),
           "-vf", f"select='between(n\\,{f0}\\,{f1})',crop={w}:{h}:{c0}:{r0}",
           "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**7)
    fsz = w * h
    prev = None
    out = []
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        f = np.frombuffer(buf, dtype=np.uint8).reshape(h, w).astype(np.float32)
        if prev is not None:
            out.append(float(np.abs(f - prev).mean()))
        prev = f
    p.wait()
    return np.array(out)

def dedupe_adaptive(movie, box, frange):
    """Two-pass plateau dedupe. Pass 1: diffs, threshold = midpoint of 2-means on log10 diffs.
    Pass 2: keep only plateau frames (diff to BOTH neighbors < thr) - these are the stable
    held frames; cross-fade transition frames are excluded. If plateau fraction < 20%, the
    panel updates every frame (no holds) and ALL frames are kept. Blind and structural."""
    diffs = panel_diffs(movie, box, frange)
    n_raw = len(diffs) + 1
    if n_raw < 8:
        return np.zeros((0, 1, 1), dtype=np.float32), n_raw, 0.0, "too_few"
    x = np.log10(diffs + 1e-3)
    c = np.array([x.min(), x.max()])
    for _ in range(50):
        lab = np.abs(x[:, None] - c[None, :]).argmin(1)
        nc = np.array([x[lab == 0].mean() if (lab == 0).any() else c[0],
                       x[lab == 1].mean() if (lab == 1).any() else c[1]])
        if np.allclose(nc, c):
            break
        c = nc
    thr = float(10 ** ((c[0] + c[1]) / 2) - 1e-3)
    stable_prev = diffs < thr  # stable_prev[i]: frame i+1 is close to frame i
    n_fr = n_raw
    plateau = np.zeros(n_fr, dtype=bool)
    plateau[0] = stable_prev[0] if len(stable_prev) else False
    plateau[-1] = stable_prev[-1] if len(stable_prev) else False
    if n_fr > 2:
        plateau[1:-1] = stable_prev[:-1] & stable_prev[1:]
    frac = plateau.mean()
    if frac < 0.20:
        keep_idx = None  # keep all
        mode = "continuous_all_kept"
    else:
        keep_idx = np.where(plateau)[0]
        mode = "plateau"
    c0, r0, c1, r1 = box
    f0, f1 = frange
    w, h = c1 - c0, r1 - r0
    cmd = ["ffmpeg", "-v", "error", "-i", os.path.join(BASE, movie),
           "-vf", f"select='between(n\\,{f0}\\,{f1})',crop={w}:{h}:{c0}:{r0}",
           "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**7)
    fsz = w * h * 3
    kept = []
    n = 0
    want = set(keep_idx.tolist()) if keep_idx is not None else None
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        if want is None or n in want:
            kept.append(np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)[..., 1].astype(np.float32))
        n += 1
    p.wait()
    if not kept:
        return np.zeros((0, 1, 1), dtype=np.float32), n_raw, thr, "empty"
    return np.stack(kept), n_raw, thr, mode + f"_frac={frac:.3f}"

def bandpass(series):
    """Remove lowest and highest 10% of 0..Nyquist per pixel. float32 scipy FFT, column-chunked
    to stay within 1GB RAM. series: (T, P) float32."""
    T, P = series.shape
    out = np.empty_like(series)
    kmax_full = T // 2
    klo = int(np.floor(0.1 * kmax_full))
    khi = int(np.ceil(0.9 * kmax_full))
    CH = 20000
    for s in range(0, P, CH):
        blk = series[:, s:s + CH]
        F = scipy.fft.rfft(blk, axis=0, workers=2)
        F[:klo + 1, :] = 0
        F[khi:, :] = 0
        out[:, s:s + CH] = scipy.fft.irfft(F, n=T, axis=0, workers=2).astype(np.float32)
    return out

def panel_key(movie, cond):
    return movie.replace(".mp4", "") + "__" + cond

meta = {}
for movie in ["media-20.mp4", "media-21.mp4", "media-22.mp4"]:
    for p in SEG[movie]["panels"]:
        key = panel_key(movie, p["condition"])
        npy = os.path.join(FILT_DIR, key + ".npy")
        if os.path.exists(npy):
            arr = np.load(npy)
            meta[key] = json.load(open(npy + ".meta.json"))
            continue
        dd, n_raw, dthr, dmode = dedupe_adaptive(movie, p["analysis_box_xy"], p["analysis_frame_range"])
        ser = dd.reshape(dd.shape[0], -1)
        if ser.shape[0] < 8:
            print("SKIP too few frames:", key, ser.shape, flush=True)
            continue
        filt = bandpass(ser)
        np.save(npy, filt)
        m = {"n_raw": int(n_raw), "n_dedup": int(dd.shape[0]), "dedup_diff_threshold": dthr, "dedup_mode": dmode,
             "shape": list(filt.shape), "absmax": float(np.abs(filt).max())}
        json.dump(m, open(npy + ".meta.json", "w"))
        meta[key] = m
        print("phase1", key, m, flush=True)
        del dd, ser, filt

A_MAX = max(m["absmax"] for m in meta.values())
json.dump({"A_max": A_MAX, "panels": meta}, open(os.path.join(STATS_DIR, "_phase1_meta.json"), "w"), indent=1)
print("A_MAX", A_MAX, flush=True)

def pair_cosines(X, idx_i, idx_j):
    Xi = X[:, idx_i]; Xj = X[:, idx_j]
    ni = np.sqrt((Xi * Xi).sum(0)); nj = np.sqrt((Xj * Xj).sum(0))
    valid = (ni > 0) & (nj > 0)
    dots = (Xi * Xj).sum(0)
    cos = np.full(len(idx_i), np.nan, dtype=np.float64)
    cos[valid] = dots[valid] / (ni[valid] * nj[valid])
    return cos, valid

for movie in ["media-20.mp4", "media-21.mp4", "media-22.mp4"]:
    for p in SEG[movie]["panels"]:
        key = panel_key(movie, p["condition"])
        outpath = os.path.join(STATS_DIR, key + ".json")
        if os.path.exists(outpath):
            continue
        X = np.load(os.path.join(FILT_DIR, key + ".npy"))
        T, P = X.shape
        thr = 0.01 * A_MAX
        X[np.abs(X) < thr] = 0.0
        guard = float(np.abs(np.diff(X, axis=0)).mean())
        # chunked population variance
        var = np.empty(P, dtype=np.float64)
        CH = 20000
        for s in range(0, P, CH):
            blk = X[:, s:s + CH].astype(np.float64)
            var[s:s + CH] = blk.var(axis=0)
            del blk
        res = {"movie": movie, "condition": p["condition"], "T": int(T), "P": int(P),
               "threshold_1pct_of_Amax": thr, "compression_guard_mean_abs_framediff": guard,
               "seed": SEED, "n_pairs": N_PAIRS, "n_null": N_NULL,
               "n_dedup": meta[key]["n_dedup"], "n_raw": meta[key]["n_raw"],
               "dedup_diff_threshold": meta[key]["dedup_diff_threshold"], "dedup_mode": meta[key].get("dedup_mode")}
        rng = np.random.default_rng(SEED)
        for frac, tag in [(0.10, "top10"), (0.50, "top50")]:
            k = max(2, int(np.ceil(frac * P)))
            subset = np.argpartition(var, -k)[-k:]
            med_var = float(np.median(var[subset]))
            S = np.ascontiguousarray(X[:, subset])  # (T, k)
            m = len(subset)
            idx_i = rng.integers(0, m, N_PAIRS)
            idx_j = rng.integers(0, m, N_PAIRS)
            # empirical 100k pairs in chunks of 20k
            cos = np.full(N_PAIRS, np.nan, dtype=np.float64)
            norms_i_all = np.empty(N_PAIRS); norms_j_all = np.empty(N_PAIRS)
            for s0 in range(0, N_PAIRS, 20000):
                sl = slice(s0, min(s0 + 20000, N_PAIRS))
                c, v = pair_cosines(S, idx_i[sl], idx_j[sl])
                cos[sl] = c
                norms_i_all[sl] = np.sqrt((S[:, idx_i[sl]] ** 2).sum(0))
                norms_j_all[sl] = np.sqrt((S[:, idx_j[sl]] ** 2).sum(0))
            med_cos = float(np.nanmedian(cos))
            n_valid = int(np.isfinite(cos).sum())
            # nulls: 25k pairs x 200 shifts (null pair count not fixed by prereg; recorded here)
            NULL_PAIRS = 25000
            null_med = []
            tgrid = np.arange(T)
            Si = np.ascontiguousarray(S[:, idx_i[:NULL_PAIRS]])
            ni = norms_i_all[:NULL_PAIRS]
            nj = norms_j_all[:NULL_PAIRS]
            for it in range(N_NULL):
                lags = rng.integers(1, T, NULL_PAIRS)
                Yj = np.take_along_axis(S[:, idx_j[:NULL_PAIRS]], (tgrid[:, None] + lags[None, :]) % T, axis=0)
                dots = (Si * Yj).sum(0)
                cc = dots / (ni * nj + 1e-12)
                cc[(ni == 0) | (nj == 0)] = np.nan
                null_med.append(float(np.nanmedian(cc)))
                del Yj
            null_med = np.array(null_med)
            res[tag] = {"n_subset_pixels": int(m), "median_variance": med_var,
                        "median_xcorr": med_cos, "n_valid_pairs": n_valid,
                        "null_pairs": NULL_PAIRS,
                        "null_median_xcorr_mean": float(null_med.mean()),
                        "null_median_xcorr_std": float(null_med.std()),
                        "null_frac_ge_empirical": float((null_med >= med_cos).mean())}
            del S, Si
        json.dump(res, open(outpath, "w"), indent=1)
        print("phase2", key, {t: round(res[t]["median_xcorr"], 4) for t in ("top10", "top50")}, flush=True)
print("DONE", flush=True)
