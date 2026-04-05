from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class UniformMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        raise NotImplementedError("UniformMutation is not yet implemented.")
