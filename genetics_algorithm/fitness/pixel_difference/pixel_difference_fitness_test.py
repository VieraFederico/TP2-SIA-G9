import unittest
from PIL import Image
import numpy as np

from genetics_algorithm.fitness.pixel_difference.mae import PixelDifferenceFitnessMAE
from genetics_algorithm.fitness.pixel_difference.pixel_difference_fitness import _mse, _mae, _ssim, \
    PixelDifferenceFitness
from genetics_algorithm.models import Individual


class PixelDifferenceFitnessTest(unittest.TestCase):
    def test_no_difference_between_images_mse(self):
        # setup images
        img1 = np.array(Image.new("RGBA", (3, 3), "white")).astype(np.float32)
        img2 = np.array(Image.new("RGBA", (3, 3), "white")).astype(np.float32)
        result = _mse(img1, img2)
        self.assertEqual(0.0, result)

    def test_no_difference_between_images_mae(self):
        # setup images
        img1 = np.array(Image.new("RGB", (3, 3), "white")).astype(np.float32)
        img2 = np.array(Image.new("RGB", (3, 3), "white")).astype(np.float32)
        result = _mae(img1, img2)
        self.assertEqual(0.0, result)

    def test_no_difference_between_images_ssim(self):
        # setup images
        img1 = np.array(Image.new("RGB", (3, 3), "white")).astype(np.float32)
        img2 = np.array(Image.new("RGB", (3, 3), "white")).astype(np.float32)
        result = _ssim(img1, img2)
        self.assertEqual(0.0, result)

    def test_opposite_colour_images_ssim(self):
        # setup images
        img1 = np.array(Image.new("RGB", (3, 3), "white")).astype(np.float32)
        img2 = np.array(Image.new("RGB", (3, 3), "black")).astype(np.float32)
        result = _ssim(img1, img2)
        self.assertAlmostEqual(1.0, result, places=3)

    def test_partial_difference_mse(self):
        img1 = np.array([[0, 0],
                         [0, 0]]).astype(np.float32)

        img2 = np.array([[10, 0],
                         [0, 0]]).astype(np.float32)

        result = _mse(img1, img2)
        self.assertEqual(25.0, result)

    def test_evaluate_run(self):
        target_image = Image.open("resources/images/noche.png").convert("RGBA")
        ind = Individual(
            target_image.width,
            target_image.height,
            20,
        )

        pixel_difference_mae = PixelDifferenceFitnessMAE(target_image)
        pixel_difference = PixelDifferenceFitness(target_image)
        print("Start evaluating")
        result = pixel_difference.evaluate(ind )
        result_mae = pixel_difference_mae.evaluate(ind )
        print(result)
        print(result_mae)
        print(f"end")
        self.assertEqual(result_mae, result)


if __name__ == '__main__':
    unittest.main()
