import random
from PIL import Image, ImageDraw

from genetics_algorithm.models.Polygon import Polygon


class Individual:
    def __init__(self,
                 width: int,
                 height: int,
                 polygons_per_ind: int = 0,
                 polygons: list[Polygon] = None):

        #Canvas size
        self.width = width
        self.height = height
        self.polygons_per_ind = polygons_per_ind
        self.fitness: float = 0.0
        self.relative_fitness: float = 0.0

        if polygons is not None:
            self.polygons = polygons
        else:
            self.polygons = self._generate_random_polygons(polygons_per_ind)

    def _generate_random_polygons(self, amount: int) -> list[Polygon]:
        polygons = []
        for _ in range(amount):
            polygons.append(self.generate_random_polygon())
        return polygons

    def generate_random_polygon(self) -> Polygon:
        v1 = (random.randint(0, self.width), random.randint(0, self.height))
        v2 = (random.randint(0, self.width), random.randint(0, self.height))
        v3 = (random.randint(0, self.width), random.randint(0, self.height))

        color = (random.randint(0, 255), random.randint(0, 255),
                 random.randint(0, 255), random.randint(0, 255))

        return Polygon(vertices=(v1, v2, v3), color=color)

    def draw(self) -> Image.Image:
        base_image = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))

        for polygon in self.polygons:
            poly_layer = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(poly_layer)

            draw.polygon(polygon.vertices, fill=polygon.color)

            base_image = Image.alpha_composite(base_image, poly_layer)

        return base_image

    def get_fitness(self) -> float:
        return self.fitness


    def get_polygons(self) -> list[Polygon]:
        return self.polygons

    def clone(self):
        polygons = [polygon.clone() for polygon in self.polygons]
        return Individual(self.width, self.height, self.polygons_per_ind, polygons)

