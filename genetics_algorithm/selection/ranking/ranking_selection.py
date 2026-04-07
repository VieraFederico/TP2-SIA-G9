from typing import List

from genetics_algorithm.fitness.relative_fitness import set_rank_relative_fitness
from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.selection.roulette.roulette_selection import execute_roulette


class RankingSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int) -> list[Individual]:
       population = set_rank_relative_fitness(population)
       selected_population: List[Individual] = []
       return execute_roulette(num_to_choose,population, selected_population)


