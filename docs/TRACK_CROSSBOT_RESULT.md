# Cross-bot motion predictability result (2026-09-27)

Protocol locked before outcome compute: docs/TRACK_CROSSBOT_PROTOCOL.md, SHA-256
27635b2fc1dbcb37595176ee6680664c79ae0c47ada896eb110f5239ecb82fb2 (commit 10a1a84).
Estimator: src/track_crossbot.py; data: swarm-lab/xenobots commit
3d8e4c3f460578700039a1c111d14adc6b1ccb52, all 12 zip SHA-256 verified against
data/source-manifest.json. One pipeline run, no re-specification.

## Primary outcome: negative

Adding same-arena population features (others' mean velocity vector, others' mean
speed, focal distance to others' centroid at t-1) to a focal bot's own-history ridge
does NOT reliably improve 10-second-ahead velocity prediction on held-out bots:

- Median relative RMSE gain across the 12 arena replicates: **-0.00017**
  (mean -0.00017); 4/12 replicates positive; exact two-sided sign-flip p = 0.388.
- Only 2/12 replicates (12 and 14) show a positive gain exceeding the 95th percentile
  of their circular-alignment null; the largest, replicate 12, is +0.00131 (about
  0.13% relative RMSE) - real against its null but negligible in magnitude.
- 5/12 replicates sit above their null p95 while having near-zero or negative gains;
  several nulls are themselves systematically negative (shifted population features
  hurt), meaning the population features carry arena-state information, but aligned
  cross-bot timing adds essentially nothing usable for prediction.

Per-replicate numbers: results/track-crossbot.json.

## Interpretation boundaries
- This is a dynamical/methods result about shared-arena motion statistics. One
  condition per numbered replicate blocks any condition-level or biological reading;
  it says nothing about cellular causal networks, memory, or intelligence.
- A null/negative here does not prove Xenobots do not influence each other; the test
  covers one feature set, one horizon (10 s), one estimator (ridge), tracker pixel
  coordinates, and bots swimming in the same arena without imposed perturbation.
- Tracker limitations apply: ignore-filtered artifacts, track fragmentation, and
  pixel-coordinate noise are not corrected.
- Prior-art check stands: the authors' published five behavior classes and aggregation
  analyses are not contradicted or extended biologically by this result.

## Reproducibility
21 unit tests pass (16 pre-existing + 5 new for this module).
Exact run: `python3 src/track_crossbot.py <rawdata dir>` with N_NULL=100, SEED=20260927,
h=10, W=10, ridge penalty 1.0, per-replicate every-3rd-bot test groups.
