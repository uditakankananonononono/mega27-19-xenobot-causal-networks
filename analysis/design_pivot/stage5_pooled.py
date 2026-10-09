"""Stage-5 report-only secondary (amendment-07 sec. 4): post-hoc pooled permutation including
stage-5 bests, marked DESCRIPTIVE. S4-H2's registered verdict (p = 0.01016) stands as
registered and is NOT re-fished; this adds stage-5 per-seed bests (GA) and the null8000
best (null) to the same label-permutation machinery for continuity only.
One-sided exact label-permutation, difference of means, 15 GA per-seed best F
(stages 1-5) vs 8 null per-pool best F. Exact C(23,8)=490314 labelings."""
import json, itertools
import numpy as np

GA_123 = [0.00616, 0.00920, 0.00382, 0.00586, 0.00738, 0.00694, 0.01872, 0.01228, 0.03364]
NU_123 = [0.01298, 0.00106, 0.00362, 0.00760, 0.00292]

def main():
    ga4, nu4 = [], []
    for sd in (10, 11, 12):
        r = json.load(open(f"/tmp/stage4/seed{sd}/result.json"))
        ga4.append(max(x["F"] for x in r["final"]))
    for n in (6000, 7000):
        r = json.load(open(f"/tmp/stage4/null{n}/null.json"))
        rows = r["rows"] if isinstance(r, dict) else r
        nu4.append(max(x["F"] for x in rows))
    ga5, nu5 = [], []
    for sd in (20, 21, 22):
        r = json.load(open(f"/tmp/stage5/seed{sd}/result.json"))
        ga5.append(max(x["best_F"] for x in r["history"]))
    r = json.load(open("/tmp/stage5/null8000/null.json"))
    nu5.append(max(x["F"] for x in r["rows"]))
    ga = GA_123 + ga4 + ga5
    nu = NU_123 + nu4 + nu5
    pooled = np.array(ga + nu)
    n_g = len(ga); total = pooled.sum()
    obs = pooled[:n_g].sum() / n_g - pooled[n_g:].sum() / len(nu)
    comb = np.array(list(itertools.combinations(range(len(pooled)), n_g)))
    sums = pooled[comb].sum(axis=1)
    stat = sums / n_g - (total - sums) / len(nu)
    p = float((stat >= obs - 1e-12).mean())
    print(json.dumps(dict(ga_bests=ga, null_bests=nu, observed_diff=obs,
                          n_labelings=len(comb), p=p,
                          note="DESCRIPTIVE ONLY - S4-H2 registered verdict p=0.01016 stands"), indent=1))

if __name__ == "__main__":
    main()
