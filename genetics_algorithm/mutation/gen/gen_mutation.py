import random
from genetics_algorithm.models import Polygon, Individual
from genetics_algorithm.mutation.mutation_method import MutationMethod

# Only a single locus (one randomly chosen Polygon from the array of N polygons)
# is targeted and mutated
class GenMutation(MutationMethod):
    def _tweak(self, individual: Individual, p_tweak: float):
        if random.random() > p_tweak:
            return None

        # TODO check implementation, maybe changes are way too small in each gen
        target_index = random.randint(0, len(individual.polygons) - 1)
        polygon = individual.polygons[target_index]
        self.single_polygon_tweak(polygon, individual, p_tweak)
        return None

    #Buenos dias, hice esto una funcion por que la vi repetida en muchos lados
    def single_polygon_tweak(self, polygon: Polygon, individual: Individual, p_tweak: float):
        if random.random() < 0.5:
            # Pick a vertex from the polygon
            vertex_idx = random.randint(0, 2)
            x, y = polygon.vertices[vertex_idx]

            # Shift the point by up to 15 pixels in any direction
            delta_x = random.randint(-15, 15)
            delta_y = random.randint(-15, 15)

            # Ensure the new vertex doesn't go outside the canvas boundaries
            new_x = max(0, min(individual.width, x + delta_x))
            new_y = max(0, min(individual.height, y + delta_y))

            # Update the polygon's vertices
            new_vertices = list(polygon.vertices)
            new_vertices[vertex_idx] = (new_x, new_y)
            polygon.vertices = tuple(new_vertices)

        else:
            # Change color
            channel_idx = random.randint(0, 3)
            color = list(polygon.color)

            # Shift the color value by up to 20 units
            delta_c = random.randint(-20, 20)

            # Ensure the color value stays between 0 and 255
            new_c = max(0, min(255, color[channel_idx] + delta_c))

            color[channel_idx] = new_c
            polygon.color = tuple(color)
        return None
