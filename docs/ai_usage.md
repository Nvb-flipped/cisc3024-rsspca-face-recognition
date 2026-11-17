# AI use and execution evidence

Codex performed the technical work requested in the course handout, [AGENTS.md](../AGENTS.md) and [Prompt 01](../prompts/01_RESEARCH_IMPLEMENT_REPORT.md). The handout's six topics were preserved in the report. The student supplied the reflection. This record summarizes observed actions, with the [exact research queries](research.md) and a [dated decision lock](algorithm_selection.md) retained separately.

## Tools and skills

- **PDF** guided extraction and page-level rendering. PyMuPDF extracted the one-page assignment locally and was used to render the report for inspection.
- **Literature review** guided targeted discovery, full-text screening and DOI/title verification. **Mathbox computation audit** guided the independent rational solve, tested range and provenance. **Experimental design**, **exploratory data analysis**, **scikit-learn** and **statistical analysis** informed the writer-separated holdout, development data profile, training-only feature fits, common evaluator and descriptive paired analysis.
- **Scientific visualization**, locally modified **Nature Figure** and **Plot from Data** informed legible panels, color-plus-shape encodings, a single diverging scale for loadings, and reproducible vector exports. The gallery skill was inspected for applicability. Its workflow is for human-selected reference bundles. Figures here follow the autonomous figure plan and use experiment evidence and mathematical operations as inputs.
- **Scientific writing** and **English LaTeX paper** informed the evidence sequence, citations, limitations, section and equation organization. **Markdown and Mermaid** informed the GitHub workflow diagram and math formatting. **LaTeX compile** and **LaTeX doctor** were used for Tectonic detection, build and checks.
- Analytical method validation is tailored to regulated measurement procedures. The mathbox computation-audit skill covers the numerical linear algebra used here. Bayesian modeling and image-reference reconstruction were outside the study design.

