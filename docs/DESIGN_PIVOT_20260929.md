# DESIGN PIVOT: evolutionary design of novel xenobot morphologies in open simulation

2026-09-29. Mandate (parent relay of user's 11:07 AM instruction): "actually design xenobots" - evolutionary
design of novel xenobot morphologies/behaviors in open physics simulation (the open VoxCAD/Voxelyze lineage
the original work used, or a better free equivalent - verify what runs), candidates selected for behaviors
the literature hasn't reported, novelty measured against published designs. Honesty gates unchanged:
locked prereg before outcome compute, negative register maintained, everything labeled simulation-only/
unvalidated, heavy compute needs concrete plan + parent green-light. The PIVOT 05 audit result (ATP 24h
decohesion contradicts the authors' own deposited movie; commit 9d9bff5) stays banked as lane evidence.

**ALL RESULTS FROM THIS LANE ARE SIMULATION-ONLY AND UNVALIDATED IN WET LAB. NO CLAIM ABOUT REAL XENOBOTS.**

## 1. What actually runs (verified 2026-09-29, this sandbox)

Environment: Ubuntu 22.04, Python 3.10.12, gcc/g++ 11.4, 2 cores, 1982 MB RAM, no GPU.

| Option | What it is | Verdict |
|---|---|---|
| voxcraft (voxcraft/voxcraft-sim, Voxelyze3) | GPU voxel simulator, Hiller/Kriegman | RULED OUT: CUDA-only, install docs require nvidia GPUs; sandbox has none |
| VoxCAD GUI + evosoro (skriegman/evosoro) | Original xenobot pipeline lineage | BLOCKED AS-IS: Python 2.7 + libqt4-dev; Qt4 is not in Ubuntu 22.04 repos |
| Voxelyze physics engine (jonhiller/Voxelyze; copy inside skriegman/reconfigurable_organisms/_voxcad) | Qt-free C++ soft-body library, zlib dep | PRIMARY CANDIDATE: compiles with gcc headless; needs a small custom C++ driver (load .vxa, run N steps, emit center-of-mass trajectory + voxel positions) |
| evosorocore (davidmatthews1uvm/EvoSoroCore) | Python 3 port of evosoro (encoding, GA, networkx) | USABLE as the encoding/evolution layer on top of the headless Voxelyze driver |
| evogym (PyPI evogym 2.0.0, gymnasium + numpy<2.0) | MIT free equivalent, pip-installable, CPU | FALLBACK: works on Py3.10 but is 2D voxel physics, different lineage; weaker claim to "the simulators the original work used" |
| MuJoCo 3.14 (PyPI) | General physics, flexcomp soft bodies | VIABLE but fully custom; no xenobot precedent; kept as second fallback |

Plan: headless Voxelyze + custom C++ eval driver + evosorocore (or a minimal custom CPPN GA) as primary stack.
Sources: https://github.com/skriegman/evosoro, https://github.com/voxcraft/voxcraft-sim,
https://voxcraft.readthedocs.io/en/latest/get-started/install.html,
https://github.com/davidmatthews1uvm/EvoSoroCore,
https://github.com/skriegman/reconfigurable_organisms (Kriegman et al. 2020 PNAS pipeline, CC0).

## 2. What the literature reports (novelty baseline)

Published xenobot behaviors (the set a new behavior must NOT duplicate):
- Locomotion, linear and circular (Kriegman et al. 2020 PNAS, "scalable pipeline for designing reconfigurable organisms").
- Object/particle pushing and collective aggregation; drag reduction via holes (same).
- Kinematic self-replication: rotating C-shapes sweep loose cells into piles (Kriegman et al. 2021 PNAS).
- Xenobot 2.0: cilia-driven swimming, collective swarming, self-healing, dye-based memory reporter (Blackiston et al. 2021 Sci Robotics).
- Calcium-level sensory integration / bistable "memory" claims (Varley & Levin 2025; memory preprint 2026 - and our audit shows its own deposited movies do not verify the decohesion signature).

Novelty reference designs (published morphology corpora to measure distance against): bestSoFar .vxa designs
in skriegman/reconfigurable_organisms (CC0), PNAS 2020 supplementary design archives, PNAS 2021 replication
designs. Exact inventory + hashes at prereg time (chain-of-custody same as the movie audit).

## 3. Target behaviors (literature-unreported candidates)

Primary targets (choose at prereg; all with explicit fitness definitions):
1. **Incline climbing** - net uphill displacement on a 15-degree slope against gravity within fixed sim time. Locomotion on flat ground is reported; inclined/terrain locomotion is not.
2. **Aperture traversal** - passage of the body's centroid (and >80% of voxels) through a rigid wall aperture narrower than the design's rest width. Squeezing/gap traversal is not reported.
3. **Bidirectional locomotion** - displacement in BOTH +x and -x under two actuation phase conditions of the same design. Published designs locomote one way; reversible locomotion is not reported.
4. (backup) **Transient jump/hop** - z-displacement of the lowest voxel above a threshold. Not reported, but furthest from wet-lab plausibility; only if 1-3 stall.

Each target gets: a fitness function (defined in the locked prereg, pre-outcome), an environment spec (.vxa
scene with gravity, floor/aperture/ramp geometry, Kriegman-2020 material parameters for passive/support and
contractile "cardiac-like" voxels), and a fixed evaluation budget.

## 4. Novelty measurement (against published designs)

- **Morphological novelty**: normalized symmetric difference of 3D voxel occupancy sets, minimized over the 24
  cube rotations and integer translations, between each evolved design and every design in the published corpora
  (sec. 2). Report the distance of each candidate to its nearest published design; candidate is "novel
  morphology" iff nearest-neighbor distance >= threshold (threshold fixed in prereg, pre-outcome).
- **Behavioral novelty**: fitness vector of the candidate across a battery (flat locomotion, pushing, + the
  target task) minus the same vector for published reference designs re-evaluated headlessly in OUR engine
  (same physics, same settings). Reported only as simulation-internal comparison.
- Published designs re-evaluated in our engine also serve as **reference anchors** (sanity that our headless
  pipeline reproduces their reported qualitative behavior - flat locomotion works, holes reduce drag).

## 5. Evolution protocol (draft; becomes the locked prereg)

- Encoding: CPPN-NEAT generative encoding over a bounded voxel grid (7x7x7, matching Kriegman 2020), materials:
  passive, contractile (phase-offset actuation), support. Max actuation phases fixed.
- Search: age-fitness Pareto or simple elitist GA (fixed at prereg), population 30, 30 generations, N seeds
  (fixed at prereg, >= 5 per target behavior). All fitness used for selection computed ONLY after prereg lock.
- Nulls/baselines: (a) random search with identical evaluation budget per behavior - evolved must beat random
  on held-out re-evaluation trials (mean over >= 20 fresh-episode evals, report distribution not best);
  (b) published reference designs re-evaluated on the target tasks (expected ~0 fitness - anchors the claim
  that the behavior is new for this design class).
- Reporting: full distributions, no best-run cherry-picking; failures (targets that stall, physics artifacts,
  sim exploits) go to NEGATIVE_REGISTER.md. Any sim exploit (designs that score via physics bugs, e.g.
  interpenetration launches) is a negative-register entry, not a result.
- Compute estimate (to be measured at build): ~1-5 s wall per 5-10 s Voxelyze eval on these 2 cores at xenobot
  scale (<1k voxels); pop 30 x 30 gens = 900 evals ~ 15-90 min per seed per behavior; 5 seeds x 3 behaviors ~
  2-23 h total. HEAVY RUN - needs parent green-light before the first selection-used evaluation.
- Prereg: separate doc (docs/DESIGN_PIVOT_PREREG.md), SHA-256 reported to parent before any selection-used
  fitness evaluation, per lane rules. Amendments allowed only if locked before outcomes.

## 6. Immediate bounded steps (no heavy compute, within mandate "verify what runs")

1. THIS DOC - committed, reported to parent. (now)
2. Build verification (bounded, ~10-20 min, repo downloads are MBs): compile Voxelyze headless from
   reconfigurable_organisms/_voxcad, write minimal driver, run ONE sanity eval of a published bestSoFar design
   and one random design; record wall time per eval. No evolution, no selection-used compute.
3. Report build outcome + measured per-eval cost + the concrete heavy-run plan (behaviors, seeds, budget,
   duration) to parent; prereg locked and hashed BEFORE the heavy run, per gate.

## 7. Risks and honesty notes

- Sim exploits are the main failure mode of voxel evolution; mitigation = exploit checklist in prereg
  (interpenetration, floor-clipping, energy injection via actuation limits) + visual/trajectory audit of any
  high-fitness design before it counts as a candidate.
- 2GB RAM: Voxelyze at xenobot scale is small; driver will stream state, checkpoint per-generation populations
  to disk so a sandbox wipe loses <1 generation. Git checkpoints continue every 30 min during active work.
- No wet-lab claims, no public posts, no judge-verdict self-runs - per standing lane rules.
