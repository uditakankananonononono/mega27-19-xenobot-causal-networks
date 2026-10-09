# Design Pivot - Preregistration Amendment 08 (Stage 6: Second-Round Champion-Seeded Intensification - Compounding or Saturation)

Status: LOCKED before any stage-6 compute. SHA-256 of this file is reported to the parent before compute.
Decision authority: parent directive 2026-10-09 14:46 IST ("resume active building on the xenobot
causal-nets continuation while deposits are pending ... Report what you're building"), under the
standing grant (everything except email as the user; paid spend per-action; free compute only).

Stage-6 question: does champion-seeded intensification COMPOUND - a second mutation-only round from
the stage-5 champion producing another material gain - or did stage 5's 4.75x jump (0.03364 ->
0.15994) saturate this design class's reachable effect size in one round? Either registered outcome
is informative: compounding re-opens the path toward anchor scale; saturation maps the ceiling and
returns the next-question choice to the user/board with evidence.

New evidence motivating the stage (registered, from stage-5 outputs): all three stage-5 winners are
morphologically convergent - pairwise occupancy min_d 0.0000-0.0217 across seed20 g23_i0 (0.15994),
seed21 g23_i9 (0.04236), seed22 g23_i1 (0.04152) - while differing in actuation (the two stage-6
champions differ in 10 material cells and 35 phase cells). Stage 5's gains came from actuation
program search on one shape basin, not morphology exploration. This is registered as standing
honesty item 20 in NEGATIVE_REGISTER.

Everything not explicitly changed below is inherited unchanged from the prereg and amendments 01-07:
grid 8x8x7 (448 voxels), fill exactly 224, validity gates (genomes.is_valid), fitness F = min(F_A,
-F_B) with the two-stage evaluation, GA parameters (pop 20, tournament 3, elitism 1, mutation-only,
GENS = 24), sim parameters (LATTICE 0.05, STOP_T 11.0, INIT_T 1.0, PERIOD 0.5, GRAV -0.1), 120 s sim
timeout with one relaunch then F=-inf, corpus floor min_d >= 0.5 vs the locked 27-design corpus
(data/stage3-corpus27.json, SHA-256 cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17)
for BOTH init draws and offspring/mutants, identical rules for GA and null arms, and the full
section-7 audit with the stage-1 anchor energy scale (max anchor F_A 5.57002).

## 1. Champion-seeded initialization

Champions are frozen in data/stage6-champions.json (SHA-256
03ab6cc7df2461de43dae10698ccf53696099232cf01e273755262b6321c9314): the stage-5 champion
(seed20 g23_i0, F = 0.15994, elite-carried from the gen22 i19 lineage) and the stage-5 second
(seed21 g23_i9, F = 0.04236), extracted from the durable run checkpoints (source checkpoint SHAs
recorded inside the file). The second is morphologically near-identical (occupancy min_d 0.0216)
but carries a different actuation program - the dimension stage 5's gains actually came from;
stated plainly, the two-champion design seeds two actuation programs, not two shapes.
- GA population 20 = the 2 champions (slots 0-1) + 18 stratified ensemble draws (i = 2..19, family
  i%4: shell 4, ellipsoid 4, strata 5, core_appendage 5). Champions exempt from the init draw and
  floor: pre-verified valid and floor-compliant vs the corpus (min_d 0.5697 and 0.5687).
- GENS = 24, unchanged: stage 5 showed all bests arriving at gen 20+ under this budget.
- Exactly 3 GA seeds: 30, 31, 32. Exactly 1 null pool: null9000. No additions without a new amendment.

## 2. Champion-mutant null (identical sharp control)

null9000 = 480 champion-mutants: draw i applies ONE mutate() call (identical operator to the GA) to
parent CHAMP_NAMES[i % 2] (alternating, 240 each); up to 200 attempts per draw for a valid +
floor-passing mutant; valid-but-subfloor attempts increment per-champion culls; on exhaustion the
draw is recorded as a failed row with F = None (frozen rule). Identical fitness evaluation to the
GA arm. Same rationale as amendment-07: equal-budget random champion-mutation is the sharp control
for whether selection adds value.

