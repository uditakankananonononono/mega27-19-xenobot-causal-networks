# Oracle observed-driver sensitivity, a synthetic diagnostic only

Protocol SHA-locked and remote-pushed at `0ea2b21298a95bf5cdbf065759d80bff1d666b43` **before** scores. Same generative X series as Pivot 03, verified elementwise for every replicate and condition; `src/observed_driver_sensitivity.py`, `results/synthetic-observed-driver-sensitivity.json` and tests reproduce it. The model now observes the simulator's true U(t), which is not a known variable in real Xenobots or epidermal organoids. Training 16 independent replicates, scoring eight per scenario, 64 cells and 240 frames each. Per-replicate heldout RMSE relative gain is (own+oracle-U error - own+oracle-U+population-mean error) / own+oracle-U error. No model selection or threshold tuned after results.

| Synthetic ground truth | Old gain, U omitted | New gain, U observed | Fitted U coefficient with population | Fitted other-cell-mean coefficient |
|---|---:|---:|---:|---:|
| Independent null g=0,h=0 | -0.000000912 | -0.000001430 | 0.001827 | -0.011116 |
| Coupling g=.25,h=0 | +0.002109689 | +0.002123141 | -0.001014 | +0.252653 |
| Shared drive only g=0,h=.5 | +0.035643735 | +0.000002345 | +0.499644 | +0.000526 |

An oracle driver nearly eliminates the large non-causal population forecast gain in this exact toy equation; the direct mean-field coupling scenario retains its modest gain. This demonstrates how a **measured** common cause can help separate mechanisms in a constructed system. It cannot show real recordings have such a measured covariate or that conditioning on an estimated factor fixes confounding. Shared-drive amplitude and coupling amplitude remain unequal, training is pooled over many simulated cells, and the sensitivity was conceived after the initial outcome. It does not establish a Xenobot biological result, a robust confound-aware causal discovery method, a published benchmark beat, or scientific completion. Next honest stress test would require predeclared imperfect observable proxy measurements and alternative common causes, matched task baselines, and independent biological validation.
