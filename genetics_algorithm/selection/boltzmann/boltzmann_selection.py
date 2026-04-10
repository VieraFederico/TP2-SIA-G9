from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.fitness.relative_fitness import set_boltzmann_relative_fitness
from genetics_algorithm.selection.roulette.roulette_selection import execute_roulette
from typing import List

class BoltzmannSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int, generation=0) -> list[Individual]:

        #TODO: set it as a configurable param by terminal.
        initial_t0 = 10
        alpha= 0.95

        temperature = max(initial_t0 * (alpha ** generation), 1e-6)
        population = set_boltzmann_relative_fitness(population,temperature)
        selected_population: List[Individual] = []
        return execute_roulette(num_to_choose, population, selected_population)

