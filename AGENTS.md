# AGENTS.md

## Project identity

- **Course:** CISC3024 — Pattern Recognition
- **Assignment:** AI Assignment #3 (November 2026)
- **Student:** Paco, Sou Chak Tong
- **Student ID:** U-C3-2652-3
- **Topic:** **RSSPCA (Wang et al., 2025)**, selected and implemented in Prompt 01; Prompt 01B explores a documented *primary face-recognition* application pivot, preserving the completed Optdigits study. A feasibility gate must pass before the face-study conclusions replace the digit-based primary report.
- **Submission:** A self-contained LaTeX-compiled PDF report containing a verified link to a public GitHub source-code repository.

The agent performs the technical work (literature search, design, code, experiments, visualizations, documentation, compilation, testing and publication). The student's personal learning reflection must be authored by the student, not invented by the agent.

## Source of truth and instruction priority

1. The original `AIassign3.pdf` and any direct instructor clarification.
2. This `AGENTS.md` for persistent repository-wide standards.
3. The current stage prompt in `prompts/` (Prompt 01B is a documented post-Prompt-01 pivot and must not rewrite the original research timeline).
4. Relevant installed skills and their supporting references.

Read the real assignment PDF before making project decisions. Distinguish instructor requirements from additional project quality goals. Never claim a full-mark grade is guaranteed.

## Research and algorithm constraints

- Select a verifiable recent, substantive **PCA and/or LDA algorithm** that is central to the method, not merely an incidental preprocessing step.
- Use primary papers, official implementations/documentation and reliable dataset sources; verify titles, years, venues and URLs/DOIs.
- Explain exactly how the selected method differs from classical PCA/LDA and which pieces are adapted for this project.
- Strongly prefer a **verifiable original, peer-reviewed 2024–2026** methodological contribution. A 2022–2023 paper may be used only with a specific comparative justification; an older foundational method alone does **not** satisfy the recency goal. Never disguise a recent application of unchanged classical PCA/LDA as a newly developed algorithm.
- Never fabricate references, unobserved literature searches, AI interactions, experimental data or claims of novelty.

## Mandatory algorithm-selection gate

**Do not start the main implementation merely because a paper sounds advanced.** Prompt 01 must carry out and record a formal selection gate first.

- Investigate at least **three** credible primary research candidates when the available literature permits; verify paper dates, actual PCA/LDA contribution, methodology and vision application.
- Evaluate **recency, centrality of PCA/LDA, mathematical substance, accessible algorithmic details, implementation risk, feasibility on observed hardware, fair baseline experiments, and data-driven figure potential**.
- Use a transparent documented **candidate suitability matrix**, with any numerical weights labeled as **self-imposed decision guidance, never an instructor rubric**.
- Reject methods that are not genuinely PCA/LDA-based, cannot be described and mathematically implemented from verifiable sources, cannot be fairly evaluated, or are infeasible under the actual assignment timeframe/hardware.
- Before full experiments, require a small independent mathematical or numerical **feasibility prototype** of the method-defining step, plus a baseline/dataset smoke test. Do not consult the final test set during this gate.
- Select the strongest **verified balance** of academic relevance, recentness, technical sophistication, numerical correctness, experimental depth, and report explainability. Do not automatically select the newest or hardest algorithm.
- Lock and record the chosen algorithm, paper, deviations, dataset protocol, evaluation questions and baseline plan **before the held-out final test**. Later changes for genuine correctness defects must be logged and scientifically reconciled.
- If no candidate passes the essential conditions, continue the search or report a genuine blocker; do not silently substitute a basic PCA/LDA tutorial or make false claims of recency.

## Preservation of completed work and face pivot

- Preserve all existing digit-experiment evidence and its selection/test history. Do not silently retune or erase results.
- The primary face experiment is a **new predeclared study** requiring its own split/parameter lock before viewing face test outcomes; it does not retroactively alter the original experiment.
- Preserve the verified RSSPCA numerical core, refactoring only as necessary for image size and data protocol. Run an early face feasibility gate before full execution.
- Treat close-set face identity classification precisely, verify permissible image usage, and correctly handle nonorthogonal subspaces in any reconstruction analysis.

## Scientific methodology

