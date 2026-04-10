from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy
from genetics_algorithm.models.Individual import Individual


class ExclusiveSurvival(SurvivalStrategy):
    """Offspring fully replace the parent generation; best N from offspring survive."""

    def select_survivors(
        self,
        parents: list[Individual],
        offspring: list[Individual],
        population_size: int,
        total_population_size: int,
    ) -> tuple[list[Individual], float]:

        parents_len = len(parents)
        offspring_len = len(offspring)

        if offspring_len < parents_len:
            survivors = offspring + parents[: population_size - offspring_len]
            surviving_offspring_count = offspring_len
        else:
            survivors = offspring[:population_size]
            surviving_offspring_count = population_size

        # Returns generational gap taking into consideration total population size
        generational_gap = surviving_offspring_count / total_population_size

        return survivors, generational_gap
