# TP2 — GA Image Approximation

Genetic algorithm that approximates an input image using semi-transparent triangles drawn on a white canvas. Each individual in the population is a canvas of N triangles; fitness is measured by how closely the rendered canvas matches the target image.

## Requirements

- Python 3.10+

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (CMD)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python main.py -i <path/to/image> [options]
```

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--image` | `-i` | — | Path to target input image **(required)** |
| `--triangles` | `-t` | `20` | Number of triangles per individual |
| `--population` | `-p` | `100` | Population size |
| `--generations` | `-g` | `1000` | Maximum number of generations |
| `--crossover` | `-c` | `one_point` | Crossover method: `one_point` / `two_point` / `uniform` / `ring` |
| `--mutation` | `-m` | `gen` | Mutation method: `gen` / `multi_gen` / `uniform` / `non_uniform` |
| `--mutation-rate` | | `0.01` | Mutation probability per gene (0.0–1.0) |
| `--selection` | `-s` | `elite` | Selection method: `elite` / `roulette` / `universal` / `boltzmann` / `tournament` / `ranking` |
| `--survival` | | `exclusive` | Survival strategy: `additive` / `exclusive` |
| `--config` | | `genetics_algorithm/config.json` | Path to config file |

The best individual is saved under `output/` as `{input_basename}_result.png` (for example `random_triangles_result.png`).

### Example

```bash
python main.py \
  -i resources/images/random_triangles.png \
  -t 50 \
  -p 100 \
  -g 500 \
  -c two_point \
  -m gen \
  --mutation-rate 0.02 \
  -s elite \
  --survival exclusive
```

## Configuration

All options can also be set in `genetics_algorithm/config.json`. CLI arguments take precedence over config file values.

```json
{
  "triangles_per_canvas": 20,
  "population_size": 100,
  "max_generations": 1000,
  "crossover_method": "one_point",
  "mutation_method": "gen",
  "mutation_rate": 0.01,
  "selection_method": "elite",
  "survival_strategy": "exclusive",
  "fitness_function": "pixel_difference"
}
```

## Project Structure

```
TP2-SIA-G9/
├── main.py                          # Entry point — engine wiring + save to output/
├── requirements.txt
├── README.md
├── output/                          # Generated images (created at run time)
├── utils/
│   ├── cmd_parser.py                # argparse, load_config, build_settings
│   ├── paths.py                     # PROJECT_ROOT, OUTPUT_DIR
│   └── registries.py                # GA component class maps
├── resources/
│   └── images/                      # Input images
└── genetics_algorithm/
    ├── config.json                  # Default hyperparameters
    ├── settings.py                  # Frozen Settings dataclass (built once at startup)
    ├── engine.py                    # GA main loop
    ├── models/
    │   ├── Polygon.py               # Single triangle (vertices, color, z_index)
    │   ├── Individual.py            # One canvas of N polygons
    │   └── Population.py           # Collection of individuals
    ├── crossover/
    │   ├── crossover_method.py      # Abstract base class
    │   ├── one_point/
    │   ├── two_point/
    │   ├── uniform/
    │   └── ring/
    ├── mutation/
    │   ├── mutation_method.py       # Abstract base class
    │   ├── gen/
    │   ├── multi_gen/
    │   ├── uniform/
    │   └── non_uniform/
    ├── selection/
    │   ├── selection_method.py      # Abstract base class
    │   ├── elite/
    │   ├── roulette/
    │   ├── universal/
    │   ├── boltzmann/
    │   ├── tournament/              # Deterministic + probabilistic via constructor param
    │   └── ranking/
    ├── fitness/
    │   ├── fitness_function.py      # Abstract base class
    │   └── pixel_difference/
    └── survival_strategies/
        ├── survival_strategy.py     # Abstract base class
        ├── additive/                # Parents + offspring compete together
        └── exclusive/               # Offspring fully replace parents
```
