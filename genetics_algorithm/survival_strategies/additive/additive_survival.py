from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy
from genetics_algorithm.models.Individual import Individual


class AdditiveSurvival(SurvivalStrategy):
    """Parents and offspring compete together; best N survive."""

    def select_survivors(
        self,
        parents: list[Individual],
        offspring: list[Individual],
        population_size: int,
        total_population_size: int,
    ) -> tuple[list[Individual], float]:
        generation = parents + offspring
        generation.sort(key=lambda individual: individual.fitness)
        survivors = generation[:population_size]

        offspring_ids = {id(o) for o in offspring}
        surviving_offspring_count = sum(1 for s in survivors if id(s) in offspring_ids)
        generational_gap = (
            surviving_offspring_count / total_population_size if total_population_size else 0.0
        )

        return survivors, generational_gap
