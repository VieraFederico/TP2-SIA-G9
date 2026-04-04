from abc import ABC, abstractmethod

from genetics_algorithm.models.Individual import Individual


class SurvivalStrategy(ABC):
    @abstractmethod
    def select_survivors(
        self,
        parents: list[Individual],
        offspring: list[Individual],
        population_size: int,
    ) -> list[Individual]:
        ...
