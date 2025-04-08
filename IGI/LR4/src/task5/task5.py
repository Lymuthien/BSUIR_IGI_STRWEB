from .math_models import MatrixProcessor
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task5(ITask):
    """
    Creates a matrix of random elements with given dimensions and performs some actions with the matrix.

    Obtains a new matrix by dividing all elements of the original matrix by its largest absolute value element.
    Calculates the variance of the elements of the new matrix with rounding to hundredths via the standard function
    and via the formula.
    """

    @repeating_program
    def run(self):
        """Do task actions with array and print results."""

        try:
            n, m = self._input_values()

            processor = MatrixProcessor(n, m)
            print("Original matrix:\n", processor.matrix)

            normalized_matrix = processor.normalize_by_max_abs()
            print("Normalized matrix:\n", normalized_matrix)

            var_func, var_formula = processor.compute_variance()
            print("Variance with numpy method:", round(var_func, 2))
            print("Variance with formula:", round(var_formula, 2))

        except Exception as e:
            print(e)

    @staticmethod
    def _input_values():
        """
        Input values:
            - n: The number of rows in the matrix.
            - m: The number of columns in the matrix.

        :return: input values as tuple(n, m).
        """

        n = int(input_with_validating(lambda x: int(x) > 0, 'Enter n: '))
        m = int(input_with_validating(lambda x: int(x) > 0, 'Enter m: '))

        return n, m
