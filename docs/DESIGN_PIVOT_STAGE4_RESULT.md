# DESIGN PIVOT - STAGE 4 RESULT: initial-morphology ensemble + permutation power (simulation-only)

Completed 2026-10-08 ~14:30 IST. Protocol: docs/DESIGN_PIVOT_PREREG_AMENDMENT_06.md (SHA-256
3fc4366a2b74625831cb9951d9dab3ab07af8aec62064c1d4e5f6d2a654fa722, locked before any stage-4 compute),
on top of the prereg and amendments 01-05. Corpus: data/stage3-corpus27.json (SHA-256
cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17). Runner: ga4.py (SHA-256
714e7e90b9d581a62c1d43201a3b000038abce65b959b1c428ecb20606dde054). Audit: audit_stage4.py
(adapted from audit_stage3.py, identical section-7 checks, committed at 1e354b3 before any audit ran).
Raw data and custody: results/design_pivot/stage4/ (SHA256SUMS.txt; custody tarball coverage verified
against the full design index at archive time: 6268 scene files, tar/disk equality, 1613 row-scene
references checked, 0 missing). ALL RESULTS ARE SIMULATION-ONLY AND UNVALIDATED IN WET LAB.
Free compute only (sandbox, 2 cores).

## Registered tests

| Test | Verdict | Basis |
|---|---|---|
| S4-H1: each GA init population has median pairwise min_d >= 0.30 with exactly 5 members per family | SUPPORTED, 3/3 | seed10 0.4814, seed11 0.4916, seed12 0.4966; 5/5/5/5 shell/ellipsoid/strata/core_appendage in all three |
| S4-H2 (primary): one-sided exact label permutation, 12 GA bests vs 7 null bests, C(19,7)=50388 labelings | SUPPORTED | difference of means 0.00833, p = 0.01016 < 0.05 |
| S4-H3: each stage-4 GA best beats EACH stage-4 null pool best (6 comparisons) | SUPPORTED, 6/6 | GA bests 0.01980 / 0.01922 / 0.02156 vs null bests 0.00350 (null6000, n0) and 0.00600 (null7000, n385) |
| S4-H4: each stage-4 seed yields >= 1 final-pop F>0 design passing the full sec-7 audit | SUPPORTED, 3/3 | seed10: 7, seed11: 10, seed12: 8 F>0 final-pop designs; all 32 F>0 designs in stage 4 (25 GA + 7 null) pass all five checks (trajectory, energy, exact determinism on re-runs, validity, zero Fixed regions) |

## What the primary result does and does not say
- S4-H2 is the first pooled best-F separation at the registered threshold: stage 2 gave 37/84 = 0.44,
  stage 3 gave 177/2002 = 0.088, stage 4 gives p = 0.01016 over all 12 GA seeds and all 7 null pools.
  The test is exact (full enumeration of labelings), one-sided on the difference of means, as registered.
- Context that still applies: the stage-1 null best (0.01298) remains the largest single null value and
  exceeds the stage-1 and stage-2 GA bests; every stage-3 and stage-4 GA best exceeds it. The pooled
  result leans on the newer seeds. p = 0.01016 clears 0.05 but is not an order-of-magnitude margin.
- Hit rate stays the GA's largest advantage: final populations hold F>0 designs at 35-50% (7, 10, 8 of
  20) vs 0.4-1.0% for the null pools (2/480 and 5/480). Registered-secondary observation, not a primary
  test.
- Magnitudes stay marginal: best stage-4 bidirectional F is 0.02156 voxels (about 1.08 mm net over 10 s),
  ~258x weaker than the strongest anchor's one-way locomotion (5.57). Stage-4 best F did NOT beat the
  stage-3 best (0.03364) - reported per the registered secondary; more seeds bought power, not a new
  best design.

## Init ensemble and diversity (attacks stage-3 limitation 10)
- The stratified four-family ensemble replaced stage-3's single narrow shell family (mutual min_d
  0.02-0.05): GA init medians 0.4814-0.4966, null-pool subsample medians 0.5116 (null6000) and 0.5017
  (null7000), all far above the 0.30 floor.
