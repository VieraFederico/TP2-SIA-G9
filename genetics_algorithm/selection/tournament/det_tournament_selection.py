import random

from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual

class DetTournamentSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int) -> list[Individual]:
        winners = []

        # todo dynamically reduce torunament size: https://algorithmafternoon.com/books/genetic_algorithm/chapter04/#configuration-heuristics
        tournament_size = int(0.1 * len(population))
        for _ in range(num_to_choose):
            contestants = random.sample(population, tournament_size)
            tournament_winner = max(contestants, key=lambda individual: individual.fitness)
            winners.append(tournament_winner)

        return winners