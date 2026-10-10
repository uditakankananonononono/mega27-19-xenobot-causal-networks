"""Stage-6 report-only secondary (amendment-08 sec. 4): post-hoc pooled permutation including
stage-6 bests, marked DESCRIPTIVE. S4-H2's registered verdict (p = 0.01016) stands as
registered and is NOT re-fished; this adds stage-6 per-seed bests (GA) and the null9000
best (null) to the same label-permutation machinery for continuity only.
One-sided exact label-permutation, difference of means, 18 GA per-seed best F
(stages 1-6) vs 9 null per-pool best F. Exact C(27,9)=4686825 labelings (computed over
the 9-position null side, identical count to the 18-position GA side)."""
import itertools, json
import numpy as np

GA_123 = [0.00616, 0.00920, 0.00382, 0.00586, 0.00738, 0.00694, 0.01872, 0.01228, 0.03364]
NU_123 = [0.01298, 0.00106, 0.00362, 0.00760, 0.00292]

def main():
    ga4, nu4 = [], []
    for sd in (10, 11, 12):
        r = json.load(open(f"../../results/design_pivot/stage4/seed{sd}-result.json"))
        ga4.append(max(x["F"] for x in r["final"]))
    for n in (6000, 7000):
        r = json.load(open(f"../../results/design_pivot/stage4/null{n}-null.json"))
        rows = r["rows"] if isinstance(r, dict) else r
        nu4.append(max(x["F"] for x in rows))
    ga5, nu5 = [], []
    for sd in (20, 21, 22):
        r = json.load(open(f"../../results/design_pivot/stage5/seed{sd}-result.json"))
        ga5.append(max(x["best_F"] for x in r["history"]))
    r = json.load(open("../../results/design_pivot/stage5/null8000-null.json"))
    nu5.append(max(x["F"] for x in r["rows"]))
    ga6, nu6 = [], []
    for sd in (30, 31, 32):
        r = json.load(open(f"/tmp/stage6/seed{sd}/result.json"))
        ga6.append(max(x["best_F"] for x in r["history"]))
    r = json.load(open("/tmp/stage6/null9000/null.json"))
    nu6.append(max(x["F"] for x in r["rows"]))
    ga = GA_123 + ga4 + ga5 + ga6
    nu = NU_123 + nu4 + nu5 + nu6
    pooled = np.array(ga + nu)
    n_g, n_n = len(ga), len(nu)
    total = pooled.sum()
    obs = pooled[:n_g].sum() / n_g - pooled[n_g:].sum() / n_n
    n_lab = 0
    n_ge = 0
    CH = 500000
    it = itertools.combinations(range(len(pooled)), n_n)
    while True:
        chunk = list(itertools.islice(it, CH))
        if not chunk:
            break
        comb = np.array(chunk)
        nsums = pooled[comb].sum(axis=1)
        stat = (total - nsums) / n_g - nsums / n_n
        n_ge += int((stat >= obs - 1e-12).sum())
        n_lab += len(chunk)
    p = n_ge / n_lab
    print(json.dumps(dict(ga_bests=ga, null_bests=nu, observed_diff=obs,
                          n_labelings=n_lab, p=p,
                          note="DESCRIPTIVE ONLY - S4-H2 registered verdict p=0.01016 stands"), indent=1))

if __name__ == "__main__":
    main()
