# DESIGN PIVOT - STAGE 6 RESULT: champion-seeded intensification, second round (simulation-only)

Completed 2026-10-10 ~21:40 IST. Protocol: docs/DESIGN_PIVOT_PREREG_AMENDMENT_08.md (SHA-256
6b108fa69bb43c99356312c20ff33cf7ec68ebd02b410cf932a3d2140fe0384d, locked before any stage-6 compute;
prespec commit 47f0c8c). Runner: ga6.py (SHA-256
f1a600da6d1dd6d611e49d11afd04aabc1b79d0e71f4560c7af02490c5ff1bba). Audit: audit_stage6.py (SHA-256
8f65eed910eda3f75d52eb1ed8b0b03268e0d28249cd3ff9aec6fa6850c31a31, committed before any audit runs -
this is the exact executed script; the audit supports resume and was run to completion in one
continuous sweep). Champions: data/stage6-champions.json (SHA-256
03ab6cc7df2461de43dae10698ccf53696099232cf01e273755262b6321c9314), extracted from the durable
stage-5 checkpoints (stage5_champ_seed20_g23_i0 F=0.15994, stage5_second_seed21_g23_i9 F=0.04236).
Corpus: data/stage3-corpus27.json (SHA-256
cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17). Raw data and custody:
results/design_pivot/stage6/ (SHA256SUMS.txt). ALL RESULTS ARE SIMULATION-ONLY AND UNVALIDATED IN
WET LAB. Free compute only (sandbox, 2 cores).

## Registered tests

| Test | Verdict | Basis |
|---|---|---|
| S6-H1 (production, stated expected-vacuous): each seed yields >= 1 final-pop F>0 design passing the full sec-7 audit | SUPPORTED, 3/3 | seed30 13/20, seed31 10/20, seed32 14/20 F>0 final-pop designs; every F>0 candidate in stage 6 passes all five audit checks |
| S6-H2 (primary): at least one seed's best F >= 0.19993 (1.25x the stage-5 champion 0.15994) | NOT SUPPORTED | seed30 best 0.17000, seed31 best 0.18068, seed32 best 0.17474 - all three miss; the best (seed31) falls 0.01925 short |
| S6-H3: each seed's best F strictly beats the null9000 best F (3 comparisons) | NOT SUPPORTED | null best 0.17336 (n362); seed31 0.18068 and seed32 0.17474 beat it, seed30 0.17000 does not. 2/3 comparisons pass; the registered each-seed form fails |

## What the primary result does and does not say
- The stage-5 outlier lineage did NOT intensify a further 1.25x. All three seeds improved on the
  stage-5 champion (0.15994) by small margins (+0.010 to +0.021) and clustered in a narrow band
  (0.17000-0.18068). The 1.25x bar was not approached: seed31's 0.18068 is 1.13x the stage-5
  champion. This is the first stage whose primary registered test is NOT SUPPORTED.
- The seeds are not independent replicates (shared stage-5 champions, per amendment-08), but the
  clustering is itself evidence: three seeds from the same two parents under mutation-only search
  landed within 0.011 of each other, all below the bar. The champion basin appears near-saturated
  for this operator and budget; stage 5's 4.75x jump was not repeatable in a second round.
- The null ceiling rose with the stronger parents: null9000 best 0.17336 vs the stage-5 null's
  0.03450. Random champion-mutation at equal budget now produces designs that beat ONE of the three
  GA seeds (seed30, 0.17000). In stage 5 selection clearly beat the null ceiling on every seed; in
  stage 6 it does so on only two of three. The selection advantage over champion-local random
  mutation narrowed materially.
- Magnitude honesty: best stage-6 F 0.18068 voxels bidirectional is ~30.8x weaker than the strongest
  anchor's one-way F_A (5.57002) - improved from ~34.8x (stage 5), but the gain over stage 5 is
  0.021 voxels, an order of magnitude smaller than stage 5's own jump.
- Audit: 372 candidates with F>0 across all four arms (seed30 13, seed31 10, seed32 14, null9000
  335); 372/372 pass all five checks (trajectory, energy, exact determinism on re-runs, validity,
  zero Fixed regions). 0 failures, 0 culls mid-audit. Energy scale: stage-1 anchor max F_A 5.57002.
  All three GA seed champions reproduce EXACTLY on audit re-run (0.17000 / 0.18068 / 0.17474), as
  does the null best (0.17336, n362).