Scientific Agent Skills guidance is acknowledged in the report bibliography. [Kassis et al., 2026](https://doi.org/10.48550/arXiv.2609.00065)

## Run chronology, 17 November 2026 (UTC+8)

| Step | Observed action and output |
| --- | --- |
| Read and audit | Extracted handout text with PyMuPDF. `git status --short --branch` and `git remote -v` found no local Git repository. GitHub CLI was present. Machine reported Windows 11, 16 logical processors, 34,192,162,816 bytes of RAM and an RTX 5060 Ti with 16,311 MiB reported by `nvidia-smi`. CPU only was used. |
| Primary verification | Read the PLOS and available journal/accepted manuscripts; checked Wang et al.'s MATLAB solver, Laplacian and classification scripts at the author repo. Screened four candidates. |
| Data acquisition | Initial sandboxed UCI request could not resolve the host. A network-enabled request acquired only `optdigits.tra`. |
| Gate | `python scripts/gate_probe.py data/optdigits.tra` generated the [gate evidence](../results/gate_probe.json). The gate and study documents were written at about 14:05 before the main implementation. |
| Smoke and tests | `python -m src.experiment smoke` evaluated all five estimators on an internal 300/50 split. Standard pytest collection hit a Windows DLL initialization error. The explicit launcher in the README loaded scikit-learn before pytest and collected all 10 tests successfully. The local Windows development commands set `LOKY_MAX_CPU_COUNT=1` after the unavailable wmic probe triggered a joblib fallback. |
| Selection and freeze | `python -m src.experiment tune` wrote `selection.json` at 14:09:51. `python -m src.experiment prepare` froze 165 condition/method/rank records at 14:10:00. |
| Final evaluation | After that freeze, `python -m src.experiment fetch-tes` wrote the official data file at 14:10:14. `python -m src.experiment final` wrote predictions and scores at 14:10:29. No final scores were used to update the locked models. |
| Replay and independent check | Repeated `tune`, `prepare`, and `final` under `results/reproduction`. Verification matched 165 arrays exactly. `python -m src.summarize` independently recomputed metrics against the official labels and audited splits and fold masks. |
| Figures and build | `python -m src.figures` exported seven figure pairs. LaTeX doctor found bundled Tectonic 0.17.0+20260731 and no installed TeX Live commands on PATH. The sandboxed smoke compile could not fetch its bundle index. A network-enabled smoke compile passed and the same bundled engine built the report. |
| PDF corrections and inspection | The initial table input raised a TeX alignment error. A generated row macro fixed it. Page renders exposed isolated floats and overflow paragraphs, and the figure audit detected legend text over gridlines. After layout revisions, all seven vector figures passed the collision and minimum text-size checks. PyMuPDF rendered the final ten pages for inspection in order. The final check verified the six headings, bounding margins, reference links and all figure captions. |

## Evidence files

Input provenance is in the [UCI data note](../data/README.md). [Selection](../results/selection.json) pins the protocol, development hash, environment and source hashes. [Frozen manifest](../results/frozen.json) pins the selected settings, development fits and recorded split/fit outputs. [Final records](../results/final.json) identify the test SHA-256 and contain each run, metric and prediction key. [Test log](../results/tests.txt), [repeatability check](../results/reproduction_check.json) and [consistency check](../results/consistency_check.txt) capture the executed checks.

The [PDF verification record](../results/report_check.json) identifies the inspected build and records its non-blocking engine diagnostics.

## Subsequent reviewer revision and Prompt 01B

The student first requested consistent Latin Modern typography and deeper reviewer detail. Codex compiled and inspected the expanded 14-page digit report with matching OpenType fonts, and saved it alongside the original 10-page report in the [Optdigits archive](../report/optdigits/README.md). The digit QA record above refers to the original build and its then-current path.

The student then made faces primary to distinguish the application from Assignment #2. Codex preserved the original result archive and initialized the local baseline and face branches. The separate [face decision and execution chronology](face_pivot_decision.md) includes the dataset provenance, numerical gate and dates of the lock and first test. The [face protocol](face_study_design.md) specifies the new comparisons. Experimental-design and computation-audit skills informed the closed-set split and independent solve checks. Scientific-visualization guidance informed the matched-scale face galleries, loading diagnostics and recognition/reconstruction figures. The expanded face PDF follows the same Latin Modern convention.

## Prompt 02 critical review

The student then requested examiner-style assessment of the frozen face study. Prompt 02 says, “Preserve factual integrity and valuable negative findings.” Codex used the academic-paper-reviewer guidance for internal mathematical, protocol and figure review passes. The computation-audit guidance informed an independent direct-distance and least-squares check. The Nature Figure and scientific-visualization guidance informed the signed loading grid, paired mask markers and stopping-threshold plot. English LaTeX, LaTeX compile and PDF guidance supported the revised report and rendered-page verification. This was a Codex self-audit.

The review reopened the selected source paper and primary sources for the alternatives, repeated both development probes, repeated the unit checks and replayed the face study in a fresh output directory. The original digit replay was verified separately. Codex corrected two inaccurate values in prose, documented baseline geometry and the published protocol differences, revised the instruction and algorithm diagrams and used saved traces to explain what the stopping criterion measures. [Review and repair record](quality_review.md) · [Executable archive audit](../scripts/review_face.py)

## Prompt 03 public release

The student supplied the reflection and initialized the repository's Wiki Home page. Codex published the verified studies and populated the eight Wiki pages. The public figure set shows the archived mask values and individual reconstruction errors in place of portrait examples. The earlier research commits and locally reproducible portrait galleries remain in the local project. The public Git history starts from the reviewed release snapshot.

An anonymous clone obtained both datasets from the documented sources, passed 13 tests, matched 143 face prediction arrays and 99 reconstruction-error arrays exactly, and verified 165 supplementary digit arrays. GitHub served the README, the mathematics and figure links, and all eight Wiki pages without authentication. The publication build includes active repository and Wiki links. [Public repository](https://github.com/Nvb-flipped/cisc3024-rsspca-face-recognition) · [Public Wiki](https://github.com/Nvb-flipped/cisc3024-rsspca-face-recognition/wiki) · [Report checks](../results/faces/publication_report_check.json)
