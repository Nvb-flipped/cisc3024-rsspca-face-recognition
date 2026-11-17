# Prompt 02 — Independent-Style Technical Review, Mathematical Audit and Figure Refinement

Read `AGENTS.md`, `AIassign3.pdf`, Prompt 01, the current source code/configs, saved experimental evidence, AI-use log and **every page of the compiled report**.

**Your role:** act as a meticulous external-examiner-style critic of the **existing** Assignment #3 work. This is a self-audit by the same AI unless an actually independent reviewer is used; do not label it independent peer review.

The goal is to address the previous Assignment #1 feedback ("all correct, but could have more details and graphs were not excellent") **before submission**. Preserve factual integrity and valuable negative findings.

## Face-primary scope (mandatory addendum to this existing review)

Read and independently review `prompts/01B_FACE_PRIMARY_MIGRATION.md`, `docs/face_pivot_decision.md` and `docs/face_study_design.md` before evaluating the new report. This is **not a new project from scratch**. Distinguish the original *locked* digit results from the new *locked* face evaluation; verify there was no cross-experiment result rewriting, and that the date/order of the human-directed pivot is accurately reported. Verify Olivetti or other face dataset source, usage conditions, image sizes, resolution/resampling, identity-stratified closed-set split, no held-out leakage, training-only tuning, and per-subject sample limitations. Recheck the general RSSPCA grid Laplacian, scaled numerical solves, run-time evidence and mathematically sound reconstruction with nonorthogonal directions. Evaluate whether new figures genuinely explain face structure, sparsity/smoothness and robustness, instead of repeating the digit report's graph family. Require correct face-report methods, ablations, figure captions, and honest negatives. If the feasibility gate failed, do not pretend a successful face study exists; review the preserved digit fallback instead.
## 1. Build a traceable assignment audit

Map each of the instructor's six items to actual pages/sections, with concrete evidence:

1. how the student instructed AI to find a **recent PCA/LDA algorithm**;
2. algorithm description and mathematical derivation;
3. AI implementation, source modules and verification;
4. actual experimental setup, results and interpretations;
5. student-authored learning reflection or explicit pending placeholder;
6. a working public source-code URL or explicit **not yet published** status.

Distinguish **requirements already passed**, missing deliverables, visual weaknesses and optional enhancements. Do not allow a mathematically strong report to compensate for a missing mandatory item.

## 2. Independently challenge the algorithm-selection gate and mathematics

Before reviewing equations, read `docs/algorithm_selection.md`. Check whether the **hard-gate evidence existed before the main implementation** (rather than being retrofitted after experiments). Reopen the selected primary paper and at least two cited alternatives when accessible; independently verify original publication year/venue, what is actually novel, PCA/LDA centrality, the claimed application, the selected solver and limitations.

- Was the 2024–2026 recency preference satisfied? If an older method was chosen, was the comparative justification specific and persuasive, without pretending a classical algorithm is new?
- Were **at least three** credible candidates compared where available, with honest limitations? Were original paper citations and official-code/license claims verified?
- Was difficulty substantive but technically justified, rather than impressive-sounding only? Could the selected method's mathematical core truly be checked and explained?
- Did the method-defining feasibility proof actually run before full experiments, and are its commands/results verifiable?
- Were alternative methods rejected for documented constraints, not because the selected test result looked favorable?
- Is the comparison/suitability matrix labeled as a **project decision aid**, not an official professor rubric?

Any failure of **recent method, real PCA/LDA contribution or mathematical implementability** is a **critical issue**, even if the report has attractive graphs. If necessary, repair selection and execution with a new justified method and a fresh, leakage-free study; do not silently relabel a weak choice.

Now review the mathematics:

- Confirm the selected primary paper really proposes or materially develops a PCA/LDA method; verify year, venue, DOI/URL and vision relevance.
- Verify that all changes from conventional PCA/LDA and all differences from the cited paper are honestly explained.
- Independently check each major equation against implemented code and/or derivation. Check shapes, centering, scatter matrices, symmetry, rank limits, eigenvalue ordering, feature normalization, sign conventions, regularization and numerical stability as applicable.
- Independently test analytic results on toy problems and numerical residuals; validate no method-defining mathematics were merely asserted.
- Flag oversimplified proof claims, ambiguously defined symbols, unsupported novelty claims and leakage risks.
- Ensure a worked example, executable pseudocode and a **genuine equation-to-code mapping** are present.

## 3. Adversarially audit experiment logic

Check:
- train/validation/test integrity and all fitted transformations;
- baseline fairness (same split, class information restrictions, component budgets and downstream evaluation);
- algorithm/parameter selection made before final test;
- test leakage through error-analysis-based retuning;
- random seeds and repeat counts;
- correct denominators and uncertainty semantics;
- meaningful ablations/controls;
- saved metric equivalence to reported tables and figures;
- run artifacts and environment claims;
- numerical reproducibility, including source/config hashes where practical.

