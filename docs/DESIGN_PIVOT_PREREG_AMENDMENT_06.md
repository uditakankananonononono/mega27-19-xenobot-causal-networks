# Design Pivot - Preregistration Amendment 06 (Stage 4: Initial-Morphology Ensemble + Permutation Power)

Status: LOCKED before any stage-4 compute. SHA-256 of this file is reported to the parent before compute.
Parent directive (2026-10-08 04:31 IST): attack the two registered stage-3 limitations: (1) the narrow
initial-morphology family, (2) the pooled best-F permutation still above 0.05. Wider init diversity first
if compute bounds force a choice.

Everything not explicitly changed below is inherited unchanged from the prereg and amendments 01-05:
grid 8x8x7 (448 voxels), fill exactly 224, validity gates (genomes.is_valid), fitness F = min(F_A, -F_B)
with the two-stage evaluation, GA parameters (pop 20, gens 16, tournament 3, elitism 1, mutation-only),
null pool size 480, sim parameters (LATTICE 0.05, STOP_T 11.0, INIT_T 1.0, PERIOD 0.5, GRAV -0.1),
120 s sim timeout with one relaunch then F=-inf, corpus floor min_d >= 0.5 vs the locked 27-design corpus
(data/stage3-corpus27.json, SHA-256 cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17)
for BOTH initialization and offspring, identical for GA and null runs, and the full section-7 audit.

## 1. Initial-morphology ensemble (attacks limitation 10)

Initialization is a stratified four-family constructive ensemble. Draw index i uses family (i mod 4):
- shell: the amendment-05 greedy low-coverage growth (kept; one attempt per try),
- ellipsoid: off-center compact ellipsoid, random center/radii, bisected to exactly 224 voxels,
- strata: random-axis layered slabs, per-layer random 2D blobs seeded from the previous layer,
- core_appendage: compact ellipsoid core plus 2-4 random-walk appendages with frontier top-up.
Each draw: up to 200 attempts of its assigned family; every failed attempt increments the init cull
(counted per family). The returned genome must pass genomes.is_valid AND min_d >= 0.5 vs the corpus.
GA population 20 = exactly 5 members per family; null pool 480 = exactly 120 per family.
Diversity metric (frozen): median pairwise min_d over the 48-isometry occupancy distance
(novelty_stage2.dist) across the init population; per-family counts logged; for null pools the metric
is computed over a deterministic 60-member subsample (random.Random(999)) and is report-only.
Calibration before locking (pilot, 15 draws/family, no fitness compute): yields shell 15/15,
ellipsoid 15/15, strata 8/15, core_appendage 15/15; all valid draws at min_d 0.5026-0.5849 vs corpus;
ensemble median pairwise min_d 0.444 (stage-3 init family: mutual min_d 0.02-0.05); within-family
median 0.222, cross-family median 0.600. Smoke test of the locked generator (seed 10 population):
median 0.4814, all four families >= 0.5127 vs corpus, 7 strata init culls.

## 2. Seed and null counts (attacks limitation 9; FROZEN)

Exactly 3 GA seeds: seeds 10, 11, 12. Exactly 2 null pools: null6000, null7000 (480 designs each).
No additional seeds or pools may be added without a new amendment.

## 3. Registered hypotheses

- S4-H1 (init diversity): each of the 3 stage-4 GA init populations has median pairwise min_d >= 0.30
  with exactly 5 members per family. SUPPORTED iff all 3 populations pass.
- S4-H2 (pooled permutation): one-sided exact label-permutation test on the difference of means over
  ALL 12 GA per-seed best F (stages 1-4, seeds 1-12) vs ALL 7 null per-pool best F (pools null1000,
  null2000, null3000, null4000, null5000, null6000, null7000); exact enumeration of C(19,7) = 50388
  labelings. SUPPORTED iff p < 0.05. The observed stage-1/2/3 values are fixed inputs: GA bests
  0.00616, 0.00920, 0.00382, 0.00586, 0.00738, 0.00694, 0.01872, 0.01228, 0.03364; null bests
  0.01298, 0.00106, 0.00362, 0.00760, 0.00292.
- S4-H3 (per-seed superiority): each stage-4 GA seed's best F beats EACH stage-4 null pool's best F
  (all 6 comparisons must hold).
- S4-H4 (production): each stage-4 seed yields >= 1 final-population F>0 design passing the full
  section-7 audit; all 3 seeds must.

Sizing rationale for S4-H2 (not a guarantee): 1000 Monte Carlo replicates drawing stage-4 GA bests
from the stage-3 GA-best empirical distribution {0.01872, 0.01228, 0.03364} and stage-4 null bests
from the stage-3 null-best distribution {0.00760, 0.00292} give P(p < 0.05) = 1.000, median p = 0.0131.

## 4. Secondaries (report-only)

Per-pool F>0 rates; stage-4 best F vs stage-3 best 0.03364; novelty vs the 4 anchors for audit-passing
designs; effect size vs anchors; per-family init cull counts; null-pool init diversity; within-family
pairwise diversity of evolved finals.

## 5. Honesty and negatives

Culls are registered per family per run. S4-H2 is registered regardless of outcome. Within-family
clustering (pilot within-family median 0.222 << cross-family 0.600) is registered as a residual
limitation. Null-pool init diversity is report-only. No padding: population, pool sizes, gen counts,
and seeds are exactly as stated.

## 6. Budget and compute

3 GA seeds (~2.5 CPU-h each) + 2 null pools (~3.5 CPU-h each) ~= 14.5 CPU-h, within the ~39 CPU-h
envelope; free compute only; 2 cores; identical fitness and audit cost structure as stage 3.

## 7. Code and custody

Runner: analysis/design_pivot/ga4.py, SHA-256 714e7e90b9d581a62c1d43201a3b000038abce65b959b1c428ecb20606dde054. Audit: audit_stage4.py adapted from
audit_stage3.py with identical section-7 checks, committed before any audit runs. Data custody:
results/design_pivot/stage4/ tarball + SHA256SUMS, custody verification against the full design
index at archive time, same standard as stage 3. Outputs land in /tmp/stage4/ and are archived
into the repo. Termination: stage 4 ends after exactly these 5 runs and their audits; any further
seeds, pools, families, floors, or metric changes require a new amendment locked before compute.
