import random
from PIL import Image, ImageDraw

from genetics_algorithm.models.Polygon import Polygon



class Individual:
    def __init__(self, width: int, height: int, polygons_per_ind: int):
        self.width = width
        self.height = height
        self.polygons = self._generate_random_polygons(polygons_per_ind)

    def _generate_random_polygons(self, amount: int) -> list[Polygon]:
        polygons = []
        for z_index in range(amount):
            # For now, default polygon is triangle
            v1 = (random.randint(0, self.width), random.randint(0, self.height))
            v2 = (random.randint(0, self.width), random.randint(0, self.height))
            v3 = (random.randint(0, self.width), random.randint(0, self.height))

            color = (random.randint(0, 255), random.randint(0, 255),
                     random.randint(0, 255), random.randint(0, 255))

            polygons.append(Polygon(vertices=(v1, v2, v3), color=color, z_index=z_index))
        return polygons

    def draw(self) -> Image.Image:
        base_image = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))

        for polygon in sorted(self.polygons, key=lambda p: p.z_index):
            poly_layer = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(poly_layer)

            draw.polygon(polygon.vertices, fill=polygon.color)

            base_image = Image.alpha_composite(base_image, poly_layer)

        return base_image