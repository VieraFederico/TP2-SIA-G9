import random
from typing import List

from genetics_algorithm.fitness.relative_fitness import set_relative_fitness
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.selection.selection_method import SelectionMethod


class UniversalSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int, generation=0) -> list[Individual]:
        population = set_relative_fitness(population)
        population.sort(key=lambda ind: ind.relative_fitness)

        r = random.random()
        selected: List[Individual] = []

        for j in range(num_to_choose):
            r_j = (r + j) / num_to_choose
            accumulated = 0.0
            for individual in population:
                accumulated += individual.relative_fitness
                if r_j <= accumulated:
                    selected.append(individual)
                    break

        return selected
