from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class GenMutation(MutationMethod):
    def mutate(self, individual: Individual, mutation_rate: float) -> Individual:
        raise NotImplementedError("GenMutation is not yet implemented.")