- Select an appropriate real computer-vision/pattern-recognition dataset and document provenance and usage terms.
- Isolate train/validation/final-test data; fit preprocessing, dimensionality reduction, feature selection and model selection using training/validation data only.
- Never select algorithms, hyperparameters, figure examples or conclusions by repeatedly consulting the final test set.
- Use matched, meaningful classical PCA/LDA baselines and downstream evaluators appropriate to the task.
- Prefer controlled ablations, repeated seeds/splits, meaningful uncertainty summaries and failure analysis when feasible.
- Preserve seeds, split indices, configuration, metrics, figures, provenance and enough artifacts to reproduce results.
- Results and hardware/runtime claims must come from actual execution, not estimates disguised as measurements.

## Mathematics and correctness

- Define every symbol and assumption. Give substantive derivations of the chosen PCA/LDA method, not just textbook equations.
- Verify numerical linear algebra, dimensions, normalization, eigensystems, rank limits, symmetry/PSD conditions where applicable, and solver behavior.
- Use independent analytic, symbolic or small numerical checks for nontrivial equations; distinguish mathematically exact steps from approximations.
- Handle numerical instability, degenerate eigenvalues, arbitrary eigenvector signs, rank deficiency and leakage explicitly as relevant.
- Do not claim general superiority without matched evidence.

## Source code and testing

- Use Python and suitable scientific tools (NumPy/SciPy/scikit-learn, PyTorch only when warranted).
- Keep source, configs, scripts, tests, results, figures, documentation and `report/` modular.
- Make authoritative workflows runnable non-interactively from the project root; do not rely on a notebook alone.
- Run meaningful unit, numerical, pipeline, reproduction and result-consistency checks.
- Fix root causes of failures; never suppress failing tests or invent successful runs.

## Figure and report standards

- Target technically rigorous, clear, well-edited undergraduate research quality: detailed enough to be self-contained, not inflated with filler.
- Select figures for scientific value; use evidence-grounded, aesthetically consistent, accessible, readable plots and diagrams.
- Prefer vector PDF/SVG for plots and diagrams; high-resolution raster for images. Keep source generation reproducible.
- Use descriptive captions, legible font sizes at **final printed page scale**, appropriate palettes/units/uncertainty, and honest axes.
- Compile the LaTeX PDF, render and visually inspect **every page**; correct clipping, white space, inconsistent typography, unreadable panels, broken glyphs and unsupported claims.
- Include **actual short verbatim prompt excerpts and an instruction-to-execution workflow diagram** in the PDF, not solely a link to prompts on GitHub.

## Mandatory report topics

The final report must cover all six instructor requirements:

1. How AI was asked to find the algorithm (with truthful interaction evidence).
2. Detailed algorithm description and mathematics.
3. How AI implemented and verified the algorithm.
4. Executed experiment settings, results and discussion.
5. What the student learnt from this AI assignment.
6. A working **public** source-code webpage link.

Include course, student name and ID exactly as listed above in the report title area.

The personal reflection is **student-authored**. Before it is provided, leave a conspicuous placeholder; once provided, preserve the student's intended meaning.

## GitHub and documentation

- Deliver a **public GitHub repository** with sources, executable scripts, dependency/environment instructions, verified results and report source plus final PDF.
- Make `README.md`, `docs/*.md` and wiki text valid **GitHub Flavored Markdown**.
- Use `$...$` for inline math and `$$...$$` or fenced `math` blocks for display math; do not assume LaTeX document environments render in GitHub Markdown.
- Mermaid diagrams are allowed only when they render correctly on GitHub; provide vector alternatives for the PDF.
- Prefer a populated public GitHub Wiki, but distinguish an actual published wiki from Markdown files merely staged under `docs/wiki/`.
- Do not commit API tokens, secrets, unnecessary large data/checkpoints, private paths, virtual environments or caches.
- Never invent a GitHub URL, published wiki, test pass, uploaded PDF or completed submission.

## Skill selection and provenance

Skills may initially reside in the **Assignment #2** folder. Locate their real `SKILL.md` and relevant references wherever they actually exist (project-local, specified Assignment #2 path or installed globally). Do not claim a skill was used if it was only installed or listed. Do not modify or overwrite the original Assignment #2 skills during reuse.

Prioritize relevant research, mathematical validation, experiment design, data analysis, figure construction, scientific writing and LaTeX skills. The detailed skills inventory and application plan are in Prompt 01; do not force every skill into every task.

## Completion standard

**Full marks are an aspiration, not an outcome the agent can guarantee.** Seek zero outstanding verifiable requirement defects; escalate only genuine external blockers such as authentication or unavailable services.

A "complete" status requires executed tests, evidence-backed results, visually inspected compiled PDF, student-authored reflection included, working public repository URL in the PDF, pushed final commit, and public/wiki checks where available. Otherwise report precisely what remains unfinished.
