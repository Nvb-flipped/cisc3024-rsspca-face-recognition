from pathlib import Path

import numpy as np
import pytest
from scipy.linalg import eigh, orth
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from threadpoolctl import threadpool_limits

from src.data import apply_masks, corrupt, load_partition, overlap
from src.experiment import classifier, metrics, read_json, select_hp
from src.projectors import fit_projection, fixed_point, grid_laplacian

CONFIG = read_json(Path("configs/study.json"))


@pytest.fixture(autouse=True)
def one_thread():
    with threadpool_limits(1):
        yield


def test_grid_laplacian_has_expected_edges_and_energy():
    L = grid_laplacian((2, 3))
    np.testing.assert_array_equal(L, L.T)
    np.testing.assert_array_equal(L.sum(axis=0), np.zeros(6))
    assert np.trace(L) == 14
    assert L[2, 3] == 0
    eigenvalues = np.linalg.eigvalsh(L)
    assert abs(eigenvalues[0]) < 1e-14 and eigenvalues[1] > 0
    w = np.array([1., 4., 5., 2., 3., 1.])
    assert w @ L @ w == sum((w[i] - w[j])**2
                            for i, j in [(0, 1), (1, 2), (3, 4), (4, 5),
                                         (0, 3), (1, 4), (2, 5)])


@pytest.mark.parametrize("eta,gamma", [(0.2, 0.5), (1e-9, 0.0), (1e-8, 100.)])
def test_symmetric_fit_agrees_with_independent_unsymmetric_system(eta, gamma):
    rng = np.random.default_rng(252)
    x = rng.normal(size=(50, 6))
    w = np.array([.6, -.8, .0001, 0, 0, .01])
    w /= np.linalg.norm(w)
    L = grid_laplacian((2, 3))
    U = np.diag(np.abs(w))
    system = U + eta * np.eye(6) + gamma * L @ U
    raw = U @ np.linalg.solve(system, x.T @ np.sign(x @ w))
    target = raw / np.linalg.norm(raw)
    actual = fixed_point(x, w, L, eta, gamma)
    orientation = np.sign(actual @ target)
    np.testing.assert_allclose(actual, orientation * target, atol=1e-10)
    np.testing.assert_allclose(fixed_point(x, -w, L, eta, gamma), -actual, atol=1e-12)
    assert np.abs(actual[[3, 4]]).sum() == 0


def test_exact_example_and_invalid_updates():
    x = np.array([[1., 2.], [-1., -2.]])
    L = grid_laplacian((1, 2))
    w = np.array([.6, .8])
    expected = np.array([132., 200.])
    np.testing.assert_allclose(fixed_point(x, w, L, 0.2, 0.5),
                               expected / np.linalg.norm(expected))
    with pytest.raises(ValueError, match="eta"):
        fixed_point(x, w, L, 0.0, 0.5)
    with pytest.raises(ValueError, match="normalize"):
        fixed_point(x * 0, w, L, 0.2, 0.5)


def test_rsspca_deflation_and_repeatability():
    rng = np.random.default_rng(42)
    x = rng.normal(size=(80, 6))
    kwargs = ({"image_shape": [2, 3], "step_tolerance": 1e-5, "max_iterations": 100},
              .02, .25)
    y = np.arange(len(x)) % 3
    first = fit_projection("RSSPCA", x, y, [3], *kwargs)
    repeated = fit_projection("RSSPCA", x, y, [1, 3], *kwargs)
    one = fit_projection("RSSPCA", x, y, [1], *kwargs)
    np.testing.assert_array_equal(first.weights, repeated.weights)
    np.testing.assert_array_equal(first.weights[:, :1], one.weights)
    np.testing.assert_allclose(np.linalg.norm(first.weights, axis=0), 1)
    np.testing.assert_allclose(first.transform(x, 3).mean(axis=0), 0, atol=1e-14)
    q = orth(first.weights)
    r = (x - first.center) - ((x - first.center) @ q) @ q.T
    np.testing.assert_allclose(r @ first.weights, 0, atol=1e-13)
    assert all(len(t["step"]) + 1 == len(t["mean_abs_score"]) for t in first.traces)
    with pytest.raises(ValueError, match="numerical data rank"):
        fit_projection("RSSPCA", np.ones_like(x), y, [1], *kwargs)
    with pytest.raises(ValueError, match="aligned labels"):
        fit_projection("RSSPCA", x, y[:-1], [1], *kwargs)
    with pytest.raises(ValueError, match="rank"):
        first.transform(x, 4)


