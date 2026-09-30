"""Prereg sec 6 novelty: min occupancy distance of F>0 GA candidates vs the 4-anchor corpus.
d(G,P) = |G symdiff P| / |G union P|, minimized over the full octahedral group
(48 isometries: 24 proper + 24 improper rotations - superset of the prereg's "24",
making the novelty threshold strictly harder to pass; stated in the result doc)
and the integer translation aligning centers of mass to the nearest voxel."""
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

def isometries():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = np.zeros((3, 3), dtype=int)
            for i, p in enumerate(perm):
                m[i, p] = signs[i]
            mats.append(m)
    return mats  # 48

def transform(s, m, t):
    out = set()
    for p in s:
        q = m @ np.array(p) + t
        out.add(tuple(int(v) for v in q))
    return out

def cm(s):
    a = np.array(list(s), dtype=float)
    return a.mean(axis=0)

def dist(g, p, m):
    t = np.round(cm(g) - m @ cm(p)).astype(int)
    p2 = transform(p, m, t)
    sym = len(g.symmetric_difference(p2)); uni = len(g.union(p2))
    return sym / uni

def main():
    mats = isometries()
    anchors = {}
    adir = "/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain"
    for d in ["Example_1", "Example_2", "Example_3", "Example_withPhaseOffset"]:
        grid, _ = vxa_scene.parse_vxa_structure(os.path.join(adir, d + ".vxa"))
        anchors[d] = occ(grid)
    cands = json.load(open("/tmp/stage1/audit/audit_stage1.json"))["results"]
    out = []
    for r in cands:
        if r["arm"] == "anchors" or not r["pass_all"]:
            continue
        base = {"seed1": "/tmp/stage1/seed1", "seed2": "/tmp/stage1/seed2",
                "seed3": "/tmp/stage1/seed3", "null": "/tmp/stage1/null"}[r["arm"]]
        grid, _ = vxa_scene.parse_vxa_structure(os.path.join(base, r["tag"] + "_A.vxa"))
        g = occ(grid)
        per_anchor = {a: min(dist(g, p, m) for m in mats) for a, p in anchors.items()}
        dmin = min(per_anchor.values())
        nearest = min(per_anchor, key=per_anchor.get)
        out.append(dict(arm=r["arm"], tag=r["tag"], F=r["F"], size=len(g),
                        min_dist=dmin, nearest_anchor=nearest,
                        per_anchor=per_anchor, novel=dmin >= 0.5))
        print(f"{r['arm']:6s} {r['tag']:9s} |G|={len(g):3d} min_d={dmin:.4f} "
              f"nearest={nearest} novel={dmin >= 0.5}", flush=True)
    json.dump(out, open("/tmp/stage1/audit/novelty_stage1.json", "w"), indent=1)
    print("NOVELTY DONE", flush=True)

if __name__ == "__main__":
    main()
