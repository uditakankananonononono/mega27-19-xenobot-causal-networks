# Design Pivot - Preregistration Amendment 07 (Stage 5: Champion-Seeded Effect-Size Intensification)

Status: LOCKED before any stage-5 compute. SHA-256 of this file is reported to the parent before compute.
Decision authority: parent directive 2026-10-08 16:06 IST relaying the user's delegation of the stage-5
choice ("do whatever"); the lane selected Option A (attack effect size) per
docs/DESIGN_PIVOT_STAGE5_PROPOSAL.md, on the register's evidence: stage 4 bought power, not design
quality; best-F stalled (0.03364 stage 3 -> 0.02156 stage 4); magnitudes ~165-258x below anchors.
Stage-5 question: can mutation-only search improve MATERIALLY on the frozen champions, or are the
champions local optima of this design class under this search?

Everything not explicitly changed below is inherited unchanged from the prereg and amendments 01-06:
grid 8x8x7 (448 voxels), fill exactly 224, validity gates (genomes.is_valid), fitness F = min(F_A, -F_B)
with the two-stage evaluation, GA parameters (pop 20, tournament 3, elitism 1, mutation-only; GENS
changed below), sim parameters (LATTICE 0.05, STOP_T 11.0, INIT_T 1.0, PERIOD 0.5, GRAV -0.1), 120 s sim
timeout with one relaunch then F=-inf, corpus floor min_d >= 0.5 vs the locked 27-design corpus
(data/stage3-corpus27.json, SHA-256 cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17)
for BOTH init draws and offspring/mutants, identical rules for GA and null arms, and the full section-7
audit with the stage-1 anchor energy scale (max anchor F_A 5.57002).

## 1. Champion-seeded initialization

Champions are frozen in data/stage5-champions.json (SHA-256
10f7b5317ff8d51826c937bbf33138c22b1bb81c27230272af5c4f929feccb2e): the stage-3 champion
(seed9 g15_i0, F = 0.03364) and the stage-4 champion (seed12 g15_i0, F = 0.02156), extracted from the
durable run checkpoints (source checkpoint SHAs recorded inside the file).
- GA population 20 = the 2 champions (slots 0-1) + 18 stratified ensemble draws (i = 2..19, family i%4:
  shell 4, ellipsoid 4, strata 5, core_appendage 5). Champions are exempt from the init draw and floor:
  they are the registered starting material, pre-verified valid and floor-compliant vs the corpus
  (min_d 0.5711 and 0.5151).
- GENS = 24, extended from 16: stage-3/4 best-F trajectories plateaued at gens 13-15, so intensification
  budget goes to generations past the plateau. All other GA parameters unchanged.
- Exactly 3 GA seeds: 20, 21, 22. Exactly 1 null pool: null8000. No additions without a new amendment.

## 2. Champion-mutant null (the sharp control)

null8000 = 480 champion-mutants: draw i applies ONE mutate() call (identical operator to the GA) to
parent CHAMP_NAMES[i % 2] (alternating champions, 240 each); up to 200 attempts per draw for a valid +
floor-passing mutant; valid-but-subfloor attempts increment per-champion culls; on exhaustion the draw
is recorded as a failed row with F = None (frozen rule). Identical fitness evaluation to the GA arm.
Rationale: stage 5 asks whether SELECTION adds value over random mutation around the champions at equal
evaluation budget; an unseeded ensemble null would be vacuous because the seeded champions already beat
every such pool. The null's diversity metric is champion-local by design - report-only and NOT
comparable to the stage-4 ensemble pools.

## 3. Registered hypotheses

- S5-H1 (production, continuity check): each of the 3 seeds yields >= 1 final-population F>0 design
  passing the full section-7 audit. STATED AS EXPECTED-VACUOUS: the champions are F>0 and elitism
  preserves them; registered for chain continuity, not as evidence of anything.
- S5-H2 (primary): at least one stage-5 seed's best F >= 0.04205 (= 1.25 x the stage-3 champion
  0.03364). If no seed clears the bar: registered NULL - the champion neighborhoods are local optima
  under mutation-only search at this budget, which is the pre-registered trigger for pivoting the
  question (proposal Option C). The 1.25x margin is a materiality bar, frozen here as a stated judgment
  call: smaller improvements would not change the effect-size picture (~165-258x below the strongest
  anchor) and claiming progress on noise-sized gains is the failure mode this bar exists to prevent.
- S5-H3: each stage-5 seed's best F strictly beats the null8000 best F (3 comparisons). This is the
  sharp test that selection adds value over random champion-mutation at equal evaluation budget.

## 4. Secondaries (report-only)

Best stage-5 F vs the champions (any improvement, including sub-margin); per-arm F>0 rates; novelty vs
the 4 anchors for audit-passing designs; culls per family (init) and per champion (mutant); init
diversity including champions; a post-hoc pooled permutation including stage-5 bests, marked
DESCRIPTIVE - S4-H2's registered verdict (p = 0.01016) stands as registered and is not re-fished.

## 5. Honesty and negatives

S5-H1's expected vacuity is stated above. The null's mutation depth (one mutate() call per draw) is one
frozen choice among plausible ones. All three GA seeds share the same two champions, so seeds are not
fully independent replicates - stated plainly; S5-H2 counts seeds, not independent discoveries. Init
draws remain floor-constrained with per-family culls registered. No padding: seeds, pool size, and
generation counts are exactly as stated.

## 6. Budget and compute

3 seeds x 24 generations (~490 evaluations each) + 480 mutants ~= 1950 evaluations ~= 17-18 CPU-h on
2 cores; free compute only; identical fitness and audit cost structure as stages 3-4.

## 7. Code, pilot calibration, custody, termination

Runner: analysis/design_pivot/ga5.py, SHA-256 7791296ce5320bb704e3c4a5f6f3e6770d21291f78e402d23d914d334d43354e.
Audit: analysis/design_pivot/audit_stage5.py, SHA-256 1112b81691b0ec6c2e395d8845aa31f871949fd58596876653a1d88745659384,
committed before any audit runs. Pilot calibration BEFORE locking (amendment-05 lesson): both champions
pass validity and floor (0.5711, 0.5151); 40 champion-mutants smoked (18/20 and 15/20 valid, all valid
mutants pass the floor, 0 floor culls); seed-20 init smoke: diversity median 0.4762, families 4/4/5/5,
4 strata init culls; mutant stream verified deterministic under resume-replay. Custody:
results/design_pivot/stage5/ tarball + SHA256SUMS, verified against the full design index at archive
time, same standard as stages 3-4. Outputs land in /tmp/stage5/ and are archived into the repo.
Termination: stage 5 ends after exactly these 3 seeds + 1 pool + audits; any further seeds, pools,
objective changes, margins, or mutation changes require a new amendment locked before compute.
