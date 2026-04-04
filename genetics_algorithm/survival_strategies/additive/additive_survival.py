from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy
from genetics_algorithm.models.Individual import Individual


class AdditiveSurvival(SurvivalStrategy):
    """Parents and offspring compete together; best N survive."""

    def select_survivors(
        self,
        parents: list[Individual],
        offspring: list[Individual],
        population_size: int,
    ) -> list[Individual]:
        raise NotImplementedError("AdditiveSurvival is not yet implemented.")
