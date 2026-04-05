from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class NonUniformMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        raise NotImplementedError("NonUniformMutation is not yet implemented.")
