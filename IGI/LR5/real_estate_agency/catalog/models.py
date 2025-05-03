from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Model representing an estate category (e.g. Land plot, Commercial estate).
    """

    name = models.CharField(max_length=200, help_text="Enter the estate category name")

    def __str__(self):
        return self.name


class Estate(models.Model):
    cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        help_text="Enter the estate cost",
        validators=[MinValueValidator(0.01)],
    )
    area = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        help_text="Enter the estate area",
        validators=[MinValueValidator(0.01)],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Enter the estate category",
    )
    description = models.TextField(
        max_length=2000, help_text="Enter the estate description"
    )
    address = models.CharField(max_length=200)
    owner = models.ManyToManyField("Owner", blank=True)

    class Meta:
        ordering = ("-cost",)

    def __str__(self):
        return f"{self.address}: {self.cost}"

    def get_absolute_url(self):
        return reverse("estate-detail", args=[str(self.pk)])


class Owner(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the owner name")

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the buyer name")
    email = models.EmailField(max_length=200, help_text="Enter the buyer email")
    phone_number = models.CharField(
        max_length=11, help_text="Enter the buyer phone number"
    )

    GENDERS = (
        ("m", "Male"),
        ("f", "Female"),
        ("o", "Other"),
    )

    gender = models.CharField(
        max_length=10, choices=GENDERS, help_text="Enter the buyer gender"
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the employee name")
    email = models.EmailField(
        max_length=200, help_text="Enter the employee email", default="<EMAIL>"
    )

    def __str__(self):
        return self.name


class Sale(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date_of_contract = models.DateField()
    date_of_sale = models.DateField()
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.name} - {self.date_of_contract}"
