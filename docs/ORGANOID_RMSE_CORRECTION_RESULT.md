# Post-outcome correction of per-cell RMSE aggregation

2026-09-26. Original locked Pivot 02 plan specified per-cell RMSE, but the first implementation pooled errors across cells and frames. The mismatch is disclosed in `docs/PROTOCOL_DEVIATIONS.md`; original plan hash is preserved. A separate correction plan `docs/ORGANOID_RMSE_AMENDMENT.md` was committed before computing this new score, **but after the initial outcome was known**, so corrected results remain exploratory, not new confirmatory evidence. Six organoids from primary source https://github.com/caitlingrasso/bio-connectivity/tree/0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700/data/series_raw ; different Xenopus epidermal construct, not Xenobots. See `src/organoid_percell_correction.py` and `results/organoid-percell-correction.json`.

| Organoid | Pooled estimator paired delta | Corrected mean-per-cell RMSE paired delta |
|---|---:|---:|
| 1 | -0.013599 | -0.019586 |
| 2 | -0.009053 | -0.017076 |
| 3 | -0.002165 | -0.001971 |
| 4 | -0.001505 | -0.003328 |
| 5 | -0.000039 | +0.000077 |
| 6 | -0.001632 | -0.002370 |

Corrected mean -0.007375673486; **1/6 positive**, two-sided exact sign-flip p=.0625. Prior pooled mean -0.004665612552, 0/6 positive and p=.03125 must be identified as protocol-deviant exploratory scores, not clean preregistered inference. Both are negative-direction patterns, but neither supports biological coupling or communication changes. Source-cell count mismatches, raw-scaling sensitivity, shared-input counterexample, n=6, article prior art and lack of independent replication remain. The corrected p is not a published benchmark comparison. No external validation, Xenobot discovery or finished paper follows.
