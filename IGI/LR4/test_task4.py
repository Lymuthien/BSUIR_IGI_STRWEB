import unittest

from src.task4.models import Color, Triangle
from src.task4.services import TriangleManager
from src.task3.drawer import Drawer


class TestColor(unittest.TestCase):
    def test_color_initialization(self):
        color = Color("red")
        self.assertEqual(color.color, "red")

    def test_color_setter(self):
        color = Color("red")
        color.color = "blue"
        self.assertEqual(color.color, "blue")


class TestTriangle(unittest.TestCase):
    def test_invalid_triangle_sides(self):
        with self.assertRaises(ValueError):
            Triangle(1, 2, 10, "blue")

    def test_triangle_area_valid(self):
        triangle = Triangle(3, 4, 5, "green")
        self.assertAlmostEqual(triangle.square(), 6.0)

    def test_triangle_str_method(self):
        triangle = Triangle(3, 4, 5, "green")
        triangle_str = str(triangle)
        self.assertEqual(triangle_str, "a: 3, b: 4, c: 5, color: green, square: 6.0")

    def test_triangle_name_of_class(self):
        self.assertEqual(Triangle.name_of_class(), "Triangle")

    def test_sides(self):
        triangle = Triangle(3, 4, 5, "green")
        self.assertEqual(triangle.sides, (3, 4, 5))

    def test_color(self):
        triangle = Triangle(3, 4, 5, "green")
        self.assertEqual(triangle.color, "green")

    def test_name_of_class(self):
        self.assertEqual(Triangle.name_of_class(), "Triangle")


class TestTriangleManager(unittest.TestCase):
    def setUp(self):
        self.drawer = Drawer()
        self.directory = "test_directory/"
        self.triangle_manager = TriangleManager(self.directory, self.drawer)
        self.triangle = Triangle(3, 4, 5, "red")

    def test_calculate_coordinates(self):
        x_coords, y_coords = self.triangle_manager.calculate_coordinates(self.triangle)
        self.assertEqual(len(x_coords), 4)
        self.assertEqual(len(y_coords), 4)


if __name__ == "__main__":
    unittest.main()
