#!/usr/bin/env python3
"""Draw the coverage figures proposed for the HCMO article.

Reads the same mapping tables as ``tooling/evaluate.py`` and reuses its Wilson
interval, so every number in a figure equals the one in
``evaluation/reports/coverage.md``. Writes PDF (for the paper) and PNG (for
review) under ``evaluation/figures/``:

  coverage-by-system   stacked mapping kinds per system, native share with 95 % CI
  coverage-by-module   HCMO-native share per system x module (k/n in each cell)
  gaps-by-system       modelling gaps of HCMO 0.3.0 against the systems they affect

All values describe mappings of synthetic exports made by a single annotator
(see evaluation/CONTRIBUTOR-REVIEW.md); the figures are provisional until the
mappings are independently reviewed.

Needs matplotlib (not part of the CI requirements):
  pip install matplotlib
  python evaluation/plots.py
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tooling"))
from evaluate import MODULE_NAMESPACES, coverage_stats, load_index, read_mapping, wilson_interval  # noqa: E402

OUT = ROOT / "evaluation" / "figures"

SHORT_NAMES = {
    "dvc-tecniplast": "Tecniplast DVC",
    "tse-phenomaster": "TSE PhenoMaster",
    "noldus-phenotyper": "Noldus PhenoTyper",
    "fed3": "FED3",
    "live-mouse-tracker": "Live Mouse Tracker",
    "beatbox": "BEATBox",
}

# Mapping kinds are ordered (native -> lossy -> absent): one blue ramp, dark to
# light (validated as an ordinal ramp on the light surface), then neutral grey.
KIND_COLORS = {
    "hcmo": "#104281",
    "external": "#3987e5",
    "partial": "#86b6ef",
    "not-covered": "#d4d3cf",
}
KIND_LABELS = {
    "hcmo": "HCMO term",
    "external": "external term",
    "partial": "partial / generic",
    "not-covered": "not covered",
}
ABBREVIATIONS = {
    "dvc-tecniplast": "DVC",
    "tse-phenomaster": "TSE",
    "noldus-phenotyper": "Noldus",
    "fed3": "FED3",
    "live-mouse-tracker": "LMT",
    "beatbox": "BEATBox",
}
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_MUTED = "#52514e"
GRID = "#e4e3df"

# Gaps of HCMO 0.3.0 and the systems whose mapping table records them
# (partial or not-covered rows in docs/hcm-systems/systems/*/hcmo-mapping.tsv).
GAPS = [
    ("No task / trial / session vocabulary", ["beatbox", "fed3", "noldus-phenotyper"]),
    ("No n-ary behavioural event with roles", ["live-mouse-tracker"]),
    ("No subtype for numeric activity/metabolic/operant results",
     ["dvc-tecniplast", "tse-phenomaster", "noldus-phenotyper", "fed3", "beatbox"]),
    ("No genotype property", ["live-mouse-tracker"]),
    ("ExperimentalGroup cannot carry strain or sex", ["dvc-tecniplast"]),
    ("Location and arena zones have no history", ["dvc-tecniplast", "noldus-phenotyper", "live-mouse-tracker"]),
    ("No subject identifier property", ["tse-phenomaster", "noldus-phenotyper", "fed3", "live-mouse-tracker", "beatbox"]),
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 7,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT_MUTED,
    "xtick.color": TEXT_MUTED,
    "ytick.color": TEXT,
    "axes.titlesize": 8,
    "axes.titleweight": "bold",
    "svg.hashsalt": "hcmo",
})
PDF_METADATA = {"CreationDate": None, "Producer": None, "Creator": "evaluation/plots.py"}
PNG_METADATA = {"Software": None}


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf", metadata=PDF_METADATA, facecolor=SURFACE)
    fig.savefig(OUT / f"{name}.png", dpi=300, metadata=PNG_METADATA, facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote evaluation/figures/{name}.pdf and .png")


def system_stats(index: dict) -> list[tuple[str, dict]]:
    return [(s["id"], coverage_stats(read_mapping(ROOT / s["mapping"]))) for s in index["systems"]]


def coverage_by_system(stats: list[tuple[str, dict]]) -> None:
    pooled = Counter()
    for _, st in stats:
        pooled.update(st["kinds"])
    rows = sorted(stats, key=lambda item: item[1]["native"] / item[1]["total"])
    labels = [SHORT_NAMES[sid] for sid, _ in rows] + ["All systems"]
    kinds = [st["kinds"] for _, st in rows] + [pooled]
    totals = [sum(k[m] for m in KIND_COLORS) for k in kinds]

    fig, ax = plt.subplots(figsize=(4.8, 2.4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    y = list(range(len(labels)))
    for i, (k, n) in enumerate(zip(kinds, totals)):
        left = 0.0
        for kind, color in KIND_COLORS.items():
            width = 100.0 * k[kind] / n
            ax.barh(i, width, left=left, height=0.62, color=color, edgecolor=SURFACE, linewidth=1.0)
            left += width
        native = 100.0 * k["hcmo"] / n
        low, high = wilson_interval(k["hcmo"], n)
        ax.errorbar(native, i, xerr=[[native - low], [high - native]], fmt="none",
                    ecolor=TEXT, elinewidth=0.8, capsize=2.0, capthick=0.8)
        ax.text(1.5, i, f"{native:.0f}%", ha="left", va="center", color="#ffffff", fontsize=6.5)
        ax.text(101.5, i, f"n = {n}", ha="left", va="center", color=TEXT_MUTED, fontsize=6.5)
    ax.axhline(len(labels) - 1.5, color=GRID, linewidth=0.8)
    ax.set_yticks(y, labels)
    ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100 %"])
    ax.set_xlabel("share of the system's native concepts")
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in KIND_COLORS.values()]
    ax.legend(handles, KIND_LABELS.values(), ncol=4, loc="lower left", bbox_to_anchor=(0, 1.0),
              frameon=False, fontsize=6.5, handlelength=1.0, columnspacing=1.0, borderaxespad=0.3)
    fig.tight_layout()
    save(fig, "coverage-by-system")


def coverage_by_module(index: dict) -> None:
    systems = [s["id"] for s in index["systems"]]
    modules = list(MODULE_NAMESPACES)
    cells: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for system in index["systems"]:
        for row in read_mapping(ROOT / system["mapping"]):
            cells[(system["id"], row["module"])][row["mapping"]] += 1
            cells[("pooled", row["module"])][row["mapping"]] += 1
    row_ids = systems + ["pooled"]

    fig, ax = plt.subplots(figsize=(4.8, 2.3), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for r, sid in enumerate(row_ids):
        for c, module in enumerate(modules):
            counts = cells.get((sid, module), Counter())
            n = sum(counts.values())
            if n == 0:
                ax.add_patch(plt.Rectangle((c, r), 1, 1, facecolor=SURFACE, edgecolor=SURFACE, linewidth=2))
                ax.text(c + 0.5, r + 0.5, "—", ha="center", va="center", color=TEXT_MUTED)
                continue
            share = counts["hcmo"] / n
            color = SEQUENTIAL[min(int(share * len(SEQUENTIAL)), len(SEQUENTIAL) - 1)]
            ax.add_patch(plt.Rectangle((c, r), 1, 1, facecolor=color, edgecolor=SURFACE, linewidth=2))
            ink = "#ffffff" if share >= 3 / len(SEQUENTIAL) else TEXT
            ax.text(c + 0.5, r + 0.5, f"{counts['hcmo']}/{n}", ha="center", va="center", color=ink,
                    fontsize=6.5, fontweight="bold" if sid == "pooled" else "normal")
    ax.set_xlim(0, len(modules))
    ax.set_ylim(len(row_ids), 0)
    ax.set_xticks([c + 0.5 for c in range(len(modules))], [f"hcm-{m}" if m != "core" else "hcm (core)" for m in modules])
    ax.xaxis.tick_top()
    ax.set_yticks([r + 0.5 for r in range(len(row_ids))], [SHORT_NAMES.get(s, "All systems") for s in row_ids])
    ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    sm = plt.cm.ScalarMappable(cmap=matplotlib.colors.ListedColormap(SEQUENTIAL), norm=plt.Normalize(0, 100))
    bar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
    bar.set_label("HCMO-native share (%)", color=TEXT_MUTED, fontsize=6.5)
    bar.outline.set_visible(False)
    bar.ax.tick_params(labelsize=6, length=0)
    fig.tight_layout()
    save(fig, "coverage-by-module")


def gaps_by_system(index: dict) -> None:
    systems = [s["id"] for s in index["systems"]]
    fig, ax = plt.subplots(figsize=(4.8, 2.2), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for r, (_, hit) in enumerate(GAPS):
        ax.axhline(r, color=GRID, linewidth=0.6, zorder=0)
        for c, sid in enumerate(systems):
            if sid in hit:
                ax.scatter(c, r, s=38, color=KIND_COLORS["hcmo"], edgecolors=SURFACE, linewidths=1.5, zorder=2)
        ax.text(len(systems) - 0.4, r, str(len(hit)), ha="left", va="center", color=TEXT_MUTED, fontsize=6.5)
    ax.set_xlim(-0.6, len(systems) - 0.2)
    ax.set_ylim(len(GAPS) - 0.5, -0.5)
    ax.set_xticks(range(len(systems)), [ABBREVIATIONS[s] for s in systems], rotation=45, ha="left")
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(GAPS)), [g for g, _ in GAPS])
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.text(len(systems) - 0.4, -0.7, "n", ha="left", va="bottom", color=TEXT_MUTED, fontsize=6.5)
    fig.tight_layout()
    fig.subplots_adjust(right=0.94)
    save(fig, "gaps-by-system")


def main() -> int:
    index = load_index()
    known = {s["id"] for s in index["systems"]}
    for _, hit in GAPS:
        unknown = set(hit) - known
        if unknown:
            raise SystemExit(f"GAPS names unknown systems: {sorted(unknown)}")
    coverage_by_system(system_stats(index))
    coverage_by_module(index)
    gaps_by_system(index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
