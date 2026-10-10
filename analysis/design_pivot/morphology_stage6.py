"""Stage-6 report-only secondary (amendment-08 sec. 4): morphology-convergence follow-up.
Stage-5's registered finding (NEGATIVE_REGISTER 20): all stage-5 winners were morphologically
convergent (occupancy min_d 0.0000-0.0217 vs each other); gains came from actuation, not shape.
This measures occupancy min_d of each stage-6 seed's FINAL POPULATION (g23, i0-19) vs the
stage-5 champion's occupancy, using the same distance as novelty_stage5 (48 isometries +
integer translation aligning centers of mass). Descriptive only."""
import itertools, json, os, sys
import numpy as np
sys.path.insert(0, ".")
import vxa_scene

def occ(grid):
    s = set()
    for z, layer in enumerate(grid):
        for y, row in enumerate(layer):
            for x, v in enumerate(row):
                if v > 0:
                    s.add((x, y, z))
    return s

def occ_from_mat(mat):
    s = set()
    for z, layer in enumerate(mat):
        for y, row in enumerate(layer):
            for x, v in enumerate(row):
                if v > 0:
                    s.add((x, y, z))
    return s

def isometries():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = np.zeros((3, 3), dtype=int)
            for i, p in enumerate(perm):
                m[i, p] = signs[i]
            mats.append(m)
    return mats

def transform(s, m, t):
    out = set()
    for p in s:
        q = m @ np.array(p) + t
        out.add(tuple(int(v) for v in q))
    return out

def cm(s):
    return np.array(list(s), dtype=float).mean(axis=0)

def dist(g, p, m):
    t = np.round(cm(g) - m @ cm(p)).astype(int)
    p2 = transform(p, m, t)
    sym = len(g.symmetric_difference(p2)); uni = len(g.union(p2))
    return sym / uni

def main():
    mats = isometries()
    ch = json.load(open("../../data/stage6-champions.json"))
    champ = occ_from_mat(ch["stage5_champ_seed20_g23_i0"]["genome"][0])
    print("champion |G| =", len(champ), flush=True)
    out = {}
    for sd in (30, 31, 32):
        rows = []
        for i in range(20):
            p = f"/tmp/stage6/seed{sd}/g23_i{i}_A.vxa"
            if not os.path.exists(p):
                continue
            grid, _ = vxa_scene.parse_vxa_structure(p)
            g = occ(grid)
            d = min(dist(g, champ, m) for m in mats)
            rows.append(dict(i=i, size=len(g), min_d_vs_champ=round(d, 4)))
            print(f"seed{sd} g23_i{i} |G|={len(g):3d} min_d_vs_champ={d:.4f}", flush=True)
        ds = [r["min_d_vs_champ"] for r in rows]
        out[f"seed{sd}"] = dict(rows=rows, min=min(ds), median=float(np.median(ds)), max=max(ds))
    json.dump(out, open("/tmp/stage6/morphology_stage6.json", "w"), indent=1)
    print("MORPHOLOGY DONE", flush=True)

if __name__ == "__main__":
    main()
