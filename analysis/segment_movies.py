"""PIVOT 05 blind structural segmentation of memory-preprint movies 18-20.
Structure-only rules, blind to outcome statistics:
- panels = non-black row/col bands in the temporal-average frame
- analysis boxes = panel boxes minus fixed overlay margins (top 6%, bottom 10%, sides 2%)
- active frames per panel = frames where panel mean luma > 1% of that panel's max
- held-frame cadence = median run length of near-identical consecutive frames
Outputs JSON + prints summary. No outcome statistic is computed here.
"""
import json, subprocess, sys
import numpy as np

W, H = 1920, 1080
MOVIES = {
    "media-20.mp4": {"label": "Movie 18 (baseline, Fig 5)",
                     "panel_map": ["xenobot_i", "xenobot_ii", "embryo_iii", "embryo_iv", "xenobot_v", "xenobot_vi"]},
    "media-21.mp4": {"label": "Movie 19 (embryo extract, Fig 6C-E)",
                     "panel_map": ["before", "during", "3h_post", "24h_post"]},
    "media-22.mp4": {"label": "Movie 20 (ATP, Fig 6F-H)",
                     "panel_map": ["before", "during", "3h_post", "24h_post"]},
}
BASE = "/tmp/movies/"

def frames(path, step=1):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**7)
    n = 0
    fsz = W * H
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        if n % step == 0:
            yield n, np.frombuffer(buf, dtype=np.uint8).reshape(H, W).astype(np.float32)
        n += 1
    p.wait()
    # return total via attribute
    frames.total = n

def bands(profile, thr):
    idx = np.where(profile > thr)[0]
    if len(idx) == 0:
        return []
    out, s, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > 8:  # gap > 8 px ends a band
            out.append((s, prev)); s = i
        prev = i
    out.append((s, prev))
    return out

result = {"generated": "2026-09-29", "rules": {
    "panel_detection": "bands of temporal-mean luma > 3% of max band mean; bands > 8px gap separated",
    "analysis_box": "panel box inset: top 6%, bottom 10%, sides 2% (excludes timestamp text and scale-bar strips)",
    "active_frame": "panel mean luma in analysis box > 1% of panel max mean",
    "cadence": "median run length of consecutive frames with mean abs diff < 0.5% of 255",
}}

for name, meta in MOVIES.items():
    path = BASE + name
    # pass 1: every 10th frame for structure
    acc = np.zeros((H, W), dtype=np.float64); cnt = 0
    for n, fr in frames(path, step=10):
        acc += fr; cnt += 1
    mean_img = acc / max(cnt, 1)
    colprof = mean_img.mean(axis=0); rowprof = mean_img.mean(axis=1)
    cb = bands(colprof, 0.03 * colprof.max())
    rb = bands(rowprof, 0.03 * rowprof.max())
    boxes = []
    for (r0, r1) in rb:
        for (c0, c1) in cb:
            if (r1 - r0) * (c1 - c0) < 0.02 * W * H:
                continue
            if mean_img[r0:r1+1, c0:c1+1].mean() < 0.03 * mean_img.max():
                continue
            boxes.append([c0, r0, c1, r1])
    boxes.sort(key=lambda b: (b[1] // (H // 2), b[0]))  # row-major
    panels = []
    for k, (c0, r0, c1, r1) in enumerate(boxes):
        w, h = c1 - c0, r1 - r0
        ic0 = int(c0 + 0.02 * w); ic1 = int(c1 - 0.02 * w)
        ir0 = int(r0 + 0.06 * h); ir1 = int(r1 - 0.10 * h)
        label = meta["panel_map"][k] if k < len(meta["panel_map"]) else f"panel_{k}"
        panels.append({"panel_index": k, "condition": label,
                       "panel_box_xy": [int(c0), int(r0), int(c1), int(r1)],
                       "analysis_box_xy": [ic0, ir0, ic1, ir1]})
    # pass 2: every frame, per-panel activity + cadence on first panel
    means = {p["condition"]: [] for p in panels}
    prev = None; diffsmall = 0; runlens = []; cur_run = 1
    for n, fr in frames(path, step=1):
        for p in panels:
            c0, r0, c1, r1 = p["analysis_box_xy"]
            means[p["condition"]].append(float(fr[r0:r1, c0:c1].mean()))
        if prev is not None:
            if np.abs(fr - prev).mean() < 0.5:
                cur_run += 1
            else:
                runlens.append(cur_run); cur_run = 1
        prev = fr
    runlens.append(cur_run)
    total = frames.total
    for p in panels:
        m = np.array(means[p["condition"]])
        act = m > 0.01 * m.max()
        # compress to ranges
        ranges, s = [], None
        for i, a in enumerate(act):
            if a and s is None: s = i
            if not a and s is not None: ranges.append([s, i - 1]); s = None
        if s is not None: ranges.append([s, len(act) - 1])
        p["active_frame_ranges"] = ranges
        p["mean_luma_minmax"] = [float(m.min()), float(m.max())]
    result[name] = {"label": meta["label"], "total_frames": total,
                    "fps": 30, "panels": panels,
                    "held_frame_cadence_median": float(np.median(runlens)),
                    "n_frame_runs": len(runlens)}
    print(name, "frames:", total, "panels:", [(p["condition"], p["active_frame_ranges"]) for p in panels],
          "cadence:", np.median(runlens), "runs:", len(runlens))

json.dump(result, open("/tmp/movies/segmentation.json", "w"), indent=1)
print("WROTE /tmp/movies/segmentation.json")
