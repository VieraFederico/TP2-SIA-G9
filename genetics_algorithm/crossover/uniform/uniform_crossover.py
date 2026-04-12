from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.models.Individual import Individual
import random


class UniformCrossover(CrossoverMethod):
    def cross(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        child1 = parent1.clone()
        child2 = parent2.clone()

        max_polygons = min(len(child1.get_polygons()), len(child2.get_polygons()))

        for i in range(max_polygons-1):
            coin = random.random()
            if coin < 0.5:
                temp = child1.get_polygons()[i]
                child1.get_polygons()[i] = child2.get_polygons()[i]
                child2.get_polygons()[i] = temp

        return child1, child2