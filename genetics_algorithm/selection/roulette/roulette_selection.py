from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class RouletteSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int) -> list[Individual]:
        raise NotImplementedError("RouletteSelection is not yet implemented.")
