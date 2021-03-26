from django.forms import ModelForm
from django import forms
from .models import Contract


class ContractBetaForm(forms.Form):
    GEEKS_CHOICES = (
        ("1", "Договор"),
    )
    type = forms.ChoiceField(choices=GEEKS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}))
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control', 'type':'text', 'rows':'4'}))



class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('comment', 'date', 'contract_name')