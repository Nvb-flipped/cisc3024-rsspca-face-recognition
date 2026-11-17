# Prompt 01 — Research, Design, Implement, Experiment and Draft the Report

**Execution instruction:** Read `AGENTS.md` and the **actual** `AIassign3.pdf` in the current workspace. Follow the full instructions below autonomously. Do not just produce a plan or code: research, implement, execute and generate a serious first LaTeX/PDF report.

The target is **CISC3024 AI Assignment #3**: find a **recent PCA/LDA algorithm with an application to computer vision and pattern recognition**. All work, including programming, is performed by AI as required by the assignment.

**Critical first decision:** Topic difficulty and publication recency can plausibly influence assessment although the handout publishes no numerical grading rubric. Therefore **do not select the algorithm informally and do not begin the full implementation until the mandatory algorithm-selection gate (Section B2) is passed.** Select autonomously using evidence, not prestige or a promise of 100/100.

## A. Initial environment and skills audit

1. Inspect this workspace, existing files, Git status, Python/scientific libraries, available CPU/GPU, operating system, LaTeX build options and GitHub tooling. Record only facts that are observed.
2. Locate and inspect the complete instructions (`SKILL.md` and any pertinent references) for each applicable skill. They currently may be at:

   `~\Documents\Codex\Pattern Recognition\bayesian-handwritten-digit-recognition\.agents\skills\<skill-name>\`

   I will move them into the new Assignment #3 `.agents/skills/` folder later. If they have moved, locate the new installation rather than failing due to an old path.
3. Use the **relevant** skills below, distinguishing central skills from conditional ones. Verify actual applicability instead of invoking all blindly.

| Skill | Intended role |
| --- | --- |
| `literature-review` | Primary-paper discovery, verification and algorithm-selection evidence |
| `experimental-design` | Research questions, matched baselines, split discipline and ablations |
| `analytical-method-validation` | Derivations, eigenproblems, numerical and theoretical consistency checks |
| `exploratory-data-analysis` | Dataset provenance, class structure, image characteristics, leakage screening |
| `scikit-learn` | Classical PCA/LDA baselines, pipelines, train/test isolation and metrics |
| `statistical-analysis` | Run-to-run variation, intervals, comparisons and significance caveats |
| `scientific-visualization` | Quantitative plot design and scientific readability |
| `agent-figure-gallery` | Figure layout/reference patterns, not data or evidence |
| `nature-figure` | Scientific figure composition and styling; inspect its locally modified content without overwriting it |
| `scientific-figure-making` | Vector, reproducible technical figures |
| `scipilot-figure-skill` | Scientific diagram guidance where useful |
| `plot-from-data` | Reproducible plots grounded in saved metrics and arrays |
| `plot-from-image` | Only if a real supplied visual reference genuinely needs reconstruction; never invent/tracing data |
| `latex-paper-en` | Academic report, mathematical typography, bibliography and layout |
| `scientific-writing` | Clear research narrative, evidence, limitations and critical interpretation |
| `markdown-mermaid-writing` | GitHub-compatible workflow diagrams and explanatory docs |
| `pymc` | Conditional only if the chosen method actually involves Bayesian modeling; not a PCA/LDA requirement |

   If tools such as `latex:latex-compile`, `pdf:pdf` or computer-use are installed, inspect/use them for compilation, PDF verification and allowed publication interactions as appropriate. Otherwise use available equivalent tools.
4. Maintain a truthful `docs/ai_usage.md`: the actual task file names, noteworthy exact commands/search queries, skills **actually consulted**, their specific contributions, debugging/revision steps and outcomes. Never reconstruct fictional interactions.

## B. Research a genuine recent PCA/LDA algorithm (mandatory before architecture choice)

1. Search credible **primary literature**, strongly favoring **2024–2026 original peer-reviewed research**; consider 2022–2023 only when convincingly justified. Use older foundational sources to explain the mathematics, **not** as evidence that an unchanged older algorithm is recent. Search suitable families such as:
   - robust/sparse/structured PCA for images;
   - two-dimensional, tensor, kernel, incremental, randomized or graph-regularized PCA;
   - regularized, local, graph-based, sparse, kernel or matrix/tensor LDA;
   - discriminative subspace methods explicitly grounded in PCA/LDA.
2. These are search directions **not preselected algorithms**. Do not mislabel ordinary PCA/LDA used as preprocessing as a recent algorithm. Confirm the selected paper contributes a substantive methodological change.
3. Verify paper metadata and obtain the algorithm's objective, constraints, optimization/solver, derivation, datasets, baseline protocol and known limitations from the actual source. If a paper is not accessible or verifiable, do not invent its details.
4. Assess **at least three independently verified credible candidates if available** (do not fabricate candidates to fill a quota), using a concise comparison matrix:
   - publication year and venue;
   - defining novelty relative to classical PCA/LDA;
   - image-recognition/vision relevance;
   - required mathematics and computational complexity;
   - dataset/licensing availability;
   - implementability and feasible experimental depth on available hardware;
   - meaningful baselines and ablations.
5. Select the strongest **defensible and executable** candidate autonomously **only after passing Section B2**. Explain why it is better for this assignment than alternatives. If the selected work is older than your target recency range, state why and never claim it to be newer.
6. Decide whether the main task will be **classification, subspace learning, reconstruction, clustering support, or another directly evaluated vision task**. All evaluations must match the chosen claim.
7. Save research notes, verified references, links and decision rationale in `docs/research.md`; use a real `.bib` file in the report.
8. Keep the selected method's scope scientifically honest: an educational adaptation is not an official reproduction unless it faithfully matches the source paper's protocol.

## B2. MANDATORY Algorithm Selection Gate — pass before full implementation

This is a **hard stage gate**, not a narrative paragraph added after the fact. Create `docs/algorithm_selection.md` **before** implementing the main system. Keep dated evidence of the actual search and decision. Do not request the student to manually choose between ordinary technically feasible options; select using the standards below.

### 1. Hard eligibility tests (each must PASS)

For each candidate, verify and record:

- **Direct requirement match:** A substantive new/revised PCA or LDA **objective, constraint, solver, mathematical framework or theoretically grounded variant** is central to the method. Merely passing a pretrained embedding through sklearn PCA does not qualify as a recent PCA/LDA algorithm.
- **Verified recentness:** Prefer **2024–2026 peer-reviewed primary research**. A reputable 2022–2023 paper is an exception requiring a specific explanation of why the recent alternatives are less suitable. Foundational PCA/LDA papers may be cited as foundations but not presented as recent discoveries.
- **Vision/pattern-recognition relevance:** The paper or the implemented experiment gives a direct, defensible image/vision/pattern-recognition application. Dataset suitability must be grounded, not assumed from a generic method name.
- **Mathematical specificity:** Obtain and understand the method-defining objective, key derivation, update/eigenproblem, constraints and convergence/termination rules. Distinguish exact derivations from approximation or heuristic procedures.
- **Implementability:** Have enough primary-source detail to implement the defining algorithm **correctly** in Python. Inspect the official reference code if available, record its license, and independently check the resulting mathematics rather than blindly copying code. If the paper or solver cannot be reconstructed reliably, reject the candidate.
- **Controlled scientific evaluation:** Obtain legitimate data and a matched classical PCA/LDA baseline, clear metrics and at least one meaningful sensitivity/ablation or robustness experiment.
- **Compute and timing feasibility:** Given the actually observed runtime/hardware and assignment schedule, the experiment must be runnable and auditable with a safe margin for retries, analysis and PDF refinement.

Any **FAIL** on direct relevance, verifiable source, implementability or viable evaluation disqualifies a candidate. Record uncertainty transparently; do not guess missing paper details.

### 2. Comparative suitability matrix

For **at least three verified candidates where available**, create a matrix with source URL, publication year/venue, algorithmic contribution, vision task, dataset and official implementation availability, mathematics, solver type, time/memory complexity, important limitations and risk. Use the following **internal assessment factors**, with scores 1–5 supported by explanations:

| Factor | Indicative decision weight | Evidence that should influence the judgment |
| --- | ---: | --- |
| Recent publication (strongly 2024–2026) | 15% | Verified primary paper date and whether the *algorithmic change* is recent |
| Genuine PCA/LDA methodological contribution | 20% | Distinct objective/constraints/solver and convincing link to PCA/LDA |
| Implementation and numerical feasibility | 20% | Accessible method details/reference code, solvability, stability, practical compute |
| Quality of experiments and baseline fairness | 20% | Suitable datasets, matched comparisons, valid controls and meaningful uncertainty |
| Mathematical depth and independent verifiability | 15% | Derivations, checkable toy example, eigensystem/solver tests |
| Evidence-grounded figures and report explainability | 10% | Real visual questions, readable plots, interpretable results |

These percentages are **decision aids invented for this project**, **NOT** official grading weights or guaranteed grade predictors. The winner is not simply the highest unqualified weighted sum: apply all hard eligibility criteria first, examine robustness of the ranking, and explain trade-offs. Favor a method that can be thoroughly and correctly evaluated over a flashy but fragile method.

### 3. Candidate discovery guidance (not a preselected answer)

As promising starting leads, **independently verify** the published method, exact title/year, mathematical details and code availability of:

- a 2025 **robust sparse smooth PCA** approach for image/face analysis (RSSPCA, if the claimed paper/source is verified);
- a 2024 **robust and sparse LDA** approach (if the paper's primary source and complete solver are accessible);
- at least one additional credible **2024–2026** PCA/LDA variant discovered through actual literature search.

These are **search leads**, not facts to be copied unverified and not mandatory final choices. Search more broadly when stronger candidates appear. Avoid a 2021–2022 classic simply because it is easiest to code.

### 4. Small technical feasibility proof before the full experiment

Before locking the method, execute all of the following **without using the final test partition**:

1. Derive/implement the **method-defining** numerical step on a tiny synthetic or training-only problem. Verify dimensions, objective/eigenpair residuals, invariants, updates or convergence, as applicable.
2. Compare that step with an analytic toy example, independent numeric calculation or available reference implementation under a fair, clearly documented small setting.
3. Load the intended dataset through a **training-only** smoke test; verify licensing/provenance, matrix size, class structure, split feasibility and required compute/memory.
4. Run at least one classical PCA/LDA baseline through the intended downstream evaluator on training/validation data only; verify that the experiment can distinguish methods without leakage.
5. Record technical blockers and acceptable adaptations, then either PASS the method or reject it and evaluate the next-best candidate.

Do not re-use this feasibility test as the held-out final evaluation. If there is no viable candidate, search further, and report a blocker only after serious alternatives have been exhausted.

### 5. Decision lock and audit artifact

After a candidate passes, produce `docs/algorithm_selection.md` containing:

- exact chosen paper, verified DOI/URL, year, venue, algorithm and code-license information;
- the hard-gate results and the comparative suitability matrix;
- **why chosen over at least two viable alternatives** (when available);
- the method's specific mathematical contribution and what the project will **not** claim;
- any project adaptation and risk mitigation;
- the feasibility-proof command(s), observed outputs and pass/fail evidence;
- proposed dataset, baselines, experimental questions and figure opportunities;
- an unambiguous **selection-locked-before-final-test** decision record.

The report's Section 1 must summarize these true decisions and cite prompt excerpts and real search queries. Keep the full comparison and feasibility evidence in the repository.

**Proceed to Section C and full implementation only after this gate is satisfied.**

## C. Design a rigorous and computationally feasible study

After passing Section B2 and **before substantial coding**, write `docs/study_design.md` with the following **pre-execution decisions**, consistent with the locked algorithm and the feasibility proof.

### Dataset and leakage controls

- Select a credible, documented public image or visual-pattern dataset with appropriate usage rights. Match dimensionality and labels to the algorithm; use more than one dataset only when it provides meaningful extra evidence and is feasible.
- Describe exact dataset variant/source, size, classes, image resolution, preprocessing and original recommended protocol.
- Prefer official train/validation/test partitions if available. Otherwise perform a reproducible stratified/grouped split and preserve split indices; use group/writer/subject isolation where the task requires it.
- Fit centering, normalization, SVD/PCA, LDA, kernels, graph structures, dimensionality choices, feature selection and classifiers only on training data (with validation-based selection). Never fit on all images before splitting.
- Keep final test data inaccessible for choosing methods, components, hyperparameters, figures or optimization decisions.
- Record deterministic seeds and exact split counts. Handle repeated observations, class imbalance and domain shift honestly.

### Questions, baselines and metrics

Define 2–4 specific, measurable study questions such as:
- Does the selected recent PCA/LDA variant improve recognition or projection quality relative to conventional PCA/LDA under a matched downstream classifier?
- How do subspace dimension, regularization or neighborhood hyperparameters affect the result?
- What accuracy/quality vs runtime/memory trade-off results from the proposed approach?
- Which classes, images or regimes benefit, and where does the method fail?

Specify only meaningful comparators:
- an untransformed feature or simple evaluator baseline where informative;
- **classical PCA and/or classical LDA** with methodologically sound solver/regularization;
- the selected recent method;
- one controlled ablation or alternative variant that isolates a key mechanism.

Use **the same splits, preprocessing policies, dimension budget, downstream evaluator, selection procedure and evaluation metrics wherever comparability permits**; explicitly disclose unavoidable asymmetries.

Choose metrics by task. For classification, consider accuracy, balanced accuracy, macro-F1, confusion matrices, per-class results and training/inference time. For reconstruction, consider normalized image MSE/PSNR/SSIM when well-defined. For PCA-style embeddings, consider explained variance, reconstruction error, class separation, trustworthiness or downstream classifier performance as applicable. Do not force inappropriate metrics.

Use validation-selected hyperparameters and repeated seeds/splits where meaningful. Distinguish:
- retraining or random-seed variability;
- dataset split uncertainty;
- bootstrap uncertainty for a fixed held-out test set;
- solver randomness;
- statistical significance.

Predefine honest comparison, timing and plotting protocols before looking at final test outcomes. Do not artificially manufacture significance or overclaim generality.

## D. Mathematical derivation and verification — unusually thorough

The report must go beyond a textbook overview. Depending on the selected algorithm, develop the **actual method used**, with:

1. Problem setting, symbols, array shapes and assumptions.
2. Classical PCA/LDA foundations **as needed**, including covariance/SVD or within-/between-class scatter, generalized eigenproblems, rank and dimension bounds.
3. The selected recent method's explicit objective function and constraints.
4. A **step-by-step derivation** of its solver, updates, eigenproblem, kernel transformation, regularization or optimization procedure as applicable.
5. Mathematical explanations of each modification compared with baseline PCA/LDA.
6. A numerical toy example or simple analytically checkable special case, validated independently.
7. Complexity, memory footprint, numerical conditioning and convergence properties where justified.
8. A precise equation-to-code mapping and shapes/normalization checks.
9. Limitations and conditions under which the method is expected to help or fail.

Check nontrivial formulas using independent derivation, finite differences, SymPy or numerical reference calculations where appropriate; avoid claims that cannot be verified. Address arbitrary eigenvector sign, eigenvalue degeneracy, label leakage and singular scatter matrices when applicable. Include theorem or optimality claims only when their actual assumptions are met.

## E. Implement and **run** the project

Create a sensible maintainable project layout, rather than blindly pre-creating empty modules. Typical areas:

- `src/` — actual method, baselines, data, evaluation and plotting logic;
- `configs/` — exact protocol;
- `scripts/` — runnable entry points and reproduction;
- `tests/` — numerical and pipeline tests;
- `results/` — evidence, split indices, metrics, figures, selected artifacts;
- `docs/` — research, study design, AI-use evidence, method/decision notes;
- `report/` — LaTeX, bibliography and compiled PDF.

Use NumPy/SciPy/scikit-learn and PyTorch only as justified. Do not simply wrap a built-in estimator and relabel it as an original implementation if the assignment expects implementation of the chosen algorithm. Implement and validate the selected method's distinctive computations while using established libraries for standard linear algebra.

### Mandatory checks

- Verify algorithm dimensions, centering, label alignment and data partition non-overlap.
- Verify eigenpair/generalized eigenpair residuals and invariants as applicable.
- Test small synthetic cases, numerical edge cases, ill-conditioned settings and deterministic reruns.
- Check reference classical PCA/LDA against independent library behavior on compatible toy cases.
- Test negative/degenerate input behavior, checkpoint/artifact serialization if needed, and the full evaluation path.
- Run a tiny end-to-end smoke test **before** the full experiment.
- Log exact device actually used, dependencies, seeds, settings, wall-clock method and result provenance.

### Mandatory execution

1. Execute all preplanned baselines and main experiments.
2. Validate and lock model/hyperparameter selection.
3. Only then evaluate the final held-out test set.
4. Save per-run and aggregated metrics, labels/predictions where relevant, component/eigenvalue summaries, selected parameters and runtime evidence.
5. Run at least one controlled ablation or dimension/parameter sensitivity study where computationally realistic.
6. Distinguish exploratory/post hoc analyses clearly, and never retune based on final test scores.
7. Recompute results from saved artifacts and test reproducibility. Preserve honest negative results.

## F. Figures: premium scientific presentation, not decorative graphics

**Figure quality is a major acceptance gate.** Earlier Assignment #1 feedback identified inadequate detail and weak graphs; Assignment #2 achieved substantially better mathematical explanations and evidence-based visuals.

First design a **figure plan**, with each figure's question, exact evidence inputs, intended panel structure and report placement. Use `scientific-visualization`, `plot-from-data`, `nature-figure`, `agent-figure-gallery` and other pertinent skills as **design/implementation guidance**. Gallery images are stylistic references, never experimental evidence.

Choose a coherent set of **approximately 6–10 meaningful figures when supported**, such as:

1. **Instruction-to-AI-execution workflow diagram**: assignment requirements → `AGENTS.md` + verbatim task prompts → Codex + applied skills → literature search/candidate comparison → implementation/validation → experiments/report → critical review/publication.
2. **Selected algorithm schematic**: mathematically faithful stages of the actual PCA/LDA variant, from input images to projection/eigenspace to predicted class or reconstructed image.
3. **Dataset evidence**: class distribution, representative fixed-index images and honest split details.
4. **Eigen/subspace structure**: scree or component spectrum, retained dimensionality or explained variance **only if defined for this algorithm**.
5. **Embedding/feature visualization**: 2D/3D class structure or basis/eigenimage examples with explicit projection provenance; no invented separability or t-SNE parameter inference.
6. **Baseline comparison**: method vs matched PCA/LDA controls with per-run points, variability and appropriate baseline labeling.
7. **Dimension/hyperparameter sensitivity**: accuracy/quality, runtime or error vs selected dimension/regularization.
8. **Class-level results**: confusion matrix and per-class effects for recognition tasks.
9. **Ablation and cost trade-off**: isolate the algorithm's contribution and report cost or memory when supported.
10. **Qualitative outcomes/failure cases**: fixed-index genuine examples, reconstructions or misclassifications where meaningful.

Only retain figures that actually help answer a study question. Fewer excellent figures are better than ten redundant ones.

### Enforce final-page scientific graphics standards

- Data-generated, reproducible; source arrays, script and config must be archived.
- Prefer vector PDF/SVG plots and diagrams; raster images at effective ~300 dpi where needed.
- Use consistent scientifically appropriate palettes, colorblind-conscious contrast, clear axes/units/legends, readable mathematical notation and thoughtful multi-panel design.
- At final page size, text should normally remain approximately **8–10 pt or larger**; avoid microscopic legends and overcrowded subplots.
- Don't truncate axes misleadingly, suppress unfavorable data, hide outliers or misrepresent error bars.
- Do not use error bars outside a physically valid range without explicit justification; prefer observed points/min–max or suitable intervals.
- For subspace visualizations, state scaling/centering, random seed, class labels and selection policy.
- Caption every plot with what was measured, dataset/protocol, sample or run count, interpretation and uncertainty definition.
- Avoid near-empty pages, huge whitespace, clipped labels, bitmap-blurry plots, broken fonts or a figure not discussed in the text.

Generate **actual vector diagrams** for the report, not a screenshot of a Markdown diagram. Use TikZ/Graphviz/SVG-to-PDF when appropriate. Keep compatible Mermaid sources for GitHub if useful.

## G. Produce a detailed, self-contained LaTeX report

Make it technically strong enough to be judged **without opening GitHub**. Aim for a rigorous, coherent report; a typical target is around **12–18 pages if the instructor sets no length cap**, but depth and clarity outrank page count.

The title area must include:
- **CISC3024 — Pattern Recognition**
- **AI Assignment #3**
- **Paco, Sou Chak Tong**
- **U-C3-2652-3**

Follow the instructor's six requirements as primary headings:

1. **How AI Found the Algorithm**
2. **Algorithm Description**
3. **How AI Implemented the Algorithm**
4. **Experiment Settings and Results**
5. **What I Have Learnt from This AI Assignment**
6. **Webpage Link of the Source Codes**

Also include an abstract, conclusions, verified references and optional appendix where appropriate.

### Mandatory detail in "How AI Found the Algorithm"

This section must be **self-contained**, unlike the first version of Assignment #2:

- Explain your input materials (assignment PDF, `AGENTS.md`, staged Codex prompt files, relevant skills) and why these were separated.
- Include **two to four short, exact, verified verbatim excerpts** from the actual `AGENTS.md`/stage prompts **with filenames**, not paraphrases disguised as quotes.
- For each excerpt, describe its objective and **actual observed effect** (searches, candidate comparison, methodological choices or validation actions).
- Present the **actual search-query strings and verified paper candidates**, selection criteria and defensible final selection.
- Include the mandatory **AI instruction/execution workflow diagram** and explain it in the surrounding text.
- Explain how skills were applied, not just listed. Never claim a skill was used solely because it was installed.
- Preserve full original instructions in the repository as supplementary evidence, while including enough in the PDF for an examiner to understand the interactions.
- Avoid irrelevant computer-directory history, invented chat transcripts or exaggerated claims of independent review.

### Other required report content

- Explain the method with derivations, notation, a worked example, pseudocode, computational cost and a mapping to code.
- Explain actual data sources/splits, baselines, tuning constraints, environment and detailed experimental settings.
- Include rigorous quantitative tables, explanatory figures, sensitivity/ablation results, strengths, failures and limitations.
- Explain **why** each finding is observed, distinguishing measured evidence from plausible mechanism.
- Document tests, integrity checks and reproducibility.
- Keep final GitHub URL unresolved until genuinely published; do not invent it.
- Leave a clear placeholder for **student-authored reflection**. Do **not** write or fabricate learning experiences.
- Avoid copying paper prose; accurately cite all borrowed information and figures.

### PDF verification

Compile LaTeX (using actual installed toolchain). Inspect every rendered page in order. Check equations, fonts, tables, float placement, clipping, page breaks, figure sizes, labels, links and references. Fix formatting and rerun until no evident defects remain. Save both `.tex` and final `.pdf`.

## H. GitHub-compatible documentation in parallel

Create a real `README.md`, `docs/` content and optional `docs/wiki/` sources. Mathematics in GitHub Markdown must use:

- inline `$x^\top Sx$`;
- display `$$ ... $$` on separate lines; or
- fenced `math` code blocks.

Do not paste LaTeX's `equation` environments into Markdown and assume GitHub will render them. For the PDF use proper LaTeX math environments separately. Use relative links, correct case-sensitive paths and GitHub-renderable Mermaid where applicable.

Publish only in Prompt 03, after independent-style review; mark staged content as **not yet published**.

## I. Completion evidence and handoff

Prompt 01 is complete only when:
- a verified recent PCA/LDA method has been selected and justified;
- `docs/algorithm_selection.md` records a passed recency/substance/feasibility gate and its pre-implementation numerical prototype;
- the code actually executes;
- meaningful classical baselines and the main method have been compared;
- the final test protocol has been respected;
- results/figures and detailed math exist;
- meaningful tests and reproduction checks run;
- a technically detailed initial PDF is compiled and visually checked;
- AI prompt excerpts and the workflow diagram appear in the PDF;
- student reflection remains a conspicuous placeholder;
- GitHub URL remains pending until truly published.

Report concise facts: method + papers, dataset, split, actual settings, measured results, ablations, figure inventory, tests, PDF path and blockers. Do not claim 100/100 or production-level correctness without evidence. Proceed autonomously through the entire stage.
