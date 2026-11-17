# Dataset and protocol

The Olivetti derivative used by scikit-learn contains 400 grayscale images of 40 known identities at 64 × 64 pixels. `src/face_data.py` checks the source hash, uses the maintainer loader's orientation and averages nonoverlapping 4 × 4 blocks on a fixed intensity scale to obtain a 16 × 16 grid. The face database is credited to AT&T Laboratories Cambridge. [Data sources and access](../../data/README.md)

| Stage | Views per identity | Total views | Purpose |
| --- | ---: | ---: | --- |
| Fit | 6 | 240 | Development parameter grid and inner feasibility check |
| Validation | 2 | 80 | Rank-16 parameter selection on clean inputs |
| Holdout | 2 | 80 | Clean, fixed evaluation after fitting on the combined 320 development views |

At each positive severity, an 8 × 8 patch on each selected training image is assigned independent zeros and ones. Exactly 25% or 50% of fitting rows receive patches. Shared seeds and nested row selection keep the comparisons paired. There is one deterministic clean case and five paired masks per positive severity. The score budgets are 8, 16 and 24, with 16 primary and raw pixels using all 256. All arms use Euclidean 3-NN. LDA uses identity labels during projection fitting.

Validation compares three $\eta$ values and two $\gamma$ values on three training corruption levels. Both top settings reached 171 correct out of 240 repeated validation predictions. The recorded tie rule selected $\eta=0.001$ and $\gamma=0.3$. The controlled ablation sets $\gamma=0$ and keeps $\eta$ fixed. The frozen models, masks and provenance were saved before final scoring. [Study design](../face_study_design.md) · [Configuration](../../configs/faces.json) · [Selection and freeze](../../results/faces/)
