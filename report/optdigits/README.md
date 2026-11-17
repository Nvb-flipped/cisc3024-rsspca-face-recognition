# Archived Optdigits study

Prompt 01 used UCI Optdigits as its primary application. Its writer-disjoint protocol, code and verified records were preserved when Prompt 01B made faces primary. [Prompt 01 design](../../docs/study_design.md) · [AI use record](../../docs/ai_usage.md)

The two digit PDFs and their source preserve the wording at their original review stages. The current submission report includes the live repository and Wiki links in Section 6. [Face-primary report](../report.pdf)

- [Original 10-page PDF](prompt01-initial.pdf)
- [Expanded 14-page Latin Modern PDF](report.pdf) and [LaTeX source](report.tex)
- [Original configuration](../../configs/study.json), [validation selection](../../results/selection.json), [frozen record](../../results/frozen.json), [predictions](../../results/predictions.npz) and [results](../../results/final.json)

The same project-root commands reproduce the archived digit results in a fresh directory. The raw Optdigits files are fetched from UCI.

```text
python -m src.experiment fetch-tra
python scripts/gate_probe.py data/optdigits.tra
python -m src.experiment smoke
python -m src.experiment tune --out results/reproduction/digit-replay
python -m src.experiment prepare --out results/reproduction/digit-replay
python -m src.experiment fetch-tes --out results/reproduction/digit-replay
python -m src.experiment final --out results/reproduction/digit-replay
python -m src.experiment verify --out results/reproduction/digit-replay --against results
python -m src.summarize --write-tex report/optdigits/results_table.tex
python -m src.figures
```

Compile from this archive directory with `tectonic -X compile --untrusted report.tex` or `latexmk -xelatex report.tex`. The archive points to the same figure and font files as the baseline. The full verified digit workspace is also recorded on local branch `study/optdigits-baseline`, commit `181d542`.
