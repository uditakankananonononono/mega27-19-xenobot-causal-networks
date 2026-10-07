"""Stage-4 evolution runner (amendment-06): broader initial-morphology ensemble.
Identical fitness, audit, GA parameters, mutation operator, and corpus floor (min_d >= 0.5 vs the
locked 27-design corpus) as amendment-05. Only the initialization changes: a stratified four-family
constructive ensemble (shell / ellipsoid / strata / core_appendage), draw i uses family i % 4, used
IDENTICALLY for GA and null initialization. Per-family cull counts and init-population diversity
(median pairwise min_d over the 48-isometry occupancy metric) are recorded.
"""
import json, os, random, sys, time
import numpy as np
import vxa_scene, fitness, genomes

DRV = "/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain/voxelyze"
POP, GENS, TOURNEY, ELITE = 20, 16, 3, 1
SIM_TIMEOUT = 120
LATTICE, STOP_T, INIT_T, PERIOD, GRAV = 0.05, 11.0, 1.0, 0.5, -0.1

CORPUS, FLOOR = None, None
CORPUS_ROT = None  # precomputed: [(rotated set, rounded cm), ...] for all corpus x 48 isometries
CULL = dict(init=0, offspring=0, init_by_family=dict(shell=0, ellipsoid=0, strata=0, core_appendage=0))

def load_corpus(path, floor):
    global CORPUS, CORPUS_ROT, FLOOR
    import numpy as np
    import novelty_stage2 as nov
    man = json.load(open(path))
    CORPUS = [set(map(tuple, d["occupancy"])) for d in man["designs"]]
    FLOOR = floor
    CORPUS_ROT = []
    for p in CORPUS:
        pa = np.array(list(p), dtype=float)
        cmp_ = pa.mean(axis=0)
        for m in nov.isometries():
            pr = (m @ pa.T).T
            cmr = pr.mean(axis=0)
            CORPUS_ROT.append((set(map(tuple, pr.astype(int))), cmr))
    return len(CORPUS)

def occ_of_mat(mat):
    return {(x, y, z) for z in range(genomes.NZ) for y in range(genomes.NY) for x in range(genomes.NX) if mat[z][y][x]}

def min_dist_to_corpus(mat):
    import numpy as np
    g = occ_of_mat(mat)
    ga_ = np.array(list(g), dtype=float)
    cmg = ga_.mean(axis=0)
    best = 1.0
    for pr, cmr in CORPUS_ROT:
        t = np.round(cmg - cmr).astype(int)
        p2 = {(x + t[0], y + t[1], z + t[2]) for (x, y, z) in pr}
        d = len(g.symmetric_difference(p2)) / len(g.union(p2))
        if d < best:
            best = d
    return best

def novel_enough(mat):
    return CORPUS is None or min_dist_to_corpus(mat) >= FLOOR

