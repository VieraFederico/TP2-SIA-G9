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

        sorted_offspring = sorted(offspring, key=lambda ind: ind.fitness, reverse=True)

        if len(sorted_offspring) >= population_size:
            survivors = sorted_offspring[:population_size]
            surviving_offspring_count = population_size
        else:
            needed = population_size - len(sorted_offspring)
            sorted_parents = sorted(parents, key=lambda ind: ind.fitness, reverse=True)
            survivors = sorted_offspring + sorted_parents[:needed]
            surviving_offspring_count = len(sorted_offspring)

        generational_gap =  surviving_offspring_count / total_population_size

        return survivors, generational_gap
