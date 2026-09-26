# Prospective-calibration diagnostic: no stable positive response

Date 2026-09-26. Distinct post-outcome protocol `docs/PIVOT_04_CALIBRATED_PROSPECTIVE_TEST.md` was pushed as commit `d6c2be638bb33dd788ba2e991e8da36059f9c568` before these results. Public upstream: https://github.com/caitlingrasso/bio-connectivity/tree/0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700/data/series_raw ; 12 CSVs directly loaded, six pre/post organoid pairs, all finite. Source file dimensions range 53–1180 cells and 151–282 frames. This is *Xenopus epidermal organoid*, not Xenobot, data. See `src/organoid_prospective.py`, `results/organoid-prospective-calibration.json`, and tests.

An initial 25% recording window (floor, at least 20 frames) estimates cell-specific mean/SD, and only later frames are scored. Pre and post windows are separately calibrated because cell identities are not matched. Five other **pre** recordings fit the ridge coefficients; the sixth organoid's pre/post recordings are kept out of coefficient training. The tested task now includes adaptation to each held-out recording and is not a direct benchmark comparison to Pivot 02's wholly unseen raw recording.

| Organoid | Before relative gain | After relative gain | Paired after-before delta |
|---|---:|---:|---:|
| 1 | +0.003704 | +0.006159 | +0.002455 |
| 2 | -0.060875 | -0.146229 | -0.085354 |
| 3 | -0.006834 | -0.014241 | -0.007407 |
| 4 | -0.018232 | -0.003645 | +0.014586 |
| 5 | +0.002780 | -0.031157 | -0.033937 |
| 6 | +0.001180 | -0.067472 | -0.068652 |

Mean paired delta -0.02971809545, positive in 2/6 pairs, exact two-sided sign-flip p=.1875 across 64 assignments. The result neither restores the failed original positive hypothesis nor supports a new biological directional interpretation. The source paper already reports puncture-related functional information changes. Open gaps: only six independent organoids, no independent cohort or published same-task forecast comparator, known global-driver causal confound, different cell segmentation counts before/after, no selective cell intervention, no Xenobot physiological/behavior pairing, no 50-page scientific paper. Tests check calibration-window no-future leakage and six-organism result assembly but not independent software reproduction. Do not call this completed research or a benchmark beat.
