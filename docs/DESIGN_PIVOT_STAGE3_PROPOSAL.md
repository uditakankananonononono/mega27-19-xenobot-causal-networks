# DESIGN PIVOT - STAGE 3 PROPOSAL (DRAFT FOR REVIEW - NOT LOCKED, NO COMPUTE RUN)

Drafted 2026-10-07 IST by the lane in response to the parent's no-idle-lanes directive. This is a scoping
proposal for the user/parent, NOT a preregistration amendment. No stage-3 compute has run and no outcome
data beyond the already-reported stage-1/stage-2 results was inspected to write it. If the user picks an
option, it is rewritten as AMENDMENT_04, SHA-256 locked, and reported to the parent BEFORE any compute.
SIMULATION-ONLY scope is unchanged.

## Evidence base (already reported; no new analysis)
- Stage 1: H1 supported (bidirectional F > 0 exists), H2 not supported (shared-null best 0.01298 beat all
  3 GA bests), H3 exception registered (one out-of-class anchor at noise floor), H4 novelty held vs the
  4 published anchors. Best effects ~40-430x weaker than one-way anchor locomotion.
- Stage 2 (amendment-03): S2-H1 supported 3/3, S2-H2 supported 6/6 vs two fresh nulls, pooled best-F
  permutation 37/84 = 0.44 (GA not separated from random on best-F; GA advantage is hit rate 10-25% vs
  <1%), S2-H3 NOT supported: fresh GA seeds re-converged on the stage-1 morphology family (min occupancy
  distance 0.27-0.33 vs stage-1 candidates; 0.53-0.58 vs the published anchors alone).

## Circularity warning (load-bearing)
The cheap next move - more seeds, more generations, same space, same fitness - is the loop that already
produced the S2-H3 negative. Convergence of fresh seeds on one morphology family is evidence about the
SEARCH SPACE + FITNESS LANDSCAPE, not about seed luck. Any stage 3 that does not change the space, the
initialization, the selection pressure, or the behavior target is expected to re-register the same
negative and should not be run.

## Option A: novelty-constrained search (recommended)
Change the selection pressure, not just the seeds.
- Initialization: random valid genomes FILTERED to min occupancy distance >= 0.5 vs the full prior corpus
  (4 anchors + 7 stage-1 + 16 stage-2 audit-passing designs, 27 total, listed by hash). Rejection-sampled,
  count reported.
- Selection: tournament as before, but any child with min_d < 0.5 vs the corpus is culled and regenerated
  (same validity-regenerate rule as prereg sec 3). Fitness, audit (sec 7) and novelty metric unchanged.
- Null: budget-matched random pool drawn from the SAME filtered initialization distribution.
- Registered tests (draft):
  - S3-H1: >= 1 audit-passing design with F > 0 and min_d >= 0.5 vs the 27-design corpus per seed (3 seeds).
  - S3-H2 (primary): per-seed best F among S3-H1 designs beats the best of the matched filtered null.
  - S3-H3 (registered failure check): if S3-H1 passes but best F <= stage-2 best (0.00738), register that
    novelty was bought at zero fitness progress.
- Budget: same caps as amendment-02/03 (~39 CPU-h, 8 h per-seed cap, truncation reported).
- Risk registered up front: the occupancy metric ignores materials, so d >= 0.5 requires genuine body-plan
  change; the floor cannot be gamed by material flips. It CAN be gamed by stray-voxel appendages; the
  connectedness and 50%-fill validity rules bound this, and material-composition differences are reported
  descriptively as before.

## Option B: registered stop-rule (no new search)
Lock the decision criterion instead of running more search: declare the 8x8x7 / min(F_A,-F_B) /
flat-ground lane exhausted at this budget class, archive the corpus + code, and register the final
negative in NEGATIVE_REGISTER.md. Costs no compute. Appropriate if the marginal effect sizes
(0.37-0.65 mm net over 10 s, ~40-430x below one-way anchor locomotion) are judged not worth pushing.

## Option C: new behavior target (needs explicit user direction)
New objective/fitness (e.g., slope, turning, pushing) was deliberately excluded from stage 2
("no new objective, no new fitness"). Picking a new target is a user decision, not a lane decision; if
chosen, it is a fresh preregistration, not amendment-04.

## Decision needed from the user
One of: A (novelty-constrained search), B (stop-rule), C (new target - name it), or redirect entirely.
Until then: no stage-3 compute. The deposit watch continues independently.
