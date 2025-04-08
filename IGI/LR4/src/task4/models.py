from abc import ABC, abstractmethod


class Figure(ABC):
    """
    Abstract base class for geometric figures.

    Classes inheriting from Figure must implement the `square` method.
    """

    @abstractmethod
    def square(self) -> float: ...


class Color(object):
    """
    Class representing the color of a figure.

    The color is stored as a string and can be accessed or modified using the `color` property.
    """

    def __init__(self, color: str):
        """
        Initialize the color of a figure.

        :param color: The color of the figure as a string (e.g., "red", "blue").
        """

        self._color: str = color

    def get_color(self) -> str:
        """Get the current color of the figure."""

        return self._color

    def set_color(self, value: str):
        """
        Set (update) the color of the figure.

        :param value: The new color of the figure as a string.
        """

        self._color = value

    color = property(fget=get_color, fset=set_color, doc="Color property")


class Triangle(Figure):
    """
    Class representing a triangle, which is a geometric figure with three sides.

    name: The class-level name of the figure (Triangle).
    """

    name = 'Triangle'

    def __init__(self, a: float, b: float, c: float, color: str):
        """
        Initialize a triangle with the given sides and color.

        :param a: The length of side a.
        :param b: The length of side b.
        :param c: The length of side c.
        :param color: The color of the triangle as a string.
        :raises ValueError: If the side lengths are invalid (e.g., non-positive or not forming a valid triangle).
        """

        self._a: float = a
        self._b: float = b
        self._c: float = c
        self._color: Color = Color(color)
        self._validate_sides(a, b, c)

    def __str__(self):
        """
        Return a string representation of the triangle instance.

        The string includes the values of its sides, the color, and the square (area) of the triangle.

        :return: A formatted string describing the triangle.
        """

        return 'a: {}, b: {}, c: {}, color: {}, square: {}'.format(
            self._a, self._b, self._c, self._color.color, self.square())

    def square(self) -> float:
        """
        Calculate the area of the triangle using Heron's formula.

        :return: The area of the triangle as a float.
        """

        s = (self._a + self._b + self._c) / 2  # Semi-perimeter
        area = (s * (s - self._a) * (s - self._b) * (s - self._c)) ** 0.5
        return area

    @property
    def sides(self) -> tuple[float, float, float]:
        """
        Get the lengths of the sides of the triangle.

        :return: A tuple containing the lengths of the three sides as floats.
        """

        return self._a, self._b, self._c

    @property
    def color(self) -> str:
        """
        Get the color of the triangle.

        :return: The color of the triangle as a string.
        """

        return self._color.color

    @staticmethod
    def _validate_sides(a: float, b: float, c: float):
        """
        Validate the lengths of the triangle's sides.

        A valid triangle must satisfy these conditions:
        - Each side length must be greater than 0.
        - The sum of any two sides must be greater than the length of the third side.

        :param a: The length of side a.
        :param b: The length of side b.
        :param c: The length of side c.
        :raises ValueError: If any condition is violated.
        """

        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError('The value of a, b, or c must be greater than 0.')

        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError('The sum of two sides must be greater than the length of the third side.')

    @classmethod
    def name_of_class(cls) -> str:
        """
        Get the class-level name of the figure.

        :return: The name of the class (Triangle).
        """

        return cls.name
