# Model design and falsifiers (no model fitted)

## Units and admissible observations
A cellular node is a segmented cell with an organism identifier, frame/time, spatial calibration and tracking lineage. A whole-bot centroid is one organism-level observation, never a cell node. Temporal edges connect identified cells to themselves across frames; spatial edges require measured contacts or distance under preregistered physical radius, never learned solely to maximize the behavioral outcome. Edge types distinguish physical contact, inferred adjacency, putative signaling and measured functional coupling; the last two must not be mislabeled as causal connections.

Each modality has a `measured/missing/not-applicable` mask. Cell expression from pooled Xenobots, embryo atlases and a different cohort must not be broadcast onto tracked individual cells. Calcium-imaging intensity is a physiological proxy, not a direct voltage reading without calibrated sensor evidence. Ciliary motion, local flow, stiffness and forces are distinct. Source-to-source transfer can generate candidate priors only; validation requires matched organism experiments.

## Benchmark stages
1. Release a source manifest with hashes, license, biological unit, intervention metadata and raw/derived provenance. Recover cell positions/times and verify identity switches and missing-frame rates without consulting behavior labels.
2. Freeze a held-out independent experiment within each condition; split entire organisms before making windows. If no such independent experiment exists, restrict to descriptive analysis, document that the prediction gate cannot be tested.
3. Baselines: zero motion, last displacement/persistence, shape/cell count if measured, pooled-state temporal model. Equal temporal histories and training budgets.
4. Temporal graph model only if enough independent organisms, linked cell measurements and plausible edges exist. Evaluate organism-level error and independent-organism confidence intervals. Compare against shuffled graph, degree-preserving spatial rewiring, time-reversal and modality-mask controls. A shuffled graph beating the proposed graph is a clear negative.
5. Any ablation is a sensitivity analysis of the fitted predictor, with equivalently accurate models and out-of-support checks. A model's 'minimal' subgraph is non-identifiable if multiple distinct graphs fit equally well. Report the equivalence class instead of a single discovered mechanism.
6. Information localization is an explicit contest between best single-cell, local-neighborhood and whole-network representations on independent held-out organisms, calibrated against label-shuffling and finite-sample bias. Prediction improvement does not imply emergent intelligence.
7. Memory requires controlled exposure and washout, baseline matching, animal-level analysis, time trends and a no-stimulus comparator. Genuine predictive response requires a manipulated cue with a separated future event rather than a post-hoc video pattern. All hypotheses need separate experimental confirmation.
8. Architecture evolution is a computational proposal generator: freeze simulator parameters first, keep search budget equal to random/greedy/novelty controls and avoid equating simulator reward with replication in living constructs.

## Known source bottlenecks
The 12-track original behavior dataset has one numbered replicate per condition; no same-condition independent experiment is identified, and tracks are whole-organism. The memory preprint describes spatial calcium, but public raw matching data were not yet verified. The existing RNA data are bulk/pooled, and the embryonic scRNA reference is not longitudinal Xenobot expression. Therefore stages 2-8 are presently gated, not scored.
