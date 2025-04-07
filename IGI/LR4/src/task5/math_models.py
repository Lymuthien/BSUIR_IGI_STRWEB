import numpy


class MatrixProcessor(object):
    """
    Class for generating and performing operations on matrices:
    - Generates a matrix of random integers.
    - Normalizes the matrix elements by its maximum absolute value.
    - Computes the variance of matrix elements using two methods.
    """

    def __init__(self, rows: int, cols: int):
        """
        Initializes the MatrixProcessor by generating a random matrix with given dimensions.

        :param rows: Number of rows in the matrix.
        :param cols: Number of columns in the matrix.
        """

        self.matrix = numpy.random.randint(-100, 100, size=(rows, cols))

    def normalize_by_max_abs(self) -> numpy.ndarray:
        """
        Normalizes the matrix by dividing all elements by the maximum absolute value.

        :return: A new normalized matrix.
        """
        max_abs_elem = numpy.max(numpy.abs(self.matrix))

        return self.matrix / max_abs_elem

    def compute_variance(self) -> tuple[numpy.floating, float]:
        """
        Computes the variance of the matrix using two methods:
        1. Built-in numpy function.
        2. Manual formula for variance computation.

        :return: Tuple with two variance values: (numpy function result, manual formula result).
        """
        variance_std_func = numpy.var(self.matrix)

        mean_value = numpy.mean(self.matrix)
        variance_formula = numpy.sum((self.matrix - mean_value) ** 2) / self.matrix.size

        return variance_std_func, variance_formula
