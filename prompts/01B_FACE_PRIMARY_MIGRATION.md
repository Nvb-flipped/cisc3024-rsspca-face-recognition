# Prompt 01B — Face-Recognition Pivot, Preserving Verified RSSPCA Work

**Do not start a new Assignment #3 project and do not rerun Prompt 01 from scratch.** Read `AGENTS.md`, the original `AIassign3.pdf`, `prompts/01_RESEARCH_IMPLEMENT_REPORT.md`, the latest `report.pdf` (or compiled report), research/selection records, all source code, saved digit-experiment results, and any available skills. This prompt is a deliberate, student-directed *change of primary application after Prompt 01*, made to differentiate Assignment #3 from Assignment #2. **It is not evidence that face data were part of the original locked digit experiment.**

## Main decision

Retain **Robust Sparse Smooth PCA (RSSPCA)** from Wang et al. (PLOS ONE, 2025), including verified mathematics, validated solver and literature-selection history. Change the **primary application** to face recognition and, if scientifically justified, face reconstruction. Preserve the original UCI Optdigits study as a clearly labeled, previously executed *secondary transfer experiment* or archived experiment, not as the main subject.

The paper actually studies face reconstruction and recognition. A possible accessible dataset is **Olivetti/AT&T Faces** via `sklearn.datasets.fetch_olivetti_faces`: 400 faces, 40 identities, ten images per identity, original loader resolution 64×64. Independently verify its source, terms and suitability. You may choose a better verifiable face dataset if that materially improves the study without creating excessive cost or access issues. Do **not** claim a faithful reproduction of the paper's original experiments unless the protocols truly match.

## A. Protect existing work and record provenance

