# DESIGN PIVOT: build verification (bounded, no evolution run)

2026-09-29. Verifies the "what runs" claims of docs/DESIGN_PIVOT_20260929.md on this sandbox
(Ubuntu 22.04, gcc 11.4, 2 cores, 2GB RAM, no GPU). No selection-used fitness compute was performed.

## What was built
- Cloned skriegman/reconfigurable_organisms (CC0, Kriegman 2020 PNAS pipeline), shallow, 55 MB, to
  /home/sandbox/deps/ (sandbox-local dependency, not vendored into this repo).
- Compiled _voxcad/Voxelyze (libvoxelyze.0.9, Qt-free C++) - clean build, no patches, no Qt needed.
- Compiled _voxcad/voxelyzeMain (headless CLI driver: `voxelyze -f <design.vxa> -of <out> [-p]`) - clean build.
- Output: per-design fitness XML (voxel count, normAbsoluteDisplacement, forward-model error) + with -p a
  center-of-mass trajectory time series (basis for custom behavior fitness: ramp climbing, aperture, bidirectional).

## Measured sanity evals (shipped example designs, 1.0 s sim time each)
| Design | Voxels | Wall time | normAbsoluteDisplacement |
|---|---|---|---|
| Example_withPhaseOffset | 79 | ~1 s | 56.14 (strong locomotion) |
| Example_1 | 98 | ~15-20 s (-p verbose) | 0.075 (barely moves - non-locomotor demo) |
| Example_3 | 642 | 29 s (quiet) | 53.59 |

Cost scales with voxel count. Xenobot-scale designs (7x7x7 grid, ~100-200 voxels): ~1-5 s wall per 1 s sim;
a Kriegman-style 5 s eval ~ 5-25 s. Phase-offset actuation (needed for bidirectional target) works.

## Corrections to the design doc estimate
Doc said "~1-5 s wall per 5-10 s eval": too optimistic for large designs but roughly right at xenobot scale.
Revised: ~5-25 s per 5 s eval at 100-343 voxels. pop 30 x 30 gens = 900 evals ~ 1.5-6 h per seed (one core).
Anti-DoS note: evolution can generate dense 343-voxel designs (slowest case ~30-60 s/eval); budget planning
uses the slow case.

## Gaps found
- Published bestSoFar .vxa corpora are NOT inside the repo (only demo .vxa). Novelty reference designs must be
  fetched from the PNAS 2020/2021 supplements at prereg time (chain-of-custody hashes, same as movie audit).
- Ramp/aperture environments need custom .vxa scene construction (fixed-material geometry) - part of prereg build.
- Fitness for the target behaviors = CM-trajectory parsing wrapper (driver already emits CM time series with -p).

## Conclusion
PRIMARY STACK CONFIRMED RUNNABLE: headless Voxelyze + voxelyzeMain driver, xenobot-relevant scale, sane physics
outputs. Ready for prereg lock; heavy evolution runs remain gated on parent green-light.