## The null's hit rate and ceiling both rose
- null9000 F>0 rate: 335/480 (70%) - up from 49% in stage 5. Champion seeding from a stronger
  parent makes random mutation even more productive per draw, as expected.
- But unlike stage 5, the null ceiling is no longer low: best 0.17336, and 0/480 over the 0.19993
  bar. The null distribution's head (0.17336) now overlaps the GA seeds' band (0.17000-0.18068).
  Median F 0.03255 (vs 0.03450 best in stage 5) - the body of the null distribution stayed low
  while the tail reached GA territory. Culls: 0 in all runs.
- At equal budget, selection still improves the expected outcome (GA bests 0.170-0.181 vs null
  median 0.03255) but no longer guarantees beating the null's best draw.

## Constraint and cull honesty
- GA init culls: seed30 0, seed31 3, seed32 12 - ALL strata, matching the registered pilot yields
  (strata is the fragile family vs the 0.5 corpus floor, third stage running). Offspring culls: 0
  in all three seeds - the floor shaped init, never evolution (same as stages 3-5).
- null9000 culls: 0 (all 480 draws produced a valid + floor-passing mutant within 200 attempts).
- Init diversities (median pairwise min_d, including champions): seed30 0.4865, seed31 0.5215,
  seed32 0.4552 - above the 0.30 floor; families 4/4/5/5 in all three, as registered.

## Secondaries (report-only)
- Novelty vs the 4 published anchors (descriptive): all 372 audit-passing designs have min occupancy
  distance 0.6907-0.7058 (nearest anchor Example_3 for all 372). Best design seed31 g23_i0: min_d
  0.7024, 230 voxels. Novel by construction; the measurement confirms the constraint held.
- Post-hoc pooled permutation INCLUDING stage-6 bests (18 GA bests vs 9 null bests across stages
  4-6, exact 4,686,825 labelings): difference of means 0.02460, p = 0.13177. DESCRIPTIVE ONLY -
  S4-H2's registered verdict (p = 0.01016) stands as registered and is not re-fished.
- Morphology-convergence follow-up (amendment-08): occupancy min_d of each seed's final pop vs the
  stage-5 champion - seed30 min 0.0000 / median 0.0066 / max 0.0173; seed31 min 0.0043 / median
  0.0087 / max 0.0216; seed32 min 0.0000 / median 0.0087 / max 0.0173. Convergent again: the seeds
  climbed by actuation-program search on the champion's shape basin, not morphology exploration
  (extends NEGATIVE_REGISTER 20).
- Audit-passing F>0 candidates per arm: seed30 13, seed31 10, seed32 14 (final pops), null9000
  335/480.

## Per-run summary
| Run | Sims/draws | Failed | F>0 | Best F | Culls (init/offspring) |
|---|---|---|---|---|---|
| seed30 | 877 | 0 | 13/20 | 0.17000 (gen18 i10; elite-carried to g23_i0/i8/i13/i19) | 0 / 0 |
| seed31 | 889 | 0 | 10/20 | 0.18068 (gen15 i11; elite-carried to g23_i0) | 3 / 0 (all strata) |
| seed32 | 878 | 0 | 14/20 | 0.17474 (gen21 i1; elite-carried to g23_i0) | 12 / 0 (all strata) |
| null9000 | 480 draws | 0 | 335/480 | 0.17336 (n362) | 0 / 0 |

Best-F trajectories (per generation, improvement waypoints):
- seed30: 0.15994 (gen0, champion) -> 0.16392 (gen4) -> 0.16750 (gen5) -> 0.16868 (gen8) ->
  0.17000 (gen18). Slow grind, best at gen18 of 23.
- seed31: 0.15994 (gen0) -> 0.16946 (gen1) -> 0.17006 (gen5) -> 0.17622 (gen6) -> 0.18068 (gen15).
  Early jump, best at gen15.
- seed32: 0.15994 (gen0, held to gen6) -> 0.16032 (gen7) -> 0.16808 (gen9) -> 0.17448 (gen13) ->
  0.17474 (gen21). Flat early, best at gen21.

## Standing limits (carried, unchanged)
Simulation-only; no wet-lab validation. Champions shared across seeds (not independent replicates).
Null mutation depth (one mutate() call per draw) is one frozen choice among plausible ones. Stage-6
designs remain ~31x below anchor energy scale. Termination per amendment-08: stage 6 ends here; any
further seeds, pools, objective changes, margins, or mutation changes require a new amendment
locked before compute.
