"""REGISTERED PILOT (prereg sec. 8): 10 valid random genomes through the full
2-condition wrapper. Measures per-eval wall-clock ONLY; fitness values are not
used for selection or hypothesis tests."""
import json, random, time, sys
import vxa_scene, fitness, genomes

DRV = "/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain/voxelyze"
OUT = "/tmp/pilot"
SEED = 999  # pilot seed, distinct from stage-1 seeds 1-3

rng = random.Random(SEED)
rows = []
for i in range(10):
    mat, ph = genomes.valid_random_genome(rng)
    nvox = sum(1 for z in mat for r in z for v in r if v)
    for cond, shift in (("A", 0.0), ("B", 0.5)):
        ph2 = [[[v + shift if v + shift <= 1 else v + shift - 2 for v in r] for r in z] for z in ph]
        vxa = vxa_scene.build_vxa(mat, ph2, lattice_dim=0.05, stop_time=11.0, init_cm_time=1.0,
                                  temp_period=0.5, gravity=-0.1,
                                  fitness_file=f"{OUT}/g{i}_{cond}.fitness")
        p = f"{OUT}/g{i}_{cond}.vxa"
        open(p, "w").write(vxa)
        t0 = time.time()
        try:
            traj, fx = fitness.run_eval(p, DRV, f"{OUT}/g{i}_{cond}.fitness", timeout=150)
            fl = fitness.fitness_locomotion(traj, lattice_dim=0.05, init_cm_time=1.0)
            rows.append(dict(genome=i, cond=cond, nvox=nvox, wall=round(time.time()-t0, 2),
                             ok=True, fl=round(fl, 2) if fl is not None else None))
        except Exception as e:
            rows.append(dict(genome=i, cond=cond, nvox=nvox, wall=round(time.time()-t0, 2),
                             ok=False, err=str(e)[:80]))
    print(f"[{i}/10] nvox={nvox} A={rows[-2]['wall']}s B={rows[-1]['wall']}s", flush=True)
    json.dump(rows, open(f"{OUT}/pilot.json", "w"), indent=1)
print("PILOT DONE")
