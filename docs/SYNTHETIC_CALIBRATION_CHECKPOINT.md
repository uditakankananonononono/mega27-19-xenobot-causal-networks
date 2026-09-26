# Synthetic ground-truth calibration: cross-cell mean forecasts are not causally specific

2026-09-26. Separate methods-only protocol `docs/PIVOT_03_SYNTHETIC_CALIBRATION.md` SHA-256 in adjacent `.sha256` file was pushed before running scores. See `src/synthetic_calibration.py` and `results/synthetic-calibration.json`; 24 independent simulated replicates/scenario, 16 fit and eight unseen replicate scores, 64 simulated cells, 240 scored frames. Model and seed are in the protocol and code. This is not evidence about Xenobots or epidermal organoids.

| Ground truth | Cross-cell coupling g | Shared external drive h | Mean held-out RMSE relative gain from cross-cell mean |
|---|---:|---:|---:|
| independent null | 0 | 0 | -0.0000009125 |
| direct mean-field coupling | 0.25 | 0 | +0.002109689 |
| shared drive with no cell-to-cell coupling | 0 | 0.5 | +0.035643735 |

The simple predictor discriminates the coupling case from independent noise in this chosen simulator, but **fails its locked causal-specificity gate**: the no-coupling shared-drive condition produces a far larger cross-cell incremental forecast gain. Hence a positive cross-cell mean forecast score alone cannot identify cell-to-cell signaling. Amplitude parameters differ; this test is an existence counterexample, not an exchangeable effect-size comparison or a calibrated real-data benchmark. Robustness, matched signal-to-noise and alternative baselines remain to test in explicitly versioned sensitivity analyses. No positive biological discovery or external published same-task benchmark beat.
