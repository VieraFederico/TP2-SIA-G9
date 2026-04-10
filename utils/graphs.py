import csv
from pathlib import Path
from typing import List, TYPE_CHECKING
import matplotlib.pyplot as plt
from genetics_algorithm.models import Individual
from utils.paths import OUTPUT_DIR
if TYPE_CHECKING:
    from genetics_algorithm.engine import GeneticEngine

#TODO add more init params as needed
class AnalyticsMetadata:
    def __init__(self,
                 engine : "GeneticEngine"):
        self.engine = engine
        self.generations = 0
        self.best_fitness = 0
        self.best_per_generation: List[Individual] = []
        self.best_individual = None
        self.cutoff_reason = "max_generations"

    def generate_generations_vs_error_graph(self):
        if not self.best_per_generation:
            return None

        generations = list(range(len(self.best_per_generation)))

        # Plot error magnitude: lower abs(fitness) => lower point on Y
        error_values = [abs(ind.fitness) for ind in self.best_per_generation]

        stem = Path(self.engine.settings.image_path).stem
        output_path = OUTPUT_DIR / f"{stem}_generations_vs_error.png"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(10, 5))
        plt.plot(generations, error_values, color="tab:blue", linewidth=2)
        plt.title("Best Individual Error per Generation")
        plt.xlabel("Generation")
        plt.ylabel("Absolute Fitness Error |fitness|")
        plt.grid(True, alpha=0.3)

        # Standard orientation: small error near bottom, large error near top
        y_max = max(error_values) if error_values else 1.0
        plt.ylim(0, y_max + 1)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def append_results_to_csv(self) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        csv_path = OUTPUT_DIR / "generation_results.csv"

        fieldnames = [
            # AnalyticsMetadata
            "best_fitness",
            "generations_computed",
            # GeneticEngine / runtime
            "target_width",
            "target_height",
            # Settings
            "image_path",
            "triangles_per_ind",
            "population_size",
            "max_generations",
            "selection_method",
            "crossover_method",
            "mutation_method",
            "survival_strategy",
            "fitness_function",
            "cutoff_reason"
        ]

        row = {
            "best_fitness": self.best_fitness,
            "generations_computed": self.generations,
            "target_width": self.engine.target_image.width,
            "target_height": self.engine.target_image.height,
            "image_path": self.engine.settings.image_path,
            "triangles_per_ind": self.engine.settings.triangles_per_ind,
            "population_size": self.engine.settings.population_size,
            "max_generations": self.engine.settings.max_generations,
            "selection_method": self.engine.settings.selection_method,
            "crossover_method": self.engine.settings.crossover_method,
            "mutation_method": self.engine.settings.mutation_method,
            "survival_strategy": self.engine.settings.survival_strategy,
            "fitness_function": self.engine.settings.fitness_function,
            "cutoff_reason" : self.cutoff_reason
        }

        write_header = not csv_path.exists() or csv_path.stat().st_size == 0
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(row)

        return csv_path
