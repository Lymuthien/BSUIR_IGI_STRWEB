from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from ..utils import RestrictedAgeValidator

class RestrictedAgeValidatorTests(TestCase):
    def setUp(self):
        self.fixed_today = date(2025, 5, 8)
        self.original_date = date
        self.validator = RestrictedAgeValidator(limit_value=18)

    def test_valid_age(self):
        birth_date = date(2000, 5, 8)
        try:
            self.validator(birth_date)
        except ValidationError:
            self.fail("ValidationError raised for valid age")

    def test_invalid_age(self):
        birth_date = date(2015, 5, 9)
        with self.assertRaises(ValidationError) as cm:
            self.validator(birth_date)
        self.assertEqual(cm.exception.code, "restricted_age")

    def test_future_birth_date(self):
        birth_date = date(2030, 5, 8)
        with self.assertRaises(ValidationError) as cm:
            self.validator(birth_date)
        self.assertEqual(cm.exception.code, "restricted_age")

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            self.validator("2000-05-08")
