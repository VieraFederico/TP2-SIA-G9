import json

from PIL import Image

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.fitness.fitness_function import FitnessFunction
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

        # 1. Evaluate fitness of the INITIAL population ONCE before the loop starts
        print(f"Evaluating fitness of individuals")
        for ind in population.individuals:
            ind.fitness = self.fitness_fn.evaluate(ind)

        for generation in range(self.settings.max_generations):
            print(f"Start {generation} analysis")

            best_ind = max(population.individuals, key=lambda individual: individual.fitness)
            print(f"Generation {generation} | Best Fitness (Error): {best_ind.fitness}")

            # 2. Termination check
            if self._should_terminate(generation, population):
                break

            # 1. Check for elite individuals
            elite_individuals_amount = int(self.settings.elite_pop_percentage * self.settings.population_size)
            elite_individuals = sorted(population.individuals, key=lambda individual: individual.fitness, reverse=True)[:elite_individuals_amount]

            offsprings = []

            # 2. Select parents (by fitness)
            parents = self.selection.select(population.individuals, self.settings.population_size - elite_individuals_amount)

            # 3. Generate enough offsprings to cover the remaining generation spaces
            for i in range(0, len(parents)-1, 2):
                parent1, parent2 = parents[i], parents[i+1]

                # 4. Crossover
                # TODO crossover probability else clone, for now is only crossing
                offspring1, offspring2 = self.crossover.cross(parent1, parent2)

                # 5. Mutation
                # TODO can be converted into a offspring method
                offspring1 = self.mutation.mutate(offspring1)
                offspring2 = self.mutation.mutate(offspring2)

                # 6. Calculate Offspring fitness
                offspring1.fitness = self.fitness_fn.evaluate(offspring1)
                offspring2.fitness = self.fitness_fn.evaluate(offspring2)

                offsprings.extend([offspring1, offspring2])

            # 6. Survival: pool = remaining individuals + offspring → select N based on survival method
            # TODO return generational gap too based on selection method
            #  (take into consideration the elite portion of the population) -> for metrics
            remaining_individuals = [ind for ind in population.individuals if ind not in elite_individuals]
            survivors = self.survival.select_survivors(
                remaining_individuals,
                offsprings,
                self.settings.population_size - elite_individuals_amount
            )

            population.individuals = elite_individuals + survivors

        return population

    def _should_terminate(self, generation: int, population: Population) -> bool:
        # TODO: implement termination conditions (max generations, fitness threshold, etc.)
        return False

