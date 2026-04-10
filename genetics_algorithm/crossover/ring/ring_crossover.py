import random
import math

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual


class RingCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        child_1 = parent1.clone()
        child_2 = parent2.clone()

        max_polygons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))

        # (para la persona que quiera entender el codigo)
        # NOTE: border case when one of the parents has no polygons!!
        if max_polygons != 0:

            k = random.randint(0, max_polygons - 1)
            l = random.randint(0, math.ceil(max_polygons / 2))

            # (para la persona que quiera entender el codigo)
            # NOTE: swap the polygons in the range [k, k + l) (module max_polygons).
            # in case both polygon lens are different, only consider the first max_polygons for circular operations.

            for i in range(l):
                idx = (k + i) % max_polygons
                child_1.polygons[idx], child_2.polygons[idx] = child_2.polygons[idx], child_1.polygons[idx]


        return child_1, child_2