def constrained_random_genome(rng, max_tries=200):
    """Amendment-05: constructive initialization. Uniform random genomes sit at min_d ~0.26-0.31 vs the
    corpus (occupancy metric saturates for near-full grids), so rejection sampling cannot seed the novel
    region. Instead: randomized greedy connected growth toward corpus-low-coverage cells to exactly
    MIN_FILL voxels, then random material/phase assignment, min_d >= FLOOR verified before returning.
    Used for BOTH GA and null initialization (identical distribution) when a corpus is loaded."""
    if CORPUS is None:
        return genomes.valid_random_genome(rng)
    import numpy as np
    import novelty_stage2 as nov
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    n_target = int(genomes.MIN_FILL * NX * NY * NZ)
    center = np.array([NX / 2, NY / 2, NZ / 2])
    cov = np.zeros((NZ, NY, NX))
    for p in CORPUS:
        if len(p) < 300:
            continue  # small anchors exclude little; the near-full family drives the constraint
        t = np.round(center - nov.cm(p)).astype(int)
        for (x, y, z) in p:
            xx, yy, zz = x + t[0], y + t[1], z + t[2]
            if 0 <= xx < NX and 0 <= yy < NY and 0 <= zz < NZ:
                cov[zz, yy, xx] += 1
    BOX_SYMS = [lambda x, y, z: (x, y, z), lambda x, y, z: (NX - 1 - x, y, z),
                lambda x, y, z: (x, NY - 1 - y, z), lambda x, y, z: (x, y, NZ - 1 - z),
                lambda x, y, z: (NX - 1 - x, NY - 1 - y, z), lambda x, y, z: (NX - 1 - x, y, NZ - 1 - z),
                lambda x, y, z: (x, NY - 1 - y, NZ - 1 - z), lambda x, y, z: (NX - 1 - x, NY - 1 - y, NZ - 1 - z),
                lambda x, y, z: (y, x, z), lambda x, y, z: (NY - 1 - y, x, z),
                lambda x, y, z: (y, NX - 1 - x, z), lambda x, y, z: (y, x, NZ - 1 - z),
                lambda x, y, z: (NY - 1 - y, NX - 1 - x, z), lambda x, y, z: (NY - 1 - y, x, NZ - 1 - z),
                lambda x, y, z: (y, NX - 1 - x, NZ - 1 - z), lambda x, y, z: (NY - 1 - y, NX - 1 - x, NZ - 1 - z)]
    for _ in range(max_tries):
        cells = [(cov[z, y, x], rng.random(), x, y, z)
                 for z in range(NZ) for y in range(NY) for x in range(NX)]
        cells.sort()
        S = {(cells[0][2], cells[0][3], cells[0][4])}
        while len(S) < n_target:
            cands = {}
            for (x, y, z) in S:
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    n = (x + dx, y + dy, z + dz)
                    if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ and n not in S:
                        cands[n] = cov[n[2], n[1], n[0]]
            kbest = sorted(cands, key=cands.get)[:6]
            S.add(kbest[rng.randrange(len(kbest))])  # randomized frontier for init diversity
        sym = BOX_SYMS[rng.randrange(len(BOX_SYMS))]  # random 8x8x7 box symmetry
        S = {sym(x, y, z) for (x, y, z) in S}
        mat = [[[rng.randint(1, 4) if (x, y, z) in S else 0
                 for x in range(NX)] for y in range(NY)] for z in range(NZ)]
        if not any(mat[z][y][x] in (3, 4) for z in range(NZ) for y in range(NY) for x in range(NX)):
            x0, y0, z0 = next(iter(S)); mat[z0][y0][x0] = 3
        ph = [[[rng.uniform(-1, 1) for _ in range(NX)] for _ in range(NY)] for _ in range(NZ)]
        if genomes.is_valid(mat) and novel_enough(mat):
            return mat, ph
        CULL["init"] += 1
    raise RuntimeError("no valid novel genome in %d tries" % max_tries)


NEI6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
N_TARGET4 = int(genomes.MIN_FILL * genomes.NX * genomes.NY * genomes.NZ)

def _mat_from_cells(S, rng):
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    mat = [[[rng.randint(1, 4) if (x, y, z) in S else 0 for x in range(NX)] for y in range(NY)] for z in range(NZ)]
    if not any(mat[z][y][x] in (3, 4) for z in range(NZ) for y in range(NY) for x in range(NX)):
        x0, y0, z0 = next(iter(S)); mat[z0][y0][x0] = 3
    ph = [[[rng.uniform(-1, 1) for _ in range(NX)] for _ in range(NY)] for _ in range(NZ)]
    return mat, ph

