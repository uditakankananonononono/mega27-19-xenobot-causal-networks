# PREREG AMENDMENT 04: STAGE 3 - novelty-constrained search (locked before any stage-3 compute)

Locked 2026-10-07 IST. Basis: user instruction "You do what you want." relayed by the parent at 20:39 IST
(delegating the stage-3 option pick), selecting Option A of docs/DESIGN_PIVOT_STAGE3_PROPOSAL.md. Extends
docs/DESIGN_PIVOT_PREREG.md (19441cc5a97c5e4eb1a6fd4c684ffa0a043bd07a3e5abe35a0fb39e8b32ce061),
AMENDMENT_01 (d51e8f484955617f185e88da73c9d3fd777073c26b9bcf82f4557cbb6c17c07d), AMENDMENT_02
(138a360c45a3a73a7e5f75aa6671ffa2653b66d695410222735c49359d2adc3b), AMENDMENT_03
(fccd6d0602071f15bb36105c9b563a5a1e65949af97b50db099553f02d13c55c). Everything not changed here stands.
SIMULATION-ONLY.

## Rationale
Stage 2 showed fresh GA seeds re-converge on the stage-1 morphology family (S2-H3 not supported, min
distance 0.27-0.33). Convergence from independent seeds is evidence about the search-space/fitness
landscape, not seed luck, so re-running the same search would re-register the same negative. Stage 3
changes the selection pressure: the search is confined to the region of design space at occupancy
distance >= 0.5 from everything found so far. No new objective, no new fitness.

## Locked corpus
data/stage3-corpus27.json, SHA-256 cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17.
27 designs: 4 published anchors + 7 audit-passing stage-1 candidates + 16 audit-passing stage-2
candidates (12 GA + 4 null), each with custody-verified condition-A .vxa SHA-256 and occupancy set
(voxel counts cross-checked against novelty_stage1.json / novelty_stage2.json). Distance metric and 48
-isometry minimization exactly as analysis/design_pivot/novelty_stage2.py.

## Design (locked)
- GA: seeds 7, 8, 9; pop 20 x 16 generations; identical code, fitness, audit (sec 7) and novelty
  procedure as stage 2, plus the constraint below.
- Constraint: any genome (initialization or child) with min occupancy distance < 0.5 vs the 27-design
  corpus is rejected and regenerated BEFORE evaluation, under the same regenerate rule as prereg sec 3.
  Rejection/cull counts per seed are reported. Consequence: every evaluated design is novel by
  construction, so novelty vs the corpus is not a stage-3 test; it is a design property.
- Null: two independent pools of 480 valid random genomes, Random(4000) and Random(5000), drawn from the
  SAME filtered initialization distribution (min_d >= 0.5 enforced identically); identical fitness.
- Stage-1/stage-2 data are NOT re-used for selection. Pooled analyses are labelled pooled.
- Code change: analysis/design_pivot/ga.py takes a corpus manifest path and novelty-floor argument and
  writes seeds>=7 / null in {4000,5000} to /tmp/stage3; default behavior for stage-1/2 seeds unchanged.
  Distance checks reuse the novelty_stage2.py functions, not a reimplementation.

## Registered tests
- S3-H1: each new GA seed yields >= 1 final-population design with F > 0 passing the full sec-7 audit.
  Supported only if all 3 seeds do. This tests whether bidirectional designs exist at all in the
  constrained region.
- S3-H2 (primary): per new GA seed, best F exceeds the best F of EACH of the two new filtered null
  pools. Supported only if all 3 GA seeds beat both null pools (6 comparisons); otherwise not supported.
- S3-H3 (registered progress check): if S3-H1 passes, best stage-3 F is compared against the stage-2
  best (0.00738). Best F <= 0.00738 is registered as "novelty bought at zero fitness progress"; this
  clause is reported, not treated as pass/fail of S3-H1/H2.
- Secondary, descriptive: per-pool count of F > 0 designs (GA final population vs filtered-null rate);
  pooled one-sided exact label-permutation rank over all 9 GA bests (stages 1-3) vs all 5 null bests
  (14 values); novelty vs the 4 published anchors alone for audit-passing designs.
- Report in either direction. Failures go to NEGATIVE_REGISTER.md without reframing.

## Budget and stops
Same per-seed 8 h cap and truncation reporting as amendment-02/03. About 39 CPU-h, roughly 20 h wall on
2 cores (constraint checks add genome-generation and distance compute only, no extra simulations). Free
compute only. No outcome analysis before all runs complete or truncate. No applications, sends or
contacts. Deposit watch continues independently and does not interact with stage 3.