1. Inspect Git status, remotes, local uncommitted changes and current artifacts. Preserve them; do not delete or overwrite the digit project/evidence. Use a safe separate branch such as `study/face-primary` after ensuring no work is lost. Avoid force push.
2. Preserve existing digit configuration, predictions, mask seeds, results, final-test history, figures and paper source in an archive or namespaced output folder with provenance. Do not silently change old metric values.
3. Create `docs/face_pivot_decision.md`: explain the human request, rationale (Assignment #2 also used 8×8 digits), what is unchanged (method/literature/mathematics), what is newly chosen (dataset/protocol/results), and exactly when the face-study design was locked relative to its first held-out evaluation.
4. In Section 1 of the final report, distinguish original Prompt 01 literature search, the later human-directed face pivot, this exact Prompt 01B and Prompt 02 review. Cite **actual** prompt excerpts; do not rewrite history to claim the original search was always for faces.

## B. Mandatory face feasibility gate — before full experiments

1. Inspect core RSSPCA code for assumptions tied to digit grids, 8×8 or 64-dimensional vectors. Refactor properly for arbitrary rectangular image shape; explicitly define how the 4-neighbor pixel-grid Laplacian is built. Check 8×8 regression tests still pass.
2. Evaluate a **small training-only face prototype** with independent numerical checks: grid energy, fixed-point update and SPD residual, zero-coordinate behavior, sign invariance, deﬂation, rank, stability of learned loadings and projection/reconstruction as applicable. Preserve the mathematically validated RSSPCA mechanism.
3. The face loader outputs 64×64 images (d=4096), substantially larger than the digit study (d=64). The existing dense RSSPCA solver must **not** be assumed scalable at d=4096. Preselect and validate a smaller representation such as **16×16 (d=256)** using a fixed documented antialiased resampling rule. A 20×20 representation is a possible alternative if profiling and numerical tests justify it. Measure actual fit cost and memory using training-only samples. Do not silently compare methods on different resolutions. If maintaining original resolution, require a real validated scalable formulation, not an unjustified dense solve.
4. Validate classical PCA and LDA on the same training-only face prototype with shared input representation and downstream classifier. LDA has at most **C − 1 = 39** nontrivial discriminant coordinates for 40 identities; respect numerical/sample-rank limits. Verify any proposed feature budgets are legal for all compared methods.
5. Before the first face-test evaluation, write `docs/face_study_design.md`, including dataset provenance, resolution, split design, all candidate hyperparameters, classifiers, seeds, corruption procedures, metrics, figures, controls, evaluation order and explicitly locked acceptance requirements.
6. If a meaningful face-study prototype **fails** because the numerical method cannot be validated, runtime or memory is impractical, or the dataset/protocol is unsound, **do not replace it with invented results**. Record the blocker and fall back to the intact digit study. Do not switch to an unrelated algorithm without explaining and separately validating a fresh decision.

## C. Proper face-recognition experiment

**Recognition setting:** Closed-set identification of the same 40 identities using **different images** of each person for fitting and testing. Avoid accidentally treating an identity-disjoint split as a valid closed-set 40-class recognition test: a classifier cannot predict classes absent from training. State that results concern known identities and cannot establish generalization to unseen people.

- Define a deterministic **identity-stratified train/validation/test split** (for example 6/2/2 images per identity), preserving every identity in training. Alternatively use a better well-justified predeclared protocol. All tuning and method development are on training/validation only. One fixed held-out face test should be touched only after locking; if repeated holdouts are used, predeclare all splits and use nested selection, reporting the correct estimand rather than claiming one untouched test.
- Predefine meaningful matched baselines: unprojected pixels, classical PCA, Fisher LDA, RSSPCA without smoothing and full RSSPCA, as feasible. Match input resolution, train examples, corruption masks, downstream evaluator and projection budget. Explicitly note the supervised advantage of LDA when labels determine the subspace.
- Predefine train-only corruption levels (including clean and at least one corruption condition) and mask seeds; apply equivalent corruption to all methods. If test images are corrupted for a separate robustness question, predeclare this as a distinct evaluation with clear target definitions.
- Compare feasible feature counts using the same permitted subspace dimension budgets where possible. Predefine a small hyperparameter grid for sparsity and smoothness using training/validation only. Include a controlled smoothing ablation (gamma=0) and, if computationally justified, other mechanism ablations.
- Use appropriately cautious metrics: accuracy and balanced accuracy/macro-F1 for identity recognition, per-subject recall or confusion analysis; repeated training-corruption variation and/or appropriately separated splits; runtime and numerical convergence. With only 10 images per identity, acknowledge wide uncertainty and avoid inflated statistical claims.
- If evaluating **reconstruction**, implement an explicit mathematically correct reconstruction for **possibly nonorthogonal** learned loadings (e.g. orthogonal projection through an orthonormal basis of their span, not naively treating W W^T as a projector). Verify the identity and compute train-independent errors. Clearly distinguish restoring a clean target from merely projecting a noisy image; never label the latter denoising without valid matched evidence.
- Run actual experiments, save machine-readable evidence, independently audit metrics and model artifacts, test deterministic reruns, and document failures and negative outcomes. Never optimize the method based on the final test observations.

## D. A deliberately different scientific visual story

The original digit report has confusion matrices, class balance and classification comparisons resembling Assignment #2. Make the revised report visually and scientifically distinct through *face structure and the PCA mechanism*, without fabricating extra evidence. Create a figure plan and use relevant installed skills (`nature-figure`, `plot-from-data`, `scientific-visualization`, `scientific-figure-making`, `agent-figure-gallery` and any actually relevant others).

Strong candidates (keep only evidence-backed, useful figures):

1. **Human-to-AI workflow diagram**, accurately showing initial digit study, post-Prompt-01 face pivot, implementation, evaluation and review as distinct chronological stages.
2. **RSSPCA mechanism diagram**: face image → centering → sparse/robust/smooth projection optimization → face subspace → downstream evaluation/reconstruction.
3. **Genuine face-gallery and corruption protocol**, including fixed selected indices and attributions/rights.
4. **Component/eigenface and spatial loading maps** for classical PCA vs RSSPCA, with comparable scales and sign convention.
5. **Clean/corrupted/reconstructed face grid** if reconstruction is actually implemented, mathematically valid and evaluated.
6. **Recognition performance vs training corruption**, paired across matched masks and baselines, with appropriate uncertainty semantics.
7. **Projection budget and method ablation**, reporting the effect of component count, smoothness/regularization and potential method interactions.
8. **Grid energy/sparsity/convergence** diagnostics directly supporting the three regularization mechanisms.
9. **Runtime or memory vs feature count**, measured rather than estimated.
10. **Failure analysis** with carefully selected actual face examples and class-level errors where appropriate.

Use figure families that teach the reader the distinctive PCA mechanism, not repeated generic classification plots. A confusion matrix is allowed if useful but need not be the headline graph. Prefer consistent vector outputs with readable typography at page scale, scientifically honest color scales and meaningful captions. Inspect every PDF page, fix clipping, inconsistent fonts and excess whitespace.

## E. Revise the LaTeX report in place — not cosmetic search/replace

- Change report title, abstract, primary figures/tables, protocol, analyses and conclusions to reflect **face recognition / reconstruction**, if the feasibility gate passes.
- Preserve verified RSSPCA derivations, update equations, toy examples, code mappings and literature source, revising image-grid dimensions and operation counts accurately.
- Include documented differences from Wang et al.'s published face experiments, especially source dataset, resizing, optimizer initialization/stopping/deﬂation and evaluator choices.
- In Section 1, include actual `AGENTS.md` + Prompt 01 + **Prompt 01B** instructions and accurately describe why the human changed the application after observing the digit overlap. Include the mandatory workflow diagram.
- In Section 4, present the face dataset as **primary** and Optdigits only as an optional **secondary transfer study** with clear separation; do not combine metrics from different datasets into a single unexplained table.
- Keep the instructor's six main headings. Leave the student-authored reflection for the student; leave public repository link pending until actually published.
- Update README/docs/wiki drafts and all reproduction commands to support the new primary experiment. Preserve clear provenance for both experiments.
- Recompile and render every page, compare all report numbers against archived outputs and fix presentation defects. Preserve real negative results.

## F. Acceptance gate and handoff to Prompt 02

Completion requires: the face feasibility test passed; real face results saved and audited; scientific method baselines/ablations implemented and fairly compared; clear disclosure of dataset/protocol deviations; self-contained mathematically rigorous PDF with face-centric figures; the old digit experiment preserved; traceable prompt history; runnable reproduction; and no fabricated measurements. If feasibility fails, return a reasoned, documented fallback without erasing any work.

**Do not publish to GitHub yet; do not invent a personal reflection.** Once this stage completes, proceed to the face-aware Prompt 02 quality review in a separate Codex task.
