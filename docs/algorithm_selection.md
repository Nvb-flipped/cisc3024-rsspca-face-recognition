# Algorithm selection gate

**Decision locked 17 November 2026, 14:05 Asia/Shanghai. PASS for RSSPCA. Selection locked before final test and before main implementation.** The official test asset had neither been downloaded nor parsed. See [research and exact queries](research.md) and [probe output](../results/gate_probe.json).

## Hard eligibility

| Test | RSSPCA | DLR-2DPCA | SCRAMBLE | RSLDA+ |
| --- | --- | --- | --- | --- |
| Substantive PCA/LDA contribution | Pass. L1 projected dispersion with grid-regularized sparse loadings | Pass. Matrix reconstruction criterion with double robustness | Pass. Cellwise robust reconstruction on an orthogonality manifold | Pass. Sparse terms change LDA directly |
| Recent peer-reviewed work | Pass, 2025 PLOS One | Pass, 2025 IEEE TCE | Pass, 2025 journal version | Pass, 2024 Pattern Recognition |
| Direct vision relevance | Pass, face recognition and reconstruction | Pass, face, digit and traffic sign recognition | Pass, wear-scar image regression and loading analysis | Pass, image classification |
| Specific mathematics and solver | Pass, full §§3.1–3.5 and reference loop | Pass at paper screen, objective and Algorithm 1 readable in accepted manuscript | Pass at paper screen, loss, gradient, retraction and initialization described | Fail, full updates unavailable |
| Implementability | Pass, normalized map checked independently | Viable on paper, more numerical edge cases and no located code | Viable on paper, more design choices and R reference | Fail, implementation would require guessing |
| Controlled evaluation | Pass, official UCI split, same scores budget, 3-NN, no-smoothness ablation | Viable, scalar budget in multiples of image height, classical 2DPCA and matched 3-NN | Viable, matched PCA and squared-loss ablation on the same UCI split | Unverified, blocked by solver access |
| Compute and schedule | Pass, measured development probe, 64-feature dense solve | Plausible on 8×8 data, unbenchmarked | Plausible on 8×8 data, unbenchmarked | Unverified |
| Disposition | Selected following technical probe | Viable alternative at source review | Viable alternative at source review | Ineligible |

## Suitability matrix

Scores are 1–5; weights are self-imposed decision guidance from Prompt 01. This is a comparison for the assignment using observed source evidence and projected operation counts.

| Method and verified source | Recency 15% | Centrality 20% | Implementation 20% | Experiments 20% | Math 15% | Figures 10% | Weighted /5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [RSSPCA](https://doi.org/10.1371/journal.pone.0323281) | 5 | 5 | 5 | 5 | 5 | 5 | 5.00 |
| [DLR-2DPCA](https://doi.org/10.1109/TCE.2025.3602258) | 5 | 5 | 3 | 4 | 5 | 4 | 4.30 |
| [SCRAMBLE](https://doi.org/10.1007/s11634-025-00656-3) | 5 | 5 | 3 | 4 | 4 | 4 | 4.15 |
| [RSLDA+](https://doi.org/10.1016/j.patcog.2024.110512) | 5 | 5 | 1 | 2 | 2 | 3 | 2.95 |

| Method | Workload and risk | Evidence and comparison opportunities |
| --- | --- | --- |
| RSSPCA | For $n$ rows and $d$ pixels, one dense update costs $O(nd+d^3)$ time and $O(nd+d^2)$ memory including data. Exact zeros are absorbing for the positive sparsity update. The full constrained optimum is unverified. | Four-neighbor energy and loading maps diagnose the new term directly. The same projected coordinate budget is available to classical PCA and LDA. Official MATLAB GPL-3.0 reference is available. |
| DLR-2DPCA | For $n$ matrices of $h$ rows and $w$ columns and $r$ projection axes, straightforward residual, weighted scatter and polar steps cost roughly $O(nhwr+nhw^2+w^2r)$ per sweep with cached/streamed row matrices, plus residual and weight storage. Cut-threshold boundaries and near-zero residual denominators require careful handling. | Good corruption and reconstruction figures. A right projection still yields $hr$ scalars, so matching general vector methods restricts the rank schedule. Paper uses CMU PIE, GTSRB and MNIST. No verified author code or reuse license. |
| SCRAMBLE | A dense loss/gradient sweep costs roughly $O(ndr+dr^2)$ with QR, plus scale estimation and outer tuning. Robust initialization, scale treatment, retraction, thresholding and regularization selection increase implementation choices. | Image regression and residual maps are evidenced by the paper; a digit classifier requires a larger protocol transfer. MIT R reference and author replication files exist. A no-smoothness contrast is specific to RSSPCA. |
| RSLDA+ | Insufficient accessible equations for an accountable complexity estimate or independent threshold-update audit. | Recognition target is relevant, but code or full solver was unavailable in this search. |

Each eligible 2025 approach scored equally for recency and genuine PCA substance. RSSPCA was at least tied on every remaining criterion. Positive weight on implementation or matched evaluation preserves the preference. The choice does not depend on predicting which method will win on test accuracy.

## Independent feasibility proof

```powershell
python scripts/gate_probe.py data/optdigits.tra
```

The probe derived a symmetric positive-definite form of the paper’s defining update and compared it to an independent rational two-by-two solve. It returned $(132/71,200/71)$ before normalization, the expected unit direction, and an original-system residual of $6.28\times10^{-16}$. The zero-coordinate test returned $(20/17,0)$, and the smallest symmetric-system eigenvalue in the nonzero toy was $0.87251$. The normalized candidate had a sphere-tangent residual of 0.37589 for the quadratic surrogate. This separately checks why the normalized rule needs to be described as a fixed-point procedure.

The development file had 3,823 unique image rows, 64 block counts, ten classes with 376–389 examples and two constant pixels. One stratified 3,058/765 split with seed 193 gave 96.08% validation accuracy using PCA-8 and Euclidean 3-NN. The full float64 development image matrix used 1,957,376 bytes. A one-direction RSSPCA probe reached the $10^{-4}$ step bound in 27 iterations at $(0.01,0.3)$; the recorded pass took about 9.8 ms including duplicate counting. This exercises the core operations on the observed CPU and supports the proposed run budget without testing final data.

## Locked choice and scope

Use Wang et al. (2025), DOI [10.1371/journal.pone.0323281](https://doi.org/10.1371/journal.pone.0323281). Implement the sign-based absolute-score map and four-neighbor smoothness independently in Python, using a congruent symmetric solve, residual SVD starts, orthogonal projection for deflation and sign-invariant step stopping with an iteration cap. Retain raw normalized loading scores for classification. The study adapts the method to handwritten digits and evaluates recovery of recognition accuracy when training images are corrupted. Loose results in the source paper cannot establish global optimization, constraint-budget satisfaction, general robustness, or superiority on Optdigits.

Use official UCI Optdigits and its writer-disjoint final partition. Use classical PCA, Fisher LDA, raw pixels, and the RSSPCA update with the smoothing coefficient fixed at zero. Compare clean and synthetically corrupted training sets with shared kNN and dimension budgets. Track recognition, loading energy, fit cost and class errors. Tune inside the official development partition. See [study design](study_design.md).
