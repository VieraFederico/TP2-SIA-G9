from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class BoltzmannSelection(SelectionMethod):
    def select(self, population: list[Individual], k: int) -> list[Individual]:
        raise NotImplementedError("BoltzmannSelection is not yet implemented.")
