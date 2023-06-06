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

class HeladoForm(forms.Form):
    OPTIONS = (
        ("VAN", "Vainilla"),
        ("CHO", "Chocolate"),
        ("STR", "Fresa"),
    )
    flavours = forms.MultipleChoiceField(choices = OPTIONS, widget=forms.CheckboxSelectMultiple)