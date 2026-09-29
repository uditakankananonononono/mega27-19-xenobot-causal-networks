# Source-availability recheck (2026-09-27, afternoon)

Scope: re-verify, after the previous task agent's interruption, whether any new public
deposits change the source-gated status in SOURCE_AUDIT.md and STATUS_GATES_20260927.md.
This is a descriptive availability audit only; no outcome data were inspected and no
model was run, so no new preregistration was required. 16/16 unittest tests pass at
commit a9444b2 before this note.

## March 2026 memory preprint (doi:10.64898/2026.03.17.712168)
- Supplementary-material listing re-fetched from bioRxiv: the complete supplement set is
  2 xlsx (Supplementary Data 1-2) and 20 mp4 movies (Supplementary Movies 1-20). There is
  no raw calcium-movie archive, no per-organism numeric calcium series, and no behavior
  track data file among the deposits.
- GEO GSE320387 re-verified via seqout/GEO FTP index: 15 pooled bulk RNA-seq samples
  (50 Xenobots per sample; Ctrl, Ext-0h, Ext-4h, ATP-0h, ATP-4h x3), series last updated
  2026-03-28. No imaging data.
- Published-version check (web search + Tufts faculty publications page, fetched
  2026-09-27): still listed as a bioRxiv preprint only. No journal version with
  additional deposits found.
- Conclusion: NEXT_STEPS item 1 stays resolved as NOT publicly deposited. The
  same-organism pre/during/3h/24h calcium-plus-stimulus structure exists only as
  figure-level reporting and representative mp4s; the linked cell-state/stimulus/behavior
  claim remains untestable on public data. Do not invent linked records.

## June 2026 purinergic preprint (doi:10.64898/2026.06.04.730190)
- Its own data-availability statement (previously retrieved PDF, see SOURCE_AUDIT.md)
  promises calcium CSVs "upon final publication". Rechecked 2026-09-27: no journal
  version found (web search, EuropePMC PPR1249079 still preprint-only, no accession
  cross-references), and bioRxiv still shows no supplementary CSV deposit. HTML full-text
  endpoint timed out again on recheck; the earlier PDF read stands.
- Conclusion: promised pre/post-ATP per-cell calcium CSVs are still NOT public. Do not
  treat a promised future deposit as available. This preprint remains strong prior art,
  not a benchmark substrate.

## Standing implication
The data-gated status is unchanged: no public same-individual cell-state + stimulus +
behavior linkage exists for basal Xenobots as of 2026-09-27 ~15:50 IST. The honest
routes remain (a) watch for the purinergic CSV deposit and any journal versions,
(b) the author data-access request in DATA_ACCESS_REQUEST_DRAFT.md (user-approved
sending still required), (c) methods work on already-audited public matrices within
declared novelty limits.

## 2026-09-29 09:12 IST deposit-watch recheck (false positive)
- bioRxiv details API: purinergic preprint (10.64898/2026.06.04.730190) still version 1 "new results" only; memory preprint (10.64898/2026.03.17.712168) still version 1 only. No journal version, no new supplementary deposit.
- Crossref works record for 10.64898/2026.06.04.730190: relation = {} (empty), subtype still preprint.
- Promised per-cell calcium CSVs (purinergic) remain unavailable; no new GEO/imaging accession found. Linked cell-state+stimulus+behavior gate UNCHANGED (still unmet).
