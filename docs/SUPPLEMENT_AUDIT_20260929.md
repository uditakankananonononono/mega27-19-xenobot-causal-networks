# Supplementary bundle audit - Varley et al. 2025 (2026-09-29)

Question audited: does the only public supplementary bundle for Varley et al. 2025
("Identification of brain-like complex information architectures in embryonic tissue of
Xenopus laevis organoids", Commun Integr Biol, DOI 10.1080/19420889.2025.2568307,
PMC12520083) contain a cell-coordinates file? This decides whether a spatially-embedded
network reproduction (path A) is possible from public data, or the lane falls back to
path B (computational reproduction of the memory preprint's calcium quantification).

## Source chain (verified)

- The Taylor & Francis article page lists exactly ONE supplementary file:
  `kcib_a_2568307_sm1148.zip` (17.8 MB) at
  `https://www.tandfonline.com/action/downloadSupplement?doi=10.1080/19420889.2025.2568307&file=kcib_a_2568307_sm1148.zip`
- Direct curl and in-browser fetch of that URL both hit a Cloudflare "Just a moment"
  challenge (the HTML pages themselves load clean). Recorded in browser guidance.
- Workaround: EuropePMC `supplementaryFiles` endpoint for PMC12520083
  (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12520083/supplementaryFiles`)
  returned the full bundle (outer zip, 21,989,736 bytes, MD5 44f73e3462b845b2e17e26098603a7db).
- Inner data zip identity verified against the previously recorded hash:
  `KCIB_A_2568307_SM1148.zip` MD5 `83f778af536ec216f80770039248c1b8` - MATCHES.
  `calcium_data.tar.gz` SHA-256 `3cf2877d972a615d10c3869fe6819c124c3149d47ff4e9d4dcaaacabc08a732b` - MATCHES.

## Complete inventory

Outer EuropePMC zip (214 entries): 213 figure/illustration images
(KCIB_A_2568307_*.jpg/gif) + the inner data zip.

Inner `KCIB_A_2568307_SM1148.zip` (3 entries):
1. `brain_vs_xenobot_si.pdf.zip` -> 15,097,288-byte SI PDF. pdftotext extraction yields
   123 lines (methods math notes; the bulk is figure images). No occurrence of
   "coordinate", "centroid", "position", or "spatial location" in the extractable text.
2. `calcium_data.tar.gz` -> 28 NPZ files, `xenobot_series_{01..32}.npz`
   (numbers 15, 23, 25, 28 absent). Every NPZ contains exactly ONE array (`arr_0`,
   float64), a timepoints x cells matrix. Cells per series range 156-288, timepoints
   28-293. NO coordinates array, no metadata keys, no cell labels.
3. `results.zip` -> 9 CSVs of the authors' network statistics: `autocorr_results.csv`,
   `bte_results.csv`, `fc_modularity_results.csv`, `oinfo.csv`, `phi_results.csv`,
   `rss_results.csv`, `tc_dtc_results.csv`, `tse_results.csv`, `within_between.csv`.
   Headers inspected; all are statistic tables (fmri/xenobot rows, empirical/null),
   none contain cell positions.

## Conclusion

NO cell-coordinates file exists anywhere in the public deposit (data zip, results
tables, or SI text). A spatially-embedded network reproduction on the 28 bots is
impossible from public data alone; coordinates were not deposited. Path A is closed
unless the authors supply coordinates (would require a new author data request).
Per the 2026-09-29 07:23 plan, the lane falls back to path B: preregister a
computational reproduction of the March 2026 memory preprint's Figure 6 calcium
quantification from its 20 bioRxiv supplementary movies (heavy step: requires
green light per the heavy-compute rule before any movie download).

Secondary blockers noted during this audit: EuropePMC REST (search endpoint) returning
intermittent 503s; bioRxiv rate-limiting (HTTP 429) repeated page fetches.
