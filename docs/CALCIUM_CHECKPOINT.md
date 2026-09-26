# Exploratory same-study calcium checkpoint: negative, not a result counted toward completion

Source: official processed matrices, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12520083/supplementaryFiles ; source hashes in data manifest. Frozen script was committed at `5fdfe173b3160832bcf2bf32f298e3be584edcf1`, but the first attempt failed because the 28 source IDs are nonconsecutive: 15, 23, 25, 28 absent. Corrected the *unscored* ID partition at `2b0b203f274746085f299c25f85ad094c8a80470`: 19 development bots with numeric IDs <=20, nine heldout bots >20. First successful score is in `results/varley-exploratory-cross-bot.json`, SHA-256 `516f4d83e918a8585e0a555fb8559698e59e6587c18671b52af4076e5da3d66e`.

| Cross-bot fit (same study) | Mean bot RMSE |
|---|---:|
| Persistence | 0.51790435 |
| Own-history ridge (best simple baseline) | 0.50027386 |
| Own-history + other-cells mean ridge | 0.50026775 |

Other-cell mean's gain vs own-history is only 0.00000610 absolute (about 0.00122% relative) and wins only 4 of nine individual bots. It is not a meaningful beat, not a biological discovery, not a published method comparison, and does not support directed cell communication. This is a development-only negative on author-processed and previously analyzed data, not an independently verified external result. Do not run feature fishing on this cohort to force significance. Next: consult ChatGPT for stalled-negative redirection, seek distinct accessible biological contrast and independently valid benchmark. No final paper or 10-round judging gate satisfied.
