# Study design locked before main implementation

Recorded 17 November 2026, Asia/Shanghai, immediately after the [selection lock](algorithm_selection.md). Final data remains untouched.

## Unit, dataset and partitions

UCI [Optical Recognition of Handwritten Digits](https://doi.org/10.24432/C50P49), Alpaydin and Kaynak, CC BY 4.0. Each image is an 8×8 array of counts (0–16) from nonoverlapping 4×4 blocks of a normalized 32×32 bitmap. Flatten in row-major order and divide by 16. Fit centering inside each training condition. Retain all 64 coordinates, including constant borders, to preserve adjacency. No learned pixel scaling or whitening.

Official development file: 3,823 images from 30 writers. Use shuffled stratified three-fold CV, seed 193 (2,548 or 2,549 fit images; 1,274 or 1,275 validation images). Per-row writer identifiers are absent, so the internal folds may share writers. The 1,797-image official test file represents 13 other writers. Use it after parameter locking and full-development refits. Archive indices with 0-based within-file row IDs, data checksums, explicit prediction labels, corruption rows and masks. Check duplicate pixel vectors and label consistency. Test duplicates, if any, are reported without changing predefined test membership.

## Questions and conditions

1. At eight projected coordinates, what are RSSPCA's accuracy and accuracy changes versus classical PCA and Fisher LDA under clean, 25%, and 50% corrupted training?
2. At a fixed sparsity penalty, does smoothing change recognition, loading roughness and fit cost?
3. How do feature budget and training corruption affect accuracy? Which classes contribute errors under the hardest condition?

Use uniform Euclidean 3-nearest-neighbor for all methods with fixed training row order. The raw pixel reference uses 64 coordinates. PCA uses a full centered SVD. LDA uses the classical multiclass Fisher subspace via a rank-aware SVD, with at most nine coordinates and supervised use of the same training labels. RSSPCA and the no-smoothing ablation share preprocessing and extraction except for the smoothing coefficient. All reduced methods use budgets 4 and 8; add budgets 16 and 24 for PCA and the robust PCA arms. Eight is the primary budget, chosen below the LDA rank ceiling. The raw reference gets its natural budget and is labeled accordingly.

Corrupt exactly $\lfloor f n\rfloor$ training rows, sampled without replacement, at $f\in\{0,0.25,0.50\}$. In each selected row, place one uniformly positioned 4×4 block and replace its 16 entries independently by 0 or 1 with equal probability. The 25% and 50% conditions use nested row choices and the same patch for shared rows. Maintain the original labels. The transform is applied to both subspace-fit and 3-NN training inputs. Validation and final test images remain clean. This tests noisy training, and the training-neighbor design includes both subspace and exemplar effects. Raw pixels expose the latter baseline.

Use fold corruption seeds 6101, 6102, 6103. Use final corruption seeds 7301–7305 for each positive fraction. Fit the deterministic clean condition once (seed field 0). All methods share each fold, seed, masks and class labels. Development-only fixed examples use the smallest row index for every digit class; the loading and diagnostic panels use the clean fit and first 50% seed where needed. Class plots show all classes at rank 8 under 50% training corruption and select the first prespecified seed for confusion counts. No example is selected by browsing the held-out images.

## Selection and analysis

Tune RSSPCA only on folds using the Cartesian grid $\eta\in\{0.001,0.01,0.1\}$ and $\gamma\in\{0.03,0.3,3\}$. Maximize mean validation accuracy at eight coordinates, weighting all nine fold × contamination conditions equally. Ties favor smaller $\gamma$, then smaller $\eta$. The controlled comparator inherits the selected $\eta$ and sets $\gamma=0$. Evaluate its independently tuned $\eta$ using the same grid and fold procedure as a secondary check if the inherited value differs, with the matched-penalty row retained as the ablation. Fit to all development rows after the lock. Fixed-point tolerance $10^{-4}$ in direction and a maximum of 100 steps per component. Save step histories and count capped components.

Primary metric is accuracy. Also record balanced accuracy, macro-F1, per-class recall, confusion counts, loading grid energy, median absolute sparsity indicators and measured wall time. Compute exact clean accuracy once and summarize positive-fraction results as mean and sample SD across five corruption realizations on the same test images. For the paired primary contrast RSSPCA minus PCA and paired smoothing contrast, report mean difference and paired run range, plus individual runs. These summaries condition on one official split and reuse the same labels. Writer-level inference is unavailable. No p-values or independent-run confidence intervals. Time from after corruption through fit (subspace plus kNN) and through batched prediction, with a CPU, BLAS and OpenMP thread limit of one. At rank eight time only the first eight robust coordinate computations even if the experiment also extracts higher ranks. Software versions and wall-clock measurements will be recorded.

## Figure plan

| Figure | Question and source | Report placement |
| --- | --- | --- |
| AI workflow | Trace the prompt inputs, candidate screening, gate, execution and report from the recorded task | 1 |
| Solver map | Relate training rows, sign votes, grid penalty, SPD normalization, deflation and 3-NN | 2 |
| Dataset and mask | Fixed-index development examples, class counts, one illustrative random patch | 4, data |
| Test comparison | Rank 8 accuracy, paired corruptions and clean/corrupt comparisons including raw reference | 4, results |
| Budget and smoothness | Accuracy versus feature count under severe corruption, shared smoothness ablation and fit time | 4, results |
| Loading maps and stopping | Fixed seed, rank 8 loadings/energy, step norm and cap | 4, interpretation |
| Class errors | Full confusion matrix and all per-class recalls for the first 50% draw | 4, limitations |
