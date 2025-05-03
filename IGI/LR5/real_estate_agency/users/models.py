from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("employee", "Manager"),
        ("manager", "Client"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=11, help_text="Enter phone number")
    birth_date = models.DateField(null=True, blank=True)

    # GENDERS = (
    #     ("m", "Male"),
    #     ("f", "Female"),
    #     ("o", "Other"),
    # )
    #
    # gender = models.CharField(
    #     max_length=10, choices=GENDERS, help_text="Enter the client gender"
    # )

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
