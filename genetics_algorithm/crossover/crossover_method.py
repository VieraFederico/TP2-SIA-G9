from abc import ABC, abstractmethod

from genetics_algorithm.models.Individual import Individual


class CrossoverMethod(ABC):
    @abstractmethod
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        ...
