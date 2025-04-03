import numpy

from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


class Task5(object):
    """
    Creates a matrix of random elements with given dimensions and performs some actions with the matrix.

    Obtains a new matrix by dividing all elements of the original matrix by its largest absolute value element.
    Calculates the variance of the elements of the new matrix with rounding to hundredths via the standard function
    and via the formula.
    """

    @repeating_program
    def run(self):
        """Do task actions with array and print results."""

        n, m = self._input_values()

        arr = numpy.random.randint(-100, 100, size=(n, m))
        print(arr)

        new_matrix = self._divide_matrix_by_max_abs_elem(arr)
        print("New matrix after divide:\n", new_matrix)

        var_func, var_formula = self._divide_matrix_by_max_abs_elem(new_matrix)
        print("Variance of array elements (with numpy method):", round(var_func, 2))
        print("Variance of elements (by formula):", round(var_formula, 2))

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

    @staticmethod
    def _divide_matrix_by_max_abs_elem(arr: numpy.ndarray):
        """
        Divides each element of a given matrix by its maximum absolute element.

        :param arr: A NumPy array representing the matrix whose elements will be divided by the maximum
        absolute element.

        :return: A NumPy array where each element is divided by the maximum absolute element of the input array.
        """

        max_abs_elem = numpy.max(numpy.abs(arr))

        return arr / max_abs_elem

    @staticmethod
    def _get_variance(arr: numpy.ndarray):
        """
        Computes the variance of an array using both the statistical function and a manual formula.

        This static method calculates the variance of the given numpy array using two different approaches:
        the built-in numpy statistical function and a formula that manually implements variance computation.
        It returns both results for comparison.

        :param arr: The input array for which the variance is to be calculated.
        :return: A tuple containing two values:
            - The variance calculated using numpy's built-in function.
            - The variance calculated using the manual formula.
        """

        variance_std_func = numpy.var(arr)

        mean_value = numpy.mean(arr)
        variance_formula = numpy.sum((arr - mean_value) ** 2) / arr.size

        return variance_std_func, variance_formula


if __name__ == '__main__':
    Task5().run()
