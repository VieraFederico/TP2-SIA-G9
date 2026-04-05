from PIL import Image

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.fitness.fitness_function import FitnessFunction
from genetics_algorithm.models.Individual import Individual
from genetics_algorithm.models.Population import Population
from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.settings import Settings
from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy


class GeneticEngine:
    def __init__(
        self,
        settings: Settings,
        target_image: Image.Image,
        fitness_fn: FitnessFunction,
        selection: SelectionMethod,
        crossover: CrossoverMethod,
        mutation: MutationMethod,
        survival: SurvivalStrategy,
    ):
        self.settings = settings
        self.target_image = target_image
        self.fitness_fn = fitness_fn
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.survival = survival

    def run(self) -> Population:
        population = Population(
            population_size=self.settings.population_size,
            polygons_per_ind=self.settings.triangles_per_ind,
            width=self.target_image.width,
            height=self.target_image.height,
        )

        for generation in range(self.settings.max_generations):
            # 1. Evaluate fitness of current population
            for ind in population.individuals:
                ind.fitness = self.fitness_fn.evaluate(ind, self.target_image)

            # 2. Termination check
            if self._should_terminate(generation, population):
                break

            # 3. Select parents (by fitness)
            parents = self.selection.select(
                population.individuals, k=self.settings.population_size
            )

            # 4. Crossover → offspring
            offspring = self._do_crossover(parents)

            # 5. Mutation → mutated offspring
            offspring = [
                self.mutation.mutate(ind)
                for ind in offspring
            ]

            # 6. Evaluate fitness of offspring
            for ind in offspring:
                ind.fitness = self.fitness_fn.evaluate(ind, self.target_image)

            # 7. Survival: pool = parents + offspring → select N best → new generation
            population.individuals = self.survival.select_survivors(
                population.individuals, offspring, self.settings.population_size
            )

        return population

    def _should_terminate(self, generation: int, population: Population) -> bool:
        # TODO: implement termination conditions (max generations, fitness threshold, etc.)
        return False

    def _do_crossover(self, parents: list[Individual]) -> list[Individual]:
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = self.crossover.cross(parents[i], parents[i + 1])
            offspring.extend([child1, child2])
        return offspring
