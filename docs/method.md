# RSSPCA method and implementation

For centered residual rows $R$, the proposed loading maximizes $\|Rw\|_1$ under a unit norm, an $\ell_1$ budget and the pixel-graph energy budget $w^\top Lw\le c_2$. Wang et al. derive a sign-based update using a quadratic minorizer. Set $D=\operatorname{diag}(|w|)$, $H=D^{1/2}$ and $v=R^\top\operatorname{sign}(Rw)$. The project computes the published map with the equivalent symmetric system

$$
(D+\eta I+\gamma HLH)t=Hv,\qquad p=Ht,\qquad w^+=p/\|p\|_2.
$$

For $\eta>0$ and $\gamma\ge0$ the system is positive definite. The graph Laplacian $L$ connects each pixel only to immediate horizontal or vertical neighbors. Its quadratic form is the sum of squared loading differences over 480 edges in the primary 16 × 16 face grid. The report gives the inequalities, equivalence proof, numerical example and a stationarity countercheck for the normalized quadratic update. [Report](../report/report.pdf) · [Original paper](https://doi.org/10.1371/journal.pone.0323281)

[projectors.py](../src/projectors.py) uses leading residual eigenvectors for initialization, a sign-invariant direction-change stop at $10^{-4}$ with a cap of 100 updates, and exact span deflation using an orthonormal basis $Q$ for previously extracted raw directions. The score vectors sent to 3-NN use the raw directions $W$, while deflation uses $R=X-XQQ^\top$. Exact zeros stay zero and PCA-type scores are unwhitened. Fisher LDA uses a rank-aware SVD to remove null within-class directions, and retains its conventional scatter-scaled coordinates.

The face runner tunes on the development data, freezes masks and fitted models, and evaluates the clean held-out views. A thin QR factorization $W=QB$ gives $\widehat a=\mu+QQ^\top(a-\mu)$, which is an orthogonal projection even when the raw loading columns are nonorthogonal. The clean target is the reconstruction input. [Face runner](../src/face_study.py) · [Independent archive audit](../scripts/review_face.py) · [Face protocol](face_study_design.md)

```mermaid
flowchart LR
    A["Handout and AGENTS.md"] --> B["Prompt 01: search and verify candidate papers"]
    B --> C["Validate update and development smoke test"]
    C --> D["Freeze, evaluate and archive Optdigits"]
    D --> E["Prompt 01B: student requests faces"]
    E --> F["Pass face gate, tune, freeze and evaluate"]
    F --> G["Prompt 02: replay, audit and revise"]
    G --> H["Student reflection and Prompt 03 release"]
```

The original digit adaptation uses the same update on an 8 × 8 grid with 112 edges and its own development and held-out protocol. The Python solver is an implementation of the paper equations. The authors' GPL-3.0 MATLAB package was used as a reference. [Vector workflow](../results/faces/figures/face_workflow.pdf) · [Optdigits archive](../report/optdigits/README.md) · [Author reference package](https://github.com/yuzhounh/RSSPCA)
