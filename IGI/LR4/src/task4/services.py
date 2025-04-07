import math

from ..task3.drawer import Drawer
from .models import Triangle


class TriangleManager(object):
    """
    Manages operations and workflows related to a triangle.
    """

    def __init__(self, directory: str, drawer: Drawer):
        self._directory = directory
        self._drawer = drawer

    def draw_triangle(self, triangle: Triangle, title: str):
        """
        Draws the triangle using the Drawer utility and saves its visualization to a file.

        :param triangle: A `Triangle` instance to be visualized.
        :param title: The title of the visualization, provided by the user.
        """

        x_coords, y_coords = self._calculate_coordinates(triangle)

        self._drawer.plot_by_coords(
                x_coords,
                y_coords,
                title,
                f"{self._directory}triangle.png",
                triangle.color
        )

    @staticmethod
    def _calculate_coordinates(triangle: Triangle) -> tuple[tuple[float, ...], tuple[float, ...]]:
        """
        Calculates the x, y coordinates of the triangle's vertices based on the sides.

        :param triangle: A `Triangle` instance.
        :return: Tuple of x and y coordinates of the triangle's vertices.
        """

        a, b, c = triangle.sides

        x1, y1 = 0, 0
        x2, y2 = a, 0

        angle = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
        x3 = c * math.cos(angle)
        y3 = c * math.sin(angle)

        x_coords = (x1, x2, x3, x1)
        y_coords = (y1, y2, y3, y1)

        return x_coords, y_coords
