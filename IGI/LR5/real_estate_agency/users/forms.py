import logging
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator

from .models import User, Client
from .utils import RestrictedAgeValidator

logger = logging.getLogger(__name__)


class ClientSignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        validators=[User.phone_regex],
        help_text="Format: +375(29)XXX-XX-XX",
    )
    birth_date = forms.DateField(
        validators=[RestrictedAgeValidator(18), MaxValueValidator(date.today())],
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="User must be at least 18 y.o.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "birth_date",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        logger.debug(
            f"Preparing to save user with username: {self.cleaned_data.get('username')}"
        )
        try:
            user = super().save(commit=False)
            user.role = "client"
            user.last_name = self.cleaned_data["last_name"]
            if commit:
                user.save()
                logger.info(f"User saved: {user.username}, role: {user.role}")
                Client.objects.create(user=user)
                logger.info(f"Client created for user: {user.username}")
            return user
        except Exception:
            logger.exception(
                f"Error saving user {self.cleaned_data.get('username')} or creating Client:"
            )
            raise
