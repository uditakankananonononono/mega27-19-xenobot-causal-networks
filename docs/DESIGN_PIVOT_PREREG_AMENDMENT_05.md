# PREREG AMENDMENT 05: STAGE 3 init mechanism fix (locked before any stage-3 compute)

Locked 2026-10-07 IST. Supersedes ONLY the initialization mechanism of AMENDMENT_04
(a159f29a3ca26cd4fb21fb965f7fa0cad15e9112b38b50970647243218820d65); every other clause of
amendments 01-04 and the base prereg stands unchanged. SIMULATION-ONLY. No stage-3 compute has run.

## Finding that forces this amendment (pre-compute smoke test, registered)
Amendment-04's locked initialization ("random valid genomes FILTERED to min_d >= 0.5, rejection-sampled")
is unsatisfiable in practice: the prereg's occupancy distance saturates for near-full-grid designs. The
converged family fills 342-376 of 448 voxels; 40 uniform-random valid genomes measured min_d 0.26-0.31 vs
the locked corpus (max 0.308), so rejection sampling at floor 0.5 rejects essentially every draw and the
GA cannot initialize. This is a measurement property of the metric on near-full grids, not a bug.
No compute ran under amendment-04.

## Replacement initialization (locked)
Constructive initialization, implemented in analysis/design_pivot/ga.py
SHA-256 06c0e3395525bacd8c6c3598551856d00b69dba440b0dd565c402e1f04776a7a:
1. Coverage: each grid cell scored by how many corpus designs with >= 300 voxels cover it (corpus designs
   COM-aligned to grid center, raw frame).
2. Growth: seed at the lowest-coverage cell; grow a 6-connected set to exactly 224 voxels (50% fill),
   each step adding a uniform-random choice among the 6 lowest-coverage frontier cells.
3. Apply a uniform-random symmetry of the 8x8x7 box (16 elements: x/y swap x axis flips).
4. Random materials (1-4) on occupied cells (at least one Active), random phases in [-1,1] as before.
5. Accept only if valid (prereg sec 3) AND exact registered min occupancy distance vs the full 27-design
   corpus >= 0.5 (identical arithmetic to novelty_stage2.py; verified bit-identical against it on
   samples). Rejected draws are counted (cull counts) and regenerated; 200-try cap, then RuntimeError.
Measured on the locked corpus: 6/6 constructed genomes valid with min_d 0.568-0.585; ~0.33 s per genome.
Init morphology diversity inside the novel region is narrow (mutual min_d ~0.02-0.05) - stated plainly:
the constraint confines morphology to a thin peripheral-shell family; material/phase diversity is
unconstrained. Null pools (Random(4000), Random(5000)) use the IDENTICAL constructive distribution.
Offspring culling (amendment-04) is unchanged and measured effective: 10/10 mutated children of a
constructed genome stayed >= 0.5.

## Everything else stands
Corpus (data/stage3-corpus27.json, cd9c301671d1777eccaa3f5d93ade6acd0147d56397026bf68c75e5c9de0cc17),
seeds 7/8/9, pop 20 x 16, fitness, audit, S3-H1/H2/H3 tests, secondaries, budget (~39 CPU-h, 8 h/seed cap,
free compute only), truncation and reporting rules exactly as amendment-04. Report in either direction.
