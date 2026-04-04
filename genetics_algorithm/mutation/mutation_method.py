from abc import ABC, abstractmethod

from genetics_algorithm.models.Individual import Individual


class MutationMethod(ABC):
    @abstractmethod
    def mutate(self, individual: Individual, mutation_rate: float) -> Individual:
        ...
