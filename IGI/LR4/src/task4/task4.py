import math
from abc import ABC, abstractmethod

from ..task3.task3 import Drawer
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


class Figure(ABC):
    @abstractmethod
    def square(self) -> float: ...


class Color(object):
    def __init__(self, color: str):
        self._color: str = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value

    @color.deleter
    def color(self):
        del self._color


class Triangle(Figure):
    name = 'Triangle'

    def __init__(self, a: float, b: float, c: float, color: str):
        self._a: float = a
        self._b: float = b
        self._c: float = c
        self._color: Color = Color(color)
        self.validate_sides(a, b, c)

    def square(self) -> float:
        s = (self._a + self._b + self._c) / 2
        area = (s * (s - self._a) * (s - self._b) * (s - self._c)) ** 0.5
        return area

    def __str__(self):
        return 'a: {}, b: {}, c: {}, color: {}, square: {}'.format(
            self._a, self._b, self._c, self._color.color, self.square())

    def sides(self) -> tuple[float, float, float]:
        return self._a, self._b, self._c

    def color(self) -> str:
        return self._color.color

    @staticmethod
    def validate_sides(a: float, b: float, c: float):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError('The value of a, b, or c must be greater than 0.')

        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError('The sum of two sides must be less than the length of the third side.')

    @classmethod
    def name_of_class(cls):
        return cls.name


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
