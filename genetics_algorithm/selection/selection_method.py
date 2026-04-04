from abc import ABC, abstractmethod

from genetics_algorithm.models.Individual import Individual


class SelectionMethod(ABC):
    @abstractmethod
    def select(self, population: list[Individual], k: int) -> list[Individual]:
        ...
