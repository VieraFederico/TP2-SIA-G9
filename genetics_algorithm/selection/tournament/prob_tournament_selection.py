from genetics_algorithm.models import Individual
from genetics_algorithm.selection import SelectionMethod


class ProbTournamentSelection(SelectionMethod):
    def select(self, population: list[Individual], k: int) -> list[Individual]:
        raise NotImplementedError("ProbTournamentSelection is not yet implemented.")