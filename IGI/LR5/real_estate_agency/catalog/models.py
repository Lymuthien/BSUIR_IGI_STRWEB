from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from real_estate_agency import settings
from users.models import Employee, Client


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
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Enter the estate category",
    )
    description = models.TextField(
        max_length=2000, help_text="Enter the estate description"
    )
    image = models.ImageField(blank=True, null=True, upload_to="media/")
    address = models.CharField(max_length=200)
    owner = models.ManyToManyField(Client, blank=True)

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return "/media/image_placeholder.jpg"

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.address}: {self.cost}"

    def get_absolute_url(self):
        return reverse("estate-detail", args=[str(self.pk)])


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the service category name")

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the estate category name")
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.category} - {self.name}"


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date_of_contract = models.DateField()
    date_of_sale = models.DateField()
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)
    category = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.service_cost is None and self.category:
            self.service_cost = self.category.cost

        self.cost = self.service_cost + self.estate.cost

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date_of_contract}"


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
