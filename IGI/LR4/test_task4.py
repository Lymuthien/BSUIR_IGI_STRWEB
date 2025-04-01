import unittest

from src.task4.task4 import Color, Triangle


class TestColor(unittest.TestCase):
    def test_color_initialization(self):
        color = Color("red")
        self.assertEqual(color.color, "red")  # Проверка начального значения

    def test_color_setter(self):
        color = Color("red")
        color.color = "blue"  # Изменение цвета через сеттер
        self.assertEqual(color.color, "blue")

    def test_color_deleter(self):
        colorr = Color("red")
        del colorr.color
        with self.assertRaises(AttributeError):
            _ = colorr.color


class TestTriangle(unittest.TestCase):

    def test_triangle_area_valid(self):
        triangle = Triangle(3, 4, 5, "green")
        self.assertAlmostEqual(triangle.square(), 6.0)

    def test_triangle_str_method(self):
        triangle = Triangle(3, 4, 5, "green")
        triangle_str = str(triangle)
        self.assertEqual(triangle_str, "a: 3, b: 4, c: 5, color: green")

    def test_triangle_name_of_class(self):
        self.assertEqual(Triangle.name_of_class(), "Triangle")


if __name__ == "__main__":
    unittest.main()
