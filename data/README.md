# Data

## Olivetti faces

The primary face study downloads the 64×64 MATLAB derivative used by scikit-learn. From the project root, `python -m src.face_study fetch` stores `olivettifaces.mat` in the ignored `data/` directory and checks SHA-256 `b612fb967f2dc77c9c62d3e1266e0c73d5fca46a4b8906c18e454d41af987794`. The report credits the underlying database to AT&T Laboratories Cambridge and documents the 16×16 block-average reduction. Its public illustrations use learned coefficients, generated perturbations and archived errors. The optional local galleries use images from the verified download. [Original face source](https://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html) · [Maintainer loader and source hash](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/datasets/_olivetti_faces.py)

## Optdigits

[Optical Recognition of Handwritten Digits](https://doi.org/10.24432/C50P49), Ethem Alpaydin and Cenk Kaynak, UCI Machine Learning Repository (1998), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source CSV records use 64 integer block counts followed by the digit label. The project scales counts by 16 and applies synthetic training-only corruption described in the [study design](../docs/study_design.md). Grayscale examples in this repository are renderings of the block counts. Raw data are fetched from UCI and excluded from Git.
