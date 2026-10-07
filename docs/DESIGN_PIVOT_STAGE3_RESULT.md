# DESIGN PIVOT - STAGE 3 RESULT: novelty-constrained search (simulation-only)

Completed 2026-10-08 ~04:30 IST. Protocol: docs/DESIGN_PIVOT_PREREG_AMENDMENT_04.md (SHA-256
a159f29a3ca26cd4fb21fb965f7fa0cad15e9112b38b50970647243218820d65) as repaired by
docs/DESIGN_PIVOT_PREREG_AMENDMENT_05.md (SHA-256 8bf887941f9b3cfa2d7c7c8b7fa21d368c4e80b73c73bb56e31648b507a57bb7),
both locked before any stage-3 compute. Corpus: data/stage3-corpus27.json (SHA-256
cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17). GA code: ga.py (SHA-256
06c0e3395525bacd8c6c3598551856d00b69dba440b0dd565c402e1f04776a7a). Raw data and custody:
results/design_pivot/stage3/ (SHA256SUMS.txt; custody tarball coverage verified against the full design
index: 3048 row-scene references checked, 0 missing). ALL RESULTS ARE SIMULATION-ONLY AND UNVALIDATED
IN WET LAB. Free compute only (sandbox, 2 cores).

## Registered tests

| Test | Verdict | Basis |
|---|---|---|
| S3-H1: each new GA seed has >= 1 final-pop design with F > 0 passing the full sec-7 audit | SUPPORTED, 3/3 | seed7: 3, seed8: 4, seed9: 10 F>0 final-pop designs; all 22 F>0 designs in stage 3 (17 GA + 5 null) pass all five checks (trajectory, energy, exact determinism on 2xA+2xB re-runs, validity, zero Fixed regions) |
| S3-H2 (primary): each new GA best beats the best of EACH new filtered null pool (6 comparisons) | SUPPORTED, 6/6 | GA bests 0.01872 / 0.01228 / 0.03364 vs null4000 best 0.00760 (n203) and null5000 best 0.00292 (n274) |
| S3-H3 (report-only): best stage-3 F vs stage-2 best 0.00738 | PROGRESS | best stage-3 F is 0.03364 (seed9 g15_i0) - the "novelty bought at zero fitness progress" clause does not apply |

## What the primary result does and does not say
- The novelty constraint (min occupancy distance >= 0.5 vs the 27-design corpus, constructive init per
  amendment-05) did not prevent the GA from finding bidirectional designs: all 3 seeds beat both
  budget-matched filtered null pools on best F, and every F>0 design passed the full audit.
- Hit rate: GA final populations hold F>0 designs at 15-50% (3, 4, 10 of 20) vs 0.4-0.6% for the filtered
  null pools (3/480 and 2/480). The GA concentrates bidirectional designs far better than random sampling
  in the constrained region as well.
- Pooled descriptive check (registered secondary): 9 GA bests (stages 1-3) vs 5 null bests (0.01298,
  0.00106, 0.00362, 0.00760, 0.00292). One-sided exact label permutation on the difference of means:
  177/2002 = 0.088. Improved from stage 2 (37/84 = 0.44) but still above 0.05: pooled across all stages,
  the GA's edge on best-F alone is still not separated at the conventional level. The stage-1 null best
  (0.01298) still exceeds the stage-1 and stage-2 GA bests; the stage-3 GA bests all exceed it.
- Novelty vs the 4 published anchors (registered secondary, descriptive): all 22 audit-passing designs
  have min occupancy distance 0.6991-0.7189 (nearest anchor always Example_3). Novel by construction;
  the measurement confirms the constraint held.
- Magnitudes stay marginal in absolute terms: best stage-3 bidirectional F is 0.03364 voxels (about
  1.68 mm net over 10 s), ~165x weaker than the strongest anchor's one-way locomotion (5.57).
  Bidirectional locomotion in the novel region exists in simulation at this budget but is a marginal
  behavior, not a robust gait.

## Constraint and cull honesty
- Cull counts were 0 (init) and 0 (offspring) in all 5 runs: the novelty floor never bound during search.
  This was pre-measured, not assumed: amendment-05's smoke tests showed 6/6 constructed inits at min_d
  0.568-0.585 and 10/10 mutated children staying >= 0.5. The constraint shaped the search region; it did
  not reject anything mid-run.
- Init morphology diversity inside the novel region is narrow (amendment-05, stated there plainly): a thin
  peripheral-shell family with mutual min_d 0.02-0.05. Material and phase diversity is unconstrained; the
  morphology claim is limited to that family.

## Per-run summary
| Run | Sims/evals | Failed | F>0 | Best F | Culls (init/offspring) |
|---|---|---|---|---|---|
| seed7 | 481 | 0 | 3/20 final pop | 0.01872 (g15_i0, g15_i9) | 0 / 0 |
| seed8 | 475 | 0 | 4/20 final pop | 0.01228 (g15_i3) | 0 / 0 |
| seed9 | 531 | 0 | 10/20 final pop | 0.03364 (g15_i0) | 0 / 0 |
| null4000 | 480 draws, 713 evals | 0 | 3/480 | 0.00760 (n203) | 0 / 0 |
| null5000 | 480 draws, 715 evals | 0 | 2/480 | 0.00292 (n274) | 0 / 0 |

Best-F trajectories (per generation):
- seed7: -0.0274 -> +0.0111 (gen2) -> +0.0187 (gen9, held to gen15)
- seed8: -0.0288 -> +0.0049 (gen3) -> +0.0078 (gen5) -> +0.0097 (gen9) -> +0.0123 (gen15)
- seed9: -0.0030 -> +0.0099 (gen2) -> +0.0164 (gen4) -> +0.0198 (gen10) -> +0.0336 (gen13, held to gen15)

Wall-clock: seed7 21:01-23:36, seed8 23:38-01:44, seed9 01:46-04:12, null4000 21:01-00:31,
null5000 00:33-03:45, audit 03:48-04:29 (all IST 2026-10-07/08, two cores with sandbox suspensions).
