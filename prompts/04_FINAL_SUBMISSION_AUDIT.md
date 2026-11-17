# Prompt 04 — Final Full-Mark-Oriented AI Assignment #3 Submission Audit

Read `AGENTS.md`, the original `AIassign3.pdf`, every stage prompt, the **final** LaTeX/PDF report, the public GitHub repo (if published), saved experiment artifacts and the wiki (if published).

Treat yourself as a demanding CISC3024 examiner performing a complete **source + report + visualization + publication** audit. The user aims for full marks, but you must not guarantee a grade or invent an official marking rubric.

## Face-study transition audit (mandatory)

Read `prompts/01B_FACE_PRIMARY_MIGRATION.md` and verify its pass/fail evidence. Confirm the face study, if adopted, was an appropriately documented **later human-directed application change** with a fresh face-study design lock before final held-out evaluation; confirm original digit results remain traceable. Validate subject-stratified closed-set face identification, resizing assumptions, PCA/LDA dimension/rank limits, fair corruption masks, robust PCA mathematical equivalence and any valid reconstruction projection. Compare all face figures/results with machine-readable evidence and confirm that the final PDF contains a meaningful face-centric study, not a mislabeled digit report. If the face feasibility gate failed, assess the correctly disclosed digit fallback instead. Check the distinctiveness of graphical presentation without demanding artificial novelty.
## 1. Six-item compliance table — no omissions

Build a pass/fail/evidence table for the instructor's exact requirements:

1. **How AI finds the algorithm** — exact prompts and verified excerpts **in the PDF**, search queries, at least three credible candidates when available, an **evidence-backed 2024–2026 recency preference**, substantive PCA/LDA contribution, pre-implementation algorithm-selection/feasibility gate, scholarly references, method selection and instruction/workflow diagram.
2. **Algorithm description** — recent PCA/LDA contribution, mathematical model, derivations, assumptions, pseudocode, numerical checks, limitations.
3. **How AI implements it** — source structure, equation-to-code map, implementation details, tests, debugging/reproduction evidence.
4. **Experiments** — real dataset, legitimate splitting, baseline fairness, settings, results, figures, ablations, seed/uncertainty semantics and analysis.
5. **Student learning** — genuinely student-authored reflection, no unfilled placeholder.
6. **Source-code webpage** — working, public URL visibly printed and clickable in PDF, correct repository and published files.

Verify course code/title, student name/ID and assignment number on the title page.

If a requirement is missing, mark the audit **FAIL** even if the rest is exceptional.

## 2. Numerical and source reproducibility

- Rerun tests and appropriate data/metric/report-generation commands from the documented environment if feasible.
- Verify key reported numbers match machine-readable result files, correct denominator/normalization, exact comparison group and split policy.
- Verify bibliography and provenance; no fabricated citations.
- Ensure no tracked secrets, broken imports or missing dependencies.
- Check README instructions, config paths, clean-clone feasibility and actual source code existence.
- Confirm the selected method is the method implemented, not an unrelated generic PCA/LDA with a borrowed paper citation. Recheck the decision record and actual pre-implementation feasibility commands/results. Assess the maturity/recency/difficulty trade-off as a subjective grading risk, not an invented rubric.
- Check clear distinction between completed, post hoc and suggested future experiments.

If changed code or plots alter results, rerun affected experiments and regenerate every dependent table, figure and interpretation. Do not silently retain stale metrics.

## 3. Figure-specific and full-document inspection

Render **all PDF pages**, then inspect suspect pages at higher resolution.

- All plots are legible at actual page size.
- Axes, legends, units, palettes, math symbols and error bars are correct.
- Figures are scientifically useful, professionally styled and backed by actual data.
- Algorithm schematic and AI workflow diagram accurately show the executed process.
- Prompt excerpt typography is readable and sources are labeled.
- Tables/captions/references are not clipped or overlapping.
- Float placement and page whitespace are reasonable, no near-empty pages due to accidental placement.
- Citation links, internal references and public GitHub URL work.

Do not inflate page count just to appear more thorough. Professional figures should clarify evidence and math, not decorate.

## 4. Repository + wiki audit

- Verify public `README.md`, exact source tree, runnable commands, final PDF, figures and experiment provenance.
- Verify mathematical expressions in rendered GitHub Markdown; don't trust local LaTeX build as proof of GitHub rendering.
- Verify Wiki `Home` **actually exists online**, is public and contains functional links; distinguish optional wiki issues from mandatory repository failure.
- Confirm report and remote source agree about method, dataset, metrics, implementation and publication state.
- Confirm latest final Git commits pushed; no local-only submission changes.

## 5. Deliver final quality and risk report

Save a concise audit result, for example `docs/final_submission_audit.md`:

- exact assignment requirement status and evidence;
- candidate-selection gate status, chosen paper publication date, PCA/LDA novelty and evidence of appropriate technical difficulty;
- important objective methodological limitations;
- graphics and formatting assessment;
- scientific consistency and reproducibility checks;
- public links and actual commit hash;
- remaining critical/major/minor issues, if any;
- fixes applied and results rerun;
- honest final submission readiness.

Do not claim "100/100 guaranteed." Instead target **zero missing mandatory requirements and zero known major technical/visual defects**, while identifying any inherently subjective marking risk (e.g. whether the selected publication is sufficiently "recent").

If mandatory conditions remain unsatisfied, keep fixing them where possible. If authentication or a student-authored reflection is genuinely required, report it transparently rather than marking the submission ready.

Your final answer must include the **exact final PDF location**, verified public source-code URL, wiki URL if genuinely published, commit hash, all six requirement statuses and a short statement of any remaining risk.
