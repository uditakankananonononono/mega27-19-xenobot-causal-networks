# REGISTERED PILOT RESULT (prereg sec 8; fitness values NOT used for selection/tests)

2026-09-29. 10 valid random genomes (seed 999) through the full 2-condition bidirectional wrapper,
Kriegman pass-2 settings (8x8x7, 5cm voxels, gravity -0.1, 2Hz, 11s evals, 1s settle).

- 20/20 evals completed ok. Voxel counts 350-366 (random init >= 50% fill is near-dense).
- Wall time per eval: median 47.2s, mean 74.3s, range 45.1-588.2s.
  Excluding one outlier (588s; see anomaly below): mean ~46.6s.
- F_A (one-way displacement, voxel units): [-0.68, -0.62, -0.58, -0.14, -0.06, 0.4, 0.47, 0.52, 0.55, 0.69] - random designs barely move, as expected.
- F_A > 0 in 5/10 genomes -> amended two-stage cost ~70s/design.
- AMENDED BUDGET: ~9.4 CPU-h/seed, ~28.2 CPU-h for 3 seeds
  (within the 8 h/seed cap; ~half the cap on 2 cores if seeds run serially 2-at-a-time).

ANOMALY (honest record): genome 7 condition A measured 588.2s wall with ok=True despite a 150s subprocess
timeout in pilot.py (timeout should have raised). Cause undetermined (clock jump vs timeout not enforced).
Stage-1 prereg sec 4 caps sims at 120s with F=-inf on timeout, so pathological genomes become registered
failures there; if the timeout proves unenforced in stage 1 this becomes a harness bug and is registered.
