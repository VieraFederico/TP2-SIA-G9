from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    image_path: str
    triangles_per_ind: int
    population_size: int
    max_generations: int
    crossover_method: str
    pc: float
    mutation_method: str
    pm: float
    p_tweak: float
    p_insert: float
    p_delete: float
    elite_pop_percentage: float
    selection_method: str
    survival_strategy: str
    fitness_function: str
    output_suffix: str
