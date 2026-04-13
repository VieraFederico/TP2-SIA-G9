import csv
import fcntl
import os
from pathlib import Path
from typing import List, TYPE_CHECKING
import matplotlib.pyplot as plt
from genetics_algorithm.models import Individual
from utils.paths import OUTPUT_DIR, get_run_output_dir, ANIMATION_OUTPUT_DIR
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
        self.total_runtime_s = 0.0
        self.cutoff_reason = "max_generations"
        self.phase_times_s = {
            "calculate_fitness": 0.0,
            "elite_selection": 0.0,
            "parent_selection": 0.0,
            "crossover": 0.0,
            "mutation": 0.0,
            "calculate_fitness_offspring": 0.0,
            "survival": 0.0,
            "image_generation": 0.0,
            "termination_check": 0.0,
        }
        self.generational_gaps: list[float] = []

    def add_phase_time(self, phase: str, elapsed_s: float) -> None:
        if phase not in self.phase_times_s:
            self.phase_times_s[phase] = 0.0
        self.phase_times_s[phase] += elapsed_s

    def _run_output_dir(self) -> Path:
        return get_run_output_dir(self.engine.settings.output_suffix)

    def generate_generations_vs_error_graph(self):
        if not self.best_per_generation:
            return None

        generations = list(range(len(self.best_per_generation)))

        # Plot error magnitude: lower abs(fitness) => lower point on Y
        error_values = [abs(ind.fitness) for ind in self.best_per_generation]

        stem = Path(self.engine.settings.image_path).stem
        run_output_dir = self._run_output_dir()
        output_path = run_output_dir / f"{stem}_generations_vs_error.png"
        run_output_dir.mkdir(parents=True, exist_ok=True)

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

    def generate_phase_times_bar_graph(self):
        if not self.phase_times_s:
            return None

        # Keep only phases that were actually timed
        phase_items = [(name, value) for name, value in self.phase_times_s.items() if value > 0]
        if not phase_items:
            return None

        # Sort slowest -> fastest for easier comparison
        phase_items.sort(key=lambda kv: kv[1], reverse=True)
        phase_names = [name for name, _ in phase_items]
        phase_values = [value for _, value in phase_items]

        stem = Path(self.engine.settings.image_path).stem
        run_output_dir = self._run_output_dir()
        output_path = run_output_dir / f"{stem}_phase_times.png"
        run_output_dir.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(10, 6))
        bars = plt.barh(phase_names, phase_values, color="tab:orange")
        plt.gca().invert_yaxis()  # slowest on top
        plt.title("Accumulated Runtime per GA Phase")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Phase")
        plt.grid(axis="x", alpha=0.3)

        # Value labels at bar end
        for bar, value in zip(bars, phase_values):
            plt.text(
                bar.get_width(),
                bar.get_y() + bar.get_height() / 2,
                f" {value:.4f}s",
                va="center",
                ha="left",
            )

        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def generate_generational_gap_graph(self) -> str:
        if not self.generational_gaps:
            return ""

        plt.figure(figsize=(10, 6))

        # X-axis: generations, Y-axis: gap metric (0.0 to 1.0)
        generations = list(range(len(self.generational_gaps)))
        plt.plot(generations, self.generational_gaps, label='Effective Generational Gap', color='purple')

        plt.title('Generational Gap vs Generations')
        plt.xlabel('Generation')
        plt.ylabel('Generational Gap (Percentage of Offspring Surviving)')
        plt.ylim(0, 1.05)
        plt.grid(True)
        plt.legend()

        # Save the graph
        run_output_dir = self._run_output_dir()
        run_output_dir.mkdir(parents=True, exist_ok=True)
        output_path = run_output_dir / "generational_gap.png"

        plt.savefig(output_path)
        plt.close()

        return str(output_path)

    def print_timing_report(self) -> None:
        print("\n=== Timing report (accumulated) ===")
        ranked = sorted(self.phase_times_s.items(), key=lambda kv: kv[1], reverse=True)
        for phase, seconds in ranked:
            print(f"{phase:20s}: {seconds:.6f}s")
        print(f"{'total_runtime':20s}: {self.total_runtime_s:.6f}s")

        if self.generations > 0:
            avg_time = self.total_runtime_s / self.generations
            print("=== Averages ===")
            print(f"Avg time per generation : {avg_time:.4f}s")

            avg_fitness = self.phase_times_s.get('calculate_fitness_offspring', 0) / self.generations
            print(f"Avg fitness calc per gen: {avg_fitness:.4f}s")

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
            "pm",
            "pc",
            "elite_pop_percentage",
            "cutoff_reason",
            # timing columns
            "total_runtime_s",
            "time_calculate_fitness_s",
            "time_elite_selection_s",
            "time_parent_selection_s",
            "time_crossover_s",
            "time_mutation_s",
            "time_calculate_fitness_offspring_s",
            "time_survival_s",
            "time_image_generation_s",
            "time_termination_check_s",
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
            "pm": self.engine.settings.pm,
            "pc": self.engine.settings.pc,
            "elite_pop_percentage": self.engine.settings.elite_pop_percentage,
            "cutoff_reason" : self.cutoff_reason,
            "total_runtime_s": self.total_runtime_s,
            "time_calculate_fitness_s": self.phase_times_s["calculate_fitness"],
            "time_elite_selection_s": self.phase_times_s["elite_selection"],
            "time_parent_selection_s": self.phase_times_s["parent_selection"],
            "time_crossover_s": self.phase_times_s["crossover"],
            "time_mutation_s": self.phase_times_s["mutation"],
            "time_calculate_fitness_offspring_s": self.phase_times_s["calculate_fitness_offspring"],
            "time_survival_s": self.phase_times_s["survival"],
            "time_image_generation_s": self.phase_times_s["image_generation"],
            "time_termination_check_s": self.phase_times_s["termination_check"],
        }

        write_header = not csv_path.exists() or csv_path.stat().st_size == 0
        with open(csv_path, "a+", newline="", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.seek(0, os.SEEK_END)
                write_header = f.tell() == 0
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow(row)
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return csv_path
