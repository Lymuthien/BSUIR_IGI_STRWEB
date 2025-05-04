from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def restrict_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("User must be at least 18 years old.")


class User(AbstractUser):
    ROLE_CHOICES = {
        "employee": "Manager",
        "client": "Client",
        "admin": "Admin",
    }

    phone_regex = RegexValidator(
        regex=r'^\+375\(29\)\d{3}-\d{2}-\d{2}$',
        message="Phone number must be +375(29)XXX-XX-XX"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, validators=[phone_regex])
    birth_date = models.DateField(validators=[restrict_age])

    def __str__(self):
        return f"{self.username} {self.role}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateField(null=True, blank=True)
    clients = models.ManyToManyField(Client, blank=True)

    def __str__(self):
        return f"{self.user.username}"
