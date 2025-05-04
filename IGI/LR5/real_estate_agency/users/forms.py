from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, restrict_age, Client


class ClientSignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        validators=[User.phone_regex],
        help_text="Format: +375(29)XXX-XX-XX"
    )
    birth_date = forms.DateField(
        validators=[restrict_age],
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Пользователь должен достигнуть 18 лет."
    )

    class Meta:
        model = User
        fields = (
        "username", "email", "phone_number", "birth_date", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "client"
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            Client.objects.create(user=user)
        return user

