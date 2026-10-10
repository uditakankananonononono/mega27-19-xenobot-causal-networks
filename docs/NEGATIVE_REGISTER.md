# Fail-closed result register

Historical status *at initial preregistration only*: no outcome data had been inspected or model fitted. Subsequent entries below supersede this as a current-state summary; do not infer the project is still pre-outcome.

| Date | Test/data | Predesign gate | Result | Interpretation |
|---|---|---|---|---|
| 2026-09-26 | Source eligibility | Paired organism/time/cell modalities and independent split | Pending | No score or causal claim |
| 2026-09-26 | Prior art on naive calcium networks | Novelty beyond calcium correlation/integration | Failed for naive question | Varley 2025 already reports cellular functional network/information analysis; pivot needs new endpoint and raw data |
| 2026-09-26 | Exploratory same-study calcium checkpoint (19 dev bots, 9 unseen bots by original nonconsecutive IDs) | Other-cell mean beyond own-history ridge | No meaningful advantage: RMSE 0.50026775 vs 0.50027386, difference 0.00000610 absolute; own-history better on 5/9 heldout bots | Null for naive global cross-cell predictor; not external replication, no novel biological network, pivot and stronger controls needed |
| 2026-09-26 | Biological contrast metadata for Varley 28 bot matrices | Verified condition/stimulus assignment per bot | Not available in inspected article/supplement | Cannot turn unlabeled clusters into a new Xenobot state claim; continue source search |

## 2026-09-26: distinct epidermal organoid method arm (not Xenobot biology)
After a separate SHA-locked exploratory protocol, the protocol-deviant **pooled-RMSE** implementation showed **zero of six** organoids with the specified positive post-minus-pre incremental cross-cell mean gain. Mean paired relative-gain delta -0.00466561255, two-sided exact sign-flip p=0.03125 in the opposite direction. See `docs/ORGANOID_METHOD_CHECKPOINT.md` and `results/organoid-method-exploratory.json`. This does not falsify cellular signaling or the flagship Xenobot premise; it fails this method/predictor hypothesis in the distinct epidermal-organoid construct. Preserve it, but the later disclosed per-cell-RMSE mismatch means this is not a clean preregistered test; see the correction entry below. Do not flip the locked direction or claim a benchmark beat.

## 2026-09-26: synthetic causal-specificity gate failure
Known-ground-truth simulation in `docs/SYNTHETIC_CALIBRATION_CHECKPOINT.md`: a shared latent drive without any cell-to-cell coupling gave a much larger cross-cell forecast gain than explicit mean-field coupling. The locked synthetic discriminator's causal-specificity gate failed. This prevents interpreting forecast improvement alone as cell signaling, and reinforces rather than resolves the original Xenobot dataset limitation.

## 2026-09-26: post hoc organoid scale sensitivity
Within-cell full-series z-scoring flips the mean post-minus-pre gain to +0.016585, but only 3/6 signs are positive, p=.84375, with one outlier; the original raw sign was 0/6 positive. These z-scored scores leak full-series scale information and are a diagnostic, not prospective benchmark evidence. See `docs/ORGANOID_SCALE_SENSITIVITY.md`. Stop biological interpretation of either directional sign.

## 2026-09-26: prospective-calibration method diagnostic
Separately versioned within-recording 25% calibration window (not the original held-out task) yields 2/6 positive paired post-pre forecast-gain deltas, mean -0.029718 and two-sided exact sign-flip p=.1875. It does not rescue the failed original directional result. See `docs/ORGANOID_PROSPECTIVE_CHECKPOINT.md`; relevant open gaps remain.

## 2026-09-26: estimator correction weakens the earlier sign test
Pivot 02's original code pooled cell/frame squared errors despite the per-cell RMSE text. Post-outcome corrected aggregation yields 1/6 positive, mean -0.00737567 and two-sided p=.0625. The prior p=.03125 should never be described as a clean preregistered result. See `docs/PROTOCOL_DEVIATIONS.md` and `docs/ORGANOID_RMSE_CORRECTION_RESULT.md`. Neither estimator establishes biology or completion.

