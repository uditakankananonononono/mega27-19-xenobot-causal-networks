# Locked protocol: cross-bot motion predictability in shared arenas (methods test)

Locked 2026-09-27 ~15:52 IST before any outcome computation. Only structural/QC
properties of the data have been inspected (row counts, track counts per replicate,
frame ranges, ignore-flag values). No motion statistic, fit, or predictability score
has been computed on these tracks by this agent. This protocol is a NEW question,
versioned separately from all prior locked protocols; it does not amend them.

## Question
In the 12 public multi-bot arena recordings (swarm-lab/xenobots, commit
3d8e4c3f460578700039a1c111d14adc6b1ccb52), does the simultaneous state of the OTHER
bots in the same arena improve short-horizon prediction of a focal bot's motion,
beyond the focal bot's own recent history, under bot-level grouped splits?

## Why this is not prior art, and its limits
Blackiston et al. (Science Robotics 2020) published five behavior classes, motion
metrics and collective aggregation structure from these tracks. They did not publish a
held-out-bot short-horizon cross-bot predictability test with a temporal-alignment
null. This study is a dynamical/methods artifact: one condition per numbered replicate
means NO condition-level or biological interpretation is possible, and nothing here is
a cellular causal-network, memory, or intelligence result. A positive score is evidence
about shared-arena motion statistics only.

## Data and units (structural facts already verified)
- 12 replicate CSVs (replicates 3-14), SHA-256 verified against data/source-manifest.json.
- Rows with ignore=TRUE dropped (tracker artifacts; rep 3 example: 25 of 200k rows).
- 7-12 simultaneously tracked bots per replicate, all remaining tracks >=600 frames;
  15,308-86,400 frames per replicate at 1 frame/second (period per upstream data_prep.R).
- Positions are tracker pixel coordinates; motion is in pixels/second. Units are the
  arena recordings. Each replicate is one arena; conditions are not separable from
  replicates, which is irrelevant to the dynamical question and blocks biological claims.

## Estimator (all constants fixed here)
For each focal bot i and frame t (edges excluded):
- Target: focal velocity vector at t+h, h = 10 frames (10 s), computed as
  (pos(t+h) - pos(t+h-1)).
- Own-history features: focal velocities at t-1..t-10 (20 scalars) plus intercept.
- Full model adds population features at t-1: mean velocity vector of all other bots,
  mean speed of other bots, focal distance to the centroid of other bots (4 scalars).
- Ridge regression, closed form, L2 penalty 1.0 on all non-intercept coefficients,
  matching the style of src/organoid_prospective.py.

## Splits and leakage controls
- Per replicate: bots are split into train/test groups; every test bot is scored with
  coefficients fit ONLY on train bots' timepoints. With n bots, test group = ceil(n/3)
  bots, chosen as every 3rd bot in track_fixed sort order; remainder are train.
- Frames where any feature/target is undefined (gaps, edges) are dropped, not imputed.
- Primary endpoint: per-replicate relative RMSE reduction of the full model vs the
  own-history model on test bots (positive = cross-bot information helps).
- Alignment null: 100 circular time shifts of the population-feature series relative
  to the focal series within each replicate, full pipeline recomputed; report the
  percentile of the real gain in its null distribution. A gain that does not exceed
  the null is shared-condition similarity, NOT real-time coupling.
- Secondary: median per-replicate gain and exact two-sided sign-flip p over the 12
  replicates.

## Stop rule
The pipeline is run once as specified. Outcomes are reported exactly as they land:
positive-with-null-support, null-indistinguishable, or negative are all publishable
outcomes in the result doc. No post-outcome re-specification of h, window, features,
penalty, splits, or null count as confirmatory; any such exploration is labeled
exploratory. No biological, condition-level, or intelligence claim under any outcome.

## Deliverables
src/track_crossbot.py, tests/test_track_crossbot.py (no-leakage and assembly tests),
results/track-crossbot.json, docs/TRACK_CROSSBOT_RESULT.md.
