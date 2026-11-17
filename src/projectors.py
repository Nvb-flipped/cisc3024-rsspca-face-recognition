"""Train-only feature extractors and the RSSPCA fixed-point step."""
from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.linalg import eigh, solve, svd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


@dataclass
class Projection:
    center: np.ndarray
    weights: np.ndarray
    spectrum: np.ndarray
    elapsed: dict
    traces: list

    def transform(self, x, rank):
        if not 1 <= rank <= self.weights.shape[1]:
            raise ValueError("Requested rank exceeds fitted feature count")
        return (x - self.center) @ self.weights[:, :rank]


def grid_laplacian(shape):
    """Unweighted four-neighbor graph in row-major pixel order."""
    coordinates = np.indices(shape).reshape(2, -1).T
    adjacency = (np.abs(coordinates[:, None] - coordinates).sum(axis=2) == 1).astype(float)
    return np.diag(adjacency.sum(axis=1)) - adjacency


def canonical(vector):
    """Make the largest-magnitude coordinate nonnegative for reproducible display."""
    return vector if vector[np.argmax(np.abs(vector))] >= 0 else -vector


def fixed_point(x, w, laplacian, eta, gamma):
    """Paper Eq. (32)–(33), evaluated through an equivalent SPD solve."""
    if not np.isfinite([eta, gamma]).all() or eta <= 0 or gamma < 0:
        raise ValueError("RSSPCA requires finite eta > 0 and gamma >= 0")
    magnitude = np.abs(w)
    root = np.sqrt(magnitude)
    signed_sum = x.T @ np.sign(x @ w)
    system = np.diag(magnitude + eta) + gamma * root[:, None] * laplacian * root
    proposal = root * solve(system, root * signed_sum, assume_a="pos", check_finite=False)
    norm = np.linalg.norm(proposal)
    if norm == 0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize an empty or nonfinite RSSPCA update")
    result = proposal / norm
    return -result if result @ w < 0 else result


def iterate_component(x, initial, laplacian, eta, gamma, tolerance, max_iterations):
    w = initial
    trace = {"step": [], "mean_abs_score": [float(np.abs(x @ w).mean())]}
    for _ in range(max_iterations):
        next_w = fixed_point(x, w, laplacian, eta, gamma)
        step = float(np.linalg.norm(next_w - w))
        trace["step"].append(step)
        trace["mean_abs_score"].append(float(np.abs(x @ next_w).mean()))
        w = next_w
        if step <= tolerance:
            break
    trace["converged"] = step <= tolerance
    return canonical(w), trace


def fit_rsspca(x, ranks, shape, eta, gamma, tolerance, max_iterations):
    start = perf_counter()
    if not np.isfinite(tolerance) or tolerance <= 0 or max_iterations < 1:
        raise ValueError("Stopping parameters must be positive")
    n, d = x.shape
    if np.prod(shape) != d:
        raise ValueError("Image grid does not match the number of columns")
    center = x.mean(axis=0)
    centered = x - center
    scale = np.linalg.norm(centered)
    rank = int(np.linalg.matrix_rank(centered))
    if max(ranks) > rank:
        raise ValueError(f"Requested components exceed numerical data rank {rank}")
    laplacian = grid_laplacian(shape)
    residual = centered
    weights, traces, elapsed = [], [], {}
    basis = np.empty((d, 0))
    for k in range(1, max(ranks) + 1):
        # A leading residual covariance eigenvector initializes the published map.
        value, direction = eigh(residual.T @ residual, subset_by_index=(d - 1, d - 1))
        if value[0] <= (np.finfo(float).eps * max(n, d) * scale) ** 2:
            raise ValueError("Deflation exhausted the available data")
        w, trace = iterate_component(
            residual, canonical(direction[:, 0]), laplacian, eta, gamma, tolerance, max_iterations
        )
        orthogonal = w - basis @ (basis.T @ w)
        orthogonal -= basis @ (basis.T @ orthogonal)
        norm = np.linalg.norm(orthogonal)
        if norm < 1e-10:
            raise ValueError("A learned loading is numerically dependent on its predecessors")
        basis = np.column_stack((basis, orthogonal / norm))
        residual = centered - (centered @ basis) @ basis.T
        weights.append(w)
        traces.append(trace)
        if k in ranks:
            elapsed[k] = perf_counter() - start
    return Projection(center, np.column_stack(weights), np.array([]), elapsed, traces)


def fit_projection(method, x, y, ranks, cfg, eta=0, gamma=0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    if x.ndim != 2 or not np.isfinite(x).all() or len(x) < 2 or y.shape != (len(x),):
        raise ValueError("Projection requires aligned labels and a finite 2D sample matrix")
    if not ranks or min(ranks) < 1 or max(ranks) > x.shape[1]:
        raise ValueError("Invalid projected dimension")
    if method in ("RSSPCA", "No smoothness", "No smoothness (tuned)"):
        return fit_rsspca(x, ranks, cfg["image_shape"], eta, gamma,
                          cfg["step_tolerance"], cfg["max_iterations"])
    start = perf_counter()
    center = x.mean(axis=0)
    spectrum = np.array([])
    if method == "Pixels":
        weights = np.eye(x.shape[1])
    elif method == "PCA":
        _, singular, vectors = svd(x - center, full_matrices=False)
        rank = np.count_nonzero(singular > np.finfo(float).eps * max(x.shape) * singular[0])
        if max(ranks) > rank:
            raise ValueError(f"Requested components exceed numerical data rank {rank}")
        weights = vectors[:max(ranks)].T
        spectrum = singular ** 2 / (len(x) - 1)
    elif method == "LDA":
        lda = LinearDiscriminantAnalysis(solver="svd", n_components=max(ranks)).fit(x, y)
        weights = lda.scalings_[:, :max(ranks)]
        if weights.shape[1] < max(ranks):
            raise ValueError("Fisher subspace has lower rank than requested")
        spectrum = lda.explained_variance_ratio_
    else:
        raise ValueError(f"Unknown projection method {method}")
    elapsed = perf_counter() - start
    weights = np.column_stack([canonical(w) for w in weights.T])
    return Projection(center, weights, spectrum, {k: elapsed for k in ranks}, [])
