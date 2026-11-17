# Figures and visualization

The report figures are generated as vector PDF and SVG from archived numerical evidence. The two workflow figures are diagrams of the study and solver.

| Figure | Scientific purpose |
| --- | --- |
| [Training masks](../../results/faces/figures/face_protocol.svg) | Shows the first four archived seed-8301 placements and binary replacement values. Untouched elements are outside the patch. |
| [Recognition](../../results/faces/figures/face_recognition.svg) | Shows accuracy and paired within-mask contrasts on 80 fixed clean views. |
| [Loading maps](../../results/faces/figures/face_loadings.svg) | Compares signed unit coefficients on a common scale and labels energy averaged over the first 16 directions. |
| [Diagnostics](../../results/faces/figures/face_diagnostics.svg) | Shows mask-to-mask roughness, measured fit time and the number of updates to the direction-change threshold. |
| [Budget sensitivity](../../results/faces/figures/face_budget.svg) | Shows accuracy and reconstruction MSE at 8, 16 and 24 coordinates. Whiskers are the sample SD across severe-corruption masks. |
| [Per-image reconstruction errors](../../results/faces/figures/face_reconstruction.svg) | Reports error for the five prespecified source rows. The primary comparison uses all 80 held-out views. |

Public figures use masks, learned coefficients and reconstruction errors. Locally downloaded face inputs enable the optional portrait galleries. [Figure source](../../src/face_figures.py) · [Data and attribution](../../data/README.md)
