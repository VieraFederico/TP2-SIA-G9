import random

from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class MultiGenMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        if random.random() > self.p_tweak:
            return None

        random_polygons = random.randint(1, len(individual.polygons))

        # TODO i know its repeated code but for now...
        for _ in range(random_polygons):
            target_index = random.randint(0, len(individual.polygons) - 1)
            polygon = individual.polygons[target_index]
            GenMutation.single_polygon_tweak(polygon, p_tweak)
        return None
