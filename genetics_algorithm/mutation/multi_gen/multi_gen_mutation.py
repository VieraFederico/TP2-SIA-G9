import random

from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.mutation.gen.gen_mutation import GenMutation

class MultiGenMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        if random.random() < self.p_tweak: #TODO: Chequear que darlo vuelta esta bien. Pero si la probabilidad de mutacion es 0.9, como estaba antes solo mutabamos 0.1 de las veces
            return None

        n = len(individual.polygons)
        if n == 0:
            return None

        random_polygons = random.randint(1, n)

        # TODO i know its repeated code but for now...
        for _ in range(random_polygons):
            target_index = random.randint(0, n - 1)
            polygon = individual.polygons[target_index]
            GenMutation.single_polygon_tweak(polygon, individual, p_tweak)
        return None
