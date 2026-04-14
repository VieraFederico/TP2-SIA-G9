import numpy as np
from PIL import Image

from genetics_algorithm.fitness import FitnessFunction
from genetics_algorithm.models import Individual
from skimage.metrics import structural_similarity as ssim

#TODO fix implementation
class PixelDifferenceFitnessSSIM(FitnessFunction):
    def __init__(self, target_image: Image.Image):
        self._target_image_array = np.array(target_image.convert("RGB")).astype(np.float32)

    def evaluate(self, individual: Individual) -> float:
        individual_image_array = np.array(individual.draw().convert("RGB")).astype(np.float32)
        if individual_image_array.size != self._target_image_array.size:
            raise ValueError("Individual and target images must have the same size.")

        return -_ssim(individual_image_array, self._target_image_array)

def _ssim(image_array1, image_array2) -> float:
    min_dim = min(image_array1.shape[0], image_array1.shape[1])
    win_size = min(7, min_dim)
    if win_size % 2 == 0:
        win_size -= 1

    result_ssim = ssim(image_array1, image_array2, channel_axis=-1, data_range=255, win_size=win_size)

    return float(1 - result_ssim)