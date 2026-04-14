import random

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual


class TwoPointCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        max_polygons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))
        child_1 = parent1.clone()
        child_2 = parent2.clone()

        if max_polygons != 0:
            p1 = random.randint(0, max_polygons - 1)
            p2 = random.randint(p1, max_polygons - 1)
            p1_polys = child_1.get_polygons()
            p2_polys = child_2.get_polygons()
            child_1.polygons = p1_polys[:p1] + p2_polys[p1:p2] + p1_polys[p2:]
            child_2.polygons = p2_polys[:p1] + p1_polys[p1:p2] + p2_polys[p2:]
        return child_1, child_2