import random
from typing import List

from genetics_algorithm.fitness.relative_fitness import set_relative_fitness
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.selection.selection_method import SelectionMethod


#TODO currently accepts repeated selections of same individual.
def execute_roulette(num_to_choose: int, population: list[Individual],
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
        population = set_relative_fitness(population)
        selected_population : List[Individual] = []

        #TODO maybe move relative fitness calculaion to engine?


        population.sort(key=lambda ind: ind.relative_fitness)
        return execute_roulette(num_to_choose, population, selected_population)

