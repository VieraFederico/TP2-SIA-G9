from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class RankingSelection(SelectionMethod):
    def select(self, population: list[Individual], k_percentage: float) -> list[Individual]:
        raise NotImplementedError("RankingSelection is not yet implemented.")
