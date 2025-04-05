import math
from statistics import median, mode, pvariance, pstdev


class TaylorSeries(object):
    """
    Represents a Taylor series and provides methods to calculate statistics
    for the series, such as sum, average, median, mode, variance, and standard deviation.
    """

    def __init__(self, series: tuple[float, ...]):
        """
        Initializes the TaylorSeries object with a specific series.

        :param series: The series of terms that make up the Taylor series.
        """

        self._series = series
        self._n = len(series)

    @property
    def n(self):
        """Returns the number of terms in the series."""

        return self._n

    def sum(self):
        """Calculates the sum of all terms in the series."""

        return sum(self._series)

    def average_value(self):
        """Calculates the average value of the series."""

        return sum(self._series) / self._n

    def median(self):
        """Calculates the median of the series."""

        return median(self._series)

    def mode(self):
        """Calculates the mode (the most common value) of the series."""

        return mode(self._series)

    def variance(self):
        """Calculates the variance of the series."""

        return pvariance(self._series)

    def stdev(self):
        """Calculates the standard deviation of the series."""

        return pstdev(self._series)


class TaylorSeriesLogarithm(TaylorSeries):
    """Provides methods to approximate the natural logarithm using Taylor series expansion."""

    def __init__(self, epsilon: float, x: float):
        """
        Initialize a sequence instance with elements calculated using a mathematical
        series based on the provided epsilon and x values.

        :param epsilon: The precision value used for defining the convergence of the series.
        :param x: The base value used in the series calculations.
        """

        n = self._find_min_n_for_epsilon(epsilon, x)

        super().__init__(tuple(pow(-1, i - 1) * pow(x, i) / i for i in range(1, n + 1)))

    @staticmethod
    def _find_min_n_for_epsilon(epsilon: float, x: float) -> int:
        """
        Approximates ln(value) with a given precision using Taylor series.

        :param epsilon: The acceptable error threshold for approximation.
        :param x: The input value for which ln(value) is being approximated.
        :return: The number of terms used.
        """

        math_result = math.log(x + 1)
        num_of_members = 1

        for num_of_members in range(1, 501):
            result = TaylorSeries(tuple(pow(-1, i - 1) * pow(x, i) / i for i in range(1, num_of_members + 1)))
            if abs(result.sum() - math_result) <= epsilon:
                return num_of_members

        return num_of_members
