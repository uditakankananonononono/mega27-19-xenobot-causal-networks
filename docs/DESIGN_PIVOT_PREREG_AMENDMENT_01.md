# PREREG AMENDMENT 01: budget rescope (option a, parent-approved 2026-09-29 11:26 IST)

Locked 2026-09-29 before ANY selection-used compute. Amendment to docs/DESIGN_PIVOT_PREREG.md
(SHA-256 19441cc5a97c5e4eb1a6fd4c684ffa0a043bd07a3e5abe35a0fb39e8b32ce061). Legal under the prereg's
amendment rule (locked before the compute it covers). Trigger: registered-pilot measurement of ~46 s per
evaluation at ~356 voxels made the original budget (pop 50 x 30 gens = 9000 sims, ~115 CPU-hours) truncate
to ~6 generations under the 8 h/seed cap.

CHANGES (everything else in the prereg stands unchanged):
1. Population 50 -> 24. Generations 30 -> 20. Stage-1 total: 3 seeds x 24 x 20 = 1440 genomes (was 9000).
2. Two-stage evaluation: condition B (phase shift +0.5) is computed ONLY when condition A yields F_A > 0;
   otherwise F = min(F_A, -F_B) cannot exceed 0, so F is recorded as "F_A<=0 (B skipped)" and treated as
   F_A for ranking purposes. EXACTNESS ARGUMENT (locked): under F = min(F_A, -F_B), F > 0 iff F_A > 0 and
   F_B < 0; skipping B when F_A <= 0 changes no positive-fitness detection and no argmax. Selection,
   best-design identification, H1/H2 tests are unaffected.
3. Random-search null budget: 480 valid random genomes per seed (was 1500), same two-stage rule,
   budget-matched to the amended GA.
4. Corpora (per prereg sec 6 drop clause): H3 published anchors = the 4 author demo .vxa designs
   (reconfigurable_organisms repo, hashes in data/design-corpora-manifest.json). H4 morphological-novelty
   evidence is THIN (corpus of 4) and will be stated as such; the headline deposit finding - no public
   machine-readable corpus of evolved xenobot designs exists in any checked deposit - is reported
   prominently as its own result.
5. Budget estimate after amendment: ~4-7.5 CPU-hours per seed (480 genomes, ~40-50% skipping B),
   within the 8 h/seed cap; truncation rule of the prereg still applies as backstop.
