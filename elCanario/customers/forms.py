from django import forms
from customers.models import Customer
class TuFormulario(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'dni', 'phone_number', 'address', 'email']