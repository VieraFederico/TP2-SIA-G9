from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class EliteSelection(SelectionMethod):
    def select(self, population: list[Individual], k_percentage: float) -> list[Individual]:
        k_percentage = 0.4
        k = int(len(population) * k_percentage)
        return sorted(population, key=lambda ind: ind.fitness, reverse=True)[:k]
