# Final submission audit

**17 November 2026 (Asia/Shanghai) · CISC3024 Pattern Recognition · AI Assignment #3**

**Ready for submission.** All six requirements from the original handout pass. The title page gives the course, assignment number, and the specified student name and ID. This audit covers the report and public repository. The course submission itself is a separate UMMoodle action.

## Handout requirements

| Requirement | Status | Evidence in the final PDF |
| --- | --- | --- |
| 1. How AI finds the algorithm | **Pass** | Section 1, pp. 1–4. Four verbatim instruction excerpts match their named files. Six exact search strings, four credible candidates, the pre-implementation selection and face feasibility gates, and a labeled AI workflow explain the method choice and subsequent face pivot. |
| 2. Algorithm description | **Pass** | Section 2, pp. 5–6. Classical PCA and Fisher LDA provide contrasting objectives. The graph energy, absolute-score bound, damped update, symmetric solve, zero-coordinate equivalence and conditioning bound are derived. The worked example tests the update and shows the limits of the normalized map. |
| 3. How AI implements it | **Pass** | Section 3, pp. 7–8. Covers solver differences, residual initialization, span deflation, inference, QR reconstruction, computational cost, equation-to-code mapping, tests and numerical replay. The source contains the corresponding functions and checks. |
| 4. Experiment settings and results | **Pass** | Section 4, pp. 9–16. The primary study uses Olivetti faces. The closed-set split, shared masks, tuning, classifier, feature counts, smoothing ablation, test results and limitations are specified. Figure captions explain scales and variability. The distinct writer-disjoint digit study appears as secondary evidence on p. 16. |
| 5. What the student learnt | **Pass** | Section 5, p. 17. The student's five-paragraph reflection is complete. The final page matches the previously approved reflection in both text and rendered pixels. |
| 6. Source-code webpage | **Pass** | Section 6, p. 18. The public repository and Wiki URLs are visible and clickable. The repository contains the cited code, evidence, report source and compiled PDF. |

## Selection, mathematics and frozen study

- **Recency and difficulty.** Wang et al. published RSSPCA in peer-reviewed *PLOS One* on 27 May 2025. Its image-graph smoothing term changes the robust sparse PCA objective and yields a controlled ablation at fixed sparsity and dimension. The original search compared RSSPCA with DLR-2DPCA, SCRAMBLE and RSLDA+. The final audit located an author-linked RSLDA+ MATLAB solver. The matrix in Section 1 records the evidence available at selection. [RSSPCA article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0323281) · [Search ledger](research.md) · [Selection matrix and gate](algorithm_selection.md)
- **Two separate decision records.** The project logs place the Optdigits gate at 14:05 and the face gate at 14:55:18 on 17 November (UTC+8). The face design was saved at 14:57:01, the fits were frozen at 14:59:22 and the final face results were first written at 14:59:40. The student chose faces after the digit experiment. These timestamps come from the project records. [Face pivot chronology](face_pivot_decision.md) · [Locked protocol](face_study_design.md) · [Face freeze](../results/faces/freeze.json)
- **Fair comparisons.** All face arms use the same 16 × 16 inputs, disjoint 240/80/80 fit/validation/test views, final 320-row training pool, five matched masks at each positive severity, and Euclidean 3-NN. The four reduced arms share 8, 16 and 24 coordinates. Raw pixels retain 256, and LDA uses identity labels when fitting its projection. Removing graph smoothing keeps $\eta$ fixed. Each identity contributes six fitting, two validation and two test views. The $16\times16$ four-neighbor graph has 480 edges, and every final LDA fit supported 24 coordinates.

## Executed verification

An anonymous clone of `59c5b1d493092dcc408c0cbc576f2c23a2bbe96a` fetched both source datasets. All **13 tests** and `pip check` passed. The solve code, frozen settings, predictions, fits and experimental results are byte-identical between that revision and the final scientific release. The two feasibility probes were rerun. The two-pixel update reproduced the exact fractions and a $6.28\times10^{-16}$ linear residual. The face gate reproduced a $3.85\times10^{-16}$ SPD residual, loading agreement within $3.25\times10^{-16}$ and orthogonal deflation overlap $3.18\times10^{-14}$.

