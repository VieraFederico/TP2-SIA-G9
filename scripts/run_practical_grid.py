#!/usr/bin/env python3
"""
Run a practical subset of GA configurations for TP2-SIA-G9.

Why config-per-run?
- Your parser reads many params only from config (e.g., elite_pop_percentage, pc, p_tweak/p_insert/p_delete).
- See `utils/cmd_parser.py` + `genetics_algorithm/settings.py`.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run practical GA grid with repeats.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root (default: parent of this script's directory).",
    )
    parser.add_argument(
        "--base-config",
        type=Path,
        default=Path("genetics_algorithm/config.json"),
        help="Base config JSON path (relative to project root unless absolute).",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Repeats per hyperparameter combination (default: 3).",
    )
    parser.add_argument(
        "--max-generations",
        type=int,
        default=600,
        help="Override max_generations for all runs (default: 600).",
    )
    parser.add_argument(
        "--polygons",
        type=int,
        default=20,
        help="Number of polygons per individual (default: 20).",
    )

    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Optional image path override for all runs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned runs only; do not execute.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run only first N planned runs (useful for smoke tests).",
    )
    return parser.parse_args()


def resolve_path(project_root: Path, p: Path) -> Path:
    return p if p.is_absolute() else (project_root / p)


def run_cmd(cmd: list[str], cwd: Path, log_path: Path) -> tuple[int, float]:
    start = time.perf_counter()
    with open(log_path, "w", encoding="utf-8") as f_log:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=f_log,
            stderr=subprocess.STDOUT,
            text=True,
        )
    elapsed = time.perf_counter() - start
    return completed.returncode, elapsed


def build_grid() -> Iterable[tuple]:
    # Practical subset (high-signal, much smaller than exhaustive).
    selections = [
        "elite",
        "roulette",
        "deterministic_tournament",
        "probabilistic_tournament"
    ]
    mutations = [
        "gen",
        "multi_gen",
        "non_uniform",
    ]
    crossovers = [
        "one_point",
        "uniform",
    ]
    survivals = [
        "exclusive",
        "additive",
    ]
    pms = [0.4]
    elite_pcts = [0.05]
    pcs = [0.5]

    return itertools.product(
        selections,
        mutations,
        crossovers,
        survivals,
        pms,
        elite_pcts,
        pcs,
    )


def main() -> int:
    args = parse_args()

    project_root = args.project_root.resolve()
    base_config_path = resolve_path(project_root, args.base_config)

    if not base_config_path.exists():
        print(f"ERROR: base config not found: {base_config_path}", file=sys.stderr)
        return 1

    with open(base_config_path, "r", encoding="utf-8") as f:
        base_cfg = json.load(f)

    runs_root = project_root / "experiments" / "practical_grid"
    configs_dir = runs_root / "configs"
    logs_dir = runs_root / "logs"
    reports_dir = runs_root / "reports"
    configs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    summary_csv = reports_dir / "summary.csv"

    base_grid = list(build_grid())
    all_runs: list[tuple] = []
    for combo in base_grid:
        for rep in range(1, args.repeats + 1):
            all_runs.append((*combo, rep))

    if args.limit is not None:
        all_runs = all_runs[: max(0, args.limit)]

    total = len(all_runs)
    print(f"Planned runs: {total}")

    if args.dry_run:
        for i, run in enumerate(all_runs[:15], start=1):
            print(f"{i:03d}: {run}")
        if total > 15:
            print("... (truncated)")
        return 0

    with open(summary_csv, "w", newline="", encoding="utf-8") as f_csv:
        writer = csv.DictWriter(
            f_csv,
            # scripts/run_practical_grid.py

            # 1) Add column name in CSV header list
            fieldnames=[
                "run_id",
                "selection_method",
                "mutation_method",
                "crossover_method",
                "survival_strategy",
                "pm",
                "elite_pop_percentage",
                "pc",
                "repeat",
                "max_generations",
                "polygons",
                "image_path",
                "returncode",
                "runtime_s",
                "config_path",
                "log_path",
            ],

        )
        writer.writeheader()

        for run_id, run in enumerate(all_runs, start=1):
            (
                selection,
                mutation,
                crossover,
                survival,
                pm,
                elite_pct,
                pc,
                repeat,
            ) = run

            cfg = dict(base_cfg)
            cfg["selection_method"] = selection
            cfg["mutation_method"] = mutation
            cfg["crossover_method"] = crossover
            cfg["survival_strategy"] = survival
            cfg["triangles_per_canvas"] = args.polygons
            cfg["pm"] = pm
            cfg["elite_pop_percentage"] = elite_pct
            cfg["pc"] = pc
            cfg["max_generations"] = args.max_generations
            if args.image:
                cfg["image_path"] = args.image

            tag = (
                f"r{run_id:04d}"
                f"_sel-{selection}"
                f"_mut-{mutation}"
                f"_cross-{crossover}"
                f"_surv-{survival}"
                f"_pm-{pm}"
                f"_elite-{elite_pct}"
                f"_pc-{pc}"
                f"_rep-{repeat}"
            )
            cfg["output_suffix"] = run_id

            cfg_path = configs_dir / f"{tag}.json"
            log_path = logs_dir / f"{tag}.log"

            with open(cfg_path, "w", encoding="utf-8") as f_cfg:
                json.dump(cfg, f_cfg, indent=2)

            cmd = [sys.executable, "main.py", "--config", str(cfg_path)]
            print(f"[{run_id}/{total}] {' '.join(cmd)}")

            returncode, runtime_s = run_cmd(cmd, cwd=project_root, log_path=log_path)

            writer.writerow(
                {
                    "run_id": run_id,
                    "selection_method": selection,
                    "mutation_method": mutation,
                    "crossover_method": crossover,
                    "survival_strategy": survival,
                    "pm": pm,
                    "elite_pop_percentage": elite_pct,
                    "pc": pc,
                    "repeat": repeat,
                    "max_generations": args.max_generations,
                    "polygons": args.polygons,
                    "image_path": cfg.get("image_path", ""),
                    "returncode": returncode,
                    "runtime_s": f"{runtime_s:.3f}",
                    "config_path": str(cfg_path),
                    "log_path": str(log_path),
                }
            )
            f_csv.flush()

    print(f"Done. Summary CSV: {summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