**Do not rerun and retune models just because a test result seems disappointing.** Only correct actual bugs or protocol errors; disclose their effects and regenerate all affected evidence when necessary.

If you discover a data-leak or invalid protocol, repair it and rerun necessary experiments from clean selections, honestly documenting the correction. Do not quietly rewrite historical outputs.

## 4. Upgrade explanations: details with analytical value

Critique every report section for missing rationale, not just missing text. Especially strengthen:

- the verified **prompt engineering story**: precise verbatim excerpt(s), filename, effect, search string and selection;
- the comparison of at least three literature candidates when feasible;
- why the selected algorithm is appropriate and sufficiently recent;
- derivations of the nontrivial objective/solver and any assumptions;
- the worked numerical example and how it maps to code;
- subtle PCA/LDA issues (eigenvector sign, rank, class dimensionality, scatter singularity, centering, kernel interpretation as applicable);
- experiment matching, uncertainties and causal boundaries;
- interpretation of failures and negative results;
- computational complexity, runtime/memory and limitations.

Do **not** repeat the same explanation across Sections 1, 2 and 3; use cross-references and precise tables.

## 5. Rework the scientific graphics, not just colors

Load actual saved figure source/data and use relevant skills:
`scientific-visualization`, `agent-figure-gallery`, `nature-figure`, `plot-from-data`, `scientific-figure-making`, `scipilot-figure-skill` and other applicable installed guidance.

For **each existing figure**, record:
- research question answered;
- exact source data and plotted population;
- axes, scales and units;
- encoding choices;
- uncertainty definition;
- any misleading visual inference;
- legibility at rendered PDF size;
- link to report argument.

### Concrete design acceptance gates

- Prefer reproducible vector plots/diagrams; no screenshots of code or low-resolution plots.
- Font labels/legends must be readable at normal 100% PDF viewing, not only when zoomed.
- Visually balance multi-panel plots; avoid tiny isolated figures surrounded by giant whitespace.
- Use consistent panel labels, color palette, margins, legend placement and typographic hierarchy.
- Verify scientific accuracy of error bars, normalization, negative/positive ranges, colors, baselines and annotations.
- If samples are shown, specify deterministic indices and selection policy. Avoid cherry-picking only successful cases.
- Check captions independently: they should say what was plotted, how generated, and what the figure demonstrates without overstating causality.
- If a method-comparison scatterplot or projection graph appears, disclose projection construction and label information; never secretly use test labels during model selection.
- Make the graph family coherent across the report: opening workflow, algorithm schematic, dataset, spectrum/embedding, primary results, sensitivity, class-level performance and failure cases as appropriate.
- Keep **meaningful** detail; remove redundant panels and decorative visuals.

A reader should be able to interpret each figure without having to open the source code.

## 6. Mandatory diagram and PDF prompt evidence audit

Confirm that **Section 1 contains**:
- the human requirements → persistent rules → staged prompts → applicable skills → actual Codex activity → algorithm search/selection → implementation/experiments → refinement → verified outputs diagram;
- 2–4 **verbatim and source-verified** prompt excerpts, filenames and concise impact explanations;
- actual literature search queries and algorithms considered.

If missing, create them now. Make diagram publication quality (TikZ, SVG/PDF vector or Graphviz), with accurate arrows and no false claims of completed publication. Rebuild the PDF.

For the **algorithm diagram**, ensure every arrow and computation matches what code actually performs.

## 7. Read the compiled PDF, page by page

Perform a rendered-page inspection, preferably contact-sheet first and high-resolution pages for suspect regions. Check:

- text clipping, float overflow, math symbols, broken fonts and missing characters;
- visually balanced pages and sensible figure sizes;
- inconsistent whitespace, table density and figure-caption spacing;
- legible equations and references;
- hyperlinks and bibliography;
- page counts/TOC consistency;
- whether the report can stand alone for a grader who never opens GitHub.

A successful compilation is **not** visual QA. Fix the problems and re-render/recheck the pages. Do not require an arbitrary page count. Prioritize substance and reader understanding.

## 8. Independent-minded review report and fixes

Create `docs/quality_review.md` with:

- requirement coverage table including a **recency/algorithm-difficulty/feasibility gate** assessment;
- high/medium/low issues with exact affected file/page;
- observed tests/evidence;
- repairs performed;
- findings deliberately not changed (negative outcomes, limitations);
- any unresolved blockers, such as reflection or public GitHub publication.

Ensure the final local code, plots, metrics, report and documented commands remain synchronized. Rerun all affected tests/audits and regenerate PDF from source.

Do not edit the student's own reflection if already provided; otherwise leave its placeholder.

**Completion condition:** There should be no remaining demonstrable high-severity correctness or presentation defect. GitHub publication belongs to Prompt 03. Never invent a full-marks assurance or claim independent third-party review that did not occur.
