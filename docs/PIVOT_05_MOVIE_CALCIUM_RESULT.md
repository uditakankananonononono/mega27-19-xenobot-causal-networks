# PIVOT 05 RESULT - Movie-based reproduction of memory-preprint Figure 6 calcium quantification

Locked protocol: docs/PIVOT_05_MOVIE_CALCIUM_PROTOCOL.md (SHA-256
e709ca53503fa3abccbbaeca72b02cf573357815fca4e7c62c09cb4a46d31434), locked 2026-09-29 07:38 IST
before any outcome compute. Pipeline: analysis/pivot05_pipeline.py; blind segmentation:
data/movie-segmentation.json; per-panel statistics: results/pivot05/*.json.
Date of result: 2026-09-29 ~11:00 IST.

## Data actually analyzed

Supplementary Movies 18-20 + Data 1-2 of bioRxiv 10.64898/2026.03.17.712168v1
(custody hashes in data/memory-preprint-movies-manifest.json). 14 panels:
Movie 18 = 6 baseline panels (4 Xenobots, 2 age-matched embryo epidermises);
Movies 19/20 = 4-panel trajectories (Before/During/3h/24h) for ONE representative Xenobot
each (embryo extract / ATP). Supp Data xlsx contain NO calcium quantification values
(media-1 = stimulus list; media-2 = RNA-seq DE tables), so numeric comparison targets are
limited to values stated in the paper text.

## Deviations and implementation notes (none alter the locked protocol)

- Frame extraction: movies use mixed compilation cadences (held frames with cross-fade
  transitions on some panels, continuous updates on others). A blind plateau-dedupe rule
  (2-means on log frame-diffs; panels with <20% plateau frames kept whole) recovered the
  unique imaging frames per panel; modes and thresholds are recorded per panel in
  results/pivot05/*.json (dedup_mode fields).
- Null models use 25,000 pairs x 200 circular shifts (prereg fixed 100k pairs for the
  empirical statistic only); null pair count recorded in each JSON.
- A_MAX (1% threshold reference) computed across all 14 panels, matching the authors'
  "maximum observed amplitude in any video" phrasing applied to the deposited set.
- ffmpeg select-filter sampling proved unreliable (passed 2/3 of frames); decoding is
  full-range with numpy-side dedupe. No deviation log entry required (implementation, not
  design), recorded here for transparency.

## Trajectories (median variance / median cosine xcorr; top10 primary, top50 robustness)

Movie 19, embryo extract (N=1 bot):
  var:   53.3 -> 1219.5 (during) -> 615.0 (3h) -> 305.2 (24h)   [top10]
  xcorr: 0.004 -> 0.179 (during) -> -0.001 (3h) -> 0.060 (24h)  [top10]
         0.007 -> 0.155 -> -0.002 -> 0.256                      [top50]
Movie 20, ATP (N=1 bot):
  var:   79.0 -> 1024.7 (during) -> 2462.6 (3h) -> 483.4 (24h)  [top10]
  xcorr: 0.004 -> 0.063 (during) -> -0.005 (3h) -> 0.011 (24h)  [top10]
         0.000 -> 0.046 -> -0.005 -> 0.016                      [top50]
Movie 18 baselines (top10 xcorr): Xenobots 0.860, 0.006, 0.036, 0.175; embryos 0.021, -0.047.
Circular-shift nulls: all null medians within +/-0.005 (std <= 0.001), so xenobot_i's
0.86-0.92 synchrony is far above the autocorrelation null (real coherence, not a
held-frame artifact); all near-zero values are null-consistent.

## Endpoint verdicts (success rule from locked Section 5)

- A1 (ATP variance trajectory: during>base, 3h>during, 24h below peak but >base):
  REPRODUCED, both subsets, all three clauses. Caveat below on variance gain-sensitivity.
- A2 (ATP cross-correlation DECREASED at 24h vs baseline): NOT REPRODUCED. 24h xcorr is
  slightly ABOVE baseline (0.011 vs 0.004 top10; 0.016 vs 0.000 top50), opposite direction
  to the paper's "all four Xenobots showed a substantial decrease". Absolute values are
  small but above null. Cross-correlation is gain-invariant, so this contradiction is robust
  to compilation artifacts. Single-bot caveat applies.
- E1 (EE variance: during>base; 3h<base): NOT REPRODUCED. During>base holds (23x); but 3h
  variance is ~11.5x baseline (615.0 vs 53.3), contradicting the paper's "fluctuations
  became noticeably smaller than baseline" at 3h. Gain caveat below applies to this clause.
- E2 (EE cross-correlation: no major change during; INCREASED at 24h): PARTIAL. The 24h
  increase reproduces strongly (0.060 vs 0.004 top10, 0.256 vs 0.007 top50; both >> null).
  The "no major change during stimulus" clause is contradicted: xcorr rises ~30-40x during
  stimulus in our pipeline.
- B1 (baseline state-space ranges and Xenobot<embryo cross-correlation ordering):
  NOT REPRODUCED. Our 4 baseline Xenobots: xcorr 0.006-0.860 (mean 0.27); 2 embryos:
  0.021, -0.047 (mean -0.01) - ordering OPPOSITE to the paper's Xenobot-mean 0.547 <
  embryo-mean 0.663 across their N=30/N=22. Our high-xcorr Xenobot outlier matches the
  paper's own note of rare high-correlation Xenobot outliers. Variance values are NOT
  unit-comparable to the paper's 0.4-70 range (compressed 8-bit movie pixels vs raw confocal
  intensities); prereg's 0.5-dex numeric check is inapplicable here.

## Methodological caveats (honest limits of this reproduction)

1. N=1 representative bot per stimulus trajectory vs paper N=5 (EE) / N=4 (ATP); the
   movies show only the figure bots. Baseline comparison is 4 Xenobots + 2 embryos vs
   paper N=30/N=22.
2. Variance endpoints are sensitive to per-panel gain/brightness in the compiled movies
   (GCaMP brightness is itself signal, but h264 compilation may rescale panels
   differently). Cross-correlation (cosine) is gain-invariant: A2, E2, B1 verdicts rest on
   the robust statistic; A1 and E1 carry the gain caveat.
3. Deposits are 1080p h264 compilations, not raw stacks; compression quantization adds
   pixel noise (partially suppressed by the locked 1%-of-global-max threshold).
4. The paper's own xlsx supplements do not expose Figure 6 numeric values, so numeric
   agreement could not be tested beyond text-reported ranges.

## Bottom line

One of five preregistered endpoints reproduced cleanly (ATP variance trajectory), one
partially (EE 24h cohesion increase reproduced; EE during-stimulus xcorr stability
contradicted), three not reproduced (ATP 24h decohesion, EE 3h variance suppression,
baseline ordering). The deposited movies therefore do NOT support an independent
verification of the preprint's stimulus-specific "physiological memory" signatures as
published; the strongest robust discrepancy is the ATP 24h cross-correlation direction
(gain-invariant statistic, above null). This is consistent with this lane's standing
position that these remain preprint authors' claims, not independently verified results.
The single strongly-synchronous baseline Xenobot (xenobot_i, xcorr 0.86-0.92, far above
circular-shift null) does reproduce the paper's qualitative note of rare high-coherence
outlier Xenobots.

Negative-register entries added in docs/NEGATIVE_REGISTER.md (2026-09-29).
