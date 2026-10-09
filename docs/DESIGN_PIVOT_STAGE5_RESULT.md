# DESIGN PIVOT - STAGE 5 RESULT: champion-seeded effect-size intensification (simulation-only)

Completed 2026-10-09 ~08:15 IST. Protocol: docs/DESIGN_PIVOT_PREREG_AMENDMENT_07.md (SHA-256
981aecd5d720c3fb0b3e9d5e187fb638c81233daa4f96188bbea74dcc6c4342b, locked before any stage-5 compute;
decision authority: parent directive 2026-10-08 16:06 IST relaying the user's "do whatever" delegation;
lane selected Option A, effect size). Runner: ga5.py (SHA-256
7791296ce5320bb704e3c4a5f6f3e6770d21291f78e402d23d914d334d43354e). Audit: audit_stage5.py (SHA-256
1112b81691b0ec6c2e395d8845aa31f871949fd58596876653a1d88745659384, committed before any audit runs -
this is the exact executed script; the audit supports resume and was run to completion in one
continuous sweep plus resume markers). Champions: data/stage5-champions.json (SHA-256
10f7b5317ff8d51826c937bbf33138c22b1bb81c27230272af5c4f929feccb2e), extracted from the durable
stage-3/4 checkpoints. Corpus: data/stage3-corpus27.json (SHA-256
cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17). Raw data and custody:
results/design_pivot/stage5/ (SHA256SUMS.txt; custody tarball coverage verified against the full
design index at archive time). ALL RESULTS ARE SIMULATION-ONLY AND UNVALIDATED IN WET LAB.
Free compute only (sandbox, 2 cores).

## Registered tests

| Test | Verdict | Basis |
|---|---|---|
| S5-H1 (production, stated expected-vacuous): each seed yields >= 1 final-pop F>0 design passing the full sec-7 audit | SUPPORTED, 3/3 | seed20 15/20, seed21 9/20, seed22 8/20 F>0 final-pop designs; every F>0 candidate in stage 5 passes all five audit checks |
| S5-H2 (primary): at least one seed's best F >= 0.04205 (1.25x the stage-3 champion 0.03364) | SUPPORTED | seed20 best 0.15994 (3.80x the bar); seed21 best 0.04236 (clears by 0.0003); seed22 best 0.04152 (misses by 0.0005) |
| S5-H3: each seed's best F strictly beats the null8000 best F (3 comparisons) | SUPPORTED, 3/3 | 0.15994 / 0.04236 / 0.04152 vs null best 0.03450 (n420, parent stage-3 champion) |

## What the primary result does and does not say
- The frozen champions are NOT local optima of this design class under mutation-only search: two of
  three seeds improved materially on them, and all three beat 480 random champion-mutants at equal
  evaluation budget. Selection adds value over random champion-mutation (S5-H3).
- seed20's 0.15994 is the stage's outlier: 4.75x the stage-3 champion, reached by steady climbing from
  gen 1 (0.07246) through gen 22, with the final population dominated by its lineage (g23_i0 0.15994
  elite-carried; g23_i6 and g23_i14 0.15972; g23_i7 0.13836). One seed, one lineage - the seeds are
  NOT independent replicates (all share the same two champions, per amendment-07 sec. 5), so S5-H2
  counts seeds, not independent discoveries.
- seed21 clears the frozen bar by 0.0003 and seed22 misses it by 0.0005. Both are flat-then-late:
  seed21 held ~0.035 through gen 17 before gains at gens 18-23; seed22 held the champion value
  0.03364 for 21 straight generations before jumping at gens 21-23. Without the GENS=24 extension
  (registered on the stage-3/4 plateau evidence), all three seeds' bests would have been missed:
  every seed's best arrived at gen 20 or later.
- Magnitude honesty: 0.15994 voxels bidirectional F is ~34.8x weaker than the strongest anchor's
  one-way F_A (5.57002) - improved from ~165x (stage 3) but still far below anchor scale. The
  effect-size gap narrowed ~4.7x; it did not close.
- Audit: 267 candidates with F>0 across all four arms; 267/267 pass all five checks (trajectory,
  energy, exact determinism on re-runs, validity, zero Fixed regions). 0 failures, 0 culls mid-audit.
  Energy scale: stage-1 anchor max F_A 5.57002.

