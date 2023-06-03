from django import forms
from .models import Comensal

class ComensalForm(forms.ModelForm):
    class Meta:
        model = Comensal
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control py-2',
                'placeholder': 'Escribe tu nombre',
            })
        }