def _family_shell(rng):
    """Single-attempt version of the amendment-05 greedy low-coverage growth."""
    import novelty_stage2 as nov
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    center = np.array([NX / 2, NY / 2, NZ / 2])
    cov = np.zeros((NZ, NY, NX))
    for p in CORPUS:
        if len(p) < 300:
            continue
        t = np.round(center - nov.cm(p)).astype(int)
        for (x, y, z) in p:
            xx, yy, zz = x + t[0], y + t[1], z + t[2]
            if 0 <= xx < NX and 0 <= yy < NY and 0 <= zz < NZ:
                cov[zz, yy, xx] += 1
    BOX_SYMS = [lambda x, y, z: (x, y, z), lambda x, y, z: (NX - 1 - x, y, z),
                lambda x, y, z: (x, NY - 1 - y, z), lambda x, y, z: (x, y, NZ - 1 - z),
                lambda x, y, z: (NX - 1 - x, NY - 1 - y, z), lambda x, y, z: (NX - 1 - x, y, NZ - 1 - z),
                lambda x, y, z: (x, NY - 1 - y, NZ - 1 - z), lambda x, y, z: (NX - 1 - x, NY - 1 - y, NZ - 1 - z),
                lambda x, y, z: (y, x, z), lambda x, y, z: (NY - 1 - y, x, z),
                lambda x, y, z: (y, NX - 1 - x, z), lambda x, y, z: (y, x, NZ - 1 - z),
                lambda x, y, z: (NY - 1 - y, NX - 1 - x, z), lambda x, y, z: (NY - 1 - y, x, NZ - 1 - z),
                lambda x, y, z: (y, NX - 1 - x, NZ - 1 - z), lambda x, y, z: (NY - 1 - y, NX - 1 - x, NZ - 1 - z)]
    cells = [(cov[z, y, x], rng.random(), x, y, z)
             for z in range(NZ) for y in range(NY) for x in range(NX)]
    cells.sort()
    S = {(cells[0][2], cells[0][3], cells[0][4])}
    while len(S) < N_TARGET4:
        cands = {}
        for (x, y, z) in S:
            for dx, dy, dz in NEI6:
                n = (x + dx, y + dy, z + dz)
                if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ and n not in S:
                    cands[n] = cov[n[2], n[1], n[0]]
        kbest = sorted(cands, key=cands.get)[:6]
        S.add(kbest[rng.randrange(len(kbest))])
    sym = BOX_SYMS[rng.randrange(len(BOX_SYMS))]
    S = {sym(x, y, z) for (x, y, z) in S}
    return _mat_from_cells(S, rng)

def _ellipsoid_cells(cx, cy, cz, rx, ry, rz):
    S = set()
    for z in range(genomes.NZ):
        for y in range(genomes.NY):
            for x in range(genomes.NX):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2 <= 1.0:
                    S.add((x, y, z))
    return S

def _family_ellipsoid(rng):
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    cx, cy, cz = rng.uniform(1.5, NX - 1.5), rng.uniform(1.5, NY - 1.5), rng.uniform(1.0, NZ - 1.0)
    rx, ry, rz = rng.uniform(2.0, 5.0), rng.uniform(2.0, 5.0), rng.uniform(1.5, 4.5)
    lo, hi = 0.2, 3.0
    best = None
    for _ in range(40):
        s = (lo + hi) / 2
        S = _ellipsoid_cells(cx, cy, cz, rx * s, ry * s, rz * s)
        if len(S) == N_TARGET4:
            best = S; break
        if len(S) < N_TARGET4: lo = s
        else: hi = s
        best = S
    if best is None or len(best) != N_TARGET4:
        return None
    return _mat_from_cells(best, rng)

def _family_strata(rng):
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    axis = rng.randrange(3)
    lim = (NX, NY, NZ)[axis]
    nlayers = rng.randint(max(2, lim - 3), lim)
    start = rng.randint(0, lim - nlayers)
    weights = sorted(rng.uniform(0.3, 1.0) for _ in range(nlayers))
    tot = sum(weights)
    counts = [int(N_TARGET4 * w / tot) for w in weights]
    counts[-1] += N_TARGET4 - sum(counts)
    CAP = 56
    for _ in range(20):
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
        seed2 = rng.choice(list(prev2d)) if prev2d else (rng.randrange(NX), rng.randrange(NY))
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
    if len(S) != N_TARGET4:
        return None
    return _mat_from_cells(S, rng)

