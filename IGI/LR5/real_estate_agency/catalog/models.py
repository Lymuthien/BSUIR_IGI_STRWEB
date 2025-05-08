from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.conf import settings
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
    image = models.ImageField(blank=True, null=True, upload_to="estates/")
    address = models.CharField(max_length=200)

    def get_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return settings.MEDIA_URL + "image_placeholder.jpg"

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
        on_delete=models.CASCADE,
        related_name="services",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"({str(self.category)[:2]}) - {self.name}"


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date_of_contract = models.DateField(auto_now_add=True)
    date_of_sale = models.DateField(auto_now_add=True)
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, auto_created=True)

    def save(self, *args, **kwargs):
        service_cost = 0
        if self.estate.category:
            service_cost = self.estate.category.cost

        self.cost = service_cost + self.estate.cost

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date_of_contract}"


class PurchaseRequestManager(models.Manager):
    def create_with_assignment(self, **kwargs):
        active_statuses = ["new", "in_progress"]
        employee = (
            Employee.objects.annotate(
                request_count=Count(
                    "purchaserequest",
                    filter=models.Q(purchaserequest__status__in=active_statuses),
                )
            )
            .order_by("request_count")
            .first()
        )

        if employee:
            kwargs["employee"] = employee
        else:
            raise ValueError("Employee does not exist.")

        return self.create(**kwargs)


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    objects = PurchaseRequestManager()

    class Meta:
        unique_together = ["estate", "client"]

    def __str__(self):
        return f"{self.estate} - {self.client.user.username}"
