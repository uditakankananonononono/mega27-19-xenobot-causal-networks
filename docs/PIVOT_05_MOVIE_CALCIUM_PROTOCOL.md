# PIVOT 05 - Computational reproduction of memory-preprint Figure 6 calcium quantification from deposited movies

Status: LOCKED BEFORE OUTCOME COMPUTE (hash in docs/PIVOT_05_MOVIE_CALCIUM_PROTOCOL.sha256).
Locked: 2026-09-29 ~07:40 IST. Parent green light 2026-09-29 07:32 IST with conditions (inventory first,
5GB cap, prereg hash before outcome compute, memory-mapped processing, hashes at download).

## 1. Source and declared novelty limits

Source: Pai, Traer, Sperry, Zeng, Levin (March 2026), "Behavioral, Physiological, and
Transcriptional Mechanisms of Memory in a Synthetic Living Construct", bioRxiv
10.64898/2026.03.17.712168v1. This is a PREPRINT; its claims are the authors' findings,
not independently verified results. This pivot is a computational reproduction/audit of
the authors' published Figure 6 calcium-dynamics quantification using only their
deposited supplementary files. It is NOT new biology and NOT the flagship linked
cell-state+stimulus+behavior claim. Limits declared up front:

- The deposits are compressed time-lapse compilation movies (mp4), not raw confocal
  stacks. Compression, downsampling, overlays, and splicing may distort pixel statistics.
- The movies likely show fewer Xenobots than the paper's N (embryo extract N=5, ATP N=4);
  per-bot trajectories can only be computed for bots identifiable in the footage.
- Pixel-level analysis only; no per-cell segmentation or cell identity linkage is claimed.
- Failure to reproduce is a reportable outcome (see Section 8), not a defect to edit away.

## 2. Data (chain of custody)

All files from https://www.biorxiv.org/content/10.64898/2026.03.17.712168v1.supplementary-material
Direct curl is IP-rate-limited (HTTP 429); files were pulled through the cloud-browser page
context (read-mode lease) on 2026-09-29. Byte sizes verified by HEAD before download;
SHA-256 recorded immediately after download in data/memory-preprint-movies-manifest.json.

| File | Deposit label | Content | Bytes |
|---|---|---|---|
| media-1.xlsx | Supplementary Data 1 (712168_file03.xlsx) | quantitative data tables | 7183 |
| media-2.xlsx | Supplementary Data 2 (712168_file04.xlsx) | quantitative data tables | 9618 |
| media-20.mp4 | Supplementary Movie 18 (712168_file20.mp4) | baseline calcium dynamics (Fig 5) | 4174392 |
| media-21.mp4 | Supplementary Movie 19 (712168_file21.mp4) | embryo-extract calcium dynamics (Fig 6C-E) | 6086709 |
| media-22.mp4 | Supplementary Movie 20 (712168_file22.mp4) | ATP calcium dynamics (Fig 6F-H) | 7416671 |

Total 17,695,573 bytes (well under the 5GB pause threshold). The other 17 supplementary
files (Movies 1-17, motion/hydrodynamics) are out of scope for this pivot and were not
downloaded. Full 22-file inventory with byte sizes is in the manifest.

## 3. Authors' published pipeline (reproduction target), from the preprint Methods

1. Extract per-pixel intensity time series from each video.
2. Bandpass filter each pixel series, removing the highest and lowest 10% of frequencies
   between 0 and Nyquist.
3. Zero out fluctuations below 1% of the maximum amplitude observed in any video.
4. Per-pixel temporal variance; restrict analysis to the most active pixels
   (top 10% and top 50% by variance; Figure 5 uses the 90th percentile).
5. Summary statistics per video: median variance across the subset, and median interpixel
   cross-correlation over 100,000 randomly sampled pixel pairs from the subset.
   Cross-correlation = normalized point-wise product sum (bounded in [-1, 1]; cosine
   similarity between pixel time series).
6. Each video maps to a point in the 2D (variance, cross-correlation) state space;
   per-Xenobot trajectories connect baseline -> during-stimulus -> 3h -> 24h.

