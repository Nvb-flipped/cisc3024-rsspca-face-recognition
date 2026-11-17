"""Training-only acceptance checks for the Olivetti adaptation."""
import argparse
import json
import tracemalloc
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.linalg import orth, solve
from threadpoolctl import threadpool_limits

from src.experiment import classifier
from src.face_data import identity_split, load_faces
from src.projectors import fit_projection, fixed_point, grid_laplacian


def probe(directory):
    shape = (16, 16)
    cfg = {"image_shape": shape, "step_tolerance": 1e-4, "max_iterations": 100, "neighbors": 3}
    fit_ids, _, _ = identity_split(20261117)
    train = fit_ids.reshape(40, 6)
    x, y = load_faces(directory, train[:, :4].ravel(), shape)
    check, labels = load_faces(directory, train[:, 4:].ravel(), shape)
    centered = x - x.mean(axis=0)
    grid = grid_laplacian(shape)
    w = np.linalg.svd(centered, full_matrices=False)[2][0].copy()
    w[0] = 0
    w /= np.linalg.norm(w)
    image = w.reshape(shape)
    edge_energy = (np.diff(image, axis=0)**2).sum() + (np.diff(image, axis=1)**2).sum()
    np.testing.assert_allclose(w @ grid @ w, edge_energy, rtol=1e-12)
    np.testing.assert_array_equal(grid.sum(axis=1), np.zeros(x.shape[1]))

    eta, gamma = 0.01, 0.3
    v = centered.T @ np.sign(centered @ w)
    h = np.sqrt(abs(w))
    d = np.diag(abs(w))
    matrix = d + eta * np.eye(len(w)) + gamma * h[:, None] * grid * h
    t = solve(matrix, h * v, assume_a="pos")
    residual = float(np.linalg.norm(matrix @ t - h * v) / np.linalg.norm(h * v))
    u = np.linalg.solve(d + eta * np.eye(len(w)) + gamma * grid @ d, v)
    direct = d @ u
    direct /= np.linalg.norm(direct)
    actual = fixed_point(centered, w, grid, eta, gamma)
    update_error = float(min(np.linalg.norm(direct-actual), np.linalg.norm(direct+actual)))
    assert residual < 1e-12 and update_error < 1e-11 and actual[0] == 0
    np.testing.assert_allclose(fixed_point(centered, -w, grid, eta, gamma), -actual, atol=1e-13)

    outcomes = {}
    for method in ("Pixels", "PCA", "LDA", "RSSPCA", "No smoothness"):
        k = 256 if method == "Pixels" else 24
        start = perf_counter()
        fit = fit_projection(method, x, y, [k], cfg, eta, gamma if method == "RSSPCA" else 0)
        elapsed = perf_counter() - start
        prediction = classifier(fit.transform(x, k), y, cfg).predict(fit.transform(check, k))
        outcomes[method] = {"dimension": k, "seconds": elapsed,
                            "fit_only_check_accuracy": float(np.mean(prediction == labels))}
        if method == "RSSPCA":
            tracemalloc.start()
            repeated = fit_projection(method, x, y, [k], cfg, eta, gamma)
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            np.testing.assert_array_equal(fit.weights, repeated.weights)
            q = orth(fit.weights)
            projector = q @ q.T
            deflated = centered - centered @ projector
            deflation = float(np.linalg.norm(deflated @ fit.weights))
            assert q.shape == (256, k) and deflation < 1e-10
            np.testing.assert_allclose(projector @ projector, projector, atol=1e-12)
            np.testing.assert_allclose(np.linalg.norm(fit.weights, axis=0), 1, atol=1e-13)
            test_centered = check - fit.center
            reconstruction = test_centered @ projector
            assert np.all(np.linalg.norm(test_centered-reconstruction, axis=1)
                          <= np.linalg.norm(test_centered, axis=1) + 1e-12)
            outcomes[method].update({
                "tracked_peak_bytes": peak, "deflation_residual": deflation,
                "capped_components": sum(not trace["converged"] for trace in fit.traces),
                "exact_repeated_weights": True,
            })
    assert np.linalg.matrix_rank(centered) >= 24
    assert outcomes["RSSPCA"]["seconds"] < 10
    assert outcomes["RSSPCA"]["tracked_peak_bytes"] < 64 * 1024**2
    assert outcomes["PCA"]["fit_only_check_accuracy"] > .35
    assert outcomes["LDA"]["fit_only_check_accuracy"] > .35
    return {
        "status": "PASS", "dataset_rows_used": "240 fit-partition rows only",
        "fit_images": len(x), "internal_check_images": len(check),
        "feature_shape": list(shape), "fit_rank": int(np.linalg.matrix_rank(centered)),
        "observed_fit_matrix_bytes": x.nbytes, "observed_grid_bytes": grid.nbytes,
        "relative_spd_residual": residual, "normalized_update_difference": update_error,
        "grid_energy": float(edge_energy), "fit": outcomes,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    args = parser.parse_args()
    with threadpool_limits(1):
        print(json.dumps(probe(args.data), indent=2))
