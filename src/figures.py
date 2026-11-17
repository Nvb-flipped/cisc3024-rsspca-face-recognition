"""Generate vector figures from the locked plan, masks, fits and predictions."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.ticker import MultipleLocator, PercentFormatter

from src.data import apply_masks, load_partition
from src.experiment import read_json

INK = "#182432"
MUTED = "#4A5C6D"
PALE = "#EAF2F7"
GRID = "#DCE5EC"
FRACTIONS = (0, .25, .5)
METHODS = ("Pixels", "PCA", "LDA", "No smoothness", "RSSPCA")
COLORS = dict(zip(METHODS, ("#5B6571", "#00619B", "#9C4C14",
                            "#70498B", "#00755B"), strict=True))
MARKERS = dict(zip(METHODS, ("X", "s", "^", "D", "o"), strict=True))
FONT_DIRECTORY = Path(__file__).resolve().parents[1] / "report" / "fonts"
STYLE = {
    "font.family": "Latin Modern Roman", "font.size": 10, "axes.labelsize": 10,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "legend.fontsize": 8.8, "legend.frameon": False,
    "grid.color": GRID, "axes.axisbelow": True, "pdf.fonttype": 42,
    "svg.fonttype": "path", "mathtext.fontset": "custom", "mathtext.fallback": None,
    "mathtext.rm": "Latin Modern Math", "mathtext.it": "Latin Modern Roman:italic",
    "mathtext.bf": "Latin Modern Roman:bold", "mathtext.sf": "Latin Modern Roman",
}


def data_rows(rows, method, fraction, rank=8):
    rank = 64 if method == "Pixels" else rank
    return sorted([r for r in rows if (r["method"], r["fraction"], r["rank"]) ==
                   (method, fraction, rank)], key=lambda r: r["seed"])


def values(rows, method, fraction, rank=8, key="accuracy"):
    return np.array([row[key] for row in data_rows(rows, method, fraction, rank)])


def export(fig, out, name):
    for extension in ("pdf", "svg"):
        fig.savefig(out / f"{name}.{extension}", dpi=400, facecolor="white")
    plt.close(fig)


def diagram(cards, footer):
    fig, ax = plt.subplots(figsize=(7.1, 1.43))
    fig.subplots_adjust(left=.005, right=.995, bottom=.03, top=.97)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    for i, (title, text) in enumerate(cards):
        x = .009 + i * .253
        ax.add_patch(FancyBboxPatch((x, .28), .223, .65, boxstyle="round,pad=0.006",
                                    fc=PALE if i != 2 else "#DDEFE8", ec="none"))
        ax.text(x + .013, .79, title, weight="bold", fontsize=10.1, va="top")
        ax.text(x + .013, .60, text, fontsize=8.9, va="top", linespacing=1.38)
        if i < len(cards) - 1:
            ax.annotate("", (x + .25, .60), (x + .226, .60),
                        arrowprops={"arrowstyle": "-|>", "lw": 1, "color": MUTED,
                                    "shrinkA": 0, "shrinkB": 0})
    ax.text(.011, .08, footer, fontsize=9.2, color=MUTED)
    return fig


def dataset_figure(x, y, fitted):
    fig = plt.figure(figsize=(7.1, 2.68), layout="constrained")
    gs = fig.add_gridspec(2, 10, height_ratios=[1., 1.45])
    for label in range(10):
        ax = fig.add_subplot(gs[0, label])
        index = np.flatnonzero(y == label)[0]
        ax.imshow(x[index].reshape(8, 8), cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(f"{'A  ' if label == 0 else ''}{label}", loc="center", fontsize=9)
        ax.axis("off")
    ax = fig.add_subplot(gs[1, :6])
    ax.plot(np.arange(10), np.bincount(y), "o", color=COLORS["PCA"])
    ax.set(ylim=(370, 395), xticks=np.arange(10), yticks=[375, 385, 395],
           title="B  Development counts", ylabel="Images", xlabel="Digit")
    ax.grid(axis="y")
    mask_rows = fitted["s6_rows"]
    index = int(mask_rows[0])
    corrupt = apply_masks(x, mask_rows[:1], fitted["s6_locations"][:1],
                          fitted["s6_patches"][:1], (8, 8), 4)
    for columns, images, title in ((slice(6, 8), x, "C  Original"),
                                   (slice(8, 10), corrupt, "Training patch")):
        image_ax = fig.add_subplot(gs[1, columns])
        image_ax.imshow(images[index].reshape(8, 8), cmap="Greys", vmin=0, vmax=1,
                        interpolation="nearest")
        image_ax.set_title(title, fontsize=9.5)
        image_ax.axis("off")
        if images is corrupt:
            r, c = fitted["s6_locations"][0]
            image_ax.add_patch(Rectangle((c - .5, r - .5), 4, 4, fill=False,
                                         lw=1.4, edgecolor="#B35B26"))
    return fig


def comparison_figure(rows):
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.02), layout="constrained",
                             gridspec_kw={"width_ratios": [1.03, 1]})
    ax, contrast = axes
    for idx, method in enumerate(METHODS):
        means = []
        for i, fraction in enumerate(FRACTIONS):
            scores = 100 * values(rows, method, fraction)
            offset = (idx - 2) * .058
            if len(scores) > 1:
                ax.scatter(i + offset + np.linspace(-.025, .025, len(scores)), scores,
                           s=9, color=COLORS[method], alpha=.42, linewidths=0)
            means.append(scores.mean())
        ax.plot(np.arange(3) + offset, means, marker=MARKERS[method],
                ms=4.2, lw=1.2, color=COLORS[method], label=method)
    ax.set(title="A  Held-out recognition", xlabel="Training rows corrupted",
           ylabel="Accuracy (%)", xticks=[0, 1, 2], xticklabels=["0%", "25%", "50%"],
           ylim=(89, 99.4))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.grid(axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.25), ncol=3,
              columnspacing=.7, handlelength=1.15, handletextpad=.38,
              borderaxespad=0, labelspacing=.35)

    contrast.axvline(0, color=MUTED, lw=1, linestyle="--")
    for f, color in ((.25, "#00755B"), (.50, "#9C4C14")):
        for k, method in enumerate(("PCA", "LDA", "No smoothness")):
            scores = 100 * (values(rows, "RSSPCA", f) - values(rows, method, f))
            y = k + (-.15 if f == .25 else .15)
            contrast.scatter(scores, y + np.linspace(-.035, .035, len(scores)),
                             s=15, color=color, alpha=.52, linewidths=0)
            contrast.scatter(scores.mean(), y, s=38, marker="D", facecolor="white",
                             edgecolor=color, zorder=4, label=f"{f:.0%} training" if k == 0 else None)
    contrast.set(title="B  Paired differences", xlabel="RSSPCA minus comparator (pp)",
                 yticks=[0, 1, 2], yticklabels=["PCA", "LDA", "No smooth."],
                 ylim=(2.85, -.48), xlim=(-2.05, 1.16))
    contrast.grid(axis="x")
    contrast.legend(loc="upper center", bbox_to_anchor=(.5, -.25), ncol=2,
                    handletextpad=.35, columnspacing=.85, borderaxespad=0)
    return fig


def sensitivity_figure(rows):
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.56), layout="constrained",
                             gridspec_kw={"width_ratios": [1.12, 1]})
    ax, cost = axes
    for method in METHODS[1:]:
        ranks = [4, 8] if method == "LDA" else [4, 8, 16, 24]
        scores = [100 * values(rows, method, .5, rank) for rank in ranks]
        ax.errorbar(ranks, [v.mean() for v in scores], yerr=[v.std(ddof=1) for v in scores],
                    color=COLORS[method], marker=MARKERS[method], markersize=4.7,
                    label=method, capsize=2, lw=1.2,
                    linestyle="--" if method == "No smoothness" else "-")
    ax.axhline(100 * values(rows, "Pixels", .5).mean(), color=COLORS["Pixels"],
               lw=1, linestyle=":", label="Pixels (64)")
    ax.set(title="A  Feature budget", xlabel="Projected coordinates",
           ylabel="Accuracy (%)", xticks=[4, 8, 16, 24], ylim=(70, 100))
    ax.grid(axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.32), ncol=3,
              columnspacing=.6, handlelength=1.1, handletextpad=.35, borderaxespad=0)
    for i, method in enumerate(METHODS):
        records = data_rows(rows, method, .5)
        values_ms = [1000 * r["fit_seconds"] for r in records]
        cost.scatter(values_ms, i + np.linspace(-.10, .10, len(records)), s=14, alpha=.58,
                     color=COLORS[method], linewidths=0)
        cost.scatter(np.median(values_ms), i, s=42, edgecolor=COLORS[method], marker=MARKERS[method],
                     zorder=3, facecolor="white")
    cost.set(title="B  Fit time", xlabel="Fit wall time (ms)",
             yticks=np.arange(len(METHODS)), yticklabels=METHODS, ylim=(4.55, -.55),
             xlim=(0, max(1000*r["fit_seconds"] for r in rows if r["fraction"] == .5
                          and r["rank"] in (8,64)) * 1.11))
    cost.grid(axis="x")
    return fig


def loading_figure(rows, fit_rows, fitted):
    fig = plt.figure(figsize=(7.1, 2.60), layout="constrained")
    gs = fig.add_gridspec(3, 6, width_ratios=[1.32, .67, .67, .67, .18, 2.85])
    names = ["PCA", "No smoothness", "RSSPCA"]
    selected = [data_rows(rows, m, .5)[0] for m in names]
    columns = [fitted[f"{r['key']}_weights"][:, :3] for r in selected]
    extent = np.max(np.abs(columns))
    image_axes = []
    for i, (method, weights, row) in enumerate(zip(names, columns, selected, strict=True)):
        label = fig.add_subplot(gs[i, 0])
        label.axis("off")
        label.text(.02, .50, f"{method}\nEnergy {row['unit_direction_energy']:.2f}",
                   fontsize=8.8, va="center", linespacing=1.25)
        if i == 0:
            label.set_title("A  Loadings", fontsize=10)
        for j in range(3):
            ax = fig.add_subplot(gs[i, j + 1])
            image = ax.imshow(weights[:, j].reshape(8, 8), cmap="RdBu_r", vmin=-extent, vmax=extent,
                              interpolation="nearest")
            ax.axis("off")
            if i == 0:
                ax.set_title(f"$w_{j+1}$", fontsize=10, loc="center")
            image_axes.append(ax)
    bar = fig.colorbar(image, ax=image_axes, location="bottom", fraction=.075, pad=.035,
                       aspect=24)
    bar.set_label("Loading weight", fontsize=9)
    c = fig.add_subplot(gs[:, 5])
    for m in names[1:]:
        record = data_rows(fit_rows, m, .5, 24)[0]
        for idx, trace in enumerate(record["trace"][:8]):
            c.semilogy(np.arange(1, len(trace["step"])+1),
                       np.maximum(trace["step"], 1e-12), color=COLORS[m], lw=1,
                       linestyle="--" if m == "No smoothness" else "-",
                       alpha=.62, label=m if idx == 0 else None)
    c.axhline(1e-4, color=MUTED, lw=1, linestyle=":")
    c.set(title="B  Loading updates", xlabel="Iteration", ylabel="Step norm")
    c.grid(axis="y")
    c.legend(loc="upper center", bbox_to_anchor=(.5, -.32), ncol=2, columnspacing=.85,
             handletextpad=.35, borderaxespad=0)
    return fig


def class_figure(rows):
    fig, (ax, recall) = plt.subplots(1, 2, figsize=(7.1, 2.94), layout="constrained",
                                     gridspec_kw={"width_ratios": [1.13, 1]})
    rss = np.array(data_rows(rows, "RSSPCA", .5)[0]["confusion"])
    norm = rss / rss.sum(axis=1, keepdims=True)
    im = ax.imshow(norm, cmap="Blues", vmin=0, vmax=1, interpolation="nearest")
    for i, j in np.argwhere(rss > 0):
        ax.text(j, i, str(rss[i, j]), va="center", ha="center", fontsize=8.5,
                color="white" if norm[i, j] > .53 else INK)
    ax.set(title="A  RSSPCA confusions", xticks=range(10), yticks=range(10),
           xlabel="Predicted digit", ylabel="True digit")
    ax.spines[["top", "right"]].set_visible(True)
    cbar = fig.colorbar(im, ax=ax, fraction=.046, pad=.035)
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    for method in ("PCA", "LDA", "RSSPCA"):
        matrix = np.array(data_rows(rows, method, .5)[0]["confusion"])
        r = matrix.diagonal() / matrix.sum(axis=1)
        recall.plot(np.arange(10), r * 100, label=method, color=COLORS[method],
                    marker=MARKERS[method], markersize=4, lw=1)
    recall.set(title="B  Recall by true digit", xlabel="Digit", ylabel="Recall (%)",
               xticks=range(10), ylim=(60, 102))
    recall.grid(axis="y")
    recall.legend(loc="lower left", ncol=3, columnspacing=.7, handlelength=1.35)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--data", type=Path, default=Path("data"))
    args = parser.parse_args()
    out = args.results / "figures"
    out.mkdir(parents=True, exist_ok=True)
    # Register the same font files used by LaTeX, independent of machine fonts.
    for filename in ("lmroman10-regular.otf", "lmroman10-bold.otf",
                     "lmroman10-italic.otf", "latinmodern-math.otf"):
        font_manager.fontManager.addfont(FONT_DIRECTORY / filename)
    rows = read_json(args.results / "final.json")["runs"]
    fit_rows = read_json(args.results / "fit_records.json")
    x, y, _ = load_partition(args.data, "tra")
    with plt.rc_context(STYLE), np.load(args.results / "fitted.npz") as fitted:
        export(diagram([
            ("Instructions", "Handout · AGENTS.md\nPrompt 01"),
            ("Codex research", "Use research skills\nScreen primary papers"),
            ("Decision gate", "Exact toy update\nDevelopment smoke"),
            ("Execute and report", "Validate and freeze\nScore held-out data"),
        ], "Prompt 01 produces the technical draft. Critical review and publication are subsequent stages."),
               out, "workflow")
        export(diagram([
            ("Center and start", "Fit training mean\nUse residual PCA axis"),
            ("Build sign votes", r"$v=R^\mathsf{T}\,\mathrm{sign}(Rw)$" + "\nUse four-neighbor graph"),
            ("Update loading", "Solve the SPD system\nNormalize to unit length"),
            ("Deflate and score", "Remove learned span\nUse raw scores in 3-NN"),
        ], "Repeat the middle steps to tolerance or iteration cap. Repeat extraction to reach the feature budget."),
               out, "solver")
        export(dataset_figure(x, y, fitted), out, "dataset")
        export(comparison_figure(rows), out, "comparison")
        export(sensitivity_figure(rows), out, "sensitivity")
        export(loading_figure(rows, fit_rows, fitted), out, "loadings")
        export(class_figure(rows), out, "class_errors")


if __name__ == "__main__":
    main()
