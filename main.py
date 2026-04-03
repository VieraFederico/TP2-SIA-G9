from genetics_algorithm.models.Individual import Individual

# Handles GA's main state and logic including initialization of
# population, all of GA's phases, termination.

if __name__ == '__main__':
    ind = Individual(width=400, height=400, polygons_per_ind=20)

    img = ind.draw()

    img.save("random_triangles.png")