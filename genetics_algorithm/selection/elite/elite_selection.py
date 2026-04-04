from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class EliteSelection(SelectionMethod):
    def select(self, population: list[Individual], k: int) -> list[Individual]:
        raise NotImplementedError("EliteSelection is not yet implemented.")
