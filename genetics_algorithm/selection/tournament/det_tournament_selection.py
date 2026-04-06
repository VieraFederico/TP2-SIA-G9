from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class DetTournamentSelection(SelectionMethod):
    def select(self, population: list[Individual], num_to_choose: int) -> list[Individual]:
        raise NotImplementedError("DetTournamentSelection is not yet implemented.")
