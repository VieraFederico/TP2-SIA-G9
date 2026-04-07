from typing import List

from genetics_algorithm.models import Individual


class RelativeFitness:
    def __init__(self, population: List[Individual]):

        n = len(population)
        self.fitness_sum = sum(p.fitness for p in population)

        if n == 0:
            self.relative_sum = 0.0
            return

        # If total fitness is Fallback to uniform probabilities.
        if self.fitness_sum == 0.0 or n == 1:
            uniform = 1.0 / n
            for p in population:
                p.relative_fitness = uniform
            self.relative_sum = 1.0
            return

        inv_sum = 1.0 / self.fitness_sum
        relative_sum = 0.0
        norm = 1.0 / (n - 1)
        for p in population:
            p.relative_fitness = (1.0 - p.fitness * inv_sum) * norm
            relative_sum += p.relative_fitness


#optimized version of
#         self.fitness_sum = _get_sum(population)
#         self.relative_sum = 0
#
#
#         for p in population:
#
#             p.relative_fitness = (self.fitness_sum - p.fitness) / self.fitness_sum
#             self.relative_sum += p.relative_fitness
#
#
#
#         for p in population:
#             p.relative_fitness = p.relative_fitness / self.relative_sum
# this code calculates the relative fitness of each individual (0,1) and normalizes it
# so SUM(relative fitness) = 1
# this is necessary for selection methods like roulette selection, where the accumulated
# fitness needs to be used
