import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from real_estate_agency import settings


class AboutCompany(models.Model):
    text = models.TextField(help_text="Enter the company text")

    def __str__(self):
        return f"{self.text[:40]}..."


class News(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()
    added_date = models.DateField()

    def __str__(self):
        return self.question


class Contact(models.Model):
    name = models.CharField(max_length=100, default="")
    position = models.CharField(max_length=100, default="")
    photo = models.ImageField(upload_to='media/')
    description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def clean(self):
        try:
            phone_number = phonenumbers.parse(self.phone, 'BY')
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Invalid phone number")
            self.phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise ValidationError("Valid +375 (29) XXX-XX-XX")

    def __str__(self):
        return self.name


class Policy(models.Model):
    pass


class Vacancy(models.Model):
    position = models.CharField(max_length=100, default="")
    salary = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.position


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    text = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:40]}..."


class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    description = models.TextField(default="")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.code

