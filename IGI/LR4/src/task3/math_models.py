import math
from statistics import median, mode, pvariance, pstdev


class TaylorSeries(object):
    def __init__(self, series: tuple[float, ...]):
        self._series = series
        self._n = len(series)

    @property
    def n(self):
        return self._n

    def sum(self):
        return sum(self._series)

    def average_value(self):
        return sum(self._series) / self._n

    def median(self):
        return median(self._series)

    def mode(self):
        return mode(self._series)

    def variance(self):
        return pvariance(self._series)

    def stdev(self):
        return pstdev(self._series)


class TaylorSeriesLog(object):
    @staticmethod
    def find_n_for_series(epsilon: float, value: float) -> tuple[TaylorSeries, int]:
        """
        Approximates ln(value) using Taylor series expansion.

        :param epsilon: Required precision (acceptable error threshold).
        :param value: Input value for natural logarithm calculation.
        :return: Tuple containing (approximation result, terms used).
        """
        result = None
        math_result = math.log(value + 1)
        num_of_members = 1

        for num_of_members in range(1, 501):
            result = TaylorSeriesLog.taylor_series_of_ln(value, num_of_members)
            if abs(result.sum() - math_result) <= epsilon:
                return result, num_of_members

        return result, num_of_members

    @staticmethod
    def taylor_series_of_ln(x: float, n: int) -> TaylorSeries:
        """
        Calculates the ln of the argument x + 1 for a given number of terms of the taylor series.

        :param x: Value in range (-1; 1).
        :param n: Number of terms of the taylor series in range [1; +inf].
        :return: Sum of the terms of the taylor series.
        """
        if abs(x) >= 1 or n < 1:
            raise ValueError

        return TaylorSeries(tuple(pow(-1, i - 1) * pow(x, i) / i for i in range(1, n + 1)))
