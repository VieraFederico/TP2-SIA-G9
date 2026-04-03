from genetics_algorithm.models.Individual import Individual


class Population:
    def __init__(self,
                 population_size: int,
                 polygons_per_ind: int,
                 width: int,
                 height: int
                 ):
        self.population_size = population_size
        self.width = width
        self.height = height

        self.individuals = self._generate_individuals(polygons_per_ind)

    def _generate_individuals(self, polygons_per_ind: int) -> list[Individual]:
        return [Individual(self.width, self.height, polygons_per_ind) for _ in range(self.population_size)]