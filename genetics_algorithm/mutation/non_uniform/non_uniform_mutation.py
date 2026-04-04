from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.models.Individual import Individual


class NonUniformMutation(MutationMethod):
    def mutate(self, individual: Individual, mutation_rate: float) -> Individual:
        raise NotImplementedError("NonUniformMutation is not yet implemented.")
