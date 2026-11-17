"""Run development selection, frozen fits, held-out evaluation and evidence checks."""
import argparse
import itertools
import json
import os
import platform
import sys
from collections import defaultdict
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy
import sklearn
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from threadpoolctl import threadpool_info, threadpool_limits

from src.data import apply_masks, corrupt, fetch_partition, file_hash, load_partition, overlap
from src.projectors import fit_projection, grid_laplacian

LABELS = np.arange(10)
CODE = [Path("src") / filename for filename in ("data.py", "projectors.py", "experiment.py")]


def write_json(path, data):
    path = Path(path)
    partial = path.with_suffix(path.suffix + ".tmp")
    partial.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    partial.replace(path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def environment():
    return {
        "device": "CPU",
        "platform": platform.platform(),
        "processor_identifier": os.getenv("PROCESSOR_IDENTIFIER") or platform.processor(),
        "logical_processors": os.cpu_count(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "threadpools": [
            {name: item[name] for name in ("internal_api", "user_api", "num_threads", "version")}
            for item in threadpool_info()
        ],
    }


def code_hashes():
    return {path.as_posix(): file_hash(path) for path in CODE}


def classifier(features, labels, cfg):
    return KNeighborsClassifier(n_neighbors=cfg["neighbors"], algorithm="brute", n_jobs=1).fit(
        features, labels
    )


def training_variation(x, fraction, seed, cfg):
    return corrupt(x, fraction, seed, cfg["image_shape"], cfg["patch_size"])


def select_hp(candidates):
    scores = defaultdict(list)
    for row in candidates:
        scores[(row["eta"], row["gamma"])].append(row["accuracy"])
    eta, gamma = min(scores, key=lambda key: (-np.mean(scores[key]), key[1], key[0]))
    return {"eta": eta, "gamma": gamma, "mean_accuracy": float(np.mean(scores[(eta, gamma)]))}


def tune(cfg, dev, out):
    x, y, digest = dev
    folds = StratifiedKFold(len(cfg["fold_corruption_seeds"]), shuffle=True,
                            random_state=cfg["fold_seed"])
    records, splits, validation_masks = [], [], {}
    rank = cfg["primary_rank"]
    grid = list(itertools.product(cfg["eta"], [0.0, *cfg["gamma"]]))
    for index, ((fit, valid), seed) in enumerate(zip(folds.split(x, y),
                                                   cfg["fold_corruption_seeds"], strict=True)):
        splits.append({"fold": index, "fit": fit.tolist(), "validation": valid.tolist(), "seed": seed})
        for fraction_index, fraction in enumerate(cfg["fractions"]):
            train_x, rows, locations, patches = training_variation(x[fit], fraction, seed, cfg)
            key = f"f{index}_r{fraction_index}"
            validation_masks[f"{key}_rows"] = fit[rows]
            validation_masks[f"{key}_locations"] = locations
            validation_masks[f"{key}_patches"] = patches
            for eta, gamma in grid:
                result = fit_projection("RSSPCA", train_x, y[fit], [rank], cfg, eta, gamma)
                knn = classifier(result.transform(train_x, rank), y[fit], cfg)
                predictions = knn.predict(result.transform(x[valid], rank))
                records.append({
                    "fold": index, "fraction": fraction, "eta": eta, "gamma": gamma,
                    "accuracy": float(accuracy_score(y[valid], predictions)),
                    "capped_components": sum(not item["converged"] for item in result.traces),
                })
    np.savez_compressed(out / "validation_masks.npz", **validation_masks)
    lock = {
        "phase": "development_only", "development_sha256": digest, "config": cfg,
        "code_sha256": code_hashes(), "environment": environment(),
        "rss": select_hp([r for r in records if r["gamma"] > 0]),
        "no_smoothness": select_hp([r for r in records if r["gamma"] == 0]),
    }
    write_json(out / "validation.json", records)
    write_json(out / "splits.json", {"development_folds": splits,
                                      "official_test_indices": list(range(1797))})
    write_json(out / "selection.json", lock)
    return lock


def checked_selection(cfg, dev, out):
    lock = read_json(out / "selection.json")
    if lock["config"] != cfg or lock["development_sha256"] != dev[2]:
        raise ValueError("Development data or protocol differ from the selection lock")
    if lock["code_sha256"] != code_hashes():
        raise ValueError("Experimental code differs from the selection lock")
    return lock


def scenarios(cfg):
    for fraction in cfg["fractions"]:
        for seed in (cfg["test_corruption_seeds"] if fraction else [0]):
            yield fraction, seed


def methods(cfg, lock):
    shared = [rank for rank in cfg["ranks"] if rank <= 9]
    eta, gamma = lock["rss"]["eta"], lock["rss"]["gamma"]
    yield "Pixels", [int(np.prod(cfg["image_shape"]))], 0.0, 0.0
    yield "PCA", cfg["ranks"], 0.0, 0.0
    yield "LDA", shared, 0.0, 0.0
    yield "RSSPCA", cfg["ranks"], eta, gamma
    yield "No smoothness", cfg["ranks"], eta, 0.0
    independent_eta = lock["no_smoothness"]["eta"]
    if independent_eta != eta:
        yield "No smoothness (tuned)", cfg["ranks"], independent_eta, 0.0


def prepare(cfg, dev, out):
    x, y, _ = dev
    lock = checked_selection(cfg, dev, out)
    evidence, arrays = [], {}
    graph = grid_laplacian(cfg["image_shape"])
    for case, (fraction, seed) in enumerate(scenarios(cfg)):
        noisy, rows, locations, patches = training_variation(x, fraction, seed, cfg)
        arrays.update({f"s{case}_rows": rows, f"s{case}_locations": locations,
                       f"s{case}_patches": patches})
        for method_id, (method, ranks, eta, gamma) in enumerate(methods(cfg, lock)):
            key = f"s{case}_m{method_id}"
            projection = fit_projection(method, noisy, y, ranks, cfg, eta, gamma)
            arrays.update({f"{key}_center": projection.center, f"{key}_weights": projection.weights,
                           f"{key}_spectrum": projection.spectrum})
            energies = np.sum(projection.weights * (graph @ projection.weights), axis=0)
            for rank in ranks:
                start = perf_counter()
                classifier(projection.transform(noisy, rank), y, cfg)
                evaluator_time = perf_counter() - start
                weights = projection.weights[:, :rank]
                evidence.append({
                    "method": method, "fraction": fraction, "seed": seed, "rank": rank,
                    "eta": eta, "gamma": gamma, "case": case, "key": key,
                    "corrupted_rows": len(rows),
                    "fit_seconds": projection.elapsed[rank] + evaluator_time,
                    "unit_direction_energy": float(np.mean(energies[:rank] /
                                                           np.sum(weights ** 2, axis=0))),
                    "near_zero_fraction": float(np.mean(np.abs(weights) <= 0.001)),
                    "capped_components": sum(not item["converged"] for item in projection.traces[:rank]),
                    "trace": projection.traces[:rank] if rank == max(ranks) else [],
                })
    np.savez_compressed(out / "fitted.npz", **arrays)
    write_json(out / "fit_records.json", evidence)
    frozen = {name: file_hash(out / name) for name in
              ("selection.json", "fitted.npz", "fit_records.json", "splits.json")}
    write_json(out / "frozen.json", frozen)
    return len(evidence)


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro", zero_division=0)),
        "confusion": confusion_matrix(y, pred, labels=LABELS).tolist(),
    }


def checked_frozen(cfg, dev, out):
    checked_selection(cfg, dev, out)
    frozen = read_json(out / "frozen.json")
    if any(file_hash(out / name) != digest for name, digest in frozen.items()):
        raise ValueError("A frozen result was modified before final scoring")


def evaluate(cfg, dev, data, out):
    checked_frozen(cfg, dev, out)
    if (out / "final.json").exists():
        raise FileExistsError("Existing held-out results. Use a separate output directory for reproduction.")
    x, y, _ = dev
    test_x, test_y, test_sha = load_partition(data, "tes")
    evidence = read_json(out / "fit_records.json")
    result, predictions = [], {"test_row": np.arange(len(test_y)), "y": test_y}
    case_id = None
    with np.load(out / "fitted.npz") as arrays:
        for entry in evidence:
            case, key, rank = entry["case"], entry["key"], entry["rank"]
            if case != case_id:
                mask_prefix = f"s{case}"
                train = apply_masks(x, arrays[f"{mask_prefix}_rows"],
                                    arrays[f"{mask_prefix}_locations"],
                                    arrays[f"{mask_prefix}_patches"],
                                    cfg["image_shape"], cfg["patch_size"])
                case_id = case
            center, weights = arrays[f"{key}_center"], arrays[f"{key}_weights"][:, :rank]
            model = classifier((train - center) @ weights, y, cfg)
            start = perf_counter()
            pred = model.predict((test_x - center) @ weights)
            predict_time = perf_counter() - start
            pred_key = f"{key}_k{rank}"
            predictions[pred_key] = pred
            row = {k: v for k, v in entry.items() if k != "trace"}
            result.append({**row, "prediction_key": pred_key, "predict_seconds": predict_time,
                           **metrics(test_y, pred)})
    np.savez_compressed(out / "predictions.npz", **predictions)
    write_json(out / "final.json", {
        "test_sha256": test_sha,
        "n_test": len(test_y),
        "official_partition_overlap": overlap((x, y), (test_x, test_y)),
        "environment": environment(), "runs": result,
    })
    return len(result)


def verify(out, against=None):
    final = read_json(out / "final.json")
    with np.load(out / "predictions.npz") as predictions:
        np.testing.assert_array_equal(predictions["test_row"], np.arange(final["n_test"]))
        for row in final["runs"]:
            expected = metrics(predictions["y"], predictions[row["prediction_key"]])
            if any(row[key] != value for key, value in expected.items()):
                raise ValueError(f"Stored metric mismatch for {row['prediction_key']}")
        if against:
            other = read_json(against / "final.json")
            if final["test_sha256"] != other["test_sha256"]:
                raise ValueError("Test data changed across reproductions")
            for name in ("validation.json", "splits.json", "selection.json"):
                if read_json(out / name) != read_json(against / name):
                    raise ValueError(f"Reproduction differs in {name}")
            with np.load(against / "predictions.npz") as reference:
                if set(predictions.files) != set(reference.files):
                    raise ValueError("Reproduction predictions have a different schema")
                for key in predictions.files:
                    np.testing.assert_array_equal(predictions[key], reference[key], err_msg=key)
    return len(final["runs"])


def smoke(cfg, dev):
    """Reduced end-to-end run on an internal development slice."""
    x, y, _ = dev
    fit = np.r_[0:100, 120:320]
    valid = np.r_[100:120, 320:350]
    noisy, *_ = training_variation(x[fit], 0.5, 6101, cfg)
    results = {}
    for method, rank in [("Pixels", 64), ("PCA", 4), ("LDA", 4),
                         ("RSSPCA", 4), ("No smoothness", 4)]:
        projection = fit_projection(method, noisy, y[fit], [rank], cfg, 0.01,
                                    0.3 if method == "RSSPCA" else 0)
        model = classifier(projection.transform(noisy, rank), y[fit], cfg)
        predictions = model.predict(projection.transform(x[valid], rank))
        results[method] = float(accuracy_score(y[valid], predictions))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["fetch-tra", "fetch-tes", "smoke", "tune", "prepare",
                                         "final", "verify"])
    parser.add_argument("--config", type=Path, default=Path("configs/study.json"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--out", type=Path, default=Path("results"))
    parser.add_argument("--against", type=Path)
    args = parser.parse_args()
    cfg = read_json(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    with threadpool_limits(cfg["threads"]):
        if args.phase == "verify":
            result = verify(args.out, args.against)
        elif args.phase == "fetch-tra":
            result = str(fetch_partition(args.data, "tra"))
        else:
            dev = load_partition(args.data, "tra")
            if args.phase == "smoke":
                result = smoke(cfg, dev)
            elif args.phase == "tune":
                result = tune(cfg, dev, args.out)["rss"]
            elif args.phase == "prepare":
                result = prepare(cfg, dev, args.out)
            elif args.phase == "fetch-tes":
                checked_frozen(cfg, dev, args.out)
                result = str(fetch_partition(args.data, "tes"))
            else:
                result = evaluate(cfg, dev, args.data, args.out)
    print(json.dumps({"phase": args.phase, "result": result}, allow_nan=False))


if __name__ == "__main__":
    sys.exit(main())
