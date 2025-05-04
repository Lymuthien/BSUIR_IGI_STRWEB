from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, restrict_age

class ClientSignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        validators=[User.phone_regex],
        help_text="Format: +375(29)XXX-XX-XX"
    )
    birth_date = forms.DateField(
        validators=[restrict_age],
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="You must be at least 18 years old."
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "birth_date", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.ROLE_CHOICES["client"]
        if commit:
            user.phone_number = self.cleaned_data['phone_number']
            user.birth_date = self.cleaned_data['birth_date']
            user.save()
        return user

