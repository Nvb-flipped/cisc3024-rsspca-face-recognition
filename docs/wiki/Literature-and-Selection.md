# Literature and selection

The Prompt 01 search screened recent primary methods for a direct change to PCA or LDA, publication date, mathematical substance, implementation feasibility, matched evaluation and useful figures. The weights and ratings were used for the project decision. [Exact search queries](../research.md) · [Hard gate and score matrix](../algorithm_selection.md)

| Candidate | Verified methodological contribution | Suitability for this assignment |
| --- | --- | --- |
| RSSPCA, Wang et al., PLOS One, 2025 | Absolute-score projection with sparse loadings and neighborhood smoothness. Demonstrated on face reconstruction and recognition. | Accessible equations and MATLAB reference. The graph term can be removed while retaining the remaining update and score budget. |
| DLR-2DPCA, Bi et al., IEEE TCE, 2025 | Cut matrix reconstruction loss and adaptive sample weights for image recognition. | Accessible accepted manuscript. Right matrix projection restricts matching the number of scalar scores on a small image grid. |
| SCRAMBLE, Pfeiffer et al., ADAC, 2025 | Cellwise robust reconstruction with elastic-net sparsity and an orthogonality constraint. | Accessible equation and R reference. Transfer to digits adds decisions about scale and sparsity. Its wear-scar image application disabled sparsity. |
| RSLDA+, Liu et al., Pattern Recognition, 2024 | Sparse LDA for image classification with ADMM updates. | The accessible material did not expose enough of the solver for a defensible reproduction. |

Before implementing the digit runner, Codex checked the two-pixel direction with rational arithmetic and tested a one-direction update and PCA/3-NN using the development partition. After the student requested a face-primary project, the face gate tested the unchanged solver on a 16 × 16 grid using only fitting rows. Both probes passed before the respective holdout evaluations. [Gate outputs for digits](../../results/gate_probe.json) · [Gate outputs for faces](../../results/faces/gate.json) · [Face decision chronology](../face_pivot_decision.md)

[RSSPCA](https://doi.org/10.1371/journal.pone.0323281) · [DLR-2DPCA](https://doi.org/10.1109/TCE.2025.3602258) · [SCRAMBLE](https://doi.org/10.1007/s11634-025-00656-3) · [RSLDA+](https://doi.org/10.1016/j.patcog.2024.110512)
