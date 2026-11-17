"""Development selection, frozen refits, face scoring and independent evidence checks."""
import argparse
import itertools
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.linalg import orth
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
from threadpoolctl import threadpool_limits

from src.data import apply_masks, corrupt, file_hash
from src.experiment import classifier, environment, read_json, select_hp, write_json
from src.face_data import IDENTITIES, SOURCE_SHA, fetch_faces, identity_split, load_faces
from src.projectors import fit_projection, grid_laplacian

PCA_FAMILY = ("PCA", "No smoothness", "RSSPCA")
LABELS = np.arange(IDENTITIES)
LOCK_FILES = ("selection.json", "split.json", "models.npz", "fits.json")
CODE = ("face_study.py", "face_data.py", "data.py", "projectors.py", "experiment.py")


def source_digests():
    return {name: file_hash(Path("src") / name) for name in CODE}


def partition_set(cfg):
    fit, valid, test = identity_split(cfg["split_seed"])
    return fit, valid, test


def tune(cfg, data, out):
    fit, valid, test = partition_set(cfg)
    x, y = load_faces(data, fit, cfg["image_shape"])
    vx, vy = load_faces(data, valid, cfg["image_shape"])
    records, masks = [], {}
    k = cfg["primary_rank"]
    for i, fraction in enumerate(cfg["fractions"]):
        noisy, rows, xy, patch = corrupt(x, fraction, cfg["validation_seed"],
                                         cfg["image_shape"], cfg["patch_size"])
        masks.update({f"r{i}_rows": fit[rows], f"r{i}_locations": xy, f"r{i}_patches": patch})
        for eta, gamma in itertools.product(cfg["eta"], cfg["gamma"]):
            projection = fit_projection("RSSPCA", noisy, y, [k], cfg, eta, gamma)
            pred = classifier(projection.transform(noisy, k), y, cfg).predict(
                projection.transform(vx, k)
            )
            records.append({"eta": eta, "gamma": gamma, "fraction": fraction,
                            "accuracy": float(accuracy_score(vy, pred)),
                            "caps": sum(not q["converged"] for q in projection.traces)})
    picked = select_hp(records)
    write_json(out / "split.json", dict(fit=fit.tolist(), validation=valid.tolist(), test=test.tolist()))
    write_json(out / "validation.json", records)
    np.savez_compressed(out / "validation_masks.npz", **masks)
    write_json(out / "selection.json", dict(picked=picked, config=cfg, source_sha256=SOURCE_SHA,
                                           code=source_digests(), environment=environment()))
    return picked


def selection(cfg, out):
    record = read_json(out / "selection.json")
    if record["config"] != cfg or record["source_sha256"] != SOURCE_SHA or record["code"] != source_digests():
        raise ValueError("Face protocol, source identity or fitting code changed after selection")
    actual = read_json(out / "split.json")
    for key, values in zip(("fit", "validation", "test"), partition_set(cfg), strict=True):
        if actual[key] != values.tolist():
            raise ValueError("Declared face split differs from the saved split")
    return record["picked"]


def prepare(cfg, data, out):
    hp = selection(cfg, out)
    fit, valid, _ = partition_set(cfg)
    dev = np.sort(np.r_[fit, valid])
    x, y = load_faces(data, dev, cfg["image_shape"])
    grid = grid_laplacian(cfg["image_shape"])
    k_all = cfg["ranks"]
    arms = [
        ("Pixels", [x.shape[1]], 0, 0),
        ("PCA", k_all, 0, 0),
        ("LDA", k_all, 0, 0),
        ("No smoothness", k_all, hp["eta"], 0),
        ("RSSPCA", k_all, hp["eta"], hp["gamma"]),
    ]
    records, arrays = [], {}
    scenarios = [(fraction, seed) for fraction in cfg["fractions"]
                 for seed in (cfg["corruption_seeds"] if fraction else [0])]
    for i, (fraction, seed) in enumerate(scenarios):
        noisy, rows, xy, patches = corrupt(x, fraction, seed, cfg["image_shape"], cfg["patch_size"])
        arrays.update({f"s{i}_rows": rows, f"s{i}_locations": xy, f"s{i}_patches": patches})
        for j, (method, ks, eta, gamma) in enumerate(arms):
            key = f"s{i}_m{j}"
            proj = fit_projection(method, noisy, y, ks, cfg, eta, gamma)
            arrays.update({f"{key}_center": proj.center, f"{key}_weights": proj.weights})
            energy = np.sum(proj.weights * (grid @ proj.weights), axis=0) / np.sum(proj.weights**2, axis=0)
            elapsed = {}
            for k in ks:
                start = perf_counter()
                classifier(proj.transform(noisy, k), y, cfg)
                elapsed[k] = proj.elapsed[k] + perf_counter() - start
            records.append({
                "case": i, "key": key, "method": method, "fraction": fraction, "seed": seed,
                "ranks": ks, "fit_seconds": elapsed, "count_corrupted": len(rows),
                "energy": energy.tolist(), "trace": proj.traces, "eta": eta, "gamma": gamma,
            })
    np.savez_compressed(out / "models.npz", **arrays)
    write_json(out / "fits.json", records)
    write_json(out / "freeze.json", {name: file_hash(out / name) for name in LOCK_FILES})
    return len(records)