## 2026-09-26: source-equivalent TimeGraph graph-target correction
The locked two-direct-edge target in the 30-seed generator grid scores VAR(2) worse when it reports genuine *reduced-form* lag paths through contemporaneous mediators. Those are counted false positives only relative to direct structural truth. This is a model/target mismatch, not an established false-discovery rate. Post-outcome reduced-form sensitivity is labeled separately in `docs/TIMEGRAPH_GRID_02_RESULT.md`; no published benchmark comparison is valid yet.

## 2026-09-26: synthetic oracle-driver sensitivity
Giving the predictor the simulator's exact U almost eliminates no-coupling shared-drive cross-cell forecast gain (+0.035643735 without U to +0.000002345 with U), while coupling's +0.00211 remains +0.00212. This is a useful **constructed** causal-specificity diagnostic, not a positive biological finding or an available real-world confound correction. No benchmark win; source-linked Xenobot data and final paper remain open. See `docs/SYNTHETIC_OBSERVED_DRIVER_SENSITIVITY_RESULT.md`.

## 2026-09-26: real Xenobot disjoint-sensor forecast
Separate post-outcome real-matrix method robustness check `docs/REAL_CALCIUM_SENSOR_FOCAL_RESULT.md`: disjoint sensor mean gives only ~0.0015% pooled RMSE benefit over own-history on each arbitrary parity split, and both mean-per-cell aggregations favor own-history. This is a concrete, reproducible result on public processed calcium matrices, **not** cell-cell causality or movement/behavior. Prior holdout IDs were reused; no independent validation, biological discovery or published benchmark beat.

## 2026-09-27: cross-bot motion predictability in shared arenas
Locked-protocol test (protocol SHA-256 27635b2f..., commit 10a1a84) on the 12 public multi-bot track replicates: adding same-arena population features to a focal bot's own-history ridge does not improve 10-second-ahead velocity prediction on held-out bots. Median relative RMSE gain -0.00017 across replicates, 4/12 positive, exact two-sided sign-flip p=0.388; only 2/12 replicates positive and above their circular-alignment null p95, largest +0.00131 (~0.13%). Dynamical/methods result only; one condition per replicate blocks biological reading. See `docs/TRACK_CROSSBOT_RESULT.md`.

