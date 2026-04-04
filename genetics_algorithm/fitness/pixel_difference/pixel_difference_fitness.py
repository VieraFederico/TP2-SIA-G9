from PIL import Image
import numpy as np

from genetics_algorithm.fitness.fitness_function import FitnessFunction
from genetics_algorithm.models.Individual import Individual
from skimage.metrics import structural_similarity as ssim

# Fitness functions based on error -> lowe error, better individual -> return negative error as to choose the greatest "fitness"
class PixelDifferenceFitness(FitnessFunction):
    def evaluate(self, individual: Individual, target: Image.Image) -> float:
        # Converting to RGB first makes MSE calculation faster
        individual_image_array = np.array(individual.draw().convert("RGB")).astype(np.float32)
        target_image_array = np.array(target.convert("RGB")).astype(np.float32)

        if individual_image_array.size != target_image_array.size:
            raise ValueError("Individual and target images must have the same size.")

        # Error calculation (MSE)
        return -_mse(individual_image_array, target_image_array)

# Mean Square Error
def _mse(image_array1, image_array2) -> float:
    return float(np.mean((image_array1 - image_array2) ** 2))


# Mean Absolute Error
def _mae(image_array1, image_array2) -> float:
    return float(np.mean(np.abs(image_array1-image_array2)))

# SSIM is a better approximation but ranges from -1 to 1 with 1 being identical
# images and -1 being the opposite, taking into consideration structural differences too.
# To patch it the result will transformed to error
def _ssim(image_array1, image_array2) -> float:
    dim = image_array1.shape[0]

    win_size = min(7, dim)
    if win_size % 2 == 0:
        win_size -= 1

    result_ssim = ssim(image_array1, image_array2, channel_axis=-1, data_range=255, win_size=win_size)
    print(result_ssim)
    return float(1 - result_ssim)