from datetime import datetime

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages
from ..views import (
    ServiceListView,
    AvailableEstateListView,
    EstateDetailView,
    ClientDashboardView,
    EmployeeDashboardView,
)
from ..models import Service, ServiceCategory, Estate, Sale, PurchaseRequest
from users.models import Client, Employee, User

class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            first_name="client",
            last_name="Test",
            role="client",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="client",
            password="testpass",
        )
        Client.objects.create(user=user1)
        employee_user = User.objects.create_user(
            first_name="employee",
            last_name="Test",
            role="employee",
            phone_number="+375(29)777-77-77",
            birth_date=datetime(2000, 1, 1),
            username="employee",
            password="testpass",
        )
        Employee.objects.create(user=employee_user, hire_date=datetime(2000, 1, 1))
        service_category = ServiceCategory.objects.create(name='Category1')
        Service.objects.create(name='Service1', cost=100, category=service_category)
        estate_category = Service.objects.create(name='EstateService', cost=500, category=service_category)
        Estate.objects.create(
            address='123 Test St',
            cost=100000,
            area=100,
            description='Test Estate',
            category=estate_category
        )

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='client')
        self.client_user = Client.objects.get(user=self.user)
        self.employee_user = User.objects.get(username="employee")
        self.employee = Employee.objects.get(user=self.employee_user)
        self.service_category = ServiceCategory.objects.get(name='Category1')
        self.service = Service.objects.get(name='Service1')
        self.estate_category = Service.objects.get(name='EstateService')
        self.estate = Estate.objects.get(address='123 Test St')

    def login(self, username='client', password='testpass'):
        self.client.login(username=username, password=password)

class ServiceListViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_get_queryset_filter_price(self):
        request = self.factory.get(reverse('services'), {'min_price': 50, 'max_price': 150})
        view = ServiceListView.as_view()
        response = view(request)
        self.assertEqual(list(response.context_data['object_list']), [self.service])

    def test_get_context_data(self):
        request = self.factory.get(reverse('services'))
        view = ServiceListView.as_view()
        response = view(request)
        self.assertIn('service_categories', response.context_data)
        self.assertEqual(list(response.context_data['service_categories']), [self.service_category])


class AvailableEstateListViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_get_queryset_no_filters(self):
        self.login()
        request = self.factory.get(reverse('estates'))
        request.user = self.user
        view = AvailableEstateListView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context_data['object_list']), [self.estate])

    def test_get_queryset_search(self):
        self.login()
        request = self.factory.get(reverse('estates'), {'search': 'Test St'})
        request.user = self.user
        view = AvailableEstateListView.as_view()
        response = view(request)
        self.assertEqual(list(response.context_data['object_list']), [self.estate])

    def test_get_queryset_filter_category(self):
        self.login()
        request = self.factory.get(reverse('estates'), {'category': self.estate_category.id})
        request.user = self.user
        view = AvailableEstateListView.as_view()
        response = view(request)
        self.assertEqual(list(response.context_data['object_list']), [self.estate])

    def test_get_queryset_sort(self):
        self.login()
        request = self.factory.get(reverse('estates'), {'sort': 'price_asc'})
        request.user = self.user
        view = AvailableEstateListView.as_view()
        response = view(request)
        self.assertEqual(list(response.context_data['object_list']), [self.estate])

    def test_get_context_data(self):
        self.login()
        request = self.factory.get(reverse('estates'))
        request.user = self.user
        view = AvailableEstateListView.as_view()
        response = view(request)
        self.assertIn('categories', response.context_data)
        self.assertIn('service_categories', response.context_data)
        self.assertEqual(response.context_data['search_query'], '')
        self.assertIsNone(response.context_data['current_sort'])

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('estates'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class EstateDetailViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_get_context_data_unauthenticated(self):
        response = self.client.get(reverse('estate_detail', kwargs={'pk': self.estate.id}))
        self.assertEqual(response.status_code, 302)

    def test_request_exists(self):
        self.login()
        PurchaseRequest.objects.create(client=self.client_user, estate=self.estate, status='new')
        request = self.factory.get(reverse('estate_detail', kwargs={'pk': self.estate.id}))
        request.user = self.user
        view = EstateDetailView.as_view()
        response = view(request, pk=self.estate.id)
        self.assertTrue(response.context_data['request_exists'])


class CreatePurchaseRequestViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_form_valid(self):
        self.login()
        form_data = {'message': 'Interested in this estate'}
        response = self.client.post(
            reverse('create_request', kwargs={'pk': self.estate.id}),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PurchaseRequest.objects.filter(client=self.client_user, estate=self.estate).exists())

    def test_duplicate_purchase_request(self):
        self.login()
        PurchaseRequest.objects.create(client=self.client_user, estate=self.estate, status='new')
        form_data = {'message': 'Another request'}
        response = self.client.post(
            reverse('create_request', kwargs={'pk': self.estate.id}),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PurchaseRequest.objects.filter(client=self.client_user, estate=self.estate).count(), 1)

    def test_unauthenticated_access(self):
        response = self.client.post(reverse('create_request', kwargs={'pk': self.estate.id}))
        self.assertEqual(response.status_code, 302)


class ClientDashboardViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_get_context_data(self):
        self.login()
        PurchaseRequest.objects.create(client=self.client_user, estate=self.estate, status='new')
        Sale.objects.create(client=self.client_user, estate=self.estate, employee=self.employee)
        request = self.factory.get(reverse('client_dashboard'))
        request.user = self.user
        view = ClientDashboardView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['requests']), 1)
        self.assertEqual(len(response.context_data['sales']), 1)

    def test_post_buy_action(self):
        self.login()
        purchase_request = PurchaseRequest.objects.create(
            client=self.client_user, estate=self.estate, status='new', employee=self.employee
        )
        response = self.client.post(
            reverse('client_dashboard'),
            {'action': 'buy', 'request_id': purchase_request.id}
        )
        self.assertEqual(response.status_code, 302)
        purchase_request.refresh_from_db()
        self.assertEqual(purchase_request.status, 'completed')
        self.assertTrue(Sale.objects.filter(client=self.client_user, estate=self.estate).exists())

    def test_post_cancel_action(self):
        self.login()
        purchase_request = PurchaseRequest.objects.create(
            client=self.client_user, estate=self.estate, status='new'
        )
        response = self.client.post(
            reverse('client_dashboard'),
            {'action': 'cancel', 'request_id': purchase_request.id}
        )
        self.assertEqual(response.status_code, 302)
        purchase_request.refresh_from_db()
        self.assertEqual(purchase_request.status, 'completed')

    def test_post_invalid_request_id(self):
        self.login()
        response = self.client.post(
            reverse('client_dashboard'),
            {'action': 'buy', 'request_id': 999}
        )
        self.assertEqual(response.status_code, 404)


class EmployeeDashboardViewTests(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def setUp(self):
        super().setUp()

    def test_get_context_data(self):
        self.client.login(username='employee', password='testpass')
        PurchaseRequest.objects.create(
            client=self.client_user, estate=self.estate, employee=self.employee, status='new'
        )
        Sale.objects.create(
            client=self.client_user, estate=self.estate, employee=self.employee
        )
        request = self.factory.get(reverse('employee_dashboard'))
        request.user = self.employee_user
        view = EmployeeDashboardView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['clients']), 1)
        self.assertEqual(len(response.context_data['requests']), 1)
        self.assertEqual(len(response.context_data['sales']), 1)

    def test_no_employee(self):
        self.login()
        response = self.client.get(reverse('employee_dashboard'))
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You must be employee.')

