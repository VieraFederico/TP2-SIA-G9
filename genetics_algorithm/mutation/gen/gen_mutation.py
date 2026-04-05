import random
from genetics_algorithm.models import Polygon, Individual
from genetics_algorithm.mutation.mutation_method import MutationMethod

# Only a single locus (one randomly chosen Polygon from the array of N polygons)
# is targeted and mutated
class GenMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        if random.random() < self.p_tweak:
            return None

        target_index = random.randint(0, len(individual.polygons) - 1)
        individual.polygons[target_index] = individual.generate_random_polygon()
        return None