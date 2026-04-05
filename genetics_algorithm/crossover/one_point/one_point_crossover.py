import random
from typing import List

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.models.Polygon import Polygon


class OnePointCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        max_poligons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))
        k_percentage = random.random()
        k = int(k_percentage * max_poligons)
        #gets first k polygons from parent1 and the rest from parent2
        child_1_polygons = parent1.get_polygons()[:k] + parent2.get_polygons()[k:]
        child_2_polygons = parent2.get_polygons()[:k] + parent1.get_polygons()[k:]
        child_1 = Individual(parent1.width, parent1.height, len(child_1_polygons), child_1_polygons)
        child_2 = Individual(parent2.width, parent2.height, len(child_2_polygons), child_2_polygons)
        return child_1, child_2


