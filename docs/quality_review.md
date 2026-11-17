# Prompt 02 critical review

Codex conducted an examiner-style self-audit with three internal AI review passes covering the mathematics, protocol and graphics. The audit compares the pre-review face commit `8267cad` and the digit baseline `181d542` in the local research history with the Prompt 02 report. Its page numbers and PDF checksum refer to that edition. The current public report adds the student's reflection and repository URL and uses numeric illustrations for Figures 3 and 8. The frozen study artifacts are the record of the original evaluations. [Current report](../report/report.pdf)

## Assignment coverage and selection gate

| Requirement | Revised PDF | Evidence and disposition |
| --- | --- | --- |
| 1. Explain how AI found the recent method | §1, pp. 1–4 | Four verified verbatim excerpts, six search strings and a literature lookup, four candidates, both development-only gates, documented skill use and an instruction-to-execution diagram. |
| 2. Derive and explain the algorithm | §2, pp. 5–6 | Classical scatter models and rank bounds, grid energy, linear and quadratic bounds, published update, equivalent SPD system, positive lower eigenvalue bound, zero support, exact two-pixel example and failed tangent-stationarity example. |
| 3. Explain AI implementation and verification | §3, pp. 7–8 | Reference differences, orthogonal deflation, raw-score distance, cost bound, equation-to-code table, QR reconstruction, tests and independent archive/replay checks. |
| 4. Present experiment settings, results and discussion | §4, pp. 9–16 | Locked split and masks, validation grid and tie rule, matched 3-NN controls, accuracy/F1, reconstruction, mechanism ablation, stability diagnostics, error examples and distinct supplementary digits. |
| 5. Student learning reflection | §5, p. 16 | Prompt 02 reserved space for the student's writing. The current report contains the supplied reflection on p. 17. |
| 6. Public source webpage | §6, p. 17 | Public release was scoped to Prompt 03. The current report links the public repository on p. 18. |

