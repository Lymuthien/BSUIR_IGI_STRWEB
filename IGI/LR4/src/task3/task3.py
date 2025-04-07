from .drawer import Drawer
from .math_models import TaylorSeries, TaylorSeriesLogarithm, TaylorSeriesLogTable
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task3(ITask):
    """
    Expansion according to the given accuracy in the Taylor logarithm series for the given x.
    Definition:
        - arithmetic mean of the elements of the sequence;
        - median;
        - mode;
        - dispersion;
        - standard deviation of the sequence;

    Graphs of different colors are drawn in one coordinate axis
    (for the expansion of math.log and manual in the Taylor series).
    """
    X_START, X_END, X_STEP = -99, 99, 1

    def __init__(self, directory: str):
        self._log_handler = TaylorSeriesLogarithm
        self._table = None
        self._table_manager = TaylorSeriesLogTable
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
        print(series)

        self._table = self._table_manager.create_table(self._log_handler, eps)
        self._plot_ln()
        self._plot_n()

    def _plot_ln(self):
        """Plots the graphs of the natural logarithm using the Taylor series and the math.log function."""

        x, y_taylor, y_math = self._table_manager.extract_columns(self._table, 'x', 'fx', 'math_f')

        self._drawer.plot_table(((x, y_taylor), (x, y_math)), ('x', 'y'),
                                ('y = taylor_ln(x)', 'y = math_ln(x)'),
                                'Comparison of natural logarithm graphs using Taylor series and math',
                                f'{self._directory}ln_graphics.png')

    def _plot_n(self):
        """Plots the dependence of the number of terms on x."""

        x, n = self._table_manager.extract_columns(self._table, 'x', 'n')

        self._drawer.plot_table(((x, n),), ('x', 'n'), ('n(x)',),
                                'Dependence of the number of Taylor series terms on x',
                                f'{self._directory}n_graphics.png')

    @staticmethod
    def _input_values():
        """Prompts the user to input x and eps with validation."""

        x = float(input_with_validating(lambda i: abs(float(i)) < 1 and float(i) != 0,
                                        'Enter the value of x: (-1; 0) or (0; 1): '))
        eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))
        return x, eps
