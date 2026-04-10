import random
from typing import List

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.models.Polygon import Polygon


class OnePointCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        child_1 = parent1.clone()
        child_2 = parent2.clone()

        max_polygons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))
        k_percentage = random.random()
        k = int(k_percentage * max_polygons)

        to_swap = child_1.get_polygons()[k:]
        child_1.polygons = child_1.get_polygons()[:k] + child_2.get_polygons()[k:]
        child_2.polygons = child_2.get_polygons()[:k] + to_swap

        return child_1, child_2


