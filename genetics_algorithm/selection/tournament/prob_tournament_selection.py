import random

from genetics_algorithm.models import Individual
from genetics_algorithm.selection import SelectionMethod


class ProbTournamentSelection(SelectionMethod):

    def select(self, population: list[Individual], num_to_choose: int,  generation=0) -> list[Individual]:
        threshold_value = 0.75 #TODO get from param
        winners = []
        for _ in range(num_to_choose):
            contestants = random.sample(population, 2)
            if random.random() < threshold_value:
                tournament_winner = max(contestants, key=lambda individual: individual.fitness)
            else:
                tournament_winner = min(contestants, key=lambda individual: individual.fitness)
            winners.append(tournament_winner)
        return winners

