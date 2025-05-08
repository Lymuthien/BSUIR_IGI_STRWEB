from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
import logging
from .utils import RestrictedAgeValidator

logger = logging.getLogger(__name__)


def restrict_age(birth_date):
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    logger.debug(f"Validating age for birth_date {birth_date}: calculated age {age}")
    if age < 18:
        logger.error(f"Age validation failed: User is under 18 (age {age})")
        raise ValidationError("Пользователь должен достигнуть 18 лет.")
    logger.info(f"Age validation passed for birth_date {birth_date}")


class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Profile"


class User(AbstractUser):
    ROLE_CHOICES = {
        "employee": "Manager",
        "client": "Client",
        "admin": "Admin",
    }

    phone_regex = RegexValidator(
        regex=r"^\+375\(29\)\d{3}-\d{2}-\d{2}$",
        message="Формат номера: +375(29)XXX-XX-XX",
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, validators=[phone_regex])
    birth_date = models.DateField(
        validators=[RestrictedAgeValidator(18), MaxValueValidator(date.today())]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self)

    def __str__(self):
        return f"{self.username} {self.role}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_place = models.CharField(
        max_length=100, blank=True, null=True, default="Nowhere"
    )

    def __str__(self):
        return f"{self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateField(null=True, blank=True)
    clients = models.ManyToManyField(Client, blank=True)

    def __str__(self):
        return f"{self.user.username}"
