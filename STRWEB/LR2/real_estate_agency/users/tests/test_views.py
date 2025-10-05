import datetime

from django.test import TestCase
from django.urls import reverse
from home.models import Review
from ..models import Client, User, Profile
from ..forms import ClientSignUpForm
import logging



class SignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/accounts/signup/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "signup.html")

    def test_signup_form_in_context(self):
        resp = self.client.get(reverse("signup"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("form" in resp.context)
        self.assertIsInstance(resp.context["form"], ClientSignUpForm)

    def test_successful_signup_redirects_to_home(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "phone_number": "+375(29)123-45-67",
            "birth_date": "1990-01-01",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        resp = self.client.post(reverse("signup"), data=form_data)
        self.assertRedirects(resp, reverse("home"))

    def test_successful_signup_creates_user_and_client(self):
        user_count = User.objects.count()
        client_count = Client.objects.count()

        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "phone_number": "+375(29)123-45-67",
            "birth_date": "1990-01-01",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "Test",
            "last_name": "User",
        }
        self.client.post(reverse("signup"), data=form_data)

        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(Client.objects.count(), client_count + 1)

        new_user = User.objects.last()
        self.assertTrue(Client.objects.filter(user=new_user).exists())

    def test_invalid_signup_does_not_create_user(self):
        user_count = User.objects.count()
        client_count = Client.objects.count()

        form_data = {
            "username": "",
            "email": "invalid-email",
            "password1": "short",
            "password2": "mismatch",
        }
        resp = self.client.post(reverse("signup"), data=form_data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(Client.objects.count(), client_count)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            password='test123',
            email="test@example.com",
            phone_number="+375(29)123-45-67",
            birth_date=datetime.date(1990,1,1),
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        for i in range(5):
            Review.objects.create(
                user=self.user,
                text=f'Test review {i}',
                rating=5,
            )

        self.client_obj = Client.objects.create(user=self.user)
        self.profile = Profile.objects.get(pk=1)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('profile', kwargs={'pk': self.user.pk}))
        self.assertRedirects(
            resp,
            f'/accounts/login/?next=/accounts/profile/{self.profile.pk}'
        )
