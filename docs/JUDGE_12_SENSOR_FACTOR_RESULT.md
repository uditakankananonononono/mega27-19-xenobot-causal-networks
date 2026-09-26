# Judge 12 sensor-only factor test: factor does not remove shared-drive false signal

Text-paste external judge: https://chatgpt.com/c/6ab7a19a-6f48-83e8-a29c-83c273c6d1fd , response captured in `docs/JUDGE_ROUND_12_RESPONSE.txt`. Protocol SHA locked at remote main `009815ad37fc4b424ffd57b266da0c839708e472` before scores. Synthetic X matches previous generator elementwise. Disjoint 32 sensor cells and 32 focal cells, first 60 frames of each recording for sensor-PC1 centering/loading; fit on remaining 180 target frames for 16 train recordings and score 8 heldout per scenario. No heldout scoring frames enter PCA loadings; however the heldout recording's *first 60 frames do* enter calibration, so this is an adapted recording task, not a completely untouched out-of-bot score. Model A focal own-lag, B + sensor mean, C + sensor PC1, D + both, same target frames, ridge 1.

| Synthetic truth | B over A gain | C over A gain | D over C residual gain | PC1/mean correlation |
|---|---:|---:|---:|---:|
| Null g=0,h=0 | -0.00000205 | +0.00000047 | -0.00000184 | +0.12976 |
| Coupling g=.25,h=0 | +0.00194198 | +0.00025540 | +0.00167849 | +0.35617 |
| Shared drive only g=0,h=.5 | +0.03461761 | +0.02375754 | +0.01097372 | +0.99959 |

The proposed rank-one factor is **nearly the same as sensor mean under shared drive**; adding the mean after PC1 still gives a noncausal gain +0.01097. Thus it fails as an independent stronger baseline and cannot separate coupling from shared cause. In the coupling-only system, PC1's low average alignment and weaker gain may reflect per-recording component instability, not a biological contrast. ChatGPT's suggested permutation of cell labels is an algebraically invalid control for a population mean, so no such score was run. This is an implemented novelty-angle test prompted by round 12, but a **negative method finding**, not evidence of new-to-literature novelty, published benchmark beat, causal cell-cell edges or motile Xenobot biology. Original linked behavior/intervention data, factor/VAR comparison on matched tasks, external replication, and 50-page body manuscript are open.
