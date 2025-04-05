from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def square(self) -> float: ...


class Color(object):
    def __init__(self, color: str):
        self._color: str = color

    def get_color(self):
        return self._color

    def set_color(self, value):
        self._color = value

    color = property(fget=get_color, fset=set_color, doc='Color property')


class Triangle(Figure):
    name = 'Triangle'

    def __init__(self, a: float, b: float, c: float, color: str):
        self._a: float = a
        self._b: float = b
        self._c: float = c
        self._color: Color = Color(color)
        self.validate_sides(a, b, c)

    def __str__(self):
        return 'a: {}, b: {}, c: {}, color: {}, square: {}'.format(
            self._a, self._b, self._c, self._color.color, self.square())

    def square(self) -> float:
        s = (self._a + self._b + self._c) / 2
        area = (s * (s - self._a) * (s - self._b) * (s - self._c)) ** 0.5
        return area

    def sides(self) -> tuple[float, float, float]:
        return self._a, self._b, self._c

    def color(self) -> str:
        return self._color.color

    @staticmethod
    def validate_sides(a: float, b: float, c: float):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError('The value of a, b, or c must be greater than 0.')

        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError('The sum of two sides must be less than the length of the third side.')

    @classmethod
    def name_of_class(cls):
        return cls.name
