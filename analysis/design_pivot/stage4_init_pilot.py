"""Stage-4 pilot: broader initial-morphology ensemble. Four constructive families, each producing
valid genomes (genomes.is_valid) at min_d >= 0.5 vs the locked 27-design corpus. Measures per-family
yield, min_d vs corpus, and pairwise diversity of the ensemble. No fitness compute."""
import json, random, sys
import numpy as np
sys.path.insert(0, ".")
import genomes, ga
import novelty_stage2 as nov

NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
N_TARGET = int(genomes.MIN_FILL * NX * NY * NZ)  # 224
NEI = ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))

def mat_from_cells(S, rng):
    mat = [[[rng.randint(1, 4) if (x, y, z) in S else 0 for x in range(NX)] for y in range(NY)] for z in range(NZ)]
    if not any(mat[z][y][x] in (3, 4) for z in range(NZ) for y in range(NY) for x in range(NX)):
        x0, y0, z0 = next(iter(S)); mat[z0][y0][x0] = 3
    ph = [[[rng.uniform(-1, 1) for _ in range(NX)] for _ in range(NY)] for _ in range(NZ)]
    return mat, ph

def family_shell(rng):
    return ga.constrained_random_genome(rng)

def ellipsoid_cells(cx, cy, cz, rx, ry, rz):
    S = set()
    for z in range(NZ):
        for y in range(NY):
            for x in range(NX):
                if ((x-cx)/rx)**2 + ((y-cy)/ry)**2 + ((z-cz)/rz)**2 <= 1.0:
                    S.add((x, y, z))
    return S

def family_ellipsoid(rng):
    """Off-center compact ellipsoid, random radii/orientation-ish, scaled to exactly N_TARGET."""
    cx, cy, cz = rng.uniform(1.5, NX-1.5), rng.uniform(1.5, NY-1.5), rng.uniform(1.0, NZ-1.0)
    rx, ry, rz = rng.uniform(2.0, 5.0), rng.uniform(2.0, 5.0), rng.uniform(1.5, 4.5)
    lo, hi = 0.2, 3.0
    best = None
    for _ in range(40):  # bisect scale to hit N_TARGET exactly
        s = (lo + hi) / 2
        S = ellipsoid_cells(cx, cy, cz, rx*s, ry*s, rz*s)
        if len(S) == N_TARGET:
            best = S; break
        if len(S) < N_TARGET: lo = s
        else: hi = s
        best = S
    if best is None or len(best) != N_TARGET:
        return None
    return mat_from_cells(best, rng)

