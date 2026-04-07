import random
from typing import List

from genetics_algorithm.fitness.relative_fitness import RelativeFitness
from genetics_algorithm.models import Individual
from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual

#TODO currently accepts repeated selections of same individual.
#to remove this, add line "population.remove(individual)" after "selected_population.append(individual)"

def _execute_roulette(num_to_choose: int, population: list[Individual],
                      selected_population: list[Individual]) -> list[Individual]:
    for i in range(num_to_choose):
        rand_float = random.random()
        accumulated_fitness = population[0].relative_fitness
        for individual in population:
            if rand_float <= accumulated_fitness:
                selected_population.append(individual)
                break
            accumulated_fitness += individual.relative_fitness
    return selected_population


class RouletteSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int) -> list[Individual]:
        relative_fitness = RelativeFitness(population)
        selected_population : List[Individual] = []

        #TODO maybe move relative fitness calculaion to engine?


        population.sort(key=lambda ind: ind.relative_fitness)
        return _execute_roulette(num_to_choose, population, selected_population)

