import datetime
import logging

from django.test import TestCase

from ..forms import ClientSignUpForm
from ..models import Client


class ClientSignUpFormTest(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_phone_number_field_label(self):
        form = ClientSignUpForm()
        self.assertTrue(
            form.fields["phone_number"].label is None
            or form.fields["phone_number"].label == "Phone number"
        )

    def test_phone_number_field_help_text(self):
        form = ClientSignUpForm()
        self.assertEqual(
            form.fields["phone_number"].help_text,
            "Format: +375(29)XXX-XX-XX",
        )

    def test_birth_date_field_label(self):
        form = ClientSignUpForm()
        self.assertTrue(
            form.fields["birth_date"].label is None
            or form.fields["birth_date"].label == "birth date"
        )

    def test_birth_date_field_help_text(self):
        form = ClientSignUpForm()
        self.assertEqual(
            form.fields["birth_date"].help_text,
            "User must be at least 18 y.o.",
        )

    def test_save_method_creates_client(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "phone_number": "+375(29)123-45-67",
            "birth_date": datetime.date(1990, 1, 1),
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        form = ClientSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.role, "client")

        self.assertTrue(Client.objects.get(pk=1))
