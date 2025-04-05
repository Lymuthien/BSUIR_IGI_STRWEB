import math

from .drawer import Drawer
from .math_models import TaylorSeries, TaylorSeriesLogarithm
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task3(ITask):
    def __init__(self, directory: str):
        self._log_handler = TaylorSeriesLogarithm
        self._table = None
        self._directory = directory
        self._drawer = Drawer()

    @repeating_program
    def run(self):
        """
        Calculate the value of the function ln(1+x) using the expansion of the function into a
        taylor series with a given calculation accuracy.
        """

        x, eps = self._input_values()

        series = self._log_handler(eps, x)
        self._print_info_about_series(series)

        self._table = self._create_x_table(eps)
        self._plot_ln()
        self._plot_n()

    @staticmethod
    def _print_info_about_series(series: TaylorSeries):
        print(f'Average value: {series.average_value()}\n'
              f'Median: {series.median()}\n'
              f'Mode: {series.mode()}\n'
              f'Variance: {series.variance()}\n'
              f'Stdev: {series.stdev()}')

    def _create_x_table(self, eps: float):
        table = []
        for x in range(-99, 99, 1):
            f_x = self._log_handler(eps, x * 0.01)
            table.append((x * 0.01, f_x.n, f_x.sum(), math.log(x * 0.01 + 1), eps))

        return table

    def _plot_ln(self):
        x = tuple(row[0] for row in self._table)
        y_taylor = tuple(row[2] for row in self._table)
        y_math = tuple(row[3] for row in self._table)

        self._drawer.plot_table(((x, y_taylor), (x, y_math)), ('x', 'y'),
                                ('y = taylor_ln(x)', 'y = math_ln(x)'),
                                'Comparison of natural logarithm graphs using Taylor series and math',
                                f'{self._directory}/ln_graphics.png')

    def _plot_n(self):
        x = tuple(row[0] for row in self._table)
        n = tuple(row[1] for row in self._table)

        self._drawer.plot_table(((x, n),), ('x', 'n'), ('n(x)',),
                                'Dependence of the number of Taylor series terms on x',
                                f'{self._directory}/n_graphics.png')

    @staticmethod
    def _input_values():
        x = float(input_with_validating(lambda i: abs(float(i)) < 1 and float(i) != 0,
                                        'Enter the value of x: (-1; 0) or (0; 1): '))
        eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))
        return x, eps
