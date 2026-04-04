from PIL import Image

from genetics_algorithm.fitness.fitness_function import FitnessFunction
from genetics_algorithm.models.Individual import Individual


class PixelDifferenceFitness(FitnessFunction):
    def evaluate(self, individual: Individual, target: Image.Image) -> float:
        raise NotImplementedError("PixelDifferenceFitness is not yet implemented.")
