# Face application pivot

The student requested Prompt 01B after the verified Optdigits experiment and asked to distinguish the primary application from Assignment #2, which also used 8×8 digits. The 2025 Wang et al. RSSPCA selection, exact toy update, symmetric-system derivation, and original experiment remain part of the project. Prompt 01B changes the primary application to known-identity face recognition, closer to the selected paper's application. It introduces a separate feasibility gate, data split, evaluation protocol and result archive.

The workspace had no Git history before the pivot. The expanded Latin Modern digit report and the verified implementation were saved on local branch `study/optdigits-baseline`, commit `181d542`. The requested branch `study/face-primary` starts from this snapshot. Digit results, code, masks, config and figure files stay at their established paths. Both digit PDFs and the expanded source are also preserved in the Optdigits report archive. The later public snapshot preserves these files and keeps the portrait-containing commits in the local history. [Optdigits report archive](../report/optdigits/)

## Source and resolution decision

The AT&T Laboratories Cambridge archive describes 40 identities and ten frontal grayscale views per identity. Expression, illumination and details such as glasses vary across views. The original PGM release is 92×112. This project uses the 64×64 Olivetti derivative referenced by scikit-learn. The archive digest matches its loader metadata. The source asks users to credit AT&T Laboratories Cambridge. The raw archive is downloaded separately. The public edition uses the saved masks, learned coefficients and reconstruction errors for its figures. Locally generated portraits are credited to the source. [AT&T archive](https://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html) · [scikit-learn dataset documentation](https://scikit-learn.org/stable/datasets/real_world.html#the-olivetti-faces-dataset)

Before the feasibility probe, the chosen representation was 16×16 using a fixed 4×4 block average with source-scale normalization by 255. The same reduction is used for every arm. The source file is compressed as one MATLAB archive. It is decoded by the loader, then only explicitly requested fit rows are reduced during the gate. The planned validation and face-test rows are excluded from the prototype fit, inspection and metrics.

The shared RSSPCA implementation already builds its graph from an arbitrary rectangular `shape` and checks the feature count. The digit classifier runner handles ten labels and specific input files. The face study uses a separate runner and preserves the shared solver and digit-source digests.

## Dated execution

| Time on 17 November 2026 (UTC+8) | Observed milestone |
| --- | --- |
| 14:55:18 | Training-only gate passed on a nested 160/80 split of the 240 fitting rows. The rank-24 RSSPCA trial took 0.391 s and tracked 2.84 MiB of allocations. |
| 14:57:01 | The face design and configuration were saved before writing the main runner. |
| 14:59:14 | Clean-development validation selected eta 0.001 and gamma 0.3 with a 71.25% mean across the three training conditions. |
| 14:59:22 | All 55 face scenario/arm fits and their data/code provenance were frozen. |
| 14:59:40 | The first face holdout output was written. It contains 143 prediction arrays and 99 per-image reconstruction error arrays. |

The independent audit verified 400 unique reduced faces, labels and shared masks. Repeating the locked pipeline reproduced the split, validation, selected penalties, masks, loadings, predictions and reconstruction errors exactly. Fitting and prediction times are measured values and can vary. The face extension added three tests to the ten original tests. See [audit](../results/faces/audit.txt), [replay](../results/faces/replay.txt) and [tests](../results/faces/tests.txt).

The 17-page Latin Modern face report was compiled with Tectonic and visually inspected. The eight face figures passed the rendered collision checks. The final audit checks the embedded typefaces, figure count, required headings, references, reported accuracy and preserved digit artifacts. The archived Optdigits source also compiled independently. The Prompt 01B audit identifies the PDF stored at `report/report.pdf` in commit `8267cad`. Prompt 02 subsequently revised the report while keeping the experimental archive. [Prompt 01B PDF audit](../results/faces/report_check.json) · [Prompt 02 review](quality_review.md)
