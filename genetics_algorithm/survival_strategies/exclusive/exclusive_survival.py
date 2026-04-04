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
        raise NotImplementedError("ExclusiveSurvival is not yet implemented.")
