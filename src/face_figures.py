"""Export face-specific, Latin Modern figures from the frozen evidence."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.ticker import PercentFormatter

from src.data import apply_masks
from src.experiment import read_json
from src.face_data import load_faces
from src.face_study import PCA_FAMILY, reconstruct
from src.figures import FONT_DIRECTORY, MUTED, PALE, STYLE, export

METHODS = ("Pixels", "PCA", "LDA", "No smoothness", "RSSPCA")
COLORS = dict(zip(METHODS, ("#626A71", "#255A92", "#A04620", "#815075", "#007267"),
                  strict=True))
MARKERS = dict(zip(METHODS, ("X", "s", "^", "D", "o"), strict=True))


def records(rows, method, f, k):
    return sorted([r for r in rows if (r["method"], r["fraction"], r["rank"]) == (method, f, k)],
                  key=lambda r: r["seed"])


def data(rows, method, f, k, metric):
    return np.array([r[metric] for r in records(rows, method, f, k)])


def workflow():
    fig, ax = plt.subplots(figsize=(7.1, 2.05))
    fig.subplots_adjust(left=.007, right=.993, bottom=.02, top=.98)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    cards = [
        ("Course handout", "Define six required\nreport topics"),
        ("AGENTS.md", "Set screening, split\nand evidence rules"),
        ("Staged prompts", "01 digits → 01B faces\n→ 02 critical review"),
        ("Skills applied", "Guide search, math,\nfigures and typesetting"),
        ("Codex searches", "Screen four methods\nand pass the gates"),
        ("Codex evaluates", "Build, freeze and test\nthe two studies"),
        ("Codex reviews", "Replay, audit and\nrevise report figures"),
        ("Verified outputs", "Results, tests, PDF\nand public source"),
    ]
    width, height = .215, .365
    positions = [(x, .60) for x in (.01, .264, .518, .772)]
    positions += [(x, .038) for x in (.772, .518, .264, .01)]
    for i, ((title, body), (x, y)) in enumerate(zip(cards, positions, strict=True)):
        ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.006",
                                    fc="#DDEFE8" if i in (4, 7) else PALE, ec="none"))
        ax.text(x + .016, y + .29, title, weight="bold", fontsize=10, va="top")
        ax.text(x + .016, y + .168, body, fontsize=9, va="top", linespacing=1.2)
    for (x, y), (nx, ny) in zip(positions[:-1], positions[1:], strict=True):
        if x == nx:
            start, stop = (x + width/2, y - .012), (nx + width/2, ny + height + .012)
        elif nx > x:
            start, stop = (x + width + .012, y + height/2), (nx - .012, ny + height/2)
        else:
            start, stop = (x - .012, y + height/2), (nx + width + .012, ny + height/2)
        ax.annotate("", stop, start, arrowprops={"arrowstyle": "-|>", "color": MUTED,
                                                 "shrinkA": 0, "shrinkB": 0})
    return fig


def mechanism():
    fig, ax = plt.subplots(figsize=(7.1, 1.56))
    fig.subplots_adjust(left=.007, right=.993, bottom=.04, top=.96)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    cards = (
        (.012, .22, .202, .60, "Center faces", "4 × 4 box averages\nBuild pixel graph"),
        (.25, .22, .263, .60, "Update on residual", "Signs → SPD solve\nNormalize and align signs\nRepeat to threshold or cap"),
        (.55, .22, .207, .60, "Append and deflate", "Remove learned span\nInitialize next direction"),
        (.80, .56, .185, .42, "Recognition", "Raw scores → 3-NN"),
        (.80, .04, .185, .42, "Reconstruction", "QR → pixel MSE"),
    )
    for i, (x, y, width, height, title, body) in enumerate(cards):
        ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.006",
                                    fc="#DDEFE8" if i == 1 else PALE, ec="none"))
        ax.text(x + .013, y + height - .075, title, weight="bold", fontsize=9.6, va="top")
        ax.text(x + .013, y + height - .233, body, fontsize=8.9, va="top", linespacing=1.23)
    for start, stop in (((.222, .52), (.243, .52)), ((.521, .52), (.542, .52)),
                        ((.765, .52), (.792, .75)), ((.765, .52), (.792, .26))):
        ax.annotate("", stop, start, arrowprops={"arrowstyle": "-|>", "color": MUTED,
                                                 "shrinkA": 0, "shrinkB": 0})
    return fig


def gallery_axes(rows, cols, height):
    fig = plt.figure(figsize=(7.1, height), layout="constrained")
    gs = fig.add_gridspec(rows, cols+1, width_ratios=[.95] + [1.0]*cols)
    return fig, gs


def face_panel(fig, slot, values, **kwargs):
    ax = fig.add_subplot(slot)
    artist = ax.imshow(values.reshape(16, 16), interpolation="nearest", **kwargs)
    ax.set_axis_off()
    return ax, artist


def label_panel(fig, slot, name):
    ax = fig.add_subplot(slot)
    ax.set_axis_off()
    ax.text(0, .5, name, va="center", weight="bold")


def mask_gallery(train, dev, models, case, cfg):
    prefix = f"s{case}"
    rows = models[f"{prefix}_rows"][:4]
    locs = models[f"{prefix}_locations"][:4]
    patches = models[f"{prefix}_patches"][:4]
    noisy = apply_masks(train, rows, locs, patches, cfg["image_shape"], cfg["patch_size"])
    fig, gs = gallery_axes(3, 4, 3.20)
    for i, title in enumerate(("Clean source", "Training input", "Affected cells")):
        label_panel(fig, gs[i, 0], title)
    for j, (row, (top, left)) in enumerate(zip(rows, locs, strict=True), 1):
        mask = np.zeros((16, 16))
        mask[top:top+8, left:left+8] = 1
        ax, _ = face_panel(fig, gs[0, j], train[row], cmap="gray", vmin=0, vmax=1)
        ax.set_title(f"Source row {dev[row]}", loc="center")
        face_panel(fig, gs[1, j], noisy[row], cmap="gray", vmin=0, vmax=1)
        face_panel(fig, gs[2, j], mask, cmap=ListedColormap(["#EAF0F1", "#007267"]), vmin=0, vmax=1)
    return fig


def mask_figure(dev, models, case, cfg):
    """Show the archived perturbations without showing the input portraits."""
    prefix = f"s{case}"
    rows = models[f"{prefix}_rows"][:4]
    locations = models[f"{prefix}_locations"][:4]
    patches = models[f"{prefix}_patches"][:4]
    size = cfg["patch_size"]
    colors = ["#EAF0F1", "#16303C", "#29958A"]
    fig, axes = plt.subplots(1, 4, figsize=(7.1, 2.12), sharey=True, layout="constrained")
    for ax, row, (top, left), patch in zip(axes, rows, locations, patches, strict=True):
        values = np.zeros(cfg["image_shape"], dtype=np.uint8)
        values[top:top+size, left:left+size] = patch+1
        ax.imshow(values, cmap=ListedColormap(colors), interpolation="nearest", vmin=0, vmax=2)
        ax.set(title=f"Source row {dev[row]}", xlabel="Pixel column", xticks=(0, 5, 10, 15),
               yticks=(0, 5, 10, 15))
    axes[0].set_ylabel("Pixel row")
    legend = [Patch(color=color, label=label) for color, label in
              zip(colors, ("Untouched", "Replaced with 0", "Replaced with 1"), strict=True)]
    fig.legend(handles=legend, loc="outside lower center", ncol=3)
    return fig


def loadings(rows, models, cfg):
    fig, gs = gallery_axes(3, 4, 4.05)
    first = [records(rows, m, .5, cfg["primary_rank"])[0] for m in PCA_FAMILY]
    matrices = [models[f"{r['key']}_weights"][:, :4] for r in first]
    bound = max(np.abs(w).max() for w in matrices)
    axes = []
    for i, (method, row, vectors) in enumerate(zip(PCA_FAMILY, first, matrices, strict=True)):
        label_panel(fig, gs[i, 0], f"{method}\nEnergy {row['energy']:.3f}")
        for j in range(4):
            ax, image = face_panel(fig, gs[i, j+1], vectors[:, j], cmap="RdBu_r",
                                   vmin=-bound, vmax=bound)
            if not i:
                ax.set_title(f"Loading {j+1}", loc="center")
            axes.append(ax)
    bar = fig.colorbar(image, ax=axes, location="bottom", shrink=.64, pad=.045, aspect=35)
    bar.set_label("Signed loading weight")
    return fig


def recognition(rows, cfg):
    fig, (acc, diff) = plt.subplots(1, 2, figsize=(7.1, 3.25), layout="constrained")
    fractions, rank = cfg["fractions"], cfg["primary_rank"]
    for j, method in enumerate(METHODS):
        k = 256 if method == "Pixels" else rank
        offset = (j - 2) * .14
        color, marker = COLORS[method], MARKERS[method]
        averages = []
        for i, f in enumerate(fractions):
            a = 100 * data(rows, method, f, k, "accuracy")
            averages.append(a.mean())
            if len(a) > 1:
                position = i + offset
                acc.vlines(position, a.min(), a.max(), color=color, lw=.7, alpha=.48)
                acc.scatter(position + np.linspace(-.032, .032, len(a)), a,
                            marker=marker, color=color, alpha=.57, s=13, linewidths=0)
        acc.scatter(np.arange(len(fractions))+offset, averages, marker=marker, s=29,
                    color=color, edgecolor="white", linewidth=.5, label=method, zorder=4)
    acc.set(title="A  Known-identity recognition", ylabel="Accuracy (%)", xlabel="Training rows corrupted",
            xticks=range(3), xticklabels=["0%", "25%", "50%"], xlim=(-.44, 2.44),
            ylim=(45, 95), yticks=(50, 60, 70, 80, 90))
    acc.grid(axis="y")
    acc.legend(loc="upper center", bbox_to_anchor=(.5, -.25), ncol=3,
               columnspacing=.75, handlelength=1.15, borderaxespad=0)
    diff.axvline(0, color="#5c6871", ls="--", lw=1)
    contrast_order = ("PCA", "No smoothness", "LDA")
    for j, f in enumerate((.25, .5)):
        color = ("#007267", "#A04620")[j]
        marker = ("o", "^")[j]
        for i, method in enumerate(contrast_order):
            delta = 100*(data(rows, "RSSPCA", f, rank, "accuracy")-
                         data(rows, method, f, rank, "accuracy"))
            position = i + (-.15 if j == 0 else .15)
            diff.hlines(position, delta.min(), delta.max(), color=color, lw=.7, alpha=.48)
            diff.scatter(delta, position+np.linspace(-.045, .045, len(delta)),
                         color=color, marker=marker, alpha=.55, s=16, linewidths=0)
            diff.scatter(delta.mean(), position, edgecolor=color, facecolor="white", marker=marker,
                         s=42, label=f"{f:.0%} corruption" if i==0 else None, zorder=4)
    diff.set(title="B  Matched-mask contrasts", xlabel="RSSPCA minus comparator (pp)",
             xticks=(-20, -10, 0, 10), xlim=(-25, 12.5),
             yticks=range(3), yticklabels=contrast_order, ylim=(2.55, -.55))
    diff.grid(axis="x")
    diff.legend(loc="upper center", bbox_to_anchor=(.5, -.25), ncol=2,
                columnspacing=.9, handlelength=1, borderaxespad=0)
    return fig


def budget(rows, cfg):
    fig, (acc, err) = plt.subplots(1, 2, figsize=(7.1, 3.1), layout="constrained")
    ranks = np.array(cfg["ranks"])
    reduced = METHODS[1:]
    for index, method in enumerate(reduced):
        accuracies = [100 * data(rows, method, .5, k, "accuracy") for k in ranks]
        x = ranks + .42*(index-(len(reduced)-1)/2)
        weight = 1.45 if method == "RSSPCA" else 1.05
        acc.errorbar(x, [v.mean() for v in accuracies], yerr=[v.std(ddof=1) for v in accuracies],
                     marker=MARKERS[method], color=COLORS[method], capsize=2, label=method,
                     lw=weight, markersize=4.8)
        if method in PCA_FAMILY:
            errors = [1000 * data(rows, method, .5, k, "mean_mse") for k in ranks]
            x = ranks + .42*(PCA_FAMILY.index(method)-1)
            err.errorbar(x, [v.mean() for v in errors], yerr=[v.std(ddof=1) for v in errors],
                         marker=MARKERS[method], color=COLORS[method], capsize=2,
                         label=method, lw=weight, markersize=4.8)
    acc.set(title="A  Recognition", xlabel="Projected coordinates", ylabel="Accuracy (%)",
            xticks=ranks, ylim=(40, 80), yticks=np.arange(40, 81, 10))
    err.set(title="B  Clean-image reconstruction", xlabel="Projected coordinates",
            ylabel=r"Pixel MSE × $10^3$", xticks=ranks, ylim=(0, None))
    for ax in (acc, err):
        ax.set_xlim(ranks[0]-2, ranks[-1]+2)
        ax.axvline(cfg["primary_rank"], color="#7E8C99", lw=.9, ls="--", zorder=0)
        ax.grid(axis="y")
        ax.legend(loc="upper center", bbox_to_anchor=(.5, -.25), ncol=2,
                  columnspacing=.75, handlelength=1.15, borderaxespad=0)
    return fig


def diagnostics(rows, fits, cfg):
    fig, axes = plt.subplot_mosaic([["rough", "cost"], ["steps", "steps"]],
                                   figsize=(7.1, 4.55), layout="constrained")
    rough, cost, steps = (axes[name] for name in ("rough", "cost", "steps"))
    k = cfg["primary_rank"]
    for i, method in enumerate(PCA_FAMILY):
        energy = data(rows, method, .5, k, "energy")
        rough.scatter(energy, i+np.linspace(-.10, .10, len(energy)),
                      color=COLORS[method], alpha=.55, s=19, linewidths=0)
        rough.scatter(np.mean(energy), i, facecolors="white", s=45,
                      edgecolors=COLORS[method], marker=MARKERS[method])
    rough.set(title="A  Grid energy of unit loadings", xlabel="Mean edge energy per loading",
              yticks=range(3), yticklabels=PCA_FAMILY, ylim=(2.55, -.55))
    for i, method in enumerate(METHODS):
        times = 1000 * data(rows, method, .5, 256 if method=="Pixels" else k, "fit_seconds")
        cost.scatter(times, i+np.linspace(-.10, .10, len(times)),
                     color=COLORS[method], alpha=.55, s=19, linewidths=0)
        cost.scatter(np.median(times), i, facecolors="white", s=45,
                     edgecolors=COLORS[method], marker=MARKERS[method])
    cost.set(title="B  Single-thread fit cost", xlabel=r"Wall time (ms, $\log_{10}$ scale)",
             xscale="log", yticks=range(5), yticklabels=METHODS, ylim=(4.55, -.55))
    for ax in (rough, cost):
        ax.grid(axis="x")
    terminal_step = max(len(trace["step"]) for fit in fits if fit["fraction"] == .5
                        for trace in fit["trace"] if trace["converged"])
    limit = terminal_step + 2
    for method, style in (("No smoothness", "--"), ("RSSPCA", "-")):
        traces = [trace for fit in fits if fit["method"] == method and fit["fraction"] == .5
                  for trace in fit["trace"]]
        counts = sorted(len(trace["step"]) for trace in traces if trace["converged"])
        proportions = np.arange(1, len(counts)+1)/len(traces)
        steps.step([0, *counts, limit], np.r_[0, proportions, len(counts)/len(traces)],
                   where="post", color=COLORS[method], linestyle=style, label=method)
    steps.set(title="C  Steps to the stopping threshold", xlabel="Normalized updates",
              ylabel="Directions stopped (%)", xlim=(0, limit), ylim=(0, 1.06),
              xticks=np.arange(0, limit+1, 5), yticks=np.linspace(0, 1, 5))
    steps.yaxis.set_major_formatter(PercentFormatter(xmax=1, symbol=""))
    steps.grid(axis="y")
    steps.legend(loc="lower right", bbox_to_anchor=(1, 1), ncol=2, borderaxespad=0)
    return fig


def reconstruction_gallery(rows, x, test, models, cfg):
    selected = [np.flatnonzero(test // 10 == label)[0] for label in cfg["gallery_identity_ids"]]
    fig, gs = gallery_axes(len(selected), 4, 4.5)
    fits = [records(rows, m, .5, cfg["primary_rank"])[0] for m in PCA_FAMILY]
    col_images = [x[selected]]
    for run in fits:
        key = run["key"]
        col_images.append(reconstruct(x[selected], models[f"{key}_center"],
                                      models[f"{key}_weights"][:, :cfg["primary_rank"]]))
    for i, index in enumerate(selected):
        label_panel(fig, gs[i, 0], f"ID {test[index]//10:02}\nrow {test[index]}")
        for j, array in enumerate(col_images):
            ax, _ = face_panel(fig, gs[i, j+1], array[i], cmap="gray", vmin=0, vmax=1)
            if not i:
                ax.set_title(("Clean target", *PCA_FAMILY)[j], loc="center")
    return fig


def reconstruction_errors(rows, test, errors, cfg):
    identities = cfg["gallery_identity_ids"]
    selected = [np.flatnonzero(test // 10 == label)[0] for label in identities]
    fig, ax = plt.subplots(figsize=(7.1, 3.1), layout="constrained")
    groups = np.arange(len(identities))
    for index, method in enumerate(PCA_FAMILY):
        run = records(rows, method, .5, cfg["primary_rank"])[0]
        mse = 1000 * errors[run["prediction_key"]][selected]
        ax.scatter(groups + (index-1)*.13, mse, color=COLORS[method], marker=MARKERS[method],
                   s=39, label=method)
    labels = [f"ID {label:02}\nrow {test[index]}" for label, index in
              zip(identities, selected, strict=True)]
    ax.set(xlabel="Prespecified identity and source row", ylabel=r"Pixel MSE × $10^3$",
           xticks=groups, xticklabels=labels, ylim=(0, None))
    ax.grid(axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.28), ncol=3, borderaxespad=0)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results/faces"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--local-image-galleries", action="store_true",
                        help="regenerate the portrait galleries into an ignored local directory")
    args = parser.parse_args()
    cfg = read_json(args.results / "selection.json")["config"]
    rows = read_json(args.results / "final.json")["runs"]
    fits = read_json(args.results / "fits.json")
    split = read_json(args.results / "split.json")
    dev = np.sort(np.r_[split["fit"], split["validation"]])
    test = np.asarray(split["test"])
    out = args.results / "figures"
    out.mkdir(parents=True, exist_ok=True)
    for name in ("lmroman10-regular.otf", "lmroman10-bold.otf",
                 "lmroman10-italic.otf", "latinmodern-math.otf"):
        font_manager.fontManager.addfont(FONT_DIRECTORY / name)
    with (plt.rc_context(STYLE), np.load(args.results / "models.npz") as models,
          np.load(args.results / "reconstruction.npz") as errors):
        export(workflow(), out, "face_workflow")
        export(mechanism(), out, "face_mechanism")
        case = records(rows, "RSSPCA", .5, cfg["primary_rank"])[0]["case"]
        export(mask_figure(dev, models, case, cfg), out, "face_protocol")
        export(loadings(rows, models, cfg), out, "face_loadings")
        export(recognition(rows, cfg), out, "face_recognition")
        export(budget(rows, cfg), out, "face_budget")
        export(diagnostics(rows, fits, cfg), out, "face_diagnostics")
        export(reconstruction_errors(rows, test, errors, cfg), out, "face_reconstruction")
        if args.local_image_galleries:
            local = args.results / "local-image-galleries"
            local.mkdir(parents=True, exist_ok=True)
            train, _ = load_faces(args.data, dev, cfg["image_shape"])
            clean, _ = load_faces(args.data, test, cfg["image_shape"])
            export(mask_gallery(train, dev, models, case, cfg), local, "face_protocol")
            export(reconstruction_gallery(rows, clean, test, models, cfg), local, "face_reconstruction")


if __name__ == "__main__":
    main()
