"""Stage-1 evolution runner: bidirectional locomotion (prereg + amendments 01/02).

Generational GA (elitism 1, tournament 3, mutation-only), 20 x 16 per seed,
seeds 1-3; two-stage fitness (B only if F_A>0); 120s sim timeout with one relaunch
then F=-inf; checkpoint (genomes+fitness+rng state) every generation.
Shared null and anchors are separate entry points (--mode).
"""
import json, os, random, sys, time
import numpy as np
import vxa_scene, fitness, genomes

DRV = "/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain/voxelyze"
POP, GENS, TOURNEY, ELITE = 20, 16, 3, 1
SIM_TIMEOUT = 120
LATTICE, STOP_T, INIT_T, PERIOD, GRAV = 0.05, 11.0, 1.0, 0.5, -0.1

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
        if genomes.is_valid(m2):
            return m2, p2
    log.append("re-mutate exhausted; parent clone filled slot")
    return mat, ph

def run_ga(seed):
    rng = random.Random(seed); np.random.seed(seed)
    outdir = f"/tmp/stage1/seed{seed}"; os.makedirs(outdir, exist_ok=True)
    pop = [genomes.valid_random_genome(rng) for _ in range(POP)]
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
    json.dump(dict(seed=seed, history=history, final=scored, log=log),
              open(os.path.join(outdir, "result.json"), "w"), default=str)
    print(f"SEED {seed} DONE", flush=True)

def run_null():
    rng = random.Random(1000)
    outdir = "/tmp/stage1/null"; os.makedirs(outdir, exist_ok=True)
    rows = []
    for i in range(480):
        mat, ph = genomes.valid_random_genome(rng)
        F, fa, fb, ns, failed = eval_genome(mat, ph, outdir, f"n{i}")
        rows.append(dict(i=i, F=F, F_A=fa, F_B=fb, failed=failed))
        if i % 20 == 0:
            json.dump(rows, open(os.path.join(outdir, "null.json"), "w"), default=str)
            print(f"[null {i}/480]", flush=True)
    json.dump(rows, open(os.path.join(outdir, "null.json"), "w"), default=str)
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
    mode = sys.argv[1]
    if mode == "ga":
        run_ga(int(sys.argv[2]))
    elif mode == "null":
        run_null()
    elif mode == "anchors":
        run_anchors()
