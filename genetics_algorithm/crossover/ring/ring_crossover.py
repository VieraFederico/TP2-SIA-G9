import random
import math

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual


class RingCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        child_1 = parent1.clone()
        child_2 = parent2.clone()

        max_polygons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))

        k = random.randint(1, max_polygons - 1)
        l = random.randint(0, math.ceil(k / 2))

        to_swap_head = child_1.get_polygons()[:k]
        to_swap_tail = child_1.get_polygons()[k+l:]
        child_1.polygons = child_2.get_polygons()[:k] + child_1.get_polygons()[k:k+l] + child_2.get_polygons()[k+l:]
        child_2.polygons = to_swap_head + child_2.get_polygons()[k:k+l] + to_swap_tail

        return child_1, child_2