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

# ---------------------------------------------------------------------------
# Terminal colors (ANSI, no external deps)
# ---------------------------------------------------------------------------
_USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text


def green(t: str) -> str:   return _c("32;1", t)
def red(t: str) -> str:     return _c("31;1", t)
def yellow(t: str) -> str:  return _c("33;1", t)
def cyan(t: str) -> str:    return _c("36;1", t)
def bold(t: str) -> str:    return _c("1", t)
def dim(t: str) -> str:     return _c("2", t)


def _sep(char: str = "─", width: int = 72) -> str:
    return dim(char * width)


def _tail_log(log_path: Path, n: int = 15) -> list[str]:
    """Return the last *n* non-empty lines of a log file."""
    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
        non_empty = [l for l in lines if l.strip()]
        return non_empty[-n:]
    except Exception:
        return []


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

    # -----------------------------------------------------------------------
    # Header banner
    # -----------------------------------------------------------------------
    print()
    print(_sep("═"))
    print(bold(f"  GA Practical Grid — {total} run(s)"))
    print(f"  Max generations : {bold(str(args.max_generations))}")
    print(f"  Polygons        : {bold(str(args.polygons))}")
    print(f"  Repeats         : {bold(str(args.repeats))}")
    print(f"  Base config     : {dim(str(base_config_path))}")
    print(f"  Output root     : {dim(str(runs_root))}")
    print(_sep("═"))
    print()

    if args.dry_run:
        print(yellow("DRY RUN — no experiments will be executed.\n"))
        for i, run in enumerate(all_runs[:15], start=1):
            sel, mut, cross, surv, pm, elite, pc, rep = run
            print(
                f"  {dim(f'{i:03d}/{total}:')}  "
                f"sel={cyan(sel)}  mut={cyan(mut)}  cross={cyan(cross)}  "
                f"surv={cyan(surv)}  pm={pm}  elite={elite}  pc={pc}  rep={rep}"
            )
        if total > 15:
            print(dim(f"  ... and {total - 15} more (truncated)"))
        print()
        return 0

    fieldnames = [
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
    ]

    successes = 0
    failures = 0

    with open(summary_csv, "w", newline="", encoding="utf-8") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
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
            cfg["output_suffix"] = str(run_id)

            cfg_path = configs_dir / f"{tag}.json"
            log_path = logs_dir / f"{tag}.log"

            with open(cfg_path, "w", encoding="utf-8") as f_cfg:
                json.dump(cfg, f_cfg, indent=2)

            cmd = [sys.executable, "main.py", "--config", str(cfg_path)]

            # --- Pre-run separator & info -----------------------------------
            print(_sep())
            print(
                f"  {bold(f'Run {run_id}/{total}')}  "
                f"{dim(f'(repeat {repeat})')}"
            )
            print(
                f"  sel={cyan(selection)}  mut={cyan(mutation)}  "
                f"cross={cyan(crossover)}  surv={cyan(survival)}"
            )
            print(
                f"  pm={pm}  elite={elite_pct}  pc={pc}  "
                f"max_gen={args.max_generations}  polygons={args.polygons}"
            )
            print(f"  log  : {dim(str(log_path))}")
            print(f"  cfg  : {dim(str(cfg_path))}")
            print(f"  cmd  : {dim(' '.join(cmd))}")
            print()

            returncode, runtime_s = run_cmd(cmd, cwd=project_root, log_path=log_path)

            # --- Post-run result --------------------------------------------
            if returncode == 0:
                successes += 1
                status = green(f"SUCCESS  (rc=0)  {runtime_s:.1f}s")
            else:
                failures += 1
                status = red(f"FAILED   (rc={returncode})  {runtime_s:.1f}s")

            print(f"  {status}")

            if returncode != 0:
                tail = _tail_log(log_path)
                if tail:
                    print(f"  {yellow('Last log lines:')}")
                    for line in tail:
                        print(f"    {dim(line)}")
                else:
                    print(f"  {dim('(log file empty or unreadable)')}")

            print()

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

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------
    print(_sep("═"))
    print(bold("  DONE"))
    print(f"  Total runs : {total}")
    print(f"  {green(f'Succeeded  : {successes}')}")
    if failures:
        print(f"  {red(f'Failed     : {failures}')}")
    else:
        print(f"  {dim('Failed     : 0')}")
    print(f"  Summary CSV: {dim(str(summary_csv))}")
    print(_sep("═"))
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
