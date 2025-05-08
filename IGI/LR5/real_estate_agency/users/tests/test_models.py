from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import User, Profile, Client, Employee


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            first_name="Big",
            last_name="Bob",
            role="client",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="loo",
            password="<PASSWORD>",
        )

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_first_name_label(self):
        field_label = self.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        field_label = self.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_role_label(self):
        field_label = self.user._meta.get_field('role').verbose_name
        self.assertEqual(field_label, 'role')

    def test_phone_number_label(self):
        field_label = self.user._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'phone number')

    def test_birth_date_label(self):
        field_label = self.user._meta.get_field('birth_date').verbose_name
        self.assertEqual(field_label, 'birth date')

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_role_max_length(self):
        max_length = self.user._meta.get_field('role').max_length
        self.assertEqual(max_length, 20)

    def test_phone_number_max_length(self):
        max_length = self.user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 20)

    def test_object_name_is_username_comma_role(self):
        expected_object_name = f"{self.user.username} {self.user.role}"
        self.assertEqual(expected_object_name, str(self.user))

    def test_object_has_profile(self):
        self.assertTrue(hasattr(self.user, "profile"))

    def test_role_choices(self):
        valid_choices = User.ROLE_CHOICES

        for valid_choice in valid_choices:
            self.user.role = valid_choice
            self.assertEqual(self.user.role, valid_choice)

    def test_role_set_invalid_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            role = "invalid"
            user = User(
                username=f'test_{role}',
                role=role,
                phone_number='+375(29)123-45-67',
                birth_date=datetime(1990, 1, 1),
                first_name='Big',
                last_name='Bob',
            )
            user.full_clean()


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            first_name="Big",
            last_name="Bob",
            role="client",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="loo",
            password="<PASSWORD>",
        )

    def setUp(self):
        self.profile = Profile.objects.get(pk=1)

    def test_user_label(self):
        field_label = self.profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_user_relation(self):
        self.assertEqual(self.profile.user.username, "loo")
        self.assertEqual(self.profile.user.role, "client")

    def test_object_name_is_username_profile(self):
        expected_object_name = f"{self.profile.user.username} Profile"
        self.assertEqual(expected_object_name, str(self.profile))

    def test_object_created_automatically(self):
        new_user = User.objects.create(
            first_name="New",
            last_name="User",
            role="client",
            phone_number="+375(29)888-88-88",
            birth_date=datetime(1990, 1, 1),
            username="new_user",
            password="<PASSWORD>",
        )
        self.assertTrue(hasattr(new_user, 'profile'))
        new_user.full_clean()


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            first_name="Client",
            last_name="Test",
            role="client",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="client_test",
            password="<PASSWORD>",
        )
        Client.objects.create(user=user)

    def setUp(self):
        self.client = Client.objects.get(pk=1)

    def test_user_label(self):
        field_label = self.client._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_work_place_label(self):
        field_label = self.client._meta.get_field('work_place').verbose_name
        self.assertEqual(field_label, 'work place')

    def test_work_place_max_length(self):
        max_length = self.client._meta.get_field('work_place').max_length
        self.assertEqual(max_length, 100)

    def test_work_place_default(self):
        self.assertEqual(self.client.work_place, "Nowhere")

    def test_object_name_is_username(self):
        expected_object_name = f"{self.client.user.username}"
        self.assertEqual(expected_object_name, str(self.client))

    def test_object_has_correct_user(self):
        self.assertEqual(self.client.user.role, "client")
        self.assertEqual(self.client.user.first_name, "Client")


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            first_name="Employee",
            last_name="Test",
            role="employee",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="employee_test",
            password="<PASSWORD>",
        )
        user2 = User.objects.create(
            first_name="Client",
            last_name="Test",
            role="client",
            phone_number="+375(29)888-88-88",
            birth_date=datetime(2000, 1, 1),
            username="client_for_employee",
            password="<PASSWORD>",
        )
        employee = Employee.objects.create(user=user1, hire_date=datetime(2020, 1, 1))
        client = Client.objects.create(user=user2)
        employee.clients.add(client)

    def setUp(self):
        self.employee = Employee.objects.get(pk=1)

    def test_user_label(self):
        field_label = self.employee._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_hire_date_label(self):
        field_label = self.employee._meta.get_field('hire_date').verbose_name
        self.assertEqual(field_label, 'hire date')

    def test_clients_label(self):
        field_label = self.employee._meta.get_field('clients').verbose_name
        self.assertEqual(field_label, 'clients')

    def test_object_name_is_username(self):
        expected_object_name = f"{self.employee.user.username}"
        self.assertEqual(expected_object_name, str(self.employee))

    def test_object_has_correct_user(self):
        self.assertEqual(self.employee.user.role, "employee")
        self.assertEqual(self.employee.user.first_name, "Employee")

    def test_object_client_relationship(self):
        client = self.employee.clients.first()
        self.assertEqual(client.user.username, "client_for_employee")
        self.assertEqual(client.user.role, "client")