## 2026-09-29 - PIVOT 05 movie reproduction of memory-preprint Figure 6 (mostly negative)
Locked prereg e709ca53; result doc docs/PIVOT_05_MOVIE_CALCIUM_RESULT.md; per-panel stats results/pivot05/.
- ATP 24h cross-correlation decrease (paper's decohesion claim): NOT REPRODUCED (opposite direction, gain-invariant statistic, above null).
- EE 3h variance suppression below baseline: NOT REPRODUCED (3h variance ~11.5x baseline on the deposited movie; gain caveat noted).
- EE during-stimulus cross-correlation stability: NOT REPRODUCED (xcorr rises ~30-40x during stimulus).
- Baseline Xenobot<embryo cross-correlation ordering: NOT REPRODUCED on 4+2 deposited baseline panels (opposite ordering; consistent with paper's own outlier note).
- Reproduced: ATP variance trajectory (all clauses, both pixel subsets); EE 24h cohesion increase (both subsets).

## 2026-09-30: DESIGN PIVOT stage 1 (bidirectional locomotion, simulation-only)

1. H2 NOT SUPPORTED: budget-matched shared random null (480 designs) found a better
   bidirectional design (n394, F=0.01298) than any of the 3 GA seeds (bests 0.00616 / 0.00920 /
   0.00382). 16 generations of pop-20 mutation-only search added no measurable value over random
   sampling at this budget. Best overall design came from random search.
2. H3 exception: anchor Example_1 scored F=+0.00084>0 (noise-floor: 42 um net over 10 s; design
   is outside the stage-1 class - 10x10x10, 9.8% fill, fails the candidate validity check).
   Registered per prereg sec 5; weakens the "novel for this design class" claim as stated.
3. Process: custody gap - the null scene tarball archived only post-restart designs (n301+);
   pre-restart scenes n39/n266 had to be reconstructed by validated byte-identical RNG replay.
   Archive coverage must be verified against the full design index at archive time, not assumed.
4. Effect size honesty: even the best bidirectional F (0.01298 voxels ~ 0.65 mm net over 10 s)
   is ~40-430x weaker than the anchors' one-way locomotion. Bidirectional locomotion exists in
   simulation at this budget but is a marginal behavior, not a robust gait.

## Stage 2 (replication, amendment-03) - 2026-10-02
5. S2-H3 not supported: all 16 audit-passing stage-2 designs are within distance 0.27-0.33 of stage-1 GA
   designs (threshold 0.5). Fresh seeds re-found the same morphology family; no new morphologies.
   Novelty vs the 4 published anchors alone (descriptive) is 0.53-0.58.
6. Pooled best-F: stage-1 null best (0.01298) still exceeds all 6 GA bests across stage 1 and 2;
   one-sided permutation 37/84 = 0.44. Primary S2-H2 passed 6/6 against two weaker fresh nulls,
   so the GA's advantage is in hit rate (10-25% vs <1% of designs with F>0), not shown for best-F.
7. Effect size unchanged: best stage-2 F is 0.00738 voxels (~0.37 mm net over 10 s) - marginal.

## Stage 3 process item - 2026-10-07: amendment-04 init mechanism unsatisfiable (caught pre-compute)
Pre-compute smoke testing of locked amendment-04 found its rejection-sampled initialization cannot seed
the search: occupancy distance saturates for near-full-grid designs (converged family fills 342-376/448
voxels), 40 uniform-random valid genomes measured min_d 0.26-0.31 vs the locked corpus (max 0.308), so a
0.5 floor rejects ~all draws. No compute ran under amendment-04. Fixed by amendment-05 (constructive
initialization, identical for GA and null arms). Registered as a process finding: novelty floors must be
calibrated against the fill structure of the corpus before locking.

## Stage 3 (novelty-constrained search, amendment-04/05) - 2026-10-08
No registered test failed: S3-H1 supported 3/3, S3-H2 supported 6/6, S3-H3 reports real progress
(best F 0.03364 > stage-2 best 0.00738). Standing honesty items, registered without reframing:
8. Pooled best-F still not separated at 0.05: one-sided exact label permutation over 9 GA bests
   (stages 1-3) vs 5 null bests gives 177/2002 = 0.088. Better than stage 2's 0.44, and all three
   stage-3 GA bests exceed the stage-1 null best (0.01298) for the first time, but the pooled
   best-F evidence remains descriptive, not decisive. The GA's robust advantage is hit rate
   (15-50% vs 0.4-0.6% F>0), which is a registered-secondary observation, not a primary test.
9. Effect size still marginal: best stage-3 bidirectional F is 0.03364 voxels (~1.68 mm net over
   10 s), ~165x weaker than the strongest anchor's one-way locomotion (5.57).
10. Novelty floor never bound mid-run: culls 0/0 in all 5 runs. The constraint defined the search
   region (constructive init, pre-measured 6/6 and 10/10 compliant) but rejected nothing during
   the search itself. Init morphology diversity is narrow (thin peripheral-shell family, mutual
   min_d 0.02-0.05): the morphology-novelty claim is limited to that family; material/phase
   diversity was unconstrained.

## Stage 4 (init-morphology ensemble + permutation power, amendment-06) - 2026-10-08
No registered test failed: S4-H1 supported 3/3, S4-H2 supported (p = 0.01016 < 0.05), S4-H3 supported
6/6, S4-H4 supported 3/3. Standing honesty items, registered without reframing:
11. Margin is thin: S4-H2 p = 0.01016 clears 0.05 but the pooled separation leans on the stage-3/4
    seeds; the stage-1 null best (0.01298) still exceeds every stage-1/2 GA best. One heavy-tail null
    draw away from a weaker claim.
12. Stage-4 best F (0.02156) did not beat the stage-3 best (0.03364). The added seeds bought
    statistical power, not a better design. Best-F progress has stalled across stages 3-4.
13. Within-family init clustering persists: ensemble diversity is cross-family (pilot medians 0.222
    within vs 0.600 cross). Inside each family, init draws cluster; evolved finals cluster further
    per seed. Morphology exploration remains family-bound.
14. Strata init culls dominate: 27 GA init culls (all strata; seed10 7, seed11 5, seed12 15) and 483
    null init culls (481 strata + 2 core_appendage; null6000 236, null7000 247). Shell, ellipsoid and
    core_appendage almost never culled, matching the pilot yields. Offspring culls 0 in all runs -
    the floor shaped init, never evolution.
15. Effect size still marginal: best stage-4 F 0.02156 voxels (~1.08 mm net over 10 s), ~258x weaker
    than the strongest anchor's one-way locomotion (5.57).

## Stage 5 (champion-seeded effect-size intensification, amendment-07) - 2026-10-09
No registered test failed: S5-H1 supported 3/3 (expected-vacuous, as stated), S5-H2 supported
(seed20 0.15994 and seed21 0.04236 >= the 0.04205 bar), S5-H3 supported 3/3. Standing honesty
items, registered without reframing:
16. Between-seed variance is extreme under identical conditions: one seed reached 0.15994 (4.75x the
    stage-3 champion) while the other two landed at 0.04236 and 0.04152, straddling the bar by
    +/-0.0005. A single seed's lineage dominates the headline number; seed21's excess over the bar
    (0.0003) is far below the 1.25x materiality margin the bar encodes. All three seeds share the
    same two champions, so they are not independent replicates (registered in amendment-07 sec. 5).
17. seed22 missed the frozen S5-H2 bar: best 0.04152 vs 0.04205. It sat at the champion value for 21
    generations before a late surge; one generation's difference in the budget would have changed
    which side of the bar it landed on. The bar is frozen and the miss is registered as a miss.
18. The null's ceiling, not its hit rate, is what selection beat: champion-mutant nulls produced F>0
    at 49% (235/480) - higher than the GA final-pop rates (40-75%) is not the comparison that
    matters; the null best (0.03450) never approached the bar (0/480 over it). Hit-rate claims from
    stages 3-4 do not transfer to champion-seeded search.
19. Effect size still marginal in absolute terms: best stage-5 F 0.15994 voxels (~8.0 mm net over
    10 s) remains ~34.8x weaker than the strongest anchor's one-way locomotion (5.57). The gap
    narrowed ~4.7x from stage 3; it did not close.
20. Stage-5 winners are morphologically convergent: pairwise occupancy min_d 0.0000-0.0217 across
    seed20 g23_i0 (0.15994), seed21 g23_i9 (0.04236) and seed22 g23_i1 (0.04152). The 4.75x gain
    came from actuation-program search (materials/phases) on ONE shape basin, not morphology
    exploration. Any morphology-generalization claim from stage 5 is limited accordingly; the
    novelty floor kept designs away from the corpus but did not prevent convergence into a single
    post-corpus basin.

## Stage 6 (champion-seeded intensification, second round, amendment-08) - 2026-10-10
S6-H1 supported 3/3 (expected-vacuous, as stated). S6-H2 NOT SUPPORTED (first stage whose primary
registered test fails). S6-H3 NOT SUPPORTED in its registered each-seed form (2/3 comparisons pass).
Standing honesty items, registered without reframing:
21. Primary miss: no seed reached the 0.19993 bar; the three seeds clustered at 0.17000 / 0.18068 /
    0.17474 (1.06x-1.13x the stage-5 champion). A second round of the same recipe that produced
    stage 5's 4.75x jump yielded +0.010 to +0.021. The champion basin looks near-saturated for
    mutation-only search at this budget; the stage-5 outlier was not a repeatable slope.
22. The null ceiling caught up to a GA seed: null9000 best 0.17336 beats seed30's 0.17000 outright.
    In stage 5 selection beat the null ceiling on every seed; in stage 6 it does so on only two of
    three. Champion-local random mutation at equal budget is now a real competitor to selection at
    the head of the distribution (null F>0 rate also rose to 70%). The stage-5 "ceiling, not hit
    rate" framing weakened within one stage.
23. Morphological convergence again: final-pop occupancy min_d vs the stage-5 champion is
    0.0000-0.0216 across all three seeds (extends item 20). Gains came from actuation-program
    search on the same shape basin. Combined with item 21: the actuation axis itself may be
    saturating on this basin - the lane has no evidence of remaining headroom in either axis under
    the current operator.
24. Recurring discrete F values in the null: F=0.15994 (the stage-5 champion's exact value) appears
    in 10+ null9000 candidates, and 0.04236 (stage-5 second) recurs as well. These are elite-parent
    mutants whose mutations did not change locomotion (silent mutations on this metric), not
    independent discoveries; descriptive observation only, no verdict affected.