| Review criterion | Disposition |
| --- | --- |
| Recency and direct PCA contribution | Pass. Wang et al., PLOS One 20(5), e0323281, published 27 May 2025. The methodological contribution adds a spatial smoothness constraint to robust sparse PCA. It combines a sign-based absolute-score update, local quadratic sparsity majorization and graph regularization. The paper applies the method directly to face reconstruction and recognition. [Version of record](https://doi.org/10.1371/journal.pone.0323281) |
| Published details and difficulty | Pass. The paper supplies the method-defining system and the authors supply a GPL-3.0 MATLAB reference. The Python implementation derives its own SPD solve and specifies the initialization, stopping and deflation differences. All required calculations and principal limitations can be verified at assignment scale. [Author reference](https://github.com/yuzhounh/RSSPCA) |
| Alternatives and feasibility tradeoffs | DLR-2DPCA uses cut reconstruction loss and adaptive weights for recognition including CMU PIE, GTSRB and MNIST. Right matrix projections on digits restrict scalar-budget matching to multiples of eight. SCRAMBLE offers cellwise robust loss and elastic-net sparsity, with the latter disabled in the wear-scar image regression example. The reference implementation is available, but solver and scale choices increase transfer work. RSLDA+ directly targets image classification with a sparse LDA/ADMM approach. The publisher preview and audit evidence were insufficient to reproduce the complete solver. [DLR-2DPCA accepted manuscript](https://trepo.tuni.fi/bitstream/handle/10024/231390/Double_Layer_Robust_2DPCA.pdf) · [SCRAMBLE version of record](https://doi.org/10.1007/s11634-025-00656-3) · [RSLDA+ publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0031320324002632) |
| Selection lock and chronology | The original gate records the decision at 14:05 on 17 November 2026 (UTC+8), and the digit runner froze its development fit before acquiring the final asset. After the student's pivot, the face gate passed at 14:55:18 using only the 240 fitting rows, followed by the protocol at 14:57:01, the fit freeze at 14:59:22 and final face scores at 14:59:40. The timestamps come from the project records and staged runner. The Git snapshots postdate the evaluations. The suitability weights are a project decision aid. [Original gate](algorithm_selection.md) · [Face chronology](face_pivot_decision.md) · [Protocol](face_study_design.md) |
| Executable gate | Both pre-existing gate scripts were rerun. The digit probe returned the exact two-pixel update and a 27-step RSSPCA fit. The face probe passed the original limits at 16 × 16, with a 24-direction fit in 0.386 s on this rerun, 2.84 MiB of tracked allocations and normalized update agreement of $3.25\times10^{-16}$. The original archived timing remains the reported measurement. [Digit gate record](../results/gate_probe.json) · [Face gate record](../results/faces/gate.json) |

## Findings and repairs

Baseline page numbers below refer to the pre-review 17-page PDF. Severity applies to the defect observed in that build.

| Severity | Baseline file and page | Finding and repair | Revised PDF |
| --- | --- | --- | --- |
| High | `report/report.tex`, p. 1, Figure 1 | The required workflow began at the staged prompts. It omitted the handout, persistent rules, relevant skills, actual review work and inspected outputs. Redrew the complete workflow and verified four exact source excerpts and their effects, including Prompt 02. | pp. 1–4 |
| High | `report/experiments.tex`, p. 12 | The mechanism discussion gave 4.37% near-zero weights for the no-smoothing arm. That number matches the accuracy SD in pp. The correct fraction is 2.67% at rank 16 under the five severe masks, versus 1.97% with smoothing. Recomputed from the weights and defined the threshold and population. | p. 12 |
| Medium | `report/algorithm.tex`, pp. 5–6 | The distinction between the constrained objective and tuned fixed penalty ratios was implicit, and the graph description understated attenuation near a zero loading. Clarified both, retained the toy stationarity counterexample and anchored stopping to saved traces. | pp. 5–6, 13 |
| Medium | `report/report.tex`, p. 4, Figure 2 | The update schematic concealed the repeat-to-stop loop and combined readouts in one node. Revised the algorithm schematic and caption to explain normalized sign alignment, residual deflation and distinct score and QR readouts. | p. 4 |
| Medium | `report/experiments.tex`, pp. 10–12 | Fairness details lacked the fitted LDA scale, tie behavior, and fit-time accounting across budgets. Documented rank and geometry, shared Euclidean 3-NN, the fixed identity-code tie rule, and cumulative versus reused decomposition timing. The exact tuning tie was 171/240 for each of the two best settings. | pp. 5, 10, 13, 15 |
| Medium | `report/experiments.tex`, p. 12, Figure 6 | Iteration counts alone could be read as evidence of objective convergence. Added a severe-mask cumulative stop plot and an independently computed next-step and score diagnostic. All saved directions met the step rule. One subsequent step slightly exceeded its threshold and the raw score sometimes decreased. | p. 13 |
| Medium | `report/experiments.tex`, p. 15 | The comparison with the published paper omitted key details that bear on interpretation. Added original recognition split, standardization, rank and nearest-neighbor procedure plus the reconstruction fit/evaluation relationship. The face and digit archives have different protocols, independent locks and separate conclusions. | p. 16 |
| Low | `report/experiments.tex`, p. 13 | Clean PCA MSE in prose rounded to 2.662. The archived scaled value is 2.661450..., which rounds to 2.661 as in the table. Corrected the prose. | p. 14 |
| Low | `src/face_figures.py`, Figures 3–5 and 7–8 | Clarified mask support, matching, panel normalization, nested budgets and display clipping. Separated the two severities in the paired plot using color and marker shape. Enlarged loading maps and marked the primary budget. | pp. 9, 11–12, 14–15 |
| Low | `README.md`, replay instructions | The canonical fit directory is also the runner default. Documented the fresh-directory replay and a separate archive audit with one derived output, protecting the recorded metrics and manifest from incidental replay writes. | p. 17 points to the replay commands |

The first revised build isolated Figure 1 on a nearly empty page. The rendered figure audit also identified a legend/grid collision and a schematic label touching the edge of its card. The final layout places Figure 1 on the opening page, moves the affected legend, shortens the card label and enlarges the spatial loading maps.

## Numerical, protocol and reproduction checks

- Both gate scripts and all 13 existing tests passed. The archived face freeze verified the settings, source/data digests, split, fitted weights and masks. The fresh same-environment replay matched 143 recognition arrays and 99 reconstruction-error arrays exactly. The digit replay verified 165 arrays separately. The digit runner, fit code, lock, predictions, results and archived PDFs remain unchanged relative to the preserved baseline. Timings in the report come from the original measurements.
- The independent archive script rebuilt the source orientation and block means, verified all 400 distinct faces and the disjoint 6/2/2 counts for each identity, regenerated the validation and final mask streams and checked every fitted center. The original MAT file decodes as one archive. Before final scoring, only designated development rows were used for feature reduction, fits and validation statistics. The audit recalculated 11,440 predictions using direct squared distances and class votes, reproduced all metrics, and found zero ties at the third-neighbor boundary.
- The support-preserving SPD reduction agrees with the independent nonsymmetric system in gate and unit checks. The review tested archived unit norms, residual orthogonality, grid energy from finite differences, normalized PCA residuals (maximum $2.42\times10^{-15}$), within-class whitening for LDA and rank-24 availability in all final LDA fits. Independent least-squares solves reproduced the stored per-image reconstruction errors. The audit also applied one additional nonsymmetric update to each of 528 robust saved loadings. [Audit output](../results/faces/prompt02_audit.json)
- Five shared masks at each positive severity vary the training treatment on the same fixed 80 test views. Their sample SDs and paired ranges quantify mask sensitivity conditional on this split. There is one deterministic clean run. The validation tie and held-out comparisons did not change the prior choice of rank or penalties.

The audited face commands ran with `LOKY_MAX_CPU_COUNT=1` on the available Windows environment. Follow the [test launcher](../README.md#reproduce-the-face-study) and choose a fresh replay directory.

```text
python -m scripts.face_gate
python scripts/gate_probe.py data/optdigits.tra
python -m src.face_study tune --out results/reproduction/prompt02-faces
python -m src.face_study prepare --out results/reproduction/prompt02-faces
python -m src.face_study final --out results/reproduction/prompt02-faces
python -m src.face_study audit --out results/reproduction/prompt02-faces --against results/faces
python -m scripts.review_face
python -m src.experiment verify --out results/reproduction --against results
python -m src.face_summary
python -m src.face_figures
```

The digit `verify` command compares the prior replay's saved outputs. For a new digit replay, use the [archived reproduction commands](../report/optdigits/README.md).

## Figure audit

All eight figures export vector labels and axes in Latin Modern. Face tiles maintain their native 16 × 16 cells, and figure-specific raster regions use nearest-neighbor display. All eight exported PDFs passed the strict collision and minimum-text audits. The final report was rendered and all pages inspected, with the loading maps, stopping plot and equations also checked at an enlarged view. [Face figures](../results/faces/figures/) · [Compiled PDF](../report/report.pdf) · [PDF verification record](../results/faces/prompt02_report_check.json)

| Figure, page | Question and exact source | Population, scale and encoding | Uncertainty and inference boundary |
| --- | --- | --- | --- |
| 1, p. 1 | How did instructions produce the local evidence? Handout, `AGENTS.md`, three prompts, `docs/research.md` and `docs/ai_usage.md`. | Eight directional cards follow the two-row reading order. No measurement axis. | Chronology and dependencies, with no independent timestamp implied and no publication claim. |
| 2, p. 4 | Where do the graph and learned span act? `src/face_data.py`, `src/projectors.py`, `src/face_study.py`. | Directional cards show centering, the sign/SPD loop, deflation and the two readouts. No measurement axis. | Schematic of implemented operations. The loop's stopping condition is evaluated empirically in Fig. 6. |
| 3, p. 9 | What training perturbation was applied? Pinned source MAT, `split.json` and seed-8301 mask in `models.npz`. | First four positions of the severe mask, source rows 176, 178, 392 and 28. Common $[0,1]$ grayscale and binary replacement support. | Deterministic development examples. Support shows cells eligible for a value change. |
| 4, p. 11 | Does RSSPCA improve identification with shared masks? `final.json` and `predictions.npz`. | Accuracy on 80 fixed clean views, rank 16 except 256 raw pixels. A has a zero-based accuracy axis. B shows within-mask RSSPCA minus comparator in pp, shape and color distinguish severity, and open marks show means. | Five points at each positive severity per arm or contrast. One clean fit. A paired point represents one training mask, and repeated masks reuse each test face. |
| 5, p. 12 | Where are the spatial weights, and how rough are they? Seed-8301 arrays in `models.npz` and energies in `final.json`. | Four extraction-order maps per PCA-family arm, a common symmetric signed weight scale and mean energy across the first 16 loadings. | One prespecified severe fit. Columns show within-arm order. Fig. 6 shows the corresponding roughness across all severe masks. |
| 6, p. 13 | How much smoothing, fitting cost and finite-step termination were observed? `final.json` and `fits.json`. | A edge energy by mask and means at rank 16. B fit wall time in ms on a log axis and medians. C cumulative percentage of directions reaching the threshold by update count, 120 directions per arm. | Fit-time differences include implementation-specific accounting. Directions are nested within five mask fits. The $10^{-4}$ threshold applies to the sign-invariant step in Euclidean norm between unit loadings. The displayed endpoint is an empirical stop, with no stationarity certificate. |
| 7, p. 14 | Does the coordinate budget change the results? `final.json`, `reconstruction.npz` and locked ranks in `selection.json`. | Ranks 8, 16, 24. Recognition in percent and pre-clipping pixel MSE × $10^3$ over clean held-out inputs. | Whiskers give sample SD across the five severe masks on the same test images. The dashed guide marks the locked primary budget. |
| 8, p. 15 | What structure does a learned span retain? Pinned source MAT, saved `models.npz` and locked gallery identities. | First held-out source row for each chosen identity (7, 91, 190, 294, 393), using seed 8301 at rank 16. Thin QR projection and common $[0,1]$ display. | Deterministic examples with display-only clipping. The primary inference uses all 80 clean test inputs and the unmodified errors in Fig. 7 and Table 8. |

Assignment #2's actual comparison and convergence figures concern prediction error counts, likelihood/Brier scores and epoch-level learning curves. Here the diagrams and plots emphasize a spatial graph, linked mask contrasts, signed loading fields, edge energy, finite-step directions and orthogonal reconstruction. The distinction follows the scientific questions and recorded variables.

## Findings retained and publication scope

At 50% training corruption and 16 coordinates RSSPCA achieved 58.25% face accuracy, versus 55.50% for PCA, 56.50% without smoothing and 68.25% for Fisher LDA. Its paired accuracy differences versus PCA ranged from −7.50 to +10.00 pp, and raw pixels also led RSSPCA with a larger feature budget. Severe-corruption reconstruction MSE was 24.5% below PCA, but PCA had lower MSE with clean training. On Optdigits, RSSPCA was worse than PCA at 50% corruption (90.76% vs 91.13%). The original results and fitted models were kept without test-driven retuning.

The fixed-$\eta$ ablation identifies the effect of the graph penalty under a shared setup. The separate effects of the absolute-score criterion and sparsity regularization were outside the design. Training patches affect both subspace estimation and reference neighbors, so the study does not isolate their pathways. It is a low-resolution, known-identity study with two distinct held-out views per identity and synthetic training corruption. Evidence about genuinely occluded inputs, unknown people, alternate voting tie rules, or other resolutions would require a separate experiment.

The report includes the student's reflection and links the public repository. The raw AT&T archive is obtained separately. Its official page asks users to credit AT&T Laboratories Cambridge and gives no explicit terms for redistributing portraits. The public snapshot uses generated mask illustrations and measured per-image error plots. [AT&T source](https://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html) · [Olivetti source code](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/datasets/_olivetti_faces.py)
