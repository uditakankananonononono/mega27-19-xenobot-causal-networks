# PREREG AMENDMENT 03: STAGE 2 - does the stage-1 H2 failure replicate? (locked before any stage-2 compute)

Locked 2026-10-01 IST. Basis: user instruction "Deploy all tasks" relayed by the parent at 11:43 IST; the
parent asked the lane to pick the most defensible stage-2 scope from the current gate state. Chosen scope
is an assumption and may be redirected by the user. Extends docs/DESIGN_PIVOT_PREREG.md
(19441cc5a97c5e4eb1a6fd4c684ffa0a043bd07a3e5abe35a0fb39e8b32ce061), AMENDMENT_01
(d51e8f484955617f185e88da73c9d3fd777073c26b9bcf82f4557cbb6c17c07d), AMENDMENT_02
(138a360c45a3a73a7e5f75aa6671ffa2653b66d695410222735c49359d2adc3b). Everything not changed here stands.
SIMULATION-ONLY.

## Rationale
Stage 1 had one shared random null draw (480 designs) with a heavy-tailed best (0.01298, 4/480 bidirectional).
Three GA seeds vs one null draw cannot separate "GA is no better than random" from "one lucky null draw".
Stage 2 replicates with fresh seeds and independent null draws. No new objective, no new fitness.

## Design (locked)
- GA: seeds 4, 5, 6; pop 20 x 16 generations; identical code, fitness, audit (sec 7) and novelty procedure.
- Null: two independent pools of 480 valid random genomes, Random(2000) and Random(3000); identical fitness.
- Stage-1 data are NOT re-used for selection. Pooled analyses (below) are labelled pooled.
- Code change: analysis/design_pivot/ga.py takes a null seed argument and writes seeds>=4 / null!=1000 to
  /tmp/stage2; default behavior for stage-1 seeds is unchanged.

## Registered tests
- S2-H1: each new GA seed yields >= 1 final-population design with F > 0 passing the full sec-7 audit.
- S2-H2 (primary): per new GA seed, best F exceeds the best F of EACH of the two new null pools. Supported
  only if all 3 GA seeds beat both null pools (6 comparisons); otherwise not supported. Secondary,
  descriptive: pooled over all 3 stage-1 + 3 stage-2 GA seeds vs all 3 null pools (best-F ranks), and the
  per-pool count of F > 0 designs (GA final population vs null rate); no p-values beyond a one-sided exact
  rank statement over the 6 GA bests vs 3 null bests (9 values, permutation of labels).
- S2-H3: audit-passing new candidates are novel by the stage-1 rule (min occupancy distance >= 0.5 against
  the 4-anchor corpus plus the 7 stage-1 audited candidates).
- Report in either direction. A failed S2-H2 is registered in NEGATIVE_REGISTER.md without reframing.

## Budget and stops
Same per-seed 8 h cap and truncation reporting as amendment-02. About 39 CPU-h, roughly 20 h wall on 2 cores.
No outcome analysis before all runs complete or truncate. No applications, sends or contacts. Deposit
watch continues independently and does not interact with stage 2.
