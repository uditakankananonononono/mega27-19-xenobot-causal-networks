# Post hoc scale sensitivity of the six-organoid forecasting result

This is **not** a repaired preregistration, a biological discovery, or a deployable forecast. The diagnostic was declared in `docs/ORGANOID_SENSITIVITY_PLAN.md` and pushed at commit `ad76e9bba60b58f0d22cb1d03efb660ac8a51c95` after the raw score but before the z-scored computation. Source, six-organism unit and prior-work caveats: `docs/ORGANOID_METHOD_CHECKPOINT.md`. The original raw-intensity direction remains a recorded failed positive hypothesis.

Within-cell mean/SD of every complete recording was used to z-score its own full time series. This directly allows test-future statistics into a scale transform, so the scores **cannot** be compared as operational future prediction. It diagnoses whether the earlier observation is stable to routine recording scale changes.

| Organoid | Raw paired post-pre relative gain | Full-series z-scored paired post-pre relative gain |
|---|---:|---:|
| 1 | -0.013599 | +0.000848 |
| 2 | -0.009053 | +0.182227 |
| 3 | -0.002165 | -0.047165 |
| 4 | -0.001505 | -0.044630 |
| 5 | -0.000039 | +0.010116 |
| 6 | -0.001632 | -0.001885 |

The raw mean -0.004666 with 0/6 positive contrasts with z-scored mean +0.016585, 3/6 positive and two-sided exact sign-flip p=.84375; one large positive organoid drives that mean. This strong instability means the raw score cannot support an organism-level biological interpretation. With six units, descriptive Pearson correlations between raw within-condition relative gain and cell count were -0.147 before and -0.900 after; frame-count correlations +0.378 before and +0.682 after. These are post hoc, noisy diagnostics, not independent evidence of technical causation. The planned across-cell global mean subtraction is algebraically degenerate: for a zero-sum set of residualized cells, leave-one-out mean is exactly -own-cell/(N-1), adding no independent feature beyond own-cell history. Do not fit it and present a p value as an empirical test. The article's published pre/post functional network results remain distinct from this method's unstable forecast score.
