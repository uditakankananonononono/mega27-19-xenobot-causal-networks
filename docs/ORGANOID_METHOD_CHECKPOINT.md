# Epidermal organoid cross-system method checkpoint: directional pattern negative, implementation deviation

Date: 2026-09-26. **Different biological system from Xenobots**: six punctured *Xenopus* epidermal organoids. Upstream source and 12 public raw processed CSVs: https://github.com/caitlingrasso/bio-connectivity/tree/0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700/data/series_raw . Prior art: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012149 . Exploratory method protocol `docs/PIVOT_02_ORGANOID_METHOD.md`, SHA-256 `3797a025cb65753510760a23712641d7402bfb4a7be48c80aae5640e5f8ddc1` locked before scores; this **does not** supersede original Xenobot preregistration.

Leave-one-organoid-out training on the five other **pre-puncture** matrices. Tested frozen own-history ridge vs own-history+other-cell-mean ridge on pre and post recordings of each held-out organoid. Same coefficients on both held-out conditions; each matrix comprises cells x frames, with different cell counts before and after, so there is no cell-level pre/post matching. Paired delta is post minus pre relative RMSE gain from adding the cross-cell mean. From `results/organoid-method-exploratory.json`:

| Organoid | Pre relative gain | Post relative gain | Paired delta |
|---|---:|---:|---:|
| 1 | -0.000058 | -0.013657 | -0.013599 |
| 2 | +0.003537 | -0.005516 | -0.009053 |
| 3 | +0.001254 | -0.000911 | -0.002165 |
| 4 | +0.001318 | -0.000187 | -0.001505 |
| 5 | +0.000583 | +0.000544 | -0.000039 |
| 6 | +0.000372 | -0.001260 | -0.001632 |

Mean paired delta -0.00466561255; 0/6 positive; two-sided exact sign-flip p=0.03125 across 64 sign assignments. Under the protocol-deviant pooled-RMSE estimator, this gives a negative directional pattern, **opposite the locked positive hypothesis**; it is not proof that tissue cells lose coordination, since changed calcium magnitude, global wound response, recording quality/length, cell composition and model misspecification can all affect RMSE. The published article already reports perturbation-related functional-information changes. The raw intensities were not independently calibrated for photobleaching or cross-recording scale. No published same-task forecasting comparator, no external cohort replication, no causal cellular inference and no new biological discovery. Code's circular-shifted-population control is scored and retained per organoid; no claim is made from it. A future revised study must be versioned as a *new* question, not reverse the sign of this locked hypothesis after seeing its failure.

**Protocol deviation notice (2026-09-26):** `src/organoid_method.py` uses pooled per-recording RMSE over all cells/frames, whereas the frozen protocol specified per-cell RMSE before organoid-level aggregation. The numerical 0/6 pattern is exploratory, not a clean confirmatory preregistered test. See `docs/PROTOCOL_DEVIATIONS.md`; original locked protocol remains unchanged.

The subsequent per-cell aggregation correction (`docs/ORGANOID_RMSE_CORRECTION_RESULT.md`) gives 1/6 positive, mean -0.007376 and p=.0625. It was computed after the first outcome, so neither version is clean confirmatory evidence.
