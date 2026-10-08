# Design Pivot - Stage 5 Proposal (NOT locked; for user decision via parent)

Status: PROPOSAL ONLY. No stage-5 compute has run and none will run without a locked amendment
approved through the parent. Stage 4 closed per amendment-06 termination (commit dee88bd).

## Where the lane stands (all simulation-only)
- Evolution separates from budget-matched random search on best bidirectional design for the
  first time: exact pooled permutation p = 0.01016 over 12 seeds vs 7 null pools (S4-H2).
- Hit rate is the GA's largest advantage: 35-50% of final populations vs 0.4-1.0% of random draws.
- Init morphology diversity is fixed across families (medians 0.48-0.50 vs stage-3's 0.02-0.05).
- The open problem is no longer search vs random. It is that the best behavior is weak:
  best bidirectional F = 0.03364 (~1.68 mm net over 10 s), ~165-258x below published one-way
  anchors. Best-F progress stalled across stages 3-4 (0.03364 -> 0.02156).

## Options, with honest expected value

### Option A - Attack effect size (recommended)
New registered objective rewarding displacement magnitude per direction (e.g., F' = min over
conditions of net displacement, or a shaped sum), seeded from the stage-3/4 champions
(0.03364, 0.02156 designs as registered starting material) plus fresh ensemble inits, with
frozen seed/null counts sized to the compute envelope and the same audit/custody chain.
- EV: highest. A robust bidirectional gait is the lane's first claim-worthy positive; every
  stage so far has converged at marginal magnitudes under the current objective, which only
  requires ANY net motion per direction. Stage-1's registered next-experiment #2 is exactly this.
- Cost/risk: comparable compute per design (same sim window); main risk is a registered null -
  the magnitude landscape may be barren for the 8x8x7/224-voxel class. That outcome is itself
  informative (it would motivate Option C) but adds to the negative tally.

### Option B - Attack within-family init diversity
New families, morphology-level mutation operators, within-family diversity floors.
- EV: low. Cross-family diversity already passes its floor 3/3 + 2/2; within-family clustering
  (0.222 vs 0.600) is a registered residual, but there is no evidence it caps fitness - the
  stall is in magnitude, not in diversity of what is found. This polishes a constraint instead
  of attacking the binding limitation.

### Option C - Pivot the question
Leave bidirectional locomotion: e.g., corpus growth + external benchmarking against published
evolved designs, or a different unreported behavior class on the same engine.
- EV: medium, and premature. Pivoting is the right move IF Option A returns a registered null
  showing the magnitude ceiling is a property of the design class. Buying that information
  directly (Option A) is cheaper than pivoting on a guess.

## Recommendation
Option A, one frozen stage: new magnitude-rewarding objective, champions-seeded + ensemble
starts, frozen counts, full audit and custody, explicit registered fallback to Option C on a
null. If approved, the amendment is drafted and locked before any compute, as usual.

## What this does NOT request
No new seeds under the old objective (power is bought; more of it answers nothing), no
wet-lab claims, no compute beyond the free envelope.
