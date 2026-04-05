class Polygon:
    def __init__(self, vertices: tuple[tuple[int, int], ...], color: tuple[int, int, int, int]):
        if len(color) != 4:
            raise ValueError("Color must be an RGBA tuple of length 4")
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("RGBA values must be between 0 and 255")
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        self.vertices = vertices
        self.color = color