- Residual limitation, registered in amendment-06 and unchanged: within-family clustering (pilot
  within-family median 0.222 << cross-family 0.600). The ensemble diversifies ACROSS families; inside
  each family, draws stay clustered. Evolved finals also cluster per seed (novelty table in
  results/design_pivot/stage4/novelty_stage4.json).
- Null-pool init diversity is report-only per registration; both pools pass the 0.30 floor descriptively.

## Constraint and cull honesty
- Init culls (registered per family per run): seed10 7 (all strata), seed11 5 (all strata), seed12 15
  (all strata), null6000 236 (all strata), null7000 247 (245 strata, 2 core_appendage). The strata
  family fails the 0.5 corpus floor on ~half its draws (pilot-measured 8/15 yield), as pre-registered;
  shell, ellipsoid and core_appendage almost never culled. The floor bound init generation, exactly as
  designed.
- Offspring culls: 0 in all 5 runs - the corpus floor never rejected a mutated child mid-run (same as
  stage 3). The constraint shaped the init region; it did not filter evolution.

## Secondaries (report-only)
- Per-pool F>0 rates: null6000 2/480, null7000 5/480. GA: 7/20, 10/20, 8/20.
- Stage-4 best F 0.02156 vs stage-3 best 0.03364: no progress (see above).
- Novelty vs the 4 published anchors (descriptive): all 32 audit-passing designs have min occupancy
  distance 0.6473-0.7094 (nearest anchor Example_3 or Example_withPhaseOffset for 31 of 32; Example_1
  for null7000 n242). Novel by construction; the measurement confirms the constraint held.
- Effect size vs anchors: best 0.02156 vs anchor max F_A 5.57002 (~258x weaker).

## Per-run summary
| Run | Sims | Failed | F>0 (final pop or pool) | Best F | Culls (init/offspring) |
|---|---|---|---|---|---|
| seed10 | 548 | 0 | 7/20 | 0.01980 (g15_i0) | 7 / 0 |
| seed11 | 511 | 0 | 10/20 | 0.01922 (g15_i12) | 5 / 0 |
| seed12 | 526 | 0 | 8/20 | 0.02156 (g15_i0) | 15 / 0 |
| null6000 | 480 draws | 0 | 2/480 | 0.00350 (n0) | 236 / 0 |
| null7000 | 480 draws | 0 | 5/480 | 0.00600 (n385) | 247 / 0 |

Best-F trajectories (per generation):
- seed10: -0.0688 -> +0.0131 (gen6) -> +0.0162 (gen10) -> +0.0198 (gen13, held to gen15)
- seed11: -0.0267 -> +0.0017 (gen4) -> +0.0122 (gen10) -> +0.0169 (gen11) -> +0.0192 (gen15)
- seed12: -0.0151 -> +0.0183 (gen1) -> +0.0201 (gen4) -> +0.0216 (gen10, held to gen15)

Wall-clock (IST 2026-10-08, first/last scene written; includes sandbox suspensions, two cores):
seed10 04:44-07:46, null6000 04:45-08:47, seed11 07:47-10:32, seed12 08:49-11:43,
null7000 10:33-14:15, audit sweep 1 12:02-12:26 (29 candidates), sweep 2 14:19-14:24 (3 more).

## Custody
Scene archive results/design_pivot/stage4/custody/stage4-scenes.tar.gz (6268 scene files; tar/disk
equality and 1613 design-index row-scene references verified at archive time, 0 missing; builder
analysis/design_pivot/custody_stage4.py). Hashes in results/design_pivot/stage4/SHA256SUMS.txt.
Pooled-permutation script analysis/design_pivot/stage4_pooled.py; novelty script
analysis/design_pivot/novelty_stage4.py.

## Limits
Same sim-only scope as stages 1-3: no wet-lab validation, a 10 s window, flat ground, one reversal
condition. Three new seeds and two new pools are still a small sample; S4-H2's p = 0.01016 clears the
registered threshold with limited margin and leans on stage-3/4 seeds. Within-family init clustering
(0.222 within vs 0.600 cross, pilot) is unchanged and registered. Novelty is occupancy-only against 4
published anchors plus our own corpus. No stage-4 design beats the stage-3 best. Stage 4 is closed per
amendment-06 termination: exactly 5 runs + audits; any further seeds, pools, families, floors, or metric
changes require a new amendment locked before compute.