The same-environment face replay matched **143 prediction arrays** and **99 reconstruction-error arrays** exactly. The independent archive audit reproduced **11,440 classifications** from Euclidean distances and votes and checked reconstruction against least squares. It verified 400 distinct reduced inputs, the rank and geometry checks, shared masks and the exact 171/240 validation tie. The separate writer-disjoint replay matched **165 digit prediction arrays**. Regenerating the face tables and summaries reproduced the committed values. The report's wall times are observations from the original run and can vary. [Reproduction commands](../README.md#reproduce-the-face-study) · [Independent face audit](../results/faces/prompt02_audit.json) · [Publication checks](../results/faces/publication_report_check.json)

At 50% training corruption and 16 coordinates, face accuracy is 58.25% for RSSPCA, 55.50% for PCA, 56.50% without smoothing and 68.25% for Fisher LDA. The paired RSSPCA–PCA differences range from −7.50 to +10.00 percentage points. RSSPCA reduced mean loading energy from 2.440 to 1.226 relative to its no-smoothing arm and reduced reconstruction MSE by 24.5% relative to PCA. The digit report retains RSSPCA's severe-corruption deficit against PCA, 90.76% versus 91.13%. [Face results](../results/faces/final.json) · [Digit results](../results/summary.json)

## Figure and layout audit

All 19 pages were rendered and visually inspected at the final layout. Pages with revised equations and dense plots were checked at larger size. The build has embedded Latin Modern fonts, valid internal destinations and no TeX or bibliography warnings affecting the report. All eight figure PDFs passed strict collision and text-size checks. Final plotted panels in Figures 3–7 passed the rendered alignment audit.

| Figure | What was verified or improved |
| --- | --- |
| 1–2 (pp. 1, 4) | The first diagram connects the handout, prompts, skills, Codex work and verified public outputs. The second connects residual fitting and deflation to the separate 3-NN and QR outputs. |
| 3 (p. 9) | Four indexed square masks use uniform pixel ticks and mark untouched cells, 0 and 1 with a consistent legend. Source rows and actual stored patches agree. |
| 4 (p. 11) | Replaced overlapping lines with point ranges at the three tested severities. The declared 45–95% window contains all scores. Large and small markers distinguish summary and mask scores. The paired panel preserves all masks, a zero reference and min–max spans. |
| 5 (p. 12) | Shared symmetric signed scale and identical panel geometry. The caption identifies the orientation and distinguishes displayed loadings from the 16-direction row energy average. |
| 6 (p. 13) | Energy uses a linear scale, time uses a declared base-10 scale, and the empirical stopping curve uses percent of fitted directions. The caption defines the groups and stopping rule. |
| 7 (p. 14) | The 40–80% accuracy window retains all SD whiskers. Horizontal offsets and distinct shapes make them readable. The reconstruction panel starts at zero, and both show the locked primary budget of 16. |
| 8 (p. 15) | Zero-based MSE axis with common units and distinct method markers at the five prespecified source rows. The full 80-view comparison appears in Table 8. |

The changes were confined to presentation, mathematical exposition and source documentation. The report clarifies the block-triangular equivalence at zero loading coordinates, specifies the macro-F1 scale and links the newly located RSLDA+ solver. No experimental setting or value was changed.

## Public release and remaining risks

- Branch `main` in the [public repository](https://github.com/Nvb-flipped/cisc3024-rsspca-face-recognition) serves the final PDF and source at [`aa4e13ce55ff4efe2a8e6e0c49930104cdb888a5`](https://github.com/Nvb-flipped/cisc3024-rsspca-face-recognition/commit/aa4e13ce55ff4efe2a8e6e0c49930104cdb888a5). The audit is recorded in a documentation-only successor on `main`.
- **Final PDF location** is [`report/report.pdf`](../report/report.pdf), SHA-256 `b294afe966692d2aca5251f3ead251f470cacb291f937ef1f469429d635718e3`. The anonymous download matches the inspected local PDF byte for byte. The public README table and SVGs, rendered math, source tree and provenance files were checked.
- All eight [public Wiki](https://github.com/Nvb-flipped/cisc3024-rsspca-face-recognition/wiki) pages are accessible without sign-in. Figures and literature pages were synchronized at Wiki commit `80edb6fad33734002b7901f693abefb0bd46e422`. The dataset source requests attribution and leaves portrait redistribution terms unspecified. The public release uses saved masks, coefficients and numeric errors. Local galleries are regenerable from the checksum-verified input. [AT&T source](https://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html)

No outstanding critical or major issues were identified. Conclusions are conditional on the 40 known identities, two held-out views per identity, low-resolution inputs and fixed synthetic corruption procedure. Mask SDs measure variability on this split. The stopping rule measures changes in the fitted direction. Practical efficacy for unseen people, real test occlusions and global optimality are outside the demonstrated claims.
