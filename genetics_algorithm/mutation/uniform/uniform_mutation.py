import random

from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.mutation.gen.gen_mutation import GenMutation


class UniformMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        for polygon in individual.polygons:
            if random.random() < p_tweak:  # TODO: Chequear que darlo vuelta esta bien. Pero si la probabilidad de mutacion es 0.9, como estaba antes solo mutabamos 0.1 de las veces
                GenMutation.single_polygon_tweak(polygon, individual, p_tweak)
        return None