def frozen(cfg, out):
    selection(cfg, out)
    manifest = read_json(out / "freeze.json")
    expected = {name: file_hash(out / name) for name in LOCK_FILES}
    if manifest != expected:
        raise ValueError("A locked face artifact changed or is missing")


def reconstruct(images, center, weights):
    q, r = np.linalg.qr(weights, mode="reduced")
    if np.any(np.abs(np.diag(r)) < 1e-10):
        raise ValueError("Reconstruction requires independent loading columns")
    return center + ((images - center) @ q) @ q.T


def masked_faces(images, arrays, case, cfg):
    prefix = f"s{case}"
    return apply_masks(images, arrays[f"{prefix}_rows"], arrays[f"{prefix}_locations"],
                       arrays[f"{prefix}_patches"], cfg["image_shape"], cfg["patch_size"])


def evaluate(cfg, data, out):
    frozen(cfg, out)
    if (out / "final.json").exists():
        raise FileExistsError("Face holdout already evaluated in this output directory")
    fit, valid, test = partition_set(cfg)
    dev = np.sort(np.r_[fit, valid])
    x, y = load_faces(data, dev, cfg["image_shape"])
    tx, ty = load_faces(data, test, cfg["image_shape"])
    records = read_json(out / "fits.json")
    predictions = {"test_indices": test, "y": ty}
    errors, results = {}, []
    with np.load(out / "models.npz") as arrays:
        for case, group in itertools.groupby(records, key=lambda r: r["case"]):
            noisy = masked_faces(x, arrays, case, cfg)
            for run in group:
                key = run["key"]
                center, weights = arrays[f"{key}_center"], arrays[f"{key}_weights"]
                for k in run["ranks"]:
                    w = weights[:, :k]
                    model = classifier((noisy-center) @ w, y, cfg)
                    start = perf_counter()
                    pred = model.predict((tx-center) @ w)
                    time = perf_counter() - start
                    pred_key = f"{key}_k{k}"
                    predictions[pred_key] = pred
                    cm = confusion_matrix(ty, pred, labels=LABELS)
                    mse = None
                    if run["method"] in PCA_FAMILY:
                        error = np.mean((tx - reconstruct(tx, center, w))**2, axis=1)
                        errors[pred_key] = error
                        mse = float(error.mean())
                    results.append({
                        **{field: run[field] for field in ("key", "method", "fraction", "seed", "case")},
                        "rank": k, "prediction_key": pred_key, "correct": int((pred == ty).sum()),
                        "accuracy": float(accuracy_score(ty, pred)),
                        "balanced_accuracy": float(balanced_accuracy_score(ty, pred)),
                        "macro_f1": float(f1_score(ty, pred, labels=LABELS, average="macro",
                                                   zero_division=0)),
                        "identity_recall": (np.diag(cm) / cm.sum(axis=1)).tolist(),
                        "fit_seconds": run["fit_seconds"][str(k)], "predict_seconds": time,
                        "mean_mse": mse, "energy": float(np.mean(run["energy"][:k])),
                        "near_zero_fraction": float(np.mean(np.abs(w) <= 0.001)),
                        "capped": sum(not trace["converged"] for trace in run["trace"][:k]),
                    })
    np.savez_compressed(out / "predictions.npz", **predictions)
    np.savez_compressed(out / "reconstruction.npz", **errors)
    write_json(out / "final.json", {"source_sha256": SOURCE_SHA, "test_count": len(ty), "runs": results})
    return len(results)


