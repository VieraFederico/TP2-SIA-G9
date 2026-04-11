from abc import ABC, abstractmethod
import random

from genetics_algorithm.models import Individual, Polygon

class MutationMethod(ABC):
    def __init__(self, pm: float, p_delete: float, p_insert: float, p_tweak: float):
        self.pm = pm
        self.p_delete = p_delete
        self.p_insert = p_insert
        self.p_tweak = p_tweak

    def mutate(self, individual: Individual) -> Individual:
        if random.random() > self.pm:
            return individual

        if random.random() < self.p_delete and len(individual.polygons) > 1:
            target_index = random.randint(0, len(individual.polygons) - 1)
            individual.polygons.pop(target_index)

        if random.random() < self.p_insert:
            new_poly = individual.generate_random_polygon()
            individual.polygons.append(new_poly)

        self._tweak(individual, self.p_tweak)
        individual.fitness = 0.0 # reset fitness value because individual has been modified
        return individual

    @abstractmethod
    def _tweak(self, individual: Individual, p_tweak: float):
        """
        Depending on the selected mutation method, classes must implement the respective tweaking method
        """
        pass