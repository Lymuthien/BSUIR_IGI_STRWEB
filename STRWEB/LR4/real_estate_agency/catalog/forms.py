from django import forms
import logging


from .models import PurchaseRequest

logger = logging.getLogger(__name__)

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
