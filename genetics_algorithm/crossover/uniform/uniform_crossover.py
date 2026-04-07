import random

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual


def switch_polygon(child_1: Individual, child_2: Individual, idx: int):
    child_1.polygons[idx], child_2.polygons[idx] = child_2.polygons[idx], child_1.polygons[idx]


class UniformCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        child_1 = parent1.clone()
        child_2 = parent2.clone()

        max_polygons = min(len(parent1.get_polygons()), len(parent2.get_polygons()))
        switch_probability = random.uniform(0.35,0.65)
        for i in range(max_polygons):
            if random.random() < switch_probability:
                switch_polygon(child_1, child_2, i)

        return child_1, child_2
