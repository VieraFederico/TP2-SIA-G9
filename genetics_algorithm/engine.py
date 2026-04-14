import json
import random
from pathlib import Path
from time import perf_counter
from typing import List

from PIL import Image

from genetics_algorithm.crossover.crossover_method import CrossoverMethod
from genetics_algorithm.fitness.fitness_function import FitnessFunction
from genetics_algorithm.models import Individual
from genetics_algorithm.models.Population import Population
from genetics_algorithm.mutation.mutation_method import MutationMethod
from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.settings import Settings
from genetics_algorithm.survival_strategies.survival_strategy import SurvivalStrategy
from utils.graphs import AnalyticsMetadata
from utils.paths import OUTPUT_DIR, get_animation_output_dir



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
        self.analysis_metadata = None
        self.settings = settings
        self.target_image = target_image
        self.fitness_fn = fitness_fn
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.survival = survival

    def run(self) -> Population:
        self.analysis_metadata = AnalyticsMetadata(engine=self)
        # population = Population(
        #     population_size=self.settings.population_size,
        #     polygons_per_ind=self.settings.triangles_per_ind,
        #     width=self.target_image.width,
        #     height=self.target_image.height,
        # )
        population = self.initialize_population()
        run_start = perf_counter()

        # 1. Evaluate fitness of the INITIAL population ONCE before the loop starts
        print(f"Evaluating fitness of individuals")
        t0 = perf_counter()
        self.evaluate_population(population)
        # for ind in population.individuals:
        #     ind.fitness = self.fitness_fn.evaluate(ind)
        self.analysis_metadata.add_phase_time("initial_fitness", perf_counter() - t0)

        for generation in range(self.settings.max_generations):

            self.record_best_individual(population, generation)

            if self._should_terminate(generation, population):
                break
            
            elite_individuals, elite_individuals_amount = self.select_elite_individuals(population)
            parents = self.select_parents(population, elite_individuals_amount, generation)
            offsprings = self.produce_offsprings(parents)

            survivors = self.select_survivors(population, elite_individuals, offsprings, elite_individuals_amount)
            population.individuals = elite_individuals + survivors

        self.analysis_metadata.total_runtime_s = perf_counter() - run_start
        self.analysis_metadata.print_timing_report()
        self.analysis_metadata.append_results_to_csv()

        phase_graph_path = self.analysis_metadata.generate_phase_times_bar_graph()
        if phase_graph_path:
            print(f"Phase times graph saved to {phase_graph_path}")

        print(f"final fitness {population.individuals[0].fitness}")
        graph_path = self.analysis_metadata.generate_generations_vs_error_graph()
        if graph_path:
            print(f"Generations vs error graph saved to {graph_path}")

        gap_graph_path = self.analysis_metadata.generate_generational_gap_graph()
        if gap_graph_path:
            print(f"Generational gap graph saved to {gap_graph_path}")

        print(f"Results appended to CSV in {OUTPUT_DIR / 'generation_results.csv'}")


        return population

    def _should_terminate(self, generation: int, population: Population) -> bool:
        if generation >= self.settings.max_generations:
            self.analysis_metadata.cutoff_reason = "max_generations"
            return True
        return False

    def generate_image(self, individual: Individual, generation: int = None) -> None:
        output_image = individual.draw()

        stem = Path(self.settings.image_path).stem

        gen_suffix = f"_{generation}" if generation is not None else ""
        animation_dir = get_animation_output_dir(self.settings.output_suffix)
        animation_dir.mkdir(parents=True, exist_ok=True)
        output_path = animation_dir / f"{stem}_result{gen_suffix}.png"

        output_image.save(output_path)

    def initialize_population(self) -> Population:
        population = Population(
            population_size=self.settings.population_size,
            polygons_per_ind=self.settings.triangles_per_ind,
            width=self.target_image.width,
            height=self.target_image.height,
        )
        return population

    def evaluate_population(self, population: Population) -> None:
        for ind in population.individuals:
            ind.fitness = self.fitness_fn.evaluate(ind)

    def record_best_individual(self, population: Population, generation: int) -> None:
        best_ind = max(population.individuals, key=lambda individual: individual.fitness)
        print(f"Generation {generation} | Best Fitness (Error): {best_ind.fitness}")
        self.analysis_metadata.best_individual = best_ind
        self.analysis_metadata.generations = generation
        self.analysis_metadata.best_fitness = best_ind.fitness
        self.analysis_metadata.best_per_generation.append(best_ind)

    def select_elite_individuals(self, population: Population) -> tuple[List[Individual], int]:
        t0 = perf_counter()
        elite_individuals_amount = int(self.settings.elite_pop_percentage * self.settings.population_size)
        elite_individuals = sorted(
            population.individuals,
            key=lambda individual: individual.fitness,
            reverse=True
        )[:elite_individuals_amount]
        self.analysis_metadata.add_phase_time("elite_selection", perf_counter() - t0)
        return elite_individuals, elite_individuals_amount

    def select_parents(self, population: Population, elite_individuals_amount: int, generation: int) -> list[Individual]:
        t0 = perf_counter()
        parents = self.selection.select(population.individuals,
                                        self.settings.population_size - elite_individuals_amount,
                                        generation)
        self.analysis_metadata.add_phase_time("parent_selection", perf_counter() - t0)
        return parents

    def produce_offsprings(self, parents: list[Individual]) -> list[Individual]:
        offsprings = []

        for i in range(0, len(parents)-1, 2):
            parent1, parent2 = parents[i], parents[i+1]

            # 4. Crossover
            t0 = perf_counter()
            if random.random() < self.settings.pc:
                offspring1, offspring2 = self.crossover.cross(parent1, parent2)
            else:
                offspring1, offspring2 = parent1.clone(), parent2.clone()
            self.analysis_metadata.add_phase_time("crossover", perf_counter() - t0)

            # 5. Mutation
            t0 = perf_counter()
            offspring1 = self.mutation.mutate(offspring1)
            offspring2 = self.mutation.mutate(offspring2)
            self.analysis_metadata.add_phase_time("mutation", perf_counter() - t0)

            # 6. Calculate Offspring fitness
            t0 = perf_counter()
            offspring1.fitness = self.fitness_fn.evaluate(offspring1)
            offspring2.fitness = self.fitness_fn.evaluate(offspring2)
            self.analysis_metadata.add_phase_time("calculate_fitness_offspring", perf_counter() - t0)

            offsprings.extend([offspring1, offspring2])
            
        return offsprings

    def select_survivors(self, population: Population, elite_individuals: list[Individual], offsprings: list[Individual], elite_individuals_amount: int) -> list[Individual]:
            remaining_individuals = [ind for ind in population.individuals if ind not in elite_individuals]
            t0 = perf_counter()
            survivors, current_gap = self.survival.select_survivors(
                remaining_individuals,
                offsprings,
                self.settings.population_size - elite_individuals_amount,
                self.settings.population_size
            )
            self.analysis_metadata.add_phase_time("survival", perf_counter() - t0)
            self.analysis_metadata.generational_gaps.append(current_gap)
            return survivors