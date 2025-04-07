import math

from .models import Triangle
from ..task3.task3 import Drawer
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task4(ITask):
    """
    A triangle is constructed on three sides
    Class testing is performed.

    Functionality:
        - user input of parameter values;
        - checking the correctness of the entered data;
        - construction, coloring of the figure in the selected color entered from the keyboard,
        and signature of the figure with text entered from the keyboard;
        - output of the figure to the screen and to a file.
    """

    def __init__(self, directory: str):
        self._directory = directory

    @staticmethod
    def input_figure():
        """
        Prompts the user to input the sides and color of a triangle, validates the input,
        and creates a `Triangle` instance.

        :return: Tuple containing the sides and color of the triangle.
        """

        a = float(input_with_validating(lambda i: float(i) > 0, 'Enter a: '))
        b = float(input_with_validating(lambda i: float(i) > 0, 'Enter b: '))
        c = float(input_with_validating(lambda i: float(i) > 0, 'Enter c: '))
        color = input('Enter figure color (#rgb, #rrggbb or color name...): ').strip().lower()

        return a, b, c, color

    @repeating_program
    def run(self):
        """
        Main program method that drives the workflow of Task 4.

        - Prompts the user to input the sides and color of a triangle through `input_figure`.
        - If a valid triangle is created, prints its details.
        - Requests a title for the triangle and passes it to the `draw_triangle` method
          for visualization.

        If the triangle cannot be created due to invalid input values, the program prompts the user again.
        """
        try:
            triangle = Triangle(*self.input_figure())
        except ValueError as e:
            print(e)
            return

        print(triangle.name_of_class() + ': ' + str(triangle))
        self.draw_triangle(triangle, input('Enter figure title: '))

    def draw_triangle(self, triangle: Triangle, title: str):
        """
        Draws the triangle using the `Drawer` utility and saves its visualization to a file.

        The method uses the triangle's sides to compute the vertex coordinates
        and then calls a plotting utility to generate a visualization. The resulting
        image is saved as 'data/triangle.png'.

        :param triangle: A `Triangle` instance to be visualized.
        :param title: The title of the visualization, provided by the user.
        """

        a, b, c = triangle.sides
        color = triangle.color

        x1, y1 = 0, 0
        x2, y2 = a, 0

        angle = math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c))
        x3 = c * math.cos(angle)
        y3 = c * math.sin(angle)

        x_coords = (x1, x2, x3, x1)
        y_coords = (y1, y2, y3, y1)

        try:
            Drawer().plot_by_coords(x_coords, y_coords, title, f'{self._directory}triangle.png', color)
        except Exception as e:
            print(e)