def test_pca_against_sklearn_and_eigen_equation():
    rng = np.random.default_rng(155)
    x = rng.normal(size=(60, 6)) * np.arange(1, 7)
    p = fit_projection("PCA", x, np.zeros(len(x)), [3], CONFIG)
    ref = PCA(3, svd_solver="full").fit(x)
    np.testing.assert_allclose(p.weights @ p.weights.T,
                               ref.components_.T @ ref.components_, atol=1e-13)
    np.testing.assert_allclose(np.cov(x.T) @ p.weights, p.weights * p.spectrum[:3],
                               atol=1e-12)
    np.testing.assert_allclose(p.weights.T @ p.weights, np.eye(3), atol=1e-13)


def test_lda_subspace_against_generalized_eigenproblem_and_constant_pixel():
    rng = np.random.default_rng(756)
    y = np.repeat(np.arange(3), 45)
    x = rng.normal(size=(len(y), 5))
    x[:, 0] += y
    x[:, 1] += y == 1
    means = np.array([x[y == label].mean(axis=0) for label in range(3)])
    residuals = x - means[y]
    between = means[y] - x.mean(axis=0)
    within_scatter = residuals.T @ residuals
    between_scatter = between.T @ between
    lam, weights = eigh(between_scatter, within_scatter)
    p = fit_projection("LDA", x, y, [2], CONFIG)
    reference = LinearDiscriminantAnalysis(n_components=2, solver="svd").fit(x, y)
    np.testing.assert_allclose(np.abs(p.transform(x, 2)), np.abs(reference.transform(x)),
                               atol=1e-12)
    target = orth(weights[:, -2:])
    actual = orth(p.weights)
    np.testing.assert_allclose(target @ target.T, actual @ actual.T, atol=1e-13)
    np.testing.assert_allclose(between_scatter @ weights[:, -2:],
                               (within_scatter @ weights[:, -2:]) * lam[-2:], atol=1e-13)
    with_constant = np.column_stack([x, np.ones(len(x))])
    constant_fit = fit_projection("LDA", with_constant, y, [2], CONFIG)
    np.testing.assert_allclose(np.abs(constant_fit.transform(with_constant, 2)),
                               np.abs(p.transform(x, 2)), atol=1e-12)


def test_paired_masks_round_trip_and_evaluation(tmp_path):
    x = np.arange(12 * 64, dtype=float).reshape(12, 64)
    a, a_rows, a_pos, a_patch = corrupt(x, .25, 6101, (8, 8), 4)
    b, b_rows, b_pos, b_patch = corrupt(x, .5, 6101, (8, 8), 4)
    assert len(np.unique(a_rows)) == 3 and len(np.unique(b_rows)) == 6
    np.testing.assert_array_equal(a_rows, b_rows[:3])
    np.testing.assert_array_equal(a_pos, b_pos[:3])
    np.testing.assert_array_equal(a_patch, b_patch[:3])
    np.testing.assert_array_equal(a[a_rows], b[a_rows])
    np.testing.assert_array_equal(b[np.setdiff1d(np.arange(len(x)), b_rows)],
                                  x[np.setdiff1d(np.arange(len(x)), b_rows)])
    path = tmp_path / "masks.npz"
    np.savez(path, rows=b_rows, locations=b_pos, patches=b_patch)
    with np.load(path) as data:
        regenerated = apply_masks(x, data["rows"], data["locations"], data["patches"], (8, 8), 4)
    np.testing.assert_array_equal(regenerated, b)
    y = np.repeat(np.arange(3), 4)
    pred = classifier(x, y, CONFIG).predict(x)
    assert metrics(y, pred)["accuracy"] == 1
    assert overlap((x, y), (x[:3], y[:3]))["cross_partition_matching_test_rows"] == 3


def test_selection_ties_and_invalid_source(tmp_path):
    rows = [dict(eta=eta, gamma=gamma, accuracy=.96)
            for eta in [0.1, .01] for gamma in [.3, .03]]
    assert select_hp(rows) == {"eta": .01, "gamma": .03, "mean_accuracy": .96}
    (tmp_path / "optdigits.tra").write_text("invalid data")
    with pytest.raises(ValueError, match="hash"):
        load_partition(tmp_path, "tra")
