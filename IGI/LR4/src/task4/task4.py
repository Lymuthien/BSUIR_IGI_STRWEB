from .models import Triangle
from .services import TriangleManager
from ..task3.task3 import Drawer
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task4(ITask):
    """
    A triangle is constructed on three sides.
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
            triangle_manager = TriangleManager(self._directory, Drawer())
            triangle = Triangle(*self.input_figure())

            print(triangle.name_of_class() + ': ' + str(triangle))
            triangle_manager.draw_triangle(triangle, input('Enter figure title: '))
        except Exception as e:
            print(e)
