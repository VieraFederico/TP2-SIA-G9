import numpy as np
from PIL import Image

from genetics_algorithm.fitness import FitnessFunction
from genetics_algorithm.models import Individual


class PixelDifferenceFitnessMAE(FitnessFunction):
    def __init__(self, target_image: Image.Image):
        self._target_image_array = np.array(target_image).astype(np.float32)

    def evaluate(self, individual: Individual) -> float:
        individual_image_array = np.array(individual.draw()).astype(np.float32)
        if individual_image_array.size != self._target_image_array.size:
            raise ValueError("Individual and target images must have the same size.")

        return -_mae(individual_image_array, self._target_image_array)


def _mae(image_array1, image_array2) -> float:
    return float(np.mean(np.abs(image_array1 - image_array2)))