## 3. Registered hypotheses

- S6-H1 (production, continuity check): each of the 3 seeds yields >= 1 final-population F>0 design
  passing the full section-7 audit. STATED AS EXPECTED-VACUOUS: the champions are F>0 and elitism
  preserves them; registered for chain continuity, not as evidence of anything.
- S6-H2 (primary): at least one stage-6 seed's best F >= 0.19993 (= 1.25 x the stage-5 champion
  0.15994). The 1.25x margin is the same materiality bar logic as amendment-07, frozen here as a
  stated judgment call. If no seed clears the bar: registered SATURATION - one intensification round
  captured this design class's reachable gain under mutation-only search at this budget; the
  next-question choice (including the stage-5 proposal's Option C) returns to the user/board with
  that evidence. A saturation result is NOT a failed stage: it is the ceiling measurement this
  stage exists to buy.
- S6-H3: each stage-6 seed's best F strictly beats the null9000 best F (3 comparisons).

## 4. Secondaries (report-only)

Best stage-6 F vs the stage-5 champion (any improvement, including sub-margin); per-arm F>0 rates;
novelty vs the 4 anchors for audit-passing designs; culls per family (init) and per champion
(mutant); init diversity including champions; morphology-convergence follow-up: occupancy min_d of
each seed's final population vs the stage-5 champion (does round 2 stay in the basin?); a post-hoc
pooled permutation including stage-6 bests, marked DESCRIPTIVE - S4-H2's registered verdict
(p = 0.01016) stands as registered and is not re-fished.

## 5. Honesty and negatives

S6-H1's expected vacuity is stated above. The null's mutation depth (one mutate() call) is one
frozen choice among plausible ones. All three GA seeds share the same two champions, so seeds are
not fully independent replicates - stated plainly; S6-H2 counts seeds, not independent discoveries.
The two champions are morphologically near-identical by the lane's own occupancy metric; the
stage-5 convergence finding (register item 20) limits any morphology-generalization claim from this
stage. Init draws remain floor-constrained with per-family culls registered. No padding: seeds,
pool size, and generation counts are exactly as stated.

## 6. Budget and compute

3 seeds x 24 generations (~490 evaluations each) + 480 mutants ~= 1950 evaluations ~= 17-18 CPU-h on
2 cores; free compute only; identical fitness and audit cost structure as stages 3-5.

## 7. Code, pilot calibration, custody, termination

Runner: analysis/design_pivot/ga6.py, SHA-256 f1a600da6d1dd6d611e49d11afd04aabc1b79d0e71f4560c7af02490c5ff1bba
(ga5.py with only stage-6 output paths and champion names changed; POP/GENS/operator/fitness/audit
logic byte-identical). Audit: analysis/design_pivot/audit_stage6.py, SHA-256
8f65eed910eda3f75d52eb1ed8b0b03268e0d28249cd3ff9aec6fa6850c31a31, committed before any audit runs.
Pilot calibration BEFORE locking (amendment-05 lesson): both champions pass validity and floor
(0.5697, 0.5687); 40 champion-mutants smoked per champion (33/40 and 34/40 valid, ALL valid mutants
pass the floor, 0 floor culls); seed-30 init smoke: diversity median 0.4865, families 4/4/5/5,
0 init culls in the smoke draw; mutant stream determinism under resume-replay inherited unchanged
from ga5.py (verified in amendment-07's pilot). Custody: results/design_pivot/stage6/ tarball +
SHA256SUMS, verified against the full design index at archive time, same standard as stages 3-5.
Outputs land in /tmp/stage6/ and are archived into the repo. Termination: stage 6 ends after
exactly these 3 seeds + 1 pool + audits; any further seeds, pools, objective changes, margins, or
mutation changes require a new amendment locked before compute.
