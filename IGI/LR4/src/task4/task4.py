import math

from .models import Triangle
from ..task3.task3 import Drawer
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


class Task4(object):
    @staticmethod
    def input_figure():
        a = float(input_with_validating(lambda i: float(i) > 0, 'Enter a: '))
        b = float(input_with_validating(lambda i: float(i) > 0, 'Enter b: '))
        c = float(input_with_validating(lambda i: float(i) > 0, 'Enter c: '))
        color = input('Enter figure color (red, green, blue): ').strip().lower()

        try:
            return Triangle(a, b, c, color)
        except ValueError as e:
            print(e)
            return None

    @repeating_program
    def run(self):
        triangle = self.input_figure()
        if triangle is None:
            return

        print('Triangle: ' + str(triangle))
        self.draw_triangle(triangle, input('Enter figure title: '))

    @staticmethod
    def draw_triangle(triangle: Triangle, title: str):
        a, b, c = triangle.sides()
        color = triangle.color()

        x1, y1 = 0, 0
        x2, y2 = a, 0

        angle = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
        x3 = c * math.cos(angle)
        y3 = c * math.sin(angle)

        x_coords = (x1, x2, x3, x1)
        y_coords = (y1, y2, y3, y1)

        try:
            Drawer().plot_by_coords(x_coords, y_coords, title, 'data/triangle.png', color)
        except Exception as e:
            print(e)
