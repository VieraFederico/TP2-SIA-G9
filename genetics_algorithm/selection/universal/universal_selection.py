from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class UniversalSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int, generation=0) -> list[Individual]:
        raise NotImplementedError("UniversalSelection is not yet implemented.")
