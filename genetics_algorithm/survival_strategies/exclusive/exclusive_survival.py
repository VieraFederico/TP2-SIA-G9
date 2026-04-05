from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy
from genetics_algorithm.models.Individual import Individual


class ExclusiveSurvival(SurvivalStrategy):
    """Offspring fully replace the parent generation; best N from offspring survive."""

    def select_survivors(
        self,
        parents: list[Individual],
        offspring: list[Individual],
        population_size: int,
    ) -> list[Individual]:

        #TODO proper implementation
        parents_len = len(parents)
        offspring_len = len(offspring)
        if offspring_len < parents_len:
            return offspring + parents[: population_size - offspring_len]
        else:
            return sorted(offspring, key=lambda ind: ind.fitness, reverse=True)[:population_size]
