from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class DetTournamentSelection(SelectionMethod):
    def select(self, population: list[Individual], k_percentage: float) -> list[Individual]:
        raise NotImplementedError("DetTournamentSelection is not yet implemented.")
