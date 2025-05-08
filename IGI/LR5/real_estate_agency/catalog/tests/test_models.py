from django.core.validators import MinValueValidator
from django.test import TestCase
from decimal import Decimal
from datetime import date
from users.models import User, Employee, Client
from ..models import (
    Estate,
    ServiceCategory,
    Service,
    Sale,
    PurchaseRequest,
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
        employee = Employee.objects.create(user=user2, hire_date=date(2010, 1, 1))
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

        s = Sale.objects.create(
            client=client,
            employee=employee,
            estate=estate,
        )
        s.save()

    def setUp(self):
        self.sale = Sale.objects.get(pk=1)

    def test_client_label(self):
        field_label = self.sale._meta.get_field("client").verbose_name
        self.assertEqual(field_label, "client")

    def test_employee_label(self):
        field_label = self.sale._meta.get_field("employee").verbose_name
        self.assertEqual(field_label, "employee")

    def test_date_of_contract_label(self):
        field_label = self.sale._meta.get_field("date_of_contract").verbose_name
        self.assertEqual(field_label, "date of contract")

    def test_date_of_sale_label(self):
        field_label = self.sale._meta.get_field("date_of_sale").verbose_name
        self.assertEqual(field_label, "date of sale")

    def test_estate_label(self):
        field_label = self.sale._meta.get_field("estate").verbose_name
        self.assertEqual(field_label, "estate")

    def test_cost_label(self):
        field_label = self.sale._meta.get_field("cost").verbose_name
        self.assertEqual(field_label, "cost")

    def test_client_relation(self):
        self.assertEqual(self.sale.client.user.username, "client_user")

    def test_employee_relation(self):
        self.assertEqual(self.sale.employee.user.username, "employee_user")

    def test_estate_relation(self):
        self.assertEqual(self.sale.estate.address, "Test Address 123")

    def test_str_representation(self):
        expected_str = (
            f"{self.sale.employee.user.username} - {self.sale.date_of_contract}"
        )
        self.assertEqual(str(self.sale), expected_str)


class PurchaseRequestModelTest(TestCase):
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
        employee = Employee.objects.create(user=user2, hire_date=date(2010, 1, 1))
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
        )

    def setUp(self):
        self.request = PurchaseRequest.objects.get(pk=1)

    def test_estate_label(self):
        field_label = self.request._meta.get_field("estate").verbose_name
        self.assertEqual(field_label, "estate")

    def test_employee_label(self):
        field_label = self.request._meta.get_field("employee").verbose_name
        self.assertEqual(field_label, "employee")

    def test_client_label(self):
        field_label = self.request._meta.get_field("client").verbose_name
        self.assertEqual(field_label, "client")

    def test_message_label(self):
        field_label = self.request._meta.get_field("message").verbose_name
        self.assertEqual(field_label, "message")

    def test_created_at_label(self):
        field_label = self.request._meta.get_field("created_at").verbose_name
        self.assertEqual(field_label, "created at")

    def test_status_label(self):
        field_label = self.request._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_status_max_length(self):
        max_length = self.request._meta.get_field("status").max_length
        self.assertEqual(max_length, 20)

    def test_estate_relation(self):
        self.assertEqual(self.request.estate.address, "Test Address 123")

    def test_client_relation(self):
        self.assertEqual(self.request.client.user.username, "client_user")

    def test_status_choices(self):
        choices = self.request._meta.get_field("status").choices
        self.assertEqual(choices, PurchaseRequest.STATUS_CHOICES)

    def test_status_default(self):
        self.assertEqual(self.request.status, "new")

    def test_meta_unique_together(self):
        unique_together = self.request._meta.unique_together
        self.assertEqual(unique_together, (("estate", "client"),))

    def test_str_representation(self):
        expected_str = f"{self.request.estate} - {self.request.client.user.username}"
        self.assertEqual(str(self.request), expected_str)

