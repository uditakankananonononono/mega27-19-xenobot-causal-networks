"""Stage-3: Stage-1 prereg sec 7 exploit checks for every design with recorded F > 0.

Scope: seed10-12 final populations (result.json), null 6000/7000 (null.json rows),
anchors (repo stage-1 anchors-result.json, byte-stable). For each F>0 design, the ORIGINAL .vxa scene files
(byte-identical to what was evaluated) are re-run with trajectory capture:
- sec 7.1 trajectory audit: cumulative y-z CM path over the eval <= 0.15 m
- sec 7.2 energy sanity: |F_A|, |F_B| <= 3x largest anchor one-way (condition A) fitness
- sec 7.3 determinism: two re-runs of A and B; F must match the recorded value exactly
- sec 7.4 validity re-check of the genome parsed from the A scene
- sec 7.5 no Fixed regions in the scene
Writes audit_stage4.json under /tmp/stage4/audit/. Read-only on inputs; re-run scenes
go to /tmp/stage4/audit/.
"""
import json, os, re, subprocess, sys
sys.path.insert(0, ".")
import fitness, genomes, vxa_scene

DRV = "/home/sandbox/deps/reconfigurable_organisms/_voxcad/voxelyzeMain/voxelyze"
OUT = "/tmp/stage4/audit"; os.makedirs(OUT, exist_ok=True)
LATTICE, INIT_T = 0.05, 1.0
YZ_LIMIT = 0.15

def collect():
    cands = []
    for sd in (10, 11, 12):
        p = f"/tmp/stage4/seed{sd}/result.json"
        if not os.path.exists(p):
            continue
        r = json.load(open(p))
        for x in r["final"]:
            if not x["failed"] and x["F"] > 0:
                cands.append(dict(arm=f"seed{sd}", tag=f"g15_i{x['i']}", F=x["F"], F_A=x["F_A"], F_B=x["F_B"]))
    for n in (6000, 7000):
        d = json.load(open(f"/tmp/stage4/null{n}/null.json"))
        for x in d["rows"]:
            if not x["failed"] and x["F"] > 0:
                cands.append(dict(arm=f"null{n}", tag=f"n{x['i']}", F=x["F"], F_A=x["F_A"], F_B=x["F_B"]))
    return cands

def anchor_scale():
    """Largest anchor one-way (condition A) flat-ground fitness, sec 7.2 scale."""
    rows = json.load(open("/home/sandbox/mega27-19-xenobot-causal-networks/results/design_pivot/stage1/anchors-result.json"))  # stage-1 anchors, fixed scale per amendment-03
    vals = [r["F_A"] for r in rows if not r["failed"] and r["F_A"] is not None]
    return max(vals), vals

def rerun(vxa_src, tag):
    p = os.path.join(OUT, tag + ".vxa")
    data = open(vxa_src).read()
    open(p, "w").write(data)
    traj, _ = fitness.run_eval(p, DRV, p + ".fitness", timeout=180)
    return traj

def yz_cumulative(traj):
    tot = 0.0
    for a, b in zip(traj, traj[1:]):
        dy = (b[2] or 0) - (a[2] or 0); dz = (b[3] or 0) - (a[3] or 0)
        tot += (dy * dy + dz * dz) ** 0.5
    return tot

def audit(c, scale):
    base = {"seed10": "/tmp/stage4/seed10", "seed11": "/tmp/stage4/seed11", "seed12": "/tmp/stage4/seed12",
            "null6000": "/tmp/stage4/null6000", "null7000": "/tmp/stage4/null7000"}[c["arm"]]
    res = dict(c)
    a_vxa = os.path.join(base, c["tag"] + "_A.vxa")
    b_vxa = os.path.join(base, c["tag"] + "_B.vxa")
    res["a_vxa_exists"] = os.path.exists(a_vxa); res["b_vxa_exists"] = os.path.exists(b_vxa)
    # sec 7.5 fixed regions
    txt = open(a_vxa).read()
    m = re.search(r"<NumFixed>(\d+)</NumFixed>", txt)
    res["fixed_voxel_count"] = int(m.group(1)) if m else None
    res["fixed_regions_present"] = (res["fixed_voxel_count"] or 0) > 0
    # sec 7.4 validity
    mat, ph = vxa_scene.parse_vxa_structure(a_vxa)
    res["valid"] = bool(genomes.is_valid(mat))
    # re-runs with trajectory (2x A, 2x B)
    fa_vals, fb_vals, yz_a, yz_b = [], [], None, None
    for k in (1, 2):
        t = rerun(a_vxa, f"{c['arm']}_{c['tag']}_A_r{k}")
        fa_vals.append(fitness.fitness_locomotion(t, LATTICE, INIT_T))
        if yz_a is None: yz_a = yz_cumulative(t)
        t = rerun(b_vxa, f"{c['arm']}_{c['tag']}_B_r{k}")
        fb_vals.append(fitness.fitness_locomotion(t, LATTICE, INIT_T))
        if yz_b is None: yz_b = yz_cumulative(t)
    res.update(rerun_F_A=fa_vals, rerun_F_B=fb_vals, yz_path_A=yz_a, yz_path_B=yz_b)
    res["traj_ok"] = (yz_a <= YZ_LIMIT) and (yz_b <= YZ_LIMIT)
    res["energy_ok"] = (abs(c["F_A"]) <= 3 * scale) and (abs(c["F_B"]) <= 3 * scale)
    det = all(v == c["F_A"] for v in fa_vals) and all(v == c["F_B"] for v in fb_vals)
    res["determinism_ok"] = bool(det)
    res["pass_all"] = all([res["traj_ok"], res["energy_ok"], res["determinism_ok"],
                           res["valid"], not res["fixed_regions_present"]])
    return res

def main():
    cands = collect()
    scale, anchor_fa = anchor_scale()
    print(f"candidates F>0: {len(cands)}; energy scale (max anchor F_A): {scale}")
    pl = "/tmp/stage4/audit/audit_partial.jsonl"
    done = {}
    if os.path.exists(pl):
        for line in open(pl):
            line = line.strip()
            if line:
                r = json.loads(line)
                done[(r["arm"], r["tag"])] = r
    out = dict(energy_scale=scale, anchor_F_A=anchor_fa, results=[])
    for c in cands:
        key = (c["arm"], c["tag"])
        if key in done:
            r = done[key]
            print(f"{r['arm']:7s} {r['tag']:12s} F={r['F']:.5f} [resume: already audited]", flush=True)
        else:
            r = audit(c, scale)
            with open(pl, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(f"{r['arm']:7s} {r['tag']:12s} F={r['F']:.5f} traj={r['traj_ok']} "
                  f"energy={r['energy_ok']} det={r['determinism_ok']} valid={r['valid']} "
                  f"fixed={r['fixed_regions_present']} PASS={r['pass_all']}", flush=True)
        out["results"].append(r)
    json.dump(out, open("/tmp/stage4/audit/audit_stage4.json", "w"), indent=1)
    print("AUDIT DONE")

if __name__ == "__main__":
    main()
