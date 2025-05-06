from django import forms
from .models import PurchaseRequest

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['message']
        labels = {
            'message': ''
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ваши пожелания и вопросы...'
            }),
        }