def _family_core_appendage(rng):
    NX, NY, NZ = genomes.NX, genomes.NY, genomes.NZ
    cx, cy, cz = rng.uniform(2, NX - 2), rng.uniform(2, NY - 2), rng.uniform(1.5, NZ - 1.5)
    r0 = rng.uniform(3.0, 4.5)
    core = _ellipsoid_cells(cx, cy, cz, r0, r0 * rng.uniform(0.7, 1.0), r0 * rng.uniform(0.6, 1.0))
    core_size = min(len(core), rng.randint(150, 190))
    while len(core) > core_size:
        cmax = max(core, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2 + (p[2] - cz) ** 2)
        core.discard(cmax)
    S = set(core)
    if not S: return None
    n_app = rng.randint(2, 4)
    for a in range(n_app):
        remaining = N_TARGET4 - len(S)
        if remaining <= 0: break
        steps = remaining // (n_app - a) if a < n_app - 1 else remaining
        surf = [p for p in S if any((p[0] + dx, p[1] + dy, p[2] + dz) not in S for dx, dy, dz in NEI6)]
        cur = rng.choice(surf)
        walk = []
        for _ in range(min(steps, remaining)):
            dx, dy, dz = NEI6[rng.randrange(6)]
            n = (cur[0] + dx, cur[1] + dy, cur[2] + dz)
            if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ:
                cur = n
                if n not in S:
                    walk.append(n)
        for w in walk[:steps]:
            S.add(w)
    guard = 0
    while len(S) < N_TARGET4 and guard < 20000:
        guard += 1
        surf = [p for p in S if any((p[0] + dx, p[1] + dy, p[2] + dz) not in S
                                    and 0 <= p[0] + dx < NX and 0 <= p[1] + dy < NY and 0 <= p[2] + dz < NZ
                                    for dx, dy, dz in NEI6)]
        if not surf: return None
        x, y, z = rng.choice(surf)
        dx, dy, dz = NEI6[rng.randrange(6)]
        n = (x + dx, y + dy, z + dz)
        if 0 <= n[0] < NX and 0 <= n[1] < NY and 0 <= n[2] < NZ and n not in S:
            S.add(n)
    if len(S) != N_TARGET4:
        return None
    return _mat_from_cells(S, rng)

FAMILY_ORDER = ["shell", "ellipsoid", "strata", "core_appendage"]
FAMILY_FUNCS = dict(shell=_family_shell, ellipsoid=_family_ellipsoid,
                    strata=_family_strata, core_appendage=_family_core_appendage)

def stratified_init(rng, i):
    """Amendment-06 stratified init: draw i uses family i % 4; up to 200 attempts; culls per family."""
    fam = FAMILY_ORDER[i % 4]
    for _ in range(200):
        out = FAMILY_FUNCS[fam](rng)
        if out is not None:
            mat, ph = out
            if genomes.is_valid(mat) and novel_enough(mat):
                return mat, ph
        CULL["init"] += 1
        CULL["init_by_family"][fam] += 1
    raise RuntimeError("no valid novel genome from family %s in 200 tries" % fam)

