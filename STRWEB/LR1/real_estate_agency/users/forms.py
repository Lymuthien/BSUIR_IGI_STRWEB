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

class AdminEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'is_active']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'username': 'Уникальное имя пользователя для входа в систему',
            'birth_date': 'Дата рождения сотрудника',
            'is_active': 'Разрешить пользователю вход в систему',
        }

class AdminClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'is_active': 'Разрешить клиенту вход в систему и совершение покупок',
        }