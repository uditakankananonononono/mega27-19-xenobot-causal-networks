# PREREG AMENDMENT 02: search size 20x16 + shared random null (parent green-light 2026-09-29 11:48 IST)

Locked 2026-09-29 before ANY selection-used compute. Amends docs/DESIGN_PIVOT_PREREG.md
(SHA-256 19441cc5a97c5e4eb1a6fd4c684ffa0a043bd07a3e5abe35a0fb39e8b32ce061) and AMENDMENT_01
(SHA-256 d51e8f484955617f185e88da73c9d3fd777073c26b9bcf82f4557cbb6c17c07d). Legal under the prereg's
amendment rule. Basis: parent's green-light picking budget option (a).

CHANGES (everything else stands):
1. Population 24 -> 20. Generations 20 -> 16. 320 genomes per seed (supersedes amendment-01 sizes).
2. RANDOM NULL becomes ONE SHARED POOL of 480 valid random genomes (seed 1000 series), evaluated with the
   identical two-stage fitness, replacing amendment-01's per-seed 480-genome nulls. Justification (locked):
   per-seed nulls triple null cost (~19 CPU-h total) for no statistical gain; the shared pool is compared
   against EACH seed's GA distribution identically. A too-weak search still shows up honestly: if GA-best
   does not beat shared-null-best, H2 fails.
3. Budget accounting (locked, from pilot measurement of ~47 s/eval, F_A>0 ~50% on random genomes, rising
   under selection): GA per seed ~ 320 designs x ~1.7-2.0 evals x 47s ~ 7.1-8.4 CPU-h (8 h/seed cap +
   truncation reporting unchanged). Shared null ~ 480 x ~1.5 x 47s ~ 7.5 CPU-h under its own 8 h cap
   (truncation reported). Anchors: 4 author demo designs x 2 conditions (~6 min). Total stage 1
   ~ 29 CPU-h, ~15 h wall on 2 cores.
4. Implementation interpretations (locked): "steady-state GA" in the prereg is implemented as GENERATIONAL
   with elitism 1 (elite cloned unmutated; 19 offspring per generation by tournament size 3 with replacement
   + mutation). Invalid offspring are re-mutated from the same parent until valid (bounded 200 tries;
   on exhaustion the parent clone fills the slot and the event is logged). Generational chosen because the
   prereg specifies fixed generation counts and elitism 1, which define a generational loop.