Imaging parameters (Methods): Leica Stellaris 8 confocal, 25X objective, one frame every
10 seconds; movies are time-lapse compilations of these frames.

## 4. Our pipeline (preregistered)

a. Inventory frames with ffprobe (fps, frame count, resolution) and record them.
b. Movie segmentation BEFORE any statistic is computed: each movie is inspected once and
   split into labeled segments strictly by the movie's own visible structure (panel
   boundaries, text overlays, condition labels, cuts). The segmentation table (segment id,
   frame range, visible label, mapped condition/timepoint) is committed to the repo before
   step c. ALL segments mapping to Figure 5/6 conditions are analyzed; no segment is
   excluded after statistics are seen. Preregistered artifact-exclusion criterion (applied
   blind to statistics): a segment is excluded only if frames are unreadable, contain
   full-screen title cards, or show no Xenobot tissue; exclusions are logged with reason.
c. Decode frames with ffmpeg, memory-mapped, sequential (1GB RAM sandbox). Channel rule:
   if frames are RGB, use the green channel (GCaMP6s); if grayscale, use luma. The choice
   is made once from the container metadata and first frame, recorded, and applied to all
   segments uniformly.
d. Apply authors' steps 2-5 exactly: bandpass (lowest/highest 10% of 0..Nyquist removed),
   1%-of-global-max zeroing, top-10% and top-50% variance subsets, median variance,
   median cosine cross-correlation over 100,000 pixel pairs with fixed seed 20260929.
e. State-space mapping per segment; per-bot trajectories where segments are identifiable
   as the same Xenobot across timepoints (identification only via the movie's own labels).

## 5. Comparison targets (from the preprint's published claims)

Directional primary endpoints:
- E1 (embryo extract, variance): during-stimulus > baseline; 3h < baseline.
- E2 (embryo extract, cross-correlation): no major change during stimulus; INCREASED by
  24h vs baseline (more cohesive).
- A1 (ATP, variance): during > baseline; 3h > during (further increase); 24h below the
  3h peak but still > baseline.
- A2 (ATP, cross-correlation): DECREASED by 24h vs baseline (less cohesive).
- B1 (baseline, Movie 18 / Fig 5): Xenobot baseline state-space points fall within the
  authors' reported Xenobot baseline ranges (variance 0.4-70; mean cross-correlation
  ~0.547, lower than embryo epidermis mean 0.663).

Success rule: an endpoint is REPRODUCED if its stated direction holds for a majority of
identifiable per-bot trajectories (or the single bot if only one is identifiable), under
the top-10% pixel subset, with the top-50% subset reported as a robustness check.
Secondary numeric check: where Supplementary Data xlsx or figure text gives numeric
values, reproduced medians within 0.5 dex of the authors' values count as numeric
agreement; larger deviations are reported, not tuned away.

## 6. Null models and guards

- Circular time-shift null per segment: 200 random shifts per segment; cross-correlation
  is recomputed; the null distribution is reported beside each empirical value to guard
  against autocorrelation-driven false coherence (consistent with this lane's prior
  synthetic-confound findings).
- Compression guard: per-segment mean absolute frame-to-frame pixel difference is
  reported so near-static or overlay-dominated segments are visible in the record.
- No digitizing of paper plots into substitute data. No mixing of Movie 18-20 content
  with the Varley 2025 NPZ dataset; they are different experiments and stay separate.

## 7. Compute and checkpoint discipline

- Memory-mapped frame iteration; per-segment intermediate statistics committed as JSON
  after each segment (sandbox death loses at most one segment).
- Checkpoint pushes to GitHub at each milestone (segmentation table, per-segment stats,
  final result), keeping the ~30-minute active-work push cadence.

## 8. Negative-register and deviation commitments

- If reproduction fails at any stage (movie quality, unsegmentable footage, metric
  mismatch, contradicting directions), the failure mode is registered in
  docs/NEGATIVE_REGISTER.md with evidence in the same commit series as the result.
- Any deviation from this protocol is logged in docs/PROTOCOL_DEVIATIONS.md before the
  affected results are reported.
- No outcome statistic is computed before this document's SHA-256 is locked, committed,
  pushed, and sent to the parent.
