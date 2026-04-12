import numpy as np
from PIL import Image

from genetics_algorithm.fitness import FitnessFunction
from genetics_algorithm.models import Individual


class PixelDifferenceFitnessMSE(FitnessFunction):
    def __init__(self, target_image: Image.Image):
        self._target_image_array = np.array(target_image).astype(np.float32)

    def evaluate(self, individual: Individual) -> float:
        individual_image_array = np.array(individual.draw()).astype(np.float32)
        if individual_image_array.size != self._target_image_array.size:
            raise ValueError("Individual and target images must have the same size.")

        return -float(np.mean(np.abs(individual_image_array-self._target_image_array)))