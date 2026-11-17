# Prompt 03 — Publish the Verified Project to GitHub and Populate the Wiki

Read `AGENTS.md`, the original assignment requirements, Prompt 01, Prompt 02, the latest compiled report and `docs/quality_review.md`.

Goal: publish a genuinely **public, complete, reproducible GitHub repository** for Assignment #3, with a **working public source-code URL in the PDF**. Also enable and populate a GitHub Wiki where feasible.

Do not substitute "prepared to publish" for publication.

## Face-primary publication checks

Read `prompts/01B_FACE_PRIMARY_MIGRATION.md` and the face study's actual protocol/results. Publish the face experiment as primary **only if feasibility and test audits succeeded**. Preserve the original Optdigits run as a clearly labeled secondary/archived study (with provenance, not stale main-report claims). Update main README, project title, reproduction instructions, dataset attribution and Wiki to emphasize RSSPCA face recognition/reconstruction if executed. Verify image/data licensing and whether example face images may be redistributed; default to download instructions and generated figures with appropriate attribution rather than blindly committing original datasets. Ensure the README and PDF use consistent face-specific figures, method descriptions, dimensions, numerical results and URLs. Mark the post-Prompt-01 face pivot as an explicit subsequent instruction, not an invented original research plan.
## A. Publication preflight

1. Confirm all required local research, tests, experiments, figures and PDF compilation are complete, and that `docs/algorithm_selection.md` includes the **pre-implementation candidate comparison, hard-gate checks and feasible numerical prototype evidence**.
2. Confirm the student's personal reflection has been supplied in the report. **If not, do not fabricate it; complete publication of verified technical files if safe, but report the PDF as not submission-ready until the reflection is inserted.**
3. Check local Git state, GitHub CLI availability (`gh --version`), `gh auth status`, current account and existing remotes.
4. Do not overwrite or publish the unrelated Assignment #1 or Assignment #2 repositories. Choose a new descriptive name (for example `cisc3024-pca-lda-pattern-recognition`) unless an existing appropriate remote is explicitly identified.
5. Check `.gitignore` and staged files for credentials, machine paths, private material, dataset licensing limitations, excessive checkpoints, large caches and accidental binary artifacts.
6. Verify repository contains implementation, dataset access instructions, config, exact reproducibility scripts, tests, evaluation evidence, source-to-figure scripts, LaTeX source, bibliography, compiled PDF, real prompts and `AGENTS.md`.

## B. Public repo creation and push

Use authenticated GitHub CLI where available:

```powershell
gh auth status
gh repo create REPOSITORY_NAME --public --source=. --remote=origin --push
```

These are illustrative commands; inspect Git state first and avoid recreating existing repositories or overwriting remotes. When a repo already exists, verify its exact owner/name/public visibility and push the correct branch normally. Do not use dangerous force pushes without explicit necessity and justification.

- Make meaningful commits.
- Verify the remote URL, branch, latest commit and **public visibility** using actual GitHub response.
- Verify README links and a browsable code tree.
- Provide the true repo URL only after successful publication.
- Do not include API keys or credentials in the repo or screenshots.

If authentication requires user action, identify only that blocker with exact supported steps; do not request passwords in chat, fake an authenticated session, or mark publication as complete.

## C. Make all Markdown **GitHub-native**

Review `README.md`, `docs/*.md` and wiki source files for GitHub Flavored Markdown.

Rules:

- Inline math uses `$x^\top S_W x$`.
- Display math uses `$$` on standalone lines or a fenced block labeled `math`.
- Do not assume LaTeX `equation`, `align` or `\[...\]` render in Markdown.
- Use actual valid links, relative paths, correct filename case, lists, tables, alt text and in-repo figure locations.
- Mermaid is suitable for GitHub flowcharts when it truly renders; the PDF report must retain proper vector figures independently.
- Test the rendered README and at least the important math/figure/wiki pages on GitHub when possible; correct syntax rather than relying solely on local Markdown preview.

## D. Enable **and publish** the Wiki

1. Use `gh repo edit OWNER/REPO --enable-wiki` if CLI supports it. Verify availability.
2. Prepare useful wiki pages, such as:
   - `Home`: scope and navigation;
   - `Algorithm-and-Mathematics`: verified PCA/LDA derivations, assumptions, algorithm schematic;
   - `Literature-and-Selection`: actual cited paper comparison, recency/difficulty/feasibility criteria, algorithm-selection gate and verified primary-source evidence;
   - `Dataset-and-Protocol`: source, splits, baselines and leakage controls;
   - `Experiments-and-Results`: real tables/figures, hyperparameter plots, findings and limitations;
   - `Reproduction`: clean installation and commands;
   - `AI-Workflow`: actual `AGENTS.md`, prompts, applied skills and human/AI responsibility;
   - `Figures-and-Visualization` if helpful.
3. **Important:** `docs/wiki/*.md` inside the main repository is only a source copy. It does **not** itself populate the GitHub Wiki tab.
4. Publish the pages through the separate wiki Git repository (typically `https://github.com/OWNER/REPO.wiki.git`) or verified supported GitHub UI actions.
5. Some wikis need a first `Home` page created on GitHub before the wiki Git repository is accessible. If required, initialize it through supported UI access; otherwise tell the user precisely what manual step is necessary, then resume publication.
6. Verify the public **Wiki → Home** page and links, mathematics, images, cross-page navigation and content accuracy. Avoid claims of a published wiki if only source Markdown exists.

The wiki is desirable, but the assignment's mandatory core is a public source-code webpage link. An unavailable wiki must not block finishing the mandatory PDF+repo deliverables.

## E. Update and rebuild the final report

Once the repository URL actually exists:

1. Insert the verified public code URL in the report's sixth mandatory section.
2. Update earlier "deferred publication" statements in abstract, report, README and other docs.
3. Insert a real wiki URL **only if the wiki is published and accessible**.
4. Preserve all scientific findings, metrics, code provenance and student-authored reflection.
5. Recompile and visually inspect the complete final PDF.
6. Commit and push the final PDF, updated README, and any repository/wiki references.
7. Confirm that public GitHub displays the newest PDF and that its source-link URL is active.

## F. Completion summary

Return:

- public repository URL and verified public status;
- wiki URL and published status (or specific blocker);
- final branch and commit hash;
- exact path to the final PDF;
- test/reproducibility results;
- confirmation that README and mathematical expressions render correctly;
- confirmation that the report includes the actual repository link;
- any remaining user-only step (especially reflection or authentication).

Never fabricate publication, access tests or a guaranteed grade.
