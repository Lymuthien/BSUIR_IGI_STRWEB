import math
from statistics import median, mode, pvariance, pstdev

import matplotlib.pyplot as plt

from ..utils.io_functions import input_with_validating


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


class Drawer(object):
    def __init__(self):
        self._colors = ('b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-')

    def plot_table(self,
                   graphics: tuple[tuple[tuple[float, ...], tuple[float, ...]], ...],
                   coord_names: tuple[str, str],
                   graphic_names: tuple[str, ...],
                   title: str,
                   filename: str, ):
        plt.figure(figsize=(10, 6))

        for i, graphic in enumerate(graphics):
            plt.plot(*graphic, self._colors[i], label=graphic_names[i])

        self._set_plot_settings(*coord_names, title=title)
        plt.show()
        plt.savefig(filename)

    def plot_by_coords(self, x: tuple[float, ...], y: tuple[float, ...], title: str, filename: str, color: str = 'b-'):
        plt.figure(figsize=(10, 10))
        plt.plot(x, y, color=color, linewidth=2)
        plt.fill(x, y, color=color, alpha=0.5)
        plt.scatter(x[:-1], y[:-1], color='black', zorder=5)

        self._set_plot_settings('x', 'y', title, legend=False)
        plt.axis("equal")
        plt.show()
        plt.savefig(filename)

    @staticmethod
    def _set_plot_settings(x: str, y: str, title: str, legend: bool = True):
        plt.grid(True)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        if legend:
            plt.legend()


class Task3(object):
    def __init__(self):
        self._log_handler = TaylorSeriesLog()
        self._table = None
        self._drawer = Drawer()

    def run(self):
        """
        Calculate the value of the function ln(1+x) using the expansion of the function into a
        taylor series with a given calculation accuracy.
        """
        x, eps = self._input_values()

        f_x, n = self._log_handler.find_n_for_series(eps, x)
        self._print_info_about_series(f_x)

        self._table = self._create_x_table(eps)
        self._plot_ln()
        self._plot_n()

    @staticmethod
    def _print_info_about_series(series: TaylorSeries):
        print(f'СА элементов: {series.average_value()}\n'
              f'Медиана: {series.median()}\n'
              f'Мода: {series.mode()}\n'
              f'Дисперсия: {series.variance()}\n'
              f'СКО: {series.stdev()}')

    def _create_x_table(self, eps: float):
        table = []
        for x in range(-99, 99, 10):
            f_x, n = self._log_handler.find_n_for_series(eps, x * 0.01)
            table.append((x * 0.01, n, f_x.sum(), math.log(x * 0.01 + 1), eps))

        return table

    def _plot_ln(self):
        x = tuple(row[0] for row in self._table)
        y_taylor = tuple(row[2] for row in self._table)
        y_math = tuple(row[3] for row in self._table)

        self._drawer.plot_table(((x, y_taylor), (x, y_math)), ('x', 'y'),
                                ('y = taylor_ln(x)', 'y = math_ln(x)'),
                          'Сравнение графиков натуральных логарифмов через ряд тейлора и math',
                          'data/ln_graphics.png')

    def _plot_n(self):
        x = tuple(row[0] for row in self._table)
        n = tuple(row[1] for row in self._table)

        self._drawer.plot_table(((x, n),), ('x', 'n'), ('n(x)',),
                          'Зависимость n членов ряда тейлора от x',
                          'data/n_graphics.png')

    @staticmethod
    def _input_values():
        x = float(input_with_validating(lambda i: abs(float(i)) < 1 and float(i) != 0,
                                        'Enter the value of x: (-1; 0) or (0; 1): '))
        eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))
        return x, eps


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
