import argparse
import json
import sys
from pathlib import Path

from genetics_algorithm.settings import Settings

from utils.registries import (
    CROSSOVER_REGISTRY,
    MUTATION_REGISTRY,
    SELECTION_REGISTRY,
    SURVIVAL_REGISTRY,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="GA image approximation via triangles."
    )
    parser.add_argument("-i", "--image", type=str, help="Path to target input image.")
    parser.add_argument("-t", "--triangles", type=int, help="Number of triangles per individual.")
    parser.add_argument("-p", "--population", type=int, help="Population size.")
    parser.add_argument("-g", "--generations", type=int, help="Maximum number of generations.")
    parser.add_argument(
        "-c", "--crossover",
        choices=list(CROSSOVER_REGISTRY),
        help="Crossover method.",
    )
    parser.add_argument(
        "--output-suffix",
        type=str,
        help="Suffix to add to output filename. useful when running multiple times",
    )
    parser.add_argument(
        "-m", "--mutation",
        choices=list(MUTATION_REGISTRY),
        help="Mutation method.",
    )
    parser.add_argument("--mutation-rate", type=float, help="Mutation rate (0.0–1.0).")
    parser.add_argument(
        "-s", "--selection",
        choices=list(SELECTION_REGISTRY),
        help="Selection method.",
    )
    parser.add_argument(
        "--survival",
        choices=list(SURVIVAL_REGISTRY),
        help="Survival strategy.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="genetics_algorithm/config.json",
        help="Path to config.json (default: genetics_algorithm/config.json).",
    )
    return parser.parse_args()


def load_config(path: str) -> dict:
    config_path = Path(path)
    if not config_path.exists():
        print(f"Config file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


def build_settings(args, config: dict) -> Settings:
    return Settings(
        image_path=args.image if args.image is not None else config.get("image_path", ""),
        triangles_per_ind=args.triangles if args.triangles is not None else config.get("triangles_per_canvas", 20),
        population_size=args.population if args.population is not None else config.get("population_size", 100),
        max_generations=args.generations if args.generations is not None else config.get("max_generations", 1000),
        crossover_method=args.crossover if args.crossover is not None else config.get("crossover_method", "one_point"),
        pc=config.get("pc", 0.5),
        mutation_method=args.mutation if args.mutation is not None else config.get("mutation_method", "gen"),
        pm=args.mutation_rate if args.mutation_rate is not None else config.get("pm", 0.01),
        p_tweak=config.get("p_tweak", 0.7),
        p_insert=config.get("p_insert", 0.2),
        p_delete=config.get("p_delete", 0.1),
        elite_pop_percentage=config.get("elite_pop_percentage", 0.4),
        selection_method=args.selection if args.selection is not None else config.get("selection_method", "elite"),
        survival_strategy=args.survival if args.survival is not None else config.get("survival_strategy", "exclusive"),
        fitness_function=config.get("fitness_function", "pixel_difference"),
        output_suffix=args.output_suffix if args.output_suffix is not None else config.get("output_suffix", ""),

    )

