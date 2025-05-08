from django.core.validators import MinValueValidator
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
from datetime import date
from users.models import User, Employee, Client
from ..models import (
    Estate,
    ServiceCategory,
    Service,
    Sale,
    PurchaseRequest,
    PurchaseRequestManager,
)


class ServiceCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ServiceCategory.objects.create(name="Test Category")

    def setUp(self):
        self.category = ServiceCategory.objects.get(pk=1)

    def test_name_label(self):
        field_label = self.category._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        max_length = self.category._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_name_help_text(self):
        help_text = self.category._meta.get_field("name").help_text
        self.assertEqual(help_text, "Enter the service category name")

    def test_str_representation(self):
        self.assertEqual(str(self.category), self.category.name)


class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = ServiceCategory.objects.create(name="Test Category")
        Service.objects.create(
            name="Test Service", category=category, cost=Decimal("100.00")
        )

    def setUp(self):
        self.service = Service.objects.get(pk=1)

    def test_name_label(self):
        field_label = self.service._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_category_label(self):
        field_label = self.service._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "category")

    def test_cost_label(self):
        field_label = self.service._meta.get_field("cost").verbose_name
        self.assertEqual(field_label, "cost")

    def test_name_max_length(self):
        max_length = self.service._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_name_help_text(self):
        help_text = self.service._meta.get_field("name").help_text
        self.assertEqual(help_text, "Enter the estate category name")

    def test_category_relation(self):
        self.assertEqual(self.service.category.name, "Test Category")

    def test_meta_ordering(self):
        self.assertEqual(Service._meta.ordering, ["category__name", "name"])

    def test_str_representation(self):
        expected_str = f"({str(self.service.category)[:2]}) - {self.service.name}"
        self.assertEqual(str(self.service), expected_str)


class EstateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = ServiceCategory.objects.create(name="Test Category")
        service = Service.objects.create(
            name="Test Service", category=category, cost=Decimal("100.00")
        )
        Estate.objects.create(
            cost=Decimal("100000.00"),
            area=Decimal("50.00"),
            category=service,
            description="Test description",
            address="Test Address 123",
        )

    def setUp(self):
        self.estate = Estate.objects.get(pk=1)

    def test_cost_label(self):
        field_label = self.estate._meta.get_field("cost").verbose_name
        self.assertEqual(field_label, "cost")

    def test_area_label(self):
        field_label = self.estate._meta.get_field("area").verbose_name
        self.assertEqual(field_label, "area")

    def test_category_label(self):
        field_label = self.estate._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "category")

    def test_description_label(self):
        field_label = self.estate._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "description")

    def test_image_label(self):
        field_label = self.estate._meta.get_field("image").verbose_name
        self.assertEqual(field_label, "image")

    def test_address_label(self):
        field_label = self.estate._meta.get_field("address").verbose_name
        self.assertEqual(field_label, "address")

    def test_cost_validators(self):
        validators = self.estate._meta.get_field("cost").validators
        self.assertTrue(
            any(
                isinstance(v, MinValueValidator) and v.limit_value == 0.01
                for v in validators
            )
        )

    def test_area_validators(self):
        validators = self.estate._meta.get_field("area").validators
        self.assertTrue(
            any(
                isinstance(v, MinValueValidator) and v.limit_value == 0.01
                for v in validators
            )
        )

    def test_description_max_length(self):
        max_length = self.estate._meta.get_field("description").max_length
        self.assertEqual(max_length, 2000)

    def test_address_max_length(self):
        max_length = self.estate._meta.get_field("address").max_length
        self.assertEqual(max_length, 200)

    def test_cost_help_text(self):
        help_text = self.estate._meta.get_field("cost").help_text
        self.assertEqual(help_text, "Enter the estate cost")

    def test_area_help_text(self):
        help_text = self.estate._meta.get_field("area").help_text
        self.assertEqual(help_text, "Enter the estate area")

    def test_category_help_text(self):
        help_text = self.estate._meta.get_field("category").help_text
        self.assertEqual(help_text, "Enter the estate category")

    def test_description_help_text(self):
        help_text = self.estate._meta.get_field("description").help_text
        self.assertEqual(help_text, "Enter the estate description")

    def test_meta_ordering(self):
        self.assertEqual(Estate._meta.ordering, ("-id",))

    def test_str_representation(self):
        self.assertEqual(str(self.estate), f"{self.estate.address}: {self.estate.cost}")


class SaleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username="client_user",
            role="client",
            phone_number="+375(29)111-11-11",
            birth_date=date(1990, 1, 1),
            first_name="Client",
            last_name="User",
        )
        user2 = User.objects.create(
            username="employee_user",
            role="employee",
            phone_number="+375(29)222-22-22",
            birth_date=date(1990, 1, 1),
            first_name="Employee",
            last_name="User",
        )

        client = Client.objects.create(user=user1)
        employee = Employee.objects.create(user=user2)
        category = ServiceCategory.objects.create(name="Test Category")
        service = Service.objects.create(
            name="Test Service", category=category, cost=Decimal("100.00")
        )
        estate = Estate.objects.create(
            cost=Decimal("100000.00"),
            area=Decimal("50.00"),
            category=service,
            description="Test description",
            address="Test Address 123",
        )

        Sale.objects.create(
            client=client,
            employee=employee,
            estate=estate,
            category=service,
            service_cost=Decimal("100.00"),
            cost=Decimal("100100.00"),
        )

    def setUp(self):
        self.sale = Sale.objects.get(pk=1)

    def test_client_relation(self):
        self.assertEqual(self.sale.client.user.username, "client_user")

    def test_employee_relation(self):
        self.assertEqual(self.sale.employee.user.username, "employee_user")

    def test_estate_relation(self):
        self.assertEqual(self.sale.estate.address, "Test Address 123")

    def test_category_relation(self):
        self.assertEqual(self.sale.category.name, "Test Service")

    def test_save_method(self):
        # Test that save method calculates cost correctly
        new_sale = Sale(
            client=self.sale.client,
            employee=self.sale.employee,
            date_of_contract=date.today(),
            date_of_sale=date.today(),
            estate=self.sale.estate,
            category=self.sale.category,
        )
        new_sale.save()
        expected_cost = self.sale.estate.cost + self.sale.category.cost
        self.assertEqual(new_sale.cost, expected_cost)

    def test_str_representation(self):
        expected_str = (
            f"{self.sale.employee.user.username} - {self.sale.date_of_contract}"
        )
        self.assertEqual(str(self.sale), expected_str)


class PurchaseRequestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        user1 = User.objects.create(
            username="client_user",
            role="client",
            phone_number="+375(29)111-11-11",
            birth_date=date(1990, 1, 1),
            first_name="Client",
            last_name="User",
        )
        user2 = User.objects.create(
            username="employee_user",
            role="employee",
            phone_number="+375(29)222-22-22",
            birth_date=date(1990, 1, 1),
            first_name="Employee",
            last_name="User",
        )

        # Create related objects
        client = Client.objects.create(user=user1)
        employee = Employee.objects.create(user=user2)
        category = ServiceCategory.objects.create(name="Test Category")
        service = Service.objects.create(
            name="Test Service", category=category, cost=Decimal("100.00")
        )
        estate = Estate.objects.create(
            cost=Decimal("100000.00"),
            area=Decimal("50.00"),
            category=service,
            description="Test description",
            address="Test Address 123",
        )

        PurchaseRequest.objects.create(
            estate=estate,
            client=client,
            employee=employee,
            message="Test message",
            status="new",
        )

    def setUp(self):
        self.request = PurchaseRequest.objects.get(pk=1)

    def test_estate_relation(self):
        self.assertEqual(self.request.estate.address, "Test Address 123")

    def test_client_relation(self):
        self.assertEqual(self.request.client.user.username, "client_user")

    def test_employee_help_text(self):
        help_text = self.request._meta.get_field("employee").help_text
        self.assertEqual(help_text, "Employee for the purchase")

    def test_status_choices(self):
        choices = self.request._meta.get_field("status").choices
        expected_choices = [
            ("new", "New"),
            ("in_progress", "In progress"),
            ("completed", "Completed"),
        ]
        self.assertEqual(choices, expected_choices)

    def test_status_default(self):
        self.assertEqual(self.request.status, "new")

    def test_created_at_auto_now_add(self):
        auto_now_add = self.request._meta.get_field("created_at").auto_now_add
        self.assertTrue(auto_now_add)

    def test_meta_unique_together(self):
        unique_together = self.request._meta.unique_together
        self.assertEqual(unique_together, ("estate", "client"))

    def test_str_representation(self):
        expected_str = f"{self.request.estate} - {self.request.client.user.username}"
        self.assertEqual(str(self.request), expected_str)


class PurchaseRequestManagerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        user1 = User.objects.create(
            username="client_user",
            role="client",
            phone_number="+375(29)111-11-11",
            birth_date=date(1990, 1, 1),
            first_name="Client",
            last_name="User",
        )
        user2 = User.objects.create(
            username="employee1",
            role="employee",
            phone_number="+375(29)222-22-22",
            birth_date=date(1990, 1, 1),
            first_name="Employee1",
            last_name="User",
        )
        user3 = User.objects.create(
            username="employee2",
            role="employee",
            phone_number="+375(29)333-33-33",
            birth_date=date(1990, 1, 1),
            first_name="Employee2",
            last_name="User",
        )

        # Create related objects
        cls.client = Client.objects.create(user=user1)
        cls.employee1 = Employee.objects.create(user=user2)
        cls.employee2 = Employee.objects.create(user=user3)
        category = ServiceCategory.objects.create(name="Test Category")
        service = Service.objects.create(
            name="Test Service", category=category, cost=Decimal("100.00")
        )
        cls.estate = Estate.objects.create(
            cost=Decimal("100000.00"),
            area=Decimal("50.00"),
            category=service,
            description="Test description",
            address="Test Address 123",
        )

    def test_create_with_assignment(self):
        # First request should be assigned to employee1
        request1 = PurchaseRequest.objects.create_with_assignment(
            estate=self.estate, client=self.client, message="Test message 1"
        )
        self.assertEqual(request1.employee, self.employee1)

        # Second request should be assigned to employee2 (since employee1 already has one)
        request2 = PurchaseRequest.objects.create_with_assignment(
            estate=self.estate, client=self.client, message="Test message 2"
        )
        self.assertEqual(request2.employee, self.employee2)

    def test_create_with_assignment_no_employees(self):
        # Delete all employees first
        Employee.objects.all().delete()

        with self.assertRaises(ValueError):
            PurchaseRequest.objects.create_with_assignment(
                estate=self.estate, client=self.client, message="Test message"
            )



