class Polygon:
    def __init__(self, vertices: tuple[tuple[int, int], ...], color: tuple[int, int, int, int]):
        self.vertices = vertices
        self.color = color

    def __post_init__(self):
        if len(self.color) != 4:
            raise ValueError("Color must be an RGBA tuple of length 4")
        if not all(0 <= c <= 255 for c in self.color):
            raise ValueError("RGBA values must be between 0 and 255")

        if len(self.vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")