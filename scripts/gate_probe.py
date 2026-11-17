"""Pre-implementation probe; consumes only the official development file."""
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.linalg import solve
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from threadpoolctl import threadpool_limits


def check_update():
    # Derive the symmetric system by substituting p = sqrt(D) y.
    x = np.array([[1., 2.], [-1., -2.]])
    w = np.array([0.6, 0.8])
    laplacian = np.array([[1., -1.], [-1., 1.]])
    eta, gamma = 0.2, 0.5
    magnitude = abs(w)
    root = np.sqrt(magnitude)
    v = x.T @ np.sign(x @ w)
    system = np.diag(magnitude + eta) + gamma * root[:, None] * laplacian * root
    p = root * solve(system, root * v, assume_a="pos")

    # Rational 2x2 solve by Cramer's rule on the published nonsymmetric system.
    a, b, c, d = (Fraction(z) for z in ("1.1", "-.4", "-.3", "1.4"))
    determinant = a * d - b * c
    expected = [
        Fraction("0.6") * (2 * d - 4 * b) / determinant,
        Fraction("0.8") * (4 * a - 2 * c) / determinant,
    ]
    np.testing.assert_allclose(p, [float(z) for z in expected], atol=1e-13)
    direction = p / np.linalg.norm(p)
    assert abs(np.linalg.norm(direction) - 1) < 1e-14

    # Zero coordinate exercises the non-inverted D formulation.
    root_zero = np.array([1., 0.])
    zero_system = np.diag(root_zero + eta) + gamma * root_zero[:, None] * laplacian * root_zero
    with_zero = root_zero * solve(zero_system, root_zero * v, assume_a="pos")
    np.testing.assert_allclose(with_zero, [20 / 17, 0.], atol=1e-13)

    # For the normalized iterate, v - Qw need not be parallel to w:
    # normalizing the unconstrained optimum can change first-order stationarity.
    q = np.eye(2) + eta * np.diag(1 / magnitude) + gamma * laplacian
    normal_residual = (np.eye(2) - np.outer(direction, direction)) @ (v - q @ direction)
    assert np.linalg.norm(normal_residual) > 0.1
    return {
        "raw_update_exact": [str(z) for z in expected],
        "normalized_update": direction.tolist(),
        "linear_residual": float(np.linalg.norm(q @ p - v)),
        "min_system_eigenvalue": float(np.linalg.eigvalsh(system)[0]),
        "zero_coordinate_update": with_zero.tolist(),
        "sphere_tangent_residual": float(np.linalg.norm(normal_residual)),
    }


def check_training_file(path):
    if path.name != "optdigits.tra":
        raise ValueError("Pass only the official development file optdigits.tra")
    array = np.loadtxt(path, delimiter=",", dtype=np.int16)
    assert array.shape == (3823, 65)
    pixels, labels = array[:, :-1], array[:, -1]
    assert pixels.min() == 0 and pixels.max() == 16
    assert np.array_equal(np.unique(labels), np.arange(10))
    fit, valid = train_test_split(
        np.arange(len(labels)), test_size=0.20, random_state=193, stratify=labels
    )
    assert not np.intersect1d(fit, valid).size
    start = perf_counter()
    pca = PCA(n_components=8, svd_solver="full").fit(pixels[fit] / 16)
    model = KNeighborsClassifier(3, algorithm="brute").fit(
        pca.transform(pixels[fit] / 16), labels[fit]
    )
    accuracy = model.score(pca.transform(pixels[valid] / 16), labels[valid])
    assert pca.n_samples_ == len(fit) and accuracy > 0.70
    start = perf_counter()
    x = pixels[fit] / 16
    x -= x.mean(axis=0)
    coords = np.indices((8, 8)).reshape(2, -1).T
    adjacent = np.abs(coords[:, None] - coords).sum(axis=-1) == 1
    grid = np.diag(adjacent.sum(axis=0)) - adjacent
    w = pca.components_[0]
    first = np.abs(x @ w).mean()
    for iteration in range(100):
        r = np.sqrt(np.abs(w))
        a = np.diag(abs(w) + 0.01) + 0.3 * r[:, None] * grid * r
        p = r * solve(a, r * (x.T @ np.sign(x @ w)), assume_a="pos")
        next_w = p / np.linalg.norm(p)
        change = min(np.linalg.norm(next_w - w), np.linalg.norm(next_w + w))
        w = next_w
        if change <= 1e-4:
            break
    assert np.isfinite(w).all() and abs(w @ w - 1) < 1e-13
    unique_pixels = len(np.unique(pixels, axis=0))
    return {
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "shape": list(pixels.shape),
        "pixel_range": [int(pixels.min()), int(pixels.max())],
        "development_class_counts": np.bincount(labels).tolist(),
        "development_unique_images": unique_pixels,
        "constant_pixels": int(np.count_nonzero(np.ptp(pixels, axis=0) == 0)),
        "fit": len(fit),
        "validation": len(valid),
        "validation_class_counts": np.bincount(labels[valid]).tolist(),
        "baseline_pca8_3nn_validation_accuracy": accuracy,
        "prototype_rsspca_iterations": iteration + 1,
        "prototype_rsspca_last_step": change,
        "prototype_rsspca_mean_absolute_score_initial": first,
        "prototype_rsspca_mean_absolute_score_final": np.abs(x @ w).mean(),
        "prototype_rsspca_seconds_including_unique_count": perf_counter() - start,
        "full_development_float64_bytes": pixels.size * 8,
    }


if __name__ == "__main__":
    with threadpool_limits(limits=1):
        print(json.dumps({
            "update": check_update(),
            "development_only": check_training_file(Path(sys.argv[1])),
        }, indent=2))
