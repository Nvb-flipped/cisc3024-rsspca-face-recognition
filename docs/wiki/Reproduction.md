# Reproduction

Use Python 3.14.3 and the versions pinned in `requirements.txt` from a clean checkout. These commands fetch the pinned face source, run the fitting-only probe and reproduce the locked experiment into a new output directory.

```bash
python -m pip install -r requirements.txt
python -m src.face_study fetch
python -m scripts.face_gate
python -m src.face_study tune --out results/reproduction/wiki-face-replay
python -m src.face_study prepare --out results/reproduction/wiki-face-replay
python -m src.face_study final --out results/reproduction/wiki-face-replay
python -m src.face_study audit --out results/reproduction/wiki-face-replay --against results/faces
python -m scripts.review_face
```

The full replay reproduced 143 recognition arrays and 99 per-image reconstruction-error arrays in the pinned environment. Measured fit times can vary. The separate digit archive has its own replay commands and metrics. [Face setup and Windows test launcher](../../README.md#reproduce-the-face-study) · [Digit replay](../../report/optdigits/README.md)

`python -m src.face_summary` writes the report tables. `python -m src.face_figures` writes the public SVG/PDF figures from the numeric archives. To additionally generate the portrait-based illustrations from local Olivetti data, use `python -m src.face_figures --local-image-galleries`. Build the report from `report/` with `tectonic -X compile --untrusted report.tex`. The supplied Latin Modern fonts are loaded by both figure and report sources. [Report source](../../report/report.tex)
