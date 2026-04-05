import random

from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class MultiGenMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        if random.random() < self.p_tweak:
            return None

        random_polygons = random.randint(1, len(individual.polygons))

        for _ in range(random_polygons):
            target_index = random.randint(0, len(individual.polygons) - 1)
            individual.polygons[target_index] = individual.generate_random_polygon()
        return None
