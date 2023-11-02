from django import forms
from customers.models import Customer
from django.utils.translation import gettext_lazy as _
class CustomerForm(forms.ModelForm):

    class Meta:
        style_input = "input w-full"
        model = Customer
        fields = ['name', 'dni', 'phone_number', 'address', 'email']
        widgets = {
            'name': forms.TextInput(attrs={"class":style_input, "placeholder":_("Name")}),
            'dni': forms.TextInput(attrs={"class":style_input, "placeholder":_("Dni")}),
            'phone_number': forms.TextInput(attrs={"class":style_input, "placeholder":_("Phone number")}),
            'address': forms.TextInput(attrs={"class":style_input, "placeholder":_("Address")}),
            'email': forms.EmailInput(attrs={"class":style_input, "placeholder":_("Email")})
        }
        labels = {
            'name': _('Name'),
            'dni': _('Dni'),
            'phone_number': _('Phone number'),
            'address': _('Address'),
            'email': _('Email')
        }