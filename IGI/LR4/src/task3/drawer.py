import matplotlib.pyplot as plt


class Drawer(object):
    """
    A class for visualizing data and creating plots using matplotlib.
    Provides methods to plot multiple graphs or a single graph with specified settings.
    """

    def __init__(self):
        """Initializes the Drawer object with a predefined set of colors for plotting."""

        self._colors = ('b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-')

    def plot_table(self,
                   graphics: tuple[tuple[tuple[float, ...], tuple[float, ...]], ...],
                   coord_names: tuple[str, str],
                   graphic_names: tuple[str, ...],
                   title: str,
                   filename: str):
        """
        Creates and saves a multi-line plot using provided data series.

        :param graphics: A tuple of data series to plot, where each series is a tuple of x and y values.
        :param coord_names: A tuple containing x and y axis labels.
        :param graphic_names: A tuple of labels for each graph in the series.
        :param title: The title of the plot.
        :param filename: The name of the file where the plot will be saved.
        """

        plt.figure(figsize=(10, 6))

        for i, graphic in enumerate(graphics):
            plt.plot(*graphic, self._colors[i], label=graphic_names[i])

        self._set_plot_settings(*coord_names, title=title)

        plt.savefig(filename)
        plt.show()

    def plot_by_coords(self,
                       x: tuple[float, ...],
                       y: tuple[float, ...],
                       title: str,
                       filename: str,
                       color: str = 'b-'):
        """
        Creates and saves a single plot based on provided x and y coordinates.

        :param x: A tuple containing the x coordinates for the plot.
        :param y: A tuple containing the y coordinates for the plot.
        :param title: The title of the plot.
        :param filename: The name of the file where the plot will be saved.
        :param color: The color and line format for the plot (default is 'b-' for a blue line).
        """

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, color=color, linewidth=2)
        plt.fill(x, y, color=color, alpha=0.5)
        plt.scatter(x[:-1], y[:-1], color='black', zorder=5)

        self._set_plot_settings('x', 'y', title, legend=False)
        plt.axis("equal")

        plt.savefig(filename)
        plt.show()

    @staticmethod
    def _set_plot_settings(x: str, y: str, title: str, legend: bool = True):
        """
        Configures plot settings such as grid, axis labels, title, and legend.

        :param x: The label for the x-axis.
        :param y: The label for the y-axis.
        :param title: The title of the plot.
        :param legend: Whether to display the legend on the plot (default is True).
        """

        plt.grid(True)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        if legend:
            plt.legend()
