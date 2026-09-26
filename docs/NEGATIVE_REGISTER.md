# Fail-closed result register

Status at preregistration: no outcome data inspected, no model fitted, no positive or negative scientific result.

| Date | Test/data | Predesign gate | Result | Interpretation |
|---|---|---|---|---|
| 2026-09-26 | Source eligibility | Paired organism/time/cell modalities and independent split | Pending | No score or causal claim |
| 2026-09-26 | Prior art on naive calcium networks | Novelty beyond calcium correlation/integration | Failed for naive question | Varley 2025 already reports cellular functional network/information analysis; pivot needs new endpoint and raw data |
| 2026-09-26 | Exploratory same-study calcium checkpoint (19 dev bots, 9 unseen bots by original nonconsecutive IDs) | Other-cell mean beyond own-history ridge | No meaningful advantage: RMSE 0.50026775 vs 0.50027386, difference 0.00000610 absolute; own-history better on 5/9 heldout bots | Null for naive global cross-cell predictor; not external replication, no novel biological network, pivot and stronger controls needed |
| 2026-09-26 | Biological contrast metadata for Varley 28 bot matrices | Verified condition/stimulus assignment per bot | Not available in inspected article/supplement | Cannot turn unlabeled clusters into a new Xenobot state claim; continue source search |

## 2026-09-26: distinct epidermal organoid method arm (not Xenobot biology)
After a separate SHA-locked exploratory protocol, a six-organoid pre/post-puncture calcium forecast showed **zero of six** organoids with the specified positive post-minus-pre incremental cross-cell mean gain. Mean paired relative-gain delta -0.00466561255, two-sided exact sign-flip p=0.03125 in the opposite direction. See `docs/ORGANOID_METHOD_CHECKPOINT.md` and `results/organoid-method-exploratory.json`. This does not falsify cellular signaling or the flagship Xenobot premise; it fails this method/predictor hypothesis in the distinct epidermal-organoid construct. Preserve it; do not flip the preregistered direction or claim a benchmark beat.

## 2026-09-26: synthetic causal-specificity gate failure
Known-ground-truth simulation in `docs/SYNTHETIC_CALIBRATION_CHECKPOINT.md`: a shared latent drive without any cell-to-cell coupling gave a much larger cross-cell forecast gain than explicit mean-field coupling. The locked synthetic discriminator's causal-specificity gate failed. This prevents interpreting forecast improvement alone as cell signaling, and reinforces rather than resolves the original Xenobot dataset limitation.

## 2026-09-26: post hoc organoid scale sensitivity
Within-cell full-series z-scoring flips the mean post-minus-pre gain to +0.016585, but only 3/6 signs are positive, p=.84375, with one outlier; the original raw sign was 0/6 positive. These z-scored scores leak full-series scale information and are a diagnostic, not prospective benchmark evidence. See `docs/ORGANOID_SCALE_SENSITIVITY.md`. Stop biological interpretation of either directional sign.

## 2026-09-26: prospective-calibration method diagnostic
Separately versioned within-recording 25% calibration window (not the original held-out task) yields 2/6 positive paired post-pre forecast-gain deltas, mean -0.029718 and two-sided exact sign-flip p=.1875. It does not rescue the failed original directional result. See `docs/ORGANOID_PROSPECTIVE_CHECKPOINT.md`; relevant open gaps remain.

## 2026-09-26: estimator correction weakens the earlier sign test
Pivot 02's original code pooled cell/frame squared errors despite the per-cell RMSE text. Post-outcome corrected aggregation yields 1/6 positive, mean -0.00737567 and two-sided p=.0625. The prior p=.03125 should never be described as a clean preregistered result. See `docs/PROTOCOL_DEVIATIONS.md` and `docs/ORGANOID_RMSE_CORRECTION_RESULT.md`. Neither estimator establishes biology or completion.
