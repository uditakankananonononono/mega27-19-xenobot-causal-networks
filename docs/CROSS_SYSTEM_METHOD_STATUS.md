# Cross-system methods arm: current status and interpretation

Updated 2026-09-26 by direct result JSON and code review. This is separate *Xenopus epidermal organoid* data, not motile Xenobots. Primary source and paper: https://github.com/caitlingrasso/bio-connectivity/tree/0581ec7b63b30fb09d70b9d34d8cbbf88e6c4700/data/series_raw ; https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012149 . The six organoids are the paired units; pre/post matrices have different cell counts, no cell-to-cell identity match. Article already analyzes functional and information-network change after puncture.

| Test | What was actually run | Result | Inference boundary |
|---|---|---|---|
| Pivot 02 locked method, but implementation deviated | pooled squared error across cells and frames instead of locked per-cell RMSE | 0/6 positive, mean paired gain -0.00466561, exact two-sided p=.03125 | *Protocol-deviant exploratory*, not clean preregistered; no biological inference |
| Per-cell RMSE correction | post-outcome separately versioned correction | 1/6 positive, mean -0.00737567, p=.0625 | Exploratory after original outcome; no biological inference |
| Full-series z-score | post hoc sensitivity using future scale | 3/6 positive, mean +0.01658492, p=.84375 | Retrospective diagnostic only; not prospective forecast |
| 25% initial-window scaler | new within-recording adaptation/transfer task | 2/6 positive, mean -0.02971810, p=.1875 | Different task, not a clean comparison to Pivot 02 |
| Synthetic counterexample | known simulated shared latent driver without cross-cell coupling | cross-cell gain +0.03564 vs explicit coupling +0.00211 in one toy setting | Demonstrates one noncausal failure mode; not calibrated biological benchmark |

Every numerical line is traceable to a JSON file under `results/`, source in `src/` and the named protocol/deviation docs. The direction and p values do not imply injury reduces cellular communication. A shared driver can generate cross-cell prediction, and score direction is preprocessing-dependent. Distinct method deliverables exist, but no published same-task model benchmark has been beaten, no organism-level biological discovery established, and no external biological validation performed. The original Xenobot causal/memory/behavior project remains active and needs verified linked data. No 50-page final paper has been drafted. Ten separate ChatGPT critique rounds are logged; that is process progress only.
