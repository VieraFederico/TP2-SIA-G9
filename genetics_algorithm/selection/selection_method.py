from abc import ABC, abstractmethod

from genetics_algorithm.models.Individual import Individual


class SelectionMethod(ABC):
    @abstractmethod
    def select(self, population: list[Individual], num_to_choose: int,generation: int = 0 ) -> list[Individual]:
        pass