def family_strata(rng):
    """Random-axis stratified layers: per-layer random 2D blobs seeded from the previous layer."""
    axis = rng.randrange(3)
    lim = (NX, NY, NZ)[axis]
    nlayers = rng.randint(max(2, lim - 3), lim)
    start = rng.randint(0, lim - nlayers)
    weights = sorted(rng.uniform(0.3, 1.0) for _ in range(nlayers))
    tot = sum(weights)
    counts = [int(N_TARGET * w / tot) for w in weights]
    counts[-1] += N_TARGET - sum(counts)
    CAP = 56
    for _ in range(20):  # redistribute overflow to layers with capacity
        over = [i for i, c in enumerate(counts) if c > CAP]
        if not over: break
        for i in over:
            excess = counts[i] - CAP
            counts[i] = CAP
            for j in sorted(range(len(counts)), key=lambda j: counts[j]):
                take = min(excess, CAP - counts[j])
                counts[j] += take; excess -= take
                if not excess: break
    if any(c > CAP for c in counts):
        return None
    S = set()
    prev2d = None
    for li in range(nlayers):
        L = start + li
        want = counts[li]
        layer = set()
        if prev2d:
            seed2 = rng.choice(list(prev2d))
        else:
            seed2 = (rng.randrange(NX), rng.randrange(NY))
        layer.add(seed2)
        guard = 0
        while len(layer) < want and guard < 4000:
            guard += 1
            (x, y) = rng.choice(list(layer))
            d = rng.randrange(4)
            n2 = (x + (1 if d == 0 else -1 if d == 1 else 0), y + (1 if d == 2 else -1 if d == 3 else 0))
            if 0 <= n2[0] < NX and 0 <= n2[1] < NY:
                layer.add(n2)
        if len(layer) < max(4, want // 2):
            return None
        for (x, y) in layer:
            c = (x, y, L) if axis == 2 else ((x, L, y) if axis == 1 else (L, x, y))
            S.add(c)
        prev2d = layer
    if len(S) != N_TARGET:
        return None
    return mat_from_cells(S, rng)

def family_core_appendage(rng):
    """Compact ellipsoid core plus 2-4 random-walk appendages."""
    cx, cy, cz = rng.uniform(2, NX-2), rng.uniform(2, NY-2), rng.uniform(1.5, NZ-1.5)
    r0 = rng.uniform(3.0, 4.5)
    core = ellipsoid_cells(cx, cy, cz, r0, r0*rng.uniform(0.7,1.0), r0*rng.uniform(0.6,1.0))
    core_size = min(len(core), rng.randint(150, 190))
    while len(core) > core_size:  # trim outermost cells
        cmax = max(core, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2)
        core.discard(cmax)
    S = set(core)
    if not S: return None
    n_app = rng.randint(2, 4)
    budget = N_TARGET - len(S)
    for a in range(n_app):
        remaining = N_TARGET - len(S)
        if remaining <= 0: break
        steps = remaining // (n_app - a) if a < n_app - 1 else remaining
        surf = [p for p in S if any((p[0]+dx, p[1]+dy, p[2]+dz) not in S for dx,dy,dz in NEI)]
        cur = rng.choice(surf)
        walk = []
        for _ in range(min(steps, remaining)):
            dx, dy, dz = NEI[rng.randrange(6)]
            n = (cur[0]+dx, cur[1]+dy, cur[2]+dz)
            if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ:
                cur = n
                if n not in S:
                    walk.append(n)
        for w in walk[:steps]:
            S.add(w)
    guard = 0
    while len(S) < N_TARGET and guard < 20000:  # frontier top-up
        guard += 1
        surf = [p for p in S if any((p[0]+dx, p[1]+dy, p[2]+dz) not in S
                                    and 0 <= p[0]+dx < NX and 0 <= p[1]+dy < NY and 0 <= p[2]+dz < NZ
                                    for dx,dy,dz in NEI)]
        if not surf: return None
        x, y, z = rng.choice(surf)
        dx, dy, dz = NEI[rng.randrange(6)]
        n = (x+dx, y+dy, z+dz)
        if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ and n not in S:
            S.add(n)
    if len(S) != N_TARGET:
        return None
    return mat_from_cells(S, rng)

FAMILIES = dict(shell=family_shell, ellipsoid=family_ellipsoid, strata=family_strata,
                core_appendage=family_core_appendage)

def pairwise_min_d(occs, mats48):
    ds = []
    for i in range(len(occs)):
        for j in range(i + 1, len(occs)):
            g, p = occs[i], occs[j]
            ds.append(min(nov.dist(g, p, m) for m in mats48))
    return ds

def main():
    rng = random.Random(20261008)
    ga.load_corpus("/home/sandbox/mega27-19-xenobot-causal-networks/data/stage3-corpus27.json", 0.5)
    mats48 = nov.isometries()
    per = {k: dict(draws=0, valid=0, min_ds=[]) for k in FAMILIES}
    ensemble = []
    for name, fn in FAMILIES.items():
        for _ in range(15):
            per[name]["draws"] += 1
            try:
                out = fn(rng)
            except RuntimeError:
                out = None
            if out is None:
                continue
            mat, ph = out
            if not genomes.is_valid(mat):
                continue
            d = ga.min_dist_to_corpus(mat)
            if d < 0.5:
                continue
            per[name]["valid"] += 1
            per[name]["min_ds"].append(round(d, 4))
            ensemble.append((name, ga.occ_of_mat(mat)))
    occs = [o for _, o in ensemble]
    ds = pairwise_min_d(occs, mats48)
    ds_sorted = sorted(ds)
    med = ds_sorted[len(ds)//2]
    rep = {name: dict(draws=v["draws"], valid=v["valid"],
                      min_d_range=[min(v["min_ds"]), max(v["min_ds"])] if v["min_ds"] else None)
           for name, v in per.items()}
    print(json.dumps(rep, indent=1))
    print(f"ensemble size: {len(occs)}")
    print(f"pairwise min_d: n={len(ds)} median={med:.4f} p10={ds_sorted[len(ds)//10]:.4f} "
          f"min={ds_sorted[0]:.4f} max={ds_sorted[-1]:.4f}")
    # cross-family vs within-family medians
    cross, within = [], []
    for i in range(len(ensemble)):
        for j in range(i+1, len(ensemble)):
            d = min(nov.dist(ensemble[i][1], ensemble[j][1], m) for m in mats48)
            (cross if ensemble[i][0] != ensemble[j][0] else within).append(d)
    sw, sc = sorted(within), sorted(cross)
    if sw: print(f"within-family pairwise: median={sw[len(sw)//2]:.4f} min={sw[0]:.4f}")
    if sc: print(f"cross-family pairwise: median={sc[len(sc)//2]:.4f} min={sc[0]:.4f}")

if __name__ == "__main__":
    main()
