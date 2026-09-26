# External-source TimeGraph generator grid: conditioning beats pairwise lag links

2026-09-26. **Methods-only, synthetic, not Xenobot biology or published benchmark victory.** Protocol `docs/TIMEGRAPH_GRID_02_PROTOCOL.md` was SHA-locked at remote commit `76305e6e475ea7a780524d31b40305697bd3d582` before scores. Upstream KDD 2025 paper https://arxiv.org/html/2506.01361v1 ; generator code https://github.com/hferdous/TimeGraph/tree/4d93403b002664fa55607f308ad0e80623472ded/Codes . Source-equivalent local generator first matched upstream downloaded seed-42 A1/A1C public CSVs within 1e-12 (observed X and hidden U), using the exact draw order, then produced 30 matched independent seeds 1000–1029 per condition. U is deliberately withheld from both estimators. No raw upstream data are included in the repository. The truth target comprises only two visible X→X positive-lag links among 32 directed lag-1/2 slots; contemporaneous links and U links excluded. This differs from paper Table 2's graph protocol, so do not compare numbers to its FGES/PC/PCMCI+/LPCMCI scores.

Mean over 30 independent generated realizations per condition (full per-seed metrics in `results/timegraph-grid-02.json`):

| Condition / estimator | True positive of 2 | False positive | TPR | FDR | Slot Hamming |
|---|---:|---:|---:|---:|---:|
| A1 VAR(2), Bonferroni | 1.967 | 0.467 | 0.983 | 0.144 | 0.500 |
| A1 pairwise conditional own-lag | 1.967 | 0.733 | 0.983 | 0.217 | 0.767 |
| A1C U-hidden VAR(2), Bonferroni | 2.000 | 0.400 | 1.000 | 0.128 | 0.400 |
| A1C U-hidden pairwise conditional own-lag | 2.000 | 0.867 | 1.000 | 0.229 | 0.867 |
| Zero-edge reference | 0 | 0 | 0 | 0 | 2.000 |

The pairwise method has greater mean false positives and slot Hamming than VAR(2) under both source-equivalent settings; mean paired Hamming difference pairwise minus VAR is +0.267 on A1 and +0.467 on A1C. This is a negative result for an unconditioned pairwise strategy, not a new algorithm beating a benchmark. A1C's lower mean VAR Hamming than A1 does not mean latent confounding improves inference: one simple generator, only two visible positive-lag truth links, contemporaneous-path exclusions and chosen 30 seeds constrain interpretation. There is no biological discovery from synthetic data. The target does not align with TimeGraph Table 2, whose exact U inclusion, lag-zero graph conventions, threshold and published execution code remain unresolved. Need a valid matched published comparator and independent biological test before any benchmark/discovery claim. The original motile Xenobot data linkage and the 50-page paper requirement remain open. No author outreach was sent.
