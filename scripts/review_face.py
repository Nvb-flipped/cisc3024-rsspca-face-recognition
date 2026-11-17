"""Audit the frozen face evaluation with direct, independently computed checks."""
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from threadpoolctl import threadpool_limits

from src.data import file_hash
from src.experiment import read_json, write_json
from src.face_data import FILENAME
from src.face_study import frozen

ROOT = Path("results/faces")
METHODS = ("Pixels", "PCA", "LDA", "No smoothness", "RSSPCA")


def source_images(path, indices):
    vectors = loadmat(path, variable_names=["faces"])["faces"]
    # Read the source's column-major 64 x 64 raster independently of face_data.
    faces = np.stack([vectors[:, i].reshape((64, 64), order="F") for i in indices])
    means = np.empty((len(indices), 16, 16))
    for row in range(16):
        for col in range(16):
            means[:, row, col] = faces[:, 4*row:4*row+4, 4*col:4*col+4].mean(axis=(1, 2))
    return means.reshape(len(indices), 256) / 255


def reproduce_masks(n, seed, shape, size):
    """Replicate the published seed stream and nested-mask construction."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(n)
    locations = rng.integers(np.asarray(shape) - size + 1, size=(n, 2))
    patches = rng.integers(0, 2, size=(n, size, size), dtype=np.uint8)
    return order, locations, patches


def perturbed(clean, order, locations, patches, fraction, size):
    images = clean.copy().reshape(len(clean), 16, 16)
    for i in range(int(fraction*len(clean))):
        row, col = locations[i]
        images[order[i], row:row+size, col:col+size] = patches[i]
    return images.reshape(clean.shape)


def exact_selection(archive, hp, n_valid):
    groups = defaultdict(list)
    for row in archive:
        correct = round(row["accuracy"] * n_valid)
        assert abs(correct/n_valid - row["accuracy"]) < 1e-14
        groups[row["eta"], row["gamma"]].append((row["fraction"], correct))
    assert all(sorted(f for f, _ in group) == [0., .25, .5] for group in groups.values())
    order = sorted(groups, key=lambda p: (-sum(c for _, c in groups[p]), p[1], p[0]))
    assert order[0] == (hp["eta"], hp["gamma"])
    best_count = sum(c for _, c in groups[order[0]])
    assert abs(best_count/(n_valid*3) - hp["mean_accuracy"]) < 1e-14
    return {
        "matched_trial_counts": len(archive),
        "validation_correct_sum": best_count,
        "validation_score_denominator": n_valid*3,
        "tied_parameter_pairs": [list(p) for p in order if sum(c for _, c in groups[p]) == best_count],
    }


def nearest_three(train, labels, test):
    # Direct broadcasting avoids the fitted classifier and its distance backend.
    distance = ((test[:, None, :] - train[None, :, :])**2).sum(axis=2)
    order = np.argsort(distance, axis=1, kind="stable")
    ranked = np.take_along_axis(distance, order[:, :4], axis=1)
    ties = np.count_nonzero(np.isclose(ranked[:, 2], ranked[:, 3], atol=1e-14, rtol=1e-13))
    votes = labels[order[:, :3]]
    answer = np.array([np.bincount(row, minlength=40).argmax() for row in votes])
    vote_ties = np.count_nonzero((votes[:, 0] != votes[:, 1]) & (votes[:, 0] != votes[:, 2])
                                 & (votes[:, 1] != votes[:, 2]))
    return answer, int(ties), int(vote_ties)


def unit_energy(w):
    images = w.T.reshape(-1, 16, 16)
    differences = np.square(np.diff(images, axis=1)).sum(axis=(1, 2))
    differences += np.square(np.diff(images, axis=2)).sum(axis=(1, 2))
    return differences / np.square(w).sum(axis=0)


def grid_from_difference():
    reshaped = np.eye(256).reshape(16, 16, 256)
    incidence = np.concatenate([np.diff(reshaped, axis=a).reshape(-1, 256) for a in (0, 1)])
    return incidence.T @ incidence


def last_update(residual, w, eta, gamma, grid):
    mag = np.abs(w)
    v = residual.T @ np.sign(residual @ w)
    system = np.diag(mag + eta) + gamma * grid * mag[None, :]
    d = mag * np.linalg.solve(system, v)
    d /= np.linalg.norm(d)
    return min(np.linalg.norm(d - w), np.linalg.norm(d + w))


def check_traces(x, weights, entry, grid, tolerance, cap, diagnostics):
    np.testing.assert_allclose(np.linalg.norm(weights, axis=0), 1, atol=1e-13)
    diagnostics["capped"] += sum(not t["converged"] for t in entry["trace"])
    for j, trace in enumerate(entry["trace"]):
        steps = trace["step"]
        assert 1 <= len(steps) <= cap and len(trace["mean_abs_score"]) == len(steps) + 1
        assert trace["converged"] == (steps[-1] <= tolerance)
        assert all(step > tolerance for step in steps[:-1])
        q = np.linalg.qr(weights[:, :j], mode="reduced")[0]
        residual = x - (x @ q) @ q.T
        if j:
            assert np.max(np.abs(residual @ weights[:, :j])) < 1e-12
        w = weights[:, j]
        score = np.abs(residual @ w).mean()
        np.testing.assert_allclose(score, trace["mean_abs_score"][-1], atol=1e-12, rtol=1e-12)
        next_step = float(last_update(residual, w, entry["eta"], entry["gamma"], grid))
        diagnostics["directions"] += 1
        diagnostics["next_above_tolerance"] += next_step > tolerance
        diagnostics["max_next_step"] = max(diagnostics["max_next_step"], next_step)
        diagnostics["traces_with_score_decrease"] += bool(
            np.any(np.diff(trace["mean_abs_score"]) < -1e-12)
        )


def review():
    cfg = read_json("configs/faces.json")
    frozen(cfg, ROOT)
    src = Path("data") / FILENAME
    choice = read_json(ROOT / "selection.json")
    assert file_hash(src) == choice["source_sha256"]
    split = {k: np.asarray(v) for k, v in read_json(ROOT / "split.json").items()}
    np.testing.assert_array_equal(np.sort(np.concatenate(list(split.values()))), np.arange(400))
    for role, number in (("fit", 6), ("validation", 2), ("test", 2)):
        np.testing.assert_array_equal(np.bincount(split[role] // 10), np.full(40, number))
    dev = np.sort(np.r_[split["fit"], split["validation"]])
    train = source_images(src, dev)
    test = source_images(src, split["test"])
    y_train, y_test = dev // 10, split["test"] // 10
    ranks = cfg["ranks"]
    assert np.unique(np.vstack([train, test]), axis=0).shape[0] == 400
    grid = grid_from_difference()
    report = exact_selection(read_json(ROOT / "validation.json"), choice["picked"], len(split["validation"]))
    final = read_json(ROOT / "final.json")["runs"]
    fits = read_json(ROOT / "fits.json")
    rows = {(r["fraction"], r["seed"], r["method"], r["rank"]): r for r in final}
    cases = [(f, seed) for f in cfg["fractions"] for seed in (cfg["corruption_seeds"] if f else [0])]
    fit_index = {(r["fraction"], r["seed"], r["method"]): r for r in fits}
    assert len(rows) == len(final) == len(cases)*(4*len(ranks)+1)
    assert len(fit_index) == len(fits) == len(cases)*len(METHODS)
    diagnostics = {m: dict(directions=0, capped=0, next_above_tolerance=0, max_next_step=0.,
                           traces_with_score_decrease=0) for m in METHODS[-2:]}
    numerical = Counter(distance_boundaries=0, predictions=0, reconstructed_runs=0)
    primary_vote_ties = Counter()
    pca_residual = 0.
    lda_dim = 40
    mask = cfg["patch_size"]
    with (np.load(ROOT / "models.npz") as archive, np.load(ROOT / "predictions.npz") as predictions,
          np.load(ROOT / "reconstruction.npz") as errors,
          np.load(ROOT / "validation_masks.npz") as val_archive):
        np.testing.assert_array_equal(predictions["test_indices"], split["test"])
        np.testing.assert_array_equal(predictions["y"], y_test)
        vorder, vloc, vpatch = reproduce_masks(len(split["fit"]), cfg["validation_seed"],
                                               cfg["image_shape"], mask)
        for i, f in enumerate(cfg["fractions"]):
            k = int(f*len(vorder))
            np.testing.assert_array_equal(val_archive[f"r{i}_rows"], split["fit"][vorder[:k]])
            np.testing.assert_array_equal(val_archive[f"r{i}_locations"], vloc[:k])
            np.testing.assert_array_equal(val_archive[f"r{i}_patches"], vpatch[:k])
        for i, (f, seed) in enumerate(cases):
            order, loc, patch = reproduce_masks(len(train), seed, cfg["image_shape"], mask)
            n = int(f*len(train))
            for field, values in (("rows", order), ("locations", loc), ("patches", patch)):
                np.testing.assert_array_equal(archive[f"s{i}_{field}"], values[:n])
            noisy = perturbed(train, order, loc, patch, f, mask)
            for m in METHODS:
                entry = fit_index[f, seed, m]
                key = entry["key"]
                center, w = archive[f"{key}_center"], archive[f"{key}_weights"]
                np.testing.assert_allclose(center, noisy.mean(axis=0), rtol=0, atol=1e-14)
                x = noisy - center
                energy = unit_energy(w)
                np.testing.assert_allclose(energy, entry["energy"], atol=1e-13, rtol=1e-13)
                if m == "PCA":
                    cov = x.T @ x
                    rayleigh = (w * (cov @ w)).sum(axis=0)
                    assert np.all(np.diff(rayleigh) <= 0)
                    residual = float(np.linalg.norm(cov @ w - w * rayleigh) / np.linalg.norm(cov @ w))
                    pca_residual = max(pca_residual, residual)
                    assert residual < 1e-12
                if m == "LDA":
                    within = np.vstack([a-a.mean(axis=0) for a in
                                        (x[y_train == label] for label in np.arange(40))])
                    projected_within = within @ w
                    gram = projected_within.T @ projected_within / (len(x)-40)
                    np.testing.assert_allclose(gram, np.eye(w.shape[1]), rtol=1e-9, atol=1e-9)
                    lda_dim = min(lda_dim, np.linalg.matrix_rank(w))
                if m in diagnostics:
                    check_traces(x, w, entry, grid, cfg["step_tolerance"], cfg["max_iterations"],
                                 diagnostics[m])
                primary = 256 if m == "Pixels" else cfg["primary_rank"]
                for k in ([primary] if m == "Pixels" else ranks):
                    row = rows[f, seed, m, k]
                    code = row["prediction_key"]
                    wk = w[:, :k]
                    pred, boundary_ties, vote_ties = nearest_three(x @ wk, y_train, (test - center) @ wk)
                    np.testing.assert_array_equal(pred, predictions[code], err_msg=code)
                    correct = int(np.sum(pred == y_test))
                    assert row["correct"] == correct and row["accuracy"] == correct/len(y_test)
                    cm = np.bincount(40*y_test + pred, minlength=1600).reshape(40, 40)
                    tp = cm.diagonal()
                    np.testing.assert_allclose(row["macro_f1"],
                                               np.mean(2*tp/(cm.sum(axis=0)+cm.sum(axis=1))))
                    np.testing.assert_allclose(row["balanced_accuracy"], correct/len(y_test))
                    np.testing.assert_allclose(row["energy"], energy[:k].mean(), atol=1e-13)
                    assert row["near_zero_fraction"] == np.mean(np.abs(wk) <= 1e-3)
                    numerical["distance_boundaries"] += boundary_ties
                    numerical["predictions"] += len(pred)
                    if k == primary:
                        primary_vote_ties[m] += vote_ties
                    if m in ("PCA", "RSSPCA", "No smoothness"):
                        coefficients = np.linalg.lstsq(wk, (test-center).T, rcond=None)[0]
                        mse = ((test - center - (wk @ coefficients).T)**2).mean(axis=1)
                        np.testing.assert_allclose(mse, errors[code], atol=1e-13, rtol=1e-12)
                        np.testing.assert_allclose(row["mean_mse"], mse.mean(), atol=1e-13)
                        numerical["reconstructed_runs"] += 1
    return {**report, **dict(numerical), "recognition_runs": len(rows),
            "max_pca_eigen_residual": pca_residual, "min_lda_loading_rank": int(lda_dim),
            "primary_class_vote_ties": dict(primary_vote_ties), "fixed_point": diagnostics}


if __name__ == "__main__":
    with threadpool_limits(limits=1):
        evidence = review()
    write_json(ROOT / "prompt02_audit.json", evidence)
    print(evidence)
