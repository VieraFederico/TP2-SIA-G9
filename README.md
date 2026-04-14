# TP2 — GA Image Approximation

Genetic algorithm that approximates an input image using semi-transparent triangles drawn on a white canvas. Each individual in the population is a canvas of N triangles; fitness is measured by how closely the rendered canvas matches the target image.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Getting the code](#2-getting-the-code)
3. [Setting up the virtual environment](#3-setting-up-the-virtual-environment)
4. [Installing dependencies](#4-installing-dependencies)
5. [Running the algorithm](#5-running-the-algorithm)
6. [Configuration file (config.json)](#6-configuration-file-configjson)
7. [CLI flags reference](#7-cli-flags-reference)
8. [Hyperparameter reference](#8-hyperparameter-reference)
9. [Output files](#9-output-files)
10. [Project structure](#10-project-structure)

---

## 1. Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | **3.10 or newer** |
| pip | comes with Python |
| git | any recent version |

To check your Python version:

```bash
python --version
# or, on some systems:
python3 --version
```

If you do not have Python 3.10+, download it from [python.org](https://www.python.org/downloads/).

---

## 2. Getting the code

```bash
git clone <repository-url>
cd TP2-SIA-G9
```

---

## 3. Setting up the virtual environment

A virtual environment keeps the project's dependencies isolated from your system Python.

**Create the environment (run once):**

```bash
python -m venv .venv
```

> On some Linux/macOS systems you may need `python3` instead of `python`.

**Activate the environment (run every time you open a new terminal):**

```bash
# Linux / macOS
source .venv/bin/activate

# Windows — Command Prompt
.venv\Scripts\activate.bat

# Windows — PowerShell
.venv\Scripts\Activate.ps1
```

After activation you will see `(.venv)` at the start of your terminal prompt. All commands from this point on assume the environment is active.

To deactivate later:

```bash
deactivate
```

---

## 4. Installing dependencies

```bash
pip install -r requirements.txt
```

This installs: `Pillow`, `numpy`, `scikit-image`, `opencv-python`, `matplotlib`.

---

## 5. Running the algorithm

### Quickstart — use the config file only

The easiest way to run is to edit `genetics_algorithm/config.json` with your desired settings and then just call:

```bash
python main.py
```

The image path must be set in the config file when no CLI flag is given (see [Section 6](#6-configuration-file-configjson)).

### Run with CLI flags

```bash
python main.py -i <path/to/image> [options]
```

**Minimal example** using one of the bundled images:

```bash
python main.py -i resources/images/random_triangles.png
```

**Full example overriding common settings:**

```bash
python main.py \
  -i resources/images/noche.png \
  -t 100 \
  -p 100 \
  -g 600 \
  -c one_point \
  -m non_uniform \
  --mutation-rate 0.12 \
  -s roulette \
  --survival additive \
  --output-suffix my_run
```

### Bundled input images

These images are ready to use inside `resources/images/`:

| File | Description |
|------|-------------|
| `random_triangles.png` | Simple triangle pattern (fast, good for testing) |
| `cuadrado.png` | Simple square shape |
| `noche.png` | Night-scene photograph |
| `images.png` | Generic test image |
| `AppleLogo.jpeg` | Apple logo |

---

## 6. Configuration file (config.json)

Located at `genetics_algorithm/config.json`. All settings live here. **CLI flags override config file values** when both are provided.

```json
{
  "image_path": "resources/images/random_triangles.png",
  "triangles_per_canvas": 100,
  "population_size": 100,
  "max_generations": 600,
  "crossover_method": "one_point",
  "pc": 0.5,
  "mutation_method": "non_uniform",
  "pm": 0.12,
  "p_tweak": 0.7,
  "p_insert": 0.2,
  "p_delete": 0.1,
  "elite_pop_percentage": 0.05,
  "selection_method": "roulette",
  "survival_strategy": "additive",
  "fitness_function": "mae",
  "output_suffix": ""
}
```

> **Note:** `pc`, `p_tweak`, `p_insert`, `p_delete`, `elite_pop_percentage`, and `fitness_function` can **only** be set via the config file — there are no CLI flags for them.

---

## 7. CLI flags reference

| Flag | Short | Default (from config) | Description |
|------|----|---|---|
| `--image` | `-i` | `image_path` in config | Path to the target image **(required if not in config)** |
| `--triangles` | `-t` | `triangles_per_canvas` | Number of triangles per individual |
| `--population` | `-p` | `population_size` | Number of individuals in the population |
| `--generations` | `-g` | `max_generations` | Maximum number of generations to run |
| `--crossover` | `-c` | `crossover_method` | Crossover method (see valid values below) |
| `--mutation` | `-m` | `mutation_method` | Mutation method (see valid values below) |
| `--mutation-rate` | | `pm` | Mutation probability per individual (0.0–1.0) |
| `--selection` | `-s` | `selection_method` | Selection method (see valid values below) |
| `--survival` | | `survival_strategy` | Survival strategy (see valid values below) |
| `--output-suffix` | | `output_suffix` | String appended to output filenames (useful for multiple runs) |
| `--config` | | `genetics_algorithm/config.json` | Path to a different config file |

---

## 8. Hyperparameter reference

### image_path
Path to the target PNG/JPEG image the algorithm tries to approximate.  
Example: `"resources/images/noche.png"`

---

### triangles_per_canvas
**Type:** integer  
**CLI:** `-t` / `--triangles`  
Number of triangles that make up each individual. More triangles = finer approximation but slower evaluation.  
Typical range: `20` – `200`

---

### population_size
**Type:** integer  
**CLI:** `-p` / `--population`  
Number of individuals evaluated each generation. Larger populations explore more of the search space but are slower.  
Typical range: `50` – `300`

---

### max_generations
**Type:** integer  
**CLI:** `-g` / `--generations`  
Hard limit on the number of generations. The algorithm stops when this is reached.  
Typical range: `200` – `5000`

---

### crossover_method
**Type:** string  
**CLI:** `-c` / `--crossover`  
How two parent genomes are combined to produce offspring.

| Value | Description |
|-------|-------------|
| `one_point` | Cut both parents at one random point and swap tails |
| `two_point` | Cut at two points and swap the middle segment |
| `uniform` | Each gene is independently inherited from either parent with equal probability |
| `ring` | Parents are treated as circular sequences; a random arc is swapped |

---

### pc
**Type:** float (0.0 – 1.0)  
**Config only**  
Probability that crossover is applied to a given parent pair. When crossover does not fire (probability `1 - pc`), both parents are cloned directly.  
Default: `0.5`

---

### mutation_method
**Type:** string  
**CLI:** `-m` / `--mutation`  
How an individual's genome is randomly altered after crossover.

| Value | Description |
|-------|-------------|
| `gen` | Mutates exactly one randomly chosen gene |
| `multi_gen` | Mutates a random subset of genes |
| `uniform` | Each gene is replaced with a completely random value with probability `pm` |
| `non_uniform` | Like uniform but the perturbation magnitude decreases as generations progress (encourages fine-tuning over time) |

---

### pm
**Type:** float (0.0 – 1.0)  
**CLI:** `--mutation-rate`  
Probability that mutation is applied to a given individual.  
Default: `0.01`  
Recommended: `0.05` – `0.15` for most runs.

---

### p_tweak
**Type:** float (0.0 – 1.0)  
**Config only**  
Within a mutation event, the probability that a gene is _tweaked_ (slightly modified) rather than inserted or deleted.  
`p_tweak + p_insert + p_delete` should sum to `1.0`.  
Default: `0.7`

---

### p_insert
**Type:** float (0.0 – 1.0)  
**Config only**  
Within a mutation event, the probability that a new random triangle is inserted into the individual.  
Default: `0.2`

---

### p_delete
**Type:** float (0.0 – 1.0)  
**Config only**  
Within a mutation event, the probability that an existing triangle is removed.  
Default: `0.1`

---

### elite_pop_percentage
**Type:** float (0.0 – 1.0)  
**Config only**  
Fraction of the population that is automatically carried over to the next generation unchanged (elitism). Setting this to `0` disables elitism entirely.  
Default: `0.05` (5 % of the population)

---

### selection_method
**Type:** string  
**CLI:** `-s` / `--selection`  
How parents are chosen from the current population to produce the next generation.

| Value | Description |
|-------|-------------|
| `elite` | Always select the top-fitness individuals |
| `roulette` | Fitness-proportionate selection (higher fitness = higher chance) |
| `universal` | Like roulette but uses a single random offset to pick all parents at once (less variance) |
| `boltzmann` | Selection pressure increases over time using a temperature schedule (simulated annealing-style) |
| `deterministic_tournament` | Pick k random individuals; the best always wins |
| `probabilistic_tournament` | Pick k random individuals; the best wins with high (but not certain) probability |
| `ranking` | Individuals are ranked by fitness; selection probability is proportional to rank (not raw fitness) |

---

### survival_strategy
**Type:** string  
**CLI:** `--survival`  
Determines which individuals move on to the next generation after offspring are produced.

| Value | Description |
|-------|-------------|
| `exclusive` | Offspring completely replace the parent population (steady-state replacement) |
| `additive` | Offspring and parents compete together; the best `population_size` individuals survive |

---

### fitness_function
**Type:** string  
**Config only**  
Metric used to compare the rendered canvas against the target image. Higher fitness = closer match.

| Value | Description |
|-------|-------------|
| `mae` | Mean Absolute Error per pixel (default, fast) |
| `mse` | Mean Squared Error per pixel (penalises large deviations more) |
| `pixel_difference` | Alias for `mae` |

---

### output_suffix
**Type:** string  
**CLI:** `--output-suffix`  
A label appended to all output file names. Useful when running the same image multiple times with different settings so results don't overwrite each other.  
Example: `"run_boltzmann_200gen"`

---

## 9. Output files

All output is written inside the `output/` directory (created automatically). After a run you will find:

| File / directory | Contents |
|------------------|----------|
| `output/<suffix>/<stem>_result[_suffix].png` | The best-evolved canvas image |
| `output/generation_results.csv` | One row per run with all settings and final fitness — appended on every run |
| `output/<suffix>/generations_vs_error.png` | Graph of best fitness per generation |
| `output/<suffix>/phase_times.png` | Bar chart of time spent in each GA phase |
| `output/<suffix>/generational_gap.png` | Plot of the generational gap over time |

Progress is printed to the terminal on every generation:

```
Generation 0 | Best Fitness (Error): -0.0842
Generation 1 | Best Fitness (Error): -0.0801
...
Output saved to output/my_run/noche_result_my_run.png
```

---

## 10. Project structure

```
TP2-SIA-G9/
├── main.py                          # Entry point
├── requirements.txt
├── README.md
├── output/                          # Generated at run time
├── resources/
│   └── images/                      # Bundled input images
├── utils/
│   ├── cmd_parser.py                # CLI argument parsing and settings builder
│   ├── paths.py                     # Output path helpers
│   ├── registries.py                # Maps string names to GA component classes
│   └── graphs.py                    # Analytics and graph generation
└── genetics_algorithm/
    ├── config.json                  # Default hyperparameters (edit this)
    ├── settings.py                  # Frozen Settings dataclass
    ├── engine.py                    # GA main loop
    ├── models/
    │   ├── Polygon.py               # Single triangle (vertices, RGBA colour)
    │   ├── Individual.py            # One canvas of N polygons
    │   └── Population.py            # Collection of individuals
    ├── crossover/                   # one_point / two_point / uniform / ring
    ├── mutation/                    # gen / multi_gen / uniform / non_uniform
    ├── selection/                   # elite / roulette / universal / boltzmann /
    │                                #   deterministic_tournament /
    │                                #   probabilistic_tournament / ranking
    ├── fitness/
    │   └── pixel_difference/        # mae / mse / ssim
    └── survival_strategies/         # additive / exclusive
```
