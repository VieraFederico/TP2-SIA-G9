import argparse
import csv
from pathlib import Path
import re
from secrets import choice

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pkg_resources import require


def main():
    parser = argparse.ArgumentParser(
        description="GA image approximation via triangles."
    )
    parser.add_argument(
        "-s", "--source",
        type=str,
        required=True,
        help="Path to source csv."
    )
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=["selection_method", "mutation_method", "survival_strategy", "crossover_method"],
        default="selection_method",
        help="Method to use for painting and sorting graph (e.g. selection_method, mutation_method, survival_strategy, crossover_method)."
    )

    args = parser.parse_args()
    source_path = Path(args.source)
    paint_by_key = args.method



    if not source_path.exists():
        raise FileNotFoundError(f"CSV file not found: {source_path}")

    rows = []
    with source_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # each row becomes a dict {column_name: value}
        for row in reader:
            rows.append(row)


    rows.sort(key=lambda r: float(r["best_fitness"]))
    for row in rows:
        print(f"run:{row['run_id']}, fitness: {row['best_fitness']}, selection: {row['selection_method']}, mutation: {row['mutation_method']}, "
              f"crossover: {row['crossover_method']}, survival: {row['survival_strategy']}")




    scatter_path = source_path.with_name(
        f"{source_path.stem}_fitness_scatter_by_{paint_by_key}.png"
    )
    boxplot_path = source_path.with_name(
        f"{source_path.stem}_fitness_boxplot_by_{paint_by_key}.png"
    )

    scatter_fitness_abs_vs_run_id_by_selection(rows, paint_by_key, scatter_path)
    boxplot_fitness_abs_by_selection(rows, paint_by_key, boxplot_path)

    print(f"Scatter plot saved to: {scatter_path}")
    print(f"Boxplot saved to: {boxplot_path}")

    return


def _run_id_to_number(run_id: str, fallback: int) -> int:
    """
    Convert run_id like 'run_0012' (or '12') to an integer.
    Falls back to row position if parsing fails.
    """
    if run_id is None:
        return fallback

    match = re.search(r"\d+", str(run_id))
    return int(match.group()) if match else fallback


def scatter_fitness_abs_vs_run_id_by_selection(rows: list[dict], paint_by_key: str, output_path: Path) -> Path:
    """
    Scatter plot:
    - X axis: paint_by_key categories (sorted)
    - Y axis: |best_fitness|
    - Color: paint_by_key category
    """
    if not rows:
        raise ValueError("No rows available to plot.")

    # group -> y values
    grouped_values: dict[str, list[float]] = {}

    for row in rows:
        fitness_raw = row.get("best_fitness")
        if fitness_raw in (None, ""):
            continue

        try:
            y = abs(float(fitness_raw))
        except ValueError:
            continue

        group_name = row.get(paint_by_key, "unknown")
        grouped_values.setdefault(group_name, []).append(y)

    if not grouped_values:
        raise ValueError("No valid points found in CSV.")

    methods = sorted(grouped_values.keys())  # sorted axis by paint_by_key
    method_to_x = {m: i for i, m in enumerate(methods)}

    cmap = plt.get_cmap("tab20")
    method_colors = {m: cmap(i % cmap.N) for i, m in enumerate(methods)}

    fig, ax = plt.subplots(figsize=(11, 6))

    for method in methods:
        y_values = grouped_values[method]
        x_center = method_to_x[method]

        # Small deterministic spread around each category for readability
        n = len(y_values)
        if n == 1:
            x_values = [x_center]
        else:
            span = 0.28
            step = (2 * span) / (n - 1)
            x_values = [x_center - span + i * step for i in range(n)]

        ax.scatter(
            x_values,
            y_values,
            label=method,
            color=method_colors[method],
            alpha=0.85,
            s=32,
            edgecolors="none",
        )

    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=20, ha="right")
    ax.set_title(f"Absolute Fitness by {paint_by_key}")
    ax.set_xlabel(paint_by_key)
    ax.set_ylabel("|best_fitness|")
    ax.grid(True, alpha=0.3)
    ax.legend(title=paint_by_key, fontsize=8, title_fontsize=9, loc="best")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path



def boxplot_fitness_abs_by_selection(rows: list[dict], paint_by_key: str, output_path: Path) -> Path:
    """
    Single-axis figure:
    - Boxplot: Y=|best_fitness| grouped by paint_by_key
    """
    if not rows:
        raise ValueError("No rows available to plot.")

    grouped_values: dict[str, list[float]] = {}

    for row in rows:
        fitness_raw = row.get("best_fitness")
        if fitness_raw in (None, ""):
            continue

        try:
            y = abs(float(fitness_raw))
        except ValueError:
            continue

        group_name = row.get(paint_by_key, "unknown")
        grouped_values.setdefault(group_name, []).append(y)

    if not grouped_values:
        raise ValueError("No valid points found in CSV.")

    methods = sorted(grouped_values.keys())
    data = [grouped_values[m] for m in methods]

    cmap = plt.get_cmap("tab20")
    method_colors = {m: cmap(i % cmap.N) for i, m in enumerate(methods)}

    fig, ax = plt.subplots(figsize=(12, 7))
    bp = ax.boxplot(
        data,
        patch_artist=True,
        showfliers=True,

    )

    for patch, method in zip(bp["boxes"], methods):
        color = method_colors[method]
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    for whisker in bp["whiskers"]:
        whisker.set_linestyle(":")
        whisker.set_linewidth(1.2)

    for cap in bp["caps"]:
        cap.set_linestyle(":")
        cap.set_linewidth(1.2)

    for median in bp["medians"]:
        median.set_linewidth(2)

    ax.set_title(f"Absolute Fitness Distribution by {paint_by_key}")
    ax.set_xlabel(paint_by_key)
    ax.set_ylabel("|best_fitness|")
    ax.grid(True, axis="y", alpha=0.3)

    # Custom legend: same method->color mapping as scatter style
    legend_handles = [
        Patch(facecolor=method_colors[m], edgecolor=method_colors[m], alpha=0.5, label=m)
        for m in methods
    ]
    ax.legend(handles=legend_handles, title=paint_by_key, fontsize=8, title_fontsize=9, loc="best")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    main()
