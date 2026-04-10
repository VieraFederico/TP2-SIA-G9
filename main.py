import sys
from pathlib import Path

from PIL import Image

from genetics_algorithm.engine import GeneticEngine
from utils.cmd_parser import build_settings, load_config, parse_args
from utils.paths import OUTPUT_DIR
from utils.registries import (
    CROSSOVER_REGISTRY,
    FITNESS_REGISTRY,
    MUTATION_REGISTRY,
    SELECTION_REGISTRY,
    SURVIVAL_REGISTRY,
)


def main():
    args = parse_args()
    config = load_config(args.config)
    settings = build_settings(args, config)

    if not settings.image_path:
        print("Error: --image is required (or set image_path in config.json).", file=sys.stderr)
        sys.exit(1)

    target_image = Image.open(settings.image_path).convert("RGBA")
    solid_target_image = Image.new("RGBA", target_image.size, (255, 255, 255, 255))
    solid_target_image.alpha_composite(target_image)

    engine = GeneticEngine(
        settings=settings,
        target_image=solid_target_image,
        fitness_fn=FITNESS_REGISTRY[settings.fitness_function](solid_target_image),
        selection=SELECTION_REGISTRY[settings.selection_method](),
        crossover=CROSSOVER_REGISTRY[settings.crossover_method](),
        mutation=MUTATION_REGISTRY[settings.mutation_method](
            pm=settings.pm,
            p_delete=settings.p_delete,
            p_insert=settings.p_insert,
            p_tweak=settings.p_tweak,
        ),
        survival=SURVIVAL_REGISTRY[settings.survival_strategy](),
    )

    result = engine.run()

    best = max(result.individuals, key=lambda ind: ind.fitness)
    output_image = best.draw()

    stem = Path(settings.image_path).stem
    output_path = OUTPUT_DIR / f"{stem}_result.png"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_image.save(output_path)
    print(f"Output saved to {output_path}")


if __name__ == "__main__":
    main()
