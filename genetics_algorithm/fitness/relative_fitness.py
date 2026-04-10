import logging
from typing import List
import math

from genetics_algorithm.models import Individual

# we need the accumulated sum of all relative fitness to equal 1.
# so we multiply by 1/"total"
# that total is the result of the sum of (n - index) / n.
# the inv_total formula can be reached by expanding the sum and simplifying.
# we used a similar method for the "set relative fitness" function
def set_rank_relative_fitness(population: List[Individual]) -> List[Individual]:
    population.sort(key=lambda ind: ind.fitness, reverse=True)
    n = len(population)

    if n == 0:
        return population

    inv_total = 1 / ((n - 1) /2)
    inv_n = 1/n

    for index, p in enumerate(population):
        p.relative_fitness = ((n - (index + 1)) * inv_n) * inv_total


    return population

def set_boltzmann_relative_fitness(population: List[Individual], temperature: float) -> List[Individual]:
    n = len(population)
    if n == 0:
        return population

    max_fitness = max(p.fitness for p in population)
    exp_vals = [math.exp((p.fitness - max_fitness) / temperature) for p in population]

    # avg_exp = sum(exp_vals) / n
    inv_total = 1.0/sum(exp_vals)
    for p, e in zip(population, exp_vals):
        # p.relative_fitness = e / avg_exp
        p.relative_fitness = e * inv_total


    return population


def set_relative_fitness(population: List[Individual]) -> List[Individual]:
    n = len(population)
    fitness_sum = sum(p.fitness for p in population)

    if n == 0:
        return population

    # If total fitness is Fallback to uniform probabilities.
    if fitness_sum == 0.0 or n == 1:
        uniform = 1.0 / n
        for p in population:
            p.relative_fitness = uniform

        return population
    inv_sum = 1.0 / fitness_sum
    relative_sum = 0.0
    norm = 1.0 / (n - 1)
    for p in population:
        p.relative_fitness = (1.0 - p.fitness * inv_sum) * norm
        relative_sum += p.relative_fitness
    return population

#optimized version of
#         fitness_sum = _get_sum(population)
#         relative_sum = 0
#
#
#         for p in population:
#
#             p.relative_fitness = (fitness_sum - p.fitness) / fitness_sum
#             relative_sum += p.relative_fitness
#
#
#
#         for p in population:
#             p.relative_fitness = p.relative_fitness / relative_sum
# this code calculates the relative fitness of each individual (0,1) and normalizes it
# so SUM(relative fitness) = 1
# this is necessary for selection methods like roulette selection, where the accumulated
# fitness needs to be used


