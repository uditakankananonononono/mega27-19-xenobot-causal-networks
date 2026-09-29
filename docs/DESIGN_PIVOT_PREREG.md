# PREREGISTRATION: evolutionary design of xenobot morphologies for literature-unreported behaviors (stage 1: bidirectional locomotion)

Locked 2026-09-29 before ANY outcome compute (including the registered pilot below). SHA-256 of this file
is reported to the parent at lock time. Amendments allowed only as new locked versions before the compute
they cover. ALL RESULTS ARE SIMULATION-ONLY AND UNVALIDATED IN WET LAB.

## 1. Objective and hypotheses

Stage 1: evolve voxel body plans that locomote in BOTH +x and -x under two actuation phase conditions of the
same design (bidirectional locomotion), a behavior not reported in the xenobot literature (published:
one-way linear/circular locomotion, pushing/aggregation, kinematic self-replication, cilia swimming).
- H1: evolutionary search finds designs with bidirectional fitness > 0 (both directions positive).
- H2: evolved best bidirectional fitness exceeds the best found by random search with identical evaluation budget.
- H3: published reference designs (Kriegman 2020/2021 corpora) score <= 0 on bidirectional fitness
  (behavior is novel for this design class).
- H4: any design passing H1-H3 is morphologically novel vs the published corpora (metric + threshold in sec. 6).
Each hypothesis is reported as supported / not supported / inconclusive. Failures go to NEGATIVE_REGISTER.md.

## 2. Simulation environment (fidelity to Kriegman 2020 pass-2 settings)

From exp/Locomotion_pass2.py (reconfigurable_organisms, CC0): voxel size 0.05 m; gravity -0.1 (scaled);
actuation via thermal expansion at 2 Hz (TempPeriod 0.5 s, TempAmp 39, TempBase 25); stiffness 5e6 (soft) /
5e8 (hard); density 1e6; Poisson 0.35; friction uS 1, uD 0.5; DT_FRAC 0.9; floor enabled, slope 0 (stage 1);
sim time 11 s per eval = 1 s settle (InitCmTime) + 10 s fitness window. Engine: headless Voxelyze 0.9.92
(same build as docs/DESIGN_PIVOT_BUILD_VERIFICATION.md) with our CM-vector driver patch (GetCM x,y,z printed
each output step; patch is output-only, physics untouched).

## 3. Design space and encoding

- Grid: 8 x 8 x 7 voxels (matches pass-2 IND_SIZE). Materials per voxel: 0 empty, 1 Passive_Soft, 2 Passive_Hard,
  3 Active_+, 4 Active_-; phase offset per voxel in [-1, 1] (fractions of actuation period, engine convention).
- Validity (checked pre-evaluation, invalid genomes rejected and regenerated, never evaluated): >= 50% of
  voxels non-empty (MIN_PERCENT_FULL = 0.5); at least one Active voxel; design connected (single 6-connected
  component of non-empty voxels); no voxels outside the 8x8x7 grid.
- Search: direct-encoding steady-state GA. Population 50 (pass-2 value). Generations 30 per seed (budget
  decision, sec. 8 - NOT 5000; this is a bounded stage, reported as such). Selection: tournament size 3;
  elitism 1. Mutation only (no crossover): each child = clone of winner + K mutations, K ~ uniform{1..6};
  a mutation flips one random voxel to a random material (0-4) or perturbs one random phase by U(-0.25, 0.25)
  clipped to [-1, 1]. Initialization: uniform random genomes made valid per above. Seeds: 3 (seeds 1, 2, 3
  drive numpy/random exactly; recorded).

## 4. Fitness (exact definitions; wrapper = analysis/design_pivot/fitness.py, validated in build verification)

Each design is evaluated TWICE on flat ground:
- Condition A: phase offsets as encoded.
- Condition B: all phase offsets shifted by +0.5 (half period), wrapped to [-1, 1].
For each condition, wrapper fitness_locomotion = (x_CM(final sample) - x_CM(first sample at/after InitCmTime
= 1.0 s)) / 0.05 m (voxel units), from the driver's 3D CM output.
DESIGN FITNESS F = min(F_A, -F_B) in voxel units. F > 0 requires net +x motion under A AND net -x motion
under B. Sim failures (driver crash, timeout 120 s, import errors) count as F = -inf and are logged, not retried
beyond one relaunch.

## 5. Nulls and anchors

- Random-search null: 1500 valid random genomes (same initialization distribution), each evaluated identically
  (2 conditions), budget-matched to 50 x 30. Best-of-random vs best-of-evolved compared per seed; report
  full distributions (no best-run cherry-picking).
- Published-design anchors: every design in the corpora of sec. 6 re-evaluated headlessly on the SAME
  bidirectional fitness (expect F <= 0; any F > 0 anchor design is reported - it would weaken the novelty
  claim and MUST NOT be hidden).
- Flat-ground anchor sanity: corpus designs' one-way locomotion fitness (condition A only) reported as an
  engine-fidelity check.

## 6. Novelty measurement

Corpora: Kriegman 2020 PNAS supplementary design files + reconfigurable_organisms bestSoFar archives +
Kriegman 2021 PNAS (self-replication) designs, fetched with chain-of-custody hashes (manifest in
data/design-corpora-manifest.json). If a corpus proves unfetchable, that corpus is dropped and the limitation
reported (never silently).
Metric: for designs G (candidate) and P (published), take occupancy sets (voxel coords of non-empty cells,
any material). d(G,P) = |G symdiff P| / |G union P|, minimized over the 24 proper+improper cube rotations and
all integer translations aligning centers of mass to nearest voxel. A candidate is NOVEL iff min_P d(G,P) >= 0.5
over all corpus designs. Material composition differences are reported descriptively (not part of the metric).

## 7. Exploit checklist (every design with F > 0, before it counts as a candidate)

1. Trajectory audit: y and z CM displacement over the eval <= 0.15 m cumulative (design must not drift/jump
   sideways or vertically to game +x/-x differences); violations -> negative register, not a result.
2. Energy sanity: |F_A| and |F_B| each <= 3x the largest corpus one-way flat-ground fitness we measure;
   larger -> flagged as suspected physics exploit, investigated, registered.
3. Determinism check: champion re-run twice; identical F required (engine is deterministic; divergence
   indicates a harness bug - registered, design excluded).
4. Validity re-check of the final genome (grid bounds, connectedness, >= 50% fill).
5. No design voxels may be marked fixed; no fixed regions exist in stage-1 scenes at all (flat ground).

## 8. Budget, pilot, truncation

- REGISTERED PILOT (part of this prereg, runs immediately after lock): 10 valid random genomes through the
  full 2-condition wrapper to measure per-eval wall-clock distribution. Pilot fitness values are NOT used for
  any selection or hypothesis test; they calibrate the budget below and seed nothing.
- Stage-1 budget: 3 seeds x (50 pop x 30 gens x 2 conditions) = 9000 sims planned. Hard wall-clock cap:
  8 h per seed. If a seed hits the cap mid-generation, it stops and is reported TRUNCATED with the number of
  completed generations; truncated seeds count as their own data point, never silently extended.
- Checkpoints: population + RNG state saved every generation; git checkpoint of results every 30 min.

## 9. Reporting plan

Per seed: fitness trajectory (gen x max/median F), best design + genome + its corpus distance, comparison vs
random null (same seed budget), anchors table. Overall: H1-H4 verdicts, all failures and exploits in
NEGATIVE_REGISTER.md, full data under results/design_pivot/. No wet-lab claims. No public posts. Judge-verdict
route unchanged (user/parent-controlled).
