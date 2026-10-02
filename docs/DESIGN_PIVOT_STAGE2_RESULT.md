# DESIGN PIVOT - STAGE 2 RESULT: replication of the stage-1 H2 test (simulation-only)

Completed 2026-10-02 ~08:19 IST. Protocol: docs/DESIGN_PIVOT_PREREG_AMENDMENT_03.md (SHA-256
fccd6d0602071f15bb36105c9b563a5a1e65949af97b50db099553f02d13c55c, locked before any stage-2 compute),
on top of the prereg, amendment-01 and amendment-02. Code unchanged from stage 1 except a null-seed argument.
Raw data and custody: results/design_pivot/stage2/ (SHA256SUMS.txt). ALL RESULTS ARE SIMULATION-ONLY AND
UNVALIDATED IN WET LAB. Scope was picked by the lane (not specified by the user); the user can redirect.

## Registered tests

| Test | Verdict | Basis |
|---|---|---|
| S2-H1: each new GA seed has >= 1 final-pop design with F > 0 passing sec 7 | SUPPORTED, 3/3 | seed4: 2, seed5: 5, seed6: 5 designs; all 16 F>0 designs in stage 2 (12 GA + 4 null) pass all five checks with exact determinism |
| S2-H2 (primary): each new GA best beats the best of EACH new null pool (6 comparisons) | SUPPORTED, 6/6 | GA bests 0.00586 / 0.00738 / 0.00694 vs null bests 0.00106 (null2000, n9) and 0.00362 (null3000, n193) |
| S2-H3: audit-passing new candidates novel (min distance >= 0.5 vs 4 anchors + 7 stage-1 candidates) | NOT SUPPORTED | all 16 audit-passing designs have min distance 0.2695-0.3254 (nearest: stage-1 GA designs); see below |

## What the primary result does and does not say
- Both fresh null pools were much weaker than stage 1's shared null: 1/480 and 3/480 designs with F > 0
  (stage 1: 4/480), with best F of 0.00106 and 0.00362. The stage-1 null best (n394, 0.01298) was a heavy-tail draw.
- GA final populations hold F > 0 designs at 10-25% (2, 5, 5 of 20) vs 0.2-0.8% for random sampling.
  By this registered measure the GA concentrates bidirectional designs better than random search.
- Pooled descriptive check (registered as secondary): 6 GA bests (stage 1 + 2) vs 3 null bests (0.01298,
  0.00106, 0.00362). The stage-1 null best is still higher than all 6 GA bests. One-sided exact label
  permutation on the difference of means: 37/84 = 0.44. Pooled, the evidence does not separate the GA from
  random search on best-F. The two registered verdicts (stage-1 H2 not supported, stage-2 H2 supported)
  both stand. Neither overturns the other. The honest summary is: GA is clearly better at hit rate, and not
  shown to be better on the single best design.
- Magnitudes stay marginal: best bidirectional F in stage 2 is 0.00738 voxels (about 0.37 mm net over 10 s).

## S2-H3 detail
- Registered corpus included the 7 stage-1 audited candidates. Every stage-2 candidate sits at distance
  0.27-0.33 from a stage-1 GA design (seed2 g15_i0 or seed1 g15_i1). Search from fresh seeds converges on
  the same family of morphologies, so these are not new relative to stage 1.
- Descriptive only, not the registered test: against the 4 published anchors alone, all 16 designs have
  min distance 0.5331-0.5842 (>= 0.5). Novelty versus the published corpus holds, as in stage 1.
- 12 of the 16 are GA candidates; the 4 null designs are included in the table for completeness. Excluding
  them does not change the verdict.

## Per-run summary
| Run | Sims | Failed | F>0 (final pop or pool) | Best F |
|---|---|---|---|---|
| seed4 GA | 486 | 0 | 2/20 | 0.00586 (g15_i0) |
| seed5 GA | 493 | 0 | 5/20 | 0.00738 (g15_i0) |
| seed6 GA | 492 | 0 | 5/20 | 0.00694 (g15_i0) |
| null2000 | 480 designs | 0 | 1/480 | 0.00106 (n9) |
| null3000 | 480 designs | 0 | 3/480 | 0.00362 (n193) |

All five runs completed without truncation. Audit used the stage-1 energy scale (max anchor F_A 5.57).

## Custody
Scene archive in results/design_pivot/stage2/custody/ (tar and disk scene counts were verified equal at archive time, commit 929cc21; per-run counts are in that commit's log, not restated here). Hashes in SHA256SUMS.txt.
audit_stage2.json SHA-256 prefix 75015152, novelty_stage2.json prefix be79368c.

## Limits
Same sim-only scope as stage 1: no wet-lab validation, a 10 s window, flat-ground and one reversal
condition. Three seeds and three null pools are still a small sample. Novelty is measured on occupancy
only, against a corpus of 4 published designs plus our own.
