from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.mutation.gen.gen_mutation import GenMutation

class UniformMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):

        for i in range(len(individual.polygons)):
            if random.random() > p_tweak:
                GenMutation.single_polygon_tweak(individual.polygons[i], p_tweak)
        return None