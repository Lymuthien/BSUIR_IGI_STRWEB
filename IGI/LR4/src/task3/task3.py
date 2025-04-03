import math

from .drawer import Drawer
from .math_models import TaylorSeries, TaylorSeriesLog
from ..utils.io_functions import input_with_validating


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
