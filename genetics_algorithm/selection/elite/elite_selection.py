from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class EliteSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int, generation=0) -> list[Individual]:
        return sorted(population, key=lambda ind: ind.fitness, reverse=True)[:num_to_choose]