## The null's hit rate inverts the stage-4 pattern
- null8000 F>0 rate: 235/480 (49%) - vs 0.4-1.0% for the stage-4 unseeded pools. Champion seeding
  makes random mutation productive per draw, exactly as expected.
- But the null's CEILING stayed low: best 0.03450, 0/480 over the 0.04205 bar, 7/480 beating the
  stage-3 champion, median F -0.00135. At equal budget, the GA arms all beat that ceiling. In stage 4
  the GA's advantage was hit rate; in stage 5 it is the ceiling. Both arms ran identical fitness,
  operator, floor and audit rules.
- Null diversity is champion-local by design (median pairwise min_d 0.6242): report-only, NOT
  comparable to the stage-4 ensemble pools (amendment-07 sec. 2).

## Constraint and cull honesty
- GA init culls: seed20 4, seed21 14, seed22 3 - ALL strata, matching the registered pilot yields
  (strata is the fragile family vs the 0.5 corpus floor). Offspring culls: 0 in all three seeds -
  the floor shaped init, never evolution (same as stages 3-4).
- null8000 culls: 0 (all 480 draws produced a valid + floor-passing mutant within 200 attempts).
  Parent split exactly 240/240 across the two champions, as registered.
- Init diversities (median pairwise min_d, including champions): seed20 0.4762, seed21 0.5067,
  seed22 0.4552 - above the 0.30 floor; families 4/4/5/5 in all three, as registered.

## Secondaries (report-only)
- Best stage-5 F vs the frozen champions: all three seeds beat the stage-3 champion (0.03364) and the
  stage-4 champion (0.02156). Stage 5 is the first stage since stage 3 to set a new overall best.
- Post-hoc pooled permutation INCLUDING stage-5 bests (15 GA bests vs 8 null bests, exact
  C(23,8) = 490314 labelings): difference of means 0.01820, p = 0.04036. DESCRIPTIVE ONLY -
  S4-H2's registered verdict (p = 0.01016) stands as registered and is not re-fished.
- Novelty vs the 4 published anchors (descriptive): all 267 audit-passing designs have min occupancy
  distance 0.6972-0.7083 (nearest anchor Example_3 for all 267). Best design seed20 g23_i0: min_d
  0.7039, 229 voxels. Novel by construction; the measurement confirms the constraint held.
- Audit-passing F>0 candidates per arm: seed20 15, seed21 9, seed22 8 (final pops), null8000 235/480.

## Per-run summary
| Run | Sims/draws | Failed | F>0 | Best F | Culls (init/offspring) |
|---|---|---|---|---|---|
| seed20 | 872 | 0 | 15/20 | 0.15994 (gen22 i19; elite-carried to g23_i0) | 4 / 0 |
| seed21 | 847 | 0 | 9/20 | 0.04236 (gen23 i9) | 14 / 0 |
| seed22 | 817 | 0 | 8/20 | 0.04152 (gen23 i1) | 3 / 0 |
| null8000 | 480 draws | 0 | 235/480 | 0.03450 (n420) | 0 / 0 |

Best-F trajectories (per generation, improvement waypoints):
- seed20: 0.03364 (gen0, champion) -> 0.07246 (gen1) -> 0.09682 (gen5) -> 0.11390 (gen7) ->
  0.12624 (gen14) -> 0.13912 (gen18) -> 0.15972 (gen20) -> 0.15994 (gen22). Steady climber.
- seed21: 0.03364 (gen0) -> 0.03512 (gen3, held to gen17) -> 0.03538 (gen18) -> 0.04044 (gen20) ->
  0.04236 (gen23). Flat-then-late.
- seed22: 0.03364 (gen0, held through gen20) -> 0.03432 (gen21) -> 0.03598 (gen22) -> 0.04152 (gen23).
  Flat for 21 generations, then a late surge.

## Standing limits (carried, unchanged)
Simulation-only; no wet-lab validation. Champions shared across seeds (not independent replicates).
Null mutation depth (one mutate() call per draw) is one frozen choice among plausible ones. Stage-5
designs remain ~35x below anchor energy scale. Termination per amendment-07 sec. 7: stage 5 ends
here; any further seeds, pools, objective changes, margins, or mutation changes require a new
amendment locked before compute.