def init_diversity(mats):
    """Median pairwise min_d over the 48-isometry occupancy metric (amendment-06 diversity metric)."""
    import novelty_stage2 as nov
    mats48 = nov.isometries()
    occs = [occ_of_mat(m) for m in mats]
    ds = []
    for i in range(len(occs)):
        for j in range(i + 1, len(occs)):
            ds.append(min(nov.dist(occs[i], occs[j], m) for m in mats48))
    ds.sort()
    n = len(ds)
    return dict(n_pairs=n, median=round(ds[n // 2], 4), p10=round(ds[n // 10], 4),
                min=round(ds[0], 4), max=round(ds[-1], 4))

def eval_genome(mat, ph, outdir, tag):
    """Two-stage bidirectional fitness. Returns (F, F_A, F_B or None, n_sims, failed)."""
    os.makedirs(outdir, exist_ok=True)

    def run(shift, ctag):
        ph2 = [[[v + shift if v + shift <= 1 else v + shift - 2 for v in r] for r in z] for z in ph]
        p = os.path.join(outdir, f"{ctag}.vxa")
        open(p, "w").write(vxa_scene.build_vxa(
            mat, ph2, lattice_dim=LATTICE, stop_time=STOP_T, init_cm_time=INIT_T,
            temp_period=PERIOD, gravity=GRAV, fitness_file=p + ".fitness"))
        for attempt in (1, 2):  # one relaunch allowed
            try:
                traj, _ = fitness.run_eval(p, DRV, p + ".fitness", timeout=SIM_TIMEOUT)
                fl = fitness.fitness_locomotion(traj, lattice_dim=LATTICE, init_cm_time=INIT_T)
                if fl is not None:
                    return fl, False
            except Exception:
                pass
        return None, True
    fa, fail_a = run(0.0, tag + "_A")
    if fail_a:
        return float("-inf"), None, None, 1, True
    if fa <= 0:
        return fa, fa, None, 1, False
    fb, fail_b = run(0.5, tag + "_B")
    if fail_b:
        return float("-inf"), fa, None, 2, True
    return min(fa, -fb), fa, fb, 2, False

def mutate(mat, ph, rng):
    m2 = [ [ r[:] for r in z ] for z in mat ]
    p2 = [ [ r[:] for r in z ] for z in ph ]
    for _ in range(rng.randint(1, 6)):
        x, y, z = rng.randrange(genomes.NX), rng.randrange(genomes.NY), rng.randrange(genomes.NZ)
        if rng.random() < 0.5:
            m2[z][y][x] = rng.randint(0, 4)
        else:
            p2[z][y][x] = max(-1.0, min(1.0, p2[z][y][x] + rng.uniform(-0.25, 0.25)))
    return m2, p2

def valid_offspring(mat, ph, rng, log):
    for _ in range(200):
        m2, p2 = mutate(mat, ph, rng)
        if genomes.is_valid(m2) and novel_enough(m2):
            return m2, p2
        if genomes.is_valid(m2):
            CULL["offspring"] += 1
    log.append("re-mutate exhausted; parent clone filled slot")
    return mat, ph

def run_ga(seed):
    rng = random.Random(seed); np.random.seed(seed)
    outdir = f"/tmp/stage4/seed{seed}"; os.makedirs(outdir, exist_ok=True)
    pop = [stratified_init(rng, i) for i in range(POP)]
    div = init_diversity([m for m, _ in pop])
    fam_counts = {f: sum(1 for i in range(POP) if FAMILY_ORDER[i % 4] == f) for f in FAMILY_ORDER}
    print(f"[seed{seed} init diversity] median={div['median']:.4f} min={div['min']:.4f} families={fam_counts}", flush=True)
    history, log = [], []
    for gen in range(GENS):
        scored, nsims, nfail = [], 0, 0
        for i, (mat, ph) in enumerate(pop):
            F, fa, fb, ns, failed = eval_genome(mat, ph, outdir, f"g{gen}_i{i}")
            nsims += ns; nfail += failed
            scored.append(dict(i=i, F=F, F_A=fa, F_B=fb, failed=failed))
        order = sorted(range(POP), key=lambda i: -scored[i]["F"])
        best = scored[order[0]]
        history.append(dict(gen=gen, best_F=best["F"], best_i=order[0],
                            median_F=float(np.median([s["F"] for s in scored if s["F"] > float("-inf")] or [float("nan")])),
                            n_sims=nsims, n_failed=nfail))
        # checkpoint genomes + fitness + rng state
        state = dict(gen=gen, seed=seed, scored=scored, history=history,
                     rng=repr(rng.getstate()), log=log,
                     genomes=[(m, p) for m, p in pop])
        json.dump(state, open(os.path.join(outdir, "checkpoint.json"), "w"))
        print(f"[seed{seed} gen{gen}] best={best['F']:.2f} sims={nsims} fails={nfail}", flush=True)
        if gen == GENS - 1:
            break
        elite = pop[order[0]]
        newpop = [elite]
        while len(newpop) < POP:
            cand = [rng.randrange(POP) for _ in range(TOURNEY)]
            parent = pop[max(cand, key=lambda i: scored[i]["F"])]
            newpop.append(valid_offspring(parent[0], parent[1], rng, log))
        pop = newpop
    json.dump(dict(seed=seed, history=history, final=scored, log=log, cull=dict(CULL), init_diversity=div, init_family_counts=fam_counts),
              open(os.path.join(outdir, "result.json"), "w"), default=str)
    print(f"SEED {seed} DONE", flush=True)

def run_null(nseed=1000):
    rng = random.Random(nseed)
    outdir = f"/tmp/stage4/null{nseed}"; os.makedirs(outdir, exist_ok=True)
    rows = []
    partial_path = os.path.join(outdir, "null.json")
    if os.path.exists(partial_path):
        # Resume: load durable rows, replay-and-discard the same rng draws so the
        # design stream continues at the exact next draw. No re-simming, no change
        # to which designs are drawn or how they are scored.
        rows = json.load(open(partial_path))
        if isinstance(rows, dict):
            rows = rows["rows"]  # saved cull counts are NOT reloaded: the rng replay below re-accumulates them identically
        assert all(r["i"] == k for k, r in enumerate(rows)), "partial rows must be contiguous from 0"
        mats = []
        for k in range(len(rows)):
            m_, _ = stratified_init(rng, k)  # discard fitness; advances the stream identically
            mats.append(m_)
        print(f"[null resume: {len(rows)} durable designs skipped]", flush=True)
    if len(rows) == 0:
        mats = []
    for i in range(len(rows), 480):
        mat, ph = stratified_init(rng, i)
        mats.append(mat)
        F, fa, fb, ns, failed = eval_genome(mat, ph, outdir, f"n{i}")
        rows.append(dict(i=i, F=F, F_A=fa, F_B=fb, failed=failed))
        if i % 20 == 0:
            json.dump(rows, open(os.path.join(outdir, "null.json"), "w"), default=str)
            print(f"[null {i}/480]", flush=True)
    sub_idx = random.Random(999).sample(range(len(mats)), 60)
    div = init_diversity([mats[k] for k in sub_idx])
    fam_counts = {f: sum(1 for i in range(len(mats)) if FAMILY_ORDER[i % 4] == f) for f in FAMILY_ORDER}
    json.dump(dict(rows=rows, cull=dict(CULL), init_diversity=div, init_family_counts=fam_counts), open(os.path.join(outdir, "null.json"), "w"), default=str)
    print("NULL DONE", flush=True)

def run_anchors():
    outdir = "/tmp/stage1/anchors"; os.makedirs(outdir, exist_ok=True)
    demos = ["Example_1", "Example_2", "Example_3", "Example_withPhaseOffset"]
    rows = []
    for d in demos:
        src = f"/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain/{d}.vxa"
        grid, ph = vxa_scene.parse_vxa_structure(src)
        F, fa, fb, ns, failed = eval_genome(grid, ph, outdir, d)
        rows.append(dict(design=d, F=F, F_A=fa, F_B=fb, failed=failed))
        print(f"[anchor {d}] F={F} F_A={fa}", flush=True)
    json.dump(rows, open(os.path.join(outdir, "anchors.json"), "w"), default=str)
    print("ANCHORS DONE", flush=True)

if __name__ == "__main__":
    if "--corpus" in sys.argv:
        ci = sys.argv.index("--corpus")
        fi = sys.argv.index("--floor")
        n = load_corpus(sys.argv[ci + 1], float(sys.argv[fi + 1]))
        print(f"[corpus loaded: {n} designs, floor {sys.argv[fi + 1]}]", flush=True)
        del sys.argv[ci:fi + 2]
    mode = sys.argv[1]
    if mode == "ga":
        run_ga(int(sys.argv[2]))
    elif mode == "null":
        run_null(int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
    elif mode == "anchors":
        run_anchors()
