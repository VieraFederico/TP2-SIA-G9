from genetics_algorithm.selection.selection_method import SelectionMethod
from genetics_algorithm.models.Individual import Individual


class TournamentSelection(SelectionMethod):
    """
    Covers both tournament variants:
    - Deterministic: the best individual in the group always wins.
    - Probabilistic: the best wins with probability p, second-best with p*(1-p), etc.
    Controlled via a `deterministic` parameter at construction time.
    """

    def __init__(self, deterministic: bool = True):
        self.deterministic = deterministic

    def select(self, population: list[Individual], k: int) -> list[Individual]:
        raise NotImplementedError("TournamentSelection is not yet implemented.")