def audit(cfg, data, out):
    frozen(cfg, out)
    partitions = partition_set(cfg)
    np.testing.assert_array_equal(np.sort(np.concatenate(partitions)), np.arange(400))
    all_rows = []
    for idx, count in zip(partitions, (6, 2, 2), strict=True):
        features, labels = load_faces(data, idx, cfg["image_shape"])
        np.testing.assert_array_equal(np.bincount(labels, minlength=40), np.full(40, count))
        all_rows.append(features)
    fit, valid, test = partitions
    dev = np.sort(np.r_[fit, valid])
    train, _ = load_faces(data, dev, cfg["image_shape"])
    x = all_rows[2]
    y = test // 10
    validation = read_json(out / "validation.json")
    assert select_hp(validation) == read_json(out / "selection.json")["picked"]
    results = read_json(out / "final.json")["runs"]
    with (np.load(out / "models.npz") as models, np.load(out / "predictions.npz") as preds,
          np.load(out / "reconstruction.npz") as errors):
        np.testing.assert_array_equal(preds["test_indices"], test)
        np.testing.assert_array_equal(preds["y"], y)
        for case in {r["case"]: r for r in results}.values():
            i = case["case"]
            _, rows, loc, patch = corrupt(train, case["fraction"], case["seed"],
                                          cfg["image_shape"], cfg["patch_size"])
            for suffix, expected in (("rows", rows), ("locations", loc), ("patches", patch)):
                np.testing.assert_array_equal(models[f"s{i}_{suffix}"], expected)
        for record in results:
            pred = preds[record["prediction_key"]]
            cm = np.zeros((40, 40), dtype=int)
            np.add.at(cm, (y, pred), 1)
            tp = cm.diagonal()
            recall = tp / cm.sum(axis=1)
            np.testing.assert_array_equal(recall, record["identity_recall"])
            np.testing.assert_allclose([record["accuracy"], record["balanced_accuracy"],
                                       record["macro_f1"]],
                                      [tp.sum()/len(y), recall.mean(),
                                       (2*tp/(cm.sum(axis=0)+cm.sum(axis=1))).mean()])
            assert record["correct"] == tp.sum()
            if record["mean_mse"] is not None:
                k, key = record["rank"], record["key"]
                center = models[f"{key}_center"]
                q = orth(models[f"{key}_weights"][:, :k])
                assert q.shape[1] == k
                residual = x - center - (x - center) @ q @ q.T
                mse = np.mean(residual**2, axis=1)
                np.testing.assert_allclose(mse, errors[record["prediction_key"]], atol=1e-13)
                np.testing.assert_allclose(mse.mean(), record["mean_mse"], atol=1e-13)
    return {"verified_runs": len(results),
            "unique_16x16_rows": np.unique(np.concatenate(all_rows), axis=0).shape[0],
            "reconstruction_runs": sum(r["mean_mse"] is not None for r in results)}


def compare(out, reference):
    for name in ("split.json", "validation.json", "selection.json"):
        if read_json(out / name) != read_json(reference / name):
            raise ValueError(f"Replay differs in {name}")
    for name in ("models.npz", "predictions.npz", "reconstruction.npz"):
        with np.load(out / name) as left, np.load(reference / name) as right:
            assert left.files == right.files
            for key in left.files:
                np.testing.assert_array_equal(left[key], right[key], err_msg=key)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["fetch", "tune", "prepare", "final", "audit"])
    parser.add_argument("--config", type=Path, default=Path("configs/faces.json"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--out", type=Path, default=Path("results/faces"))
    parser.add_argument("--against", type=Path)
    args = parser.parse_args()
    cfg = read_json(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(cfg["threads"]):
        if args.phase == "fetch":
            result = str(fetch_faces(args.data))
        elif args.phase == "tune":
            result = tune(cfg, args.data, args.out)
        elif args.phase == "prepare":
            result = prepare(cfg, args.data, args.out)
        elif args.phase == "final":
            result = evaluate(cfg, args.data, args.out)
        else:
            result = audit(cfg, args.data, args.out)
            if args.against:
                compare(args.out, args.against)
                result["exact_replay"] = True
    print(result)


if __name__ == "__main__":
    main()
