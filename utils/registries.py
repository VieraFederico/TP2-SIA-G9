from genetics_algorithm.crossover import (
    OnePointCrossover,
    RingCrossover,
    TwoPointCrossover,
    UniformCrossover,
)
from genetics_algorithm.fitness.pixel_difference.mae import PixelDifferenceFitnessMAE
from genetics_algorithm.fitness.pixel_difference.mse import PixelDifferenceFitnessMSE
from genetics_algorithm.fitness.pixel_difference.ssim import PixelDifferenceFitnessSSIM
from genetics_algorithm.mutation import (
    GenMutation,
    MultiGenMutation,
    NonUniformMutation,
    UniformMutation,
)
from genetics_algorithm.selection import (
    BoltzmannSelection,
    EliteSelection,
    RankingSelection,
    RouletteSelection,
    DetTournamentSelection,
    ProbTournamentSelection,
    UniversalSelection,
)
from genetics_algorithm.survival_strategies import AdditiveSurvival, ExclusiveSurvival

CROSSOVER_REGISTRY = {
    "one_point": OnePointCrossover,
    "two_point": TwoPointCrossover,
    "uniform": UniformCrossover,
    "ring": RingCrossover,
}

MUTATION_REGISTRY = {
    "gen": GenMutation,
    "multi_gen": MultiGenMutation,
    "uniform": UniformMutation,
    "non_uniform": NonUniformMutation,
}

SELECTION_REGISTRY = {
    "elite": EliteSelection,
    "roulette": RouletteSelection,
    "universal": UniversalSelection,
    "boltzmann": BoltzmannSelection,
    "deterministic_tournament": DetTournamentSelection,
    "probabilistic_tournament": ProbTournamentSelection,
    "ranking": RankingSelection,
}

SURVIVAL_REGISTRY = {
    "additive": AdditiveSurvival,
    "exclusive": ExclusiveSurvival,
}

FITNESS_REGISTRY = {
    "mae": PixelDifferenceFitnessMAE,
    "mse": PixelDifferenceFitnessMSE,
    "ssim": PixelDifferenceFitnessSSIM,
}
