from django import forms
from customers.models import Customer
class TuFormulario(forms.ModelForm):
    class Meta:
        trigger = {'hx-trigger':'keyup changed delay:300ms'}
        model = Customer
        fields = ['name', 'dni', 'phone_number', 'address', 'email']
        widgets = {
            'name': forms.TextInput(attrs=trigger),
            'dni': forms.TextInput(attrs=trigger),
            'phone_number': forms.TextInput(attrs=trigger),
            'address': forms.TextInput(attrs=trigger),
            'email': forms.EmailInput(attrs=trigger)
        }